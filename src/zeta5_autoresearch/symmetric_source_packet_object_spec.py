from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_full_packet_compression_decision_gate import (
    BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH,
)
from .config import CACHE_DIR, DATA_DIR
from .symmetric_linear_forms_packet import build_symmetric_linear_forms_exact_packet

SYMMETRIC_SOURCE_PACKET_OBJECT_SPEC_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_source_packet_object_spec.md"
)
SYMMETRIC_SOURCE_PACKET_OBJECT_SPEC_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_source_packet_object_spec.json"
)


@dataclass(frozen=True)
class SymmetricSourcePacketComponent:
    component_id: str
    role: str
    scale_label: str
    max_verified_index: int
    exact_status: str
    note: str


@dataclass(frozen=True)
class SymmetricSourcePacketObjectSpec:
    spec_id: str
    source_packet_id: str
    source_family: str
    object_label: str
    object_kind: str
    object_semantics: str
    rationale: str
    components: tuple[SymmetricSourcePacketComponent, ...]
    source_boundary: str
    non_claims: tuple[str, ...]
    recommended_next_step: str


def build_symmetric_source_packet_object_spec() -> SymmetricSourcePacketObjectSpec:
    packet = build_symmetric_linear_forms_exact_packet(max_n=80)
    return SymmetricSourcePacketObjectSpec(
        spec_id="bz_phase2_symmetric_source_packet_object_spec",
        source_packet_id=packet.packet_id,
        source_family="totally_symmetric_linear_form_pipeline",
        object_label="Totally symmetric scaled coefficient packet",
        object_kind="source_backed_scaled_exact_coefficient_packet",
        object_semantics=(
            "The active family-source object is the scaled totally symmetric coefficient triple "
            "`(d_n^5 Q_n, d_n^5 P_n, d_n^2 d_{2n} P̂_n)` on the shared exact window `n=1..80`. "
            "This keeps the published arithmetic scales explicit and treats the totally symmetric linear-form "
            "pipeline as a recurrence-explicit source family rather than as a baseline surrogate."
        ),
        rationale=(
            "The baseline dual packet has now exhausted low-complexity pairwise compression in all three orientations. "
            "The next honest source pivot is the repo's source-backed totally symmetric remainder / linear-form pipeline, "
            "because it is genuinely sequence-explicit and structurally different from the exhausted baseline packet."
        ),
        components=(
            SymmetricSourcePacketComponent(
                component_id="scaled_q",
                role="scaled zeta(5) leading coefficient channel",
                scale_label=packet.q_scale_label,
                max_verified_index=packet.shared_window_end,
                exact_status="exact",
                note="This is the scaled source-backed denominator-side channel from the published totally symmetric recurrence.",
            ),
            SymmetricSourcePacketComponent(
                component_id="scaled_p",
                role="scaled rational zeta(5) companion coefficient channel",
                scale_label=packet.p_scale_label,
                max_verified_index=packet.shared_window_end,
                exact_status="exact",
                note="This is the scaled source-backed rational coefficient paired with the linear form `Q_n zeta(5) - P_n`.",
            ),
            SymmetricSourcePacketComponent(
                component_id="scaled_phat",
                role="scaled zeta(2)-side companion coefficient channel",
                scale_label=packet.phat_scale_label,
                max_verified_index=packet.shared_window_end,
                exact_status="exact",
                note="This remains explicit to keep the totally symmetric linear-form decomposition honest at the coefficient level.",
            ),
        ),
        source_boundary=(
            "This source-backed packet is not the Brown-Zudilin baseline seed. It may guide family-source experiments and "
            "calibration, but it may not be silently transferred into a claimed baseline `P_n` or baseline remainder object."
        ),
        non_claims=(
            "This spec does not claim equivalence between the totally symmetric source family and the Brown-Zudilin baseline seed.",
            "This spec does not claim a baseline extraction.",
            "This spec does not privilege one pairwise compression route before exact testing inside the symmetric source family.",
        ),
        recommended_next_step=(
            "Hash and probe the scaled symmetric source packet first, then run one bounded pairwise compression layer across all three residual orientations."
        ),
    )


def render_symmetric_source_packet_object_spec() -> str:
    spec = build_symmetric_source_packet_object_spec()
    lines = [
        "# Phase 2 symmetric source packet object spec",
        "",
        f"- Spec id: `{spec.spec_id}`",
        f"- Prior hard-wall gate: `{BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH}`",
        f"- Source packet id: `{spec.source_packet_id}`",
        f"- Source family: `{spec.source_family}`",
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
        "| component | role | scale | max verified index | exact status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for component in spec.components:
        lines.append(
            f"| `{component.component_id}` | {component.role} | `{component.scale_label}` | `{component.max_verified_index}` | `{component.exact_status}` |"
        )
    lines.extend(["", "## Component notes", ""])
    for component in spec.components:
        lines.append(f"- `{component.component_id}`: {component.note}")
    lines.extend(["", "## Source boundary", "", spec.source_boundary, "", "## Non-claims", ""])
    for item in spec.non_claims:
        lines.append(f"- {item}")
    lines.extend(["", "## Recommended next step", "", spec.recommended_next_step, ""])
    return "\n".join(lines)


def write_symmetric_source_packet_object_spec_report(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_OBJECT_SPEC_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_source_packet_object_spec(), encoding="utf-8")
    return output


def write_symmetric_source_packet_object_spec_json(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_OBJECT_SPEC_JSON_PATH,
) -> Path:
    spec = build_symmetric_source_packet_object_spec()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(spec), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_source_packet_object_spec_report()
    write_symmetric_source_packet_object_spec_json()


if __name__ == "__main__":
    main()
