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
from .symmetric_dual_baseline_transfer_object_spec import (
    SYMMETRIC_DUAL_BASELINE_TRANSFER_OBJECT_SPEC_REPORT_PATH,
    build_symmetric_dual_baseline_transfer_object_spec,
)
from .symmetric_dual_full_packet import build_symmetric_dual_full_packet

SYMMETRIC_DUAL_BASELINE_TRANSFER_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_dual_baseline_transfer_probe.md"
)
SYMMETRIC_DUAL_BASELINE_TRANSFER_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_dual_baseline_transfer_probe.json"
)


@dataclass(frozen=True)
class SymmetricDualBaselineTransferSample:
    n: int
    source_constant: str
    source_zeta3: str
    source_zeta5: str
    target_constant: str
    target_zeta3: str
    target_zeta5: str


@dataclass(frozen=True)
class SymmetricDualBaselineTransferProbe:
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
    samples: tuple[SymmetricDualBaselineTransferSample, ...]


def build_symmetric_dual_baseline_transfer_probe() -> SymmetricDualBaselineTransferProbe:
    spec = build_symmetric_dual_baseline_transfer_object_spec()
    source = build_symmetric_dual_full_packet(max_n=80)
    target_constant = get_cached_baseline_dual_f7_exact_component_terms(80, component="constant")
    target_zeta3 = get_cached_baseline_dual_f7_exact_component_terms(80, component="zeta3")
    target_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(80))

    source_payload = [
        {
            "n": n,
            "constant": fraction_to_canonical_string(c_value),
            "zeta3": fraction_to_canonical_string(z3_value),
            "zeta5": fraction_to_canonical_string(z5_value),
        }
        for n, (c_value, z3_value, z5_value) in enumerate(
            zip(source.constant_terms, source.zeta3_terms, source.zeta5_terms),
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
        for n, (c_value, z3_value, z5_value) in enumerate(zip(target_constant, target_zeta3, target_zeta5), start=1)
    ]
    source_packet_hash = compute_sequence_hash(
        provisional_signature={"kind": "symmetric_dual_transfer_source_packet", "terms": source_payload}
    )
    target_packet_hash = compute_sequence_hash(
        provisional_signature={"kind": "symmetric_dual_transfer_target_packet", "terms": target_payload}
    )
    transfer_object_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "symmetric_dual_baseline_transfer_object",
            "source_packet_hash": source_packet_hash,
            "target_packet_hash": target_packet_hash,
            "shared_window_start": 1,
            "shared_window_end": 80,
        }
    )
    samples = tuple(
        SymmetricDualBaselineTransferSample(
            n=n,
            source_constant=source_payload[n - 1]["constant"],
            source_zeta3=source_payload[n - 1]["zeta3"],
            source_zeta5=source_payload[n - 1]["zeta5"],
            target_constant=target_payload[n - 1]["constant"],
            target_zeta3=target_payload[n - 1]["zeta3"],
            target_zeta5=target_payload[n - 1]["zeta5"],
        )
        for n in range(1, 4)
    )
    return SymmetricDualBaselineTransferProbe(
        probe_id="bz_phase2_symmetric_dual_baseline_transfer_probe",
        source_spec_id=spec.spec_id,
        shared_window_start=1,
        shared_window_end=80,
        source_packet_hash=source_packet_hash,
        target_packet_hash=target_packet_hash,
        transfer_object_hash=transfer_object_hash,
        verdict="symmetric_dual_baseline_transfer_object_established",
        stabilized_findings=(
            "A paired exact dual-packet transfer object now exists on the shared window `n=1..80`.",
            "Source and target packets now share the same coefficient basis `(constant, zeta(3), zeta(5))` and the same exact extraction family.",
            "Source, target, and paired transfer objects are independently reproducible via exact hashes.",
        ),
        unresolved_findings=(
            "No transfer map has been certified.",
            "No symmetric dual packet identity has been imported into the baseline dual packet.",
            "No baseline P_n or baseline remainder pipeline has been extracted from this transfer object.",
        ),
        source_boundary=spec.source_boundary,
        recommendation="Run one bounded low-complexity packet-map ladder next: constant, difference, and lag-1 maps.",
        samples=samples,
    )


def render_symmetric_dual_baseline_transfer_probe() -> str:
    probe = build_symmetric_dual_baseline_transfer_probe()
    lines = [
        "# Phase 2 symmetric-dual to baseline-dual transfer probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source spec: `{SYMMETRIC_DUAL_BASELINE_TRANSFER_OBJECT_SPEC_REPORT_PATH}`",
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
            "| n | source constant | source zeta(3) | source zeta(5) | target constant | target zeta(3) | target zeta(5) |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{sample.source_constant}` | `{sample.source_zeta3}` | `{sample.source_zeta5}` | `{sample.target_constant}` | `{sample.target_zeta3}` | `{sample.target_zeta5}` |"
        )
    lines.extend(["", "## Recommendation", "", probe.recommendation, ""])
    return "\n".join(lines)


def write_symmetric_dual_baseline_transfer_probe_report(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_TRANSFER_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_dual_baseline_transfer_probe(), encoding="utf-8")
    return output


def write_symmetric_dual_baseline_transfer_probe_json(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_TRANSFER_PROBE_JSON_PATH,
) -> Path:
    probe = build_symmetric_dual_baseline_transfer_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_dual_baseline_transfer_probe_report()
    write_symmetric_dual_baseline_transfer_probe_json()


if __name__ == "__main__":
    main()
