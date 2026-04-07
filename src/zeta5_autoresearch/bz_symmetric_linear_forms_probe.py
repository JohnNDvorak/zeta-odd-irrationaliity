from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import gcd
from pathlib import Path

import mpmath
import yaml

from .config import DATA_DIR, REPO_ROOT
from .decay_probe import DecayMetric, DecayProbeSummary, build_decay_probe_summary
from .gate2.recurrence_eval import generate_terms_from_recurrence, recurrence_residuals
from .gate2.sequence_identity import MinimalRecurrenceIdentity
from .models import fraction_from_scalar
from .sequence_evidence import load_sequence_evidence_by_id

LINEAR_FORMS_FIXTURE_PATH = REPO_ROOT / "regression" / "fixtures" / "bz_totally_symmetric_linear_forms.yaml"
DEFAULT_LINEAR_FORMS_REPORT_PATH = DATA_DIR / "logs" / "bz_totally_symmetric_linear_forms_report.md"


@dataclass(frozen=True)
class SymmetricLinearFormsFixture:
    id: str
    q_recurrence_evidence_id: str
    source_title: str
    source_url: str
    source_version: str
    source_notes: str
    q_initial: tuple[Fraction, ...]
    phat_initial: tuple[Fraction, ...]
    p_initial: tuple[Fraction, ...]
    q_scale_label: str
    phat_scale_label: str
    p_scale_label: str
    published_gamma: float


@dataclass(frozen=True)
class SymmetricLinearFormsSample:
    n: int
    q_digits: int
    p_numerator_digits: int
    p_denominator: int
    phat_numerator_digits: int
    phat_denominator: int
    p_residual_zero: bool
    phat_residual_zero: bool
    q_root_estimate: float | None
    remainder_root_estimate: float | None
    gamma_estimate: float | None


@dataclass(frozen=True)
class BZTotallySymmetricLinearFormsProbe:
    fixture_id: str
    recurrence_evidence_id: str
    source_title: str
    source_url: str
    source_version: str
    max_n: int
    precision: int
    published_gamma: float
    latest_q_root_estimate: float
    latest_remainder_root_estimate: float
    latest_gamma_estimate: float
    all_p_residuals_zero: bool
    all_phat_residuals_zero: bool
    decay_summary: DecayProbeSummary
    samples: tuple[SymmetricLinearFormsSample, ...]


