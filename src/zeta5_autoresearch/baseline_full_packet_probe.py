from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .baseline_full_packet_object_spec import (
    BASELINE_FULL_PACKET_OBJECT_SPEC_REPORT_PATH,
    build_baseline_full_packet_object_spec,
)
from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string

BASELINE_FULL_PACKET_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_full_packet_probe.md"
)
BASELINE_FULL_PACKET_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_full_packet_probe.json"
)


@dataclass(frozen=True)
class BaselineFullPacketProbeSample:
    n: int
    constant: str
    zeta3: str
    zeta5: str


@dataclass(frozen=True)
class BaselineFullPacketProbe:
    probe_id: str
    source_spec_id: str
    shared_window_start: int
    shared_window_end: int
    packet_hash: str
    verdict: str
    stabilized_findings: tuple[str, ...]
    unresolved_findings: tuple[str, ...]
    bridge_boundary: str
    recommendation: str
    samples: tuple[BaselineFullPacketProbeSample, ...]


def build_baseline_full_packet_probe() -> BaselineFullPacketProbe:
    spec = build_baseline_full_packet_object_spec()
    constant_terms = get_cached_baseline_dual_f7_exact_component_terms(spec.components[0].max_verified_index, component="constant")
    zeta3_terms = get_cached_baseline_dual_f7_exact_component_terms(spec.components[1].max_verified_index, component="zeta3")
    zeta5_terms = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(spec.components[2].max_verified_index))
    shared_window_end = min(len(constant_terms), len(zeta3_terms), len(zeta5_terms))
    payload = [
        {
            "n": n,
            "constant": fraction_to_canonical_string(c),
            "zeta3": fraction_to_canonical_string(z3),
            "zeta5": fraction_to_canonical_string(z5),
        }
        for n, (c, z3, z5) in enumerate(
            zip(
                constant_terms[:shared_window_end],
                zeta3_terms[:shared_window_end],
                zeta5_terms[:shared_window_end],
            ),
            start=1,
        )
    ]
    packet_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "baseline_full_packet",
            "shared_window_start": 1,
            "shared_window_end": shared_window_end,
            "terms": payload,
        }
    )
    samples = tuple(
        BaselineFullPacketProbeSample(
            n=item["n"],
            constant=item["constant"],
            zeta3=item["zeta3"],
            zeta5=item["zeta5"],
        )
        for item in payload[:3]
    )
    return BaselineFullPacketProbe(
        probe_id="bz_phase2_baseline_full_packet_probe",
        source_spec_id=spec.spec_id,
        shared_window_start=1,
        shared_window_end=shared_window_end,
        packet_hash=packet_hash,
        verdict="baseline_full_packet_established",
        stabilized_findings=(
            "A baseline-native full coefficient packet now exists on the exact shared window `n=1..80`.",
            "The packet hash is reproducible and does not privilege any pairwise compression route a priori.",
            "All three exact channels are held active simultaneously at object-definition time.",
        ),
        unresolved_findings=(
            "No baseline `P_n` sequence has been extracted.",
            "No baseline remainder pipeline has been proved.",
            "No pairwise compression route has yet been selected or certified.",
        ),
        bridge_boundary=spec.bridge_boundary,
        recommendation=(
            "Run the bounded full-packet compression layer next, using the two prior hard-wall gates plus one new zeta(5)-residual route."
        ),
        samples=samples,
    )


def render_baseline_full_packet_probe() -> str:
    probe = build_baseline_full_packet_probe()
    lines = [
        "# Phase 2 baseline full-packet probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source spec: `{BASELINE_FULL_PACKET_OBJECT_SPEC_REPORT_PATH}`",
        f"- Source spec id: `{probe.source_spec_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Packet hash: `{probe.packet_hash}`",
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
            "## Bridge boundary",
            "",
            probe.bridge_boundary,
            "",
            "## Sample packet data",
            "",
            "| n | constant | zeta(3) | zeta(5) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{sample.constant}` | `{sample.zeta3}` | `{sample.zeta5}` |"
        )
    lines.extend(["", "## Recommendation", "", probe.recommendation, ""])
    return "\n".join(lines)


def write_baseline_full_packet_probe_report(
    output_path: str | Path = BASELINE_FULL_PACKET_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_full_packet_probe(), encoding="utf-8")
    return output


def write_baseline_full_packet_probe_json(
    output_path: str | Path = BASELINE_FULL_PACKET_PROBE_JSON_PATH,
) -> Path:
    probe = build_baseline_full_packet_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_full_packet_probe_report()
    write_baseline_full_packet_probe_json()


if __name__ == "__main__":
    main()
