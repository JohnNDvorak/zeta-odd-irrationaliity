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


def test_build_normalized_window_maximal_minor_vectors_matches_bruteforce_on_fractional_codim_one_windows() -> None:
    vectors = (
        (Fraction(1, 2), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(2, 3), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(3, 5)),
        (Fraction(5, 7), Fraction(7, 11), Fraction(11, 13)),
        (Fraction(13, 17), Fraction(17, 19), Fraction(19, 23)),
        (Fraction(23, 29), Fraction(29, 31), Fraction(31, 37)),
    )

    profiles = build_normalized_window_maximal_minor_vectors(vectors, window_size=4)

    def solve_coordinates(window: tuple[tuple[Fraction, ...], ...]) -> tuple[Fraction, ...]:
        basis = window[:3]
        extra = window[3]
        matrix = [
            [basis[column_index][row_index] for column_index in range(3)] + [extra[row_index]]
            for row_index in range(3)
        ]
        for column in range(3):
            pivot_row = next(
                row_index for row_index in range(column, 3) if matrix[row_index][column] != 0
            )
            if pivot_row != column:
                matrix[column], matrix[pivot_row] = matrix[pivot_row], matrix[column]

            pivot = matrix[column][column]
            for inner in range(column, 4):
                matrix[column][inner] /= pivot
            for row_index in range(column + 1, 3):
                factor = matrix[row_index][column]
                if factor == 0:
                    continue
                for inner in range(column, 4):
                    matrix[row_index][inner] -= factor * matrix[column][inner]

        solution = [Fraction(0)] * 3
        for row_index in range(2, -1, -1):
            rhs = matrix[row_index][3]
            for inner in range(row_index + 1, 3):
                rhs -= matrix[row_index][inner] * solution[inner]
            solution[row_index] = rhs
        return tuple(solution)

    expected = tuple(
        tuple(
            ((-1) ** (2 - missing_index)) * coordinates[missing_index]
            for missing_index in range(2, -1, -1)
        )
        for coordinates in (
            solve_coordinates(vectors[start : start + 4])
            for start in range(len(vectors) - 3)
        )
    )

    assert profiles == expected
