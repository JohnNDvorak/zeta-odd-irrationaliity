from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import mpmath

from .bz_dual_f7 import dual_b_vector_from_a, scale_b_vector
from .bz_q_sequence import baseline_a_vector, totally_symmetric_a_vector
from .config import DATA_DIR
from .dual_f7_exact_coefficient_cache import (
    get_cached_baseline_dual_f7_exact_component_terms,
    get_cached_symmetric_dual_f7_exact_component_terms,
)
from .gate2.sequence_identity import ProvisionalSequenceIdentity, compute_provisional_sequence_hash
from .models import fraction_to_canonical_string

DEFAULT_DUAL_F7_COMPANION_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_companion_probe_report.md"
DEFAULT_DUAL_F7_COMPANION_COMPONENTS = ("constant", "zeta3")


@dataclass(frozen=True)
class DualF7CompanionSample:
    n: int
    b0: int
    value: Fraction
    numerator_digits: int
    denominator_digits: int
    log10_abs_value: float | None


@dataclass(frozen=True)
class DualF7CompanionComponentProbe:
    component: str
    component_label: str
    sequence_hash: str
    samples: tuple[DualF7CompanionSample, ...]


@dataclass(frozen=True)
class DualF7CompanionCaseProbe:
    id: str
    label: str
    a: tuple[int, ...]
    base_b: tuple[int, ...]
    components: tuple[DualF7CompanionComponentProbe, ...]


@dataclass(frozen=True)
class BZDualF7CompanionProbe:
    report_id: str
    source_title: str
    source_url: str
    source_version: str
    source_notes: str
    cases: tuple[DualF7CompanionCaseProbe, ...]


def build_bz_dual_f7_companion_probe(
    *,
    components: tuple[str, ...] = DEFAULT_DUAL_F7_COMPANION_COMPONENTS,
    symmetric_term_count: int = 4,
    baseline_term_count: int = 6,
    start_index: int = 1,
) -> BZDualF7CompanionProbe:
    if not components:
        raise ValueError("components must be non-empty")
    if start_index <= 0:
        raise ValueError("start_index must be positive")
    if symmetric_term_count <= 0 or baseline_term_count <= 0:
        raise ValueError("term counts must be positive")

    cases = [
        _build_case_probe(
            case_id="totally_symmetric",
            label="Totally symmetric dual companion sequences",
            a=totally_symmetric_a_vector(),
            components=components,
            start_index=start_index,
            term_count=symmetric_term_count,
        ),
        _build_case_probe(
            case_id="baseline_bz",
            label="Brown-Zudilin baseline dual companion sequences",
            a=baseline_a_vector(),
            components=components,
            start_index=start_index,
            term_count=baseline_term_count,
        ),
    ]
    return BZDualF7CompanionProbe(
        report_id="bz_dual_f7_companion_probe_v1",
        source_title="Brown and Zudilin, On cellular rational approximations to zeta(5)",
        source_url="https://arxiv.org/abs/2210.03391",
        source_version="v3",
        source_notes=(
            "The exact dual F_7 linear-form extractor already determines the rational constant term and the zeta(3) "
            "coefficient. This probe promotes those companion exact sequences into cached sequence objects alongside the "
            "existing exact dual zeta(5) sequence."
        ),
        cases=tuple(cases),
    )


