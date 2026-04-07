from __future__ import annotations

from fractions import Fraction

import pytest

import zeta5_autoresearch.bz_dual_f7 as dual_f7


def _naive_harmonic_number(limit: int, weight: int) -> Fraction:
    return sum((Fraction(1, index**weight) for index in range(1, limit + 1)), start=Fraction(0))


def _naive_all_shift_sum(max_shift: int, shift: int, degree: int) -> Fraction:
    return sum(
        (Fraction(1, (index - shift) ** degree) for index in range(1, max_shift + 1) if index != shift),
        start=Fraction(0),
    )


def _naive_interval_sum(left: int, right: int, shift: int, degree: int) -> Fraction:
    return sum(
        (Fraction(1, (index - shift) ** degree) for index in range(left, right + 1) if index != shift),
        start=Fraction(0),
    )


def test_harmonic_number_kernel_matches_naive_small_windows() -> None:
    for weight in range(1, 6):
        for limit in (1, 2, 3, 5, 8, 12):
            assert dual_f7._harmonic_number(limit, weight) == _naive_harmonic_number(limit, weight)


def test_all_shift_reciprocal_power_sum_matches_naive_small_windows() -> None:
    for degree in range(1, 6):
        assert dual_f7._all_shift_reciprocal_power_sum(max_shift=9, shift=4, degree=degree) == _naive_all_shift_sum(9, 4, degree)
        assert dual_f7._all_shift_reciprocal_power_sum(max_shift=11, shift=1, degree=degree) == _naive_all_shift_sum(11, 1, degree)
        assert dual_f7._all_shift_reciprocal_power_sum(max_shift=11, shift=11, degree=degree) == _naive_all_shift_sum(11, 11, degree)


def test_interval_reciprocal_power_sum_matches_naive_small_windows() -> None:
    cases = (
        (3, 7, 1),
        (3, 7, 5),
        (3, 7, 10),
        (4, 9, 6),
    )
    for degree in range(1, 6):
        for left, right, shift in cases:
            assert dual_f7._interval_reciprocal_power_sum(left=left, right=right, shift=shift, degree=degree) == _naive_interval_sum(left, right, shift, degree)


def test_mpq_add_kernel_matches_fraction_for_coprime_denominators() -> None:
    left = Fraction(10**40 + 123, 2**31 - 1)
    right = Fraction(-(10**38) + 77, 2**19 - 1)

    assert dual_f7._add_fraction_pair(left, right) == left + right


def test_factorial_prime_exponents_match_small_factorials() -> None:
    assert dual_f7._factorial_prime_exponents(1) == ()
    assert dual_f7._factorial_prime_exponents(5) == ((2, 3), (3, 1), (5, 1))
    assert dual_f7._factorial_prime_exponents(10) == ((2, 8), (3, 4), (5, 2), (7, 1))


def test_coalesced_factorial_argument_counts_cancels_repeats() -> None:
    assert dual_f7._coalesced_factorial_argument_counts(
        numerator_factorials=(3, 5, 5, 7),
        denominator_factorials=(5, 7, 11),
    ) == ((3, 1), (5, 1), (11, -1))


@pytest.mark.skipif(dual_f7.gmpy2 is None, reason="backend exp-series path requires gmpy2")
def test_exp_series_backend_path_matches_fraction_path() -> None:
    log_coefficients = (
        Fraction(0),
        Fraction(10**80 + 17, 2**17 - 1),
        Fraction(-(10**75) + 29, 3**19 + 5),
        Fraction(10**70 + 31, 5**11 - 9),
        Fraction(-(10**65) + 7, 7**9 + 11),
    )

    assert dual_f7._exp_truncated_series_from_log_coefficients_via_mpq(log_coefficients) == dual_f7._exp_truncated_series_from_log_coefficients(log_coefficients)


@pytest.mark.skipif(dual_f7.gmpy2 is None, reason="backend component add path requires gmpy2")
def test_component_backend_add_matches_fraction_addition() -> None:
    left = Fraction(10**120 + 17, 2**61 - 1)
    right = Fraction(-(10**118) + 29, 2**59 - 1)

    assert dual_f7._add_fraction_components_via_backend(
        left_numerator=left.numerator,
        left_denominator=left.denominator,
        right_numerator=right.numerator,
        right_denominator=right.denominator,
    ) == ((left + right).numerator, (left + right).denominator)
