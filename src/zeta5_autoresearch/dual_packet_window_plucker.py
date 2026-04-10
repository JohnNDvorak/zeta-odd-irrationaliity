from __future__ import annotations

from fractions import Fraction
from itertools import combinations


PacketVector = tuple[Fraction, Fraction, Fraction]
GenericVector = tuple[Fraction, ...]


def det3(columns: tuple[PacketVector, PacketVector, PacketVector]) -> Fraction:
    (a, b, c), (d, e, f), (g, h, i) = columns
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def determinant(columns: tuple[GenericVector, ...]) -> Fraction:
    dimension = len(columns)
    if dimension == 0:
        raise ValueError("determinant requires at least one column")
    if any(len(column) != dimension for column in columns):
        raise ValueError("determinant requires square column data")

    matrix = [list(row) for row in zip(*columns)]
    sign = 1
    for column in range(dimension):
        pivot_row = None
        for row_index in range(column, dimension):
            if matrix[row_index][column] != 0:
                pivot_row = row_index
                break
        if pivot_row is None:
            return Fraction(0)
        if pivot_row != column:
            matrix[column], matrix[pivot_row] = matrix[pivot_row], matrix[column]
            sign *= -1

        pivot = matrix[column][column]
        for row_index in range(column + 1, dimension):
            factor = matrix[row_index][column]
            if factor == 0:
                continue
            ratio = factor / pivot
            for inner in range(column, dimension):
                matrix[row_index][inner] -= ratio * matrix[column][inner]

    diagonal = Fraction(sign)
    for index in range(dimension):
        diagonal *= matrix[index][index]
    return diagonal


def build_normalized_window_maximal_minor_vectors(
    vectors: tuple[GenericVector, ...],
    *,
    window_size: int,
) -> tuple[tuple[Fraction, ...], ...]:
    if not vectors:
        raise ValueError("at least one vector is required")
    dimension = len(vectors[0])
    if any(len(vector) != dimension for vector in vectors):
        raise ValueError("all vectors must have the same dimension")
    if window_size < dimension:
        raise ValueError("window_size must be at least the vector dimension")
    if len(vectors) < window_size:
        raise ValueError("not enough vectors for the requested window size")

    pivot = tuple(range(dimension))
    all_subsets = tuple(combinations(range(window_size), dimension))
    rest = tuple(subset for subset in all_subsets if subset != pivot)

    profiles: list[tuple[Fraction, ...]] = []
    for index in range(len(vectors) - window_size + 1):
        window = vectors[index : index + window_size]
        pivot_columns = tuple(window[position] for position in pivot)
        pivot_value = determinant(pivot_columns)
        if pivot_value == 0:
            raise ValueError(f"singular maximal-minor pivot in window starting at n={index + 1}")

        coordinates = []
        for subset in rest:
            columns = tuple(window[position] for position in subset)
            coordinates.append(determinant(columns) / pivot_value)
        profiles.append(tuple(coordinates))
    return tuple(profiles)


def build_normalized_window_plucker_vectors(
    vectors: tuple[PacketVector, ...],
    *,
    window_size: int,
) -> tuple[tuple[Fraction, ...], ...]:
    try:
        return build_normalized_window_maximal_minor_vectors(vectors, window_size=window_size)
    except ValueError as exc:
        message = str(exc)
        if message.startswith("singular maximal-minor pivot in window starting at n="):
            suffix = message.split("n=", 1)[1]
            raise ValueError(f"singular Plucker pivot in window starting at n={suffix}") from exc
        raise
