from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from .baseline_q_cache import get_cached_baseline_q_terms_mod_prime
from .config import DATA_DIR
from .recurrence_mining import ModularRankCertificate, modular_rank_certificate

DEFAULT_BASELINE_MODULAR_REPORT_PATH = DATA_DIR / "logs" / "bz_baseline_modular_recurrence_report.md"
DEFAULT_MODULI = (1000003, 1000033, 1000037)


@dataclass(frozen=True)
class BaselineModularDegreeSummary:
    degree: int
    certificates: tuple[ModularRankCertificate, ...]

    @property
    def certifies_no_solution(self) -> bool:
        return any(certificate.certifies_no_solution for certificate in self.certificates)

    @property
    def best_rank(self) -> int:
        return max(certificate.rank for certificate in self.certificates)

    @property
    def variable_count(self) -> int:
        return self.certificates[0].variable_count

    @property
    def best_nullity_upper_bound(self) -> int:
        return self.variable_count - self.best_rank

    @property
    def certifying_modulus(self) -> int | None:
        for certificate in self.certificates:
            if certificate.certifies_no_solution:
                return certificate.modulus
        return None


@dataclass(frozen=True)
class BaselineModularRecurrenceProbe:
    max_n: int
    shifts: tuple[int, ...]
    moduli: tuple[int, ...]
    degrees: tuple[int, ...]
    sequence_source: str
    term_compute_seconds: float
    search_seconds: float
    summaries: tuple[BaselineModularDegreeSummary, ...]

    @property
    def certified_degree_cap(self) -> int | None:
        cap = None
        for summary in self.summaries:
            if summary.certifies_no_solution:
                cap = summary.degree
            else:
                break
        return cap

    @property
    def first_uncertified_degree(self) -> int | None:
        for summary in self.summaries:
            if not summary.certifies_no_solution:
                return summary.degree
        return None


def build_baseline_modular_recurrence_probe(
    *,
    max_n: int = 38,
    degrees: tuple[int, ...] = (8, 9),
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    moduli: tuple[int, ...] = DEFAULT_MODULI,
    sequences_by_modulus: dict[int, tuple[int, ...]] | None = None,
) -> BaselineModularRecurrenceProbe:
    if max_n < 4:
        raise ValueError("max_n must be at least 4")
    if not degrees:
        raise ValueError("degrees must be non-empty")

    term_start = perf_counter()
    if sequences_by_modulus is None:
        sequences = {
            modulus: get_cached_baseline_q_terms_mod_prime(max_n, modulus=modulus)
            for modulus in moduli
        }
        sequence_source = "modular_double_sum_cache"
    else:
        sequences = {}
        for modulus in moduli:
            sequence = sequences_by_modulus.get(modulus)
            if sequence is None:
                raise ValueError(f"missing precomputed modular sequence for modulus {modulus}")
            if len(sequence) <= max_n:
                raise ValueError(f"precomputed modular sequence for modulus {modulus} does not reach n={max_n}")
            sequences[modulus] = sequence
        sequence_source = "precomputed_modular_sequences"
    term_compute_seconds = perf_counter() - term_start

    search_start = perf_counter()
    summaries = []
    for degree in degrees:
        certificates = tuple(
            modular_rank_certificate(
                sequences[modulus],
                degree=degree,
                modulus=modulus,
                shifts=shifts,
            )
            for modulus in moduli
        )
        summaries.append(BaselineModularDegreeSummary(degree=degree, certificates=certificates))
    search_seconds = perf_counter() - search_start

    return BaselineModularRecurrenceProbe(
        max_n=max_n,
        shifts=shifts,
        moduli=moduli,
        degrees=degrees,
        sequence_source=sequence_source,
        term_compute_seconds=term_compute_seconds,
        search_seconds=search_seconds,
        summaries=tuple(summaries),
    )


def render_baseline_modular_recurrence_report(
    *,
    max_n: int = 38,
    degrees: tuple[int, ...] = (8, 9),
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    moduli: tuple[int, ...] = DEFAULT_MODULI,
) -> str:
    probe = build_baseline_modular_recurrence_probe(
        max_n=max_n,
        degrees=degrees,
        shifts=shifts,
        moduli=moduli,
    )

    lines = [
        "# Brown-Zudilin baseline modular recurrence certificates",
        "",
        f"- Baseline `Q_n mod p` values computed directly from the published double-sum formula through `n={probe.max_n}`.",
        f"- Search family: polynomial recurrences supported on shifts `{probe.shifts}`.",
        f"- Modular certificate primes: `{probe.moduli}`.",
        f"- Sequence source: `{probe.sequence_source}`.",
        f"- Modular sequence generation time: `{probe.term_compute_seconds:.3f}s`.",
        f"- Modular rank scan time: `{probe.search_seconds:.3f}s`.",
    ]
    if probe.certified_degree_cap is not None:
        lines.append(
            f"- Certified consequence: no rational recurrence of this shape exists through degree `{probe.certified_degree_cap}`."
        )
    if probe.first_uncertified_degree is not None:
        lines.append(
            f"- First unresolved degree in this scan: `{probe.first_uncertified_degree}`."
        )
    lines.append(
        "- Logic: if one prime gives full column rank, the same degree is impossible over `Q`."
    )
    lines.extend(
        (
            "",
            "| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        )
    )
    for summary in probe.summaries:
        for certificate in summary.certificates:
            lines.append(
                f"| {summary.degree} | {certificate.modulus} | {certificate.equation_count} | {certificate.variable_count} | {certificate.rank} | {certificate.nullity_upper_bound} | {'yes' if certificate.certifies_no_solution else 'no'} |"
            )
    return "\n".join(lines) + "\n"


def write_baseline_modular_recurrence_report(
    *,
    max_n: int = 38,
    degrees: tuple[int, ...] = (8, 9),
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    moduli: tuple[int, ...] = DEFAULT_MODULI,
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_BASELINE_MODULAR_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_baseline_modular_recurrence_report(
            max_n=max_n,
            degrees=degrees,
            shifts=shifts,
            moduli=moduli,
        ),
        encoding="utf-8",
    )
    return output
