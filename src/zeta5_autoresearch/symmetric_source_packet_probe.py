from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .bz_symmetric_linear_forms_probe import (
    DEFAULT_LINEAR_FORMS_REPORT_PATH,
    build_bz_totally_symmetric_linear_forms_probe,
)
from .config import CACHE_DIR, DATA_DIR
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string
from .symmetric_linear_forms_packet import build_symmetric_linear_forms_exact_packet
from .symmetric_source_packet_object_spec import (
    SYMMETRIC_SOURCE_PACKET_OBJECT_SPEC_REPORT_PATH,
    build_symmetric_source_packet_object_spec,
)

SYMMETRIC_SOURCE_PACKET_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_source_packet_probe.md"
)
SYMMETRIC_SOURCE_PACKET_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_source_packet_probe.json"
)


@dataclass(frozen=True)
class SymmetricSourcePacketProbeSample:
    n: int
    scaled_q: str
    scaled_p: str
    scaled_phat: str


@dataclass(frozen=True)
class SymmetricSourcePacketProbe:
    probe_id: str
    source_spec_id: str
    source_anchor_object_id: str
    shared_window_start: int
    shared_window_end: int
    packet_hash: str
    verdict: str
    stabilized_findings: tuple[str, ...]
    unresolved_findings: tuple[str, ...]
    source_boundary: str
    recommendation: str
    samples: tuple[SymmetricSourcePacketProbeSample, ...]


def build_symmetric_source_packet_probe() -> SymmetricSourcePacketProbe:
    spec = build_symmetric_source_packet_object_spec()
    packet = build_symmetric_linear_forms_exact_packet(max_n=80)
    anchor = build_bz_totally_symmetric_linear_forms_probe(max_n=14, precision=80)
    payload = [
        {
            "n": n,
            "scaled_q": fraction_to_canonical_string(q_value),
            "scaled_p": fraction_to_canonical_string(p_value),
            "scaled_phat": fraction_to_canonical_string(phat_value),
        }
        for n, (q_value, p_value, phat_value) in enumerate(
            zip(packet.scaled_q_terms, packet.scaled_p_terms, packet.scaled_phat_terms),
            start=packet.shared_window_start,
        )
    ]
    packet_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "symmetric_source_packet",
            "shared_window_start": packet.shared_window_start,
            "shared_window_end": packet.shared_window_end,
            "terms": payload,
        }
    )
    samples = tuple(
        SymmetricSourcePacketProbeSample(
            n=item["n"],
            scaled_q=item["scaled_q"],
            scaled_p=item["scaled_p"],
            scaled_phat=item["scaled_phat"],
        )
        for item in payload[:3]
    )
    return SymmetricSourcePacketProbe(
        probe_id="bz_phase2_symmetric_source_packet_probe",
        source_spec_id=spec.spec_id,
        source_anchor_object_id=anchor.decay_summary.object_id,
        shared_window_start=packet.shared_window_start,
        shared_window_end=packet.shared_window_end,
        packet_hash=packet_hash,
        verdict="symmetric_source_packet_established",
        stabilized_findings=(
            "A source-backed scaled symmetric coefficient packet now exists exactly on the shared window `n=1..80`.",
            "The packet inherits recurrence-explicit provenance from the published totally symmetric third-order recurrence.",
            "The packet hash is reproducible and keeps the published arithmetic scales explicit rather than collapsing to raw unscaled coefficients.",
        ),
        unresolved_findings=(
            "No baseline transfer has been established from this source family.",
            "No pairwise compression route has yet been selected or certified inside the symmetric source packet.",
            "No claim is made that the symmetric source packet solves the baseline decay problem directly.",
        ),
        source_boundary=spec.source_boundary,
        recommendation=(
            "Run one bounded pairwise compression layer across all three residual orientations of the scaled symmetric packet."
        ),
        samples=samples,
    )


def render_symmetric_source_packet_probe() -> str:
    probe = build_symmetric_source_packet_probe()
    lines = [
        "# Phase 2 symmetric source packet probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source spec: `{SYMMETRIC_SOURCE_PACKET_OBJECT_SPEC_REPORT_PATH}`",
        f"- Symmetric anchor report: `{DEFAULT_LINEAR_FORMS_REPORT_PATH}`",
        f"- Source spec id: `{probe.source_spec_id}`",
        f"- Source anchor object id: `{probe.source_anchor_object_id}`",
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
            "## Source boundary",
            "",
            probe.source_boundary,
            "",
            "## Sample packet data",
            "",
            "| n | scaled Q_n | scaled P_n | scaled Phat_n |",
            "| --- | --- | --- | --- |",
        ]
    )
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{sample.scaled_q}` | `{sample.scaled_p}` | `{sample.scaled_phat}` |"
        )
    lines.extend(["", "## Recommendation", "", probe.recommendation, ""])
    return "\n".join(lines)


def write_symmetric_source_packet_probe_report(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_source_packet_probe(), encoding="utf-8")
    return output


def write_symmetric_source_packet_probe_json(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_PROBE_JSON_PATH,
) -> Path:
    probe = build_symmetric_source_packet_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_source_packet_probe_report()
    write_symmetric_source_packet_probe_json()


if __name__ == "__main__":
    main()
