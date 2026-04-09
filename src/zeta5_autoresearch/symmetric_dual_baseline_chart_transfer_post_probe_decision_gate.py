from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_chart_transfer_probe import (
    SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_PROBE_REPORT_PATH,
    build_symmetric_dual_baseline_chart_transfer_probe,
)

SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_POST_PROBE_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate.md"
)
SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_POST_PROBE_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate.json"
)


@dataclass(frozen=True)
class SymmetricDualBaselineChartTransferDecisionStatus:
    criterion_id: str
    verdict: str
    note: str


@dataclass(frozen=True)
class SymmetricDualBaselineChartTransferPostProbeDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[SymmetricDualBaselineChartTransferDecisionStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    non_claims: tuple[str, ...]


def build_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate(
) -> SymmetricDualBaselineChartTransferPostProbeDecisionGate:
    probe = build_symmetric_dual_baseline_chart_transfer_probe()
    return SymmetricDualBaselineChartTransferPostProbeDecisionGate(
        gate_id="bz_phase2_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=(
            SymmetricDualBaselineChartTransferDecisionStatus(
                criterion_id="paired_exact_chart_profiles",
                verdict="satisfied",
                note="Source and target are exact five-term chart profiles on the same shared window.",
            ),
            SymmetricDualBaselineChartTransferDecisionStatus(
                criterion_id="reproducible_hashes",
                verdict="satisfied",
                note="Source, target, and paired chart-transfer hashes are all reproducible.",
            ),
            SymmetricDualBaselineChartTransferDecisionStatus(
                criterion_id="bounded_chart_family_choice",
                verdict="not_yet_satisfied",
                note="No bounded chart-profile transfer family has been tested yet.",
            ),
        ),
        outcome="continue_symmetric_dual_baseline_chart_transfer_family_probe",
        rationale="The chart-profile object is strong enough to justify a bounded family ladder deeper than the previous low-complexity objects.",
        next_step="Implement the bounded chart-family ladder with constant, difference, and support-1 through support-4 maps.",
        non_claims=(
            "This does not claim the two chart profiles are equivalent.",
            "This does not prove a common recurrence for the symmetric and baseline dual packets.",
            "This does not justify importing symmetric identities into the baseline family.",
        ),
    )


def render_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate() -> str:
    gate = build_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate()
    lines = [
        "# Phase 2 symmetric-dual to baseline-dual chart transfer post-probe decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_PROBE_REPORT_PATH}`",
        f"- Source probe id: `{gate.source_probe_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        f"- Outcome: `{gate.outcome}`",
        "",
        "| criterion | verdict | note |",
        "| --- | --- | --- |",
    ]
    for item in gate.statuses:
        lines.append(f"| `{item.criterion_id}` | `{item.verdict}` | {item.note} |")
    lines.extend(["", "## Rationale", "", gate.rationale, "", "## Next step", "", gate.next_step, "", "## Non-claims", ""])
    for item in gate.non_claims:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def write_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate_report(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_POST_PROBE_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate(), encoding="utf-8")
    return output


def write_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate_json(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_POST_PROBE_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate_report()
    write_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate_json()


if __name__ == "__main__":
    main()
