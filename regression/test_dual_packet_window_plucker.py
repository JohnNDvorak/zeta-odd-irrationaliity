from __future__ import annotations

from fractions import Fraction

import pytest

from zeta5_autoresearch.dual_packet_window_plucker import (
    build_normalized_window_plucker_vectors,
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
