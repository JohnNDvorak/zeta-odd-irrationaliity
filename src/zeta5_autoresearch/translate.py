from __future__ import annotations

from fractions import Fraction


def s_to_a(s: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    if len(s) != 8:
        raise ValueError("s must have length 8")
    s0, s1, s2, s3, s4, s5, s6, s7 = s
    return (
        s1 + s2,
        s0 - s2,
        s2 + s3,
        s0 - s3,
        s3 + s4,
        s5 + s6,
        s6 + s7,
        s3 + s5,
    )


def a_to_s(a: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    if len(a) != 8:
        raise ValueError("a must have length 8")
    a1, a2, a3, a4, a5, a6, a7, a8 = a
    half = Fraction(1, 2)
    return (
        half * (a2 + a3 + a4),
        a1 + half * (a2 - a3 - a4),
        half * (a3 + a4 - a2),
        half * (a2 + a3 - a4),
        a5 + half * (a4 - a2 - a3),
        a8 + half * (a4 - a2 - a3),
        a6 - a8 + half * (a2 + a3 - a4),
        a7 + a8 - a6 + half * (a4 - a2 - a3),
    )
