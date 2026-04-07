from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from zeta5_autoresearch.bz_dual_f7 import dual_b_vector_from_a, evaluate_f7, search_f7_zeta_relation
from zeta5_autoresearch.bz_dual_f7_probe import build_bz_dual_f7_probe, render_bz_dual_f7_probe_report, write_bz_dual_f7_probe_report
from zeta5_autoresearch.bz_q_sequence import baseline_a_vector, totally_symmetric_a_vector


def test_dual_b_vector_matches_paper_examples() -> None:
    assert dual_b_vector_from_a(totally_symmetric_a_vector()) == (3, 1, 1, 1, 1, 1, 1, 1)
    assert dual_b_vector_from_a(baseline_a_vector()) == (41, 17, 16, 15, 14, 13, 12, 11)


def test_dual_f7_symmetric_pslq_relation_is_stable() -> None:
    value = evaluate_f7((3, 1, 1, 1, 1, 1, 1, 1), precision=120)
    relation = search_f7_zeta_relation(value, precision=180, maxcoeff=100000)

    assert relation is not None
    assert relation.coefficients == (98, -66, -18, 1)
    assert relation.constant_term == Fraction(-98, 1)
    assert relation.zeta3_coeff == Fraction(66, 1)
    assert relation.zeta5_coeff == Fraction(18, 1)


def test_dual_f7_probe_renders_and_baseline_stays_unresolved(tmp_path: Path) -> None:
    probe = build_bz_dual_f7_probe(precision=120, pslq_precision=180)
    baseline_case = next(case for case in probe.cases if case.id == "baseline_bz")

    assert baseline_case.base_b == (41, 17, 16, 15, 14, 13, 12, 11)
    assert baseline_case.samples[0].pslq_relation_text is None

    report = render_bz_dual_f7_probe_report(precision=120, pslq_precision=180)
    assert "dual F_7 probe" in report
    assert "no low-height relation found" in report

    output = write_bz_dual_f7_probe_report(
        precision=120,
        pslq_precision=180,
        output_path=tmp_path / "dual_f7.md",
    )
    contents = output.read_text(encoding="utf-8")

    assert output.exists()
    assert "uncertified numeric PSLQ witness" in contents
