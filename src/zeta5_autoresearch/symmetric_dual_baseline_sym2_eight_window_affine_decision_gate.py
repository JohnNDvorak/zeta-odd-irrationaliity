from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_sym2_eight_window_affine_matrix_recurrence_screen import (
    SYM2_EIGHT_WINDOW_AFFINE_MATRIX_RECURRENCE_SCREEN_REPORT_PATH,
    build_sym2_eight_window_affine_matrix_recurrence_screen,
)

SYM2_EIGHT_WINDOW_AFFINE_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym2_eight_window_affine_decision_gate.md"
)
SYM2_EIGHT_WINDOW_AFFINE_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym2_eight_window_affine_decision_gate.json"
)


@dataclass(frozen=True)
class Sym2EightWindowAffineStatus:
    packet_side: str
    recurrence_order: int
    verdict: str
    witness_prime: int | None


@dataclass(frozen=True)
class Sym2EightWindowAffineDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[Sym2EightWindowAffineStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    pivot_options: tuple[str, ...]
    source_boundary: str


def build_sym2_eight_window_affine_decision_gate() -> Sym2EightWindowAffineDecisionGate:
    screen = build_sym2_eight_window_affine_matrix_recurrence_screen()
    if screen.overall_verdict == "sym2_eight_window_affine_matrix_recurrence_requires_exact_followup":
        outcome = "continue_sym2_eight_window_exact_affine_followup"
        rationale = (
            "At least one side of the last overdetermined affine matrix ladder did not admit a modular inconsistency witness."
        )
        next_step = "Stay on the Sym^2-lifted eight-window object and follow up that side exactly before choosing a new family or object."
    else:
        outcome = "hard_wall_sym2_eight_window_low_order_affine_matrix_ladder_exhausted"
        rationale = (
            "The overdetermined affine matrix screen is closed through order 2 on the Sym^2-lifted eight-window object, and order 3 is already underdetermined."
        )
        next_step = "Do not keep widening affine matrix order mechanically. Move either to a genuinely different nonlocal family on the same object or to a different higher Schur/nonlinear invariant family."

    return Sym2EightWindowAffineDecisionGate(
        gate_id="bz_phase2_sym2_eight_window_affine_decision_gate",
        source_probe_id=screen.source_probe_id,
        shared_window_start=screen.shared_window_start,
        shared_window_end=screen.shared_window_end,
        statuses=tuple(
            Sym2EightWindowAffineStatus(
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
            "different_nonlocal_family_on_sym2_eight_window_lift",
            "different_higher_schur_or_nonlinear_invariant_family",
        ),
        source_boundary=screen.source_boundary,
    )


def render_sym2_eight_window_affine_decision_gate() -> str:
    gate = build_sym2_eight_window_affine_decision_gate()
    lines = [
        "# Phase 2 Sym^2-lifted eight-window affine decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{SYM2_EIGHT_WINDOW_AFFINE_MATRIX_RECURRENCE_SCREEN_REPORT_PATH}`",
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


def write_sym2_eight_window_affine_decision_gate_report(
    output_path: str | Path = SYM2_EIGHT_WINDOW_AFFINE_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym2_eight_window_affine_decision_gate(), encoding="utf-8")
    return output


def write_sym2_eight_window_affine_decision_gate_json(
    output_path: str | Path = SYM2_EIGHT_WINDOW_AFFINE_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_sym2_eight_window_affine_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym2_eight_window_affine_decision_gate_report()
    write_sym2_eight_window_affine_decision_gate_json()


if __name__ == "__main__":
    main()
