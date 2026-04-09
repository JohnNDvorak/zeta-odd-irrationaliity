from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_full_packet_compression_decision_gate import (
    BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH,
)
from .config import CACHE_DIR, DATA_DIR
from .symmetric_baseline_transfer_decision_gate import (
    SYMMETRIC_BASELINE_TRANSFER_DECISION_GATE_REPORT_PATH,
)

SYMMETRIC_DUAL_BASELINE_TRANSFER_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_dual_baseline_transfer_object_spec.md"
)
SYMMETRIC_DUAL_BASELINE_TRANSFER_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_dual_baseline_transfer_object_spec.json"
)


@dataclass(frozen=True)
class SymmetricDualTransferPacketRole:
    packet_id: str
    family: str
    object_kind: str
    shared_window_start: int
    shared_window_end: int
    note: str


@dataclass(frozen=True)
class SymmetricDualBaselineTransferObjectSpec:
    spec_id: str
    object_label: str
    object_kind: str
    source_packet: SymmetricDualTransferPacketRole
    target_packet: SymmetricDualTransferPacketRole
    transfer_semantics: str
    rationale: str
    source_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_symmetric_dual_baseline_transfer_object_spec() -> SymmetricDualBaselineTransferObjectSpec:
    return SymmetricDualBaselineTransferObjectSpec(
        spec_id="bz_phase2_symmetric_dual_baseline_transfer_object_spec",
        object_label="Symmetric-dual to baseline-dual transfer object",
        object_kind="paired_exact_dual_packet_transfer_object",
        source_packet=SymmetricDualTransferPacketRole(
            packet_id="bz_phase2_symmetric_dual_full_packet",
            family="totally_symmetric_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Symmetric dual full packet `(constant, zeta(3), zeta(5))` from the same exact F_7 extraction family.",
        ),
        target_packet=SymmetricDualTransferPacketRole(
            packet_id="bz_phase2_baseline_full_packet",
            family="baseline_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Baseline dual full packet `(constant, zeta(3), zeta(5))` on the same shared exact window.",
        ),
        transfer_semantics=(
            "The active transfer object pairs the symmetric dual F_7 full packet with the baseline dual F_7 full packet. "
            "This is the most structurally aligned packet-transfer object currently available: same extraction family, same coefficient basis, same exact window."
        ),
        rationale=(
            "The mixed symmetric-source to baseline transfer object exhausted its low-complexity ladder. The strongest remaining "
            "different transfer object is the direct dual-to-dual packet pairing, because it removes the family-type mismatch and tests whether the obstruction survives inside a single exact extraction framework."
        ),
        source_boundary=(
            "A transfer success would still be a bounded packet-level relation on `n=1..80`. It would not by itself prove baseline equivalence, a baseline recurrence, or a baseline remainder pipeline."
        ),
        non_claims=(
            "This spec does not claim the symmetric dual packet and the baseline dual packet are already equivalent.",
            "This spec does not import symmetric identities into the baseline packet without a proved transfer.",
            "This spec does not justify skipping the bounded transfer family ladder.",
        ),
        recommended_next_step=(
            "Hash the paired dual packets first, then test one bounded low-complexity packet-map ladder."
        ),
    )


def render_symmetric_dual_baseline_transfer_object_spec() -> str:
    spec = build_symmetric_dual_baseline_transfer_object_spec()
    lines = [
        "# Phase 2 symmetric-dual to baseline-dual transfer object spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Prior baseline packet hard wall: `{BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH}`",
        f"- Prior mixed-family transfer hard wall: `{SYMMETRIC_BASELINE_TRANSFER_DECISION_GATE_REPORT_PATH}`",
        f"- Object label: `{spec.object_label}`",
        f"- Object kind: `{spec.object_kind}`",
        "",
        "## Source packet",
        "",
        f"- Packet id: `{spec.source_packet.packet_id}`",
        f"- Family: `{spec.source_packet.family}`",
        f"- Kind: `{spec.source_packet.object_kind}`",
        f"- Shared window: `n={spec.source_packet.shared_window_start}..{spec.source_packet.shared_window_end}`",
        f"- Note: {spec.source_packet.note}",
        "",
        "## Target packet",
        "",
        f"- Packet id: `{spec.target_packet.packet_id}`",
        f"- Family: `{spec.target_packet.family}`",
        f"- Kind: `{spec.target_packet.object_kind}`",
        f"- Shared window: `n={spec.target_packet.shared_window_start}..{spec.target_packet.shared_window_end}`",
        f"- Note: {spec.target_packet.note}",
        "",
        "## Transfer semantics",
        "",
        spec.transfer_semantics,
        "",
        "## Rationale",
        "",
        spec.rationale,
        "",
        "## Source boundary",
        "",
        spec.source_boundary,
        "",
        "## Non-claims",
        "",
    ]
    for item in spec.non_claims:
        lines.append(f"- {item}")
    lines.extend(["", "## Recommended next step", "", spec.recommended_next_step, ""])
    return "\n".join(lines)


def write_symmetric_dual_baseline_transfer_object_spec_report(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_TRANSFER_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_dual_baseline_transfer_object_spec(), encoding="utf-8")
    return output


def write_symmetric_dual_baseline_transfer_object_spec_json(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_TRANSFER_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_symmetric_dual_baseline_transfer_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_dual_baseline_transfer_object_spec_report()
    write_symmetric_dual_baseline_transfer_object_spec_json()


if __name__ == "__main__":
    main()
