from __future__ import annotations

from fractions import Fraction

from zeta5_autoresearch.dual_packet_schur_functor import (
    build_sym2_lifted_packet_vectors,
    sym2_lift_packet_vector,
)


def test_sym2_lift_packet_vector_uses_quadratic_monomials() -> None:
    vector = (Fraction(2), Fraction(3), Fraction(5))

    assert sym2_lift_packet_vector(vector) == (
        Fraction(4),
        Fraction(6),
        Fraction(10),
        Fraction(9),
        Fraction(15),
        Fraction(25),
    )


def test_build_sym2_lifted_packet_vectors_maps_each_vector() -> None:
    vectors = (
        (Fraction(1), Fraction(2), Fraction(3)),
        (Fraction(0), Fraction(1), Fraction(1)),
    )

    assert build_sym2_lifted_packet_vectors(vectors) == (
        (Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(6), Fraction(9)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(1), Fraction(1)),
    )
