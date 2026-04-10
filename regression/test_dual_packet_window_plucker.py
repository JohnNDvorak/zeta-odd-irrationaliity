from __future__ import annotations

from fractions import Fraction

import pytest

from zeta5_autoresearch.dual_packet_window_plucker import (
    build_normalized_window_maximal_minor_vectors,
    build_normalized_window_plucker_vectors,
    determinant,
)


def test_build_normalized_window_plucker_vectors_normalizes_by_pivot_minor() -> None:
    vectors = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
        (Fraction(2), Fraction(3), Fraction(5)),
    )

    profiles = build_normalized_window_plucker_vectors(vectors, window_size=4)

    assert profiles == ((Fraction(5), Fraction(-3), Fraction(2)),)


def test_build_normalized_window_plucker_vectors_rejects_singular_pivot() -> None:
    vectors = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(2), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )

    with pytest.raises(ValueError, match="singular Plucker pivot"):
        build_normalized_window_plucker_vectors(vectors, window_size=4)


def test_determinant_handles_generic_square_columns() -> None:
    columns = (
        (Fraction(1), Fraction(0), Fraction(2), Fraction(1)),
        (Fraction(0), Fraction(1), Fraction(3), Fraction(1)),
        (Fraction(0), Fraction(0), Fraction(1), Fraction(4)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(5)),
    )

    assert determinant(columns) == Fraction(5)


def test_build_normalized_window_maximal_minor_vectors_handles_dimension_six_window_seven() -> None:
    basis = tuple(
        tuple(Fraction(1 if i == j else 0) for i in range(6))
        for j in range(6)
    )
    extra = (Fraction(2), Fraction(3), Fraction(5), Fraction(7), Fraction(11), Fraction(13))
    vectors = basis + (extra,)

    profiles = build_normalized_window_maximal_minor_vectors(vectors, window_size=7)

    assert profiles == ((
        Fraction(13),
        Fraction(-11),
        Fraction(7),
        Fraction(-5),
        Fraction(3),
        Fraction(-2),
    ),)