def build_bz_totally_symmetric_linear_forms_probe(
    *,
    max_n: int = 12,
    precision: int = 80,
) -> BZTotallySymmetricLinearFormsProbe:
    if max_n < 2:
        raise ValueError("max_n must be at least 2")
    if precision < 40:
        raise ValueError("precision must be at least 40 decimal digits")

    fixture = _load_linear_forms_fixture()
    q_recurrence = _load_shared_recurrence(fixture.q_recurrence_evidence_id)
    p_recurrence = MinimalRecurrenceIdentity(
        start_index=q_recurrence.start_index,
        initial_values=fixture.p_initial,
        terms=q_recurrence.terms,
    )
    phat_recurrence = MinimalRecurrenceIdentity(
        start_index=q_recurrence.start_index,
        initial_values=fixture.phat_initial,
        terms=q_recurrence.terms,
    )

    generation_limit = max_n + 1
    q_terms = generate_terms_from_recurrence(q_recurrence, max_index=generation_limit)
    p_terms = generate_terms_from_recurrence(p_recurrence, max_index=generation_limit)
    phat_terms = generate_terms_from_recurrence(phat_recurrence, max_index=generation_limit)

    q_by_index = {index: value for index, value in enumerate(q_terms)}
    p_by_index = {index: value for index, value in enumerate(p_terms)}
    phat_by_index = {index: value for index, value in enumerate(phat_terms)}

    p_residuals = recurrence_residuals(p_recurrence, values_by_index=p_by_index, end_n=max_n)
    phat_residuals = recurrence_residuals(phat_recurrence, values_by_index=phat_by_index, end_n=max_n)
    p_residual_by_n = {item.n: item.vanishes for item in p_residuals}
    phat_residual_by_n = {item.n: item.vanishes for item in phat_residuals}

    work_precision = precision + 20
    with mpmath.workdps(work_precision):
        zeta5 = mpmath.zeta(5)
        samples = []
        for n in range(max_n + 1):
            d_n = _lcm_upto(n)
            d_2n = _lcm_upto(2 * n)

            q_value = q_by_index[n]
            p_value = p_by_index[n]
            phat_value = phat_by_index[n]

            q_scaled = q_value * (d_n**5)
            p_scaled = p_value * (d_n**5)

            q_digits = len(str(abs(q_value.numerator)))
            p_numerator_digits = len(str(abs(p_value.numerator)))
            phat_numerator_digits = len(str(abs(phat_value.numerator)))

            q_root_estimate = None
            remainder_root_estimate = None
            gamma_estimate = None
            if n > 0:
                q_scaled_mpf = _mp_fraction(q_scaled)
                p_scaled_mpf = _mp_fraction(p_scaled)
                scaled_remainder = q_scaled_mpf * zeta5 - p_scaled_mpf
                q_root_estimate = float(mpmath.log(abs(q_scaled_mpf)) / n)
                remainder_root_estimate = float(mpmath.log(abs(scaled_remainder)) / n)
                gamma_estimate = float((q_root_estimate - remainder_root_estimate) / q_root_estimate)

            samples.append(
                SymmetricLinearFormsSample(
                    n=n,
                    q_digits=q_digits,
                    p_numerator_digits=p_numerator_digits,
                    p_denominator=p_value.denominator,
                    phat_numerator_digits=phat_numerator_digits,
                    phat_denominator=phat_value.denominator,
                    p_residual_zero=(True if n < p_recurrence.start_index else p_residual_by_n[n]),
                    phat_residual_zero=(True if n < phat_recurrence.start_index else phat_residual_by_n[n]),
                    q_root_estimate=q_root_estimate,
                    remainder_root_estimate=remainder_root_estimate,
                    gamma_estimate=gamma_estimate,
                )
            )

    latest = samples[-1]
    if latest.q_root_estimate is None or latest.remainder_root_estimate is None or latest.gamma_estimate is None:
        raise ValueError("expected a positive max_n to produce asymptotic estimates")

    decay_summary = build_decay_probe_summary(
        object_id="bz_totally_symmetric_remainder_pipeline",
        family="totally_symmetric",
        object_kind="remainder_pipeline",
        bridge_target_family="baseline",
        source_status="source_backed",
        exact_status="mixed",
        provenance_title=fixture.source_title,
        provenance_url=fixture.source_url,
        provenance_version=fixture.source_version,
        exact_indices=tuple(range(max_n + 1)),
        numeric_indices=tuple(range(1, max_n + 1)),
        max_verified_index=max_n,
        available_metrics=(
            DecayMetric(
                name="log_abs_scaled_q_over_n",
                latest_value=latest.q_root_estimate,
                published_value=None,
                description="Latest log|d_n^5 Q_n|/n estimate from the exact recurrence pipeline.",
            ),
            DecayMetric(
                name="log_abs_scaled_remainder_over_n",
                latest_value=latest.remainder_root_estimate,
                published_value=None,
                description="Latest log|d_n^5(Q_n zeta(5)-P_n)|/n estimate from numeric evaluation.",
            ),
            DecayMetric(
                name="gamma",
                latest_value=latest.gamma_estimate,
                published_value=fixture.published_gamma,
                description="Finite-n worthiness estimate for the totally symmetric anchor.",
            ),
        ),
        recommendation="Reuse this source-backed mixed exact/numeric remainder pipeline as the phase-2 decay probe anchor.",
    )

    return BZTotallySymmetricLinearFormsProbe(
        fixture_id=fixture.id,
        recurrence_evidence_id=fixture.q_recurrence_evidence_id,
        source_title=fixture.source_title,
        source_url=fixture.source_url,
        source_version=fixture.source_version,
        max_n=max_n,
        precision=precision,
        published_gamma=fixture.published_gamma,
        latest_q_root_estimate=latest.q_root_estimate,
        latest_remainder_root_estimate=latest.remainder_root_estimate,
        latest_gamma_estimate=latest.gamma_estimate,
        all_p_residuals_zero=all(sample.p_residual_zero for sample in samples if sample.n >= p_recurrence.start_index),
        all_phat_residuals_zero=all(sample.phat_residual_zero for sample in samples if sample.n >= phat_recurrence.start_index),
        decay_summary=decay_summary,
        samples=tuple(samples),
    )


