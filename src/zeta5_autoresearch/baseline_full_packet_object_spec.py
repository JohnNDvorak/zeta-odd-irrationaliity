from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_projection_target_spec import (
    DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH,
    build_phase2_dual_projection_target_spec,
)

BASELINE_FULL_PACKET_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_full_packet_object_spec.md"
)
BASELINE_FULL_PACKET_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_full_packet_object_spec.json"
)


@dataclass(frozen=True)
class BaselineFullPacketComponent:
    component_id: str
    role: str
    max_verified_index: int
    exact_status: str
    note: str


@dataclass(frozen=True)
class BaselineFullPacketObjectSpec:
    spec_id: str
    baseline_seed: str
    source_packet_id: str
    object_label: str
    object_kind: str
    object_semantics: str
    rationale: str
    components: tuple[BaselineFullPacketComponent, ...]
    bridge_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_baseline_full_packet_object_spec() -> BaselineFullPacketObjectSpec:
    target = build_phase2_dual_projection_target_spec()
    target_components = {component.component_id: component for component in target.components}
    return BaselineFullPacketObjectSpec(
        spec_id="bz_phase2_baseline_full_packet_object_spec",
        baseline_seed=target.baseline_seed,
        source_packet_id=target.target_id,
        object_label="Baseline full coefficient packet object",
        object_kind="baseline_side_exact_full_coefficient_packet",
        object_semantics=(
            "The active baseline-side object is the full exact coefficient packet `(constant, zeta(3), zeta(5))` "
            "on the shared exact window. No channel is demoted to residual at object-definition time."
        ),
        rationale=(
            "Both pair-object tranches hit hard walls. The next honest packet-level move is to keep the full coefficient "
            "packet active and treat pairwise compression as a bounded experiment rather than choosing a privileged pair up front."
        ),
        components=(
            BaselineFullPacketComponent(
                component_id="constant",
                role="exact rational constant channel retained in the active full packet",
                max_verified_index=target_components["constant"].max_verified_index,
                exact_status=target_components["constant"].exact_status,
                note="This remains exact far beyond the shared window and is kept active to avoid premature demotion.",
            ),
            BaselineFullPacketComponent(
                component_id="zeta3",
                role="exact zeta(3) channel retained in the active full packet",
                max_verified_index=target_components["zeta3"].max_verified_index,
                exact_status=target_components["zeta3"].exact_status,
                note="This remains exact far beyond the shared window and is kept active as part of the odd-weight content.",
            ),
            BaselineFullPacketComponent(
                component_id="zeta5",
                role="exact zeta(5) channel retained in the active full packet",
                max_verified_index=target_components["zeta5"].max_verified_index,
                exact_status=target_components["zeta5"].exact_status,
                note="This remains the shortest verified frontier and caps the shared exact window at n=1..80.",
            ),
        ),
        bridge_boundary=(
            "The Zudilin 2002 bridge stack remains calibration-only. It may not redefine the packet or choose a preferred compression route."
        ),
        non_claims=(
            "This spec does not claim that the full packet is already a baseline decay object.",
            "This spec does not claim any published baseline P_n or remainder sequence has been extracted.",
            "This spec does not privilege one pairwise compression route before exact testing.",
        ),
        recommended_next_step=(
            "Hash and probe the full packet first, then run one bounded pairwise compression layer across all three residual orientations."
        ),
    )


def render_baseline_full_packet_object_spec() -> str:
    spec = build_baseline_full_packet_object_spec()
    lines = [
        "# Phase 2 baseline full-packet object spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Baseline seed: `{spec.baseline_seed}`",
        f"- Source packet spec: `{DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH}`",
        f"- Source packet id: `{spec.source_packet_id}`",
        f"- Object label: `{spec.object_label}`",
        f"- Object kind: `{spec.object_kind}`",
        "",
        "## Object semantics",
        "",
        spec.object_semantics,
        "",
        "## Rationale",
        "",
        spec.rationale,
        "",
        "## Components",
        "",
        "| component | role | max verified index | exact status |",
        "| --- | --- | --- | --- |",
    ]
    for component in spec.components:
        lines.append(
            f"| `{component.component_id}` | {component.role} | `{component.max_verified_index}` | `{component.exact_status}` |"
        )
    lines.extend(["", "## Component notes", ""])
    for component in spec.components:
        lines.append(f"- `{component.component_id}`: {component.note}")
    lines.extend(["", "## Bridge boundary", "", spec.bridge_boundary, "", "## Non-claims", ""])
    for item in spec.non_claims:
        lines.append(f"- {item}")
    lines.extend(["", "## Recommended next step", "", spec.recommended_next_step, ""])
    return "\n".join(lines)


def write_baseline_full_packet_object_spec_report(
    output_path: str | Path = BASELINE_FULL_PACKET_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_full_packet_object_spec(), encoding="utf-8")
    return output


def write_baseline_full_packet_object_spec_json(
    output_path: str | Path = BASELINE_FULL_PACKET_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_baseline_full_packet_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_full_packet_object_spec_report()
    write_baseline_full_packet_object_spec_json()


if __name__ == "__main__":
    main()
