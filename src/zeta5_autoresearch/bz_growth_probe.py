from __future__ import annotations

from dataclasses import dataclass
from math import log
from pathlib import Path

import yaml

from .baseline_q_cache import get_cached_baseline_q_terms
from .bz_q_sequence import baseline_a_vector, compute_q_term_from_a
from .config import DATA_DIR, REPO_ROOT
from .sequence_evidence import load_sequence_evidence_by_id

BASELINE_CONSTANTS_PATH = REPO_ROOT / "regression" / "fixtures" / "bz_baseline_constants.yaml"
DEFAULT_GROWTH_REPORT_PATH = DATA_DIR / "logs" / "bz_baseline_growth_report.md"


@dataclass(frozen=True)
class GrowthSample:
    n: int
    sign: str
    digits: int
    bit_length: int
    log_abs_root_est: float | None
    log_abs_ratio_est: float | None
    c1_accel_est: float | None


@dataclass(frozen=True)
class BZBaselineGrowthProbe:
    evidence_id: str
    source_title: str
    source_url: str
    max_n: int
    published_c1: float
    evidence_signature_match: bool
    evidence_initial_data_match: bool
    samples: tuple[GrowthSample, ...]

    @property
    def latest_root_estimate(self) -> float:
        value = self.samples[-1].log_abs_root_est
        if value is None:
            raise ValueError("latest root estimate is unavailable")
        return value

    @property
    def latest_ratio_estimate(self) -> float:
        value = self.samples[-1].log_abs_ratio_est
        if value is None:
            raise ValueError("latest ratio estimate is unavailable")
        return value

    @property
    def latest_accelerated_c1_estimate(self) -> float:
        value = self.samples[-1].c1_accel_est
        if value is None:
            raise ValueError("latest accelerated C1 estimate is unavailable")
        return value

    @property
    def latest_accelerated_c1_delta(self) -> float:
        return self.latest_accelerated_c1_estimate - self.published_c1


def build_bz_baseline_growth_probe(*, max_n: int = 20) -> BZBaselineGrowthProbe:
    if max_n < 2:
        raise ValueError("max_n must be at least 2")

    evidence = load_sequence_evidence_by_id("bz_baseline_q_signature_v1")
    published_c1 = _load_published_c1()
    validation_max_n = max(max_n, evidence.start_index + len(evidence.signature) - 1)
    terms = get_cached_baseline_q_terms(validation_max_n)
    logs = [log(abs(term)) for term in terms]
    samples = []

    for n in range(max_n + 1):
        ratio = None if n == 0 else logs[n] - logs[n - 1]
        if n < 2:
            accelerated = None
        else:
            previous_ratio = logs[n - 1] - logs[n - 2]
            # Eliminate the leading 1/n drift in the ratio model d_n = C1 + A/n + O(1/n^2).
            accelerated = n * ratio - (n - 1) * previous_ratio
        term = terms[n]
        samples.append(
            GrowthSample(
                n=n,
                sign="+" if term > 0 else "-",
                digits=len(str(abs(term))),
                bit_length=abs(term).bit_length(),
                log_abs_root_est=None if n == 0 else logs[n] / n,
                log_abs_ratio_est=ratio,
                c1_accel_est=accelerated,
            )
        )

    signature_slice = tuple(str(value) for value in terms[evidence.start_index : evidence.start_index + len(evidence.signature)])
    initial_slice = tuple(str(value) for value in terms[evidence.start_index : evidence.start_index + len(evidence.initial_data)])
    return BZBaselineGrowthProbe(
        evidence_id=evidence.id,
        source_title=evidence.source_title,
        source_url=evidence.source_url,
        max_n=max_n,
        published_c1=published_c1,
        evidence_signature_match=signature_slice == evidence.signature,
        evidence_initial_data_match=initial_slice == evidence.initial_data,
        samples=tuple(samples),
    )


def render_bz_baseline_growth_report(*, max_n: int = 20) -> str:
    probe = build_bz_baseline_growth_probe(max_n=max_n)
    lines = [
        "# Brown-Zudilin baseline Q_n growth probe",
        "",
        f"- Evidence id: `{probe.evidence_id}`",
        f"- Source: `{probe.source_title}` ({probe.source_url})",
        f"- Exact terms recomputed through `n={probe.max_n}` from the published `Q(p;q)` double-sum specialization.",
        f"- Seeded signature check: `{'pass' if probe.evidence_signature_match else 'fail'}`",
        f"- Seeded initial-data check: `{'pass' if probe.evidence_initial_data_match else 'fail'}`",
        f"- Published target `C1`: `{probe.published_c1:.8f}`",
        f"- Latest `log|Q_n|/n`: `{probe.latest_root_estimate:.8f}` at `n={probe.max_n}`",
        f"- Latest `log|Q_n/Q_(n-1)|`: `{probe.latest_ratio_estimate:.8f}` at `n={probe.max_n}`",
        f"- Latest accelerated `C1` estimate: `{probe.latest_accelerated_c1_estimate:.8f}`",
        f"- Accelerated delta vs published `C1`: `{probe.latest_accelerated_c1_delta:+.8f}`",
        "- This is an uncertified numeric calibration on `Q_n` only; it does not estimate `C2`, `gamma`, or `M_proof`.",
        "",
        "| n | sign | digits | bit_length | log|Q_n|/n | log|Q_n/Q_(n-1)| | accelerated C1 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for sample in probe.samples:
        lines.append(
            "| "
            + " | ".join(
                (
                    str(sample.n),
                    sample.sign,
                    str(sample.digits),
                    str(sample.bit_length),
                    _format_optional_float(sample.log_abs_root_est),
                    _format_optional_float(sample.log_abs_ratio_est),
                    _format_optional_float(sample.c1_accel_est),
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def write_bz_baseline_growth_report(*, max_n: int = 20, output_path: str | Path | None = None) -> Path:
    output = DEFAULT_GROWTH_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_bz_baseline_growth_report(max_n=max_n), encoding="utf-8")
    return output

def _load_published_c1(path: Path = BASELINE_CONSTANTS_PATH) -> float:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    baseline = payload["baseline"]
    return float(baseline["C1"])


def _format_optional_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.8f}"
