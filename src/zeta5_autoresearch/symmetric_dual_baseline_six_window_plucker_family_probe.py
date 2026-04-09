from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_packet_local_annihilator_profile import solve_exact_linear_system_with_zero_free_variables
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string
from .symmetric_dual_baseline_six_window_plucker_probe import (
    SIX_WINDOW_NORMALIZED_PLUCKER_PROBE_REPORT_PATH,
    build_six_window_normalized_plucker_probe,
    build_six_window_normalized_plucker_sequences,
)

SIX_WINDOW_NORMALIZED_PLUCKER_FAMILY_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_six_window_normalized_plucker_family_probe.md"
)
SIX_WINDOW_NORMALIZED_PLUCKER_FAMILY_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_six_window_normalized_plucker_family_probe.json"
)


PluckerVector = tuple[Fraction, ...]


@dataclass(frozen=True)
class SixWindowNormalizedPluckerFamilyResult:
    family_id: str
    fit_window_start: int
    fit_window_end: int
    validation_window_start: int
    validation_window_end: int
    rank: int
    nullity: int
    verdict: str
    first_mismatch_index: int | None
    zero_count: int
    transformed_residual_hash: str
    note: str


@dataclass(frozen=True)
class SixWindowNormalizedPluckerFamilyProbe:
    probe_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    coordinate_count: int
    family_results: tuple[SixWindowNormalizedPluckerFamilyResult, ...]
    overall_verdict: str
    source_boundary: str
    recommendation: str


def _vector_hash(family_id: str, validation_start: int, transformed: tuple[PluckerVector, ...]) -> str:
    payload = [
        {
            "n": validation_start + index,
            "values": [fraction_to_canonical_string(value) for value in vector],
        }
        for index, vector in enumerate(transformed)
    ]
    return compute_sequence_hash(provisional_signature={"kind": family_id, "terms": payload})


def _finish_family(
    *,
    family_id: str,
    fit_window: tuple[int, int],
    validation_window: tuple[int, int],
    rank: int,
    nullity: int,
    transformed: tuple[PluckerVector, ...],
    note: str,
    verdict_override: str | None = None,
) -> SixWindowNormalizedPluckerFamilyResult:
    mismatch_indices = [
        validation_window[0] + index
        for index, vector in enumerate(transformed)
        if any(value != 0 for value in vector)
    ]
    verdict = verdict_override or ("holds_on_full_window" if not mismatch_indices else "fails_after_fit_window")
    return SixWindowNormalizedPluckerFamilyResult(
        family_id=family_id,
        fit_window_start=fit_window[0],
        fit_window_end=fit_window[1],
        validation_window_start=validation_window[0],
        validation_window_end=validation_window[1],
        rank=rank,
        nullity=nullity,
        verdict=verdict,
        first_mismatch_index=mismatch_indices[0] if mismatch_indices else None,
        zero_count=sum(1 for vector in transformed if all(value == 0 for value in vector)),
        transformed_residual_hash=_vector_hash(family_id, validation_window[0], transformed),
        note=note,
    )


def _evaluate_constant_family(
    source: tuple[PluckerVector, ...],
    target: tuple[PluckerVector, ...],
) -> SixWindowNormalizedPluckerFamilyResult:
    dimension = len(source[0])
    rows = []
    for n in range(dimension):
        feature = source[n]
        target_vector = target[n]
        for j in range(dimension):
            row = [Fraction(0)] * (dimension * dimension) + [target_vector[j]]
            base = dimension * j
            for k in range(dimension):
                row[base + k] = feature[k]
            rows.append(tuple(row))
    solution, rank, nullity = solve_exact_linear_system_with_zero_free_variables(tuple(rows))  # type: ignore[misc]
    transformed = []
    for n in range(len(source)):
        feature = source[n]
        predicted = []
        for j in range(dimension):
            total = Fraction(0)
            base = dimension * j
            for k in range(dimension):
                total += solution[base + k] * feature[k]
            predicted.append(total)
        transformed.append(tuple(target[n][j] - predicted[j] for j in range(dimension)))
    return _finish_family(
        family_id="constant_six_plucker_map",
        fit_window=(1, dimension),
        validation_window=(1, len(source)),
        rank=rank,
        nullity=nullity,
        transformed=tuple(transformed),
        note="Cheap same-index family on the full six-window normalized Plucker object.",
    )


def _evaluate_difference_family(
    source: tuple[PluckerVector, ...],
    target: tuple[PluckerVector, ...],
) -> SixWindowNormalizedPluckerFamilyResult:
    dimension = len(source[0])
    rows = []
    for n in range(1, dimension + 1):
        feature = tuple(source[n][k] - source[n - 1][k] for k in range(dimension))
        target_vector = target[n]
        for j in range(dimension):
            row = [Fraction(0)] * (dimension * dimension) + [target_vector[j]]
            base = dimension * j
            for k in range(dimension):
                row[base + k] = feature[k]
            rows.append(tuple(row))
    solution, rank, nullity = solve_exact_linear_system_with_zero_free_variables(tuple(rows))  # type: ignore[misc]
    transformed = []
    for n in range(1, len(source)):
        feature = tuple(source[n][k] - source[n - 1][k] for k in range(dimension))
        predicted = []
        for j in range(dimension):
            total = Fraction(0)
            base = dimension * j
            for k in range(dimension):
                total += solution[base + k] * feature[k]
            predicted.append(total)
        transformed.append(tuple(target[n][j] - predicted[j] for j in range(dimension)))
    return _finish_family(
        family_id="difference_six_plucker_map",
        fit_window=(2, dimension + 1),
        validation_window=(2, len(source)),
        rank=rank,
        nullity=nullity,
        transformed=tuple(transformed),
        note="Cheap first-difference family on the full six-window normalized Plucker object.",
    )


