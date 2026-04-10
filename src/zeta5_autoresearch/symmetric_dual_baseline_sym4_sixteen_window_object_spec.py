from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR

SYM4_SIXTEEN_WINDOW_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym4_sixteen_window_object_spec.md"
)
SYM4_SIXTEEN_WINDOW_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym4_sixteen_window_object_spec.json"
)


@dataclass(frozen=True)
class Sym4SixteenWindowPacketRole:
    packet_id: str
    family: str
    object_kind: str
    shared_window_start: int
    shared_window_end: int
    note: str


@dataclass(frozen=True)
class Sym4SixteenWindowObjectSpec:
    spec_id: str
    object_label: str
    object_kind: str
    source_packet: Sym4SixteenWindowPacketRole
    target_packet: Sym4SixteenWindowPacketRole
    invariant_definition: str
    rationale: str
    source_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_sym4_sixteen_window_object_spec() -> Sym4SixteenWindowObjectSpec:
    return Sym4SixteenWindowObjectSpec(
        spec_id="bz_phase2_sym4_sixteen_window_object_spec",
        object_label="Sym^4-lifted sixteen-window normalized maximal-minor object",
        object_kind="paired_higher_schur_window_invariant",
        source_packet=Sym4SixteenWindowPacketRole(
            packet_id="bz_phase2_symmetric_dual_full_packet",
            family="totally_symmetric_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Exact symmetric dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.",
        ),
        target_packet=Sym4SixteenWindowPacketRole(
            packet_id="bz_phase2_baseline_full_packet",
            family="baseline_dual_f7_packet",
            object_kind="exact_full_coefficient_packet",
            shared_window_start=1,
            shared_window_end=80,
            note="Exact baseline dual full packet `(constant, zeta(3), zeta(5))` on `n=1..80`.",
        ),
        invariant_definition=(
            "Lift each packet vector `(x,y,z)` to its `Sym^4` image in dimension `15`, using the quartic monomial basis "
            "`(x^4, x^3y, x^3z, x^2y^2, x^2yz, x^2z^2, xy^3, xy^2z, xyz^2, xz^3, y^4, y^3z, y^2z^2, yz^3, z^4)`. "
            "For each sixteen-term lifted window, form the normalized maximal-minor coordinate vector in `Gr(15,16)` by "
            "dividing all `15x15` minors by the pivot minor of the first fifteen columns and omitting that pivot coordinate."
        ),
        rationale=(
            "The `Sym^3`-lifted eleven-window object is now banked. The strongest continuation inside the higher-Schur line is a quartic lift that still leaves a genuinely overdetermined homogeneous ladder through order `4` and an affine ladder through order `3`."
        ),
        source_boundary=(
            "A success on this object would still be a bounded exact transfer statement on the shared Sym^4-lifted invariant. "
            "It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane."
        ),
        non_claims=(
            "This object spec does not claim the lifted source and target invariants are already equivalent.",
            "This object spec does not claim the quartic Schur lift is final or optimal among higher nonlinear invariants.",
            "This object spec does not justify retrying exhausted low-order families on the earlier Sym^2 or Sym^3 objects.",
        ),
        recommended_next_step=(
            "Hash the paired Sym^4-lifted object first, then test the low-order homogeneous matrix ladder through order `4` and the affine ladder through order `3`."
        ),
    )


def render_sym4_sixteen_window_object_spec() -> str:
    spec = build_sym4_sixteen_window_object_spec()
    lines = [
        "# Phase 2 Sym^4-lifted sixteen-window object spec",
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


def write_sym4_sixteen_window_object_spec_report(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym4_sixteen_window_object_spec(), encoding="utf-8")
    return output


def write_sym4_sixteen_window_object_spec_json(
    output_path: str | Path = SYM4_SIXTEEN_WINDOW_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_sym4_sixteen_window_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym4_sixteen_window_object_spec_report()
    write_sym4_sixteen_window_object_spec_json()


if __name__ == "__main__":
    main()
