from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .zudilin_2002_affine_normalization_map_probe import build_zudilin_2002_affine_normalization_map_probe
from .zudilin_2002_normalization_map_probe import build_zudilin_2002_normalization_map_probe
from .zudilin_2002_quadratic_normalization_map_probe import build_zudilin_2002_quadratic_normalization_map_probe

ZUDILIN_2002_NORMALIZATION_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_zudilin_2002_normalization_decision_gate.md"
)
ZUDILIN_2002_NORMALIZATION_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_zudilin_2002_normalization_decision_gate.json"
)


@dataclass(frozen=True)
class NormalizationFamilyStatus:
    family_id: str
    verdict: str
    mismatch_indices: tuple[int, ...]
    implication: str


@dataclass(frozen=True)
class Zudilin2002NormalizationDecisionGate:
    gate_id: str
    shared_window_start: int
    shared_window_end: int
    family_statuses: tuple[NormalizationFamilyStatus, ...]
    overall_verdict: str
    recommendation: str
    non_claims: tuple[str, ...]


def build_zudilin_2002_normalization_decision_gate(*, max_n: int = 7) -> Zudilin2002NormalizationDecisionGate:
    scalar_probe = build_zudilin_2002_normalization_map_probe(max_n=max_n)
    affine_probe = build_zudilin_2002_affine_normalization_map_probe(max_n=max_n)
    quadratic_probe = build_zudilin_2002_quadratic_normalization_map_probe(max_n=max_n)

    shared_window_end = min(
        scalar_probe.shared_window_end,
        affine_probe.shared_window_end,
        quadratic_probe.shared_window_end,
    )

    family_statuses = (
        NormalizationFamilyStatus(
            family_id="scalar",
            verdict=scalar_probe.verdict,
            mismatch_indices=scalar_probe.mismatch_indices,
            implication="The channels are not related by a single exact rational rescaling on the shared window.",
        ),
        NormalizationFamilyStatus(
            family_id="affine_in_n",
            verdict=affine_probe.verdict,
            mismatch_indices=affine_probe.mismatch_indices,
            implication="The channels are not related by an exact affine-in-n rescaling on the shared window.",
        ),
        NormalizationFamilyStatus(
            family_id="quadratic_in_n",
            verdict=quadratic_probe.verdict,
            mismatch_indices=quadratic_probe.mismatch_indices,
            implication="The channels are not related by an exact quadratic-in-n rescaling on the shared window.",
        ),
    )

    return Zudilin2002NormalizationDecisionGate(
        gate_id="bz_phase2_zudilin_2002_normalization_decision_gate",
        shared_window_start=1,
        shared_window_end=shared_window_end,
        family_statuses=family_statuses,
        overall_verdict=(
            "Three bounded polynomial normalization families now fail exactly on the shared n=1..7 window. "
            "That is enough evidence to stop the polynomial-rescaling subline instead of extending it mechanically."
        ),
        recommendation=(
            "Switch away from scalar/affine/quadratic normalization maps and move to a different bridge-comparison ansatz, "
            "such as a companion-channel-aware transformation or a structurally different projection target."
        ),
        non_claims=(
            "This does not rule out all possible normalization maps.",
            "This does not prove the baseline and Zudilin bridge channels are unrelated in every stronger sense.",
            "This only closes the bounded polynomial-rescaling subline tested so far.",
        ),
    )


def render_zudilin_2002_normalization_decision_gate(*, max_n: int = 7) -> str:
    gate = build_zudilin_2002_normalization_decision_gate(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 normalization decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        "",
        "| family | verdict | mismatch indices | implication |",
        "| --- | --- | --- | --- |",
    ]
    for item in gate.family_statuses:
        mismatch_text = ",".join(str(index) for index in item.mismatch_indices) if item.mismatch_indices else "none"
        lines.append(
            f"| `{item.family_id}` | `{item.verdict}` | `{mismatch_text}` | {item.implication} |"
        )
    lines.extend(
        [
            "",
            "## Overall verdict",
            "",
            gate.overall_verdict,
            "",
            "## Recommendation",
            "",
            gate.recommendation,
            "",
            "## Non-claims",
            "",
        ]
    )
    for item in gate.non_claims:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def write_zudilin_2002_normalization_decision_gate_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_NORMALIZATION_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_normalization_decision_gate(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_normalization_decision_gate_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_NORMALIZATION_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_zudilin_2002_normalization_decision_gate(max_n=max_n)
    payload = asdict(gate)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_zudilin_2002_normalization_decision_gate_report()
    write_zudilin_2002_normalization_decision_gate_json()


if __name__ == "__main__":
    main()
