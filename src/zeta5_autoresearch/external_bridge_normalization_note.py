from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_projection_rule_experiment import (
    DUAL_PROJECTION_RULE_REPORT_PATH,
    build_phase2_dual_projection_rule_experiment,
)
from .external_bridge_comparison_probe import (
    EXTERNAL_BRIDGE_COMPARISON_PROBE_REPORT_PATH,
    build_phase2_external_bridge_comparison_probe,
)
from .external_bridge_spec import EXTERNAL_BRIDGE_SPEC_REPORT_PATH

EXTERNAL_BRIDGE_NORMALIZATION_NOTE_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_external_bridge_normalization_note.md"
EXTERNAL_BRIDGE_NORMALIZATION_NOTE_JSON_PATH = CACHE_DIR / "bz_phase2_external_bridge_normalization_note.json"


@dataclass(frozen=True)
class NormalizationComparison:
    channel_id: str
    baseline_normalization: str
    bridge_normalization: str
    accepted_asymmetry: str
    comparison_statement: str


@dataclass(frozen=True)
class ExternalBridgeNormalizationNote:
    note_id: str
    bridge_id: str
    baseline_source_hash: str
    retained_pair_hash: str
    residual_channel_hash: str
    accepted_sequence_asymmetry: str
    channel_comparisons: tuple[NormalizationComparison, ...]
    overall_note: str
    next_step: str


def build_phase2_external_bridge_normalization_note() -> ExternalBridgeNormalizationNote:
    rule = build_phase2_dual_projection_rule_experiment()
    probe = build_phase2_external_bridge_comparison_probe()
    return ExternalBridgeNormalizationNote(
        note_id="bz_phase2_external_bridge_normalization_note",
        bridge_id=probe.bridge_id,
        baseline_source_hash=rule.packet_source_hash,
        retained_pair_hash=rule.retained_pair_hash,
        residual_channel_hash=rule.residual_channel_hash,
        accepted_sequence_asymmetry=(
            "The baseline side is only finite-window exact on n=1..80, while the Zudilin 2002 bridge is recurrence-explicit. "
            "This note accepts that asymmetry and compares only normalization shape, channel bookkeeping, and reproducibility level."
        ),
        channel_comparisons=(
            NormalizationComparison(
                channel_id="leading_target_channel",
                baseline_normalization="retained `(constant, ζ(5))` coefficient-side pair on the shared exact window",
                bridge_normalization="published linear form `q_n ζ(5) - p_n`",
                accepted_asymmetry=(
                    "The baseline object is a hashed retained pair, not yet a recurrence-backed linear form."
                ),
                comparison_statement=(
                    "These are comparable at the normalization level because both keep the target odd-zeta channel explicit "
                    "rather than collapsing it into a single opaque remainder."
                ),
            ),
            NormalizationComparison(
                channel_id="companion_channel",
                baseline_normalization="explicit residual `ζ(3)` channel carried alongside the retained pair",
                bridge_normalization="published companion linear form `q_n ζ(3) - p̃_n`",
                accepted_asymmetry=(
                    "The baseline side records the companion channel as residual data only; it does not yet derive a bridge-style companion recurrence."
                ),
                comparison_statement=(
                    "These are comparable at the normalization level because the companion channel is explicit and reproducible on both sides instead of being hidden or silently discarded."
                ),
            ),
            NormalizationComparison(
                channel_id="sequence_level_object",
                baseline_normalization="finite-window packet / retained-pair / residual-channel hashes",
                bridge_normalization="published recurrence plus initial data",
                accepted_asymmetry=(
                    "This is the active blocker: the baseline side is sequence-addressable only by finite windows, while the bridge side is globally sequence-explicit."
                ),
                comparison_statement=(
                    "These are not yet comparable as equal-strength sequence objects. The correct normalization-level statement is simply that the baseline side has reached reproducible finite-window exactness, not recurrence-level explicitness."
                ),
            ),
        ),
        overall_note=(
            "The normalization-level comparison is now explicit enough to support a stronger implementation-calibration step. "
            "The baseline side already matches the Zudilin 2002 bridge in the way it exposes the target and companion channels, "
            "but not in sequence-level strength."
        ),
        next_step=(
            "Use this note to drive one implementation-calibration artifact that compares the baseline retained pair and residual channel "
            "to the Zudilin 2002 bridge channels without claiming recurrence-level equivalence."
        ),
    )


def render_phase2_external_bridge_normalization_note() -> str:
    note = build_phase2_external_bridge_normalization_note()
    lines = [
        "# Phase 2 external bridge normalization note",
        "",
        f"- Note id: `{note.note_id}`",
        f"- Bridge spec: `{EXTERNAL_BRIDGE_SPEC_REPORT_PATH}`",
        f"- Comparison probe: `{EXTERNAL_BRIDGE_COMPARISON_PROBE_REPORT_PATH}`",
        f"- Baseline rule experiment: `{DUAL_PROJECTION_RULE_REPORT_PATH}`",
        f"- Bridge id: `{note.bridge_id}`",
        f"- Baseline source hash: `{note.baseline_source_hash}`",
        f"- Retained pair hash: `{note.retained_pair_hash}`",
        f"- Residual channel hash: `{note.residual_channel_hash}`",
        "",
        "## Accepted sequence asymmetry",
        "",
        note.accepted_sequence_asymmetry,
        "",
        "## Channel comparisons",
        "",
    ]
    for item in note.channel_comparisons:
        lines.extend(
            [
                f"### {item.channel_id}",
                "",
                f"- Baseline normalization: {item.baseline_normalization}",
                f"- Bridge normalization: {item.bridge_normalization}",
                f"- Accepted asymmetry: {item.accepted_asymmetry}",
                f"- Comparison statement: {item.comparison_statement}",
                "",
            ]
        )
    lines.extend(
        [
            "## Overall note",
            "",
            note.overall_note,
            "",
            "## Next step",
            "",
            note.next_step,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_external_bridge_normalization_note_report(
    output_path: str | Path = EXTERNAL_BRIDGE_NORMALIZATION_NOTE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_external_bridge_normalization_note(), encoding="utf-8")
    return output


def write_phase2_external_bridge_normalization_note_json(
    output_path: str | Path = EXTERNAL_BRIDGE_NORMALIZATION_NOTE_JSON_PATH,
) -> Path:
    note = build_phase2_external_bridge_normalization_note()
    payload = {
        "note_id": note.note_id,
        "bridge_id": note.bridge_id,
        "baseline_source_hash": note.baseline_source_hash,
        "retained_pair_hash": note.retained_pair_hash,
        "residual_channel_hash": note.residual_channel_hash,
        "accepted_sequence_asymmetry": note.accepted_sequence_asymmetry,
        "channel_comparisons": [asdict(item) for item in note.channel_comparisons],
        "overall_note": note.overall_note,
        "next_step": note.next_step,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_external_bridge_normalization_note_report()
    write_phase2_external_bridge_normalization_note_json()


if __name__ == "__main__":
    main()
