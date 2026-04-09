from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .construction_memo import CONSTRUCTION_MEMO_REPORT_PATH, build_phase2_construction_memo
from .dual_projection_target_spec import (
    DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH,
    build_phase2_dual_projection_target_spec,
)
from .zudilin_2002_path_selection_memo import (
    ZUDILIN_2002_PATH_SELECTION_MEMO_REPORT_PATH,
    build_zudilin_2002_path_selection_memo,
)

BASELINE_EXTRACTION_IMPLEMENTATION_PLAN_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_extraction_implementation_plan.md"
)
BASELINE_EXTRACTION_IMPLEMENTATION_PLAN_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_extraction_implementation_plan.json"
)


@dataclass(frozen=True)
class ExtractionMilestone:
    milestone_id: str
    objective: str
    deliverable: str
    success_condition: str
    stop_rule: str


@dataclass(frozen=True)
class BaselineExtractionImplementationPlan:
    plan_id: str
    baseline_seed: str
    target_object: str
    bridge_role: str
    rationale: str
    milestones: tuple[ExtractionMilestone, ...]
    non_goals: tuple[str, ...]
    next_step: str


def build_baseline_extraction_implementation_plan() -> BaselineExtractionImplementationPlan:
    memo = build_phase2_construction_memo()
    selection = build_zudilin_2002_path_selection_memo(max_n=7)
    target = build_phase2_dual_projection_target_spec()

    return BaselineExtractionImplementationPlan(
        plan_id="bz_phase2_baseline_extraction_implementation_plan",
        baseline_seed=memo.baseline_seed,
        target_object=target.target_id,
        bridge_role=(
            "Use the Zudilin 2002 bridge stack only as calibration for conventions and failure modes. "
            "Do not treat bridge-map fitting as the main line."
        ),
        rationale=(
            "The bridge program has now supplied enough calibration: explicit comparison objects, explicit stop rules, "
            "and multiple bounded ansatz failures. The next best use of cycles is to return to baseline-side extraction "
            "with a bounded implementation plan anchored on the existing exact coefficient packet."
        ),
        milestones=(
            ExtractionMilestone(
                milestone_id="baseline_pair_object_spec",
                objective=(
                    "Freeze the exact baseline-side extraction object to be manipulated directly, starting from the "
                    "baseline dual F_7 coefficient packet rather than from bridge-map surrogates."
                ),
                deliverable=(
                    "One repo-native spec naming the exact baseline extraction object, its components, and the precise "
                    "output type expected from the first extraction attempt."
                ),
                success_condition=(
                    "The object is stated entirely in repo-native terms and does not depend on unpublished bridge-style identities."
                ),
                stop_rule=(
                    "Stop if the object spec cannot be stated without introducing hidden assumptions about baseline P_n."
                ),
            ),
            ExtractionMilestone(
                milestone_id="bounded_extraction_rule",
                objective=(
                    "Define one bounded baseline-side extraction rule on the exact coefficient packet, with the bridge "
                    "used only to sanity-check bookkeeping conventions."
                ),
                deliverable=(
                    "One extraction-rule artifact that distinguishes confirmed output, inferred structure, and unresolved remainder."
                ),
                success_condition=(
                    "The rule produces a reproducible output object without reopening the old exact-kernel trench or inventing a recurrence."
                ),
                stop_rule=(
                    "Stop if the rule immediately requires an unbounded symbolic rewrite or collapses back into bridge-map fitting."
                ),
            ),
            ExtractionMilestone(
                milestone_id="bounded_extraction_probe",
                objective=(
                    "Run the first bounded extraction probe on the baseline-side object and record what, if anything, is stabilized."
                ),
                deliverable=(
                    "One generated report with explicit non-claims and a decision about whether the output is extraction-like enough to pursue."
                ),
                success_condition=(
                    "The probe creates a stable repo object that is more proof-relevant than the current bridge comparison layer."
                ),
                stop_rule=(
                    "Stop if the probe yields only another analog-comparison object rather than a more baseline-native extraction artifact."
                ),
            ),
            ExtractionMilestone(
                milestone_id="post_probe_decision_gate",
                objective=(
                    "Choose whether to deepen baseline extraction, return to a narrower calibration step, or pause for a new source-backed idea."
                ),
                deliverable=(
                    "One short decision gate based on probe output and implementation cost, not on generic optimism."
                ),
                success_condition=(
                    "The next line is chosen from evidence produced by the extraction probe itself."
                ),
                stop_rule=(
                    "Stop if the decision still depends mainly on expanding ansatz families that the bridge memo already deprioritized."
                ),
            ),
        ),
        non_goals=(
            "Do not add cubic or higher bridge normalization families by default.",
            "Do not make the Zudilin 2002 bridge object the main target; it is calibration only.",
            "Do not claim baseline P_n extraction unless the new artifact is explicitly repo-native and reproducible.",
        ),
        next_step=(
            "Implement `baseline_pair_object_spec` first, using the exact baseline dual F_7 coefficient packet as the active "
            "baseline-side object and the bridge stack only as a calibration boundary."
        ),
    )


def render_baseline_extraction_implementation_plan() -> str:
    plan = build_baseline_extraction_implementation_plan()
    lines = [
        "# Phase 2 baseline extraction implementation plan",
        "",
        f"- Plan id: `{plan.plan_id}`",
        f"- Baseline seed: `{plan.baseline_seed}`",
        f"- Construction memo: `{CONSTRUCTION_MEMO_REPORT_PATH}`",
        f"- Path-selection memo: `{ZUDILIN_2002_PATH_SELECTION_MEMO_REPORT_PATH}`",
        f"- Active target object: `{plan.target_object}`",
        "",
        "## Bridge role",
        "",
        plan.bridge_role,
        "",
        "## Rationale",
        "",
        plan.rationale,
        "",
        "## Milestones",
        "",
    ]
    for milestone in plan.milestones:
        lines.extend(
            [
                f"### {milestone.milestone_id}",
                "",
                f"- Objective: {milestone.objective}",
                f"- Deliverable: {milestone.deliverable}",
                f"- Success condition: {milestone.success_condition}",
                f"- Stop rule: {milestone.stop_rule}",
                "",
            ]
        )
    lines.extend(
        [
            "## Non-goals",
            "",
        ]
    )
    for item in plan.non_goals:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Next step",
            "",
            plan.next_step,
            "",
        ]
    )
    return "\n".join(lines)


def write_baseline_extraction_implementation_plan_report(
    output_path: str | Path = BASELINE_EXTRACTION_IMPLEMENTATION_PLAN_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_extraction_implementation_plan(), encoding="utf-8")
    return output


def write_baseline_extraction_implementation_plan_json(
    output_path: str | Path = BASELINE_EXTRACTION_IMPLEMENTATION_PLAN_JSON_PATH,
) -> Path:
    plan = build_baseline_extraction_implementation_plan()
    payload = asdict(plan)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_extraction_implementation_plan_report()
    write_baseline_extraction_implementation_plan_json()


if __name__ == "__main__":
    main()
