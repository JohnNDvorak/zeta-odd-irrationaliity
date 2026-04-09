from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_baseline_transfer_family_probe import (
    SYMMETRIC_BASELINE_TRANSFER_FAMILY_PROBE_REPORT_PATH,
    build_symmetric_baseline_transfer_family_probe,
)

SYMMETRIC_BASELINE_TRANSFER_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_baseline_transfer_decision_gate.md"
)
SYMMETRIC_BASELINE_TRANSFER_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_baseline_transfer_decision_gate.json"
)


@dataclass(frozen=True)
class SymmetricBaselineTransferStatus:
    family_id: str
    verdict: str
    note: str


@dataclass(frozen=True)
class SymmetricBaselineTransferDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[SymmetricBaselineTransferStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    pivot_options: tuple[str, ...]
    source_boundary: str


def build_symmetric_baseline_transfer_decision_gate() -> SymmetricBaselineTransferDecisionGate:
    probe = build_symmetric_baseline_transfer_family_probe()
    winner_exists = any(item.verdict == "holds_on_full_window" for item in probe.family_results)
    return SymmetricBaselineTransferDecisionGate(
        gate_id="bz_phase2_symmetric_baseline_transfer_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=tuple(
            SymmetricBaselineTransferStatus(
                family_id=item.family_id,
                verdict=item.verdict,
                note=(
                    "This bounded transfer family holds on the full validation window."
                    if item.verdict == "holds_on_full_window"
                    else "This bounded transfer family fails after its fit window."
                ),
            )
            for item in probe.family_results
        ),
        outcome=(
            "continue_symmetric_baseline_transfer_v2"
            if winner_exists
            else "hard_wall_symmetric_baseline_low_complexity_transfer_exhausted"
        ),
        rationale=(
            "At least one bounded packet-level transfer family survives on the full validation window."
            if winner_exists
            else "The bounded packet-level transfer ladder is exhausted: constant, difference, and lag-1 packet maps all fail after fitting."
        ),
        next_step=(
            "Promote the winning transfer family into a v2 transfer artifact."
            if winner_exists
            else "Stop autonomous execution and ask the user for the next pivot."
        ),
        pivot_options=(
            "richer_packet_transfer_family",
            "different_transfer_object",
        ),
        source_boundary=probe.source_boundary,
    )


def render_symmetric_baseline_transfer_decision_gate() -> str:
    gate = build_symmetric_baseline_transfer_decision_gate()
    lines = [
        "# Phase 2 symmetric-to-baseline transfer decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{SYMMETRIC_BASELINE_TRANSFER_FAMILY_PROBE_REPORT_PATH}`",
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


def write_symmetric_baseline_transfer_decision_gate_report(
    output_path: str | Path = SYMMETRIC_BASELINE_TRANSFER_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_baseline_transfer_decision_gate(), encoding="utf-8")
    return output


def write_symmetric_baseline_transfer_decision_gate_json(
    output_path: str | Path = SYMMETRIC_BASELINE_TRANSFER_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_symmetric_baseline_transfer_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_baseline_transfer_decision_gate_report()
    write_symmetric_baseline_transfer_decision_gate_json()


if __name__ == "__main__":
    main()
