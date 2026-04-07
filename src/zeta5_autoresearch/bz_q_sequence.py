from __future__ import annotations

from dataclasses import dataclass
from math import comb


def baseline_a_vector() -> tuple[int, ...]:
    return (8, 16, 10, 15, 12, 16, 18, 13)


def totally_symmetric_a_vector() -> tuple[int, ...]:
    return (1, 1, 1, 1, 1, 1, 1, 1)


def pq_parameters_from_a(a: tuple[int, ...]) -> tuple[int, ...]:
    if len(a) != 8:
        raise ValueError("a must have length 8")
    a1, a2, a3, a4, a5, a6, a7, a8 = a
    return (
        a5 + a6 - a8,
        a2 + a3 + a6 - a4 - a8,
        a6,
        a2 + a3 + a6 - a8,
        a7,
        a3 + a6 - a8,
        a1 + a2 + a6 - a4 - a8,
        a4,
        a5,
        a1 + a5 - a3,
        a1,
        a2,
    )


def scale_a_vector(a: tuple[int, ...], n: int) -> tuple[int, ...]:
    return tuple(value * n for value in a)


def compute_q_term_from_a(a: tuple[int, ...], n: int) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    return compute_q_from_pq(pq_parameters_from_a(scale_a_vector(a, n)))


def compute_q_signature_from_a(a: tuple[int, ...], *, start_index: int = 0, term_count: int = 8) -> tuple[int, ...]:
    if term_count <= 0:
        raise ValueError("term_count must be positive")
    return tuple(compute_q_term_from_a(a, start_index + offset) for offset in range(term_count))


@dataclass(frozen=True)
class ModularBinomialTable:
    modulus: int
    limit: int
    factorials: tuple[int, ...]
    inverse_factorials: tuple[int, ...]


def build_modular_binomial_table(*, modulus: int, limit: int) -> ModularBinomialTable:
    if modulus <= 2:
        raise ValueError("modulus must be greater than 2")
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    if limit >= modulus:
        raise ValueError("modular binomial table limit must stay below the modulus; Lucas reduction is not implemented")

    factorials = [1] * (limit + 1)
    for value in range(1, limit + 1):
        factorials[value] = (factorials[value - 1] * value) % modulus

    inverse_factorials = [1] * (limit + 1)
    inverse_factorials[limit] = pow(factorials[limit], modulus - 2, modulus)
    for value in range(limit, 0, -1):
        inverse_factorials[value - 1] = (inverse_factorials[value] * value) % modulus

    return ModularBinomialTable(
        modulus=modulus,
        limit=limit,
        factorials=tuple(factorials),
        inverse_factorials=tuple(inverse_factorials),
    )


def build_modular_binomial_table_for_a(a: tuple[int, ...], max_n: int, *, modulus: int) -> ModularBinomialTable:
    if max_n < 0:
        raise ValueError("max_n must be nonnegative")
    parameters = pq_parameters_from_a(scale_a_vector(a, max_n))
    return build_modular_binomial_table(modulus=modulus, limit=_required_binomial_limit(parameters))


def compute_q_term_from_a_mod(
    a: tuple[int, ...],
    n: int,
    *,
    modulus: int,
    table: ModularBinomialTable | None = None,
) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    modular_table = table if table is not None else build_modular_binomial_table_for_a(a, n, modulus=modulus)
    if modular_table.modulus != modulus:
        raise ValueError("table modulus does not match the requested modulus")
    return compute_q_from_pq_mod(
        pq_parameters_from_a(scale_a_vector(a, n)),
        table=modular_table,
    )


def compute_q_signature_from_a_mod(
    a: tuple[int, ...],
    *,
    modulus: int,
    start_index: int = 0,
    term_count: int = 8,
    table: ModularBinomialTable | None = None,
) -> tuple[int, ...]:
    if term_count <= 0:
        raise ValueError("term_count must be positive")
    max_n = start_index + term_count - 1
    modular_table = table if table is not None else build_modular_binomial_table_for_a(a, max_n, modulus=modulus)
    if modular_table.modulus != modulus:
        raise ValueError("table modulus does not match the requested modulus")
    return tuple(
        compute_q_term_from_a_mod(a, start_index + offset, modulus=modulus, table=modular_table)
        for offset in range(term_count)
    )


