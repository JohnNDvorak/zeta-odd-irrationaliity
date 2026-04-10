from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR

SYM2_SEVEN_WINDOW_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym2_seven_window_object_spec.md"
)
SYM2_SEVEN_WINDOW_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym2_seven_window_object_spec.json"
)


@dataclass(frozen=True)
class Sym2SevenWindowPacketRole:
    packet_id: str
    family: str
    object_kind: str
    shared_window_start: int
    shared_window_end: int
    note: str


@dataclass(frozen=True)
class Sym2SevenWindowObjectSpec:
    spec_id: str
    object_label: str
    object_kind: str
    source_packet: Sym2SevenWindowPacketRole
    target_packet: Sym2SevenWindowPacketRole
    invariant_definition: str
    rationale: str
    source_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_sym2_seven_window_object_spec() -> Sym2SevenWindowObjectSpec:
    return Sym2SevenWindowObjectSpec(
        spec_id="bz_phase2_sym2_seven_window_object_spec",
        object_label="Sym^2-lifted seven-window normalized maximal-minor object",
        object_kind="paired_schur_functor_window_invariant",
        source_packet=Sym2SevenWindowPacketRole(
            packet_id="bz_phase2_symmetric_dual_full_packet",
            family="totally_symmetric_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Exact symmetric dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.",
        ),
        target_packet=Sym2SevenWindowPacketRole(
            packet_id="bz_phase2_baseline_full_packet",
            family="baseline_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Exact baseline dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.",
        ),
        invariant_definition=(
            "Lift each packet vector `(x,y,z)` to its `Sym^2` image `(x^2, xy, xz, y^2, yz, z^2)` in dimension `6`. "
            "For each seven-term lifted window, form the normalized maximal-minor coordinate vector in `Gr(6,7)` by "
            "dividing all `6x6` minors by the pivot minor of the first six columns and omitting that pivot coordinate."
        ),
        rationale=(
            "Width-only normalized Plucker objects are now exhausted through the eight-window frontier at their cheap constant-matrix screens. "
            "The strongest beyond-Plucker continuation is therefore a Schur-functor lift that changes the invariant family itself while preserving exact arithmetic."
        ),
        source_boundary=(
            "A success on this object would still be a bounded exact transfer statement on the shared Sym^2-lifted invariant. "
            "It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane."
        ),
        non_claims=(
            "This object spec does not claim the lifted source and target invariants are already equivalent.",
            "This object spec does not claim the Sym^2 lift is the unique or final Schur-functor continuation.",
            "This object spec does not justify retrying quotient or cheap order-escalation families on the earlier normalized Plucker objects.",
        ),
        recommended_next_step=(
            "Hash the paired Sym^2-lifted object first, then test the low-order constant matrix recurrence ladder through the last overdetermined order."
        ),
    )


def render_sym2_seven_window_object_spec() -> str:
    spec = build_sym2_seven_window_object_spec()
    lines = [
        "# Phase 2 Sym^2-lifted seven-window object spec",
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


def write_sym2_seven_window_object_spec_report(
    output_path: str | Path = SYM2_SEVEN_WINDOW_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym2_seven_window_object_spec(), encoding="utf-8")
    return output


def write_sym2_seven_window_object_spec_json(
    output_path: str | Path = SYM2_SEVEN_WINDOW_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_sym2_seven_window_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym2_seven_window_object_spec_report()
    write_sym2_seven_window_object_spec_json()


if __name__ == "__main__":
    main()
