from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string
from .symmetric_linear_forms_packet import build_symmetric_linear_forms_exact_packet
from .symmetric_source_packet_post_probe_decision_gate import (
    SYMMETRIC_SOURCE_PACKET_POST_PROBE_DECISION_GATE_REPORT_PATH,
    build_symmetric_source_packet_post_probe_decision_gate,
)

SYMMETRIC_SOURCE_PACKET_COMPRESSION_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_source_packet_compression_probe.md"
)
SYMMETRIC_SOURCE_PACKET_COMPRESSION_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_source_packet_compression_probe.json"
)


@dataclass(frozen=True)
class SymmetricSourcePacketCompressionFamilyResult:
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
class SymmetricSourcePacketCompressionRouteResult:
    route_id: str
    retained_pair: str
    residual_channel: str
    route_verdict: str
    note: str
    family_results: tuple[SymmetricSourcePacketCompressionFamilyResult, ...]


@dataclass(frozen=True)
class SymmetricSourcePacketCompressionProbe:
    probe_id: str
    source_gate_id: str
    shared_window_start: int
    shared_window_end: int
    overall_verdict: str
    route_results: tuple[SymmetricSourcePacketCompressionRouteResult, ...]
    source_boundary: str
    recommendation: str


def build_symmetric_source_packet_compression_probe() -> SymmetricSourcePacketCompressionProbe:
    gate = build_symmetric_source_packet_post_probe_decision_gate()
    packet = build_symmetric_linear_forms_exact_packet(max_n=80)

    route_results = (
        _build_route_result(
            route_id="retain_scaled_q_scaled_p_residual_scaled_phat",
            retained_pair="(scaled Q_n, scaled P_n)",
            residual_channel="scaled Phat_n",
            retained_left=packet.scaled_q_terms,
            retained_right=packet.scaled_p_terms,
            residual=packet.scaled_phat_terms,
        ),
        _build_route_result(
            route_id="retain_scaled_q_scaled_phat_residual_scaled_p",
            retained_pair="(scaled Q_n, scaled Phat_n)",
            residual_channel="scaled P_n",
            retained_left=packet.scaled_q_terms,
            retained_right=packet.scaled_phat_terms,
            residual=packet.scaled_p_terms,
        ),
        _build_route_result(
            route_id="retain_scaled_p_scaled_phat_residual_scaled_q",
            retained_pair="(scaled P_n, scaled Phat_n)",
            residual_channel="scaled Q_n",
            retained_left=packet.scaled_p_terms,
            retained_right=packet.scaled_phat_terms,
            residual=packet.scaled_q_terms,
        ),
    )
    all_closed = all(item.route_verdict.startswith("hard_wall") for item in route_results)
    return SymmetricSourcePacketCompressionProbe(
        probe_id="bz_phase2_symmetric_source_packet_compression_probe",
        source_gate_id=gate.gate_id,
        shared_window_start=gate.shared_window_start,
        shared_window_end=gate.shared_window_end,
        overall_verdict=(
            "pairwise_low_complexity_symmetric_source_packet_compression_exhausted"
            if all_closed
            else "pairwise_low_complexity_symmetric_source_packet_has_open_route"
        ),
        route_results=route_results,
        source_boundary=(
            "The symmetric source family remains a source-backed anchor, not a hidden claim of baseline equivalence."
        ),
        recommendation=(
            "Stop and ask for the next pivot."
            if all_closed
            else "Continue on the surviving symmetric source compression route."
        ),
    )


