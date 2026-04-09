from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .dual_packet_local_annihilator_profile import (
    build_local_annihilator_profiles,
    solve_exact_linear_system,
)
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string
from .symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate import (
    SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_POST_PROBE_DECISION_GATE_REPORT_PATH,
    build_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate,
)
from .symmetric_dual_full_packet import build_symmetric_dual_full_packet

SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_FAMILY_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_symmetric_dual_baseline_annihilator_transfer_family_probe.md"
)
SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_FAMILY_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_symmetric_dual_baseline_annihilator_transfer_family_probe.json"
)


@dataclass(frozen=True)
class SymmetricDualBaselineAnnihilatorTransferFamilyResult:
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
class SymmetricDualBaselineAnnihilatorTransferFamilyProbe:
    probe_id: str
    source_gate_id: str
    shared_window_start: int
    shared_window_end: int
    overall_verdict: str
    family_results: tuple[SymmetricDualBaselineAnnihilatorTransferFamilyResult, ...]
    source_boundary: str
    recommendation: str


def build_symmetric_dual_baseline_annihilator_transfer_family_probe(
) -> SymmetricDualBaselineAnnihilatorTransferFamilyProbe:
    gate = build_symmetric_dual_baseline_annihilator_transfer_post_probe_decision_gate()
    source_packet = build_symmetric_dual_full_packet(max_n=80)
    source_vectors = tuple(
        (source_packet.constant_terms[i], source_packet.zeta3_terms[i], source_packet.zeta5_terms[i])
        for i in range(80)
    )
    target_constant = get_cached_baseline_dual_f7_exact_component_terms(80, component="constant")
    target_zeta3 = get_cached_baseline_dual_f7_exact_component_terms(80, component="zeta3")
    target_zeta5 = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(80))
    target_vectors = tuple((target_constant[i], target_zeta3[i], target_zeta5[i]) for i in range(80))

    source_profiles = build_local_annihilator_profiles(source_vectors)
    target_profiles = build_local_annihilator_profiles(target_vectors)
    family_results = (
        _evaluate_constant_map(source_profiles=source_profiles, target_profiles=target_profiles),
        _evaluate_difference_map(source_profiles=source_profiles, target_profiles=target_profiles),
        _evaluate_lag1_map(source_profiles=source_profiles, target_profiles=target_profiles),
    )
    winner_exists = any(item.verdict == "holds_on_full_window" for item in family_results)
    return SymmetricDualBaselineAnnihilatorTransferFamilyProbe(
        probe_id="bz_phase2_symmetric_dual_baseline_annihilator_transfer_family_probe",
        source_gate_id=gate.gate_id,
        shared_window_start=1,
        shared_window_end=77,
        overall_verdict=(
            "low_complexity_symmetric_dual_baseline_annihilator_transfer_has_winner"
            if winner_exists
            else "low_complexity_symmetric_dual_baseline_annihilator_transfer_exhausted"
        ),
        family_results=family_results,
        source_boundary=(
            "A local-annihilator transfer success would still be a bounded profile relation on `n=1..77`, not a proof of common recurrence or packet equivalence."
        ),
        recommendation=(
            "Promote the winning transfer family into a v2 profile-transfer artifact."
            if winner_exists
            else "Stop and ask for the next pivot."
        ),
    )


