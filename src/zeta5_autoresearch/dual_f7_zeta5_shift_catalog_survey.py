from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .baseline_shift_catalog_survey import ShiftCatalogGeneratorSpec, enumerate_normalized_shift_supports
from .bz_dual_f7_zeta5_modular_recurrence_probe import DEFAULT_DUAL_F7_ZETA5_MODULI
from .config import DATA_DIR
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms
from .models import SpecValidationError
from .recurrence_mining import modular_rank_certificate

DEFAULT_DUAL_F7_ZETA5_SHIFT_CATALOG_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_zeta5_shift_catalog_survey_report.md"


@dataclass(frozen=True)
class DualF7Zeta5ShiftCatalogSurveySpec:
    id: str
    label: str
    max_n: int
    moduli: tuple[int, ...]
    catalogs: tuple[ShiftCatalogGeneratorSpec, ...]


@dataclass(frozen=True)
class DualF7Zeta5ShiftFamilyFrontierResult:
    shifts: tuple[int, ...]
    equation_count: int
    frontier_degree: int
    certified_degree_cap: int | None
    first_uncertified_degree: int | None
    certifying_modulus: int | None

    @property
    def fully_ruled_out_through_frontier(self) -> bool:
        return self.first_uncertified_degree is None


@dataclass(frozen=True)
class DualF7Zeta5ShiftCatalogSurveyResult:
    catalog: ShiftCatalogGeneratorSpec
    family_count: int
    fully_ruled_out_count: int
    unresolved_count: int
    min_frontier_degree: int
    max_frontier_degree: int
    results: tuple[DualF7Zeta5ShiftFamilyFrontierResult, ...]


def load_dual_f7_zeta5_shift_catalog_survey(path: str | Path) -> DualF7Zeta5ShiftCatalogSurveySpec:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "survey" not in payload:
        raise SpecValidationError("dual f7 zeta(5) shift catalog survey file must contain a root 'survey' mapping")
    survey = payload["survey"]
    if not isinstance(survey, dict):
        raise SpecValidationError("survey must be a mapping")

    for key in ("id", "label", "max_n", "catalogs"):
        if key not in survey:
            raise SpecValidationError(f"survey is missing required key {key!r}")
    catalogs_payload = survey["catalogs"]
    if not isinstance(catalogs_payload, list) or not catalogs_payload:
        raise SpecValidationError("survey.catalogs must be a non-empty list")

    catalogs = []
    for item in catalogs_payload:
        if not isinstance(item, dict):
            raise SpecValidationError("survey catalog entries must be mappings")
        for key in ("id", "label", "order", "min_shift", "max_shift"):
            if key not in item:
                raise SpecValidationError(f"survey catalog is missing required key {key!r}")
        catalogs.append(
            ShiftCatalogGeneratorSpec(
                id=str(item["id"]),
                label=str(item["label"]),
                order=int(item["order"]),
                min_shift=int(item["min_shift"]),
                max_shift=int(item["max_shift"]),
                include_zero=bool(item.get("include_zero", True)),
                require_positive=bool(item.get("require_positive", True)),
                require_negative=bool(item.get("require_negative", True)),
                primitive_only=bool(item.get("primitive_only", True)),
            )
        )

    moduli_payload = survey.get("moduli", list(DEFAULT_DUAL_F7_ZETA5_MODULI))
    if not isinstance(moduli_payload, list) or not moduli_payload:
        raise SpecValidationError("survey.moduli must be a non-empty list when provided")

    return DualF7Zeta5ShiftCatalogSurveySpec(
        id=str(survey["id"]),
        label=str(survey["label"]),
        max_n=int(survey["max_n"]),
        moduli=tuple(int(value) for value in moduli_payload),
        catalogs=tuple(catalogs),
    )


def run_dual_f7_zeta5_shift_catalog_survey(
    path: str | Path,
) -> tuple[DualF7Zeta5ShiftCatalogSurveySpec, tuple[DualF7Zeta5ShiftCatalogSurveyResult, ...]]:
    spec = load_dual_f7_zeta5_shift_catalog_survey(path)
    exact_terms = get_cached_baseline_dual_f7_zeta5_terms(spec.max_n)
    sequences_by_modulus = {
        modulus: tuple(value % modulus for value in exact_terms)
        for modulus in spec.moduli
    }

    catalog_results = []
    for catalog in spec.catalogs:
        results = tuple(
            _survey_shift_family(spec.max_n, shifts, spec.moduli, sequences_by_modulus)
            for shifts in enumerate_normalized_shift_supports(catalog)
        )
        fully_ruled_out_count = sum(1 for result in results if result.fully_ruled_out_through_frontier)
        unresolved_count = len(results) - fully_ruled_out_count
        frontier_degrees = tuple(result.frontier_degree for result in results)
        catalog_results.append(
            DualF7Zeta5ShiftCatalogSurveyResult(
                catalog=catalog,
                family_count=len(results),
                fully_ruled_out_count=fully_ruled_out_count,
                unresolved_count=unresolved_count,
                min_frontier_degree=min(frontier_degrees),
                max_frontier_degree=max(frontier_degrees),
                results=results,
            )
        )
    return spec, tuple(catalog_results)


