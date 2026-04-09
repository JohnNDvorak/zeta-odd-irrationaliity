from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_transfer_decision_gate import (
    SYMMETRIC_DUAL_BASELINE_TRANSFER_DECISION_GATE_REPORT_PATH,
)

SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_dual_baseline_annihilator_transfer_object_spec.md"
)
SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_dual_baseline_annihilator_transfer_object_spec.json"
)


@dataclass(frozen=True)
class SymmetricDualAnnihilatorProfileRole:
    object_id: str
    family: str
    object_kind: str
    shared_window_start: int
    shared_window_end: int
    note: str


@dataclass(frozen=True)
class SymmetricDualBaselineAnnihilatorTransferObjectSpec:
    spec_id: str
    object_label: str
    object_kind: str
    source_profile: SymmetricDualAnnihilatorProfileRole
    target_profile: SymmetricDualAnnihilatorProfileRole
    transfer_semantics: str
    rationale: str
    source_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_symmetric_dual_baseline_annihilator_transfer_object_spec(
    *,
    shared_window_end: int = 77,
) -> SymmetricDualBaselineAnnihilatorTransferObjectSpec:
    return SymmetricDualBaselineAnnihilatorTransferObjectSpec(
        spec_id="bz_phase2_symmetric_dual_baseline_annihilator_transfer_object_spec",
        object_label="Symmetric-dual to baseline-dual local annihilator transfer object",
        object_kind="paired_local_annihilator_profile_transfer_object",
        source_profile=SymmetricDualAnnihilatorProfileRole(
            object_id="bz_phase2_symmetric_dual_local_annihilator_profile",
            family="totally_symmetric_dual_f7_packet",
            object_kind="exact_local_annihilator_profile",
            shared_window_start=1,
            shared_window_end=shared_window_end,
            note=(
                "Local annihilator profile `(a_n, b_n, c_n)` induced by four consecutive "
                "symmetric dual packet vectors."
            ),
        ),
        target_profile=SymmetricDualAnnihilatorProfileRole(
            object_id="bz_phase2_baseline_dual_local_annihilator_profile",
            family="baseline_dual_f7_packet",
            object_kind="exact_local_annihilator_profile",
            shared_window_start=1,
            shared_window_end=shared_window_end,
            note=(
                "Local annihilator profile `(a_n, b_n, c_n)` induced by four consecutive "
                "baseline dual packet vectors."
            ),
        ),
        transfer_semantics=(
            "The active transfer object compares local annihilator profiles rather than packet coordinates. "
            "Each window encodes the exact recurrence geometry of four consecutive packet vectors, so the "
            "comparison is basis-free at the packet level and closer to recurrence structure."
        ),
        rationale=(
            "Packet, pair, projective, and determinant-level transfer objects all exhausted their low-complexity "
            "ladders. The next natural object class is the local annihilator profile because it tests whether the "
            "obstruction survives after passing from packet coordinates to induced recurrence-level data."
        ),
        source_boundary=(
            "A transfer success would still be a bounded profile-level relation on `n=1..77`. It would not by itself "
            "prove family equivalence, a baseline recurrence, or a baseline remainder pipeline."
        ),
        non_claims=(
            "This spec does not claim the two local annihilator profiles are already equivalent.",
            "This spec does not prove a common minimal recurrence for the two packet families.",
            "This spec does not justify skipping the bounded transfer family ladder on the profile object.",
        ),
        recommended_next_step=(
            "Hash the paired local annihilator profiles first, then test one bounded low-complexity profile-map ladder."
        ),
    )


def render_symmetric_dual_baseline_annihilator_transfer_object_spec() -> str:
    spec = build_symmetric_dual_baseline_annihilator_transfer_object_spec()
    lines = [
        "# Phase 2 symmetric-dual to baseline-dual annihilator transfer object spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Prior packet-transfer hard wall: `{SYMMETRIC_DUAL_BASELINE_TRANSFER_DECISION_GATE_REPORT_PATH}`",
        f"- Object label: `{spec.object_label}`",
        f"- Object kind: `{spec.object_kind}`",
        "",
        "## Source profile",
        "",
        f"- Object id: `{spec.source_profile.object_id}`",
        f"- Family: `{spec.source_profile.family}`",
        f"- Kind: `{spec.source_profile.object_kind}`",
        f"- Shared window: `n={spec.source_profile.shared_window_start}..{spec.source_profile.shared_window_end}`",
        f"- Note: {spec.source_profile.note}",
        "",
        "## Target profile",
        "",
        f"- Object id: `{spec.target_profile.object_id}`",
        f"- Family: `{spec.target_profile.family}`",
        f"- Kind: `{spec.target_profile.object_kind}`",
        f"- Shared window: `n={spec.target_profile.shared_window_start}..{spec.target_profile.shared_window_end}`",
        f"- Note: {spec.target_profile.note}",
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


def write_symmetric_dual_baseline_annihilator_transfer_object_spec_report(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_dual_baseline_annihilator_transfer_object_spec(), encoding="utf-8")
    return output


def write_symmetric_dual_baseline_annihilator_transfer_object_spec_json(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_symmetric_dual_baseline_annihilator_transfer_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_dual_baseline_annihilator_transfer_object_spec_report()
    write_symmetric_dual_baseline_annihilator_transfer_object_spec_json()


if __name__ == "__main__":
    main()
