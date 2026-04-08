from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from .config import DATA_DIR
from .dual_f7_exact_coefficient_cache import (
    get_cached_baseline_dual_f7_exact_component_terms,
)
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .dual_projection_target_spec import (
    DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH,
    build_phase2_dual_projection_target_spec,
)
from .external_calibration_check import (
    EXTERNAL_CALIBRATION_REPORT_PATH,
    build_phase2_external_calibration_check,
)
from .gate2.sequence_identity import ProvisionalSequenceIdentity, compute_provisional_sequence_hash
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string

DUAL_PROJECTION_PROBE_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_dual_projection_probe.md"


@dataclass(frozen=True)
class ProjectionComponentProbe:
    component_id: str
    max_verified_index: int
    shared_window_end: int
    provisional_hash: str
    first_terms: tuple[str, ...]


@dataclass(frozen=True)
class DualProjectionProbe:
    probe_id: str
    target_id: str
    calibration_anchor_id: str
    shared_window_start: int
    shared_window_end: int
    packet_hash: str
    calibration_matches: tuple[str, ...]
    calibration_departures: tuple[str, ...]
    non_claims: tuple[str, ...]
    components: tuple[ProjectionComponentProbe, ...]
    recommendation: str


def build_phase2_dual_projection_probe() -> DualProjectionProbe:
    target = build_phase2_dual_projection_target_spec()
    calibration = build_phase2_external_calibration_check()

    constant_terms = get_cached_baseline_dual_f7_exact_component_terms(
        target.components[0].max_verified_index,
        component="constant",
    )
    zeta3_terms = get_cached_baseline_dual_f7_exact_component_terms(
        target.components[1].max_verified_index,
        component="zeta3",
    )
    zeta5_terms = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(target.components[2].max_verified_index))

    shared_window_end = min(len(constant_terms), len(zeta3_terms), len(zeta5_terms))
    if shared_window_end <= 0:
        raise ValueError("dual projection probe requires a non-empty shared exact window")

    component_payloads = []
    component_probes = []
    for component_id, terms, max_verified_index in (
        ("constant", constant_terms, len(constant_terms)),
        ("zeta3", zeta3_terms, len(zeta3_terms)),
        ("zeta5", zeta5_terms, len(zeta5_terms)),
    ):
        signature = terms[:shared_window_end]
        provisional = ProvisionalSequenceIdentity.from_scalars(
            start_index=1,
            order_bound=max(1, shared_window_end - 1),
            initial_data=signature[: min(2, len(signature))],
            signature=signature,
        )
        component_hash = compute_provisional_sequence_hash(provisional)
        component_payloads.append(
            {
                "component_id": component_id,
                "shared_window_start": 1,
                "shared_window_end": shared_window_end,
                "provisional_hash": component_hash,
            }
        )
        component_probes.append(
            ProjectionComponentProbe(
                component_id=component_id,
                max_verified_index=max_verified_index,
                shared_window_end=shared_window_end,
                provisional_hash=component_hash,
                first_terms=tuple(fraction_to_canonical_string(value) for value in signature[:3]),
            )
        )

    packet_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "dual_projection_packet",
            "target_id": target.target_id,
            "shared_window_start": 1,
            "shared_window_end": shared_window_end,
            "components": component_payloads,
        }
    )

    return DualProjectionProbe(
        probe_id="bz_phase2_dual_projection_probe_v1",
        target_id=target.target_id,
        calibration_anchor_id=calibration.chosen_anchor_id,
        shared_window_start=1,
        shared_window_end=shared_window_end,
        packet_hash=packet_hash,
        calibration_matches=(
            "Coefficient-level normalization remains explicit: the probe keeps separate component hashes instead of collapsing to one scalar remainder.",
            "Companion channels remain explicit: constant, zeta(3), and zeta(5) are all named components in the packet.",
            "Sequence-level reproducibility is preserved: each component is hashed on an exact shared window and tied to a concrete cache frontier.",
        ),
        calibration_departures=(
            "The calibration anchor is a published q_n ζ(5) - p_n linear form, whereas this probe only prepares a pre-projection coefficient packet.",
            "The baseline packet currently has asymmetric component coverage because the zeta(5) exact cache only reaches n=80 while constant and zeta(3) reach n=434.",
            "No projection rule is asserted yet; this probe only freezes the exact packet that a later projection step may consume.",
        ),
        non_claims=target.non_claims,
        components=tuple(component_probes),
        recommendation=(
            "Use this shared-window exact packet as the input to the first actual projection rule experiment. "
            "Any next probe must report what linear combination or filter is applied to this packet and must keep "
            "the departure from the Zudilin 2002 calibration anchor explicit."
        ),
    )


def render_phase2_dual_projection_probe() -> str:
    probe = build_phase2_dual_projection_probe()
    lines = [
        "# Phase 2 dual projection probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Target spec: `{DUAL_PROJECTION_TARGET_SPEC_REPORT_PATH}`",
        f"- Calibration check: `{EXTERNAL_CALIBRATION_REPORT_PATH}`",
        f"- Target id: `{probe.target_id}`",
        f"- Calibration anchor id: `{probe.calibration_anchor_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Projection-ready packet hash: `{probe.packet_hash}`",
        "",
        "## Calibration matches",
        "",
    ]
    for item in probe.calibration_matches:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Calibration departures",
            "",
        ]
    )
    for item in probe.calibration_departures:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Non-claims",
            "",
        ]
    )
    for item in probe.non_claims:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Components",
            "",
            "| component | max verified index | shared window end | provisional hash | first terms |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for component in probe.components:
        first_terms = ", ".join(component.first_terms)
        lines.append(
            f"| `{component.component_id}` | `{component.max_verified_index}` | `{component.shared_window_end}` | "
            f"`{component.provisional_hash}` | `{first_terms}` |"
        )
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            probe.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_dual_projection_probe_report(
    output_path: str | Path = DUAL_PROJECTION_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_dual_projection_probe(), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_dual_projection_probe_report()


if __name__ == "__main__":
    main()
