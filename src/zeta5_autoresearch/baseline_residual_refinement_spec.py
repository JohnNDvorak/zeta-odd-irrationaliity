from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_extraction_post_probe_decision_gate import (
    BASELINE_EXTRACTION_POST_PROBE_DECISION_GATE_REPORT_PATH,
    build_baseline_extraction_post_probe_decision_gate,
)
from .baseline_extraction_rule import (
    BASELINE_EXTRACTION_RULE_REPORT_PATH,
    build_baseline_extraction_rule,
)
from .config import CACHE_DIR, DATA_DIR

BASELINE_RESIDUAL_REFINEMENT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_residual_refinement_spec.md"
)
BASELINE_RESIDUAL_REFINEMENT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_residual_refinement_spec.json"
)


@dataclass(frozen=True)
class BaselineResidualRefinementFamilySpec:
    family_id: str
    family_label: str
    coefficient_labels: tuple[str, ...]
    fit_window_start: int
    fit_window_end: int
    validation_window_start: int
    validation_window_end: int
    family_statement: str
    goal: str


@dataclass(frozen=True)
class BaselineResidualRefinementSpec:
    spec_id: str
    source_gate_id: str
    source_rule_id: str
    shared_window_start: int
    shared_window_end: int
    active_object: str
    bridge_boundary: str
    family_specs: tuple[BaselineResidualRefinementFamilySpec, ...]
    non_goals: tuple[str, ...]
    recommendation: str


def build_baseline_residual_refinement_spec() -> BaselineResidualRefinementSpec:
    gate = build_baseline_extraction_post_probe_decision_gate()
    rule = build_baseline_extraction_rule()
    return BaselineResidualRefinementSpec(
        spec_id="bz_phase2_baseline_residual_refinement_spec",
        source_gate_id=gate.gate_id,
        source_rule_id=rule.rule_id,
        shared_window_start=rule.shared_window_start,
        shared_window_end=rule.shared_window_end,
        active_object="baseline_pair_object_with_explicit_zeta3_residual",
        bridge_boundary=rule.bridge_boundary,
        family_specs=(
            BaselineResidualRefinementFamilySpec(
                family_id="support0_same_index",
                family_label="Same-index support-0 residual recombination",
                coefficient_labels=("a", "b"),
                fit_window_start=1,
                fit_window_end=2,
                validation_window_start=1,
                validation_window_end=rule.shared_window_end,
                family_statement="r_n = zeta3_n + a * constant_n + b * zeta5_n",
                goal="Test whether the residual zeta(3) channel collapses under a same-index exact recombination with the retained pair.",
            ),
            BaselineResidualRefinementFamilySpec(
                family_id="difference_pair",
                family_label="First-difference pair residual recombination",
                coefficient_labels=("a", "b"),
                fit_window_start=2,
                fit_window_end=3,
                validation_window_start=2,
                validation_window_end=rule.shared_window_end,
                family_statement=(
                    "r_n = zeta3_n + a * (constant_n - constant_{n-1}) + b * (zeta5_n - zeta5_{n-1})"
                ),
                goal="Test whether the residual zeta(3) channel is better described against first differences of the retained pair.",
            ),
            BaselineResidualRefinementFamilySpec(
                family_id="support1_lagged_pair",
                family_label="Lag-1 support residual recombination",
                coefficient_labels=("a0", "a1", "b0", "b1"),
                fit_window_start=2,
                fit_window_end=5,
                validation_window_start=2,
                validation_window_end=rule.shared_window_end,
                family_statement=(
                    "r_n = zeta3_n + a0 * constant_n + a1 * constant_{n-1} + "
                    "b0 * zeta5_n + b1 * zeta5_{n-1}"
                ),
                goal="Test whether one lag of baseline-side support is enough to reclassify the residual zeta(3) channel.",
            ),
        ),
        non_goals=(
            "Do not fit any bridge-side object in this refinement ladder.",
            "Do not enlarge to support-2 or n-dependent families in this tranche.",
            "Do not claim a baseline P_n extraction from these families alone.",
        ),
        recommendation=(
            "Run the bounded residual-refinement probe next and let its exact full-window verdict choose between "
            "a promoted v2 extraction branch and a hard-wall decision gate."
        ),
    )


def render_baseline_residual_refinement_spec() -> str:
    spec = build_baseline_residual_refinement_spec()
    lines = [
        "# Phase 2 baseline residual refinement spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Source post-probe gate: `{BASELINE_EXTRACTION_POST_PROBE_DECISION_GATE_REPORT_PATH}`",
        f"- Source gate id: `{spec.source_gate_id}`",
        f"- Source extraction rule: `{BASELINE_EXTRACTION_RULE_REPORT_PATH}`",
        f"- Source rule id: `{spec.source_rule_id}`",
        f"- Shared exact window: `n={spec.shared_window_start}..{spec.shared_window_end}`",
        f"- Active object: `{spec.active_object}`",
        "",
        "## Bridge boundary",
        "",
        spec.bridge_boundary,
        "",
        "## Fixed family ladder",
        "",
        "| family | fit window | validation window | coefficients |",
        "| --- | --- | --- | --- |",
    ]
    for family in spec.family_specs:
        lines.append(
            f"| `{family.family_id}` | `n={family.fit_window_start}..{family.fit_window_end}` | "
            f"`n={family.validation_window_start}..{family.validation_window_end}` | "
            f"`{', '.join(family.coefficient_labels)}` |"
        )
    lines.extend(["", "## Family details", ""])
    for family in spec.family_specs:
        lines.extend(
            [
                f"### `{family.family_id}`",
                "",
                f"- Label: {family.family_label}",
                f"- Statement: `{family.family_statement}`",
                f"- Goal: {family.goal}",
                "",
            ]
        )
    lines.extend(["## Non-goals", ""])
    for item in spec.non_goals:
        lines.append(f"- {item}")
    lines.extend(["", "## Recommendation", "", spec.recommendation, ""])
    return "\n".join(lines)


def write_baseline_residual_refinement_spec_report(
    output_path: str | Path = BASELINE_RESIDUAL_REFINEMENT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_residual_refinement_spec(), encoding="utf-8")
    return output


def write_baseline_residual_refinement_spec_json(
    output_path: str | Path = BASELINE_RESIDUAL_REFINEMENT_SPEC_JSON_PATH,
) -> Path:
    spec = build_baseline_residual_refinement_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_residual_refinement_spec_report()
    write_baseline_residual_refinement_spec_json()


if __name__ == "__main__":
    main()
