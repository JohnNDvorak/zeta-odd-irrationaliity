from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .dual_packet_schur_functor import build_sym3_lifted_packet_vectors
from .dual_packet_window_plucker import build_normalized_window_maximal_minor_vectors
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string
from .symmetric_dual_baseline_sym3_eleven_window_object_spec import (
    SYM3_ELEVEN_WINDOW_OBJECT_SPEC_REPORT_PATH,
    build_sym3_eleven_window_object_spec,
)
from .symmetric_dual_full_packet import build_symmetric_dual_full_packet

SYM3_ELEVEN_WINDOW_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_sym3_eleven_window_probe.md"
)
SYM3_ELEVEN_WINDOW_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_sym3_eleven_window_probe.json"
)


Sym3ElevenWindowVector = tuple[Fraction, ...]


@dataclass(frozen=True)
class Sym3ElevenWindowSample:
    n: int
    source_values: tuple[str, ...]
    target_values: tuple[str, ...]


@dataclass(frozen=True)
class Sym3ElevenWindowProbe:
    probe_id: str
    source_spec_id: str
    shared_window_start: int
    shared_window_end: int
    coordinate_count: int
    source_invariant_hash: str
    target_invariant_hash: str
    paired_object_hash: str
    verdict: str
    stabilized_findings: tuple[str, ...]
    unresolved_findings: tuple[str, ...]
    source_boundary: str
    recommendation: str
    samples: tuple[Sym3ElevenWindowSample, ...]


@lru_cache(maxsize=1)
def build_sym3_eleven_window_sequences() -> tuple[tuple[Sym3ElevenWindowVector, ...], tuple[Sym3ElevenWindowVector, ...]]:
    source_packet = build_symmetric_dual_full_packet(max_n=80)
    source_vectors = tuple(
        (source_packet.constant_terms[i], source_packet.zeta3_terms[i], source_packet.zeta5_terms[i])
        for i in range(80)
    )
    target_constant = get_cached_baseline_dual_f7_exact_component_terms(80, component="constant")
    target_zeta3 = get_cached_baseline_dual_f7_exact_component_terms(80, component="zeta3")
    target_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(80))
    target_vectors = tuple((target_constant[i], target_zeta3[i], target_zeta5[i]) for i in range(80))

    source_lifted = build_sym3_lifted_packet_vectors(source_vectors)
    target_lifted = build_sym3_lifted_packet_vectors(target_vectors)
    source = build_normalized_window_maximal_minor_vectors(source_lifted, window_size=11)
    target = build_normalized_window_maximal_minor_vectors(target_lifted, window_size=11)
    return source, target


def _payload(values: tuple[Sym3ElevenWindowVector, ...]) -> list[dict[str, object]]:
    return [
        {"n": n, "values": [fraction_to_canonical_string(value) for value in vector]}
        for n, vector in enumerate(values, start=1)
    ]


@lru_cache(maxsize=1)
def build_sym3_eleven_window_probe() -> Sym3ElevenWindowProbe:
    spec = build_sym3_eleven_window_object_spec()
    source, target = build_sym3_eleven_window_sequences()
    source_payload = _payload(source)
    target_payload = _payload(target)
    source_hash = compute_sequence_hash(
        provisional_signature={"kind": "sym3_eleven_window_source", "terms": source_payload}
    )
    target_hash = compute_sequence_hash(
        provisional_signature={"kind": "sym3_eleven_window_target", "terms": target_payload}
    )
    paired_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "sym3_eleven_window_transfer_object",
            "source_hash": source_hash,
            "target_hash": target_hash,
            "coordinate_count": len(source[0]),
            "shared_window_start": 1,
            "shared_window_end": len(source),
        }
    )
    samples = tuple(
        Sym3ElevenWindowSample(
            n=n,
            source_values=tuple(source_payload[n - 1]["values"][:4]),  # type: ignore[index]
            target_values=tuple(target_payload[n - 1]["values"][:4]),  # type: ignore[index]
        )
        for n in range(1, 3)
    )
    return Sym3ElevenWindowProbe(
        probe_id="bz_phase2_sym3_eleven_window_probe",
        source_spec_id=spec.spec_id,
        shared_window_start=1,
        shared_window_end=len(source),
        coordinate_count=len(source[0]),
        source_invariant_hash=source_hash,
        target_invariant_hash=target_hash,
        paired_object_hash=paired_hash,
        verdict="sym3_eleven_window_object_established",
        stabilized_findings=(
            "The symmetric-dual and baseline-dual Sym^3-lifted eleven-window invariants are now repo-native exact objects.",
            "The Sym^3-lifted eleven-window invariant has coordinate count `10` on the shared exact window `n=1..70`.",
            "Source, target, and paired nonlinear objects are independently reproducible via exact hashes.",
        ),
        unresolved_findings=(
            "No recurrence-level transfer family has yet been certified on this Sym^3-lifted eleven-window object.",
            "No implication for baseline `P_n` extraction follows directly from this object alone.",
            "No claim is made that the cubic Schur lift dominates every other higher nonlinear invariant family.",
        ),
        source_boundary=spec.source_boundary,
        recommendation=(
            "Run the low-order homogeneous and affine matrix recurrence ladders through the last overdetermined order on source and target separately."
        ),
        samples=samples,
    )


def render_sym3_eleven_window_probe() -> str:
    probe = build_sym3_eleven_window_probe()
    lines = [
        "# Phase 2 Sym^3-lifted eleven-window probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source spec: `{SYM3_ELEVEN_WINDOW_OBJECT_SPEC_REPORT_PATH}`",
        f"- Source spec id: `{probe.source_spec_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Coordinate count: `{probe.coordinate_count}`",
        f"- Source invariant hash: `{probe.source_invariant_hash}`",
        f"- Target invariant hash: `{probe.target_invariant_hash}`",
        f"- Paired object hash: `{probe.paired_object_hash}`",
        f"- Verdict: `{probe.verdict}`",
        "",
        "## Stabilized findings",
        "",
    ]
    for item in probe.stabilized_findings:
        lines.append(f"- {item}")
    lines.extend(["", "## Unresolved findings", ""])
    for item in probe.unresolved_findings:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Sample normalized coordinates",
            "",
            "| n | source first four coords | target first four coords |",
            "| --- | --- | --- |",
        ]
    )
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{', '.join(sample.source_values)}` | `{', '.join(sample.target_values)}` |"
        )
    lines.extend(["", "## Source boundary", "", probe.source_boundary, "", "## Recommendation", "", probe.recommendation, ""])
    return "\n".join(lines)


def write_sym3_eleven_window_probe_report(
    output_path: str | Path = SYM3_ELEVEN_WINDOW_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_sym3_eleven_window_probe(), encoding="utf-8")
    return output


def write_sym3_eleven_window_probe_json(
    output_path: str | Path = SYM3_ELEVEN_WINDOW_PROBE_JSON_PATH,
) -> Path:
    probe = build_sym3_eleven_window_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_sym3_eleven_window_probe_report()
    write_sym3_eleven_window_probe_json()


if __name__ == "__main__":
    main()
