from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_residual_refinement_probe import (
    BASELINE_RESIDUAL_REFINEMENT_PROBE_REPORT_PATH,
    build_baseline_residual_refinement_probe,
)
from .config import CACHE_DIR, DATA_DIR

BASELINE_RESIDUAL_REFINEMENT_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_residual_refinement_decision_gate.md"
)
BASELINE_RESIDUAL_REFINEMENT_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_residual_refinement_decision_gate.json"
)

WINNER_PRIORITY = (
    "support0_same_index",
    "difference_pair",
    "support1_lagged_pair",
)


@dataclass(frozen=True)
class BaselineResidualRefinementStatus:
    family_id: str
    verdict: str
    note: str


@dataclass(frozen=True)
class BaselineResidualRefinementDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[BaselineResidualRefinementStatus, ...]
    outcome: str
    winner_family_id: str | None
    rationale: str
    next_step: str
    pivot_options: tuple[str, ...]
    bridge_boundary: str


def build_baseline_residual_refinement_decision_gate() -> BaselineResidualRefinementDecisionGate:
    probe = build_baseline_residual_refinement_probe()
    statuses = tuple(
        BaselineResidualRefinementStatus(
            family_id=item.family_id,
            verdict=item.verdict,
            note=(
                "Exact full-window winner."
                if item.verdict == "holds_on_full_window"
                else (
                    "Fit window solves exactly but the family fails on the larger validation window."
                    if item.verdict == "fails_after_fit_window"
                    else "Exact fit system is ill-posed on the prescribed fit window."
                )
            ),
        )
        for item in probe.family_results
    )
    winning_family_id = next(
        (
            family_id
            for family_id in WINNER_PRIORITY
            if any(
                item.family_id == family_id and item.verdict == "holds_on_full_window"
                for item in probe.family_results
            )
        ),
        None,
    )

    if winning_family_id is None:
        return BaselineResidualRefinementDecisionGate(
            gate_id="bz_phase2_baseline_residual_refinement_decision_gate",
            source_probe_id=probe.probe_id,
            shared_window_start=probe.shared_window_start,
            shared_window_end=probe.shared_window_end,
            statuses=statuses,
            outcome="hard_wall_low_complexity_baseline_refinement_exhausted",
            winner_family_id=None,
            rationale=(
                "All fixed low-complexity baseline-native residual-refinement families either fail after their fit windows "
                "or would be ill-posed. The bridge stack remains calibration-only, and this ladder is now exhausted on "
                "the exact shared window."
            ),
            next_step=(
                "Stop autonomous execution and ask the user to choose the next pivot. Do not add richer baseline-side "
                "families or change the target object without that decision."
            ),
            pivot_options=(
                "richer_baseline_family",
                "different_target_object",
            ),
            bridge_boundary=probe.bridge_boundary,
        )

    return BaselineResidualRefinementDecisionGate(
        gate_id="bz_phase2_baseline_residual_refinement_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=statuses,
        outcome="continue_to_baseline_remainder_candidate_spec",
        winner_family_id=winning_family_id,
        rationale=(
            "A fixed low-complexity baseline-native refinement family holds on the full shared exact window, so the "
            "residual-refinement ladder has an evidence-based winner."
        ),
        next_step=(
            "Promote the winning family into a v2 baseline extraction rule/probe stack and only then decide whether "
            "a baseline remainder candidate spec is justified."
        ),
        pivot_options=(),
        bridge_boundary=probe.bridge_boundary,
    )


def render_baseline_residual_refinement_decision_gate() -> str:
    gate = build_baseline_residual_refinement_decision_gate()
    lines = [
        "# Phase 2 baseline residual refinement decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{BASELINE_RESIDUAL_REFINEMENT_PROBE_REPORT_PATH}`",
        f"- Source probe id: `{gate.source_probe_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        f"- Outcome: `{gate.outcome}`",
        f"- Winner family id: `{gate.winner_family_id}`",
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
            "## Bridge boundary",
            "",
            gate.bridge_boundary,
            "",
        ]
    )
    if gate.pivot_options:
        lines.extend(["## Pivot options", ""])
        for item in gate.pivot_options:
            lines.append(f"- `{item}`")
        lines.append("")
    return "\n".join(lines)


def write_baseline_residual_refinement_decision_gate_report(
    output_path: str | Path = BASELINE_RESIDUAL_REFINEMENT_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_residual_refinement_decision_gate(), encoding="utf-8")
    return output


def write_baseline_residual_refinement_decision_gate_json(
    output_path: str | Path = BASELINE_RESIDUAL_REFINEMENT_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_baseline_residual_refinement_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_residual_refinement_decision_gate_report()
    write_baseline_residual_refinement_decision_gate_json()


if __name__ == "__main__":
    main()
