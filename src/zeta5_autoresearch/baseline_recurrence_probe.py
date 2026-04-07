from __future__ import annotations

from dataclasses import dataclass
from math import floor, log10
from pathlib import Path
from time import perf_counter

from .baseline_q_cache import get_cached_baseline_q_terms_as_fractions
from .config import DATA_DIR
from .recurrence_mining import RecurrenceSearchResult, search_polynomial_recurrences

DEFAULT_BASELINE_RECURRENCE_REPORT_PATH = DATA_DIR / "logs" / "bz_baseline_recurrence_report.md"


@dataclass(frozen=True)
class BaselineRecurrenceProbe:
    max_n: int
    shifts: tuple[int, ...]
    degree_min: int
    degree_max: int
    term_compute_seconds: float
    search_seconds: float
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


def build_baseline_recurrence_probe(
    *,
    max_n: int = 34,
    degree_min: int = 0,
    degree_max: int = 8,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
) -> BaselineRecurrenceProbe:
    if max_n < 4:
        raise ValueError("max_n must be at least 4")

    term_start = perf_counter()
    sequence = get_cached_baseline_q_terms_as_fractions(max_n)
    term_compute_seconds = perf_counter() - term_start

    search_start = perf_counter()
    results = search_polynomial_recurrences(
        sequence,
        shifts=shifts,
        degree_min=degree_min,
        degree_max=degree_max,
    )
    search_seconds = perf_counter() - search_start

    return BaselineRecurrenceProbe(
        max_n=max_n,
        shifts=shifts,
        degree_min=degree_min,
        degree_max=degree_max,
        term_compute_seconds=term_compute_seconds,
        search_seconds=search_seconds,
        results=results,
    )


def render_baseline_recurrence_report(
    *,
    max_n: int = 34,
    degree_min: int = 0,
    degree_max: int = 8,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
) -> str:
    probe = build_baseline_recurrence_probe(
        max_n=max_n,
        degree_min=degree_min,
        degree_max=degree_max,
        shifts=shifts,
    )

    lines = [
        "# Brown-Zudilin baseline recurrence search",
        "",
        f"- Exact baseline `Q_n` terms computed through `n={probe.max_n}` from the published double-sum formula.",
        f"- Search family: consecutive-shift order-3 polynomial recurrences with shifts `{probe.shifts}`.",
        f"- Degree scan: `{probe.degree_min}` through `{probe.degree_max}`.",
        f"- Term generation time: `{probe.term_compute_seconds:.3f}s`.",
        f"- Linear-algebra search time: `{probe.search_seconds:.3f}s`.",
    ]
    if probe.first_compatible_degree is None:
        lines.append(
            f"- Result: no nontrivial recurrence of this shape was found through degree `{probe.degree_max}` on the exact window."
        )
    else:
        lines.append(
            f"- Exact lower bound on the compatible degree over this window: no solution through degree `{probe.exact_no_solution_degree_cap}`."
        )
        lines.append(
            f"- First compatible degree on the exact window: `{probe.first_compatible_degree}`."
        )
        lines.append(
            "- Interpretation: this is a finite-window exact search result, not yet a verified recurrence for the baseline sequence."
        )

    lines.extend(
        (
            "",
            "| degree | equations | variables | rank | nullity | first basis max digits |",
            "| --- | --- | --- | --- | --- | --- |",
        )
    )
    for result in probe.results:
        first_height = "" if not result.basis else str(_decimal_digits(result.basis[0].coefficient_height))
        lines.append(
            f"| {result.degree} | {result.equation_count} | {result.variable_count} | {result.rank} | {result.nullity} | {first_height} |"
        )

    first = next((result for result in probe.results if result.has_nontrivial_solution and result.basis), None)
    if first is not None:
        lines.extend(
            (
                "",
                f"## First Compatible Basis Sample",
                "",
                f"- Degree: `{first.degree}`",
                f"- Maximum coefficient size: about `{_decimal_digits(first.basis[0].coefficient_height)}` decimal digits",
            )
        )
        for relation in first.basis[0].relations:
            lines.append(f"- Shift `{relation.shift}` summary: `{_relation_summary(relation.coefficients)}`")

    return "\n".join(lines) + "\n"


def write_baseline_recurrence_report(
    *,
    max_n: int = 34,
    degree_min: int = 0,
    degree_max: int = 8,
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_BASELINE_RECURRENCE_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_baseline_recurrence_report(
            max_n=max_n,
            degree_min=degree_min,
            degree_max=degree_max,
            shifts=shifts,
        ),
        encoding="utf-8",
    )
    return output

def _decimal_digits(value: int) -> int:
    absolute = abs(value)
    if absolute == 0:
        return 1
    return floor((absolute.bit_length() - 1) * log10(2)) + 1


def _relation_summary(coefficients: tuple[int, ...]) -> str:
    degrees = len(coefficients) - 1
    max_digits = max(_decimal_digits(value) for value in coefficients)
    nonzero = sum(1 for value in coefficients if value != 0)
    return f"degree={degrees}, nonzero_coeffs={nonzero}, max_digits~{max_digits}"
