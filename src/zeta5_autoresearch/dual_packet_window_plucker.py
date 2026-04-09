from __future__ import annotations

from fractions import Fraction
from itertools import combinations


PacketVector = tuple[Fraction, Fraction, Fraction]


def det3(columns: tuple[PacketVector, PacketVector, PacketVector]) -> Fraction:
    (a, b, c), (d, e, f), (g, h, i) = columns
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def build_normalized_window_plucker_vectors(
    vectors: tuple[PacketVector, ...],
    *,
    window_size: int,
) -> tuple[tuple[Fraction, ...], ...]:
    if window_size < 3:
        raise ValueError("window_size must be at least 3")
    if len(vectors) < window_size:
        raise ValueError("not enough packet vectors for the requested window size")

    pivot = (0, 1, 2)
    all_triples = tuple(combinations(range(window_size), 3))
    rest = tuple(triple for triple in all_triples if triple != pivot)

    profiles: list[tuple[Fraction, ...]] = []
    for index in range(len(vectors) - window_size + 1):
        window = vectors[index : index + window_size]
        pivot_columns = tuple(window[position] for position in pivot)
        pivot_value = det3(pivot_columns)  # type: ignore[arg-type]
        if pivot_value == 0:
            raise ValueError(f"singular Plucker pivot in window starting at n={index + 1}")

        coordinates = []
        for triple in rest:
            columns = tuple(window[position] for position in triple)
            coordinates.append(det3(columns) / pivot_value)  # type: ignore[arg-type]
        profiles.append(tuple(coordinates))
    return tuple(profiles)
