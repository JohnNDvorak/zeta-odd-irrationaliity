from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .dual_packet_window_chart_profile import build_window_chart_profiles
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string
from .symmetric_dual_baseline_chart_transfer_object_spec import (
    SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_OBJECT_SPEC_REPORT_PATH,
    build_symmetric_dual_baseline_chart_transfer_object_spec,
)
from .symmetric_dual_full_packet import build_symmetric_dual_full_packet

SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_dual_baseline_chart_transfer_probe.md"
)
SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_dual_baseline_chart_transfer_probe.json"
)


@dataclass(frozen=True)
class SymmetricDualBaselineChartTransferSample:
    n: int
    source_u4: tuple[str, str, str]
    source_u5: tuple[str, str, str]
    target_u4: tuple[str, str, str]
    target_u5: tuple[str, str, str]


@dataclass(frozen=True)
class SymmetricDualBaselineChartTransferProbe:
    probe_id: str
    source_spec_id: str
    shared_window_start: int
    shared_window_end: int
    source_profile_hash: str
    target_profile_hash: str
    transfer_object_hash: str
    verdict: str
    stabilized_findings: tuple[str, ...]
    unresolved_findings: tuple[str, ...]
    source_boundary: str
    recommendation: str
    samples: tuple[SymmetricDualBaselineChartTransferSample, ...]


def build_symmetric_dual_baseline_chart_transfer_probe() -> SymmetricDualBaselineChartTransferProbe:
    spec = build_symmetric_dual_baseline_chart_transfer_object_spec()
    source = build_symmetric_dual_full_packet(max_n=80)
    target_constant = get_cached_baseline_dual_f7_exact_component_terms(80, component="constant")
    target_zeta3 = get_cached_baseline_dual_f7_exact_component_terms(80, component="zeta3")
    target_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(80))

    source_vectors = tuple(
        (source.constant_terms[i], source.zeta3_terms[i], source.zeta5_terms[i])
        for i in range(80)
    )
    target_vectors = tuple((target_constant[i], target_zeta3[i], target_zeta5[i]) for i in range(80))
    source_profiles = build_window_chart_profiles(source_vectors)
    target_profiles = build_window_chart_profiles(target_vectors)

    source_payload = [
        {
            "n": n,
            "u4": [fraction_to_canonical_string(value) for value in profile[:3]],
            "u5": [fraction_to_canonical_string(value) for value in profile[3:]],
        }
        for n, profile in enumerate(source_profiles, start=1)
    ]
    target_payload = [
        {
            "n": n,
            "u4": [fraction_to_canonical_string(value) for value in profile[:3]],
            "u5": [fraction_to_canonical_string(value) for value in profile[3:]],
        }
        for n, profile in enumerate(target_profiles, start=1)
    ]
    source_profile_hash = compute_sequence_hash(
        provisional_signature={"kind": "symmetric_dual_window_chart_profile", "terms": source_payload}
    )
    target_profile_hash = compute_sequence_hash(
        provisional_signature={"kind": "baseline_dual_window_chart_profile", "terms": target_payload}
    )
    transfer_object_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "symmetric_dual_baseline_chart_transfer_object",
            "source_profile_hash": source_profile_hash,
            "target_profile_hash": target_profile_hash,
            "shared_window_start": 1,
            "shared_window_end": 76,
        }
    )
    samples = tuple(
        SymmetricDualBaselineChartTransferSample(
            n=n,
            source_u4=tuple(source_payload[n - 1]["u4"]),  # type: ignore[arg-type]
            source_u5=tuple(source_payload[n - 1]["u5"]),  # type: ignore[arg-type]
            target_u4=tuple(target_payload[n - 1]["u4"]),  # type: ignore[arg-type]
            target_u5=tuple(target_payload[n - 1]["u5"]),  # type: ignore[arg-type]
        )
        for n in range(1, 4)
    )
    return SymmetricDualBaselineChartTransferProbe(
        probe_id="bz_phase2_symmetric_dual_baseline_chart_transfer_probe",
        source_spec_id=spec.spec_id,
        shared_window_start=1,
        shared_window_end=76,
        source_profile_hash=source_profile_hash,
        target_profile_hash=target_profile_hash,
        transfer_object_hash=transfer_object_hash,
        verdict="symmetric_dual_baseline_chart_transfer_object_established",
        stabilized_findings=(
            "A paired exact chart-profile transfer object now exists on the shared window `n=1..76`.",
            "Source and target are compared through six-dimensional exact chart coordinates on five-term packet windows.",
            "Source, target, and paired chart-transfer objects are independently reproducible via exact hashes.",
        ),
        unresolved_findings=(
            "No chart-profile transfer family has been certified.",
            "No common recurrence has been proved for the symmetric and baseline dual packets.",
            "No baseline P_n or baseline remainder pipeline has been extracted from this chart object.",
        ),
        source_boundary=spec.source_boundary,
        recommendation=(
            "Run the bounded chart-family ladder next: constant, difference, support-1, support-2, support-3, and support-4."
        ),
        samples=samples,
    )


def render_symmetric_dual_baseline_chart_transfer_probe() -> str:
    probe = build_symmetric_dual_baseline_chart_transfer_probe()
    lines = [
        "# Phase 2 symmetric-dual to baseline-dual chart transfer probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source spec: `{SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_OBJECT_SPEC_REPORT_PATH}`",
        f"- Source spec id: `{probe.source_spec_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Source profile hash: `{probe.source_profile_hash}`",
        f"- Target profile hash: `{probe.target_profile_hash}`",
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
            "## Sample paired chart data",
            "",
            "| n | source u4 | source u5 | target u4 | target u5 |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for sample in probe.samples:
        lines.append(
            f"| `{sample.n}` | `{', '.join(sample.source_u4)}` | `{', '.join(sample.source_u5)}` | `{', '.join(sample.target_u4)}` | `{', '.join(sample.target_u5)}` |"
        )
    lines.extend(["", "## Recommendation", "", probe.recommendation, ""])
    return "\n".join(lines)


def write_symmetric_dual_baseline_chart_transfer_probe_report(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_dual_baseline_chart_transfer_probe(), encoding="utf-8")
    return output


def write_symmetric_dual_baseline_chart_transfer_probe_json(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_PROBE_JSON_PATH,
) -> Path:
    probe = build_symmetric_dual_baseline_chart_transfer_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_symmetric_dual_baseline_chart_transfer_probe_report()
    write_symmetric_dual_baseline_chart_transfer_probe_json()


if __name__ == "__main__":
    main()
