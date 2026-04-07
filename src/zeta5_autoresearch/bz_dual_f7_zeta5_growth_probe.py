from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mpmath

from .config import DATA_DIR
from .dual_f7_zeta5_cache import get_cached_baseline_dual_f7_zeta5_terms

DEFAULT_DUAL_F7_ZETA5_GROWTH_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_zeta5_growth_report.md"


@dataclass(frozen=True)
class DualF7Zeta5GrowthSample:
    n: int
    digits: int
    log10_abs_coefficient: float
    root_estimate: float | None
    ratio_estimate: float | None


@dataclass(frozen=True)
class BZDualF7Zeta5GrowthProbe:
    max_n: int
    latest_root_estimate: float
    latest_ratio_estimate: float
    samples: tuple[DualF7Zeta5GrowthSample, ...]


def build_bz_dual_f7_zeta5_growth_probe(*, max_n: int = 20) -> BZDualF7Zeta5GrowthProbe:
    if max_n < 2:
        raise ValueError("max_n must be at least 2")

    terms = get_cached_baseline_dual_f7_zeta5_terms(max_n)
    samples = []
    with mpmath.workdps(80):
        for n, coefficient in enumerate(terms, start=1):
            digits = len(str(abs(coefficient)))
            log10_abs = float(mpmath.log10(abs(coefficient)))
            root_estimate = float(mpmath.log(abs(coefficient)) / n)
            ratio_estimate = None
            if n >= 2:
                ratio_estimate = float(abs(mpmath.mpf(coefficient) / terms[n - 2]))
            samples.append(
                DualF7Zeta5GrowthSample(
                    n=n,
                    digits=digits,
                    log10_abs_coefficient=log10_abs,
                    root_estimate=root_estimate,
                    ratio_estimate=ratio_estimate,
                )
            )
    latest = samples[-1]
    if latest.ratio_estimate is None:
        raise ValueError("expected max_n >= 2")
    return BZDualF7Zeta5GrowthProbe(
        max_n=max_n,
        latest_root_estimate=latest.root_estimate,
        latest_ratio_estimate=latest.ratio_estimate,
        samples=tuple(samples),
    )


def render_bz_dual_f7_zeta5_growth_report(*, max_n: int = 20) -> str:
    probe = build_bz_dual_f7_zeta5_growth_probe(max_n=max_n)
    lines = [
        "# Brown-Zudilin dual F_7 zeta(5)-coefficient growth probe",
        "",
        f"- Baseline exact dual zeta(5) coefficients generated through `n={probe.max_n}`.",
        f"- Latest `log|coeff_n|/n`: `{probe.latest_root_estimate:.8f}` at `n={probe.max_n}`.",
        f"- Latest `|coeff_n/coeff_(n-1)|`: `{probe.latest_ratio_estimate:.8f}` at `n={probe.max_n}`.",
        "- This is an exact coefficient-growth calibration, not a certification statement.",
        "",
        "| n | digits | log10|coeff| | log|coeff|/n | |coeff_n/coeff_(n-1)| |",
        "| --- | --- | --- | --- | --- |",
    ]
    for sample in probe.samples:
        ratio = "" if sample.ratio_estimate is None else f"{sample.ratio_estimate:.8f}"
        lines.append(
            f"| {sample.n} | {sample.digits} | {sample.log10_abs_coefficient:.6f} | {sample.root_estimate:.8f} | {ratio} |"
        )
    return "\n".join(lines) + "\n"


def write_bz_dual_f7_zeta5_growth_report(
    *,
    max_n: int = 20,
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_DUAL_F7_ZETA5_GROWTH_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_bz_dual_f7_zeta5_growth_report(max_n=max_n), encoding="utf-8")
    return output
