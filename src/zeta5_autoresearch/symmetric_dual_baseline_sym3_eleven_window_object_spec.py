from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR

SYM3_ELEVEN_WINDOW_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym3_eleven_window_object_spec.md"
)
SYM3_ELEVEN_WINDOW_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym3_eleven_window_object_spec.json"
)


@dataclass(frozen=True)
class Sym3ElevenWindowPacketRole:
    packet_id: str
    family: str
    object_kind: str
    shared_window_start: int
    shared_window_end: int
    note: str


@dataclass(frozen=True)
class Sym3ElevenWindowObjectSpec:
    spec_id: str
    object_label: str
    object_kind: str
    source_packet: Sym3ElevenWindowPacketRole
    target_packet: Sym3ElevenWindowPacketRole
    invariant_definition: str
    rationale: str
    source_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_sym3_eleven_window_object_spec() -> Sym3ElevenWindowObjectSpec:
    return Sym3ElevenWindowObjectSpec(
        spec_id="bz_phase2_sym3_eleven_window_object_spec",
        object_label="Sym^3-lifted eleven-window normalized maximal-minor object",
        object_kind="paired_higher_schur_window_invariant",
        source_packet=Sym3ElevenWindowPacketRole(
            packet_id="bz_phase2_symmetric_dual_full_packet",
            family="totally_symmetric_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Exact symmetric dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.",
        ),
        target_packet=Sym3ElevenWindowPacketRole(
            packet_id="bz_phase2_baseline_full_packet",
            family="baseline_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Exact baseline dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.",
        ),
        invariant_definition=(
            "Lift each packet vector `(x,y,z)` to its `Sym^3` image in dimension `10`, using the cubic monomial basis "
            "`(x^3, x^2 y, x^2 z, x y^2, x y z, x z^2, y^3, y^2 z, y z^2, z^3)`. For each eleven-term lifted window, "
            "form the normalized maximal-minor coordinate vector in `Gr(10,11)` by dividing all `10x10` minors by the "
            "pivot minor of the first ten columns and omitting that pivot coordinate."
        ),
        rationale=(
            "The `Sym^2`-lifted seven-window and eight-window objects are now banked. The strongest structurally different continuation is therefore a higher Schur lift that still leaves a genuine overdetermined matrix ladder through order `6`."
        ),
        source_boundary=(
            "A success on this object would still be a bounded exact transfer statement on the shared Sym^3-lifted invariant. "
            "It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane."
        ),
        non_claims=(
            "This object spec does not claim the lifted source and target invariants are already equivalent.",
            "This object spec does not claim the cubic Schur lift is uniquely preferred over every other nonlinear invariant family.",
            "This object spec does not justify retrying richer families on the already exhausted Sym^2 or normalized Plucker objects.",
        ),
        recommended_next_step=(
            "Hash the paired Sym^3-lifted object first, then test the low-order homogeneous and affine matrix recurrence ladders through the last overdetermined order."
        ),
    )


def render_sym3_eleven_window_object_spec() -> str:
    spec = build_sym3_eleven_window_object_spec()
    lines = [
        "# Phase 2 Sym^3-lifted eleven-window object spec",
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


def write_sym3_eleven_window_object_spec_report(
    output_path: str | Path = SYM3_ELEVEN_WINDOW_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym3_eleven_window_object_spec(), encoding="utf-8")
    return output


def write_sym3_eleven_window_object_spec_json(
    output_path: str | Path = SYM3_ELEVEN_WINDOW_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_sym3_eleven_window_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym3_eleven_window_object_spec_report()
    write_sym3_eleven_window_object_spec_json()


if __name__ == "__main__":
    main()
