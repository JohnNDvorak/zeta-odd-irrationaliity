from __future__ import annotations

from fractions import Fraction

from .dual_packet_local_annihilator_profile import solve_exact_linear_system


ChartProfileVector = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]
PacketVector = tuple[Fraction, Fraction, Fraction]


def build_window_chart_profiles(vectors: tuple[PacketVector, ...]) -> tuple[ChartProfileVector, ...]:
    if len(vectors) < 5:
        raise ValueError("at least five packet vectors are required")

    profiles: list[ChartProfileVector] = []
    for index in range(len(vectors) - 4):
        c0, c1, c2, c3, c4 = vectors[index : index + 5]
        rows3 = (
            (c0[0], c1[0], c2[0], c3[0]),
            (c0[1], c1[1], c2[1], c3[1]),
            (c0[2], c1[2], c2[2], c3[2]),
        )
        rows4 = (
            (c0[0], c1[0], c2[0], c4[0]),
            (c0[1], c1[1], c2[1], c4[1]),
            (c0[2], c1[2], c2[2], c4[2]),
        )
        coeffs3 = solve_exact_linear_system(rows3)
        coeffs4 = solve_exact_linear_system(rows4)
        if coeffs3 is None or coeffs4 is None:
            raise ValueError(f"singular chart window at n={index + 1}")
        profiles.append(coeffs3 + coeffs4)
    return tuple(profiles)
