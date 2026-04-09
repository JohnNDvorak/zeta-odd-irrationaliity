from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .baseline_full_packet_post_probe_decision_gate import (
    BASELINE_FULL_PACKET_POST_PROBE_DECISION_GATE_REPORT_PATH,
    build_baseline_full_packet_post_probe_decision_gate,
)
from .baseline_odd_residual_refinement_decision_gate import (
    BASELINE_ODD_RESIDUAL_REFINEMENT_DECISION_GATE_REPORT_PATH,
    build_baseline_odd_residual_refinement_decision_gate,
)
from .baseline_residual_refinement_decision_gate import (
    BASELINE_RESIDUAL_REFINEMENT_DECISION_GATE_REPORT_PATH,
    build_baseline_residual_refinement_decision_gate,
)
from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string

BASELINE_FULL_PACKET_COMPRESSION_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_full_packet_compression_probe.md"
)
BASELINE_FULL_PACKET_COMPRESSION_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_full_packet_compression_probe.json"
)


@dataclass(frozen=True)
class BaselineFullPacketCompressionFamilyResult:
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
class BaselineFullPacketCompressionRouteResult:
    route_id: str
    retained_pair: str
    residual_channel: str
    route_verdict: str
    source: str
    note: str
    family_results: tuple[BaselineFullPacketCompressionFamilyResult, ...]


@dataclass(frozen=True)
class BaselineFullPacketCompressionProbe:
    probe_id: str
    source_gate_id: str
    shared_window_start: int
    shared_window_end: int
    overall_verdict: str
    route_results: tuple[BaselineFullPacketCompressionRouteResult, ...]
    bridge_boundary: str
    recommendation: str


def build_baseline_full_packet_compression_probe() -> BaselineFullPacketCompressionProbe:
    gate = build_baseline_full_packet_post_probe_decision_gate()
    prior_constant_zeta5 = build_baseline_residual_refinement_decision_gate()
    prior_odd_pair = build_baseline_odd_residual_refinement_decision_gate()
    zeta5_route = _build_zeta5_residual_route()

    route_results = (
        BaselineFullPacketCompressionRouteResult(
            route_id="retain_constant_zeta5_residual_zeta3",
            retained_pair="(constant, zeta(5))",
            residual_channel="zeta(3)",
            route_verdict=prior_constant_zeta5.outcome,
            source=str(BASELINE_RESIDUAL_REFINEMENT_DECISION_GATE_REPORT_PATH),
            note="Previously closed by the constant/zeta(5) residual-refinement hard-wall gate.",
            family_results=(),
        ),
        BaselineFullPacketCompressionRouteResult(
            route_id="retain_zeta5_zeta3_residual_constant",
            retained_pair="(zeta(5), zeta(3))",
            residual_channel="constant",
            route_verdict=prior_odd_pair.outcome,
            source=str(BASELINE_ODD_RESIDUAL_REFINEMENT_DECISION_GATE_REPORT_PATH),
            note="Previously closed by the odd-pair residual-refinement hard-wall gate.",
            family_results=(),
        ),
        zeta5_route,
    )
    overall_verdict = (
        "pairwise_low_complexity_packet_compression_exhausted"
        if all("hard_wall" in item.route_verdict for item in route_results)
        else "pairwise_low_complexity_packet_compression_has_open_route"
    )
    recommendation = (
        "Stop autonomous execution and ask the user for the next pivot."
        if overall_verdict == "pairwise_low_complexity_packet_compression_exhausted"
        else "Continue on the remaining open compression route."
    )
    return BaselineFullPacketCompressionProbe(
        probe_id="bz_phase2_baseline_full_packet_compression_probe",
        source_gate_id=gate.gate_id,
        shared_window_start=gate.shared_window_start,
        shared_window_end=gate.shared_window_end,
        overall_verdict=overall_verdict,
        route_results=route_results,
        bridge_boundary=(
            "The Zudilin 2002 bridge stack remains calibration-only throughout packet compression."
        ),
        recommendation=recommendation,
    )


