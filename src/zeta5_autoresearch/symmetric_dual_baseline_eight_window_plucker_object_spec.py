from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR

EIGHT_WINDOW_NORMALIZED_PLUCKER_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_eight_window_normalized_plucker_object_spec.md"
)
EIGHT_WINDOW_NORMALIZED_PLUCKER_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_eight_window_normalized_plucker_object_spec.json"
)


@dataclass(frozen=True)
class EightWindowPluckerPacketRole:
    packet_id: str
    family: str
    object_kind: str
    shared_window_start: int
    shared_window_end: int
    note: str


@dataclass(frozen=True)
class EightWindowNormalizedPluckerObjectSpec:
    spec_id: str
    object_label: str
    object_kind: str
    source_packet: EightWindowPluckerPacketRole
    target_packet: EightWindowPluckerPacketRole
    invariant_definition: str
    rationale: str
    source_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_eight_window_normalized_plucker_object_spec() -> EightWindowNormalizedPluckerObjectSpec:
    return EightWindowNormalizedPluckerObjectSpec(
        spec_id="bz_phase2_eight_window_normalized_plucker_object_spec",
        object_label="Symmetric-dual to baseline-dual eight-window normalized Plucker object",
        object_kind="paired_nonlinear_grassmannian_window_invariant",
        source_packet=EightWindowPluckerPacketRole(
            packet_id="bz_phase2_symmetric_dual_full_packet",
            family="totally_symmetric_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Exact symmetric dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.",
        ),
        target_packet=EightWindowPluckerPacketRole(
            packet_id="bz_phase2_baseline_full_packet",
            family="baseline_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Exact baseline dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.",
        ),
        invariant_definition=(
            "For each eight-term packet window `(v_n, ..., v_{n+7})`, form the normalized `Gr(3,8)` Plucker coordinate "
            "vector by dividing all `3x3` minors by the pivot minor `(1,2,3)` and omitting the pivot coordinate."
        ),
        rationale=(
            "The seven-window normalized Plucker object is now banked, and both the homogeneous and affine low-order "
            "constant-matrix ladders are exhausted there. The strongest remaining continuation is therefore a wider "
            "nonlinear invariant, with the first screen kept bounded to the last overdetermined matrix order."
        ),
        source_boundary=(
            "A success on this object would still be a bounded exact transfer statement on the shared eight-window invariant. "
            "It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane."
        ),
        non_claims=(
            "This object spec does not claim the eight-window source and target invariants are already equivalent.",
            "This object spec does not justify quotient or cross-ratio continuations, which were already weaker on smaller windows.",
            "This object spec does not claim higher matrix order is the right first screen once the order becomes underdetermined.",
        ),
        recommended_next_step=(
            "Hash the paired eight-window invariant first, then test only the overdetermined order-1 constant matrix recurrence on source and target separately."
        ),
    )


def render_eight_window_normalized_plucker_object_spec() -> str:
    spec = build_eight_window_normalized_plucker_object_spec()
    lines = [
        "# Phase 2 eight-window normalized Plucker object spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
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
        "## Invariant definition",
        "",
        spec.invariant_definition,
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


def write_eight_window_normalized_plucker_object_spec_report(
    output_path: str | Path = EIGHT_WINDOW_NORMALIZED_PLUCKER_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_eight_window_normalized_plucker_object_spec(), encoding="utf-8")
    return output


def write_eight_window_normalized_plucker_object_spec_json(
    output_path: str | Path = EIGHT_WINDOW_NORMALIZED_PLUCKER_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_eight_window_normalized_plucker_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_eight_window_normalized_plucker_object_spec_report()
    write_eight_window_normalized_plucker_object_spec_json()


if __name__ == "__main__":
    main()
