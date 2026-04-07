from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from pathlib import Path

import yaml

from zeta5_autoresearch.gate0_parse import parse_candidate_file, run_gate0
from zeta5_autoresearch.gate1_filter import run_gate1
from zeta5_autoresearch.hashes import compute_routing_hash
from zeta5_autoresearch.models import AffineFamily
from zeta5_autoresearch.translate import a_to_s, s_to_a


REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = REPO_ROOT / "specs" / "baseline_bz_seed.yaml"


def load_raw_baseline() -> dict:
    return yaml.safe_load(BASELINE_PATH.read_text(encoding="utf-8"))


def test_a_to_s_roundtrip_matches_bz_baseline() -> None:
    a = tuple(Fraction(value) for value in (8, 16, 10, 15, 12, 16, 18, 13))
    expected_s = tuple(
        Fraction(value)
        for value in ("41/2", "7/2", "9/2", "11/2", "13/2", "15/2", "17/2", "19/2")
    )
    assert a_to_s(a) == expected_s
    assert s_to_a(expected_s) == a


def test_baseline_seed_passes_gate0_and_gate1() -> None:
    gate0 = run_gate0(BASELINE_PATH)
    gate1 = run_gate1(gate0)

    assert gate0.candidate.routing_hash
    assert len(gate0.candidate.routing_hash) == 64
    assert gate1.accepted
    assert gate1.errors == ()


def test_joint_canonicalization_stabilizes_routing_hash(tmp_path: Path) -> None:
    raw = load_raw_baseline()
    permuted = deepcopy(raw)

    tail_permutation = [3, 5, 1, 7, 2, 6, 4]
    u_tail = [raw["construction"]["affine_family"]["u"][index] for index in tail_permutation]
    v_tail = [raw["construction"]["affine_family"]["v"][index] for index in tail_permutation]
    permuted["construction"]["affine_family"]["u"] = [raw["construction"]["affine_family"]["u"][0], *u_tail]
    permuted["construction"]["affine_family"]["v"] = [raw["construction"]["affine_family"]["v"][0], *v_tail]

    permuted_path = tmp_path / "permuted.yaml"
    permuted_path.write_text(yaml.safe_dump(permuted, sort_keys=False), encoding="utf-8")

    baseline_gate0 = run_gate0(BASELINE_PATH)
    permuted_gate0 = run_gate0(permuted_path)

    assert permuted_gate0.canonicalized
    assert permuted_gate0.candidate.affine_family == baseline_gate0.candidate.affine_family
    assert permuted_gate0.candidate.routing_hash == baseline_gate0.candidate.routing_hash


def test_gate1_rejects_invalid_parity(tmp_path: Path) -> None:
    raw = load_raw_baseline()
    raw["construction"]["affine_family"]["u"][1] = "4/3"

    candidate_path = tmp_path / "bad_parity.yaml"
    candidate_path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")

    result = run_gate1(run_gate0(candidate_path))
    assert not result.accepted
    assert any("not integral" in failure for failure in result.parity.failures)


def test_gate1_rejects_invalid_convergence(tmp_path: Path) -> None:
    raw = load_raw_baseline()
    raw["construction"]["affine_family"]["u"][0] = "1/2"

    candidate_path = tmp_path / "bad_convergence.yaml"
    candidate_path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")

    result = run_gate1(run_gate0(candidate_path))
    assert not result.accepted
    assert any("negative slope" in failure or "negative at n=1" in failure for failure in result.convergence.failures)


def test_routing_hash_changes_on_representation_change() -> None:
    candidate = parse_candidate_file(BASELINE_PATH)
    first_hash = compute_routing_hash(candidate.to_routing_payload())

    mutated = candidate.with_affine_family(AffineFamily(u=candidate.affine_family.u, v=candidate.affine_family.v))
    mutated_payload = mutated.to_routing_payload()
    mutated_payload["representation"] = "very_well_poised_7F6"

    assert compute_routing_hash(mutated_payload) != first_hash
