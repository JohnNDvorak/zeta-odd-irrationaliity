from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .construction_memo import CONSTRUCTION_MEMO_REPORT_PATH, build_phase2_construction_memo
from .literature_verification import LITERATURE_VERIFICATION_REPORT_PATH

DUAL_PROJECTION_PLAN_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_dual_projection_experiment_plan.md"
DUAL_PROJECTION_PLAN_JSON_PATH = CACHE_DIR / "bz_phase2_dual_projection_experiment_plan.json"


@dataclass(frozen=True)
class ExperimentMilestone:
    milestone_id: str
    objective: str
    deliverable: str
    success_condition: str
    failure_signal: str


@dataclass(frozen=True)
class DualProjectionExperimentPlan:
    plan_id: str
    baseline_seed: str
    driving_path_id: str
    rationale: str
    non_goals: tuple[str, ...]
    reusable_assets: tuple[str, ...]
    milestones: tuple[ExperimentMilestone, ...]
    stop_conditions: tuple[str, ...]
    next_step_after_plan: str


def build_phase2_dual_projection_experiment_plan() -> DualProjectionExperimentPlan:
    memo = build_phase2_construction_memo()
    primary_path = next(path for path in memo.construction_paths if path.path_id == "baseline_dual_projection_path")
    secondary_path = next(path for path in memo.construction_paths if path.path_id == "hypergeometric_bridge_path")

    return DualProjectionExperimentPlan(
        plan_id="bz_phase2_dual_projection_experiment_plan",
        baseline_seed=memo.baseline_seed,
        driving_path_id=primary_path.path_id,
        rationale=(
            "The literature search is saturated enough to stop broadening it. The best remaining move is a bounded "
            "construction experiment on the dual cellular projection path, calibrated against explicit external "
            "zeta(5) bridge objects instead of waiting for a hidden published baseline P_n formula."
        ),
        non_goals=(
            "Do not reopen the n=435 dual-companion exact-kernel fight as the active main line.",
            "Do not claim a baseline P_n sequence unless the extraction path is explicit and reproducible in the repo.",
            "Do not widen the literature search beyond targeted bridge verification needed for implementation choices.",
        ),
        reusable_assets=(
            "Exact dual F7 constant, zeta(3), and zeta(5) coefficient extraction infrastructure.",
            "Frozen baseline dual-companion caches and degree-106 exclusion checkpoint.",
            "Totally symmetric remainder pipeline through the generic decay-probe interface.",
            f"Construction memo in `{CONSTRUCTION_MEMO_REPORT_PATH}`.",
            f"Literature verification report in `{LITERATURE_VERIFICATION_REPORT_PATH}`.",
            f"Secondary calibration path `{secondary_path.path_id}` with explicit external zeta(5) bridge objects.",
        ),
        milestones=(
            ExperimentMilestone(
                milestone_id="projection_target_spec",
                objective=(
                    "Define one normalized target object for the first projection attempt: a baseline dual-side "
                    "coefficient or linear-form component whose parity/projection meaning is explicit."
                ),
                deliverable=(
                    "A repo-native target spec and report entry that names the object, its provenance assumptions, "
                    "and the exact existing caches or probes it will reuse."
                ),
                success_condition=(
                    "The target object can be stated without inventing unpublished formulas and can be tied to existing "
                    "baseline dual extraction code."
                ),
                failure_signal=(
                    "The target cannot be formulated without hidden notation or source assumptions that are absent from the repo."
                ),
            ),
            ExperimentMilestone(
                milestone_id="external_calibration_check",
                objective=(
                    "Use one explicit external bridge object to calibrate the projection logic before applying it to the "
                    "baseline cellular family."
                ),
                deliverable=(
                    "A small calibration artifact that states which external source is used, what coefficient/projection "
                    "property is being matched, and how the repo will check it."
                ),
                success_condition=(
                    "The calibration target has an explicit published sequence or coefficient statement that can be "
                    "compared against the repo's extraction conventions."
                ),
                failure_signal=(
                    "The calibration object is too structurally different to provide a meaningful convention check."
                ),
            ),
            ExperimentMilestone(
                milestone_id="bounded_projection_probe",
                objective=(
                    "Implement a first bounded projection probe that maps the chosen baseline dual object into a "
                    "candidate decay-side summary without claiming a full baseline P_n extraction."
                ),
                deliverable=(
                    "One probe module plus one generated report that explicitly separates confirmed output, inferred output, "
                    "and unresolved pieces."
                ),
                success_condition=(
                    "The probe produces a stable, reproducible summary with honest missing-data flags and without reopening "
                    "the old exact-kernel trench."
                ),
                failure_signal=(
                    "The probe immediately requires a full representation rewrite or depends on unpublished symbolic identities."
                ),
            ),
            ExperimentMilestone(
                milestone_id="decision_gate",
                objective=(
                    "Decide whether the bounded projection probe justifies a deeper extraction program or whether the "
                    "program should fall back to the external bridge path."
                ),
                deliverable=(
                    "A short decision report that names the next main line: continue projection, switch to bridge calibration, "
                    "or pause for new source material."
                ),
                success_condition=(
                    "The decision is based on explicit probe output and implementation cost, not on open-ended optimism."
                ),
                failure_signal=(
                    "The decision still depends mainly on source hunting or on the unresolved n=435 kernel fight."
                ),
            ),
        ),
        stop_conditions=(
            "Stop if the first bounded projection probe requires a full exact-arithmetic representation rewrite before yielding any new baseline-side summary.",
            "Stop if the calibration step shows that the chosen projection conventions cannot be matched even on the external bridge object.",
            "Stop if the only remaining next move is speculative source hunting rather than construction work.",
        ),
        next_step_after_plan=(
            "Implement milestone `projection_target_spec` first, then lock one external calibration object from the "
            "hypergeometric bridge path before writing any new baseline dual projection code."
        ),
    )


