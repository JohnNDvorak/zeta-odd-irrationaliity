from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from .baseline_odd_extraction_rule import build_baseline_odd_extraction_rule
from .baseline_odd_residual_refinement_spec import (
    BASELINE_ODD_RESIDUAL_REFINEMENT_SPEC_REPORT_PATH,
    BaselineOddResidualRefinementFamilySpec,
    build_baseline_odd_residual_refinement_spec,
)
from .config import CACHE_DIR, DATA_DIR
from .dual_f7_exact_coefficient_cache import get_cached_baseline_dual_f7_exact_component_terms
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .hashes import compute_sequence_hash
from .models import fraction_to_canonical_string

BASELINE_ODD_RESIDUAL_REFINEMENT_PROBE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_odd_residual_refinement_probe.md"
)
BASELINE_ODD_RESIDUAL_REFINEMENT_PROBE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_odd_residual_refinement_probe.json"
)


@dataclass(frozen=True)
class BaselineOddResidualRefinementCoefficient:
    label: str
    value: str


@dataclass(frozen=True)
class BaselineOddResidualSample:
    n: int
    value: str


@dataclass(frozen=True)
class BaselineOddResidualRefinementFamilyResult:
    family_id: str
    family_label: str
    fit_window_start: int
    fit_window_end: int
    validation_window_start: int
    validation_window_end: int
    family_statement: str
    coefficients: tuple[BaselineOddResidualRefinementCoefficient, ...]
    transformed_residual_hash: str
    verdict: str
    zero_count: int
    mismatch_indices: tuple[int, ...]
    first_mismatch_index: int | None
    first_samples: tuple[BaselineOddResidualSample, ...]


@dataclass(frozen=True)
class BaselineOddResidualRefinementProbe:
    probe_id: str
    source_spec_id: str
    source_rule_id: str
    shared_window_start: int
    shared_window_end: int
    overall_verdict: str
    family_results: tuple[BaselineOddResidualRefinementFamilyResult, ...]
    bridge_boundary: str
    recommendation: str


def build_baseline_odd_residual_refinement_probe() -> BaselineOddResidualRefinementProbe:
    spec = build_baseline_odd_residual_refinement_spec()
    rule = build_baseline_odd_extraction_rule()
    zeta5_terms, zeta3_terms, constant_terms = _load_baseline_terms(rule.shared_window_end)

    family_results = tuple(
        _evaluate_family(
            family_spec=family,
            zeta5_terms=zeta5_terms,
            zeta3_terms=zeta3_terms,
            constant_terms=constant_terms,
        )
        for family in spec.family_specs
    )
    overall_verdict = (
        "low_complexity_odd_refinement_has_winner"
        if any(item.verdict == "holds_on_full_window" for item in family_results)
        else "low_complexity_odd_refinement_exhausted"
    )
    recommendation = (
        "Promote the winning family into a v2 odd extraction branch."
        if overall_verdict == "low_complexity_odd_refinement_has_winner"
        else "Run the odd residual-refinement decision gate next and stop unless a user-approved pivot is chosen."
    )
    return BaselineOddResidualRefinementProbe(
        probe_id="bz_phase2_baseline_odd_residual_refinement_probe",
        source_spec_id=spec.spec_id,
        source_rule_id=rule.rule_id,
        shared_window_start=rule.shared_window_start,
        shared_window_end=rule.shared_window_end,
        overall_verdict=overall_verdict,
        family_results=family_results,
        bridge_boundary=rule.bridge_boundary,
        recommendation=recommendation,
    )


def render_baseline_odd_residual_refinement_probe() -> str:
    probe = build_baseline_odd_residual_refinement_probe()
    lines = [
        "# Phase 2 baseline odd residual refinement probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source spec: `{BASELINE_ODD_RESIDUAL_REFINEMENT_SPEC_REPORT_PATH}`",
        f"- Source spec id: `{probe.source_spec_id}`",
        f"- Source extraction rule id: `{probe.source_rule_id}`",
        f"- Shared exact window: `n={probe.shared_window_start}..{probe.shared_window_end}`",
        f"- Overall verdict: `{probe.overall_verdict}`",
        "",
        "## Family results",
        "",
    ]
    for family in probe.family_results:
        mismatch_text = (
            ", ".join(str(value) for value in family.mismatch_indices)
            if family.mismatch_indices
            else "none"
        )
        coefficient_text = ", ".join(
            f"{item.label}={item.value}" for item in family.coefficients
        )
        lines.extend(
            [
                f"### `{family.family_id}`",
                "",
                f"- Label: {family.family_label}",
                f"- Statement: `{family.family_statement}`",
                f"- Fit window: `n={family.fit_window_start}..{family.fit_window_end}`",
                f"- Validation window: `n={family.validation_window_start}..{family.validation_window_end}`",
                f"- Coefficients: {coefficient_text}",
                f"- Verdict: `{family.verdict}`",
                f"- Transformed residual hash: `{family.transformed_residual_hash}`",
                f"- Zero count: `{family.zero_count}`",
                f"- First mismatch index: `{family.first_mismatch_index}`",
                f"- Mismatch indices: {mismatch_text}",
                "",
                "| n | transformed residual |",
                "| --- | --- |",
            ]
        )
        for sample in family.first_samples:
            lines.append(f"| `{sample.n}` | `{sample.value}` |")
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


