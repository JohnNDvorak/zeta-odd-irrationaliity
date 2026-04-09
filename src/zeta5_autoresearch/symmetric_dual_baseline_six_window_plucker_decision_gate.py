from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_six_window_plucker_family_probe import (
    SIX_WINDOW_NORMALIZED_PLUCKER_FAMILY_PROBE_REPORT_PATH,
    build_six_window_normalized_plucker_family_probe,
)

SIX_WINDOW_NORMALIZED_PLUCKER_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_six_window_normalized_plucker_decision_gate.md"
)
SIX_WINDOW_NORMALIZED_PLUCKER_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_six_window_normalized_plucker_decision_gate.json"
)


@dataclass(frozen=True)
class SixWindowNormalizedPluckerStatus:
    family_id: str
    verdict: str
    note: str


@dataclass(frozen=True)
class SixWindowNormalizedPluckerDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[SixWindowNormalizedPluckerStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    pivot_options: tuple[str, ...]
    source_boundary: str


def build_six_window_normalized_plucker_decision_gate() -> SixWindowNormalizedPluckerDecisionGate:
    probe = build_six_window_normalized_plucker_family_probe()
    support1 = next(item for item in probe.family_results if item.family_id == "support1_free_zero_six_plucker_map")
    winner_exists = any(item.verdict == "holds_on_full_window" for item in probe.family_results)

    if winner_exists:
        outcome = "continue_six_window_plucker_v2"
        rationale = "At least one bounded recurrence-level family holds on the full six-window validation window."
        next_step = "Promote the winning family into the next six-window frontier artifact."
    elif support1.verdict == "inconsistent_fit_block":
        outcome = "hard_wall_six_window_plucker_support1_inconsistent"
        rationale = (
            "The cheap constant/difference families fail, and the canonical free-zero support-1 family is already inconsistent on the initial fit block."
        )
        next_step = "Stop this family ladder and choose a genuinely different recurrence-level family on the same six-window object."
    else:
        outcome = "hard_wall_six_window_plucker_free_zero_family_exhausted"
        rationale = (
            "The cheap constant/difference families fail, and the canonical free-zero support-1 family also fails after fitting. "
            "That means the six-window object survives as the frontier, but this recurrence family does not justify further escalation."
        )
        next_step = "Keep the six-window object, but pivot to a different recurrence-level family rather than another support-depth escalation."

    return SixWindowNormalizedPluckerDecisionGate(
        gate_id="bz_phase2_six_window_normalized_plucker_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=tuple(
            SixWindowNormalizedPluckerStatus(
                family_id=item.family_id,
                verdict=item.verdict,
                note=item.note,
            )
            for item in probe.family_results
        ),
        outcome=outcome,
        rationale=rationale,
        next_step=next_step,
        pivot_options=(
            "different_recurrence_family_on_six_window_plucker",
            "different_wider_window_nonlinear_object",
        ),
        source_boundary=probe.source_boundary,
    )


def render_six_window_normalized_plucker_decision_gate() -> str:
    gate = build_six_window_normalized_plucker_decision_gate()
    lines = [
        "# Phase 2 six-window normalized Plucker decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{SIX_WINDOW_NORMALIZED_PLUCKER_FAMILY_PROBE_REPORT_PATH}`",
        f"- Source probe id: `{gate.source_probe_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        f"- Outcome: `{gate.outcome}`",
        "",
        "| family | verdict | note |",
        "| --- | --- | --- |",
    ]
    for item in gate.statuses:
        lines.append(f"| `{item.family_id}` | `{item.verdict}` | {item.note} |")
    lines.extend(
        [
            "",
            "## Rationale",
            "",
            gate.rationale,
            "",
            "## Next step",
            "",
            gate.next_step,
            "",
            "## Source boundary",
            "",
            gate.source_boundary,
            "",
            "## Pivot options",
            "",
        ]
    )
    for item in gate.pivot_options:
        lines.append(f"- `{item}`")
    lines.append("")
    return "\n".join(lines)


def write_six_window_normalized_plucker_decision_gate_report(
    output_path: str | Path = SIX_WINDOW_NORMALIZED_PLUCKER_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_six_window_normalized_plucker_decision_gate(), encoding="utf-8")
    return output


def write_six_window_normalized_plucker_decision_gate_json(
    output_path: str | Path = SIX_WINDOW_NORMALIZED_PLUCKER_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_six_window_normalized_plucker_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_six_window_normalized_plucker_decision_gate_report()
    write_six_window_normalized_plucker_decision_gate_json()


if __name__ == "__main__":
    main()
