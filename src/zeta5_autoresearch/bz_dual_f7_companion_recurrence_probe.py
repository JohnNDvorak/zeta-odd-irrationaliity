from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from .config import DATA_DIR
from .dual_f7_exact_coefficient_cache import (
    get_cached_baseline_dual_f7_companion_terms,
)
from .recurrence_mining import RecurrenceSearchResult, search_polynomial_recurrences

DEFAULT_DUAL_F7_COMPANION_RECURRENCE_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_companion_recurrence_report.md"


@dataclass(frozen=True)
class DualF7CompanionRecurrenceComponentProbe:
    component: str
    component_label: str
    results: tuple[RecurrenceSearchResult, ...]

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
class BZDualF7CompanionRecurrenceProbe:
    max_n: int
    shifts: tuple[int, ...]
    degree_min: int
    degree_max: int
    term_compute_seconds: float
    search_seconds: float
    components: tuple[DualF7CompanionRecurrenceComponentProbe, ...]


def build_bz_dual_f7_companion_recurrence_probe(
    *,
    max_n: int = 12,
    degree_min: int = 0,
    degree_max: int = 2,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
) -> BZDualF7CompanionRecurrenceProbe:
    if max_n < 4:
        raise ValueError("max_n must be at least 4")

    term_start = perf_counter()
    constant_terms, zeta3_terms = get_cached_baseline_dual_f7_companion_terms(max_n)
    component_sequences = (
        ("constant", "Constant Sequence", constant_terms),
        ("zeta3", "zeta(3) Coefficient Sequence", zeta3_terms),
    )
    term_compute_seconds = perf_counter() - term_start

    search_start = perf_counter()
    components = []
    for component, component_label, sequence in component_sequences:
        components.append(
            DualF7CompanionRecurrenceComponentProbe(
                component=component,
                component_label=component_label,
                results=search_polynomial_recurrences(
                    sequence,
                    shifts=shifts,
                    degree_min=degree_min,
                    degree_max=degree_max,
                ),
            )
        )
    search_seconds = perf_counter() - search_start

    return BZDualF7CompanionRecurrenceProbe(
        max_n=max_n,
        shifts=shifts,
        degree_min=degree_min,
        degree_max=degree_max,
        term_compute_seconds=term_compute_seconds,
        search_seconds=search_seconds,
        components=tuple(components),
    )


def render_bz_dual_f7_companion_recurrence_report(
    *,
    max_n: int = 12,
    degree_min: int = 0,
    degree_max: int = 2,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
) -> str:
    probe = build_bz_dual_f7_companion_recurrence_probe(
        max_n=max_n,
        degree_min=degree_min,
        degree_max=degree_max,
        shifts=shifts,
    )

    lines = [
        "# Brown-Zudilin dual F_7 companion exact-sequence recurrence probe",
        "",
        f"- Exact baseline companion sequences computed through `n={probe.max_n}`.",
        f"- Search family: polynomial recurrences supported on shifts `{probe.shifts}`.",
        f"- Degree scan: `{probe.degree_min}` through `{probe.degree_max}`.",
        f"- Exact term generation time: `{probe.term_compute_seconds:.3f}s`.",
        f"- Exact linear-algebra time: `{probe.search_seconds:.3f}s`.",
        "- Interpretation: this is a finite-window exact search on the baseline dual constant and zeta(3) coefficient sequences, not a certified global recurrence.",
        "",
    ]
    for component in probe.components:
        lines.extend(
            [
                f"## {component.component_label}",
                "",
            ]
        )
        if component.first_compatible_degree is None:
            lines.append(
                f"- Result: no nontrivial recurrence of this shape was found through degree `{probe.degree_max}` on the exact window."
            )
        else:
            lines.append(
                f"- Exact no-solution cap on this window: `{component.exact_no_solution_degree_cap}`."
            )
            lines.append(
                f"- First compatible degree on this window: `{component.first_compatible_degree}`."
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


def write_bz_dual_f7_companion_recurrence_report(
    *,
    max_n: int = 12,
    degree_min: int = 0,
    degree_max: int = 2,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_DUAL_F7_COMPANION_RECURRENCE_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_bz_dual_f7_companion_recurrence_report(
            max_n=max_n,
            degree_min=degree_min,
            degree_max=degree_max,
            shifts=shifts,
        ),
        encoding="utf-8",
    )
    return output
