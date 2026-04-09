from __future__ import annotations

from fractions import Fraction


ProfileVector = tuple[Fraction, Fraction, Fraction]
PacketVector = tuple[Fraction, Fraction, Fraction]


def solve_exact_linear_system(rows: tuple[tuple[Fraction, ...], ...]) -> tuple[Fraction, ...] | None:
    width = len(rows)
    if width == 0:
        return tuple()
    matrix = [list(row) for row in rows]
    if any(len(row) != width + 1 for row in matrix):
        raise ValueError("rows must describe a square augmented system")

    for column in range(width):
        pivot_row = None
        for row_index in range(column, width):
            if matrix[row_index][column] != 0:
                pivot_row = row_index
                break
        if pivot_row is None:
            return None
        if pivot_row != column:
            matrix[column], matrix[pivot_row] = matrix[pivot_row], matrix[column]

        pivot = matrix[column][column]
        matrix[column] = [entry / pivot for entry in matrix[column]]
        for row_index in range(width):
            if row_index == column:
                continue
            factor = matrix[row_index][column]
            if factor != 0:
                matrix[row_index] = [
                    value - factor * basis
                    for value, basis in zip(matrix[row_index], matrix[column])
                ]

    return tuple(matrix[index][width] for index in range(width))


def solve_exact_linear_system_with_zero_free_variables(
    rows: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, ...], int, int] | None:
    if not rows:
        return tuple(), 0, 0
    matrix = [list(row) for row in rows]
    variable_count = len(matrix[0]) - 1
    if variable_count < 0:
        raise ValueError("rows must include an augmented value")
    if any(len(row) != variable_count + 1 for row in matrix):
        raise ValueError("rows must describe a consistent augmented system width")

    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(variable_count):
        pivot_index = None
        for row_index in range(pivot_row, len(matrix)):
            if matrix[row_index][column] != 0:
                pivot_index = row_index
                break
        if pivot_index is None:
            continue
        if pivot_index != pivot_row:
            matrix[pivot_row], matrix[pivot_index] = matrix[pivot_index], matrix[pivot_row]

        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot for entry in matrix[pivot_row]]
        for row_index in range(len(matrix)):
            if row_index == pivot_row:
                continue
            factor = matrix[row_index][column]
            if factor != 0:
                matrix[row_index] = [
                    value - factor * basis
                    for value, basis in zip(matrix[row_index], matrix[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break

    for row in matrix:
        if all(value == 0 for value in row[:variable_count]) and row[variable_count] != 0:
            return None

    solution = [Fraction(0)] * variable_count
    for row_index, column in enumerate(pivot_columns):
        solution[column] = matrix[row_index][variable_count]

    rank = len(pivot_columns)
    nullity = variable_count - rank
    return tuple(solution), rank, nullity


def build_local_annihilator_profiles(
    vectors: tuple[PacketVector, ...],
) -> tuple[ProfileVector, ...]:
    if len(vectors) < 4:
        raise ValueError("at least four packet vectors are required")

    profiles: list[ProfileVector] = []
    for index in range(len(vectors) - 3):
        v0, v1, v2, v3 = vectors[index : index + 4]
        rows = (
            (v0[0], v1[0], v2[0], -v3[0]),
            (v0[1], v1[1], v2[1], -v3[1]),
            (v0[2], v1[2], v2[2], -v3[2]),
        )
        solution = solve_exact_linear_system(rows)
        if solution is None:
            raise ValueError(f"singular local annihilator window at n={index + 1}")
        profiles.append(solution)
    return tuple(profiles)
