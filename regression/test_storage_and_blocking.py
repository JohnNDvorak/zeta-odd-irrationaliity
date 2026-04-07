from __future__ import annotations

from pathlib import Path

import pytest

from zeta5_autoresearch.gate0_parse import run_gate0
from zeta5_autoresearch.gate2.modeA_fast import run_mode_a_fast
from zeta5_autoresearch.gate2.modeA_slow import run_mode_a_slow
from zeta5_autoresearch.gate2.modeB import run_mode_b
from zeta5_autoresearch.gate3.certify import run_gate3
from zeta5_autoresearch.hashes import CertificateHashUnavailable, SequenceHashUnavailable, compute_certificate_hash, compute_sequence_hash
from zeta5_autoresearch.orchestrator import log_structural_run
from zeta5_autoresearch.sequence_evidence import resolve_candidate_sequence_evidence
from zeta5_autoresearch.storage.candidates import load_candidate_snapshot, save_candidate_snapshot
from zeta5_autoresearch.storage.results import append_result, initialize_results_store

REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = REPO_ROOT / "specs" / "baseline_bz_seed.yaml"


def test_results_store_initializes_and_appends(tmp_path: Path) -> None:
    results_path = tmp_path / "results.tsv"
    initialize_results_store(results_path)
    append_result(
        {
            "id": "demo",
            "timestamp": "2026-04-01T00:00:00Z",
            "configuration_label": "8pi8v",
            "family_label": "dual_of_8pi_odd",
            "routing_hash": "abc",
            "mode": "Mode A-fast",
            "u": ["41/2"] * 8,
            "v": ["0"] * 8,
            "gate_reached": "gate1",
            "notes": "smoke test",
        },
        results_path,
    )

    lines = results_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    assert lines[0].startswith("id\ttimestamp\tconfiguration_label")
    assert "smoke test" in lines[1]


def test_sequence_hash_requires_real_input() -> None:
    with pytest.raises(SequenceHashUnavailable):
        compute_sequence_hash()


def test_certificate_hash_requires_sequence_hash() -> None:
    with pytest.raises(CertificateHashUnavailable):
        compute_certificate_hash(
            sequence_hash=None,
            representation="cellular_dihedral",
            template="BZ_standard",
            nu_p_method="group_orbit_factorial_ratio",
        )


def test_mode_stubs_are_explicitly_blocked() -> None:
    for result in (run_mode_a_fast(), run_mode_a_slow(), run_mode_b()):
        assert not result.implemented
        assert "deferred" in result.reason or "blocked" in result.reason

    gate3 = run_gate3()
    assert not gate3.implemented
    assert "deferred" in gate3.reason


def test_candidate_snapshot_roundtrip(tmp_path: Path) -> None:
    gate0 = run_gate0(BASELINE_PATH)
    candidate, _ = resolve_candidate_sequence_evidence(gate0.candidate)
    snapshot_path = save_candidate_snapshot(candidate, root=tmp_path)
    snapshot = load_candidate_snapshot(snapshot_path)

    assert snapshot["routing_hash"] == candidate.routing_hash
    assert snapshot["configuration"]["label"] == "8pi8v"
    assert snapshot["snapshot_aliases"] == ["baseline_bz_8pi8v_seed"]
    assert snapshot["sequence_evidence_id"] == "bz_baseline_q_signature_v1"
    assert snapshot["sequence_hash"]


def test_candidate_snapshot_merges_aliases_without_clobbering_seed(tmp_path: Path) -> None:
    gate0 = run_gate0(BASELINE_PATH)
    base_candidate, _ = resolve_candidate_sequence_evidence(gate0.candidate)
    save_candidate_snapshot(base_candidate, root=tmp_path)

    campaign_variant = base_candidate.with_hashes(routing_hash=base_candidate.routing_hash)
    campaign_variant = type(base_candidate)(
        id="baseline_bz_8pi8v_seed__cellular_dihedral_bz_standard",
        routing_hash=campaign_variant.routing_hash,
        sequence_hash=campaign_variant.sequence_hash,
        certificate_hash=campaign_variant.certificate_hash,
        sequence_evidence_id=campaign_variant.sequence_evidence_id,
        configuration=campaign_variant.configuration,
        affine_family=campaign_variant.affine_family,
        extraction=campaign_variant.extraction,
        representation=campaign_variant.representation,
        certificate=campaign_variant.certificate,
        motive=campaign_variant.motive,
        hypothesis="Campaign alias",
        target_improvement=campaign_variant.target_improvement,
        mutation_from=campaign_variant.id,
        mutation_type="campaign_variant",
    )
    snapshot_path = save_candidate_snapshot(campaign_variant, root=tmp_path)
    snapshot = load_candidate_snapshot(snapshot_path)

    assert snapshot["id"] == "baseline_bz_8pi8v_seed"
    assert snapshot["mutation_type"] == "seed"
    assert snapshot["snapshot_aliases"] == [
        "baseline_bz_8pi8v_seed",
        "baseline_bz_8pi8v_seed__cellular_dihedral_bz_standard",
    ]
    assert len(snapshot["snapshot_variants"]) == 2


def test_structural_dry_run_logs_snapshot_and_result(tmp_path: Path) -> None:
    snapshot_root = tmp_path / "candidates"
    results_path = tmp_path / "results.tsv"
    logged = log_structural_run(
        candidate_path=BASELINE_PATH,
        mode="Mode A-fast",
        notes="baseline smoke",
        snapshot_root=snapshot_root,
        results_path=results_path,
    )

    snapshot_path = Path(logged["candidate_snapshot"])
    assert snapshot_path.exists()
    assert Path(logged["results_path"]).exists()
    contents = results_path.read_text(encoding="utf-8")
    assert "baseline smoke" in contents
    assert "bz_baseline_q_signature_v1" in contents
