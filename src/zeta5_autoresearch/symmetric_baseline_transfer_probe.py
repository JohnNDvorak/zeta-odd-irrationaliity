from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string
from .symmetric_baseline_transfer_object_spec import (
    SYMMETRIC_BASELINE_TRANSFER_OBJECT_SPEC_REPORT_PATH,
    build_symmetric_baseline_transfer_object_spec,
)
from .symmetric_linear_forms_packet import build_symmetric_linear_forms_exact_packet

SYMMETRIC_BASELINE_TRANSFER_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_baseline_transfer_probe.md"
)
SYMMETRIC_BASELINE_TRANSFER_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_baseline_transfer_probe.json"
)


@dataclass(frozen=True)
class SymmetricBaselineTransferSample:
    n: int
    source_q: str
    source_p: str
    source_phat: str
    target_constant: str
    target_zeta3: str
    target_zeta5: str


@dataclass(frozen=True)
class SymmetricBaselineTransferProbe:
    probe_id: str
    source_spec_id: str
    shared_window_start: int
    shared_window_end: int
    source_packet_hash: str
    target_packet_hash: str
    transfer_object_hash: str
    verdict: str
    stabilized_findings: tuple[str, ...]
    unresolved_findings: tuple[str, ...]
    source_boundary: str
    recommendation: str
    samples: tuple[SymmetricBaselineTransferSample, ...]


def build_symmetric_baseline_transfer_probe() -> SymmetricBaselineTransferProbe:
    spec = build_symmetric_baseline_transfer_object_spec()
    source = build_symmetric_linear_forms_exact_packet(max_n=80)
    constant_terms = get_cached_baseline_dual_f7_exact_component_terms(80, component="constant")
    zeta3_terms = get_cached_baseline_dual_f7_exact_component_terms(80, component="zeta3")
    zeta5_terms = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(80))

    source_payload = [
        {
            "n": n,
            "scaled_q": fraction_to_canonical_string(q_value),
            "scaled_p": fraction_to_canonical_string(p_value),
            "scaled_phat": fraction_to_canonical_string(phat_value),
        }
        for n, (q_value, p_value, phat_value) in enumerate(
            zip(source.scaled_q_terms, source.scaled_p_terms, source.scaled_phat_terms),
            start=1,
        )
    ]
    target_payload = [
        {
            "n": n,
            "constant": fraction_to_canonical_string(c_value),
            "zeta3": fraction_to_canonical_string(z3_value),
            "zeta5": fraction_to_canonical_string(z5_value),
        }
        for n, (c_value, z3_value, z5_value) in enumerate(zip(constant_terms, zeta3_terms, zeta5_terms), start=1)
    ]
    source_packet_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "symmetric_transfer_source_packet",
            "terms": source_payload,
        }
    )
    target_packet_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "symmetric_transfer_target_packet",
            "terms": target_payload,
        }
    )
    transfer_object_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "symmetric_baseline_transfer_object",
            "source_packet_hash": source_packet_hash,
            "target_packet_hash": target_packet_hash,
            "shared_window_start": 1,
            "shared_window_end": 80,
        }
    )
    samples = tuple(
        SymmetricBaselineTransferSample(
            n=n,
            source_q=source_payload[n - 1]["scaled_q"],
            source_p=source_payload[n - 1]["scaled_p"],
            source_phat=source_payload[n - 1]["scaled_phat"],
            target_constant=target_payload[n - 1]["constant"],
            target_zeta3=target_payload[n - 1]["zeta3"],
            target_zeta5=target_payload[n - 1]["zeta5"],
        )
        for n in range(1, 4)
    )
    return SymmetricBaselineTransferProbe(
        probe_id="bz_phase2_symmetric_baseline_transfer_probe",
        source_spec_id=spec.spec_id,
        shared_window_start=1,
        shared_window_end=80,
        source_packet_hash=source_packet_hash,
        target_packet_hash=target_packet_hash,
        transfer_object_hash=transfer_object_hash,
        verdict="symmetric_baseline_transfer_object_established",
        stabilized_findings=(
            "A paired source/target exact transfer object now exists on the shared window `n=1..80`.",
            "The source side is recurrence-explicit and source-backed; the target side is the exact baseline dual full packet.",
            "Both packets and the paired transfer object are independently reproducible via exact hashes.",
        ),
        unresolved_findings=(
            "No transfer map has been certified.",
            "No baseline recurrence has been imported from the source family.",
            "No baseline P_n or baseline remainder pipeline has been extracted from the transfer object.",
        ),
        source_boundary=spec.source_boundary,
        recommendation=(
            "Run one bounded packet-level transfer family ladder next: constant map, difference map, and lag-1 map."
        ),
        samples=samples,
    )


def render_symmetric_baseline_transfer_probe() -> str:
    probe = build_symmetric_baseline_transfer_probe()
    lines = [
        "# Phase 2 symmetric-to-baseline transfer probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source spec: `{SYMMETRIC_BASELINE_TRANSFER_OBJECT_SPEC_REPORT_PATH}`",
        f"- Source spec id: `{probe.source_spec_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Source packet hash: `{probe.source_packet_hash}`",
        f"- Target packet hash: `{probe.target_packet_hash}`",
        f"- Transfer object hash: `{probe.transfer_object_hash}`",
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
            "## Sample paired packet data",
            "",
            "| n | source scaled Q | source scaled P | source scaled Phat | target constant | target zeta(3) | target zeta(5) |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{sample.source_q}` | `{sample.source_p}` | `{sample.source_phat}` | `{sample.target_constant}` | `{sample.target_zeta3}` | `{sample.target_zeta5}` |"
        )
    lines.extend(["", "## Recommendation", "", probe.recommendation, ""])
    return "\n".join(lines)


def write_symmetric_baseline_transfer_probe_report(
    output_path: str | Path = SYMMETRIC_BASELINE_TRANSFER_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_baseline_transfer_probe(), encoding="utf-8")
    return output


def write_symmetric_baseline_transfer_probe_json(
    output_path: str | Path = SYMMETRIC_BASELINE_TRANSFER_PROBE_JSON_PATH,
) -> Path:
    probe = build_symmetric_baseline_transfer_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_baseline_transfer_probe_report()
    write_symmetric_baseline_transfer_probe_json()


if __name__ == "__main__":
    main()
