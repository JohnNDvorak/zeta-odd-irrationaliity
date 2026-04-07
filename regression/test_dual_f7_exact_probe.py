from __future__ import annotations

from fractions import Fraction

from zeta5_autoresearch.bz_dual_f7 import displayed_series_to_hyper_line_ratio, evaluate_exact_f7_linear_form, evaluate_f7, extract_f7_linear_form


def test_exact_dual_f7_extractor_matches_symmetric_anchor() -> None:
    linear_form = extract_f7_linear_form((3, 1, 1, 1, 1, 1, 1, 1))

    assert linear_form.constant_term == Fraction(-98, 1)
    assert linear_form.zeta_coefficient(3) == Fraction(66, 1)
    assert linear_form.zeta_coefficient(5) == Fraction(18, 1)


def test_exact_dual_f7_value_matches_canonical_numeric_evaluation() -> None:
    for b in ((3, 1, 1, 1, 1, 1, 1, 1), (41, 17, 16, 15, 14, 13, 12, 11)):
        exact_value = evaluate_exact_f7_linear_form(extract_f7_linear_form(b), precision=100)
        numeric_value = evaluate_f7(b, precision=100)
        assert abs(exact_value - numeric_value) < 1e-70


def test_displayed_series_to_hyper_line_ratio_matches_b0_plus_2() -> None:
    assert displayed_series_to_hyper_line_ratio((3, 1, 1, 1, 1, 1, 1, 1)) == 5
    assert displayed_series_to_hyper_line_ratio((41, 17, 16, 15, 14, 13, 12, 11)) == 43
