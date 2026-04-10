from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import gcd, lcm


PacketVector = tuple[Fraction, Fraction, Fraction]
GenericVector = tuple[Fraction, ...]
IntegerVector = tuple[int, ...]


def _row_content_gcd(values: list[int], *, start: int = 0) -> int:
    content = 0
    for value in values[start:]:
        if value:
            content = gcd(content, abs(value))
            if content == 1:
                return 1
    return content


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
    if dimension == 1:
        return matrix[0][0]

    sign = 1
    previous_pivot = Fraction(1)
    for column in range(dimension - 1):
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
            if matrix[row_index][column] == 0:
                continue
            for inner in range(column + 1, dimension):
                matrix[row_index][inner] = (
                    pivot * matrix[row_index][inner] - matrix[row_index][column] * matrix[column][inner]
                ) / previous_pivot
            matrix[row_index][column] = Fraction(0)
        previous_pivot = pivot

    return Fraction(sign) * matrix[dimension - 1][dimension - 1]


def _solve_basis_coordinates(
    basis_columns: tuple[GenericVector, ...],
    target: GenericVector,
) -> tuple[Fraction, ...]:
    dimension = len(basis_columns)
    if any(len(column) != dimension for column in basis_columns):
        raise ValueError("basis columns must form a square system")
    if len(target) != dimension:
        raise ValueError("target dimension mismatch")

    # Clear row denominators once, then use fraction-free elimination over integers.
    matrix: list[list[int]] = []
    for row_index in range(dimension):
        row_values = [basis_columns[column_index][row_index] for column_index in range(dimension)]
        row_values.append(target[row_index])
        scale = lcm(*(value.denominator for value in row_values))
        integer_row = [value.numerator * (scale // value.denominator) for value in row_values]
        content = _row_content_gcd(integer_row)
        if content > 1:
            integer_row = [value // content for value in integer_row]
        matrix.append(integer_row)

    previous_pivot = 1
    for column in range(dimension - 1):
        pivot_row = None
        pivot_abs = None
        for row_index in range(column, dimension):
            if matrix[row_index][column] != 0:
                candidate_abs = abs(matrix[row_index][column])
                if pivot_abs is None or candidate_abs < pivot_abs:
                    pivot_row = row_index
                    pivot_abs = candidate_abs
        if pivot_row is None:
            raise ValueError("singular basis in coordinate solve")
        if pivot_row != column:
            matrix[column], matrix[pivot_row] = matrix[pivot_row], matrix[column]

        pivot = matrix[column][column]
        for row_index in range(column + 1, dimension):
            if matrix[row_index][column] == 0:
                continue
            for inner in range(column + 1, dimension + 1):
                matrix[row_index][inner] = (
                    pivot * matrix[row_index][inner] - matrix[row_index][column] * matrix[column][inner]
                ) // previous_pivot
            matrix[row_index][column] = 0
            content = _row_content_gcd(matrix[row_index], start=column + 1)
            if content > 1:
                for inner in range(column + 1, dimension + 1):
                    matrix[row_index][inner] //= content
        previous_pivot = pivot

    if matrix[dimension - 1][dimension - 1] == 0:
        raise ValueError("singular basis in coordinate solve")

    solution = [Fraction(0)] * dimension
    for row_index in range(dimension - 1, -1, -1):
        rhs = matrix[row_index][dimension]
        for inner in range(row_index + 1, dimension):
            rhs -= matrix[row_index][inner] * solution[inner]
        diagonal = matrix[row_index][row_index]
        if diagonal == 0:
            raise ValueError("singular basis in coordinate solve")
        solution[row_index] = Fraction(rhs, diagonal)

    return tuple(solution)


def _invert_basis_columns(basis_columns: tuple[GenericVector, ...]) -> tuple[GenericVector, ...]:
    dimension = len(basis_columns)
    if any(len(column) != dimension for column in basis_columns):
        raise ValueError("basis columns must form a square system")

    matrix: list[list[int]] = []
    for row_index in range(dimension):
        basis_row = [basis_columns[column_index][row_index] for column_index in range(dimension)]
        scale = lcm(*(value.denominator for value in basis_row))
        integer_row = [value.numerator * (scale // value.denominator) for value in basis_row]
        integer_row.extend(scale if row_index == rhs_index else 0 for rhs_index in range(dimension))
        content = _row_content_gcd(integer_row)
        if content > 1:
            integer_row = [value // content for value in integer_row]
        matrix.append(integer_row)

    previous_pivot = 1
    for column in range(dimension - 1):
        pivot_row = None
        pivot_abs = None
        for row_index in range(column, dimension):
            if matrix[row_index][column] != 0:
                candidate_abs = abs(matrix[row_index][column])
                if pivot_abs is None or candidate_abs < pivot_abs:
                    pivot_row = row_index
                    pivot_abs = candidate_abs
        if pivot_row is None:
            raise ValueError("singular basis in coordinate solve")
        if pivot_row != column:
            matrix[column], matrix[pivot_row] = matrix[pivot_row], matrix[column]

        pivot = matrix[column][column]
        for row_index in range(column + 1, dimension):
            if matrix[row_index][column] == 0:
                continue
            for inner in range(column + 1, 2 * dimension):
                matrix[row_index][inner] = (
                    pivot * matrix[row_index][inner] - matrix[row_index][column] * matrix[column][inner]
                ) // previous_pivot
            matrix[row_index][column] = 0
            content = _row_content_gcd(matrix[row_index], start=column + 1)
            if content > 1:
                for inner in range(column + 1, 2 * dimension):
                    matrix[row_index][inner] //= content
        previous_pivot = pivot

    if matrix[dimension - 1][dimension - 1] == 0:
        raise ValueError("singular basis in coordinate solve")

    inverse_columns: list[tuple[Fraction, ...]] = []
    for rhs_index in range(dimension):
        solution = [Fraction(0)] * dimension
        for row_index in range(dimension - 1, -1, -1):
            rhs = matrix[row_index][dimension + rhs_index]
            for inner in range(row_index + 1, dimension):
                rhs -= matrix[row_index][inner] * solution[inner]
            diagonal = matrix[row_index][row_index]
            if diagonal == 0:
                raise ValueError("singular basis in coordinate solve")
            solution[row_index] = Fraction(rhs, diagonal)
        inverse_columns.append(tuple(solution))

    return tuple(
        tuple(inverse_columns[column_index][row_index] for column_index in range(dimension))
        for row_index in range(dimension)
    )


def _common_denominator_rows(rows: tuple[GenericVector, ...]) -> tuple[tuple[IntegerVector, ...], int]:
    denominator = 1
    for row in rows:
        denominator = lcm(denominator, *(value.denominator for value in row))

    row_numerators = tuple(
        tuple(value.numerator * (denominator // value.denominator) for value in row)
        for row in rows
    )

    content = denominator
    for row in row_numerators:
        content = _row_content_gcd([content, *row])
        if content == 1:
            break
    if content > 1:
        denominator //= content
        row_numerators = tuple(
            tuple(value // content for value in row)
            for row in row_numerators
        )

    return row_numerators, denominator


def _integerize_vector(vector: GenericVector) -> tuple[int, IntegerVector]:
    scale = lcm(*(value.denominator for value in vector))
    integer_vector = tuple(value.numerator * (scale // value.denominator) for value in vector)
    content = gcd(scale, _row_content_gcd(list(integer_vector)))
    if content > 1:
        scale //= content
        integer_vector = tuple(value // content for value in integer_vector)
    return scale, integer_vector


def _integerize_vectors(vectors: tuple[GenericVector, ...]) -> tuple[tuple[int, ...], tuple[IntegerVector, ...]]:
    scales: list[int] = []
    integerized: list[IntegerVector] = []
    for vector in vectors:
        scale, integer_vector = _integerize_vector(vector)
        scales.append(scale)
        integerized.append(integer_vector)
    return tuple(scales), tuple(integerized)


def _matvec_rows(rows: tuple[GenericVector, ...], vector: GenericVector) -> tuple[Fraction, ...]:
    return tuple(sum(entry * value for entry, value in zip(row, vector)) for row in rows)


def _encode_codimension_one_coordinates(coordinates: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    dimension = len(coordinates)
    return tuple(
        ((-1) ** (dimension - 1 - missing_index)) * coordinates[missing_index]
        for missing_index in range(dimension - 1, -1, -1)
    )


def _matvec_rows_common_den(
    row_numerators: tuple[IntegerVector, ...],
    vector: IntegerVector,
) -> tuple[int, ...]:
    return tuple(sum(entry * value for entry, value in zip(row, vector)) for row in row_numerators)


def _reduce_common_denominator_state(
    row_numerators: tuple[IntegerVector, ...],
    coordinate_numerators: tuple[int, ...],
    denominator: int,
) -> tuple[tuple[IntegerVector, ...], tuple[int, ...], int]:
    content = denominator
    for row in row_numerators:
        content = _row_content_gcd([content, *row])
        if content == 1:
            break
    if content > 1:
        for value in coordinate_numerators:
            content = gcd(content, abs(value))
            if content == 1:
                break
    if content > 1:
        denominator //= content
        row_numerators = tuple(tuple(value // content for value in row) for row in row_numerators)
        coordinate_numerators = tuple(value // content for value in coordinate_numerators)
    return row_numerators, coordinate_numerators, denominator


def _recover_codimension_one_coordinates(
    coordinate_numerators: tuple[int, ...],
    denominator: int,
    *,
    basis_scales: tuple[int, ...],
    extra_scale: int,
) -> tuple[Fraction, ...]:
    recovered = tuple(
        Fraction(coordinate_numerators[index] * basis_scales[index], denominator * extra_scale)
        for index in range(len(coordinate_numerators))
    )
    return _encode_codimension_one_coordinates(recovered)


def _advance_codimension_one_inverse_rows(
    inverse_rows: tuple[GenericVector, ...],
    coordinates: tuple[Fraction, ...],
) -> tuple[GenericVector, ...]:
    lead = coordinates[0]
    if lead == 0:
        raise ValueError("singular basis in coordinate solve")

    new_last_row = tuple(value / lead for value in inverse_rows[0])
    new_rows = [
        tuple(inverse_rows[row_index + 1][column_index] - coordinates[row_index + 1] * new_last_row[column_index] for column_index in range(len(new_last_row)))
        for row_index in range(len(inverse_rows) - 1)
    ]
    new_rows.append(new_last_row)
    return tuple(new_rows)


def _advance_codimension_one_coordinates(
    current_coordinates: tuple[Fraction, ...],
    next_extra_in_old_basis: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    lead = current_coordinates[0]
    if lead == 0:
        raise ValueError("singular basis in coordinate solve")

    next_last = next_extra_in_old_basis[0] / lead
    next_coords = [
        next_extra_in_old_basis[row_index + 1] - current_coordinates[row_index + 1] * next_last
        for row_index in range(len(current_coordinates) - 1)
    ]
    next_coords.append(next_last)
    return tuple(next_coords)


def _advance_codimension_one_common_den_state(
    row_numerators: tuple[IntegerVector, ...],
    coordinates: tuple[int, ...],
    denominator: int,
    next_extra_in_old_basis: tuple[int, ...],
) -> tuple[tuple[IntegerVector, ...], tuple[int, ...], int]:
    lead = coordinates[0]
    if lead == 0:
        raise ValueError("singular basis in coordinate solve")

    next_denominator = denominator * lead
    last_row = tuple(value * denominator for value in row_numerators[0])
    next_rows = [
        tuple(
            row_numerators[row_index + 1][column_index] * lead
            - coordinates[row_index + 1] * row_numerators[0][column_index]
            for column_index in range(len(last_row))
        )
        for row_index in range(len(row_numerators) - 1)
    ]
    next_rows.append(last_row)

    next_coordinates = [
        next_extra_in_old_basis[row_index + 1] * lead
        - coordinates[row_index + 1] * next_extra_in_old_basis[0]
        for row_index in range(len(coordinates) - 1)
    ]
    next_coordinates.append(next_extra_in_old_basis[0] * denominator)

    return _reduce_common_denominator_state(
        tuple(next_rows),
        tuple(next_coordinates),
        next_denominator,
    )


def _build_codimension_one_normalized_coordinates(
    window: tuple[GenericVector, ...],
) -> tuple[Fraction, ...]:
    dimension = len(window[0])
    basis = tuple(window[:dimension])
    extra = window[dimension]
    coordinates = _solve_basis_coordinates(basis, extra)
    return _encode_codimension_one_coordinates(coordinates)


def _build_codimension_one_normalized_coordinates_rolling(
    vectors: tuple[GenericVector, ...],
    *,
    window_size: int,
) -> tuple[tuple[Fraction, ...], ...]:
    dimension = len(vectors[0])
    basis = tuple(vectors[:dimension])
    basis_fraction = tuple(
        tuple(Fraction(value) for value in column)
        for column in _integerize_vectors(basis)[1]
    )
    basis_scales, integer_vectors = _integerize_vectors(vectors)
    inverse_rows = _invert_basis_columns(basis_fraction)
    inverse_row_numerators, inverse_denominator = _common_denominator_rows(inverse_rows)
    window_count = len(vectors) - window_size + 1
    coordinates = _matvec_rows_common_den(inverse_row_numerators, integer_vectors[dimension])

    profiles: list[tuple[Fraction, ...]] = []
    for window_index in range(window_count):
        profiles.append(
            _recover_codimension_one_coordinates(
                coordinates,
                inverse_denominator,
                basis_scales=basis_scales[window_index : window_index + dimension],
                extra_scale=basis_scales[window_index + dimension],
            )
        )
        if window_index + 1 == window_count:
            break
        if coordinates[0] == 0:
            raise ValueError(f"singular maximal-minor pivot in window starting at n={window_index + 2}")
        next_extra_in_old_basis = _matvec_rows_common_den(
            inverse_row_numerators,
            integer_vectors[window_index + window_size],
        )
        inverse_row_numerators, coordinates, inverse_denominator = _advance_codimension_one_common_den_state(
            inverse_row_numerators,
            coordinates,
            inverse_denominator,
            next_extra_in_old_basis,
        )

    return tuple(profiles)


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

    if window_size == dimension + 1:
        try:
            return _build_codimension_one_normalized_coordinates_rolling(vectors, window_size=window_size)
        except ValueError as exc:
            message = str(exc)
            if message == "singular basis in coordinate solve":
                raise ValueError("singular maximal-minor pivot in window starting at n=1") from exc
            if message.startswith("singular maximal-minor pivot in window starting at n="):
                raise
            raise

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
