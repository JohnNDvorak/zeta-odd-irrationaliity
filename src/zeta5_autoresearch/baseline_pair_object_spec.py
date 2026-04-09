from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_extraction_implementation_plan import (
    BASELINE_EXTRACTION_IMPLEMENTATION_PLAN_REPORT_PATH,
    build_baseline_extraction_implementation_plan,
)
from .config import CACHE_DIR, DATA_DIR
from .dual_projection_target_spec import (
    DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH,
    build_phase2_dual_projection_target_spec,
)

BASELINE_PAIR_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_pair_object_spec.md"
)
BASELINE_PAIR_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_pair_object_spec.json"
)


@dataclass(frozen=True)
class BaselinePairComponent:
    component_id: str
    source_component: str
    role: str
    max_verified_index: int
    exact_status: str
    note: str


@dataclass(frozen=True)
class BaselineExtractionOutputType:
    output_id: str
    label: str
    semantics: str
    non_claim: str


@dataclass(frozen=True)
class BaselinePairObjectSpec:
    spec_id: str
    baseline_seed: str
    source_packet_id: str
    object_label: str
    object_kind: str
    object_semantics: str
    components: tuple[BaselinePairComponent, ...]
    extraction_output: BaselineExtractionOutputType
    bridge_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_baseline_pair_object_spec() -> BaselinePairObjectSpec:
    plan = build_baseline_extraction_implementation_plan()
    target = build_phase2_dual_projection_target_spec()

    target_components = {component.component_id: component for component in target.components}

    return BaselinePairObjectSpec(
        spec_id="bz_phase2_baseline_pair_object_spec",
        baseline_seed=plan.baseline_seed,
        source_packet_id=target.target_id,
        object_label="Baseline extraction pair object",
        object_kind="baseline_side_exact_pair_with_explicit_residual",
        object_semantics=(
            "The active baseline-side extraction object is the ordered pair `(constant, zeta(5))` drawn from the exact "
            "baseline dual F_7 coefficient packet, together with the explicit residual `zeta(3)` channel carried as "
            "side information. This is a baseline-native extraction object, not a bridge-fit surrogate."
        ),
        components=(
            BaselinePairComponent(
                component_id="retained_constant",
                source_component="constant",
                role="rational constant term retained in the active extraction pair",
                max_verified_index=target_components["constant"].max_verified_index,
                exact_status=target_components["constant"].exact_status,
                note="This is retained because the current baseline packet already stabilizes it exactly and it pairs naturally with the zeta(5) coefficient.",
            ),
            BaselinePairComponent(
                component_id="retained_zeta5",
                source_component="zeta5",
                role="exact zeta(5) coefficient retained in the active extraction pair",
                max_verified_index=target_components["zeta5"].max_verified_index,
                exact_status=target_components["zeta5"].exact_status,
                note="This is the odd-target component of primary proof interest, but its verified window is currently the shortest component frontier.",
            ),
            BaselinePairComponent(
                component_id="residual_zeta3",
                source_component="zeta3",
                role="explicit residual companion channel carried alongside the retained pair",
                max_verified_index=target_components["zeta3"].max_verified_index,
                exact_status=target_components["zeta3"].exact_status,
                note="This remains explicit to prevent accidental collapse back into one-channel extraction rhetoric.",
            ),
        ),
        extraction_output=BaselineExtractionOutputType(
            output_id="baseline_extraction_summary_v1",
            label="Bounded baseline extraction summary",
            semantics=(
                "A bounded extraction summary is a repo-native object produced from the baseline pair object that may "
                "recombine or filter the retained pair while recording the unresolved residual channel explicitly."
            ),
            non_claim="It is not, by default, a claimed baseline P_n sequence or a proved baseline remainder pipeline.",
        ),
        bridge_boundary=(
            "The Zudilin 2002 bridge stack may be used only as calibration to sanity-check bookkeeping conventions and failure modes. "
            "It may not redefine the active baseline object or supply hidden identities for it."
        ),
        non_claims=(
            "This spec does not claim that `(constant, zeta(5))` is the unique correct baseline extraction object.",
            "This spec does not eliminate the residual `zeta(3)` channel.",
            "This spec does not claim a baseline P_n extraction.",
        ),
        recommended_next_step=(
            "Implement one bounded extraction rule on this baseline pair object and require the output to distinguish retained output from residual unresolved structure."
        ),
    )


def render_baseline_pair_object_spec() -> str:
    spec = build_baseline_pair_object_spec()
    lines = [
        "# Phase 2 baseline pair object spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Baseline seed: `{spec.baseline_seed}`",
        f"- Extraction implementation plan: `{BASELINE_EXTRACTION_IMPLEMENTATION_PLAN_REPORT_PATH}`",
        f"- Source packet spec: `{DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH}`",
        f"- Source packet id: `{spec.source_packet_id}`",
        f"- Object label: `{spec.object_label}`",
        f"- Object kind: `{spec.object_kind}`",
        "",
        "## Object semantics",
        "",
        spec.object_semantics,
        "",
        "## Components",
        "",
        "| component | source component | role | max verified index | exact status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for component in spec.components:
        lines.append(
            f"| `{component.component_id}` | `{component.source_component}` | {component.role} | `{component.max_verified_index}` | `{component.exact_status}` |"
        )
    lines.extend(
        [
            "",
            "## Component notes",
            "",
        ]
    )
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
    lines.extend(
        [
            "",
            "## Recommended next step",
            "",
            spec.recommended_next_step,
            "",
        ]
    )
    return "\n".join(lines)


def write_baseline_pair_object_spec_report(
    output_path: str | Path = BASELINE_PAIR_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_pair_object_spec(), encoding="utf-8")
    return output


def write_baseline_pair_object_spec_json(
    output_path: str | Path = BASELINE_PAIR_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_baseline_pair_object_spec()
    payload = asdict(spec)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_pair_object_spec_report()
    write_baseline_pair_object_spec_json()


if __name__ == "__main__":
    main()
