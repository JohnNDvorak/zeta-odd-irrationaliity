from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_eight_window_plucker_probe import (
    build_eight_window_normalized_plucker_probe,
    build_eight_window_normalized_plucker_sequences,
)

EIGHT_WINDOW_NORMALIZED_PLUCKER_MATRIX_RECURRENCE_SCREEN_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen.md"
)
EIGHT_WINDOW_NORMALIZED_PLUCKER_MATRIX_RECURRENCE_SCREEN_JSON_PATH = (
    CACHE_DIR / "bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen.json"
)


@dataclass(frozen=True)
class EightWindowNormalizedPluckerMatrixRecurrenceResult:
    packet_side: str
    recurrence_order: int
    matrix_size: int
    equation_count: int
    unknown_count: int
    verdict: str
    witness_prime: int | None


@dataclass(frozen=True)
class EightWindowNormalizedPluckerMatrixRecurrenceScreen:
    screen_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    order_results: tuple[EightWindowNormalizedPluckerMatrixRecurrenceResult, ...]
    overall_verdict: str
    source_boundary: str
    recommendation: str


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def _matrix_recurrence_witness_primes() -> tuple[int, ...]:
    return tuple(prime for prime in range(1009, 5000) if _is_prime(prime))


def _row_reduce_mod_prime(rows: tuple[tuple[Fraction, ...], ...], prime: int) -> bool | None:
    variable_count = len(rows[0]) - 1
    matrix: list[list[int]] = []
    for row in rows:
        mod_row: list[int] = []
        for value in row:
            numerator = value.numerator % prime
            denominator = value.denominator % prime
            if denominator == 0:
                return None
            mod_row.append((numerator * pow(denominator, -1, prime)) % prime)
        matrix.append(mod_row)

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


def _build_matrix_recurrence_rows(
    vectors: tuple[tuple[Fraction, ...], ...],
    recurrence_order: int,
) -> tuple[tuple[Fraction, ...], ...]:
    dimension = len(vectors[0])
    rows = []
    for index in range(len(vectors) - recurrence_order):
        history = [vectors[index + offset] for offset in range(recurrence_order)]
        target = vectors[index + recurrence_order]
        for target_index in range(dimension):
            row = [Fraction(0)] * (recurrence_order * dimension * dimension) + [-target[target_index]]
            for block in range(recurrence_order):
                base = block * dimension * dimension + dimension * target_index
                source_vector = history[recurrence_order - 1 - block]
                for source_index in range(dimension):
                    row[base + source_index] = source_vector[source_index]
            rows.append(tuple(row))
    return tuple(rows)


def _screen_matrix_recurrence(
    *,
    packet_side: str,
    vectors: tuple[tuple[Fraction, ...], ...],
    recurrence_order: int,
) -> EightWindowNormalizedPluckerMatrixRecurrenceResult:
    dimension = len(vectors[0])
    rows = _build_matrix_recurrence_rows(vectors, recurrence_order)
    for prime in _matrix_recurrence_witness_primes():
        inconsistent = _row_reduce_mod_prime(rows, prime)
        if inconsistent is None:
            continue
        if inconsistent:
            return EightWindowNormalizedPluckerMatrixRecurrenceResult(
                packet_side=packet_side,
                recurrence_order=recurrence_order,
                matrix_size=dimension,
                equation_count=len(rows),
                unknown_count=recurrence_order * dimension * dimension,
                verdict="inconsistent_mod_prime",
                witness_prime=prime,
            )
    return EightWindowNormalizedPluckerMatrixRecurrenceResult(
        packet_side=packet_side,
        recurrence_order=recurrence_order,
        matrix_size=dimension,
        equation_count=len(rows),
        unknown_count=recurrence_order * dimension * dimension,
        verdict="no_modular_obstruction_found",
        witness_prime=None,
    )


@lru_cache(maxsize=1)
def build_eight_window_normalized_plucker_matrix_recurrence_screen() -> (
    EightWindowNormalizedPluckerMatrixRecurrenceScreen
):
    probe = build_eight_window_normalized_plucker_probe()
    source, target = build_eight_window_normalized_plucker_sequences()

    results = []
    for packet_side, vectors in (("source", source), ("target", target)):
        results.append(
            _screen_matrix_recurrence(
                packet_side=packet_side,
                vectors=vectors,
                recurrence_order=1,
            )
        )

    any_open = any(item.verdict == "no_modular_obstruction_found" for item in results)
    return EightWindowNormalizedPluckerMatrixRecurrenceScreen(
        screen_id="bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        order_results=tuple(results),
        overall_verdict=(
            "eight_window_matrix_recurrence_requires_exact_followup"
            if any_open
            else "order1_matrix_recurrence_exhausted"
        ),
        source_boundary=probe.source_boundary,
        recommendation=(
            "A modular obstruction was not found on at least one side/order; exact follow-up is required before banking the eight-window matrix screen as exhausted."
            if any_open
            else "Do not keep increasing matrix recurrence order mechanically. Order 2 is already underdetermined on this object, so the next move must be a different nonlocal family or a different wider invariant."
        ),
    )


def render_eight_window_normalized_plucker_matrix_recurrence_screen() -> str:
    screen = build_eight_window_normalized_plucker_matrix_recurrence_screen()
    lines = [
        "# Phase 2 eight-window normalized Plucker matrix recurrence screen",
        "",
        f"- Screen id: `{screen.screen_id}`",
        f"- Source probe id: `{screen.source_probe_id}`",
        f"- Shared exact window: `n={screen.shared_window_start}..{screen.shared_window_end}`",
        f"- Overall verdict: `{screen.overall_verdict}`",
        "",
        "| side | recurrence order | matrix size | equation count | unknown count | verdict | witness prime |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in screen.order_results:
        lines.append(
            f"| `{item.packet_side}` | `{item.recurrence_order}` | `{item.matrix_size}` | `{item.equation_count}` | "
            f"`{item.unknown_count}` | `{item.verdict}` | `{item.witness_prime}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This screen tests the last overdetermined constant matrix-valued recurrence on the eight-window normalized Plucker sequence, separately on the source and target side. Order `2` is already underdetermined on this object.",
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


def write_eight_window_normalized_plucker_matrix_recurrence_screen_report(
    output_path: str | Path = EIGHT_WINDOW_NORMALIZED_PLUCKER_MATRIX_RECURRENCE_SCREEN_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_eight_window_normalized_plucker_matrix_recurrence_screen(), encoding="utf-8")
    return output


def write_eight_window_normalized_plucker_matrix_recurrence_screen_json(
    output_path: str | Path = EIGHT_WINDOW_NORMALIZED_PLUCKER_MATRIX_RECURRENCE_SCREEN_JSON_PATH,
) -> Path:
    screen = build_eight_window_normalized_plucker_matrix_recurrence_screen()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(screen), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_eight_window_normalized_plucker_matrix_recurrence_screen_report()
    write_eight_window_normalized_plucker_matrix_recurrence_screen_json()


if __name__ == "__main__":
    main()
