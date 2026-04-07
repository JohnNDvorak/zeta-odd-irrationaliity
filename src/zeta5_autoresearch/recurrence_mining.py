from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd

FULL_RANK_CERTIFICATE_PRIMES = (1000003, 1000033, 1000037, 1000039, 1000081)


@dataclass(frozen=True)
class PolynomialRelation:
    shift: int
    coefficients: tuple[int, ...]

    @property
    def degree(self) -> int:
        return len(self.coefficients) - 1


@dataclass(frozen=True)
class PolynomialRecurrenceBasisVector:
    relations: tuple[PolynomialRelation, ...]
    coefficient_height: int

    def evaluate(self, sequence: tuple[Fraction, ...], n: int) -> Fraction:
        total = Fraction(0)
        for relation in self.relations:
            total += _evaluate_integer_polynomial(relation.coefficients, n) * sequence[n + relation.shift]
        return total


@dataclass(frozen=True)
class RecurrenceSearchResult:
    degree: int
    shifts: tuple[int, ...]
    start_n: int
    end_n: int
    equation_count: int
    variable_count: int
    rank: int
    nullity: int
    basis: tuple[PolynomialRecurrenceBasisVector, ...]

    @property
    def has_nontrivial_solution(self) -> bool:
        return self.nullity > 0


@dataclass(frozen=True)
class ModularRankCertificate:
    degree: int
    modulus: int
    equation_count: int
    variable_count: int
    rank: int

    @property
    def nullity_upper_bound(self) -> int:
        return self.variable_count - self.rank

    @property
    def certifies_no_solution(self) -> bool:
        return self.rank == self.variable_count


def search_polynomial_recurrences(
    sequence: tuple[Fraction, ...],
    *,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    degree_min: int = 0,
    degree_max: int = 8,
    start_n: int | None = None,
    end_n: int | None = None,
    basis_limit: int = 2,
) -> tuple[RecurrenceSearchResult, ...]:
    if degree_min < 0:
        raise ValueError("degree_min must be nonnegative")
    if degree_max < degree_min:
        raise ValueError("degree_max must be >= degree_min")
    if not shifts:
        raise ValueError("shifts must be non-empty")

    max_shift = max(shifts)
    min_shift = min(shifts)
    default_start = max(0, -min_shift)
    default_end = len(sequence) - 1 - max_shift
    start = default_start if start_n is None else start_n
    end = default_end if end_n is None else end_n
    if start > end:
        raise ValueError("no valid recurrence window for the supplied sequence and shifts")

    results = []
    for degree in range(degree_min, degree_max + 1):
        matrix = _build_recurrence_matrix(
            sequence=sequence,
            shifts=shifts,
            degree=degree,
            start_n=start,
            end_n=end,
        )
        variable_count = (degree + 1) * len(shifts)
        if _has_exact_full_rank_certificate(matrix, target_rank=variable_count):
            basis = ()
            rank = variable_count
            grouped_basis = ()
        else:
            basis = _nullspace_basis(matrix)
            rank = 0 if not matrix else len(matrix[0]) - len(basis)
            grouped_basis = tuple(
                _group_basis_vector(vector, shifts=shifts, degree=degree)
                for vector in basis[:basis_limit]
            )
        results.append(
            RecurrenceSearchResult(
                degree=degree,
                shifts=shifts,
                start_n=start,
                end_n=end,
                equation_count=len(matrix),
                variable_count=variable_count,
                rank=rank,
                nullity=len(basis),
                basis=grouped_basis,
            )
        )
    return tuple(results)


def modular_rank_certificate(
    sequence: tuple[int, ...],
    *,
    degree: int,
    modulus: int,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    start_n: int | None = None,
    end_n: int | None = None,
) -> ModularRankCertificate:
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    if modulus <= 2:
        raise ValueError("modulus must be an odd prime greater than 2")
    if not shifts:
        raise ValueError("shifts must be non-empty")

    max_shift = max(shifts)
    min_shift = min(shifts)
    default_start = max(0, -min_shift)
    default_end = len(sequence) - 1 - max_shift
    start = default_start if start_n is None else start_n
    end = default_end if end_n is None else end_n
    if start > end:
        raise ValueError("no valid recurrence window for the supplied sequence and shifts")

    matrix = _build_modular_recurrence_matrix(
        sequence=sequence,
        shifts=shifts,
        degree=degree,
        start_n=start,
        end_n=end,
        modulus=modulus,
    )
    return ModularRankCertificate(
        degree=degree,
        modulus=modulus,
        equation_count=len(matrix),
        variable_count=(degree + 1) * len(shifts),
        rank=_modular_rank(matrix, modulus),
    )


def _build_recurrence_matrix(
    *,
    sequence: tuple[Fraction, ...],
    shifts: tuple[int, ...],
    degree: int,
    start_n: int,
    end_n: int,
) -> tuple[tuple[Fraction, ...], ...]:
    rows = []
    for n in range(start_n, end_n + 1):
        row = []
        for shift in shifts:
            term = sequence[n + shift]
            row.extend((Fraction(n) ** power) * term for power in range(degree + 1))
        rows.append(tuple(row))
    return tuple(rows)


