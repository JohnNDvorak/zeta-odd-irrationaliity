from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_projection_decision_gate import DUAL_PROJECTION_DECISION_REPORT_PATH
from .external_calibration_check import (
    EXTERNAL_CALIBRATION_REPORT_PATH,
    build_phase2_external_calibration_check,
)
from .literature_verification import (
    LITERATURE_VERIFICATION_REPORT_PATH,
    build_phase2_literature_claims,
)

EXTERNAL_BRIDGE_SPEC_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_external_bridge_spec.md"
EXTERNAL_BRIDGE_SPEC_JSON_PATH = CACHE_DIR / "bz_phase2_external_bridge_spec.json"


@dataclass(frozen=True)
class BridgeComparisonField:
    field_id: str
    target_object: str
    calibration_anchor: str
    comparison_role: str


@dataclass(frozen=True)
class ExternalBridgeSpec:
    spec_id: str
    bridge_id: str
    source: str
    location: str
    bridge_object: str
    bridge_summary: str
    why_now: str
    comparison_fields: tuple[BridgeComparisonField, ...]
    implementation_contract: tuple[str, ...]
    success_condition: str


def build_phase2_external_bridge_spec() -> ExternalBridgeSpec:
    calibration = build_phase2_external_calibration_check()
    claim = next(
        item
        for item in build_phase2_literature_claims()
        if item.source == calibration.chosen_source and item.verdict == "confirmed"
    )
    return ExternalBridgeSpec(
        spec_id="bz_phase2_external_bridge_spec",
        bridge_id=calibration.chosen_anchor_id,
        source=claim.source,
        location=claim.location,
        bridge_object="Published recurrence-based linear forms ℓ_n = q_n ζ(5) - p_n and ℓ̃_n = q_n ζ(3) - p̃_n",
        bridge_summary=(
            "Use the Zudilin 2002 third-order recurrence construction as the first implementation-calibration target. "
            "It is not the Brown-Zudilin baseline family, but it is explicit at the exact linear-form level and has the "
            "right two-channel shape for a controlled coefficient-side comparison."
        ),
        why_now=(
            "The dual projection decision gate chose the external bridge path because the baseline projection rule "
            "experiment remained bookkeeping-only. This bridge object is the strongest verified next target because it "
            "lets us compare an explicit published zeta(5)/zeta(3) linear-form structure against the repo's baseline dual-side conventions."
        ),
        comparison_fields=(
            BridgeComparisonField(
                field_id="leading_target_channel",
                target_object="baseline dual F_7 retained `(constant, ζ(5))` pair",
                calibration_anchor="published `q_n ζ(5) - p_n`",
                comparison_role="Check whether the repo records the target odd-zeta channel with explicit coefficient bookkeeping instead of a scalar-only remainder.",
            ),
            BridgeComparisonField(
                field_id="companion_channel",
                target_object="baseline dual residual `ζ(3)` channel",
                calibration_anchor="published companion `q_n ζ(3) - p̃_n`",
                comparison_role="Check whether companion-channel handling is explicit and reproducible rather than hidden or discarded.",
            ),
            BridgeComparisonField(
                field_id="sequence_level_object",
                target_object="shared-window hashed packet / retained pair / residual channel",
                calibration_anchor="published recurrence-plus-initial-data sequence object",
                comparison_role="Record where the repo object is still weaker than the external bridge because it lacks a published recurrence and only has finite exact windows.",
            ),
        ),
        implementation_contract=(
            "Do not try to rederive the full Zudilin 2002 construction immediately; first encode the bridge object as a comparison target with the three fields above.",
            "Keep the comparison one level above numerics: compare object shape, channel bookkeeping, and reproducibility assumptions before any performance-heavy extraction work.",
            "Treat a mismatch as useful information about the baseline dual conventions, not as a failure of the bridge path itself.",
        ),
        success_condition=(
            "The next artifact names one explicit comparison target derived from Zudilin 2002 and states exactly how the baseline dual packet will be compared against it on the three bridge fields."
        ),
    )


def render_phase2_external_bridge_spec() -> str:
    spec = build_phase2_external_bridge_spec()
    lines = [
        "# Phase 2 external bridge spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Bridge id: `{spec.bridge_id}`",
        f"- Source: `{spec.source}`",
        f"- Location: `{spec.location}`",
        f"- Literature verification report: `{LITERATURE_VERIFICATION_REPORT_PATH}`",
        f"- External calibration report: `{EXTERNAL_CALIBRATION_REPORT_PATH}`",
        f"- Dual projection decision gate: `{DUAL_PROJECTION_DECISION_REPORT_PATH}`",
        "",
        "## Bridge object",
        "",
        f"- {spec.bridge_object}",
        "",
        "## Summary",
        "",
        spec.bridge_summary,
        "",
        "## Why now",
        "",
        spec.why_now,
        "",
        "## Comparison fields",
        "",
        "| field | target object | calibration anchor | comparison role |",
        "| --- | --- | --- | --- |",
    ]
    for field in spec.comparison_fields:
        lines.append(
            f"| `{field.field_id}` | {field.target_object} | {field.calibration_anchor} | {field.comparison_role} |"
        )
    lines.extend(
        [
            "",
            "## Implementation contract",
            "",
        ]
    )
    for item in spec.implementation_contract:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Success condition",
            "",
            spec.success_condition,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_external_bridge_spec_report(
    output_path: str | Path = EXTERNAL_BRIDGE_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_external_bridge_spec(), encoding="utf-8")
    return output


def write_phase2_external_bridge_spec_json(
    output_path: str | Path = EXTERNAL_BRIDGE_SPEC_JSON_PATH,
) -> Path:
    spec = build_phase2_external_bridge_spec()
    payload = {
        "spec_id": spec.spec_id,
        "bridge_id": spec.bridge_id,
        "source": spec.source,
        "location": spec.location,
        "bridge_object": spec.bridge_object,
        "bridge_summary": spec.bridge_summary,
        "why_now": spec.why_now,
        "comparison_fields": [asdict(field) for field in spec.comparison_fields],
        "implementation_contract": list(spec.implementation_contract),
        "success_condition": spec.success_condition,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_external_bridge_spec_report()
    write_phase2_external_bridge_spec_json()


if __name__ == "__main__":
    main()
