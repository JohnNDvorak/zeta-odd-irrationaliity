from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_projection_target_spec import (
    DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH,
    build_phase2_dual_projection_target_spec,
)

BASELINE_ODD_PAIR_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_odd_pair_object_spec.md"
)
BASELINE_ODD_PAIR_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_odd_pair_object_spec.json"
)


@dataclass(frozen=True)
class BaselineOddPairComponent:
    component_id: str
    source_component: str
    role: str
    max_verified_index: int
    exact_status: str
    note: str


@dataclass(frozen=True)
class BaselineOddExtractionOutputType:
    output_id: str
    label: str
    semantics: str
    non_claim: str


@dataclass(frozen=True)
class BaselineOddPairObjectSpec:
    spec_id: str
    baseline_seed: str
    source_packet_id: str
    object_label: str
    object_kind: str
    object_semantics: str
    components: tuple[BaselineOddPairComponent, ...]
    extraction_output: BaselineOddExtractionOutputType
    bridge_boundary: str
    rationale: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_baseline_odd_pair_object_spec() -> BaselineOddPairObjectSpec:
    target = build_phase2_dual_projection_target_spec()
    target_components = {component.component_id: component for component in target.components}
    return BaselineOddPairObjectSpec(
        spec_id="bz_phase2_baseline_odd_pair_object_spec",
        baseline_seed=target.baseline_seed,
        source_packet_id=target.target_id,
        object_label="Baseline odd-weight pair object",
        object_kind="baseline_side_exact_odd_pair_with_constant_residual",
        object_semantics=(
            "The active baseline-side object is the ordered odd-weight pair `(zeta(5), zeta(3))` drawn from the exact "
            "baseline dual F_7 coefficient packet, together with the rational constant term carried as explicit residual "
            "structure. This is the smallest repo-native object aligned with the odd-zeta projection viewpoint."
        ),
        components=(
            BaselineOddPairComponent(
                component_id="retained_zeta5",
                source_component="zeta5",
                role="exact zeta(5) coefficient retained as the primary odd-target channel",
                max_verified_index=target_components["zeta5"].max_verified_index,
                exact_status=target_components["zeta5"].exact_status,
                note="This remains the shortest verified frontier and therefore caps the shared exact window.",
            ),
            BaselineOddPairComponent(
                component_id="retained_zeta3",
                source_component="zeta3",
                role="exact zeta(3) coefficient retained as the companion odd-weight channel",
                max_verified_index=target_components["zeta3"].max_verified_index,
                exact_status=target_components["zeta3"].exact_status,
                note="Keeping zeta(3) in the retained pair matches the odd-zeta projection framing more directly than treating it as noise.",
            ),
            BaselineOddPairComponent(
                component_id="residual_constant",
                source_component="constant",
                role="explicit rational residual carried alongside the odd pair",
                max_verified_index=target_components["constant"].max_verified_index,
                exact_status=target_components["constant"].exact_status,
                note="The constant term is demoted to residual structure rather than retained as part of the active odd-weight pair.",
            ),
        ),
        extraction_output=BaselineOddExtractionOutputType(
            output_id="baseline_odd_extraction_summary_v1",
            label="Bounded baseline odd-pair extraction summary",
            semantics=(
                "A bounded odd-pair extraction summary is a repo-native object produced from the baseline odd pair "
                "that may recombine or filter the retained odd channels while keeping the constant residual explicit."
            ),
            non_claim="It is not, by default, a claimed baseline P_n sequence or a proved baseline remainder pipeline.",
        ),
        bridge_boundary=(
            "The Zudilin 2002 bridge stack may be used only as calibration for conventions and failure modes. "
            "It may not redefine the active odd-pair object or supply hidden identities for it."
        ),
        rationale=(
            "This object is preferred after the `(constant, zeta(5))` line hit a hard wall because it keeps the odd-zeta "
            "channels together and demotes the rational constant term to residual structure, which better matches the "
            "projection language in the construction memo."
        ),
        non_claims=(
            "This spec does not claim that `(zeta(5), zeta(3))` is already the baseline decay object.",
            "This spec does not eliminate the constant residual.",
            "This spec does not claim a baseline P_n extraction.",
        ),
        recommended_next_step=(
            "Implement the first bounded odd-pair extraction rule and require it to preserve the split between retained odd channels and constant residual structure."
        ),
    )


def render_baseline_odd_pair_object_spec() -> str:
    spec = build_baseline_odd_pair_object_spec()
    lines = [
        "# Phase 2 baseline odd-pair object spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Baseline seed: `{spec.baseline_seed}`",
        f"- Source packet spec: `{DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH}`",
        f"- Source packet id: `{spec.source_packet_id}`",
        f"- Object label: `{spec.object_label}`",
        f"- Object kind: `{spec.object_kind}`",
        "",
        "## Object semantics",
        "",
        spec.object_semantics,
        "",
        "## Rationale",
        "",
        spec.rationale,
        "",
        "## Components",
        "",
        "| component | source component | role | max verified index | exact status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for component in spec.components:
        lines.append(
            f"| `{component.component_id}` | `{component.source_component}` | {component.role} | "
            f"`{component.max_verified_index}` | `{component.exact_status}` |"
        )
    lines.extend(["", "## Component notes", ""])
    for component in spec.components:
        lines.append(f"- `{component.component_id}`: {component.note}")
    lines.extend(
        [
            "",
            "## Extraction output type",
            "",
            f"- Output id: `{spec.extraction_output.output_id}`",
            f"- Label: `{spec.extraction_output.label}`",
            f"- Semantics: {spec.extraction_output.semantics}",
            f"- Non-claim: {spec.extraction_output.non_claim}",
            "",
            "## Bridge boundary",
            "",
            spec.bridge_boundary,
            "",
            "## Non-claims",
            "",
        ]
    )
    for item in spec.non_claims:
        lines.append(f"- {item}")
    lines.extend(["", "## Recommended next step", "", spec.recommended_next_step, ""])
    return "\n".join(lines)


def write_baseline_odd_pair_object_spec_report(
    output_path: str | Path = BASELINE_ODD_PAIR_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_odd_pair_object_spec(), encoding="utf-8")
    return output


def write_baseline_odd_pair_object_spec_json(
    output_path: str | Path = BASELINE_ODD_PAIR_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_baseline_odd_pair_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_odd_pair_object_spec_report()
    write_baseline_odd_pair_object_spec_json()


if __name__ == "__main__":
    main()
