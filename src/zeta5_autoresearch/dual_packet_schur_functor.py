from __future__ import annotations

from fractions import Fraction


PacketVector = tuple[Fraction, Fraction, Fraction]
Sym2Vector = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]
Sym3Vector = tuple[
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
]


def sym2_lift_packet_vector(vector: PacketVector) -> Sym2Vector:
    a, b, c = vector
    return (a * a, a * b, a * c, b * b, b * c, c * c)


def build_sym2_lifted_packet_vectors(vectors: tuple[PacketVector, ...]) -> tuple[Sym2Vector, ...]:
    return tuple(sym2_lift_packet_vector(vector) for vector in vectors)


def sym3_lift_packet_vector(vector: PacketVector) -> Sym3Vector:
    a, b, c = vector
    return (
        a * a * a,
        a * a * b,
        a * a * c,
        a * b * b,
        a * b * c,
        a * c * c,
        b * b * b,
        b * b * c,
        b * c * c,
        c * c * c,
    )


def build_sym3_lifted_packet_vectors(vectors: tuple[PacketVector, ...]) -> tuple[Sym3Vector, ...]:
    return tuple(sym3_lift_packet_vector(vector) for vector in vectors)