def render_symmetric_dual_baseline_annihilator_transfer_family_probe() -> str:
    probe = build_symmetric_dual_baseline_annihilator_transfer_family_probe()
    lines = [
        "# Phase 2 symmetric-dual to baseline-dual annihilator transfer family probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source gate: `{SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_POST_PROBE_DECISION_GATE_REPORT_PATH}`",
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
        lines.append(f"- `{item.family_id}` coefficients: `{', '.join(item.coefficients)}`")
    lines.append("")
    return "\n".join(lines)


def write_symmetric_dual_baseline_annihilator_transfer_family_probe_report(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_FAMILY_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_symmetric_dual_baseline_annihilator_transfer_family_probe(), encoding="utf-8")
    return output


def write_symmetric_dual_baseline_annihilator_transfer_family_probe_json(
    output_path: str | Path = SYMMETRIC_DUAL_BASELINE_ANNIHILATOR_TRANSFER_FAMILY_PROBE_JSON_PATH,
) -> Path:
    probe = build_symmetric_dual_baseline_annihilator_transfer_family_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def _evaluate_constant_map(
    *,
    source_profiles: tuple[tuple[Fraction, Fraction, Fraction], ...],
    target_profiles: tuple[tuple[Fraction, Fraction, Fraction], ...],
) -> SymmetricDualBaselineAnnihilatorTransferFamilyResult:
    rows = []
    for n in range(3):
        source_vector = source_profiles[n]
        target_vector = target_profiles[n]
        for target_index in range(3):
            row = [Fraction(0)] * 9 + [target_vector[target_index]]
            for source_index in range(3):
                row[3 * target_index + source_index] = source_vector[source_index]
            rows.append(tuple(row))
    solution = solve_exact_linear_system(tuple(rows))
    if solution is None:
        raise RuntimeError("constant_profile_map unexpectedly ill-posed")
    transformed = []
    for n in range(len(source_profiles)):
        source_vector = source_profiles[n]
        predicted = tuple(
            sum(solution[3 * target_index + source_index] * source_vector[source_index] for source_index in range(3))
            for target_index in range(3)
        )
        transformed.append(tuple(target_profiles[n][target_index] - predicted[target_index] for target_index in range(3)))
    return _finish_family_result(
        family_id="constant_profile_map",
        fit_window=(1, 3),
        validation_window=(1, len(source_profiles)),
        solution=solution,
        transformed=tuple(transformed),
    )


def _evaluate_difference_map(
    *,
    source_profiles: tuple[tuple[Fraction, Fraction, Fraction], ...],
    target_profiles: tuple[tuple[Fraction, Fraction, Fraction], ...],
) -> SymmetricDualBaselineAnnihilatorTransferFamilyResult:
    rows = []
    for n in range(1, 4):
        diff_vector = tuple(source_profiles[n][index] - source_profiles[n - 1][index] for index in range(3))
        target_vector = target_profiles[n]
        for target_index in range(3):
            row = [Fraction(0)] * 9 + [target_vector[target_index]]
            for source_index in range(3):
                row[3 * target_index + source_index] = diff_vector[source_index]
            rows.append(tuple(row))
    solution = solve_exact_linear_system(tuple(rows))
    if solution is None:
        raise RuntimeError("difference_profile_map unexpectedly ill-posed")
    transformed = []
    for n in range(1, len(source_profiles)):
        diff_vector = tuple(source_profiles[n][index] - source_profiles[n - 1][index] for index in range(3))
        predicted = tuple(
            sum(solution[3 * target_index + source_index] * diff_vector[source_index] for source_index in range(3))
            for target_index in range(3)
        )
        transformed.append(tuple(target_profiles[n][target_index] - predicted[target_index] for target_index in range(3)))
    return _finish_family_result(
        family_id="difference_profile_map",
        fit_window=(2, 4),
        validation_window=(2, len(source_profiles)),
        solution=solution,
        transformed=tuple(transformed),
    )


def _evaluate_lag1_map(
    *,
    source_profiles: tuple[tuple[Fraction, Fraction, Fraction], ...],
    target_profiles: tuple[tuple[Fraction, Fraction, Fraction], ...],
) -> SymmetricDualBaselineAnnihilatorTransferFamilyResult:
    rows = []
    for n in range(1, 7):
        current_vector = source_profiles[n]
        previous_vector = source_profiles[n - 1]
        target_vector = target_profiles[n]
        for target_index in range(3):
            row = [Fraction(0)] * 18 + [target_vector[target_index]]
            for source_index in range(3):
                row[3 * target_index + source_index] = current_vector[source_index]
                row[9 + 3 * target_index + source_index] = previous_vector[source_index]
            rows.append(tuple(row))
    solution = solve_exact_linear_system(tuple(rows))
    if solution is None:
        raise RuntimeError("support1_profile_map unexpectedly ill-posed")
    transformed = []
    for n in range(1, len(source_profiles)):
        current_vector = source_profiles[n]
        previous_vector = source_profiles[n - 1]
        predicted = []
        for target_index in range(3):
            current_part = sum(solution[3 * target_index + source_index] * current_vector[source_index] for source_index in range(3))
            previous_part = sum(solution[9 + 3 * target_index + source_index] * previous_vector[source_index] for source_index in range(3))
            predicted.append(current_part + previous_part)
        transformed.append(tuple(target_profiles[n][target_index] - predicted[target_index] for target_index in range(3)))
    return _finish_family_result(
        family_id="support1_profile_map",
        fit_window=(2, 7),
        validation_window=(2, len(source_profiles)),
        solution=solution,
        transformed=tuple(transformed),
    )


def _finish_family_result(
    *,
    family_id: str,
    fit_window: tuple[int, int],
    validation_window: tuple[int, int],
    solution: tuple[Fraction, ...],
    transformed: tuple[tuple[Fraction, Fraction, Fraction], ...],
) -> SymmetricDualBaselineAnnihilatorTransferFamilyResult:
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
        if vector != (Fraction(0), Fraction(0), Fraction(0))
    ]
    return SymmetricDualBaselineAnnihilatorTransferFamilyResult(
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
        zero_count=sum(1 for vector in transformed if vector == (Fraction(0), Fraction(0), Fraction(0))),
        first_mismatch_index=mismatch_indices[0] if mismatch_indices else None,
    )


def main() -> None:
    write_symmetric_dual_baseline_annihilator_transfer_family_probe_report()
    write_symmetric_dual_baseline_annihilator_transfer_family_probe_json()


if __name__ == "__main__":
    main()
