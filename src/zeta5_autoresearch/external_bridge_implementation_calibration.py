from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .external_bridge_normalization_note import (
    EXTERNAL_BRIDGE_NORMALIZATION_NOTE_REPORT_PATH,
    build_phase2_external_bridge_normalization_note,
)

EXTERNAL_BRIDGE_IMPLEMENTATION_CALIBRATION_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_external_bridge_implementation_calibration.md"
)
EXTERNAL_BRIDGE_IMPLEMENTATION_CALIBRATION_JSON_PATH = (
    CACHE_DIR / "bz_phase2_external_bridge_implementation_calibration.json"
)


@dataclass(frozen=True)
class CalibrationRule:
    rule_id: str
    allowed_comparison: str
    forbidden_claim: str
    required_disclosure: str


@dataclass(frozen=True)
class ExternalBridgeImplementationCalibration:
    calibration_id: str
    bridge_id: str
    retained_pair_hash: str
    residual_channel_hash: str
    accepted_asymmetry: str
    rules: tuple[CalibrationRule, ...]
    readiness_status: str
    next_artifact: str


def build_phase2_external_bridge_implementation_calibration() -> ExternalBridgeImplementationCalibration:
    note = build_phase2_external_bridge_normalization_note()
    return ExternalBridgeImplementationCalibration(
        calibration_id="bz_phase2_external_bridge_implementation_calibration",
        bridge_id=note.bridge_id,
        retained_pair_hash=note.retained_pair_hash,
        residual_channel_hash=note.residual_channel_hash,
        accepted_asymmetry=note.accepted_sequence_asymmetry,
        rules=(
            CalibrationRule(
                rule_id="compare_channel_shape_only",
                allowed_comparison=(
                    "Compare the baseline retained `(constant, ζ(5))` pair to the published `q_n ζ(5) - p_n` bridge "
                    "only at the level of channel shape, explicit coefficient bookkeeping, and reproducible indexing."
                ),
                forbidden_claim=(
                    "Do not claim that the retained pair already equals a bridge-style recurrence-backed linear form."
                ),
                required_disclosure=(
                    "State explicitly that the baseline side is finite-window exact while the bridge side is recurrence-explicit."
                ),
            ),
            CalibrationRule(
                rule_id="compare_companion_channel_openly",
                allowed_comparison=(
                    "Compare the baseline residual `ζ(3)` channel to the published companion `q_n ζ(3) - p̃_n` bridge "
                    "as an explicit companion-channel object."
                ),
                forbidden_claim=(
                    "Do not treat the residual channel as eliminated, negligible, or already normalized away."
                ),
                required_disclosure=(
                    "State that the baseline side carries the `ζ(3)` channel as residual data only, without a bridge-style recurrence."
                ),
            ),
            CalibrationRule(
                rule_id="accept_sequence_strength_gap",
                allowed_comparison=(
                    "Use hashes and shared exact windows to compare reproducibility level and object shape."
                ),
                forbidden_claim=(
                    "Do not present the baseline packet or retained pair as sequence-explicit in the same sense as the Zudilin 2002 bridge."
                ),
                required_disclosure=(
                    "Name the finite-window versus recurrence-level asymmetry as the active blocker in every implementation-calibration artifact."
                ),
            ),
        ),
        readiness_status="ready_for_bridge_comparison_implementation",
        next_artifact=(
            "Implement one bridge-comparison implementation note that applies these three rules directly to the baseline "
            "retained pair and residual `ζ(3)` channel against the Zudilin 2002 bridge channels."
        ),
    )


def render_phase2_external_bridge_implementation_calibration() -> str:
    calibration = build_phase2_external_bridge_implementation_calibration()
    lines = [
        "# Phase 2 external bridge implementation calibration",
        "",
        f"- Calibration id: `{calibration.calibration_id}`",
        f"- Normalization note: `{EXTERNAL_BRIDGE_NORMALIZATION_NOTE_REPORT_PATH}`",
        f"- Bridge id: `{calibration.bridge_id}`",
        f"- Retained pair hash: `{calibration.retained_pair_hash}`",
        f"- Residual channel hash: `{calibration.residual_channel_hash}`",
        f"- Readiness status: `{calibration.readiness_status}`",
        "",
        "## Accepted asymmetry",
        "",
        calibration.accepted_asymmetry,
        "",
        "## Calibration rules",
        "",
    ]
    for rule in calibration.rules:
        lines.extend(
            [
                f"### {rule.rule_id}",
                "",
                f"- Allowed comparison: {rule.allowed_comparison}",
                f"- Forbidden claim: {rule.forbidden_claim}",
                f"- Required disclosure: {rule.required_disclosure}",
                "",
            ]
        )
    lines.extend(
        [
            "## Next artifact",
            "",
            calibration.next_artifact,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_external_bridge_implementation_calibration_report(
    output_path: str | Path = EXTERNAL_BRIDGE_IMPLEMENTATION_CALIBRATION_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_external_bridge_implementation_calibration(), encoding="utf-8")
    return output


def write_phase2_external_bridge_implementation_calibration_json(
    output_path: str | Path = EXTERNAL_BRIDGE_IMPLEMENTATION_CALIBRATION_JSON_PATH,
) -> Path:
    calibration = build_phase2_external_bridge_implementation_calibration()
    payload = {
        "calibration_id": calibration.calibration_id,
        "bridge_id": calibration.bridge_id,
        "retained_pair_hash": calibration.retained_pair_hash,
        "residual_channel_hash": calibration.residual_channel_hash,
        "accepted_asymmetry": calibration.accepted_asymmetry,
        "rules": [asdict(rule) for rule in calibration.rules],
        "readiness_status": calibration.readiness_status,
        "next_artifact": calibration.next_artifact,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_external_bridge_implementation_calibration_report()
    write_phase2_external_bridge_implementation_calibration_json()


if __name__ == "__main__":
    main()