def _evaluate_support1_free_zero_family(
    source: tuple[PluckerVector, ...],
    target: tuple[PluckerVector, ...],
) -> SixWindowNormalizedPluckerFamilyResult:
    dimension = len(source[0])
    feature_dimension = 2 * dimension
    start_index = 1
    fit_count = feature_dimension

    feature_rows = [
        tuple(list(source[n]) + list(source[n - 1]))
        for n in range(start_index, start_index + fit_count)
    ]
    feature_augmented_rows = tuple(row + (Fraction(0),) for row in feature_rows)
    _, feature_rank, feature_nullity = solve_exact_linear_system_with_zero_free_variables(feature_augmented_rows)  # type: ignore[misc]

    coordinate_solutions: list[tuple[Fraction, ...]] = []
    for j in range(dimension):
        rows = []
        for offset, n in enumerate(range(start_index, start_index + fit_count)):
            rows.append(tuple(list(feature_rows[offset]) + [target[n][j]]))
        solved = solve_exact_linear_system_with_zero_free_variables(tuple(rows))
        if solved is None:
            return _finish_family(
                family_id="support1_free_zero_six_plucker_map",
                fit_window=(start_index + 1, start_index + fit_count),
                validation_window=(start_index + 1, len(source)),
                rank=feature_rank,
                nullity=feature_nullity,
                transformed=tuple(),
                note="Canonical free-zero support-1 family is inconsistent on at least one target coordinate.",
                verdict_override="inconsistent_fit_block",
            )
        solution, _, _ = solved
        coordinate_solutions.append(solution)

    transformed = []
    for n in range(start_index, len(source)):
        feature = tuple(list(source[n]) + list(source[n - 1]))
        predicted = []
        for j in range(dimension):
            total = Fraction(0)
            for k in range(feature_dimension):
                total += coordinate_solutions[j][k] * feature[k]
            predicted.append(total)
        transformed.append(tuple(target[n][j] - predicted[j] for j in range(dimension)))
    return _finish_family(
        family_id="support1_free_zero_six_plucker_map",
        fit_window=(start_index + 1, start_index + fit_count),
        validation_window=(start_index + 1, len(source)),
        rank=feature_rank,
        nullity=feature_nullity,
        transformed=tuple(transformed),
        note=(
            "Canonical support-1 family on the six-window normalized Plucker object, using exact RREF with free variables fixed to zero on the singular fit block."
        ),
    )


def build_six_window_normalized_plucker_family_probe() -> SixWindowNormalizedPluckerFamilyProbe:
    source_probe = build_six_window_normalized_plucker_probe()
    source, target = build_six_window_normalized_plucker_sequences()
    family_results = (
        _evaluate_constant_family(source, target),
        _evaluate_difference_family(source, target),
        _evaluate_support1_free_zero_family(source, target),
    )
    winner_exists = any(item.verdict == "holds_on_full_window" for item in family_results)
    return SixWindowNormalizedPluckerFamilyProbe(
        probe_id="bz_phase2_six_window_normalized_plucker_family_probe",
        source_probe_id=source_probe.probe_id,
        shared_window_start=1,
        shared_window_end=len(source),
        coordinate_count=len(source[0]),
        family_results=family_results,
        overall_verdict=(
            "six_window_plucker_family_has_winner"
            if winner_exists
            else "six_window_plucker_family_exhausted_on_current_ladder"
        ),
        source_boundary=source_probe.source_boundary,
        recommendation=(
            "Promote the winning family into the next frontier artifact."
            if winner_exists
            else "Use the family outcomes to choose whether the six-window object stays active or needs a different recurrence-level family."
        ),
    )


def render_six_window_normalized_plucker_family_probe() -> str:
    probe = build_six_window_normalized_plucker_family_probe()
    lines = [
        "# Phase 2 six-window normalized Plucker family probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source probe: `{SIX_WINDOW_NORMALIZED_PLUCKER_PROBE_REPORT_PATH}`",
        f"- Source probe id: `{probe.source_probe_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Coordinate count: `{probe.coordinate_count}`",
        f"- Overall verdict: `{probe.overall_verdict}`",
        "",
        "| family | verdict | rank | nullity | first mismatch index | zero count | residual hash |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in probe.family_results:
        lines.append(
            f"| `{item.family_id}` | `{item.verdict}` | `{item.rank}` | `{item.nullity}` | `{item.first_mismatch_index}` | `{item.zero_count}` | `{item.transformed_residual_hash}` |"
        )
    lines.extend(["", "## Notes", ""])
    for item in probe.family_results:
        lines.append(f"- `{item.family_id}`: {item.note}")
    lines.extend(["", "## Source boundary", "", probe.source_boundary, "", "## Recommendation", "", probe.recommendation, ""])
    return "\n".join(lines)


def write_six_window_normalized_plucker_family_probe_report(
    output_path: str | Path = SIX_WINDOW_NORMALIZED_PLUCKER_FAMILY_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_six_window_normalized_plucker_family_probe(), encoding="utf-8")
    return output


def write_six_window_normalized_plucker_family_probe_json(
    output_path: str | Path = SIX_WINDOW_NORMALIZED_PLUCKER_FAMILY_PROBE_JSON_PATH,
) -> Path:
    probe = build_six_window_normalized_plucker_family_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_six_window_normalized_plucker_family_probe_report()
    write_six_window_normalized_plucker_family_probe_json()


if __name__ == "__main__":
    main()
