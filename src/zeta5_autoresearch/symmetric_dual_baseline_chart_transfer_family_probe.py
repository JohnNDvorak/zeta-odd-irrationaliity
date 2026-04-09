from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .dual_packet_local_annihilator_profile import solve_exact_linear_system
from .dual_packet_window_chart_profile import build_window_chart_profiles
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string
from .symmetric_dual_baseline_chart_transfer_post_probe_decision_gate import (
    SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_POST_PROBE_DECISION_GATE_REPORT_PATH,
    build_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate,
)
from .symmetric_dual_full_packet import build_symmetric_dual_full_packet

SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_FAMILY_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_dual_baseline_chart_transfer_family_probe.md"
)
SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_FAMILY_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_dual_baseline_chart_transfer_family_probe.json"
)


@dataclass(frozen=True)
class SymmetricDualBaselineChartTransferFamilyResult:
    family_id: str
    fit_window_start: int
    fit_window_end: int
    validation_window_start: int
    validation_window_end: int
    coefficients: tuple[str, ...]
    transformed_residual_hash: str
    verdict: str
    zero_count: int
    first_mismatch_index: int | None


@dataclass(frozen=True)
class SymmetricDualBaselineChartTransferFamilyProbe:
    probe_id: str
    source_gate_id: str
    shared_window_start: int
    shared_window_end: int
    overall_verdict: str
    family_results: tuple[SymmetricDualBaselineChartTransferFamilyResult, ...]
    source_boundary: str
    recommendation: str


def build_symmetric_dual_baseline_chart_transfer_family_probe() -> SymmetricDualBaselineChartTransferFamilyProbe:
    gate = build_symmetric_dual_baseline_chart_transfer_post_probe_decision_gate()
    source_packet = build_symmetric_dual_full_packet(max_n=80)
    source_vectors = tuple(
        (source_packet.constant_terms[i], source_packet.zeta3_terms[i], source_packet.zeta5_terms[i])
        for i in range(80)
    )
    target_constant = get_cached_baseline_dual_f7_exact_component_terms(80, component="constant")
    target_zeta3 = get_cached_baseline_dual_f7_exact_component_terms(80, component="zeta3")
    target_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(80))
    target_vectors = tuple((target_constant[i], target_zeta3[i], target_zeta5[i]) for i in range(80))

    source_profiles = build_window_chart_profiles(source_vectors)
    target_profiles = build_window_chart_profiles(target_vectors)
    family_results = (
        _evaluate_constant_map(source_profiles=source_profiles, target_profiles=target_profiles),
        _evaluate_difference_map(source_profiles=source_profiles, target_profiles=target_profiles),
        _evaluate_support_map(source_profiles=source_profiles, target_profiles=target_profiles, support_depth=1),
        _evaluate_support_map(source_profiles=source_profiles, target_profiles=target_profiles, support_depth=2),
        _evaluate_support_map(source_profiles=source_profiles, target_profiles=target_profiles, support_depth=3),
        _evaluate_support_map(source_profiles=source_profiles, target_profiles=target_profiles, support_depth=4),
    )
    winner_exists = any(item.verdict == "holds_on_full_window" for item in family_results)
    return SymmetricDualBaselineChartTransferFamilyProbe(
        probe_id="bz_phase2_symmetric_dual_baseline_chart_transfer_family_probe",
        source_gate_id=gate.gate_id,
        shared_window_start=1,
        shared_window_end=76,
        overall_verdict=(
            "bounded_chart_transfer_has_winner"
            if winner_exists
            else "bounded_chart_transfer_interpolation_only"
        ),
        family_results=family_results,
        source_boundary=(
            "A chart-profile transfer success would still be a bounded relation on `n=1..76`, not a proof of common recurrence or packet equivalence."
        ),
        recommendation=(
            "Promote the winning chart family into a v2 transfer artifact."
            if winner_exists
            else "Stop if the richer support ladder shows interpolation-only behavior."
        ),
    )


