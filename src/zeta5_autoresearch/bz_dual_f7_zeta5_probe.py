from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mpmath
import yaml

from .bz_dual_f7 import compute_f7_zeta5_signature_from_a, dual_b_vector_from_a, scale_b_vector
from .config import DATA_DIR, REPO_ROOT
from .gate2.sequence_identity import ProvisionalSequenceIdentity, compute_provisional_sequence_hash

DUAL_F7_ZETA5_FIXTURE_PATH = REPO_ROOT / "regression" / "fixtures" / "bz_dual_f7_zeta5_probe.yaml"
DEFAULT_DUAL_F7_ZETA5_REPORT_PATH = DATA_DIR / "logs" / "bz_dual_f7_zeta5_probe_report.md"


@dataclass(frozen=True)
class DualF7Zeta5CaseFixture:
    id: str
    label: str
    a: tuple[int, ...]
    start_index: int
    term_count: int


@dataclass(frozen=True)
class DualF7Zeta5ProbeFixture:
    id: str
    source_title: str
    source_url: str
    source_version: str
    source_notes: str
    cases: tuple[DualF7Zeta5CaseFixture, ...]


@dataclass(frozen=True)
class DualF7Zeta5Sample:
    n: int
    b0: int
    coefficient: int
    digits: int
    log10_abs_coefficient: float
    log_abs_over_n: float


@dataclass(frozen=True)
class DualF7Zeta5CaseProbe:
    id: str
    label: str
    a: tuple[int, ...]
    base_b: tuple[int, ...]
    sequence_hash: str
    samples: tuple[DualF7Zeta5Sample, ...]


@dataclass(frozen=True)
class BZDualF7Zeta5Probe:
    fixture_id: str
    source_title: str
    source_url: str
    source_version: str
    source_notes: str
    cases: tuple[DualF7Zeta5CaseProbe, ...]


def build_bz_dual_f7_zeta5_probe() -> BZDualF7Zeta5Probe:
    fixture = _load_dual_f7_zeta5_fixture()
    cases = []
    for case in fixture.cases:
        signature = compute_f7_zeta5_signature_from_a(
            case.a,
            start_index=case.start_index,
            term_count=case.term_count,
        )
        provisional = ProvisionalSequenceIdentity.from_scalars(
            start_index=case.start_index,
            order_bound=max(1, len(signature) - 1),
            initial_data=signature[: min(2, len(signature))],
            signature=signature,
        )
        sequence_hash = compute_provisional_sequence_hash(provisional)
        base_b = dual_b_vector_from_a(case.a)
        samples = []
        for offset, coefficient in enumerate(signature):
            n = case.start_index + offset
            b = scale_b_vector(base_b, n)
            with mpmath.workdps(80):
                log10_abs = float(mpmath.log10(abs(coefficient)))
                log_abs_over_n = float(mpmath.log(abs(coefficient)) / n)
            samples.append(
                DualF7Zeta5Sample(
                    n=n,
                    b0=b[0],
                    coefficient=coefficient,
                    digits=len(str(abs(coefficient))),
                    log10_abs_coefficient=log10_abs,
                    log_abs_over_n=log_abs_over_n,
                )
            )
        cases.append(
            DualF7Zeta5CaseProbe(
                id=case.id,
                label=case.label,
                a=case.a,
                base_b=base_b,
                sequence_hash=sequence_hash,
                samples=tuple(samples),
            )
        )

    return BZDualF7Zeta5Probe(
        fixture_id=fixture.id,
        source_title=fixture.source_title,
        source_url=fixture.source_url,
        source_version=fixture.source_version,
        source_notes=fixture.source_notes,
        cases=tuple(cases),
    )


def render_bz_dual_f7_zeta5_probe_report() -> str:
    probe = build_bz_dual_f7_zeta5_probe()
    lines = [
        "# Brown-Zudilin dual F_7 zeta(5)-coefficient probe",
        "",
        f"- Fixture: `{probe.fixture_id}`",
        f"- Source: `{probe.source_title}` ({probe.source_url})",
        f"- Source version: `{probe.source_version}`",
        "- The coefficients here are exact integers extracted from the reduced fifth-order pole data of the displayed F_7 summand.",
        "- Each case is hashed as a provisional exact-term sequence object, not yet as a verified recurrence.",
        "",
    ]
    for case in probe.cases:
        signature = [sample.coefficient for sample in case.samples]
        lines.extend(
            [
                f"## {case.label}",
                "",
                f"- Case id: `{case.id}`",
                f"- Base `a`: `{case.a}`",
                f"- Base `b`: `{case.base_b}`",
                f"- Provisional sequence hash: `{case.sequence_hash}`",
                f"- Exact signature: `{signature}`",
                "",
                "| n | scaled b0 | digits | log10|coeff| | log|coeff|/n | coeff preview |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for sample in case.samples:
            lines.append(
                "| "
                + " | ".join(
                    (
                        str(sample.n),
                        str(sample.b0),
                        str(sample.digits),
                        f"{sample.log10_abs_coefficient:.6f}",
                        f"{sample.log_abs_over_n:.8f}",
                        _preview_integer(sample.coefficient),
                    )
                )
                + " |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def write_bz_dual_f7_zeta5_probe_report(*, output_path: str | Path | None = None) -> Path:
    output = DEFAULT_DUAL_F7_ZETA5_REPORT_PATH if output_path is None else Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_bz_dual_f7_zeta5_probe_report(), encoding="utf-8")
    return output


def _preview_integer(value: int, *, edge_digits: int = 12) -> str:
    text = str(value)
    if len(text) <= 2 * edge_digits + 3:
        return text
    return f"{text[:edge_digits]}...{text[-edge_digits:]}"


def _load_dual_f7_zeta5_fixture() -> DualF7Zeta5ProbeFixture:
    payload = yaml.safe_load(DUAL_F7_ZETA5_FIXTURE_PATH.read_text(encoding="utf-8"))
    root = payload["dual_f7_zeta5_probe"]
    source = root["source"]
    cases = []
    for item in root["cases"]:
        cases.append(
            DualF7Zeta5CaseFixture(
                id=str(item["id"]),
                label=str(item["label"]),
                a=tuple(int(value) for value in item["a"]),
                start_index=int(item["start_index"]),
                term_count=int(item["term_count"]),
            )
        )
    return DualF7Zeta5ProbeFixture(
        id=str(root["id"]),
        source_title=str(source["title"]),
        source_url=str(source["url"]),
        source_version=str(source["version"]),
        source_notes=str(source["notes"]),
        cases=tuple(cases),
    )