def render_dual_f7_zeta5_shift_catalog_survey_report(path: str | Path) -> str:
    spec, catalog_results = run_dual_f7_zeta5_shift_catalog_survey(path)
    lines = [
        "# Brown-Zudilin dual F_7 zeta(5)-coefficient shift-catalog survey",
        "",
        f"- Survey ID: `{spec.id}`",
        f"- Label: `{spec.label}`",
        f"- Exact baseline dual zeta(5) coefficient cache window: through `n={spec.max_n}`",
        f"- Modular certificate primes: `{spec.moduli}`",
        "- Search logic: for a fixed support, full column rank at degree `d` implies the same for all lower degrees, so each family is certified with a monotone frontier search.",
        "",
        "| Catalog | Order | Shift Window | Families | Frontier Degree Range | Fully Ruled Out | Survivors |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in catalog_results:
        lines.append(
            f"| {result.catalog.label} | {result.catalog.order} | `[{result.catalog.min_shift}, {result.catalog.max_shift}]` | {result.family_count} | `{result.min_frontier_degree}..{result.max_frontier_degree}` | {result.fully_ruled_out_count} | {result.unresolved_count} |"
        )

    lines.extend(("", "## Findings", ""))
    for result in catalog_results:
        if result.unresolved_count == 0:
            lines.append(
                f"- `{result.catalog.id}`: all `{result.family_count}` normalized supports are ruled out through their full certifiable frontier."
            )
            continue
        lines.append(
            f"- `{result.catalog.id}`: `{result.unresolved_count}` of `{result.family_count}` supports survive past the monotone frontier search."
        )
        for family in _top_unresolved_results(result.results)[:8]:
            lines.append(
                f"- unresolved `{family.shifts}`: certified through degree `{family.certified_degree_cap}`, first gap `{family.first_uncertified_degree}`, frontier `{family.frontier_degree}`, equations `{family.equation_count}`."
            )

    lines.extend(("", "## Frontier Samples", ""))
    for result in catalog_results:
        best = max(result.results, key=lambda item: (item.frontier_degree, item.shifts))
        lines.append(
            f"- `{result.catalog.id}` sample frontier support `{best.shifts}`: frontier degree `{best.frontier_degree}`, certified cap `{best.certified_degree_cap}`, first gap `{best.first_uncertified_degree}`."
        )
    return "\n".join(lines) + "\n"


def write_dual_f7_zeta5_shift_catalog_survey_report(
    path: str | Path,
    *,
    output_path: str | Path | None = None,
) -> Path:
    survey_path = Path(path)
    output = DEFAULT_DUAL_F7_ZETA5_SHIFT_CATALOG_REPORT_PATH if output_path is None else Path(output_path)
    if output_path is None:
        output = DATA_DIR / "logs" / f"{survey_path.stem}_report.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_dual_f7_zeta5_shift_catalog_survey_report(survey_path), encoding="utf-8")
    return output


def _survey_shift_family(
    max_n: int,
    shifts: tuple[int, ...],
    moduli: tuple[int, ...],
    sequences_by_modulus: dict[int, tuple[int, ...]],
) -> DualF7Zeta5ShiftFamilyFrontierResult:
    equation_count = _equation_count_for_family(max_n, shifts)
    if equation_count <= 0:
        raise ValueError(f"no valid recurrence window for shifts {shifts}")
    frontier_degree = (equation_count // len(shifts)) - 1
    if frontier_degree < 0:
        raise ValueError(f"insufficient equations to test shifts {shifts}")

    low = 0
    high = frontier_degree
    best_cap: int | None = None
    certifying_modulus: int | None = None

    while low <= high:
        probe_degree = (low + high) // 2
        degree_certifies, modulus = _certifies_family_degree(
            degree=probe_degree,
            shifts=shifts,
            moduli=moduli,
            sequences_by_modulus=sequences_by_modulus,
        )
        if degree_certifies:
            best_cap = probe_degree
            certifying_modulus = modulus
            low = probe_degree + 1
        else:
            high = probe_degree - 1

    if best_cap == frontier_degree:
        return DualF7Zeta5ShiftFamilyFrontierResult(
            shifts=shifts,
            equation_count=equation_count,
            frontier_degree=frontier_degree,
            certified_degree_cap=best_cap,
            first_uncertified_degree=None,
            certifying_modulus=certifying_modulus,
        )

    first_uncertified_degree = 0 if best_cap is None else best_cap + 1
    return DualF7Zeta5ShiftFamilyFrontierResult(
        shifts=shifts,
        equation_count=equation_count,
        frontier_degree=frontier_degree,
        certified_degree_cap=best_cap,
        first_uncertified_degree=first_uncertified_degree,
        certifying_modulus=certifying_modulus,
    )


def _certifies_family_degree(
    *,
    degree: int,
    shifts: tuple[int, ...],
    moduli: tuple[int, ...],
    sequences_by_modulus: dict[int, tuple[int, ...]],
) -> tuple[bool, int | None]:
    for modulus in moduli:
        certificate = modular_rank_certificate(
            sequences_by_modulus[modulus],
            degree=degree,
            modulus=modulus,
            shifts=shifts,
        )
        if certificate.certifies_no_solution:
            return True, modulus
    return False, None


def _equation_count_for_family(max_n: int, shifts: tuple[int, ...]) -> int:
    start_n = max(0, -min(shifts))
    end_n = max_n - max(shifts)
    return max(0, end_n - start_n + 1)


def _top_unresolved_results(
    results: tuple[DualF7Zeta5ShiftFamilyFrontierResult, ...],
) -> list[DualF7Zeta5ShiftFamilyFrontierResult]:
    unresolved = [result for result in results if not result.fully_ruled_out_through_frontier]
    return sorted(
        unresolved,
        key=lambda item: (
            -(item.frontier_degree - (item.certified_degree_cap if item.certified_degree_cap is not None else -1)),
            -(item.frontier_degree),
            item.shifts,
        ),
    )
