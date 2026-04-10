from __future__ import annotations

from fractions import Fraction


PacketVector = tuple[Fraction, Fraction, Fraction]
Sym2Vector = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]


def sym2_lift_packet_vector(vector: PacketVector) -> Sym2Vector:
    a, b, c = vector
    return (a * a, a * b, a * c, b * b, b * c, c * c)


def build_sym2_lifted_packet_vectors(vectors: tuple[PacketVector, ...]) -> tuple[Sym2Vector, ...]:
    return tuple(sym2_lift_packet_vector(vector) for vector in vectors)
