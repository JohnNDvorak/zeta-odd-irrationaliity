from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .baseline_q_cache import get_cached_baseline_q_terms_mod_prime
from .baseline_modular_recurrence_probe import DEFAULT_MODULI, build_baseline_modular_recurrence_probe
from .config import DATA_DIR, REPO_ROOT
from .models import SpecValidationError

DEFAULT_BASELINE_FAMILY_SURVEY_REPORT_PATH = DATA_DIR / "logs" / "bz_baseline_family_survey_report.md"


@dataclass(frozen=True)
class BaselineFamilySurveySpec:
    id: str
    label: str
    max_n: int
    moduli: tuple[int, ...]
    families: tuple["BaselineFamilySurveyEntry", ...]


@dataclass(frozen=True)
class BaselineFamilySurveyEntry:
    id: str
    label: str
    shifts: tuple[int, ...]
    degree_min: int
    degree_max: int


@dataclass(frozen=True)
class BaselineFamilySurveyResult:
    entry: BaselineFamilySurveyEntry
    certified_degree_cap: int | None
    first_uncertified_degree: int | None
    equation_count: int
    variable_count_at_cap: int | None
    variable_count_at_first_gap: int | None


def load_baseline_family_survey(path: str | Path) -> BaselineFamilySurveySpec:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "survey" not in payload:
        raise SpecValidationError("baseline family survey file must contain a root 'survey' mapping")
    survey = payload["survey"]
    if not isinstance(survey, dict):
        raise SpecValidationError("survey must be a mapping")

    for key in ("id", "label", "max_n", "families"):
        if key not in survey:
            raise SpecValidationError(f"survey is missing required key {key!r}")
    families_payload = survey["families"]
    if not isinstance(families_payload, list) or not families_payload:
        raise SpecValidationError("survey.families must be a non-empty list")

    entries = []
    for item in families_payload:
        if not isinstance(item, dict):
            raise SpecValidationError("survey family entries must be mappings")
        for key in ("id", "label", "shifts", "degree_min", "degree_max"):
            if key not in item:
                raise SpecValidationError(f"survey family is missing required key {key!r}")
        shifts_payload = item["shifts"]
        if not isinstance(shifts_payload, list) or not shifts_payload:
            raise SpecValidationError("survey family shifts must be a non-empty list")
        entries.append(
            BaselineFamilySurveyEntry(
                id=str(item["id"]),
                label=str(item["label"]),
                shifts=tuple(int(value) for value in shifts_payload),
                degree_min=int(item["degree_min"]),
                degree_max=int(item["degree_max"]),
            )
        )

    moduli_payload = survey.get("moduli", list(DEFAULT_MODULI))
    if not isinstance(moduli_payload, list) or not moduli_payload:
        raise SpecValidationError("survey.moduli must be a non-empty list when provided")

    return BaselineFamilySurveySpec(
        id=str(survey["id"]),
        label=str(survey["label"]),
        max_n=int(survey["max_n"]),
        moduli=tuple(int(value) for value in moduli_payload),
        families=tuple(entries),
    )


def run_baseline_family_survey(path: str | Path) -> tuple[BaselineFamilySurveySpec, tuple[BaselineFamilySurveyResult, ...]]:
    spec = load_baseline_family_survey(path)
    sequences_by_modulus = {
        modulus: get_cached_baseline_q_terms_mod_prime(spec.max_n, modulus=modulus)
        for modulus in spec.moduli
    }
    results = []
    for entry in spec.families:
        probe = build_baseline_modular_recurrence_probe(
            max_n=spec.max_n,
            degrees=tuple(range(entry.degree_min, entry.degree_max + 1)),
            shifts=entry.shifts,
            moduli=spec.moduli,
            sequences_by_modulus=sequences_by_modulus,
        )
        first_summary = probe.summaries[0]
        variable_count_at_cap = None if probe.certified_degree_cap is None else len(entry.shifts) * (probe.certified_degree_cap + 1)
        variable_count_at_first_gap = None if probe.first_uncertified_degree is None else len(entry.shifts) * (probe.first_uncertified_degree + 1)
        results.append(
            BaselineFamilySurveyResult(
                entry=entry,
                certified_degree_cap=probe.certified_degree_cap,
                first_uncertified_degree=probe.first_uncertified_degree,
                equation_count=first_summary.certificates[0].equation_count,
                variable_count_at_cap=variable_count_at_cap,
                variable_count_at_first_gap=variable_count_at_first_gap,
            )
        )
    return spec, tuple(results)


def render_baseline_family_survey_report(path: str | Path) -> str:
    spec, results = run_baseline_family_survey(path)
    lines = [
        "# Brown-Zudilin baseline recurrence family survey",
        "",
        f"- Survey ID: `{spec.id}`",
        f"- Label: `{spec.label}`",
        f"- Modular baseline cache window: through `n={spec.max_n}`",
        f"- Modular certificate primes: `{spec.moduli}`",
        "",
        "| Family | Shifts | Degree Window | Equations | Certified Cap | First Gap |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        cap = "" if result.certified_degree_cap is None else str(result.certified_degree_cap)
        gap = "" if result.first_uncertified_degree is None else str(result.first_uncertified_degree)
        degree_window = f"{result.entry.degree_min}..{result.entry.degree_max}"
        lines.append(
            f"| {result.entry.label} | `{result.entry.shifts}` | `{degree_window}` | {result.equation_count} | {cap} | {gap} |"
        )

    lines.extend(("", "## Notes", ""))
    for result in results:
        if result.first_uncertified_degree is None:
            lines.append(
                f"- `{result.entry.id}`: ruled out through the full scanned window `{result.entry.degree_min}..{result.entry.degree_max}`."
            )
        else:
            lines.append(
                f"- `{result.entry.id}`: ruled out through degree `{result.certified_degree_cap}`; first unresolved degree is `{result.first_uncertified_degree}` with `{result.variable_count_at_first_gap}` variables against `{result.equation_count}` equations."
            )
    return "\n".join(lines) + "\n"


def write_baseline_family_survey_report(
    path: str | Path,
    *,
    output_path: str | Path | None = None,
) -> Path:
    survey_path = Path(path)
    output = DEFAULT_BASELINE_FAMILY_SURVEY_REPORT_PATH if output_path is None else Path(output_path)
    if output_path is None:
        output = DATA_DIR / "logs" / f"{survey_path.stem}_report.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_family_survey_report(survey_path), encoding="utf-8")
    return output