def render_symmetric_dual_baseline_chart_transfer_family_probe() -> str:
    probe = build_symmetric_dual_baseline_chart_transfer_family_probe()
    lines = [
        "# Phase 2 symmetric-dual to baseline-dual chart transfer family probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source gate: `{SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_POST_PROBE_DECISION_GATE_REPORT_PATH}`",
        f"- Source gate id: `{probe.source_gate_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Overall verdict: `{probe.overall_verdict}`",
        "",
        "| family | verdict | first mismatch index | zero count | residual hash |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in probe.family_results:
        lines.append(
            f"| `{item.family_id}` | `{item.verdict}` | `{item.first_mismatch_index}` | `{item.zero_count}` | `{item.transformed_residual_hash}` |"
        )
    lines.extend(
        [
            "",
            "## Source boundary",
            "",
            probe.source_boundary,
            "",
            "## Recommendation",
            "",
            probe.recommendation,
            "",
            "## Family coefficients",
            "",
        ]
    )
    for item in probe.family_results:
        lines.append(f"- `{item.family_id}` coefficients: `{', '.join(item.coefficients[:6])}` ...")
    lines.append("")
    return "\n".join(lines)


def write_symmetric_dual_baseline_chart_transfer_family_probe_report(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_FAMILY_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_dual_baseline_chart_transfer_family_probe(), encoding="utf-8")
    return output


def write_symmetric_dual_baseline_chart_transfer_family_probe_json(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_CHART_TRANSFER_FAMILY_PROBE_JSON_PATH,
) -> Path:
    probe = build_symmetric_dual_baseline_chart_transfer_family_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def _evaluate_constant_map(
    *,
    source_profiles: tuple[tuple[Fraction, ...], ...],
    target_profiles: tuple[tuple[Fraction, ...], ...],
) -> SymmetricDualBaselineChartTransferFamilyResult:
    rows = []
    for n in range(6):
        s = source_profiles[n]
        t = target_profiles[n]
        for j in range(6):
            row = [Fraction(0)] * 36 + [t[j]]
            for k in range(6):
                row[6 * j + k] = s[k]
            rows.append(tuple(row))
    solution = solve_exact_linear_system(tuple(rows))
    if solution is None:
        raise RuntimeError("constant_chart_map unexpectedly ill-posed")
    transformed = []
    for n in range(len(source_profiles)):
        s = source_profiles[n]
        pred = tuple(sum(solution[6 * j + k] * s[k] for k in range(6)) for j in range(6))
        transformed.append(tuple(target_profiles[n][j] - pred[j] for j in range(6)))
    return _finish_result(
        family_id="constant_chart_map",
        fit_window=(1, 6),
        validation_window=(1, len(source_profiles)),
        solution=solution,
        transformed=tuple(transformed),
    )


def _evaluate_difference_map(
    *,
    source_profiles: tuple[tuple[Fraction, ...], ...],
    target_profiles: tuple[tuple[Fraction, ...], ...],
) -> SymmetricDualBaselineChartTransferFamilyResult:
    rows = []
    for n in range(1, 7):
        ds = tuple(source_profiles[n][k] - source_profiles[n - 1][k] for k in range(6))
        t = target_profiles[n]
        for j in range(6):
            row = [Fraction(0)] * 36 + [t[j]]
            for k in range(6):
                row[6 * j + k] = ds[k]
            rows.append(tuple(row))
    solution = solve_exact_linear_system(tuple(rows))
    if solution is None:
        raise RuntimeError("difference_chart_map unexpectedly ill-posed")
    transformed = []
    for n in range(1, len(source_profiles)):
        ds = tuple(source_profiles[n][k] - source_profiles[n - 1][k] for k in range(6))
        pred = tuple(sum(solution[6 * j + k] * ds[k] for k in range(6)) for j in range(6))
        transformed.append(tuple(target_profiles[n][j] - pred[j] for j in range(6)))
    return _finish_result(
        family_id="difference_chart_map",
        fit_window=(2, 7),
        validation_window=(2, len(source_profiles)),
        solution=solution,
        transformed=tuple(transformed),
    )


def _evaluate_support_map(
    *,
    source_profiles: tuple[tuple[Fraction, ...], ...],
    target_profiles: tuple[tuple[Fraction, ...], ...],
    support_depth: int,
) -> SymmetricDualBaselineChartTransferFamilyResult:
    blocks = support_depth + 1
    coefficient_count = 36 * blocks
    fit_count = 6 * blocks
    start_index = support_depth
    rows = []
    for n in range(start_index, start_index + fit_count):
        history = [source_profiles[n - block] for block in range(blocks)]
        t = target_profiles[n]
        for j in range(6):
            row = [Fraction(0)] * coefficient_count + [t[j]]
            for block in range(blocks):
                for k in range(6):
                    row[36 * block + 6 * j + k] = history[block][k]
            rows.append(tuple(row))
    solution = solve_exact_linear_system(tuple(rows))
    if solution is None:
        raise RuntimeError(f"support{support_depth}_chart_map unexpectedly ill-posed")
    transformed = []
    for n in range(start_index, len(source_profiles)):
        history = [source_profiles[n - block] for block in range(blocks)]
        pred = []
        for j in range(6):
            total = Fraction(0)
            for block in range(blocks):
                total += sum(solution[36 * block + 6 * j + k] * history[block][k] for k in range(6))
            pred.append(total)
        transformed.append(tuple(target_profiles[n][j] - pred[j] for j in range(6)))
    return _finish_result(
        family_id=f"support{support_depth}_chart_map",
        fit_window=(start_index + 1, start_index + fit_count),
        validation_window=(start_index + 1, len(source_profiles)),
        solution=solution,
        transformed=tuple(transformed),
    )


def _finish_result(
    *,
    family_id: str,
    fit_window: tuple[int, int],
    validation_window: tuple[int, int],
    solution: tuple[Fraction, ...],
    transformed: tuple[tuple[Fraction, ...], ...],
) -> SymmetricDualBaselineChartTransferFamilyResult:
    transformed_payload = [
        {
            "n": validation_window[0] + index,
            "values": [fraction_to_canonical_string(value) for value in vector],
        }
        for index, vector in enumerate(transformed)
    ]
    mismatch_indices = [
        validation_window[0] + index
        for index, vector in enumerate(transformed)
        if any(value != 0 for value in vector)
    ]
    return SymmetricDualBaselineChartTransferFamilyResult(
        family_id=family_id,
        fit_window_start=fit_window[0],
        fit_window_end=fit_window[1],
        validation_window_start=validation_window[0],
        validation_window_end=validation_window[1],
        coefficients=tuple(fraction_to_canonical_string(value) for value in solution),
        transformed_residual_hash=compute_sequence_hash(
            provisional_signature={"kind": family_id, "terms": transformed_payload}
        ),
        verdict="holds_on_full_window" if not mismatch_indices else "fails_after_fit_window",
        zero_count=sum(1 for vector in transformed if all(value == 0 for value in vector)),
        first_mismatch_index=mismatch_indices[0] if mismatch_indices else None,
    )


def main() -> None:
    write_symmetric_dual_baseline_chart_transfer_family_probe_report()
    write_symmetric_dual_baseline_chart_transfer_family_probe_json()


if __name__ == "__main__":
    main()
