from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_eight_window_plucker_matrix_recurrence_screen import (
    EIGHT_WINDOW_NORMALIZED_PLUCKER_MATRIX_RECURRENCE_SCREEN_REPORT_PATH,
    build_eight_window_normalized_plucker_matrix_recurrence_screen,
)

EIGHT_WINDOW_NORMALIZED_PLUCKER_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_eight_window_normalized_plucker_decision_gate.md"
)
EIGHT_WINDOW_NORMALIZED_PLUCKER_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_eight_window_normalized_plucker_decision_gate.json"
)


@dataclass(frozen=True)
class EightWindowNormalizedPluckerStatus:
    packet_side: str
    recurrence_order: int
    verdict: str
    witness_prime: int | None


@dataclass(frozen=True)
class EightWindowNormalizedPluckerDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[EightWindowNormalizedPluckerStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    pivot_options: tuple[str, ...]
    source_boundary: str


def build_eight_window_normalized_plucker_decision_gate() -> EightWindowNormalizedPluckerDecisionGate:
    screen = build_eight_window_normalized_plucker_matrix_recurrence_screen()
    if screen.overall_verdict == "eight_window_matrix_recurrence_requires_exact_followup":
        outcome = "continue_eight_window_plucker_exact_matrix_followup"
        rationale = (
            "At least one side of the last overdetermined constant matrix ladder did not admit a modular inconsistency witness."
        )
        next_step = "Stay on the eight-window object and follow up that side exactly before choosing a new family or object."
    else:
        outcome = "hard_wall_eight_window_plucker_order1_matrix_exhausted"
        rationale = (
            "The last overdetermined constant matrix screen is already closed on the eight-window object, and order 2 is underdetermined."
        )
        next_step = "Keep the eight-window object only if there is a genuinely different nonlocal family to test. Otherwise pivot beyond the current normalized Plucker family."

    return EightWindowNormalizedPluckerDecisionGate(
        gate_id="bz_phase2_eight_window_normalized_plucker_decision_gate",
        source_probe_id=screen.source_probe_id,
        shared_window_start=screen.shared_window_start,
        shared_window_end=screen.shared_window_end,
        statuses=tuple(
            EightWindowNormalizedPluckerStatus(
                packet_side=item.packet_side,
                recurrence_order=item.recurrence_order,
                verdict=item.verdict,
                witness_prime=item.witness_prime,
            )
            for item in screen.order_results
        ),
        outcome=outcome,
        rationale=rationale,
        next_step=next_step,
        pivot_options=(
            "different_nonlocal_family_on_eight_window_plucker",
            "different_wider_nonlinear_invariant_family",
        ),
        source_boundary=screen.source_boundary,
    )


def render_eight_window_normalized_plucker_decision_gate() -> str:
    gate = build_eight_window_normalized_plucker_decision_gate()
    lines = [
        "# Phase 2 eight-window normalized Plucker decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{EIGHT_WINDOW_NORMALIZED_PLUCKER_MATRIX_RECURRENCE_SCREEN_REPORT_PATH}`",
        f"- Source probe id: `{gate.source_probe_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        f"- Outcome: `{gate.outcome}`",
        "",
        "| side | recurrence order | verdict | witness prime |",
        "| --- | --- | --- | --- |",
    ]
    for item in gate.statuses:
        lines.append(
            f"| `{item.packet_side}` | `{item.recurrence_order}` | `{item.verdict}` | `{item.witness_prime}` |"
        )
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


def write_eight_window_normalized_plucker_decision_gate_report(
    output_path: str | Path = EIGHT_WINDOW_NORMALIZED_PLUCKER_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_eight_window_normalized_plucker_decision_gate(), encoding="utf-8")
    return output


def write_eight_window_normalized_plucker_decision_gate_json(
    output_path: str | Path = EIGHT_WINDOW_NORMALIZED_PLUCKER_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_eight_window_normalized_plucker_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_eight_window_normalized_plucker_decision_gate_report()
    write_eight_window_normalized_plucker_decision_gate_json()


if __name__ == "__main__":
    main()
