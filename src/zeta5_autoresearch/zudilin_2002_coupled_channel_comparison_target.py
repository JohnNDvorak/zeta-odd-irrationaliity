from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .zudilin_2002_companion_channel_ansatz import (
    ZUDILIN_2002_COMPANION_CHANNEL_ANSATZ_REPORT_PATH,
    build_zudilin_2002_companion_channel_ansatz,
)

ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_TARGET_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_zudilin_2002_coupled_channel_comparison_target.md"
)
ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_TARGET_JSON_PATH = (
    CACHE_DIR / "bz_phase2_zudilin_2002_coupled_channel_comparison_target.json"
)


@dataclass(frozen=True)
class CoupledComparisonField:
    field_id: str
    baseline_object: str
    bridge_object: str
    status: str
    next_artifact: str


@dataclass(frozen=True)
class Zudilin2002CoupledChannelComparisonTarget:
    target_id: str
    bridge_id: str
    shared_window_start: int
    shared_window_end: int
    target_label: str
    coupled_object_label: str
    fields: tuple[CoupledComparisonField, ...]
    target_verdict: str
    recommendation: str


def build_zudilin_2002_coupled_channel_comparison_target(
    *, max_n: int = 7
) -> Zudilin2002CoupledChannelComparisonTarget:
    ansatz = build_zudilin_2002_companion_channel_ansatz(max_n=max_n)
    return Zudilin2002CoupledChannelComparisonTarget(
        target_id="bz_phase2_zudilin_2002_coupled_channel_comparison_target",
        bridge_id=ansatz.bridge_id,
        shared_window_start=ansatz.shared_window_start,
        shared_window_end=ansatz.shared_window_end,
        target_label="Ordered-pair coupled comparison target",
        coupled_object_label="(baseline ζ(5), baseline ζ(3)) versus (bridge ζ(5), bridge ζ(3))",
        fields=(
            CoupledComparisonField(
                field_id="baseline_coupled_object",
                baseline_object="finite-window exact ordered pair `(baseline ζ(5), baseline ζ(3))`",
                bridge_object="published ordered pair `(q_n ζ(5)-p_n, q_n ζ(3)-p̃_n)`",
                status="ready_for_hash_probe",
                next_artifact="paired object hash on the shared window",
            ),
            CoupledComparisonField(
                field_id="channel_ordering_contract",
                baseline_object="target-first, companion-second ordering",
                bridge_object="target-first, companion-second ordering",
                status="ready_for_hash_probe",
                next_artifact="ordered-pair comparison payload",
            ),
            CoupledComparisonField(
                field_id="sequence_strength_disclaimer",
                baseline_object="finite-window exact packet",
                bridge_object="recurrence-explicit bridge object",
                status="must_remain_explicit",
                next_artifact="paired comparison verdict with asymmetry disclaimer",
            ),
        ),
        target_verdict=(
            "The coupled two-channel comparison object is now specified cleanly enough to probe directly on the shared window."
        ),
        recommendation=(
            "Build the paired comparison probe next: hash the ordered baseline pair and the ordered bridge pair on `n=1..7`, "
            "and report them as comparison-ready but not recurrence-equivalent."
        ),
    )


def render_zudilin_2002_coupled_channel_comparison_target(*, max_n: int = 7) -> str:
    target = build_zudilin_2002_coupled_channel_comparison_target(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 coupled-channel comparison target",
        "",
        f"- Target id: `{target.target_id}`",
        f"- Bridge id: `{target.bridge_id}`",
        f"- Shared exact window: `n={target.shared_window_start}..{target.shared_window_end}`",
        f"- Companion-channel ansatz: `{ZUDILIN_2002_COMPANION_CHANNEL_ANSATZ_REPORT_PATH}`",
        f"- Target label: {target.target_label}",
        f"- Coupled object: {target.coupled_object_label}",
        "",
        "| field | baseline object | bridge object | status | next artifact |",
        "| --- | --- | --- | --- | --- |",
    ]
    for field in target.fields:
        lines.append(
            f"| `{field.field_id}` | {field.baseline_object} | {field.bridge_object} | `{field.status}` | {field.next_artifact} |"
        )
    lines.extend(
        [
            "",
            "## Target verdict",
            "",
            target.target_verdict,
            "",
            "## Recommendation",
            "",
            target.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_zudilin_2002_coupled_channel_comparison_target_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_TARGET_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_coupled_channel_comparison_target(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_coupled_channel_comparison_target_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COUPLED_CHANNEL_COMPARISON_TARGET_JSON_PATH,
) -> Path:
    target = build_zudilin_2002_coupled_channel_comparison_target(max_n=max_n)
    payload = asdict(target)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_zudilin_2002_coupled_channel_comparison_target_report()
    write_zudilin_2002_coupled_channel_comparison_target_json()


if __name__ == "__main__":
    main()
