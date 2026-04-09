from __future__ import annotations

from fractions import Fraction

from zeta5_autoresearch.dual_packet_local_annihilator_profile import (
    build_local_annihilator_profiles,
    solve_exact_linear_system_with_zero_free_variables,
)


def test_solve_exact_linear_system_with_zero_free_variables_picks_canonical_solution() -> None:
    solved = solve_exact_linear_system_with_zero_free_variables(
        (
            (Fraction(1), Fraction(1), Fraction(3)),
            (Fraction(2), Fraction(2), Fraction(6)),
        )
    )

    assert solved == ((Fraction(3), Fraction(0)), 1, 1)


def test_solve_exact_linear_system_with_zero_free_variables_detects_inconsistency() -> None:
    solved = solve_exact_linear_system_with_zero_free_variables(
        (
            (Fraction(1), Fraction(1), Fraction(3)),
            (Fraction(1), Fraction(1), Fraction(4)),
        )
    )

    assert solved is None


def test_build_local_annihilator_profiles_solves_exact_window() -> None:
    profiles = build_local_annihilator_profiles(
        (
            (Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(1)),
            (Fraction(4), Fraction(3), Fraction(2)),
        )
    )

    assert profiles == ((Fraction(-4), Fraction(-3), Fraction(-2)),)
