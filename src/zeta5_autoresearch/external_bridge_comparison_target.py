from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_projection_probe import DUAL_PROJECTION_PROBE_REPORT_PATH, build_phase2_dual_projection_probe
from .dual_projection_rule_experiment import (
    DUAL_PROJECTION_RULE_REPORT_PATH,
    build_phase2_dual_projection_rule_experiment,
)
from .external_bridge_spec import (
    EXTERNAL_BRIDGE_SPEC_REPORT_PATH,
    build_phase2_external_bridge_spec,
)

EXTERNAL_BRIDGE_COMPARISON_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_external_bridge_comparison_target.md"
EXTERNAL_BRIDGE_COMPARISON_JSON_PATH = CACHE_DIR / "bz_phase2_external_bridge_comparison_target.json"


@dataclass(frozen=True)
class BridgeFieldComparison:
    field_id: str
    baseline_object: str
    bridge_object: str
    current_status: str
    current_evidence: str
    next_required_artifact: str


@dataclass(frozen=True)
class ExternalBridgeComparisonTarget:
    target_id: str
    bridge_id: str
    comparison_mode: str
    comparison_fields: tuple[BridgeFieldComparison, ...]
    overall_status: str
    next_step: str


def build_phase2_external_bridge_comparison_target() -> ExternalBridgeComparisonTarget:
    spec = build_phase2_external_bridge_spec()
    probe = build_phase2_dual_projection_probe()
    rule = build_phase2_dual_projection_rule_experiment()

    return ExternalBridgeComparisonTarget(
        target_id="bz_phase2_external_bridge_comparison_target",
        bridge_id=spec.bridge_id,
        comparison_mode="shape_and_reproducibility_before_recurrence",
        comparison_fields=(
            BridgeFieldComparison(
                field_id="leading_target_channel",
                baseline_object="retained `(constant, ζ(5))` pair from the baseline dual projection rule experiment",
                bridge_object="published `q_n ζ(5) - p_n` linear form",
                current_status="partially_aligned",
                current_evidence=(
                    "The baseline side now has a retained-pair hash "
                    f"`{rule.retained_pair_hash}` on the shared exact window n=1..{rule.shared_window_end}, so the "
                    "target odd-zeta channel is explicit at the coefficient level. It is still weaker than the bridge "
                    "object because it is not yet a published or derived recurrence-based linear form."
                ),
                next_required_artifact=(
                    "A comparison probe that states one explicit normalization map from the retained pair to the "
                    "published `q_n ζ(5) - p_n` shape."
                ),
            ),
            BridgeFieldComparison(
                field_id="companion_channel",
                baseline_object="explicit residual `ζ(3)` channel from the baseline dual projection rule experiment",
                bridge_object="published companion `q_n ζ(3) - p̃_n` linear form",
                current_status="partially_aligned",
                current_evidence=(
                    "The baseline side carries a residual-channel hash "
                    f"`{rule.residual_channel_hash}` instead of hiding the companion channel. That matches the bridge "
                    "path at the bookkeeping level, but not yet at the level of a recurrence-backed companion linear form."
                ),
                next_required_artifact=(
                    "A comparison probe that states how the residual `ζ(3)` channel is to be compared to the published "
                    "companion bridge object without pretending they are already the same kind of sequence."
                ),
            ),
            BridgeFieldComparison(
                field_id="sequence_level_object",
                baseline_object="shared-window hashed packet / retained pair / residual channel",
                bridge_object="published recurrence-plus-initial-data sequence object",
                current_status="not_yet_aligned",
                current_evidence=(
                    "The baseline side is reproducible only as finite exact windows, with source packet hash "
                    f"`{probe.packet_hash}` on n=1..{probe.shared_window_end}. The bridge object is stronger because "
                    "it comes with an explicit recurrence and initial data."
                ),
                next_required_artifact=(
                    "A comparison note that records this asymmetry explicitly and refuses to overstate the baseline object "
                    "as sequence-explicit."
                ),
            ),
        ),
        overall_status=(
            "ready_for_comparison_probe"
        ),
        next_step=(
            "Write one comparison probe that takes these three fields and produces a single report saying where the "
            "baseline dual packet already matches the Zudilin 2002 bridge structurally and where it still falls short."
        ),
    )


def render_phase2_external_bridge_comparison_target() -> str:
    target = build_phase2_external_bridge_comparison_target()
    lines = [
        "# Phase 2 external bridge comparison target",
        "",
        f"- Target id: `{target.target_id}`",
        f"- Bridge spec: `{EXTERNAL_BRIDGE_SPEC_REPORT_PATH}`",
        f"- Baseline projection probe: `{DUAL_PROJECTION_PROBE_REPORT_PATH}`",
        f"- Baseline projection rule experiment: `{DUAL_PROJECTION_RULE_REPORT_PATH}`",
        f"- Bridge id: `{target.bridge_id}`",
        f"- Comparison mode: `{target.comparison_mode}`",
        f"- Overall status: `{target.overall_status}`",
        "",
        "## Comparison fields",
        "",
    ]
    for field in target.comparison_fields:
        lines.extend(
            [
                f"### {field.field_id}",
                "",
                f"- Baseline object: {field.baseline_object}",
                f"- Bridge object: {field.bridge_object}",
                f"- Current status: `{field.current_status}`",
                f"- Current evidence: {field.current_evidence}",
                f"- Next required artifact: {field.next_required_artifact}",
                "",
            ]
        )
    lines.extend(
        [
            "## Next step",
            "",
            target.next_step,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_external_bridge_comparison_target_report(
    output_path: str | Path = EXTERNAL_BRIDGE_COMPARISON_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_external_bridge_comparison_target(), encoding="utf-8")
    return output


def write_phase2_external_bridge_comparison_target_json(
    output_path: str | Path = EXTERNAL_BRIDGE_COMPARISON_JSON_PATH,
) -> Path:
    target = build_phase2_external_bridge_comparison_target()
    payload = {
        "target_id": target.target_id,
        "bridge_id": target.bridge_id,
        "comparison_mode": target.comparison_mode,
        "comparison_fields": [asdict(field) for field in target.comparison_fields],
        "overall_status": target.overall_status,
        "next_step": target.next_step,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_external_bridge_comparison_target_report()
    write_phase2_external_bridge_comparison_target_json()


if __name__ == "__main__":
    main()
