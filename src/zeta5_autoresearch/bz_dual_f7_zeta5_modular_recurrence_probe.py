from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import DATA_DIR
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .recurrence_mining import ModularRankCertificate, modular_rank_certificate

DEFAULT_DUAL_F7_ZETA5_MODULAR_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_zeta5_modular_recurrence_report.md"
DEFAULT_DUAL_F7_ZETA5_MODULI = (1000003, 1000033, 1000037)


@dataclass(frozen=True)
class DualF7Zeta5ModularDegreeSummary:
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


@dataclass(frozen=True)
class BZDualF7Zeta5ModularRecurrenceProbe:
    max_n: int
    shifts: tuple[int, ...]
    moduli: tuple[int, ...]
    degrees: tuple[int, ...]
    summaries: tuple[DualF7Zeta5ModularDegreeSummary, ...]

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


def build_bz_dual_f7_zeta5_modular_recurrence_probe(
    *,
    max_n: int = 30,
    degrees: tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6),
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    moduli: tuple[int, ...] = DEFAULT_DUAL_F7_ZETA5_MODULI,
) -> BZDualF7Zeta5ModularRecurrenceProbe:
    if max_n < 4:
        raise ValueError("max_n must be at least 4")
    if not degrees:
        raise ValueError("degrees must be non-empty")

    exact_terms = get_cached_baseline_dual_f7_zeta5_terms(max_n)
    sequences = {
        modulus: tuple(value % modulus for value in exact_terms)
        for modulus in moduli
    }

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
        summaries.append(DualF7Zeta5ModularDegreeSummary(degree=degree, certificates=certificates))

    return BZDualF7Zeta5ModularRecurrenceProbe(
        max_n=max_n,
        shifts=shifts,
        moduli=moduli,
        degrees=degrees,
        summaries=tuple(summaries),
    )


def render_bz_dual_f7_zeta5_modular_recurrence_report(
    *,
    max_n: int = 30,
    degrees: tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6),
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    moduli: tuple[int, ...] = DEFAULT_DUAL_F7_ZETA5_MODULI,
) -> str:
    probe = build_bz_dual_f7_zeta5_modular_recurrence_probe(
        max_n=max_n,
        degrees=degrees,
        shifts=shifts,
        moduli=moduli,
    )
    lines = [
        "# Brown-Zudilin dual F_7 zeta(5)-coefficient modular recurrence certificates",
        "",
        f"- Baseline exact dual zeta(5) coefficients reduced modulo primes through `n={probe.max_n}`.",
        f"- Search family: polynomial recurrences supported on shifts `{probe.shifts}`.",
        f"- Modular certificate primes: `{probe.moduli}`.",
    ]
    if probe.certified_degree_cap is not None:
        lines.append(
            f"- Certified consequence: no rational recurrence of this shape exists through degree `{probe.certified_degree_cap}`."
        )
    if probe.first_uncertified_degree is not None:
        lines.append(
            f"- First unresolved degree in this scan: `{probe.first_uncertified_degree}`."
        )
    lines.append("- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.")
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


def write_bz_dual_f7_zeta5_modular_recurrence_report(
    *,
    max_n: int = 30,
    degrees: tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6),
    shifts: tuple[int, ...] = (1, 0, -1, -2),
    moduli: tuple[int, ...] = DEFAULT_DUAL_F7_ZETA5_MODULI,
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_DUAL_F7_ZETA5_MODULAR_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_bz_dual_f7_zeta5_modular_recurrence_report(
            max_n=max_n,
            degrees=degrees,
            shifts=shifts,
            moduli=moduli,
        ),
        encoding="utf-8",
    )
    return output
