from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.bz_q_sequence import compute_q_term_from_a, totally_symmetric_a_vector
from zeta5_autoresearch.bz_symmetric_recurrence_probe import (
    build_bz_totally_symmetric_recurrence_probe,
    render_bz_totally_symmetric_recurrence_report,
    write_bz_totally_symmetric_recurrence_report,
)
from zeta5_autoresearch.gate0_parse import parse_candidate_file
from zeta5_autoresearch.gate2.recurrence_eval import generate_terms_from_recurrence, recurrence_residuals
from zeta5_autoresearch.sequence_evidence import load_sequence_evidence_by_id, resolve_candidate_sequence_evidence


REPO_ROOT = Path(__file__).resolve().parents[1]
SYMMETRIC_PATH = REPO_ROOT / "specs" / "totally_symmetric_bz_seed.yaml"


def test_totally_symmetric_q_matches_paper_initial_values() -> None:
    a = totally_symmetric_a_vector()

    assert compute_q_term_from_a(a, 0) == 1
    assert compute_q_term_from_a(a, 1) == 21
    assert compute_q_term_from_a(a, 2) == 2989


def test_totally_symmetric_recurrence_matches_exact_formula_terms() -> None:
    evidence = load_sequence_evidence_by_id("bz_totally_symmetric_q_recurrence_v1")
    assert evidence.recurrence is not None

    recurrence_terms = generate_terms_from_recurrence(evidence.recurrence, max_index=10)
    direct_terms = {
        n: compute_q_term_from_a(totally_symmetric_a_vector(), n)
        for n in range(12)
    }
    residuals = recurrence_residuals(
        evidence.recurrence,
        values_by_index={n: value for n, value in direct_terms.items()},
        end_n=10,
    )

    assert tuple(int(value) for value in recurrence_terms) == tuple(direct_terms[n] for n in range(11))
    assert all(item.vanishes for item in residuals)


def test_totally_symmetric_candidate_binds_verified_sequence_hash() -> None:
    candidate = parse_candidate_file(SYMMETRIC_PATH)
    bound, evidence = resolve_candidate_sequence_evidence(candidate)

    assert evidence is not None
    assert evidence.id == "bz_totally_symmetric_q_recurrence_v1"
    assert evidence.sequence_hash_status == "verified"
    assert bound.sequence_hash is not None
    assert bound.certificate_hash is not None
    assert len(bound.sequence_hash) == 64
    assert len(bound.certificate_hash) == 64


def test_totally_symmetric_probe_renders_and_writes(tmp_path: Path) -> None:
    probe = build_bz_totally_symmetric_recurrence_probe(max_n=10)
    report = render_bz_totally_symmetric_recurrence_report(max_n=10)

    assert probe.all_exact_matches is True
    assert probe.all_residuals_zero is True
    assert "verified sequence-identity anchor" in report

    output = write_bz_totally_symmetric_recurrence_report(max_n=10, output_path=tmp_path / "anchor.md")
    contents = output.read_text(encoding="utf-8")

    assert output.exists()
    assert "Sequence hash status: `verified`" in contents
