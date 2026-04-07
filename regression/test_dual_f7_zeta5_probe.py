from __future__ import annotations

from zeta5_autoresearch.bz_dual_f7 import compute_f7_zeta5_signature_from_a, extract_f7_linear_form, extract_f7_zeta5_coefficient
from zeta5_autoresearch.bz_dual_f7_zeta5_probe import build_bz_dual_f7_zeta5_probe, render_bz_dual_f7_zeta5_probe_report
from zeta5_autoresearch.bz_q_sequence import baseline_a_vector, totally_symmetric_a_vector


def test_fast_zeta5_extractor_matches_exact_known_values() -> None:
    assert extract_f7_zeta5_coefficient((3, 1, 1, 1, 1, 1, 1, 1)) == 18
    assert extract_f7_zeta5_coefficient((6, 2, 2, 2, 2, 2, 2, 2)) == 938
    assert extract_f7_zeta5_coefficient((41, 17, 16, 15, 14, 13, 12, 11)) == extract_f7_linear_form((41, 17, 16, 15, 14, 13, 12, 11)).zeta_coefficient(5)
    assert extract_f7_zeta5_coefficient((82, 34, 32, 30, 28, 26, 24, 22)) == 152044985550430960231949449314536670627277608934680000


def test_zeta5_signatures_build_for_symmetric_and_baseline_cases() -> None:
    symmetric_signature = compute_f7_zeta5_signature_from_a(totally_symmetric_a_vector(), start_index=1, term_count=4)
    baseline_signature = compute_f7_zeta5_signature_from_a(baseline_a_vector(), start_index=1, term_count=4)

    assert symmetric_signature == (18, 938, 77202, 8017002)
    assert baseline_signature[0] == -17062318711073217087874368
    assert baseline_signature[1] == 152044985550430960231949449314536670627277608934680000


def test_dual_zeta5_probe_renders_sequence_hashes() -> None:
    probe = build_bz_dual_f7_zeta5_probe()
    baseline_case = next(case for case in probe.cases if case.id == "baseline_bz")

    assert len(baseline_case.samples) == 6
    assert baseline_case.samples[5].digits == 167

    report = render_bz_dual_f7_zeta5_probe_report()
    assert "Provisional sequence hash" in report
    assert "Brown-Zudilin baseline dual zeta(5) coefficient sequence" in report
