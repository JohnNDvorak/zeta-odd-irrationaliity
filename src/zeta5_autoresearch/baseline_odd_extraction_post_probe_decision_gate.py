from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_odd_extraction_probe import (
    BASELINE_ODD_EXTRACTION_PROBE_REPORT_PATH,
    build_baseline_odd_extraction_probe,
)
from .config import CACHE_DIR, DATA_DIR

BASELINE_ODD_EXTRACTION_POST_PROBE_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_odd_extraction_post_probe_decision_gate.md"
)
BASELINE_ODD_EXTRACTION_POST_PROBE_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_odd_extraction_post_probe_decision_gate.json"
)


@dataclass(frozen=True)
class BaselineOddExtractionDecisionStatus:
    criterion_id: str
    verdict: str
    note: str


@dataclass(frozen=True)
class BaselineOddExtractionPostProbeDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[BaselineOddExtractionDecisionStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    non_claims: tuple[str, ...]


def build_baseline_odd_extraction_post_probe_decision_gate() -> BaselineOddExtractionPostProbeDecisionGate:
    probe = build_baseline_odd_extraction_probe()
    return BaselineOddExtractionPostProbeDecisionGate(
        gate_id="bz_phase2_baseline_odd_extraction_post_probe_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=(
            BaselineOddExtractionDecisionStatus(
                criterion_id="baseline_native_object",
                verdict="satisfied",
                note="The probe establishes a baseline-native odd-pair extraction summary rather than another bridge-fit analog object.",
            ),
            BaselineOddExtractionDecisionStatus(
                criterion_id="reproducible_hashes",
                verdict="satisfied",
                note="Retained odd-pair output, unresolved constant residual, and full extraction summary are reproducible via exact hashes.",
            ),
            BaselineOddExtractionDecisionStatus(
                criterion_id="projection_alignment",
                verdict="satisfied",
                note="The active object keeps the odd-zeta channels together, which is better aligned with the projection story than the previous retained pair.",
            ),
            BaselineOddExtractionDecisionStatus(
                criterion_id="residual_elimination",
                verdict="not_yet_satisfied",
                note="The constant residual remains explicit and unresolved, so extraction has not yet reached a baseline remainder or P_n object.",
            ),
        ),
        outcome="continue_baseline_odd_extraction",
        rationale=(
            "The odd-pair extraction probe is strong enough to justify one bounded residual-refinement ladder: it preserves "
            "baseline-native semantics, exact hashes, and a better odd-weight alignment without relying on bridge-fit identities."
        ),
        next_step=(
            "Implement the odd-pair residual-refinement ladder as a strictly baseline-side refinement of the retained odd pair, "
            "with the goal of reducing or reclassifying the constant residual without claiming elimination prematurely."
        ),
        non_claims=(
            "This does not claim a baseline `P_n` extraction.",
            "This does not claim a proved baseline remainder pipeline.",
            "This does not justify reopening broad bridge-map experimentation as the main line.",
        ),
    )


def render_baseline_odd_extraction_post_probe_decision_gate() -> str:
    gate = build_baseline_odd_extraction_post_probe_decision_gate()
    lines = [
        "# Phase 2 baseline odd extraction post-probe decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{BASELINE_ODD_EXTRACTION_PROBE_REPORT_PATH}`",
        f"- Source probe id: `{gate.source_probe_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        f"- Outcome: `{gate.outcome}`",
        "",
        "| criterion | verdict | note |",
        "| --- | --- | --- |",
    ]
    for item in gate.statuses:
        lines.append(f"| `{item.criterion_id}` | `{item.verdict}` | {item.note} |")
    lines.extend(
        [
            "",
            "## Rationale",
            "",
            gate.rationale,
            "",
            "## Next step",
            "",
            gate.next_step,
            "",
            "## Non-claims",
            "",
        ]
    )
    for item in gate.non_claims:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def write_baseline_odd_extraction_post_probe_decision_gate_report(
    output_path: str | Path = BASELINE_ODD_EXTRACTION_POST_PROBE_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_odd_extraction_post_probe_decision_gate(), encoding="utf-8")
    return output


def write_baseline_odd_extraction_post_probe_decision_gate_json(
    output_path: str | Path = BASELINE_ODD_EXTRACTION_POST_PROBE_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_baseline_odd_extraction_post_probe_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_odd_extraction_post_probe_decision_gate_report()
    write_baseline_odd_extraction_post_probe_decision_gate_json()


if __name__ == "__main__":
    main()
