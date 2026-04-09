from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_full_packet_compression_decision_gate import (
    BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH,
)
from .config import CACHE_DIR, DATA_DIR
from .symmetric_source_packet_compression_decision_gate import (
    SYMMETRIC_SOURCE_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH,
)

SYMMETRIC_BASELINE_TRANSFER_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_baseline_transfer_object_spec.md"
)
SYMMETRIC_BASELINE_TRANSFER_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_baseline_transfer_object_spec.json"
)


@dataclass(frozen=True)
class TransferPacketRole:
    packet_id: str
    family: str
    object_kind: str
    shared_window_start: int
    shared_window_end: int
    note: str


@dataclass(frozen=True)
class SymmetricBaselineTransferObjectSpec:
    spec_id: str
    object_label: str
    object_kind: str
    source_packet: TransferPacketRole
    target_packet: TransferPacketRole
    transfer_semantics: str
    rationale: str
    source_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_symmetric_baseline_transfer_object_spec() -> SymmetricBaselineTransferObjectSpec:
    return SymmetricBaselineTransferObjectSpec(
        spec_id="bz_phase2_symmetric_baseline_transfer_object_spec",
        object_label="Symmetric-to-baseline packet transfer object",
        object_kind="paired_source_target_exact_packet_transfer_object",
        source_packet=TransferPacketRole(
            packet_id="bz_totally_symmetric_scaled_linear_forms_packet",
            family="totally_symmetric_linear_form_pipeline",
            object_kind="source_backed_scaled_exact_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Recurrence-explicit source-backed packet `(d_n^5 Q_n, d_n^5 P_n, d_n^2 d_{2n} P̂_n)`.",
        ),
        target_packet=TransferPacketRole(
            packet_id="bz_phase2_baseline_full_packet",
            family="baseline_dual_f7_packet",
            object_kind="baseline_side_exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Baseline dual full packet `(constant, zeta(3), zeta(5))` on the shared exact window.",
        ),
        transfer_semantics=(
            "The active transfer object pairs a source-backed totally symmetric exact packet with the exact baseline dual "
            "full packet on the shared window `n=1..80`. It is a bounded transfer test bed, not a claim that the two "
            "families are already identified."
        ),
        rationale=(
            "The baseline full packet and the symmetric source packet have each exhausted their own low-complexity internal "
            "pairwise compression ladders. The next honest move is to test whether a bounded exact packet-level transfer exists "
            "between the two families before enlarging either family internally."
        ),
        source_boundary=(
            "A transfer success would still be a packet-level relation on a finite exact window. It would not by itself prove "
            "baseline equivalence, baseline P_n extraction, or a baseline remainder pipeline."
        ),
        non_claims=(
            "This spec does not claim the symmetric family equals the baseline family.",
            "This spec does not claim the transfer object is motivic or canonical.",
            "This spec does not permit importing source-side recurrences as baseline-side recurrences without a proved transfer.",
        ),
        recommended_next_step=(
            "Hash the paired source/target packets first, then test one bounded low-complexity packet-map ladder."
        ),
    )


def render_symmetric_baseline_transfer_object_spec() -> str:
    spec = build_symmetric_baseline_transfer_object_spec()
    lines = [
        "# Phase 2 symmetric-to-baseline transfer object spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Prior baseline hard wall: `{BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH}`",
        f"- Prior symmetric hard wall: `{SYMMETRIC_SOURCE_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH}`",
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


def write_symmetric_baseline_transfer_object_spec_report(
    output_path: str | Path = SYMMETRIC_BASELINE_TRANSFER_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_baseline_transfer_object_spec(), encoding="utf-8")
    return output


def write_symmetric_baseline_transfer_object_spec_json(
    output_path: str | Path = SYMMETRIC_BASELINE_TRANSFER_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_symmetric_baseline_transfer_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_baseline_transfer_object_spec_report()
    write_symmetric_baseline_transfer_object_spec_json()


if __name__ == "__main__":
    main()