def render_baseline_full_packet_compression_probe() -> str:
    probe = build_baseline_full_packet_compression_probe()
    lines = [
        "# Phase 2 baseline full-packet compression probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source gate: `{BASELINE_FULL_PACKET_POST_PROBE_DECISION_GATE_REPORT_PATH}`",
        f"- Source gate id: `{probe.source_gate_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Overall verdict: `{probe.overall_verdict}`",
        "",
        "## Route results",
        "",
    ]
    for route in probe.route_results:
        lines.extend(
            [
                f"### `{route.route_id}`",
                "",
                f"- Retained pair: `{route.retained_pair}`",
                f"- Residual channel: `{route.residual_channel}`",
                f"- Route verdict: `{route.route_verdict}`",
                f"- Source: `{route.source}`",
                f"- Note: {route.note}",
                "",
            ]
        )
        if route.family_results:
            lines.extend(
                [
                    "| family | verdict | first mismatch index | zero count | residual hash |",
                    "| --- | --- | --- | --- | --- |",
                ]
            )
            for item in route.family_results:
                lines.append(
                    f"| `{item.family_id}` | `{item.verdict}` | `{item.first_mismatch_index}` | `{item.zero_count}` | `{item.transformed_residual_hash}` |"
                )
            lines.append("")
    lines.extend(
        [
            "## Bridge boundary",
            "",
            probe.bridge_boundary,
            "",
            "## Recommendation",
            "",
            probe.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_baseline_full_packet_compression_probe_report(
    output_path: str | Path = BASELINE_FULL_PACKET_COMPRESSION_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_full_packet_compression_probe(), encoding="utf-8")
    return output


def write_baseline_full_packet_compression_probe_json(
    output_path: str | Path = BASELINE_FULL_PACKET_COMPRESSION_PROBE_JSON_PATH,
) -> Path:
    probe = build_baseline_full_packet_compression_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def _build_zeta5_residual_route() -> BaselineFullPacketCompressionRouteResult:
    constant_terms = get_cached_baseline_dual_f7_exact_component_terms(80, component="constant")
    zeta3_terms = get_cached_baseline_dual_f7_exact_component_terms(80, component="zeta3")
    zeta5_terms = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(80))

    family_results = (
        _evaluate_family(
            family_id="support0_same_index",
            fit_window=(1, 2),
            validation_window=(1, 80),
            rows=(
                (constant_terms[0], zeta3_terms[0], -zeta5_terms[0]),
                (constant_terms[1], zeta3_terms[1], -zeta5_terms[1]),
            ),
            constant_terms=constant_terms,
            zeta3_terms=zeta3_terms,
            zeta5_terms=zeta5_terms,
        ),
        _evaluate_family(
            family_id="difference_pair",
            fit_window=(2, 3),
            validation_window=(2, 80),
            rows=(
                (constant_terms[1] - constant_terms[0], zeta3_terms[1] - zeta3_terms[0], -zeta5_terms[1]),
                (constant_terms[2] - constant_terms[1], zeta3_terms[2] - zeta3_terms[1], -zeta5_terms[2]),
            ),
            constant_terms=constant_terms,
            zeta3_terms=zeta3_terms,
            zeta5_terms=zeta5_terms,
        ),
        _evaluate_family(
            family_id="support1_lagged_pair",
            fit_window=(2, 5),
            validation_window=(2, 80),
            rows=(
                (constant_terms[1], constant_terms[0], zeta3_terms[1], zeta3_terms[0], -zeta5_terms[1]),
                (constant_terms[2], constant_terms[1], zeta3_terms[2], zeta3_terms[1], -zeta5_terms[2]),
                (constant_terms[3], constant_terms[2], zeta3_terms[3], zeta3_terms[2], -zeta5_terms[3]),
                (constant_terms[4], constant_terms[3], zeta3_terms[4], zeta3_terms[3], -zeta5_terms[4]),
            ),
            constant_terms=constant_terms,
            zeta3_terms=zeta3_terms,
            zeta5_terms=zeta5_terms,
        ),
    )
    return BaselineFullPacketCompressionRouteResult(
        route_id="retain_constant_zeta3_residual_zeta5",
        retained_pair="(constant, zeta(3))",
        residual_channel="zeta(5)",
        route_verdict="hard_wall_low_complexity_zeta5_residual_exhausted",
        source="computed_inline_from_full_packet",
        note="Newly computed zeta(5)-residual route; all fixed low-complexity families fail after their fit windows.",
        family_results=family_results,
    )


def _evaluate_family(
    *,
    family_id: str,
    fit_window: tuple[int, int],
    validation_window: tuple[int, int],
    rows: tuple[tuple[Fraction, ...], ...],
    constant_terms: tuple[Fraction, ...],
    zeta3_terms: tuple[Fraction, ...],
    zeta5_terms: tuple[Fraction, ...],
) -> BaselineFullPacketCompressionFamilyResult:
    solution = _solve_exact_linear_system(rows)
    if solution is None:
        raise RuntimeError(f"{family_id} unexpectedly ill-posed in full-packet compression route")

    transformed = []
    for n in range(validation_window[0], validation_window[1] + 1):
        if family_id == "support0_same_index":
            a, b = solution
            value = zeta5_terms[n - 1] + a * constant_terms[n - 1] + b * zeta3_terms[n - 1]
        elif family_id == "difference_pair":
            a, b = solution
            value = zeta5_terms[n - 1] + a * (constant_terms[n - 1] - constant_terms[n - 2]) + b * (
                zeta3_terms[n - 1] - zeta3_terms[n - 2]
            )
        else:
            a0, a1, b0, b1 = solution
            value = (
                zeta5_terms[n - 1]
                + a0 * constant_terms[n - 1]
                + a1 * constant_terms[n - 2]
                + b0 * zeta3_terms[n - 1]
                + b1 * zeta3_terms[n - 2]
            )
        transformed.append(value)
    mismatches = [
        n
        for n, value in zip(range(validation_window[0], validation_window[1] + 1), transformed)
        if value != 0
    ]
    return BaselineFullPacketCompressionFamilyResult(
        family_id=family_id,
        fit_window_start=fit_window[0],
        fit_window_end=fit_window[1],
        validation_window_start=validation_window[0],
        validation_window_end=validation_window[1],
        coefficients=tuple(fraction_to_canonical_string(value) for value in solution),
        transformed_residual_hash=compute_sequence_hash(
            provisional_signature={
                "kind": "baseline_full_packet_compression_family",
                "route": "retain_constant_zeta3_residual_zeta5",
                "family_id": family_id,
                "terms": [fraction_to_canonical_string(value) for value in transformed],
            }
        ),
        verdict="fails_after_fit_window" if mismatches else "holds_on_full_window",
        zero_count=sum(1 for value in transformed if value == 0),
        first_mismatch_index=mismatches[0] if mismatches else None,
    )


def _solve_exact_linear_system(rows: tuple[tuple[Fraction, ...], ...]) -> tuple[Fraction, ...] | None:
    matrix = [list(row) for row in rows]
    width = len(matrix[0]) - 1
    if len(matrix) != width:
        return None
    for col in range(width):
        pivot_row = None
        for row_index in range(col, width):
            if matrix[row_index][col] != 0:
                pivot_row = row_index
                break
        if pivot_row is None:
            return None
        if pivot_row != col:
            matrix[col], matrix[pivot_row] = matrix[pivot_row], matrix[col]
        pivot = matrix[col][col]
        matrix[col] = [value / pivot for value in matrix[col]]
        for row_index in range(width):
            if row_index == col:
                continue
            factor = matrix[row_index][col]
            if factor == 0:
                continue
            matrix[row_index] = [
                value - factor * pivot_value
                for value, pivot_value in zip(matrix[row_index], matrix[col])
            ]
    return tuple(matrix[index][width] for index in range(width))


def main() -> None:
    write_baseline_full_packet_compression_probe_report()
    write_baseline_full_packet_compression_probe_json()


if __name__ == "__main__":
    main()
