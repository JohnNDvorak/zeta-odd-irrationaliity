from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd, log10
from pathlib import Path
from time import perf_counter

from .config import DATA_DIR
from .dual_f7_exact_coefficient_cache import (
    get_cached_baseline_dual_f7_companion_terms,
)
from .recurrence_mining import RecurrenceSearchResult, search_polynomial_recurrences

DEFAULT_DUAL_F7_COMPANION_NORMALIZATION_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_companion_normalization_report.md"


@dataclass(frozen=True)
class DualF7CompanionNormalizationComponentProbe:
    component: str
    component_label: str
    denominator_digits: tuple[int, ...]
    window_scale: int
    cleared_terms: tuple[int, ...]
    results: tuple[RecurrenceSearchResult, ...]

    @property
    def window_scale_digits(self) -> int:
        return _decimal_digit_count(self.window_scale)

    @property
    def exact_no_solution_degree_cap(self) -> int | None:
        cap = None
        for result in self.results:
            if result.has_nontrivial_solution:
                break
            cap = result.degree
        return cap

    @property
    def first_compatible_degree(self) -> int | None:
        for result in self.results:
            if result.has_nontrivial_solution:
                return result.degree
        return None


@dataclass(frozen=True)
class BZDualF7CompanionNormalizationProbe:
    max_n: int
    shifts: tuple[int, ...]
    degree_min: int
    degree_max: int
    term_compute_seconds: float
    normalize_seconds: float
    search_seconds: float
    components: tuple[DualF7CompanionNormalizationComponentProbe, ...]


def build_bz_dual_f7_companion_normalization_probe(
    *,
    max_n: int = 20,
    degree_min: int = 0,
    degree_max: int = 4,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
) -> BZDualF7CompanionNormalizationProbe:
    if max_n < 4:
        raise ValueError("max_n must be at least 4")

    term_start = perf_counter()
    constant_terms, zeta3_terms = get_cached_baseline_dual_f7_companion_terms(max_n)
    component_sequences = (
        ("constant", "Constant Sequence", constant_terms),
        ("zeta3", "zeta(3) Coefficient Sequence", zeta3_terms),
    )
    term_compute_seconds = perf_counter() - term_start

    normalize_start = perf_counter()
    normalized_components = []
    for component, component_label, sequence in component_sequences:
        window_scale = 1
        for term in sequence:
            window_scale = _lcm(window_scale, term.denominator)
        cleared_terms = tuple(int((term * window_scale).numerator) for term in sequence)
        normalized_components.append(
            (
                component,
                component_label,
                tuple(_decimal_digit_count(term.denominator) for term in sequence),
                window_scale,
                cleared_terms,
            )
        )
    normalize_seconds = perf_counter() - normalize_start

    search_start = perf_counter()
    components = []
    for component, component_label, denominator_digits, window_scale, cleared_terms in normalized_components:
        components.append(
            DualF7CompanionNormalizationComponentProbe(
                component=component,
                component_label=component_label,
                denominator_digits=denominator_digits,
                window_scale=window_scale,
                cleared_terms=cleared_terms,
                results=search_polynomial_recurrences(
                    tuple(Fraction(value) for value in cleared_terms),
                    shifts=shifts,
                    degree_min=degree_min,
                    degree_max=degree_max,
                ),
            )
        )
    search_seconds = perf_counter() - search_start

    return BZDualF7CompanionNormalizationProbe(
        max_n=max_n,
        shifts=shifts,
        degree_min=degree_min,
        degree_max=degree_max,
        term_compute_seconds=term_compute_seconds,
        normalize_seconds=normalize_seconds,
        search_seconds=search_seconds,
        components=tuple(components),
    )


def render_bz_dual_f7_companion_normalization_report(
    *,
    max_n: int = 20,
    degree_min: int = 0,
    degree_max: int = 4,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
) -> str:
    probe = build_bz_dual_f7_companion_normalization_probe(
        max_n=max_n,
        degree_min=degree_min,
        degree_max=degree_max,
        shifts=shifts,
    )

    lines = [
        "# Brown-Zudilin dual F_7 companion normalization probe",
        "",
        f"- Exact baseline companion sequences loaded through `n={probe.max_n}`.",
        "- For each component, the report forms the exact minimal common denominator across the finite window and clears the window to integers.",
        f"- Search family on the cleared windows: polynomial recurrences supported on shifts `{probe.shifts}`.",
        f"- Degree scan on cleared windows: `{probe.degree_min}` through `{probe.degree_max}`.",
        f"- Exact term loading time: `{probe.term_compute_seconds:.3f}s`.",
        f"- Window normalization time: `{probe.normalize_seconds:.3f}s`.",
        f"- Exact recurrence scan time on cleared windows: `{probe.search_seconds:.3f}s`.",
        "",
    ]
    for component in probe.components:
        lines.extend(
            [
                f"## {component.component_label}",
                "",
                f"- Window common denominator digits: `{component.window_scale_digits}`",
                f"- First six denominator-digit counts: `{list(component.denominator_digits[:6])}`",
                f"- Cleared-term digit count at `n={probe.max_n}`: `{_decimal_digit_count(component.cleared_terms[-1])}`",
            ]
        )
        if component.first_compatible_degree is None:
            lines.append(
                f"- Cleared-window consequence: no nontrivial recurrence of this shape was found through degree `{probe.degree_max}`."
            )
        else:
            lines.append(
                f"- Cleared-window no-solution cap: `{component.exact_no_solution_degree_cap}`."
            )
            lines.append(
                f"- First compatible cleared-window degree: `{component.first_compatible_degree}`."
            )
        lines.extend(
            (
                "",
                "| degree | equations | variables | rank | nullity |",
                "| --- | --- | --- | --- | --- |",
            )
        )
        for result in component.results:
            lines.append(
                f"| {result.degree} | {result.equation_count} | {result.variable_count} | {result.rank} | {result.nullity} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def write_bz_dual_f7_companion_normalization_report(
    *,
    max_n: int = 20,
    degree_min: int = 0,
    degree_max: int = 4,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_DUAL_F7_COMPANION_NORMALIZATION_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_bz_dual_f7_companion_normalization_report(
            max_n=max_n,
            degree_min=degree_min,
            degree_max=degree_max,
            shifts=shifts,
        ),
        encoding="utf-8",
    )
    return output


def _lcm(left: int, right: int) -> int:
    return abs(left * right) // gcd(left, right)


def _decimal_digit_count(value: int) -> int:
    value = abs(value)
    if value == 0:
        return 1

    digits = int((value.bit_length() - 1) * log10(2)) + 1
    threshold = 10**digits
    if value >= threshold:
        while value >= threshold:
            digits += 1
            threshold *= 10
        return digits

    while value < 10 ** (digits - 1):
        digits -= 1
    return digits
