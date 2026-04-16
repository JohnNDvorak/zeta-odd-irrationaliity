from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_sym4_sixteen_window_matrix_recurrence_screen import (
    _matrix_recurrence_witness_primes,
)
from .symmetric_dual_baseline_sym4_sixteen_window_probe import (
    build_sym4_sixteen_window_probe,
    build_sym4_sixteen_window_sequences,
)

SYM4_SIXTEEN_WINDOW_POLYNOMIAL_MATRIX_RECURRENCE_SCREEN_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym4_sixteen_window_polynomial_matrix_recurrence_screen.md"
)
SYM4_SIXTEEN_WINDOW_POLYNOMIAL_MATRIX_RECURRENCE_SCREEN_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym4_sixteen_window_polynomial_matrix_recurrence_screen.json"
)


@dataclass(frozen=True)
class Sym4SixteenWindowPolynomialMatrixRecurrenceResult:
    family: str
    packet_side: str
    recurrence_order: int
    polynomial_degree: int
    matrix_size: int
    equation_count: int
    unknown_count: int
    verdict: str
    witness_prime: int | None


@dataclass(frozen=True)
class Sym4SixteenWindowPolynomialMatrixRecurrenceScreen:
    screen_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    order_results: tuple[Sym4SixteenWindowPolynomialMatrixRecurrenceResult, ...]
    overall_verdict: str
    source_boundary: str
    recommendation: str


def _strictly_overdetermined_cases() -> tuple[tuple[str, int, int], ...]:
    return (
        ("homogeneous", 1, 1),
        ("homogeneous", 1, 2),
        ("homogeneous", 1, 3),
        ("homogeneous", 2, 1),
        ("affine", 1, 1),
        ("affine", 1, 2),
        ("affine", 2, 1),
    )


def _unknown_count(
    *,
    family: str,
    dimension: int,
    recurrence_order: int,
    polynomial_degree: int,
) -> int:
    per_degree = recurrence_order * dimension * dimension
    if family == "affine":
        per_degree += dimension
    return per_degree * (polynomial_degree + 1)


def _polynomial_witness_primes(packet_side: str) -> tuple[int, ...]:
    preferred = (1009, 1451) if packet_side == "source" else (1451, 1009)
    fallback = tuple(prime for prime in _matrix_recurrence_witness_primes() if prime not in preferred)
    return preferred + fallback


def _fraction_to_mod(value: Fraction, prime: int) -> int | None:
    denominator = value.denominator % prime
    if denominator == 0:
        return None
    return (value.numerator % prime) * pow(denominator, -1, prime) % prime


def _build_polynomial_matrix_recurrence_rows_mod(
    vectors: tuple[tuple[Fraction, ...], ...],
    *,
    family: str,
    recurrence_order: int,
    polynomial_degree: int,
    window_start: int,
    prime: int,
) -> list[list[int]] | None:
    dimension = len(vectors[0])
    variable_count = _unknown_count(
        family=family,
        dimension=dimension,
        recurrence_order=recurrence_order,
        polynomial_degree=polynomial_degree,
    )
    matrix_block_size = recurrence_order * dimension * dimension
    rows = []
    for index in range(len(vectors) - recurrence_order):
        target_n = window_start + index + recurrence_order
        powers = [pow(target_n, degree, prime) for degree in range(polynomial_degree + 1)]
        history = [vectors[index + offset] for offset in range(recurrence_order)]
        target = vectors[index + recurrence_order]
        for target_index in range(dimension):
            target_mod = _fraction_to_mod(target[target_index], prime)
            if target_mod is None:
                return None
            row = [0] * variable_count + [(-target_mod) % prime]
            for degree, power in enumerate(powers):
                degree_base = degree * matrix_block_size
                for block in range(recurrence_order):
                    base = degree_base + block * dimension * dimension + dimension * target_index
                    source_vector = history[recurrence_order - 1 - block]
                    for source_index in range(dimension):
                        source_mod = _fraction_to_mod(source_vector[source_index], prime)
                        if source_mod is None:
                            return None
                        row[base + source_index] = (power * source_mod) % prime
                if family == "affine":
                    translation_base = matrix_block_size * (polynomial_degree + 1) + degree * dimension
                    row[translation_base + target_index] = power
            rows.append(row)
    return rows


