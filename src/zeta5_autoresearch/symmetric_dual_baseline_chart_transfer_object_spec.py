from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .symmetric_dual_baseline_annihilator_transfer_decision_gate import (
    SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_DECISION_GATE_REPORT_PATH,
)

SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_dual_baseline_chart_transfer_object_spec.md"
)
SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_dual_baseline_chart_transfer_object_spec.json"
)


@dataclass(frozen=True)
class SymmetricDualChartProfileRole:
    object_id: str
    family: str
    object_kind: str
    shared_window_start: int
    shared_window_end: int
    note: str


@dataclass(frozen=True)
class SymmetricDualBaselineChartTransferObjectSpec:
    spec_id: str
    object_label: str
    object_kind: str
    source_profile: SymmetricDualChartProfileRole
    target_profile: SymmetricDualChartProfileRole
    transfer_semantics: str
    rationale: str
    source_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_symmetric_dual_baseline_chart_transfer_object_spec(
    *,
    shared_window_end: int = 76,
) -> SymmetricDualBaselineChartTransferObjectSpec:
    return SymmetricDualBaselineChartTransferObjectSpec(
        spec_id="bz_phase2_symmetric_dual_baseline_chart_transfer_object_spec",
        object_label="Symmetric-dual to baseline-dual chart-profile transfer object",
        object_kind="paired_window_chart_profile_transfer_object",
        source_profile=SymmetricDualChartProfileRole(
            object_id="bz_phase2_symmetric_dual_window_chart_profile",
            family="totally_symmetric_dual_f7_packet",
            object_kind="exact_window_chart_profile",
            shared_window_start=1,
            shared_window_end=shared_window_end,
            note=(
                "Five-term window chart profile that expresses columns 4 and 5 in the local chart "
                "determined by columns 1, 2, and 3 of each symmetric dual packet window."
            ),
        ),
        target_profile=SymmetricDualChartProfileRole(
            object_id="bz_phase2_baseline_dual_window_chart_profile",
            family="baseline_dual_f7_packet",
            object_kind="exact_window_chart_profile",
            shared_window_start=1,
            shared_window_end=shared_window_end,
            note=(
                "Five-term window chart profile that expresses columns 4 and 5 in the local chart "
                "determined by columns 1, 2, and 3 of each baseline dual packet window."
            ),
        ),
        transfer_semantics=(
            "The active transfer object compares five-term window chart profiles. This is a richer subspace-level "
            "object than the 1D local annihilator profile: each window is represented by a 6-dimensional exact chart "
            "coordinate vector describing the induced 3-plane inside the five-column window."
        ),
        rationale=(
            "Packet, projective, determinant, and local-annihilator transfer objects all exhausted their low-complexity "
            "ladders. The five-term chart profile is the next natural object class because it keeps exact windowed "
            "subspace geometry while remaining tractable enough for bounded exact family tests."
        ),
        source_boundary=(
            "A transfer success would still be a bounded chart-profile relation on `n=1..76`. It would not by itself "
            "prove packet equivalence, a common recurrence, or a baseline remainder pipeline."
        ),
        non_claims=(
            "This spec does not claim the two chart profiles are already equivalent.",
            "This spec does not prove a common recurrence for the symmetric and baseline dual packets.",
            "This spec does not justify importing symmetric identities into the baseline family.",
        ),
        recommended_next_step=(
            "Hash the paired chart profiles first, then test one bounded family ladder on the chart object."
        ),
    )


def render_symmetric_dual_baseline_chart_transfer_object_spec() -> str:
    spec = build_symmetric_dual_baseline_chart_transfer_object_spec()
    lines = [
        "# Phase 2 symmetric-dual to baseline-dual chart transfer object spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Prior annihilator hard wall: `{SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_DECISION_GATE_REPORT_PATH}`",
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


def write_symmetric_dual_baseline_chart_transfer_object_spec_report(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_dual_baseline_chart_transfer_object_spec(), encoding="utf-8")
    return output


def write_symmetric_dual_baseline_chart_transfer_object_spec_json(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_symmetric_dual_baseline_chart_transfer_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_dual_baseline_chart_transfer_object_spec_report()
    write_symmetric_dual_baseline_chart_transfer_object_spec_json()


if __name__ == "__main__":
    main()
