from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .external_bridge_implementation_calibration import (
    EXTERNAL_BRIDGE_IMPLEMENTATION_CALIBRATION_REPORT_PATH,
    build_phase2_external_bridge_implementation_calibration,
)
from .external_bridge_normalization_note import (
    EXTERNAL_BRIDGE_NORMALIZATION_NOTE_REPORT_PATH,
    build_phase2_external_bridge_normalization_note,
)

EXTERNAL_BRIDGE_COMPARISON_IMPLEMENTATION_NOTE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_external_bridge_comparison_implementation_note.md"
)
EXTERNAL_BRIDGE_COMPARISON_IMPLEMENTATION_NOTE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_external_bridge_comparison_implementation_note.json"
)


@dataclass(frozen=True)
class ImplementationComparisonItem:
    item_id: str
    baseline_object: str
    bridge_object: str
    allowed_statement: str
    forbidden_statement: str


@dataclass(frozen=True)
class ExternalBridgeComparisonImplementationNote:
    note_id: str
    bridge_id: str
    retained_pair_hash: str
    residual_channel_hash: str
    accepted_asymmetry: str
    items: tuple[ImplementationComparisonItem, ...]
    implementation_verdict: str
    next_step: str


def build_phase2_external_bridge_comparison_implementation_note() -> ExternalBridgeComparisonImplementationNote:
    calibration = build_phase2_external_bridge_implementation_calibration()
    normalization = build_phase2_external_bridge_normalization_note()
    return ExternalBridgeComparisonImplementationNote(
        note_id="bz_phase2_external_bridge_comparison_implementation_note",
        bridge_id=calibration.bridge_id,
        retained_pair_hash=calibration.retained_pair_hash,
        residual_channel_hash=calibration.residual_channel_hash,
        accepted_asymmetry=calibration.accepted_asymmetry,
        items=(
            ImplementationComparisonItem(
                item_id="leading_target_channel",
                baseline_object="baseline retained `(constant, ζ(5))` pair",
                bridge_object="published `q_n ζ(5) - p_n` bridge channel",
                allowed_statement=(
                    "The baseline side and the bridge side are comparable as explicit target-channel objects with named odd-zeta structure and reproducible indexing."
                ),
                forbidden_statement=(
                    "Do not state or imply that the baseline retained pair is already the same kind of recurrence-backed linear form as `q_n ζ(5) - p_n`."
                ),
            ),
            ImplementationComparisonItem(
                item_id="companion_channel",
                baseline_object="baseline residual `ζ(3)` channel",
                bridge_object="published companion `q_n ζ(3) - p̃_n` bridge channel",
                allowed_statement=(
                    "The baseline side and the bridge side are comparable as explicit companion-channel objects that remain visible rather than being silently discarded."
                ),
                forbidden_statement=(
                    "Do not claim that the baseline residual `ζ(3)` channel has been analytically eliminated or normalized into the target channel."
                ),
            ),
            ImplementationComparisonItem(
                item_id="sequence_level_object",
                baseline_object="finite-window hashed packet / retained-pair / residual-channel objects",
                bridge_object="published recurrence plus initial data",
                allowed_statement=(
                    "The baseline side can only be compared to the bridge side as a finite-window exact object with weaker sequence-level strength."
                ),
                forbidden_statement=(
                    "Do not present the baseline side as sequence-explicit in the same sense as the Zudilin 2002 bridge."
                ),
            ),
        ),
        implementation_verdict=(
            "The bridge comparison is now implementable in a disciplined way: compare explicit target and companion channels directly, "
            "but carry the finite-window versus recurrence asymmetry as a permanent disclaimer rather than trying to hide it."
        ),
        next_step=(
            "Use this note as the stable rulebook for any later bridge-comparison code or report. The next genuinely new mathematical move "
            "would be either to shrink the sequence-strength gap or to find a stronger bridge object, not to restate the same comparison again."
        ),
    )


def render_phase2_external_bridge_comparison_implementation_note() -> str:
    note = build_phase2_external_bridge_comparison_implementation_note()
    lines = [
        "# Phase 2 external bridge comparison implementation note",
        "",
        f"- Note id: `{note.note_id}`",
        f"- Implementation calibration: `{EXTERNAL_BRIDGE_IMPLEMENTATION_CALIBRATION_REPORT_PATH}`",
        f"- Normalization note: `{EXTERNAL_BRIDGE_NORMALIZATION_NOTE_REPORT_PATH}`",
        f"- Bridge id: `{note.bridge_id}`",
        f"- Retained pair hash: `{note.retained_pair_hash}`",
        f"- Residual channel hash: `{note.residual_channel_hash}`",
        "",
        "## Accepted asymmetry",
        "",
        note.accepted_asymmetry,
        "",
        "## Implementation items",
        "",
    ]
    for item in note.items:
        lines.extend(
            [
                f"### {item.item_id}",
                "",
                f"- Baseline object: {item.baseline_object}",
                f"- Bridge object: {item.bridge_object}",
                f"- Allowed statement: {item.allowed_statement}",
                f"- Forbidden statement: {item.forbidden_statement}",
                "",
            ]
        )
    lines.extend(
        [
            "## Implementation verdict",
            "",
            note.implementation_verdict,
            "",
            "## Next step",
            "",
            note.next_step,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_external_bridge_comparison_implementation_note_report(
    output_path: str | Path = EXTERNAL_BRIDGE_COMPARISON_IMPLEMENTATION_NOTE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_external_bridge_comparison_implementation_note(), encoding="utf-8")
    return output


def write_phase2_external_bridge_comparison_implementation_note_json(
    output_path: str | Path = EXTERNAL_BRIDGE_COMPARISON_IMPLEMENTATION_NOTE_JSON_PATH,
) -> Path:
    note = build_phase2_external_bridge_comparison_implementation_note()
    payload = {
        "note_id": note.note_id,
        "bridge_id": note.bridge_id,
        "retained_pair_hash": note.retained_pair_hash,
        "residual_channel_hash": note.residual_channel_hash,
        "accepted_asymmetry": note.accepted_asymmetry,
        "items": [asdict(item) for item in note.items],
        "implementation_verdict": note.implementation_verdict,
        "next_step": note.next_step,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_external_bridge_comparison_implementation_note_report()
    write_phase2_external_bridge_comparison_implementation_note_json()


if __name__ == "__main__":
    main()