def compute_q_from_pq(parameters: tuple[int, ...]) -> int:
    if len(parameters) != 12:
        raise ValueError("expected 12 p/q parameters")
    p0, p1, p2, p3, p4, p5, p6, q1, q2, q3, q4, q5 = parameters
    sign = -1 if (p0 + p1 + p2 + p3 + p4 + p5 + p6) % 2 else 1
    total = 0
    k1_lo = max(p0, p1, p2)
    k1_hi = min(p1 + q1, p2 + q2)
    k2_lo = max(p6, p4, p5)
    k2_hi = min(p4 + q4, p5 + q5)
    choose_rank = p3 + q3 - p0 - p6

    for k1 in range(k1_lo, k1_hi + 1):
        left = _choose(k1, p0) * _choose(q1, k1 - p1) * _choose(q2, k1 - p2)
        if not left:
            continue
        for k2 in range(k2_lo, k2_hi + 1):
            total += (
                left
                * _choose(k2, p6)
                * _choose(k1 + k2 + q3 - p0 - p6, choose_rank)
                * _choose(q4, k2 - p4)
                * _choose(q5, k2 - p5)
            )
    return sign * total


def compute_q_from_pq_mod(parameters: tuple[int, ...], *, table: ModularBinomialTable) -> int:
    if len(parameters) != 12:
        raise ValueError("expected 12 p/q parameters")
    if _required_binomial_limit(parameters) > table.limit:
        raise ValueError("modular binomial table is too small for these parameters")

    p0, p1, p2, p3, p4, p5, p6, q1, q2, q3, q4, q5 = parameters
    choose_rank = p3 + q3 - p0 - p6
    if choose_rank < 0:
        return 0

    k1_lo = max(p0, p1, p2)
    k1_hi = min(p1 + q1, p2 + q2)
    k2_lo = max(p6, p4, p5)
    k2_hi = min(p4 + q4, p5 + q5)
    if k1_lo > k1_hi or k2_lo > k2_hi:
        return 0

    modulus = table.modulus

    def table_choose(n: int, k: int) -> int:
        return _choose_mod(table, n, k)

    left_terms = []
    for k1 in range(k1_lo, k1_hi + 1):
        left = table_choose(k1, p0)
        left = (left * table_choose(q1, k1 - p1)) % modulus
        left = (left * table_choose(q2, k1 - p2)) % modulus
        if left:
            left_terms.append((k1, left))

    right_terms = []
    for k2 in range(k2_lo, k2_hi + 1):
        right = table_choose(k2, p6)
        right = (right * table_choose(q4, k2 - p4)) % modulus
        right = (right * table_choose(q5, k2 - p5)) % modulus
        if right:
            right_terms.append((k2, right))

    if not left_terms or not right_terms:
        return 0

    central_offset = q3 - p0 - p6
    min_arg = left_terms[0][0] + right_terms[0][0] + central_offset
    max_arg = left_terms[-1][0] + right_terms[-1][0] + central_offset
    central_values = tuple(
        table_choose(argument, choose_rank) if argument >= 0 else 0
        for argument in range(min_arg, max_arg + 1)
    )

    total = 0
    for k1, left in left_terms:
        argument_base = k1 + central_offset
        for k2, right in right_terms:
            central = central_values[argument_base + k2 - min_arg]
            if central:
                total = (total + left * right * central) % modulus

    if (p0 + p1 + p2 + p3 + p4 + p5 + p6) % 2:
        return (-total) % modulus
    return total


def _choose(n: int, k: int) -> int:
    if n < 0 or k < 0 or k > n:
        return 0
    return comb(n, k)


def _choose_mod(table: ModularBinomialTable, n: int, k: int) -> int:
    if n < 0 or k < 0 or k > n:
        return 0
    if n > table.limit:
        raise ValueError("modular binomial table is too small for this lookup")
    modulus = table.modulus
    return (
        table.factorials[n]
        * table.inverse_factorials[k]
        * table.inverse_factorials[n - k]
    ) % modulus


def _required_binomial_limit(parameters: tuple[int, ...]) -> int:
    p0, p1, p2, p3, p4, p5, p6, q1, q2, q3, q4, q5 = parameters
    k1_hi = min(p1 + q1, p2 + q2)
    k2_hi = min(p4 + q4, p5 + q5)
    central_hi = k1_hi + k2_hi + q3 - p0 - p6
    return max(q1, q2, q4, q5, k1_hi, k2_hi, central_hi)