def render_bz_dual_f7_companion_probe_report(
    *,
    components: tuple[str, ...] = DEFAULT_DUAL_F7_COMPANION_COMPONENTS,
    symmetric_term_count: int = 4,
    baseline_term_count: int = 6,
    start_index: int = 1,
) -> str:
    probe = build_bz_dual_f7_companion_probe(
        components=components,
        symmetric_term_count=symmetric_term_count,
        baseline_term_count=baseline_term_count,
        start_index=start_index,
    )
    lines = [
        "# Brown-Zudilin dual F_7 companion exact-coefficient probe",
        "",
        f"- Report id: `{probe.report_id}`",
        f"- Source: `{probe.source_title}` ({probe.source_url})",
        f"- Source version: `{probe.source_version}`",
        "- This report tracks the missing exact companion sequences attached to the dual `F_7` linear form: the rational constant term and the exact `zeta(3)` coefficient.",
        "- Each component is hashed as a provisional exact-term sequence object. No recurrence is claimed here.",
        "",
    ]
    for case in probe.cases:
        lines.extend(
            [
                f"## {case.label}",
                "",
                f"- Case id: `{case.id}`",
                f"- Base `a`: `{case.a}`",
                f"- Base `b`: `{case.base_b}`",
                "",
            ]
        )
        for component_probe in case.components:
            signature = [fraction_to_canonical_string(sample.value) for sample in component_probe.samples]
            lines.extend(
                [
                    f"### {component_probe.component_label}",
                    "",
                    f"- Provisional sequence hash: `{component_probe.sequence_hash}`",
                    f"- Exact signature: `{signature}`",
                    "",
                    "| n | scaled b0 | numerator digits | denominator digits | log10|term| | term preview |",
                    "| --- | --- | --- | --- | --- | --- |",
                ]
            )
            for sample in component_probe.samples:
                log10_abs = "" if sample.log10_abs_value is None else f"{sample.log10_abs_value:.6f}"
                lines.append(
                    "| "
                    + " | ".join(
                        (
                            str(sample.n),
                            str(sample.b0),
                            str(sample.numerator_digits),
                            str(sample.denominator_digits),
                            log10_abs,
                            _preview_fraction(sample.value),
                        )
                    )
                    + " |"
                )
            lines.append("")
    return "\n".join(lines) + "\n"


def write_bz_dual_f7_companion_probe_report(
    *,
    components: tuple[str, ...] = DEFAULT_DUAL_F7_COMPANION_COMPONENTS,
    symmetric_term_count: int = 4,
    baseline_term_count: int = 6,
    start_index: int = 1,
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_DUAL_F7_COMPANION_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_bz_dual_f7_companion_probe_report(
            components=components,
            symmetric_term_count=symmetric_term_count,
            baseline_term_count=baseline_term_count,
            start_index=start_index,
        ),
        encoding="utf-8",
    )
    return output


def _build_case_probe(
    *,
    case_id: str,
    label: str,
    a: tuple[int, ...],
    components: tuple[str, ...],
    start_index: int,
    term_count: int,
) -> DualF7CompanionCaseProbe:
    base_b = dual_b_vector_from_a(a)
    component_probes = []
    for component in components:
        terms = _get_terms_for_case(case_id, component, max_n=start_index + term_count - 1)
        signature = terms[start_index - 1 : start_index - 1 + term_count]
        provisional = ProvisionalSequenceIdentity.from_scalars(
            start_index=start_index,
            order_bound=max(1, len(signature) - 1),
            initial_data=signature[: min(2, len(signature))],
            signature=signature,
        )
        samples = []
        for offset, value in enumerate(signature):
            n = start_index + offset
            scaled_b = scale_b_vector(base_b, n)
            samples.append(
                DualF7CompanionSample(
                    n=n,
                    b0=scaled_b[0],
                    value=value,
                    numerator_digits=len(str(abs(value.numerator))),
                    denominator_digits=len(str(value.denominator)),
                    log10_abs_value=_log10_abs_fraction(value),
                )
            )
        component_probes.append(
            DualF7CompanionComponentProbe(
                component=component,
                component_label=_component_label(component),
                sequence_hash=compute_provisional_sequence_hash(provisional),
                samples=tuple(samples),
            )
        )
    return DualF7CompanionCaseProbe(
        id=case_id,
        label=label,
        a=a,
        base_b=base_b,
        components=tuple(component_probes),
    )


def _get_terms_for_case(case_id: str, component: str, *, max_n: int) -> tuple[Fraction, ...]:
    if case_id == "baseline_bz":
        return get_cached_baseline_dual_f7_exact_component_terms(max_n, component=component)
    return get_cached_symmetric_dual_f7_exact_component_terms(max_n, component=component)


def _component_label(component: str) -> str:
    if component == "constant":
        return "Constant Sequence"
    if component == "zeta3":
        return "zeta(3) Coefficient Sequence"
    return component


def _log10_abs_fraction(value: Fraction) -> float | None:
    if value == 0:
        return None
    with mpmath.workdps(50):
        return float(mpmath.log10(abs(mpmath.mpf(value.numerator) / value.denominator)))


def _preview_fraction(value: Fraction, *, edge_digits: int = 10) -> str:
    text = fraction_to_canonical_string(value)
    if len(text) <= 2 * edge_digits + 3:
        return text
    return f"{text[:edge_digits]}...{text[-edge_digits:]}"
