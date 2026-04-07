from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mpmath
import yaml

from .bz_dual_f7 import (
    displayed_series_to_hyper_line_ratio,
    dual_b_vector_from_a,
    evaluate_exact_f7_linear_form,
    evaluate_f7,
    evaluate_f7_hyper_line,
    extract_f7_linear_form,
    render_exact_f7_linear_form,
    scale_b_vector,
)
from .config import DATA_DIR, REPO_ROOT
from .models import fraction_to_canonical_string

DUAL_F7_EXACT_FIXTURE_PATH = REPO_ROOT / "regression" / "fixtures" / "bz_dual_f7_exact_probe.yaml"
DEFAULT_DUAL_F7_EXACT_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_exact_probe_report.md"


@dataclass(frozen=True)
class DualF7ExactCaseFixture:
    id: str
    label: str
    a: tuple[int, ...]
    n_values: tuple[int, ...]


@dataclass(frozen=True)
class DualF7ExactProbeFixture:
    id: str
    source_title: str
    source_url: str
    source_version: str
    source_notes: str
    cases: tuple[DualF7ExactCaseFixture, ...]


@dataclass(frozen=True)
class DualF7ExactSample:
    n: int
    b: tuple[int, ...]
    exact_linear_form: str
    constant_term: str
    zeta3_coeff: str
    zeta5_coeff: str
    log10_abs_value: float
    hyper_line_log10_abs_value: float
    series_to_hyper_ratio: int


@dataclass(frozen=True)
class DualF7ExactCaseProbe:
    id: str
    label: str
    a: tuple[int, ...]
    base_b: tuple[int, ...]
    samples: tuple[DualF7ExactSample, ...]


@dataclass(frozen=True)
class BZDualF7ExactProbe:
    fixture_id: str
    source_title: str
    source_url: str
    source_version: str
    source_notes: str
    precision: int
    cases: tuple[DualF7ExactCaseProbe, ...]


def build_bz_dual_f7_exact_probe(*, precision: int = 120) -> BZDualF7ExactProbe:
    if precision < 60:
        raise ValueError("precision must be at least 60 decimal digits")

    fixture = _load_dual_f7_exact_fixture()
    cases = []
    for case in fixture.cases:
        base_b = dual_b_vector_from_a(case.a)
        samples = []
        for n in case.n_values:
            b = scale_b_vector(base_b, n)
            exact_linear_form = extract_f7_linear_form(b)
            exact_value = evaluate_exact_f7_linear_form(exact_linear_form, precision=precision)
            canonical_value = evaluate_f7(b, precision=precision)
            hyper_line_value = evaluate_f7_hyper_line(b, precision=precision)
            with mpmath.workdps(precision):
                if abs(exact_value - canonical_value) > mpmath.mpf(10) ** (-(3 * precision // 4)):
                    raise ValueError(f"exact extraction does not match canonical evaluation for b={b}")
                samples.append(
                    DualF7ExactSample(
                        n=n,
                        b=b,
                        exact_linear_form=render_exact_f7_linear_form(exact_linear_form),
                        constant_term=fraction_to_canonical_string(exact_linear_form.constant_term),
                        zeta3_coeff=fraction_to_canonical_string(exact_linear_form.zeta_coefficient(3)),
                        zeta5_coeff=fraction_to_canonical_string(exact_linear_form.zeta_coefficient(5)),
                        log10_abs_value=float(mpmath.log10(abs(exact_value))),
                        hyper_line_log10_abs_value=float(mpmath.log10(abs(hyper_line_value))),
                        series_to_hyper_ratio=displayed_series_to_hyper_line_ratio(b),
                    )
                )
        cases.append(
            DualF7ExactCaseProbe(
                id=case.id,
                label=case.label,
                a=case.a,
                base_b=base_b,
                samples=tuple(samples),
            )
        )

    return BZDualF7ExactProbe(
        fixture_id=fixture.id,
        source_title=fixture.source_title,
        source_url=fixture.source_url,
        source_version=fixture.source_version,
        source_notes=fixture.source_notes,
        precision=precision,
        cases=tuple(cases),
    )


def render_bz_dual_f7_exact_probe_report(*, precision: int = 120) -> str:
    probe = build_bz_dual_f7_exact_probe(precision=precision)
    lines = [
        "# Brown-Zudilin dual F_7 exact probe",
        "",
        f"- Fixture: `{probe.fixture_id}`",
        f"- Source: `{probe.source_title}` ({probe.source_url})",
        f"- Source version: `{probe.source_version}`",
        f"- Numeric precision for exact-value verification: `{probe.precision}` decimal digits",
        "- The exact extractor follows the displayed summand formula in equation (10), performs exact partial fractions in `mu`, and sums them into a rational term plus zeta values.",
        "- The canonical `evaluate_f7` path follows that displayed-series normalization.",
        "- The literal hypergeometric-line evaluation differs from the displayed summand by a factor `b0 + 2`; this report records that factor explicitly.",
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
                "| n | scaled b0 | constant term | zeta(3) coeff | zeta(5) coeff | log10|F_7| | log10|hyper line| | series/hyper |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for sample in case.samples:
            lines.append(
                "| "
                + " | ".join(
                    (
                        str(sample.n),
                        str(sample.b[0]),
                        sample.constant_term,
                        sample.zeta3_coeff,
                        sample.zeta5_coeff,
                        f"{sample.log10_abs_value:.6f}",
                        f"{sample.hyper_line_log10_abs_value:.6f}",
                        str(sample.series_to_hyper_ratio),
                    )
                )
                + " |"
            )
            lines.append(f"| exact linear form |  | `{sample.exact_linear_form}` |  |  |  |  |  |")
        lines.append("")
    return "\n".join(lines) + "\n"


def write_bz_dual_f7_exact_probe_report(
    *,
    precision: int = 120,
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_DUAL_F7_EXACT_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_bz_dual_f7_exact_probe_report(precision=precision), encoding="utf-8")
    return output


def _load_dual_f7_exact_fixture() -> DualF7ExactProbeFixture:
    payload = yaml.safe_load(DUAL_F7_EXACT_FIXTURE_PATH.read_text(encoding="utf-8"))
    root = payload["dual_f7_exact_probe"]
    source = root["source"]
    cases = []
    for item in root["cases"]:
        cases.append(
            DualF7ExactCaseFixture(
                id=str(item["id"]),
                label=str(item["label"]),
                a=tuple(int(value) for value in item["a"]),
                n_values=tuple(int(value) for value in item["n_values"]),
            )
        )
    return DualF7ExactProbeFixture(
        id=str(root["id"]),
        source_title=str(source["title"]),
        source_url=str(source["url"]),
        source_version=str(source["version"]),
        source_notes=str(source["notes"]),
        cases=tuple(cases),
    )