def _row_reduce_mod_matrix(matrix: list[list[int]], variable_count: int, prime: int) -> bool:
    pivot_row = 0
    for column in range(variable_count):
        pivot_index = None
        for row_index in range(pivot_row, len(matrix)):
            if matrix[row_index][column] % prime != 0:
                pivot_index = row_index
                break
        if pivot_index is None:
            continue
        if pivot_index != pivot_row:
            matrix[pivot_row], matrix[pivot_index] = matrix[pivot_index], matrix[pivot_row]

        pivot = matrix[pivot_row][column] % prime
        inverse = pow(pivot, -1, prime)
        matrix[pivot_row] = [(entry * inverse) % prime for entry in matrix[pivot_row]]
        for row_index in range(len(matrix)):
            if row_index == pivot_row:
                continue
            factor = matrix[row_index][column] % prime
            if factor:
                matrix[row_index] = [
                    (value - factor * basis) % prime
                    for value, basis in zip(matrix[row_index], matrix[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break

    for row in matrix:
        if all(value % prime == 0 for value in row[:variable_count]) and (row[variable_count] % prime != 0):
            return True
    return False


def _screen_polynomial_matrix_recurrence(
    *,
    family: str,
    packet_side: str,
    vectors: tuple[tuple[Fraction, ...], ...],
    recurrence_order: int,
    polynomial_degree: int,
    window_start: int,
) -> Sym4SixteenWindowPolynomialMatrixRecurrenceResult:
    dimension = len(vectors[0])
    variable_count = _unknown_count(
        family=family,
        dimension=dimension,
        recurrence_order=recurrence_order,
        polynomial_degree=polynomial_degree,
    )
    equation_count = (len(vectors) - recurrence_order) * dimension
    for prime in _polynomial_witness_primes(packet_side):
        rows = _build_polynomial_matrix_recurrence_rows_mod(
            vectors,
            family=family,
            recurrence_order=recurrence_order,
            polynomial_degree=polynomial_degree,
            window_start=window_start,
            prime=prime,
        )
        if rows is None:
            continue
        inconsistent = _row_reduce_mod_matrix(rows, variable_count, prime)
        if inconsistent:
            return Sym4SixteenWindowPolynomialMatrixRecurrenceResult(
                family=family,
                packet_side=packet_side,
                recurrence_order=recurrence_order,
                polynomial_degree=polynomial_degree,
                matrix_size=dimension,
                equation_count=equation_count,
                unknown_count=variable_count,
                verdict="inconsistent_mod_prime",
                witness_prime=prime,
            )
    return Sym4SixteenWindowPolynomialMatrixRecurrenceResult(
        family=family,
        packet_side=packet_side,
        recurrence_order=recurrence_order,
        polynomial_degree=polynomial_degree,
        matrix_size=dimension,
        equation_count=equation_count,
        unknown_count=variable_count,
        verdict="no_modular_obstruction_found",
        witness_prime=None,
    )


@lru_cache(maxsize=1)
def build_sym4_sixteen_window_polynomial_matrix_recurrence_screen() -> (
    Sym4SixteenWindowPolynomialMatrixRecurrenceScreen
):
    probe = build_sym4_sixteen_window_probe()
    source, target = build_sym4_sixteen_window_sequences()

    results = []
    for family, recurrence_order, polynomial_degree in _strictly_overdetermined_cases():
        for packet_side, vectors in (("source", source), ("target", target)):
            results.append(
                _screen_polynomial_matrix_recurrence(
                    family=family,
                    packet_side=packet_side,
                    vectors=vectors,
                    recurrence_order=recurrence_order,
                    polynomial_degree=polynomial_degree,
                    window_start=probe.shared_window_start,
                )
            )

    any_open = any(item.verdict == "no_modular_obstruction_found" for item in results)
    return Sym4SixteenWindowPolynomialMatrixRecurrenceScreen(
        screen_id="bz_phase2_sym4_sixteen_window_polynomial_matrix_recurrence_screen",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        order_results=tuple(results),
        overall_verdict=(
            "sym4_sixteen_window_polynomial_matrix_recurrence_requires_exact_followup"
            if any_open
            else "low_degree_polynomial_matrix_recurrence_exhausted_over_overdetermined_range"
        ),
        source_boundary=probe.source_boundary,
        recommendation=(
            "A modular obstruction was not found for at least one polynomial matrix case; exact follow-up is required before banking this polynomial-coefficient family as exhausted."
            if any_open
            else "Do not escalate polynomial degree or recurrence order mechanically. The remaining polynomial matrix cases are no longer strict overdetermined obstruction screens."
        ),
    )


def render_sym4_sixteen_window_polynomial_matrix_recurrence_screen() -> str:
    screen = build_sym4_sixteen_window_polynomial_matrix_recurrence_screen()
    lines = [
        "# Phase 2 Sym^4-lifted sixteen-window polynomial matrix recurrence screen",
        "",
        f"- Screen id: `{screen.screen_id}`",
        f"- Source probe id: `{screen.source_probe_id}`",
        f"- Shared exact window: `n={screen.shared_window_start}..{screen.shared_window_end}`",
        f"- Overall verdict: `{screen.overall_verdict}`",
        "",
        "| family | side | recurrence order | polynomial degree | matrix size | equation count | unknown count | verdict | witness prime |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in screen.order_results:
        lines.append(
            f"| `{item.family}` | `{item.packet_side}` | `{item.recurrence_order}` | `{item.polynomial_degree}` | "
            f"`{item.matrix_size}` | `{item.equation_count}` | `{item.unknown_count}` | `{item.verdict}` | `{item.witness_prime}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This screen tests matrix-valued recurrences whose coefficients are low-degree polynomials in the target index `n`, on the Sym^4-lifted sixteen-window normalized maximal-minor sequence. It only includes cases that remain strict overdetermined after the constant-coefficient matrix ladders have closed.",
            "",
            "## Cases",
            "",
            "- Homogeneous: `(order, degree) = (1, 1)`, `(1, 2)`, `(1, 3)`, and `(2, 1)`.",
            "- Affine: `(order, degree) = (1, 1)`, `(1, 2)`, and `(2, 1)`.",
            "",
            "## Boundary",
            "",
            "- Homogeneous `(order, degree) = (1, 4)` would have `1125` unknowns against `960` equations.",
            "- Homogeneous `(order, degree) = (2, 2)` would have `1350` unknowns against `945` equations.",
            "- Affine `(order, degree) = (1, 3)` would have `960` unknowns against `960` equations.",
            "- Affine `(order, degree) = (2, 2)` would have `1395` unknowns against `945` equations.",
            "",
            "## Source boundary",
            "",
            screen.source_boundary,
            "",
            "## Recommendation",
            "",
            screen.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_sym4_sixteen_window_polynomial_matrix_recurrence_screen_report(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_POLYNOMIAL_MATRIX_RECURRENCE_SCREEN_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym4_sixteen_window_polynomial_matrix_recurrence_screen(), encoding="utf-8")
    return output


def write_sym4_sixteen_window_polynomial_matrix_recurrence_screen_json(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_POLYNOMIAL_MATRIX_RECURRENCE_SCREEN_JSON_PATH,
) -> Path:
    screen = build_sym4_sixteen_window_polynomial_matrix_recurrence_screen()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(screen), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym4_sixteen_window_polynomial_matrix_recurrence_screen_report()
    write_sym4_sixteen_window_polynomial_matrix_recurrence_screen_json()


if __name__ == "__main__":
    main()
