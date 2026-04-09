from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_packet_local_annihilator_profile import solve_exact_linear_system_with_zero_free_variables
from .symmetric_dual_baseline_six_window_plucker_probe import (
    build_six_window_normalized_plucker_probe,
    build_six_window_normalized_plucker_sequences,
)

SIX_WINDOW_NORMALIZED_PLUCKER_ANNIHILATOR_SCREEN_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_six_window_normalized_plucker_annihilator_screen.md"
)
SIX_WINDOW_NORMALIZED_PLUCKER_ANNIHILATOR_SCREEN_JSON_PATH = (
    CACHE_DIR / "bz_phase2_six_window_normalized_plucker_annihilator_screen.json"
)


PluckerVector = tuple[object, ...]


@dataclass(frozen=True)
class SixWindowNormalizedPluckerAnnihilatorOrderResult:
    packet_side: str
    relation_length: int
    window_count: int
    first_inconsistent_index: int | None
    first_nonunique_index: int | None
    verdict: str


@dataclass(frozen=True)
class SixWindowNormalizedPluckerAnnihilatorScreen:
    screen_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    order_results: tuple[SixWindowNormalizedPluckerAnnihilatorOrderResult, ...]
    overall_verdict: str
    source_boundary: str
    recommendation: str


def _screen_side(
    *,
    packet_side: str,
    vectors: tuple[tuple[object, ...], ...],
    history_length: int,
) -> SixWindowNormalizedPluckerAnnihilatorOrderResult:
    first_inconsistent = None
    first_nonunique = None
    window_count = len(vectors) - history_length
    for index in range(window_count):
        history = vectors[index : index + history_length]
        target = vectors[index + history_length]
        rows = tuple(
            tuple(history[k][dimension] for k in range(history_length)) + (-target[dimension],)
            for dimension in range(len(target))
        )
        solved = solve_exact_linear_system_with_zero_free_variables(rows)
        if solved is None:
            first_inconsistent = index + 1
            break
        _, _, nullity = solved
        if (nullity > 0) and (first_nonunique is None):
            first_nonunique = index + 1

    verdict = "screen_passes" if (first_inconsistent is None and first_nonunique is None) else "screen_fails"
    return SixWindowNormalizedPluckerAnnihilatorOrderResult(
        packet_side=packet_side,
        relation_length=history_length + 1,
        window_count=window_count,
        first_inconsistent_index=first_inconsistent,
        first_nonunique_index=first_nonunique,
        verdict=verdict,
    )


def build_six_window_normalized_plucker_annihilator_screen() -> SixWindowNormalizedPluckerAnnihilatorScreen:
    probe = build_six_window_normalized_plucker_probe()
    source, target = build_six_window_normalized_plucker_sequences()
    results = []
    for history_length in (3, 4, 5):
        results.append(_screen_side(packet_side="source", vectors=source, history_length=history_length))
        results.append(_screen_side(packet_side="target", vectors=target, history_length=history_length))

    any_pass = any(item.verdict == "screen_passes" for item in results)
    return SixWindowNormalizedPluckerAnnihilatorScreen(
        screen_id="bz_phase2_six_window_normalized_plucker_annihilator_screen",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        order_results=tuple(results),
        overall_verdict=(
            "short_order_local_annihilator_family_survives"
            if any_pass
            else "short_order_local_annihilator_family_exhausted_up_to_order_6"
        ),
        source_boundary=probe.source_boundary,
        recommendation=(
            "Do not keep enlarging short local annihilator order on the six-window normalized Plucker object without a new structural reason."
        ),
    )


def render_six_window_normalized_plucker_annihilator_screen() -> str:
    screen = build_six_window_normalized_plucker_annihilator_screen()
    lines = [
        "# Phase 2 six-window normalized Plucker annihilator screen",
        "",
        f"- Screen id: `{screen.screen_id}`",
        f"- Source probe id: `{screen.source_probe_id}`",
        f"- Shared exact window: `n={screen.shared_window_start}..{screen.shared_window_end}`",
        f"- Overall verdict: `{screen.overall_verdict}`",
        "",
        "| side | relation length | window count | first inconsistent index | first nonunique index | verdict |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in screen.order_results:
        lines.append(
            f"| `{item.packet_side}` | `{item.relation_length}` | `{item.window_count}` | "
            f"`{item.first_inconsistent_index}` | `{item.first_nonunique_index}` | `{item.verdict}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This screen tests short-order local annihilator families directly on the six-window normalized Plucker sequence itself, not on transfer-map residuals.",
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


def write_six_window_normalized_plucker_annihilator_screen_report(
    output_path: str | Path = SIX_WINDOW_NORMALIZED_PLUCKER_ANNIHILATOR_SCREEN_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_six_window_normalized_plucker_annihilator_screen(), encoding="utf-8")
    return output


def write_six_window_normalized_plucker_annihilator_screen_json(
    output_path: str | Path = SIX_WINDOW_NORMALIZED_PLUCKER_ANNIHILATOR_SCREEN_JSON_PATH,
) -> Path:
    screen = build_six_window_normalized_plucker_annihilator_screen()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(screen), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_six_window_normalized_plucker_annihilator_screen_report()
    write_six_window_normalized_plucker_annihilator_screen_json()


if __name__ == "__main__":
    main()