def write_baseline_odd_residual_refinement_probe_report(
    output_path: str | Path = BASELINE_ODD_RESIDUAL_REFINEMENT_PROBE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_odd_residual_refinement_probe(), encoding="utf-8")
    return output


def write_baseline_odd_residual_refinement_probe_json(
    output_path: str | Path = BASELINE_ODD_RESIDUAL_REFINEMENT_PROBE_JSON_PATH,
) -> Path:
    probe = build_baseline_odd_residual_refinement_probe()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(probe), indent=2, sort_keys=True), encoding="utf-8")
    return output


def _load_baseline_terms(max_n: int) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...], tuple[Fraction, ...]]:
    zeta5_terms = tuple(Fraction(value) for value in get_cached_baseline_dual_f7_zeta5_terms(max_n))
    zeta3_terms = get_cached_baseline_dual_f7_exact_component_terms(max_n, component="zeta3")
    constant_terms = get_cached_baseline_dual_f7_exact_component_terms(max_n, component="constant")
    return zeta5_terms, zeta3_terms, constant_terms


def _evaluate_family(
    *,
    family_spec: BaselineOddResidualRefinementFamilySpec,
    zeta5_terms: tuple[Fraction, ...],
    zeta3_terms: tuple[Fraction, ...],
    constant_terms: tuple[Fraction, ...],
) -> BaselineOddResidualRefinementFamilyResult:
    rows = _build_augmented_rows(
        family_spec=family_spec,
        zeta5_terms=zeta5_terms,
        zeta3_terms=zeta3_terms,
        constant_terms=constant_terms,
    )
    solution = _solve_exact_linear_system(rows)
    if solution is None:
        coefficients = tuple(
            BaselineOddResidualRefinementCoefficient(label=label, value="unsolved")
            for label in family_spec.coefficient_labels
        )
        return BaselineOddResidualRefinementFamilyResult(
            family_id=family_spec.family_id,
            family_label=family_spec.family_label,
            fit_window_start=family_spec.fit_window_start,
            fit_window_end=family_spec.fit_window_end,
            validation_window_start=family_spec.validation_window_start,
            validation_window_end=family_spec.validation_window_end,
            family_statement=family_spec.family_statement,
            coefficients=coefficients,
            transformed_residual_hash=compute_sequence_hash(
                provisional_signature={
                    "family_id": family_spec.family_id,
                    "kind": "baseline_odd_residual_refinement_ill_posed",
                    "fit_window_start": family_spec.fit_window_start,
                    "fit_window_end": family_spec.fit_window_end,
                    "validation_window_start": family_spec.validation_window_start,
                    "validation_window_end": family_spec.validation_window_end,
                }
            ),
            verdict="ill_posed",
            zero_count=0,
            mismatch_indices=(),
            first_mismatch_index=None,
            first_samples=(),
        )
    transformed_residuals = tuple(
        _compute_transformed_residual(
            family_id=family_spec.family_id,
            n=n,
            coefficients=solution,
            zeta5_terms=zeta5_terms,
            zeta3_terms=zeta3_terms,
            constant_terms=constant_terms,
        )
        for n in range(family_spec.validation_window_start, family_spec.validation_window_end + 1)
    )
    mismatch_indices = tuple(
        n
        for n, value in zip(
            range(family_spec.validation_window_start, family_spec.validation_window_end + 1),
            transformed_residuals,
        )
        if value != 0
    )
    transformed_residual_hash = compute_sequence_hash(
        provisional_signature={
            "kind": "baseline_odd_residual_refinement_family",
            "family_id": family_spec.family_id,
            "fit_window_start": family_spec.fit_window_start,
            "fit_window_end": family_spec.fit_window_end,
            "validation_window_start": family_spec.validation_window_start,
            "validation_window_end": family_spec.validation_window_end,
            "coefficients": {
                label: fraction_to_canonical_string(value)
                for label, value in zip(family_spec.coefficient_labels, solution)
            },
            "terms": [fraction_to_canonical_string(value) for value in transformed_residuals],
        }
    )
    coefficients = tuple(
        BaselineOddResidualRefinementCoefficient(
            label=label,
            value=fraction_to_canonical_string(value),
        )
        for label, value in zip(family_spec.coefficient_labels, solution)
    )
    first_samples = tuple(
        BaselineOddResidualSample(
            n=n,
            value=fraction_to_canonical_string(value),
        )
        for n, value in list(
            zip(
                range(family_spec.validation_window_start, family_spec.validation_window_end + 1),
                transformed_residuals,
            )
        )[:3]
    )
    verdict = "holds_on_full_window" if not mismatch_indices else "fails_after_fit_window"
    return BaselineOddResidualRefinementFamilyResult(
        family_id=family_spec.family_id,
        family_label=family_spec.family_label,
        fit_window_start=family_spec.fit_window_start,
        fit_window_end=family_spec.fit_window_end,
        validation_window_start=family_spec.validation_window_start,
        validation_window_end=family_spec.validation_window_end,
        family_statement=family_spec.family_statement,
        coefficients=coefficients,
        transformed_residual_hash=transformed_residual_hash,
        verdict=verdict,
        zero_count=sum(1 for value in transformed_residuals if value == 0),
        mismatch_indices=mismatch_indices,
        first_mismatch_index=mismatch_indices[0] if mismatch_indices else None,
        first_samples=first_samples,
    )


