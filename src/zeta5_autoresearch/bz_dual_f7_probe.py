from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mpmath
import yaml

from .bz_dual_f7 import dual_b_vector_from_a, evaluate_f7, render_dual_f7_relation, scale_b_vector, search_f7_zeta_relation
from .config import DATA_DIR, REPO_ROOT

DUAL_F7_FIXTURE_PATH = REPO_ROOT / "regression" / "fixtures" / "bz_dual_f7_probe.yaml"
DEFAULT_DUAL_F7_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_probe_report.md"


@dataclass(frozen=True)
class DualF7CaseFixture:
    id: str
    label: str
    a: tuple[int, ...]
    expected_b: tuple[int, ...]
    n_values: tuple[int, ...]
    pslq_maxcoeff: int


@dataclass(frozen=True)
class DualF7ProbeFixture:
    id: str
    source_title: str
    source_url: str
    source_version: str
    source_notes: str
    cases: tuple[DualF7CaseFixture, ...]


@dataclass(frozen=True)
class DualF7Sample:
    n: int
    b: tuple[int, ...]
    value_text: str
    log10_abs_value: float
    log_abs_over_n: float
    pslq_relation_text: str | None
    pslq_coefficients: tuple[int, int, int, int] | None
    pslq_residual_log10_abs: float | None


@dataclass(frozen=True)
class DualF7CaseProbe:
    id: str
    label: str
    a: tuple[int, ...]
    base_b: tuple[int, ...]
    samples: tuple[DualF7Sample, ...]


@dataclass(frozen=True)
class BZDualF7Probe:
    fixture_id: str
    source_title: str
    source_url: str
    source_version: str
    source_notes: str
    precision: int
    pslq_precision: int
    cases: tuple[DualF7CaseProbe, ...]


def build_bz_dual_f7_probe(
    *,
    precision: int = 120,
    pslq_precision: int = 180,
) -> BZDualF7Probe:
    if precision < 60:
        raise ValueError("precision must be at least 60 decimal digits")
    if pslq_precision < precision:
        raise ValueError("pslq_precision must be at least precision")

    fixture = _load_dual_f7_fixture()
    probes = []
    for case in fixture.cases:
        base_b = dual_b_vector_from_a(case.a)
        if base_b != case.expected_b:
            raise ValueError(f"fixture expected_b mismatch for case {case.id}")
        samples = []
        for n in case.n_values:
            b = scale_b_vector(base_b, n)
            with mpmath.workdps(precision):
                value = evaluate_f7(b, precision=precision)
                log10_abs_value = float(mpmath.log10(abs(value)))
                log_abs_over_n = float(mpmath.log(abs(value)) / n)
                value_text = mpmath.nstr(value, 16)
            relation = search_f7_zeta_relation(
                value,
                precision=pslq_precision,
                maxcoeff=case.pslq_maxcoeff,
            )
            samples.append(
                DualF7Sample(
                    n=n,
                    b=b,
                    value_text=value_text,
                    log10_abs_value=log10_abs_value,
                    log_abs_over_n=log_abs_over_n,
                    pslq_relation_text=(None if relation is None else render_dual_f7_relation(relation)),
                    pslq_coefficients=(None if relation is None else relation.coefficients),
                    pslq_residual_log10_abs=(None if relation is None else relation.residual_log10_abs),
                )
            )
        probes.append(
            DualF7CaseProbe(
                id=case.id,
                label=case.label,
                a=case.a,
                base_b=base_b,
                samples=tuple(samples),
            )
        )

    return BZDualF7Probe(
        fixture_id=fixture.id,
        source_title=fixture.source_title,
        source_url=fixture.source_url,
        source_version=fixture.source_version,
        source_notes=fixture.source_notes,
        precision=precision,
        pslq_precision=pslq_precision,
        cases=tuple(probes),
    )


def render_bz_dual_f7_probe_report(*, precision: int = 120, pslq_precision: int = 180) -> str:
    probe = build_bz_dual_f7_probe(precision=precision, pslq_precision=pslq_precision)
    lines = [
        "# Brown-Zudilin dual F_7 probe",
        "",
        f"- Fixture: `{probe.fixture_id}`",
        f"- Source: `{probe.source_title}` ({probe.source_url})",
        f"- Source version: `{probe.source_version}`",
        f"- Numeric precision for `F_7(b)`: `{probe.precision}` decimal digits",
        f"- Numeric precision for PSLQ search: `{probe.pslq_precision}` decimal digits",
        "- The evaluator follows the displayed-series normalization for `F_7(b)` together with the affine map from `a` to `b`.",
        "- The literal hypergeometric-line evaluation differs by a factor `b0 + 2`; this report uses the displayed-series normalization because it matches the exact coefficient extractor.",
        "- Any recovered decomposition into `1`, `zeta(3)`, and `zeta(5)` is an uncertified numeric PSLQ witness, not an exact proof object.",
        "- A missing PSLQ relation means no low-height relation was found at the tested coefficient bound; it does not certify nonexistence.",
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
                "| n | scaled b0 | F_7(b*n) | log10|F_7| | log|F_7|/n | PSLQ status |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for sample in case.samples:
            relation_text = "no low-height relation found"
            if sample.pslq_relation_text is not None:
                relation_text = sample.pslq_relation_text
                if sample.pslq_residual_log10_abs is not None:
                    relation_text += f" (log10 residual {sample.pslq_residual_log10_abs:.1f})"
            lines.append(
                "| "
                + " | ".join(
                    (
                        str(sample.n),
                        str(sample.b[0]),
                        sample.value_text,
                        f"{sample.log10_abs_value:.6f}",
                        f"{sample.log_abs_over_n:.8f}",
                        relation_text,
                    )
                )
                + " |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def write_bz_dual_f7_probe_report(
    *,
    precision: int = 120,
    pslq_precision: int = 180,
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_DUAL_F7_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_bz_dual_f7_probe_report(precision=precision, pslq_precision=pslq_precision),
        encoding="utf-8",
    )
    return output


def _load_dual_f7_fixture() -> DualF7ProbeFixture:
    payload = yaml.safe_load(DUAL_F7_FIXTURE_PATH.read_text(encoding="utf-8"))
    root = payload["dual_f7_probe"]
    source = root["source"]
    cases = []
    for item in root["cases"]:
        cases.append(
            DualF7CaseFixture(
                id=str(item["id"]),
                label=str(item["label"]),
                a=tuple(int(value) for value in item["a"]),
                expected_b=tuple(int(value) for value in item["expected_b"]),
                n_values=tuple(int(value) for value in item["n_values"]),
                pslq_maxcoeff=int(item["pslq_maxcoeff"]),
            )
        )
    return DualF7ProbeFixture(
        id=str(root["id"]),
        source_title=str(source["title"]),
        source_url=str(source["url"]),
        source_version=str(source["version"]),
        source_notes=str(source["notes"]),
        cases=tuple(cases),
    )