def render_phase2_dual_projection_experiment_plan() -> str:
    plan = build_phase2_dual_projection_experiment_plan()
    lines = [
        "# Phase 2 dual projection experiment plan",
        "",
        f"- Plan id: `{plan.plan_id}`",
        f"- Baseline seed: `{plan.baseline_seed}`",
        f"- Driving path id: `{plan.driving_path_id}`",
        "",
        "## Rationale",
        "",
        plan.rationale,
        "",
        "## Non-goals",
        "",
    ]
    for item in plan.non_goals:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Reusable assets",
            "",
        ]
    )
    for asset in plan.reusable_assets:
        lines.append(f"- {asset}")
    lines.extend(
        [
            "",
            "## Milestones",
            "",
        ]
    )
    for milestone in plan.milestones:
        lines.extend(
            [
                f"### {milestone.milestone_id}",
                "",
                f"- Objective: {milestone.objective}",
                f"- Deliverable: {milestone.deliverable}",
                f"- Success condition: {milestone.success_condition}",
                f"- Failure signal: {milestone.failure_signal}",
                "",
            ]
        )
    lines.extend(
        [
            "## Stop conditions",
            "",
        ]
    )
    for item in plan.stop_conditions:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Next step",
            "",
            plan.next_step_after_plan,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_dual_projection_experiment_plan_report(
    output_path: str | Path = DUAL_PROJECTION_PLAN_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_dual_projection_experiment_plan(), encoding="utf-8")
    return output


def write_phase2_dual_projection_experiment_plan_json(
    output_path: str | Path = DUAL_PROJECTION_PLAN_JSON_PATH,
) -> Path:
    plan = build_phase2_dual_projection_experiment_plan()
    payload = {
        "plan_id": plan.plan_id,
        "baseline_seed": plan.baseline_seed,
        "driving_path_id": plan.driving_path_id,
        "rationale": plan.rationale,
        "non_goals": list(plan.non_goals),
        "reusable_assets": list(plan.reusable_assets),
        "milestones": [asdict(milestone) for milestone in plan.milestones],
        "stop_conditions": list(plan.stop_conditions),
        "next_step_after_plan": plan.next_step_after_plan,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_dual_projection_experiment_plan_report()
    write_phase2_dual_projection_experiment_plan_json()


if __name__ == "__main__":
    main()
