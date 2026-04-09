from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_annihilator_transfer_probe import (
    SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_PROBE_REPORT_PATH,
    build_symmetric_dual_baseline_annihilator_transfer_probe,
)

SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_POST_PROBE_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate.md"
)
SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_POST_PROBE_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate.json"
)


@dataclass(frozen=True)
class SymmetricDualBaselineAnnihilatorTransferDecisionStatus:
    criterion_id: str
    verdict: str
    note: str


@dataclass(frozen=True)
class SymmetricDualBaselineAnnihilatorTransferPostProbeDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[SymmetricDualBaselineAnnihilatorTransferDecisionStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    non_claims: tuple[str, ...]


def build_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate(
) -> SymmetricDualBaselineAnnihilatorTransferPostProbeDecisionGate:
    probe = build_symmetric_dual_baseline_annihilator_transfer_probe()
    return SymmetricDualBaselineAnnihilatorTransferPostProbeDecisionGate(
        gate_id="bz_phase2_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=(
            SymmetricDualBaselineAnnihilatorTransferDecisionStatus(
                criterion_id="paired_exact_annihilator_profiles",
                verdict="satisfied",
                note="Source and target are exact local-annihilator profiles on the same shared window.",
            ),
            SymmetricDualBaselineAnnihilatorTransferDecisionStatus(
                criterion_id="reproducible_hashes",
                verdict="satisfied",
                note="Source, target, and paired transfer object hashes are all reproducible.",
            ),
            SymmetricDualBaselineAnnihilatorTransferDecisionStatus(
                criterion_id="bounded_profile_family_choice",
                verdict="not_yet_satisfied",
                note="No bounded profile-level transfer family has been tested yet.",
            ),
        ),
        outcome="continue_symmetric_dual_baseline_annihilator_transfer_family_probe",
        rationale=(
            "The local-annihilator transfer object is strong enough to justify one bounded low-complexity transfer ladder."
        ),
        next_step="Implement the bounded transfer family probe with constant, difference, and lag-1 profile maps.",
        non_claims=(
            "This does not claim the two local annihilator profiles are equivalent.",
            "This does not prove a common recurrence for the symmetric and baseline dual packets.",
            "This does not justify skipping the bounded transfer family ladder.",
        ),
    )


def render_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate() -> str:
    gate = build_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate()
    lines = [
        "# Phase 2 symmetric-dual to baseline-dual annihilator transfer post-probe decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_PROBE_REPORT_PATH}`",
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


def write_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate_report(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_POST_PROBE_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate(),
        encoding="utf-8",
    )
    return output


def write_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate_json(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_POST_PROBE_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate_report()
    write_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate_json()


if __name__ == "__main__":
    main()
