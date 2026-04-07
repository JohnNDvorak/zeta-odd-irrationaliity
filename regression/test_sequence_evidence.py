from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.bz_q_sequence import baseline_a_vector, compute_q_signature_from_a
from zeta5_autoresearch.gate0_parse import parse_candidate_file
from zeta5_autoresearch.sequence_evidence import load_sequence_evidence_by_id, resolve_candidate_sequence_evidence


REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = REPO_ROOT / "specs" / "baseline_bz_seed.yaml"


def test_bz_baseline_q_signature_matches_formula() -> None:
    evidence = load_sequence_evidence_by_id("bz_baseline_q_signature_v1")
    computed = tuple(str(value) for value in compute_q_signature_from_a(baseline_a_vector(), term_count=8))

    assert evidence.signature == computed
    assert evidence.initial_data == computed[:3]


def test_baseline_candidate_binds_sequence_hash_from_evidence() -> None:
    candidate = parse_candidate_file(BASELINE_PATH)
    bound, evidence = resolve_candidate_sequence_evidence(candidate)

    assert evidence is not None
    assert evidence.id == "bz_baseline_q_signature_v1"
    assert evidence.sequence_hash_status == "provisional"
    assert bound.sequence_hash is not None
    assert bound.certificate_hash is not None
    assert len(bound.sequence_hash) == 64
    assert len(bound.certificate_hash) == 64
