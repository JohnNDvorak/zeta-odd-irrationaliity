from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_packet_local_annihilator_profile import solve_exact_linear_system_with_zero_free_variables
from .models import fraction_to_canonical_string
from .symmetric_dual_baseline_six_window_plucker_probe import (
    build_six_window_normalized_plucker_probe,
    build_six_window_normalized_plucker_sequences,
)

SIX_WINDOW_NORMALIZED_PLUCKER_GLOBAL_RECURRENCE_SCREEN_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_six_window_normalized_plucker_global_recurrence_screen.md"
)
SIX_WINDOW_NORMALIZED_PLUCKER_GLOBAL_RECURRENCE_SCREEN_JSON_PATH = (
    CACHE_DIR / "bz_phase2_six_window_normalized_plucker_global_recurrence_screen.json"
)


@dataclass(frozen=True)
class SixWindowNormalizedPluckerGlobalRecurrenceOrderResult:
    packet_side: str
    recurrence_order: int
    equation_count: int
    verdict: str
    rank: int | None
    nullity: int | None
    coefficient_preview: tuple[str, ...]


@dataclass(frozen=True)
class SixWindowNormalizedPluckerGlobalRecurrenceScreen:
    screen_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    order_results: tuple[SixWindowNormalizedPluckerGlobalRecurrenceOrderResult, ...]
    overall_verdict: str
    source_boundary: str
    recommendation: str


def _solve_global_recurrence(
    *,
    packet_side: str,
    vectors: tuple[tuple[object, ...], ...],
    order: int,
) -> SixWindowNormalizedPluckerGlobalRecurrenceOrderResult:
    rows = []
    for index in range(len(vectors) - order):
        for dimension in range(len(vectors[0])):
            row = [vectors[index + offset][dimension] for offset in range(order)]
            row.append(-vectors[index + order][dimension])
            rows.append(tuple(row))

    solved = solve_exact_linear_system_with_zero_free_variables(tuple(rows))
    if solved is None:
        return SixWindowNormalizedPluckerGlobalRecurrenceOrderResult(
            packet_side=packet_side,
            recurrence_order=order,
            equation_count=len(rows),
            verdict="inconsistent",
            rank=None,
            nullity=None,
            coefficient_preview=tuple(),
        )

    solution, rank, nullity = solved
    return SixWindowNormalizedPluckerGlobalRecurrenceOrderResult(
        packet_side=packet_side,
        recurrence_order=order,
        equation_count=len(rows),
        verdict="consistent",
        rank=rank,
        nullity=nullity,
        coefficient_preview=tuple(fraction_to_canonical_string(value) for value in solution[: min(4, len(solution))]),
    )


@lru_cache(maxsize=1)
def build_six_window_normalized_plucker_global_recurrence_screen() -> (
    SixWindowNormalizedPluckerGlobalRecurrenceScreen
):
    probe = build_six_window_normalized_plucker_probe()
    source, target = build_six_window_normalized_plucker_sequences()

    results = []
    for order in range(2, 11):
        results.append(_solve_global_recurrence(packet_side="source", vectors=source, order=order))
        results.append(_solve_global_recurrence(packet_side="target", vectors=target, order=order))

    any_consistent = any(item.verdict == "consistent" for item in results)
    return SixWindowNormalizedPluckerGlobalRecurrenceScreen(
        screen_id="bz_phase2_six_window_normalized_plucker_global_recurrence_screen",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        order_results=tuple(results),
        overall_verdict=(
            "low_order_global_vector_recurrence_survives"
            if any_consistent
            else "low_order_global_vector_recurrence_exhausted_through_order_10"
        ),
        source_boundary=probe.source_boundary,
        recommendation=(
            "Do not keep enlarging low-order global shared-scalar vector recurrence order on the six-window normalized Plucker object without a new structural reason."
        ),
    )


def render_six_window_normalized_plucker_global_recurrence_screen() -> str:
    screen = build_six_window_normalized_plucker_global_recurrence_screen()
    lines = [
        "# Phase 2 six-window normalized Plucker global recurrence screen",
        "",
        f"- Screen id: `{screen.screen_id}`",
        f"- Source probe id: `{screen.source_probe_id}`",
        f"- Shared exact window: `n={screen.shared_window_start}..{screen.shared_window_end}`",
        f"- Overall verdict: `{screen.overall_verdict}`",
        "",
        "| side | order | equation count | verdict | rank | nullity | coefficient preview |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in screen.order_results:
        preview = ", ".join(item.coefficient_preview)
        lines.append(
            f"| `{item.packet_side}` | `{item.recurrence_order}` | `{item.equation_count}` | `{item.verdict}` | "
            f"`{item.rank}` | `{item.nullity}` | `{preview}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This screen tests whether the full six-window normalized Plucker sequence satisfies a single global shared-scalar vector recurrence at low order, separately on the source and target side.",
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


def write_six_window_normalized_plucker_global_recurrence_screen_report(
    output_path: str | Path = SIX_WINDOW_NORMALIZED_PLUCKER_GLOBAL_RECURRENCE_SCREEN_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_six_window_normalized_plucker_global_recurrence_screen(), encoding="utf-8")
    return output


def write_six_window_normalized_plucker_global_recurrence_screen_json(
    output_path: str | Path = SIX_WINDOW_NORMALIZED_PLUCKER_GLOBAL_RECURRENCE_SCREEN_JSON_PATH,
) -> Path:
    screen = build_six_window_normalized_plucker_global_recurrence_screen()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(screen), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_six_window_normalized_plucker_global_recurrence_screen_report()
    write_six_window_normalized_plucker_global_recurrence_screen_json()


if __name__ == "__main__":
    main()
