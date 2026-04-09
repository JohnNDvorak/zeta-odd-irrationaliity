from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import mpmath

from .config import DATA_DIR

ZUDILIN_2002_BRIDGE_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_zudilin_2002_bridge_probe.md"


@dataclass(frozen=True)
class Zudilin2002Sample:
    n: int
    q_n: int
    p_n: Fraction
    ptilde_n: Fraction
    zeta5_error: float
    zeta3_error: float


@dataclass(frozen=True)
class Zudilin2002BridgeProbe:
    probe_id: str
    source_title: str
    source_location: str
    samples: tuple[Zudilin2002Sample, ...]


def build_zudilin_2002_bridge_probe(*, max_n: int = 7, precision: int = 80) -> Zudilin2002BridgeProbe:
    if max_n < 2:
        raise ValueError("max_n must be at least 2")

    q_terms, p_terms, ptilde_terms = _compute_terms(max_n)
    samples = []
    with mpmath.workdps(precision):
        zeta5 = mpmath.zeta(5)
        zeta3 = mpmath.zeta(3)
        for n in range(max_n + 1):
            q_n = q_terms[n]
            p_n = p_terms[n]
            ptilde_n = ptilde_terms[n]
            zeta5_error = abs(zeta5 - (mpmath.mpf(p_n.numerator) / p_n.denominator) / q_n)
            zeta3_error = abs(zeta3 - (mpmath.mpf(ptilde_n.numerator) / ptilde_n.denominator) / q_n)
            samples.append(
                Zudilin2002Sample(
                    n=n,
                    q_n=q_n,
                    p_n=p_n,
                    ptilde_n=ptilde_n,
                    zeta5_error=float(zeta5_error),
                    zeta3_error=float(zeta3_error),
                )
            )
    return Zudilin2002BridgeProbe(
        probe_id="bz_phase2_zudilin_2002_bridge_probe",
        source_title="Zudilin, A third-order Apéry-like recursion for ζ(5) (2002)",
        source_location="Theorem 1, equations (1) and (2)",
        samples=tuple(samples),
    )


def render_zudilin_2002_bridge_probe(*, max_n: int = 7, precision: int = 80) -> str:
    probe = build_zudilin_2002_bridge_probe(max_n=max_n, precision=precision)
    lines = [
        "# Phase 2 Zudilin 2002 bridge probe",
        "",
        f"- Probe id: `{probe.probe_id}`",
        f"- Source: `{probe.source_title}`",
        f"- Location: `{probe.source_location}`",
        "- This probe encodes the published third-order recurrence and initial data for the explicit bridge object.",
        "- `q_n`, `p_n`, and `p̃_n` are generated exactly from the theorem statement.",
        "",
        "| n | q_n | p_n / q_n | p̃_n / q_n | |ζ(5)-p_n/q_n| | |ζ(3)-p̃_n/q_n| |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for sample in probe.samples:
        lines.append(
            "| "
            + " | ".join(
                (
                    str(sample.n),
                    str(sample.q_n),
                    _format_fraction_ratio(sample.p_n, sample.q_n),
                    _format_fraction_ratio(sample.ptilde_n, sample.q_n),
                    f"{sample.zeta5_error:.6e}",
                    f"{sample.zeta3_error:.6e}",
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This is the first repo-native encoding of the external bridge object chosen by the phase-2 decision gate.",
            "- It is recurrence-explicit, unlike the current baseline dual packet, and is therefore stronger at the sequence-object level.",
            "",
        ]
    )
    return "\n".join(lines)


def write_zudilin_2002_bridge_probe_report(
    *,
    max_n: int = 7,
    precision: int = 80,
    output_path: str | Path = ZUDILIN_2002_BRIDGE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_bridge_probe(max_n=max_n, precision=precision), encoding="utf-8")
    return output


def _compute_terms(max_n: int) -> tuple[list[int], list[Fraction], list[Fraction]]:
    q_terms = [-1, 42, -17934]
    p_terms = [Fraction(0), Fraction(87, 2), Fraction(-1190161, 64)]
    ptilde_terms = [Fraction(0), Fraction(101, 2), Fraction(-344923, 16)]

    for n in range(2, max_n):
        q_terms.append(_next_term(q_terms, n))
        p_terms.append(_next_term(p_terms, n))
        ptilde_terms.append(_next_term(ptilde_terms, n))
    return q_terms, p_terms, ptilde_terms


def _next_term(sequence: list[int] | list[Fraction], n: int) -> Fraction:
    q_n = Fraction(sequence[n])
    q_nm1 = Fraction(sequence[n - 1])
    q_nm2 = Fraction(sequence[n - 2])
    numerator = (
        -_a1(n) * q_n
        + 4 * (2 * n - 1) * _a2(n) * q_nm1
        + 4 * (n - 1) ** 4 * (2 * n - 1) * (2 * n - 3) * _a0(n + 1) * q_nm2
    )
    denominator = (n + 1) ** 6 * _a0(n)
    return numerator / denominator


def _a0(n: int) -> int:
    return 41218 * n**3 - 48459 * n**2 + 20010 * n - 2871


def _a1(n: int) -> int:
    return 2 * (
        48802112 * n**9
        + 89030880 * n**8
        + 36002654 * n**7
        - 24317344 * n**6
        - 19538418 * n**5
        + 1311365 * n**4
        + 3790503 * n**3
        + 460056 * n**2
        - 271701 * n
        - 60291
    )


def _a2(n: int) -> int:
    return (
        3874492 * n**8
        - 2617900 * n**7
        - 3144314 * n**6
        + 2947148 * n**5
        + 647130 * n**4
        - 1182926 * n**3
        + 115771 * n**2
        + 170716 * n
        - 44541
    )


def _format_fraction_ratio(value: Fraction, denominator: int) -> str:
    ratio = value / denominator
    if ratio.denominator == 1:
        return str(ratio.numerator)
    return f"{ratio.numerator}/{ratio.denominator}"


def main() -> None:
    write_zudilin_2002_bridge_probe_report()


if __name__ == "__main__":
    main()
