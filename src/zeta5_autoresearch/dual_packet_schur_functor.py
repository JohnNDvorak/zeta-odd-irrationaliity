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
Sym4Vector = tuple[
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


def sym4_lift_packet_vector(vector: PacketVector) -> Sym4Vector:
    a, b, c = vector
    return (
        a**4,
        a**3 * b,
        a**3 * c,
        a * a * b * b,
        a * a * b * c,
        a * a * c * c,
        a * b**3,
        a * b * b * c,
        a * b * c * c,
        a * c**3,
        b**4,
        b**3 * c,
        b * b * c * c,
        b * c**3,
        c**4,
    )


def build_sym4_lifted_packet_vectors(vectors: tuple[PacketVector, ...]) -> tuple[Sym4Vector, ...]:
    return tuple(sym4_lift_packet_vector(vector) for vector in vectors)