def render_symmetric_source_packet_compression_probe() -> str:
    probe = build_symmetric_source_packet_compression_probe()
    lines = [
        "# Phase 2 symmetric source packet compression probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source gate: `{SYMMETRIC_SOURCE_PACKET_POST_PROBE_DECISION_GATE_REPORT_PATH}`",
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
                f"- Note: {route.note}",
                "",
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
            "## Source boundary",
            "",
            probe.source_boundary,
            "",
            "## Recommendation",
            "",
            probe.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_symmetric_source_packet_compression_probe_report(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_COMPRESSION_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_source_packet_compression_probe(), encoding="utf-8")
    return output


def write_symmetric_source_packet_compression_probe_json(
    output_path: str | Path = SYMMETRIC_SOURCE_PACKET_COMPRESSION_PROBE_JSON_PATH,
) -> Path:
    probe = build_symmetric_source_packet_compression_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def _build_route_result(
    *,
    route_id: str,
    retained_pair: str,
    residual_channel: str,
    retained_left: tuple[Fraction, ...],
    retained_right: tuple[Fraction, ...],
    residual: tuple[Fraction, ...],
) -> SymmetricSourcePacketCompressionRouteResult:
    family_results = (
        _evaluate_family(
            route_id=route_id,
            family_id="support0_same_index",
            fit_window=(1, 2),
            validation_window=(1, 80),
            rows=(
                (retained_left[0], retained_right[0], -residual[0]),
                (retained_left[1], retained_right[1], -residual[1]),
            ),
            retained_left=retained_left,
            retained_right=retained_right,
            residual=residual,
        ),
        _evaluate_family(
            route_id=route_id,
            family_id="difference_pair",
            fit_window=(2, 3),
            validation_window=(2, 80),
            rows=(
                (retained_left[1] - retained_left[0], retained_right[1] - retained_right[0], -residual[1]),
                (retained_left[2] - retained_left[1], retained_right[2] - retained_right[1], -residual[2]),
            ),
            retained_left=retained_left,
            retained_right=retained_right,
            residual=residual,
        ),
        _evaluate_family(
            route_id=route_id,
            family_id="support1_lagged_pair",
            fit_window=(2, 5),
            validation_window=(2, 80),
            rows=(
                (retained_left[1], retained_left[0], retained_right[1], retained_right[0], -residual[1]),
                (retained_left[2], retained_left[1], retained_right[2], retained_right[1], -residual[2]),
                (retained_left[3], retained_left[2], retained_right[3], retained_right[2], -residual[3]),
                (retained_left[4], retained_left[3], retained_right[4], retained_right[3], -residual[4]),
            ),
            retained_left=retained_left,
            retained_right=retained_right,
            residual=residual,
        ),
    )
    open_route = any(item.verdict == "holds_on_full_window" for item in family_results)
    return SymmetricSourcePacketCompressionRouteResult(
        route_id=route_id,
        retained_pair=retained_pair,
        residual_channel=residual_channel,
        route_verdict=(
            f"low_complexity_{_normalize_label(residual_channel)}_residual_has_winner"
            if open_route
            else f"hard_wall_low_complexity_{_normalize_label(residual_channel)}_residual_exhausted"
        ),
        note=(
            "At least one fixed low-complexity family holds on the full validation window."
            if open_route
            else "All fixed low-complexity families fail after their fit windows."
        ),
        family_results=family_results,
    )


def _evaluate_family(
    *,
    route_id: str,
    family_id: str,
    fit_window: tuple[int, int],
    validation_window: tuple[int, int],
    rows: tuple[tuple[Fraction, ...], ...],
    retained_left: tuple[Fraction, ...],
    retained_right: tuple[Fraction, ...],
    residual: tuple[Fraction, ...],
) -> SymmetricSourcePacketCompressionFamilyResult:
    solution = _solve_exact_linear_system(rows)
    if solution is None:
        raise RuntimeError(f"{family_id} unexpectedly ill-posed in symmetric source compression route")

    transformed = []
    for n in range(validation_window[0], validation_window[1] + 1):
        if family_id == "support0_same_index":
            a, b = solution
            value = residual[n - 1] + a * retained_left[n - 1] + b * retained_right[n - 1]
        elif family_id == "difference_pair":
            a, b = solution
            value = residual[n - 1] + a * (retained_left[n - 1] - retained_left[n - 2]) + b * (
                retained_right[n - 1] - retained_right[n - 2]
            )
        else:
            a0, a1, b0, b1 = solution
            value = (
                residual[n - 1]
                + a0 * retained_left[n - 1]
                + a1 * retained_left[n - 2]
                + b0 * retained_right[n - 1]
                + b1 * retained_right[n - 2]
            )
        transformed.append(value)
    mismatches = [
        n
        for n, value in zip(range(validation_window[0], validation_window[1] + 1), transformed)
        if value != 0
    ]
    return SymmetricSourcePacketCompressionFamilyResult(
        family_id=family_id,
        fit_window_start=fit_window[0],
        fit_window_end=fit_window[1],
        validation_window_start=validation_window[0],
        validation_window_end=validation_window[1],
        coefficients=tuple(fraction_to_canonical_string(value) for value in solution),
        transformed_residual_hash=compute_sequence_hash(
            provisional_signature={
                "kind": "symmetric_source_packet_compression_family",
                "route": route_id,
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


def _normalize_label(text: str) -> str:
    return text.lower().replace(" ", "_")


def main() -> None:
    write_symmetric_source_packet_compression_probe_report()
    write_symmetric_source_packet_compression_probe_json()


if __name__ == "__main__":
    main()