def render_bz_totally_symmetric_linear_forms_report(*, max_n: int = 12, precision: int = 80) -> str:
    probe = build_bz_totally_symmetric_linear_forms_probe(max_n=max_n, precision=precision)
    lines = [
        "# Brown-Zudilin totally symmetric linear-form probe",
        "",
        f"- Fixture: `{probe.fixture_id}`",
        f"- Shared recurrence evidence: `{probe.recurrence_evidence_id}`",
        f"- Source: `{probe.source_title}` ({probe.source_url})",
        f"- Source version: `{probe.source_version}`",
        f"- Exact recurrence generation through `n={probe.max_n}`",
        f"- Precision for numeric remainders: `{probe.precision}` decimal digits",
        f"- `P_n` recurrence residuals: `{'pass' if probe.all_p_residuals_zero else 'fail'}`",
        f"- `hat P_n` recurrence residuals: `{'pass' if probe.all_phat_residuals_zero else 'fail'}`",
        f"- Latest `log|d_n^5 Q_n|/n`: `{probe.latest_q_root_estimate:.8f}` at `n={probe.max_n}`",
        f"- Latest `log|d_n^5(Q_n zeta(5)-P_n)|/n`: `{probe.latest_remainder_root_estimate:.8f}` at `n={probe.max_n}`",
        f"- Latest worthiness estimate: `{probe.latest_gamma_estimate:.8f}`",
        f"- Published worthiness for the totally symmetric anchor: `{probe.published_gamma:.8f}`",
        "- The finite-n worthiness estimates converge slowly and oscillate; treat them as calibration, not certification.",
        "- The probe trusts the shared recurrence and the published initial values; it does not enforce the paper's separate experimental denominator claims.",
        "- This is an exact remainder pipeline for the totally symmetric anchor, not yet for the Brown-Zudilin baseline seed.",
        f"- Normalized decay-probe object id: `{probe.decay_summary.object_id}`",
        "",
        "| n | q digits | P numerator digits | P denominator | phat numerator digits | phat denominator | p residual zero | phat residual zero | log|d_n^5 Q_n|/n | log|d_n^5 I'_n|/n | gamma est |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for sample in probe.samples:
        q_root = "" if sample.q_root_estimate is None else f"{sample.q_root_estimate:.8f}"
        remainder_root = "" if sample.remainder_root_estimate is None else f"{sample.remainder_root_estimate:.8f}"
        gamma_est = "" if sample.gamma_estimate is None else f"{sample.gamma_estimate:.8f}"
        lines.append(
            "| "
            + " | ".join(
                (
                    str(sample.n),
                    str(sample.q_digits),
                    str(sample.p_numerator_digits),
                    str(sample.p_denominator),
                    str(sample.phat_numerator_digits),
                    str(sample.phat_denominator),
                    "yes" if sample.p_residual_zero else "no",
                    "yes" if sample.phat_residual_zero else "no",
                    q_root,
                    remainder_root,
                    gamma_est,
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def write_bz_totally_symmetric_linear_forms_report(
    *,
    max_n: int = 12,
    precision: int = 80,
    output_path: str | Path | None = None,
) -> Path:
    output = DEFAULT_LINEAR_FORMS_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_bz_totally_symmetric_linear_forms_report(max_n=max_n, precision=precision),
        encoding="utf-8",
    )
    return output


def _load_linear_forms_fixture(path: str | Path = LINEAR_FORMS_FIXTURE_PATH) -> SymmetricLinearFormsFixture:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    root = payload["totally_symmetric_linear_forms"]
    source = root["source"]
    arithmetic = root["arithmetic"]
    published = root["published"]
    initial_values = root["initial_values"]
    return SymmetricLinearFormsFixture(
        id=str(root["id"]),
        q_recurrence_evidence_id=str(root["q_recurrence_evidence_id"]),
        source_title=str(source["title"]),
        source_url=str(source["url"]),
        source_version=str(source.get("version", "")),
        source_notes=str(source.get("notes", "")),
        q_initial=tuple(fraction_from_scalar(value) for value in initial_values["q"]),
        phat_initial=tuple(fraction_from_scalar(value) for value in initial_values["phat"]),
        p_initial=tuple(fraction_from_scalar(value) for value in initial_values["p"]),
        q_scale_label=str(arithmetic["q_scale"]),
        phat_scale_label=str(arithmetic["phat_scale"]),
        p_scale_label=str(arithmetic["p_scale"]),
        published_gamma=float(published["worthiness_gamma"]),
    )


def _load_shared_recurrence(evidence_id: str) -> MinimalRecurrenceIdentity:
    evidence = load_sequence_evidence_by_id(evidence_id)
    if evidence.recurrence is None:
        raise ValueError(f"evidence {evidence_id!r} does not contain a minimal recurrence")
    return evidence.recurrence


@lru_cache(maxsize=None)
def _lcm_upto(n: int) -> int:
    if n <= 1:
        return 1
    return _lcm(_lcm_upto(n - 1), n)


def _lcm(left: int, right: int) -> int:
    return abs(left * right) // gcd(left, right)


def _mp_fraction(value: Fraction) -> mpmath.mpf:
    return mpmath.mpf(value.numerator) / value.denominator
