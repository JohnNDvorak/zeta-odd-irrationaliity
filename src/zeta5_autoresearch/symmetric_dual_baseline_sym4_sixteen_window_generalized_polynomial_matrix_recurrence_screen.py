from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_sym4_sixteen_window_polynomial_matrix_recurrence_screen import (
    _fraction_to_mod,
)
from .symmetric_dual_baseline_sym4_sixteen_window_probe import (
    build_sym4_sixteen_window_probe,
    build_sym4_sixteen_window_sequences,
)

try:
    from sympy import GF
    from sympy.polys.matrices import DomainMatrix
except ImportError:  # pragma: no cover - exercised only in stripped environments.
    GF = None
    DomainMatrix = None

SYM4_SIXTEEN_WINDOW_GENERALIZED_POLYNOMIAL_MATRIX_RECURRENCE_SCREEN_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.md"
)
SYM4_SIXTEEN_WINDOW_GENERALIZED_POLYNOMIAL_MATRIX_RECURRENCE_SCREEN_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.json"
)


@dataclass(frozen=True)
class Sym4SixteenWindowGeneralizedPolynomialMatrixRecurrenceResult:
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
class Sym4SixteenWindowGeneralizedPolynomialMatrixRecurrenceScreen:
    screen_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    order_results: tuple[Sym4SixteenWindowGeneralizedPolynomialMatrixRecurrenceResult, ...]
    overall_verdict: str
    source_boundary: str
    recommendation: str


def _strictly_overdetermined_cases() -> tuple[tuple[str, int, int], ...]:
    return (
        ("homogeneous", 1, 0),
        ("homogeneous", 1, 1),
        ("homogeneous", 1, 2),
        ("homogeneous", 1, 3),
        ("homogeneous", 2, 0),
        ("homogeneous", 2, 1),
        ("homogeneous", 3, 0),
        ("homogeneous", 4, 0),
        ("affine", 1, 0),
        ("affine", 1, 1),
        ("affine", 1, 2),
        ("affine", 2, 0),
        ("affine", 2, 1),
        ("affine", 3, 0),
    )


def _unknown_count(
    *,
    family: str,
    dimension: int,
    recurrence_order: int,
    polynomial_degree: int,
) -> int:
    per_degree = 1 + recurrence_order * dimension * dimension
    if family == "affine":
        per_degree += dimension
    return per_degree * (polynomial_degree + 1)


def _generalized_witness_primes(packet_side: str) -> tuple[int, ...]:
    return (1009, 1451) if packet_side == "source" else (1451, 1009)


