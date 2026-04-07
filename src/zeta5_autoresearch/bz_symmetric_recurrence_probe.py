from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from .bz_q_sequence import compute_q_term_from_a, totally_symmetric_a_vector
from .config import DATA_DIR, REPO_ROOT
from .gate0_parse import parse_candidate_file
from .gate2.recurrence_eval import generate_terms_from_recurrence, recurrence_residuals
from .sequence_evidence import load_sequence_evidence_by_id, resolve_candidate_sequence_evidence

TOTALLY_SYMMETRIC_SEED_PATH = REPO_ROOT / "specs" / "totally_symmetric_bz_seed.yaml"
DEFAULT_SYMMETRIC_REPORT_PATH = DATA_DIR / "logs" / "bz_totally_symmetric_recurrence_report.md"


@dataclass(frozen=True)
class SymmetricRecurrenceSample:
    n: int
    direct_digits: int
    recurrence_digits: int
    exact_match: bool
    residual_zero: bool


@dataclass(frozen=True)
class BZTotallySymmetricRecurrenceProbe:
    candidate_id: str
    evidence_id: str
    sequence_hash_status: str
    sequence_hash: str
    certificate_hash: str
    source_title: str
    source_url: str
    max_n: int
    all_exact_matches: bool
    all_residuals_zero: bool
    samples: tuple[SymmetricRecurrenceSample, ...]


def build_bz_totally_symmetric_recurrence_probe(*, max_n: int = 10) -> BZTotallySymmetricRecurrenceProbe:
    if max_n < 3:
        raise ValueError("max_n must be at least 3")

    seed = parse_candidate_file(TOTALLY_SYMMETRIC_SEED_PATH)
    candidate, evidence = resolve_candidate_sequence_evidence(seed)
    if evidence is None or evidence.recurrence is None:
        raise ValueError("totally symmetric seed requires minimal recurrence evidence")

    direct_terms = {
        n: Fraction(compute_q_term_from_a(totally_symmetric_a_vector(), n))
        for n in range(max_n + 2)
    }
    recurrence_terms = generate_terms_from_recurrence(evidence.recurrence, max_index=max_n)
    recurrence_by_index = {index: value for index, value in enumerate(recurrence_terms)}
    residuals = recurrence_residuals(evidence.recurrence, values_by_index=direct_terms, end_n=max_n)
    residual_by_n = {item.n: item for item in residuals}

    samples = []
    for n in range(max_n + 1):
        direct_value = direct_terms[n]
        recurrence_value = recurrence_by_index[n]
        samples.append(
            SymmetricRecurrenceSample(
                n=n,
                direct_digits=len(str(abs(direct_value.numerator))),
                recurrence_digits=len(str(abs(recurrence_value.numerator))),
                exact_match=direct_value == recurrence_value,
                residual_zero=(True if n < evidence.recurrence.start_index else residual_by_n[n].vanishes),
            )
        )

    return BZTotallySymmetricRecurrenceProbe(
        candidate_id=candidate.id or "",
        evidence_id=evidence.id,
        sequence_hash_status=evidence.sequence_hash_status,
        sequence_hash=candidate.sequence_hash or "",
        certificate_hash=candidate.certificate_hash or "",
        source_title=evidence.source_title,
        source_url=evidence.source_url,
        max_n=max_n,
        all_exact_matches=all(sample.exact_match for sample in samples),
        all_residuals_zero=all(sample.residual_zero for sample in samples if sample.n >= evidence.recurrence.start_index),
        samples=tuple(samples),
    )


def render_bz_totally_symmetric_recurrence_report(*, max_n: int = 10) -> str:
    probe = build_bz_totally_symmetric_recurrence_probe(max_n=max_n)
    lines = [
        "# Brown-Zudilin totally symmetric recurrence anchor",
        "",
        f"- Candidate: `{probe.candidate_id}`",
        f"- Evidence id: `{probe.evidence_id}`",
        f"- Sequence hash status: `{probe.sequence_hash_status}`",
        f"- Sequence hash: `{probe.sequence_hash}`",
        f"- Certificate hash: `{probe.certificate_hash}`",
        f"- Source: `{probe.source_title}` ({probe.source_url})",
        f"- Exact formula vs recurrence agreement through `n={probe.max_n}`: `{'pass' if probe.all_exact_matches else 'fail'}`",
        f"- Recurrence residual check through `n={probe.max_n}`: `{'pass' if probe.all_residuals_zero else 'fail'}`",
        "- This is a verified sequence-identity anchor for the totally symmetric family, not for the Brown-Zudilin baseline seed.",
        "",
        "| n | direct digits | recurrence digits | exact match | residual zero |",
        "| --- | --- | --- | --- | --- |",
    ]
    for sample in probe.samples:
        lines.append(
            "| "
            + " | ".join(
                (
                    str(sample.n),
                    str(sample.direct_digits),
                    str(sample.recurrence_digits),
                    "yes" if sample.exact_match else "no",
                    "yes" if sample.residual_zero else "no",
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def write_bz_totally_symmetric_recurrence_report(*, max_n: int = 10, output_path: str | Path | None = None) -> Path:
    output = DEFAULT_SYMMETRIC_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_bz_totally_symmetric_recurrence_report(max_n=max_n), encoding="utf-8")
    return output