def _build_modular_recurrence_matrix(
    *,
    sequence: tuple[int, ...],
    shifts: tuple[int, ...],
    degree: int,
    start_n: int,
    end_n: int,
    modulus: int,
) -> tuple[tuple[int, ...], ...]:
    rows = []
    for n in range(start_n, end_n + 1):
        row = []
        for shift in shifts:
            term = sequence[n + shift] % modulus
            power = 1
            for _ in range(degree + 1):
                row.append((power * term) % modulus)
                power = (power * (n % modulus)) % modulus
        rows.append(tuple(row))
    return tuple(rows)


def _nullspace_basis(matrix: tuple[tuple[Fraction, ...], ...]) -> tuple[tuple[Fraction, ...], ...]:
    rows = [list(row) for row in matrix]
    if not rows:
        return ()

    row_count = len(rows)
    column_count = len(rows[0])
    pivot_columns: list[int] = []
    pivot_row = 0

    for column in range(column_count):
        pivot = None
        for candidate in range(pivot_row, row_count):
            if rows[candidate][column] != 0:
                pivot = candidate
                break
        if pivot is None:
            continue

        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]

        for index in range(row_count):
            if index == pivot_row or rows[index][column] == 0:
                continue
            factor = rows[index][column]
            rows[index] = [
                rows[index][offset] - factor * rows[pivot_row][offset]
                for offset in range(column_count)
            ]

        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    free_columns = [column for column in range(column_count) if column not in pivot_columns]
    basis = []
    for free_column in free_columns:
        vector = [Fraction(0) for _ in range(column_count)]
        vector[free_column] = Fraction(1)
        for row_index in range(len(pivot_columns) - 1, -1, -1):
            column = pivot_columns[row_index]
            tail = Fraction(0)
            for offset in range(column + 1, column_count):
                tail += rows[row_index][offset] * vector[offset]
            vector[column] = -tail
        basis.append(tuple(vector))
    return tuple(basis)


def _has_exact_full_rank_certificate(
    matrix: tuple[tuple[Fraction, ...], ...],
    *,
    target_rank: int,
) -> bool:
    if not matrix or target_rank <= 0 or len(matrix) < target_rank:
        return False

    integer_matrix = _clear_matrix_row_denominators(matrix)
    for modulus in FULL_RANK_CERTIFICATE_PRIMES:
        if _modular_rank(integer_matrix, modulus) == target_rank:
            return True
    return False


def _clear_matrix_row_denominators(
    matrix: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    cleared_rows = []
    for row in matrix:
        scale = 1
        for value in row:
            scale = _lcm(scale, value.denominator)
        cleared_rows.append(tuple((value * scale).numerator for value in row))
    return tuple(cleared_rows)


def _modular_rank(matrix: tuple[tuple[int, ...], ...], modulus: int) -> int:
    rows = [list(row) for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0]) if rows else 0
    rank = 0

    for column in range(column_count):
        pivot = None
        for candidate in range(rank, row_count):
            if rows[candidate][column] % modulus != 0:
                pivot = candidate
                break
        if pivot is None:
            continue

        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column] % modulus, -1, modulus)
        rows[rank] = [(value * inverse) % modulus for value in rows[rank]]

        for index in range(rank + 1, row_count):
            if rows[index][column] % modulus == 0:
                continue
            factor = rows[index][column] % modulus
            rows[index] = [
                (rows[index][offset] - factor * rows[rank][offset]) % modulus
                for offset in range(column_count)
            ]

        rank += 1
        if rank == row_count:
            break

    return rank


def _group_basis_vector(
    vector: tuple[Fraction, ...],
    *,
    shifts: tuple[int, ...],
    degree: int,
) -> PolynomialRecurrenceBasisVector:
    normalized = _normalize_integer_relation(vector)
    relations = []
    offset = 0
    for shift in shifts:
        coefficients = normalized[offset : offset + degree + 1]
        relations.append(PolynomialRelation(shift=shift, coefficients=_trim_trailing_zeros(coefficients)))
        offset += degree + 1
    return PolynomialRecurrenceBasisVector(
        relations=tuple(relations),
        coefficient_height=max(abs(value) for value in normalized) if normalized else 0,
    )


def _normalize_integer_relation(vector: tuple[Fraction, ...]) -> tuple[int, ...]:
    common_denominator = 1
    for value in vector:
        common_denominator = _lcm(common_denominator, value.denominator)
    integers = [int(value * common_denominator) for value in vector]

    content = 0
    for value in integers:
        content = gcd(content, abs(value))
    if content:
        integers = [value // content for value in integers]

    for value in integers:
        if value == 0:
            continue
        if value < 0:
            integers = [-entry for entry in integers]
        break
    return tuple(integers)


def _trim_trailing_zeros(coefficients: tuple[int, ...]) -> tuple[int, ...]:
    trimmed = list(coefficients)
    while trimmed and trimmed[-1] == 0:
        trimmed.pop()
    return tuple(trimmed) if trimmed else (0,)


def _evaluate_integer_polynomial(coefficients: tuple[int, ...], n: int) -> Fraction:
    total = 0
    power = 1
    for coefficient in coefficients:
        total += coefficient * power
        power *= n
    return Fraction(total)


def _lcm(left: int, right: int) -> int:
    return abs(left * right) // gcd(left, right)