def _build_generalized_polynomial_matrix_rows_mod(
    vectors: tuple[tuple[int, ...], ...],
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
    per_degree = 1 + matrix_block_size
    if family == "affine":
        per_degree += dimension
    rows = []
    for index in range(len(vectors) - recurrence_order):
        target_n = window_start + index + recurrence_order
        powers = [pow(target_n, degree, prime) for degree in range(polynomial_degree + 1)]
        history = [vectors[index + offset] for offset in range(recurrence_order)]
        target = vectors[index + recurrence_order]
        for target_index in range(dimension):
            row = [0] * variable_count
            target_mod = target[target_index]
            for degree, power in enumerate(powers):
                degree_base = degree * per_degree
                row[degree_base] = (power * target_mod) % prime
                matrix_base = degree_base + 1
                for block in range(recurrence_order):
                    base = matrix_base + block * dimension * dimension + dimension * target_index
                    source_vector = history[recurrence_order - 1 - block]
                    for source_index in range(dimension):
                        row[base + source_index] = (-power * source_vector[source_index]) % prime
                if family == "affine":
                    translation_base = degree_base + 1 + matrix_block_size
                    row[translation_base + target_index] = (-power) % prime
            rows.append(row)
    return rows


def _vectors_to_mod(
    vectors: tuple[tuple[Fraction, ...], ...],
    prime: int,
) -> tuple[tuple[int, ...], ...] | None:
    rows = []
    for vector in vectors:
        mod_vector = []
        for value in vector:
            mod_value = _fraction_to_mod(value, prime)
            if mod_value is None:
                return None
            mod_vector.append(mod_value)
        rows.append(tuple(mod_vector))
    return tuple(rows)


def _rank_mod_matrix(rows: list[list[int]], variable_count: int, prime: int) -> int:
    if DomainMatrix is not None and GF is not None:
        return DomainMatrix.from_list(rows, GF(prime)).rank()

    pivot_row = 0
    for column in range(variable_count):
        pivot_index = None
        for row_index in range(pivot_row, len(rows)):
            if rows[row_index][column] % prime != 0:
                pivot_index = row_index
                break
        if pivot_index is None:
            continue
        if pivot_index != pivot_row:
            rows[pivot_row], rows[pivot_index] = rows[pivot_index], rows[pivot_row]

        pivot = rows[pivot_row][column] % prime
        inverse = pow(pivot, -1, prime)
        rows[pivot_row] = [(entry * inverse) % prime for entry in rows[pivot_row]]
        for row_index in range(pivot_row + 1, len(rows)):
            factor = rows[row_index][column] % prime
            if factor:
                rows[row_index] = [
                    (value - factor * basis) % prime
                    for value, basis in zip(rows[row_index], rows[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == variable_count or pivot_row == len(rows):
            break
    return pivot_row


def _screen_generalized_polynomial_matrix_recurrence(
    *,
    family: str,
    packet_side: str,
    vectors: tuple[tuple[Fraction, ...], ...],
    recurrence_order: int,
    polynomial_degree: int,
    window_start: int,
) -> Sym4SixteenWindowGeneralizedPolynomialMatrixRecurrenceResult:
    dimension = len(vectors[0])
    variable_count = _unknown_count(
        family=family,
        dimension=dimension,
        recurrence_order=recurrence_order,
        polynomial_degree=polynomial_degree,
    )
    equation_count = (len(vectors) - recurrence_order) * dimension
    for prime in _generalized_witness_primes(packet_side):
        vectors_mod = _vectors_to_mod(vectors, prime)
        if vectors_mod is None:
            continue
        rows = _build_generalized_polynomial_matrix_rows_mod(
            vectors_mod,
            family=family,
            recurrence_order=recurrence_order,
            polynomial_degree=polynomial_degree,
            window_start=window_start,
            prime=prime,
        )
        rank = _rank_mod_matrix(rows, variable_count, prime)
        if rank == variable_count:
            return Sym4SixteenWindowGeneralizedPolynomialMatrixRecurrenceResult(
                family=family,
                packet_side=packet_side,
                recurrence_order=recurrence_order,
                polynomial_degree=polynomial_degree,
                matrix_size=dimension,
                equation_count=equation_count,
                unknown_count=variable_count,
                verdict="full_column_rank_mod_prime",
                witness_prime=prime,
            )
    return Sym4SixteenWindowGeneralizedPolynomialMatrixRecurrenceResult(
        family=family,
        packet_side=packet_side,
        recurrence_order=recurrence_order,
        polynomial_degree=polynomial_degree,
        matrix_size=dimension,
        equation_count=equation_count,
        unknown_count=variable_count,
        verdict="no_full_rank_obstruction_found",
        witness_prime=None,
    )


@lru_cache(maxsize=1)
def build_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen() -> (
    Sym4SixteenWindowGeneralizedPolynomialMatrixRecurrenceScreen
):
    probe = build_sym4_sixteen_window_probe()
    source, target = build_sym4_sixteen_window_sequences()

    results = []
    for family, recurrence_order, polynomial_degree in _strictly_overdetermined_cases():
        for packet_side, vectors in (("source", source), ("target", target)):
            results.append(
                _screen_generalized_polynomial_matrix_recurrence(
                    family=family,
                    packet_side=packet_side,
                    vectors=vectors,
                    recurrence_order=recurrence_order,
                    polynomial_degree=polynomial_degree,
                    window_start=probe.shared_window_start,
                )
            )

    any_open = any(item.verdict == "no_full_rank_obstruction_found" for item in results)
    return Sym4SixteenWindowGeneralizedPolynomialMatrixRecurrenceScreen(
        screen_id="bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        order_results=tuple(results),
        overall_verdict=(
            "sym4_sixteen_window_generalized_polynomial_matrix_recurrence_requires_exact_followup"
            if any_open
            else "generalized_polynomial_matrix_recurrence_exhausted_over_overdetermined_range"
        ),
        source_boundary=probe.source_boundary,
        recommendation=(
            "A full-rank modular obstruction was not found for at least one generalized polynomial matrix case; exact follow-up is required before banking this family as exhausted."
            if any_open
            else "Do not escalate generalized polynomial matrix order or degree mechanically. The remaining cases are no longer strict overdetermined obstruction screens."
        ),
    )


def render_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen() -> str:
    screen = build_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen()
    lines = [
        "# Phase 2 Sym^4-lifted sixteen-window generalized polynomial matrix recurrence screen",
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
            "This screen tests non-monic matrix-valued recurrences whose coefficients are low-degree polynomials in the target index `n`. Unlike the monic polynomial matrix screen, this family also allows a scalar polynomial coefficient on the target vector. It is closer to the usual P-recursive shape while still staying within strict overdetermined cases.",
            "",
            "## Cases",
            "",
            "- Homogeneous: `(order, degree) = (1, 0)`, `(1, 1)`, `(1, 2)`, `(1, 3)`, `(2, 0)`, `(2, 1)`, `(3, 0)`, and `(4, 0)`.",
            "- Affine: `(order, degree) = (1, 0)`, `(1, 1)`, `(1, 2)`, `(2, 0)`, `(2, 1)`, and `(3, 0)`.",
            "",
            "## Boundary",
            "",
            "- Homogeneous `(order, degree) = (1, 4)` would have `1130` unknowns against `960` equations.",
            "- Homogeneous `(order, degree) = (2, 2)` would have `1353` unknowns against `945` equations.",
            "- Homogeneous `(order, degree) = (3, 1)` would have `1352` unknowns against `930` equations.",
            "- Affine `(order, degree) = (1, 3)` would have `964` unknowns against `960` equations.",
            "- Affine `(order, degree) = (2, 2)` would have `1398` unknowns against `945` equations.",
            "- Affine `(order, degree) = (3, 1)` would have `1382` unknowns against `930` equations.",
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


def write_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen_report(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_GENERALIZED_POLYNOMIAL_MATRIX_RECURRENCE_SCREEN_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen(), encoding="utf-8")
    return output


def write_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen_json(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_GENERALIZED_POLYNOMIAL_MATRIX_RECURRENCE_SCREEN_JSON_PATH,
) -> Path:
    screen = build_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(screen), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen_report()
    write_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen_json()


if __name__ == "__main__":
    main()