def _build_augmented_rows(
    *,
    family_spec: BaselineOddResidualRefinementFamilySpec,
    zeta5_terms: tuple[Fraction, ...],
    zeta3_terms: tuple[Fraction, ...],
    constant_terms: tuple[Fraction, ...],
) -> tuple[tuple[Fraction, ...], ...]:
    rows: list[tuple[Fraction, ...]] = []
    for n in range(family_spec.fit_window_start, family_spec.fit_window_end + 1):
        if family_spec.family_id == "support0_same_index":
            rows.append(
                (
                    zeta3_terms[n - 1],
                    zeta5_terms[n - 1],
                    -constant_terms[n - 1],
                )
            )
        elif family_spec.family_id == "difference_pair":
            rows.append(
                (
                    zeta3_terms[n - 1] - zeta3_terms[n - 2],
                    zeta5_terms[n - 1] - zeta5_terms[n - 2],
                    -constant_terms[n - 1],
                )
            )
        elif family_spec.family_id == "support1_lagged_pair":
            rows.append(
                (
                    zeta3_terms[n - 1],
                    zeta3_terms[n - 2],
                    zeta5_terms[n - 1],
                    zeta5_terms[n - 2],
                    -constant_terms[n - 1],
                )
            )
        else:
            raise ValueError(f"unsupported odd residual-refinement family {family_spec.family_id!r}")
    return tuple(rows)


def _compute_transformed_residual(
    *,
    family_id: str,
    n: int,
    coefficients: tuple[Fraction, ...],
    zeta5_terms: tuple[Fraction, ...],
    zeta3_terms: tuple[Fraction, ...],
    constant_terms: tuple[Fraction, ...],
) -> Fraction:
    if family_id == "support0_same_index":
        a, b = coefficients
        return constant_terms[n - 1] + a * zeta3_terms[n - 1] + b * zeta5_terms[n - 1]
    if family_id == "difference_pair":
        a, b = coefficients
        return constant_terms[n - 1] + a * (zeta3_terms[n - 1] - zeta3_terms[n - 2]) + b * (
            zeta5_terms[n - 1] - zeta5_terms[n - 2]
        )
    if family_id == "support1_lagged_pair":
        a0, a1, b0, b1 = coefficients
        return (
            constant_terms[n - 1]
            + a0 * zeta3_terms[n - 1]
            + a1 * zeta3_terms[n - 2]
            + b0 * zeta5_terms[n - 1]
            + b1 * zeta5_terms[n - 2]
        )
    raise ValueError(f"unsupported odd residual-refinement family {family_id!r}")


def _solve_exact_linear_system(rows: tuple[tuple[Fraction, ...], ...]) -> tuple[Fraction, ...] | None:
    if not rows:
        return None
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
    write_baseline_odd_residual_refinement_probe_report()
    write_baseline_odd_residual_refinement_probe_json()


if __name__ == "__main__":
    main()
