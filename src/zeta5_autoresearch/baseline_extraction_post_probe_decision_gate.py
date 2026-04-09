from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_extraction_probe import (
    BASELINE_EXTRACTION_PROBE_REPORT_PATH,
    build_baseline_extraction_probe,
)
from .config import CACHE_DIR, DATA_DIR

BASELINE_EXTRACTION_POST_PROBE_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_extraction_post_probe_decision_gate.md"
)
BASELINE_EXTRACTION_POST_PROBE_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_extraction_post_probe_decision_gate.json"
)


@dataclass(frozen=True)
class ExtractionDecisionStatus:
    criterion_id: str
    verdict: str
    note: str


@dataclass(frozen=True)
class BaselineExtractionPostProbeDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[ExtractionDecisionStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    non_claims: tuple[str, ...]


def build_baseline_extraction_post_probe_decision_gate() -> BaselineExtractionPostProbeDecisionGate:
    probe = build_baseline_extraction_probe()

    return BaselineExtractionPostProbeDecisionGate(
        gate_id="bz_phase2_baseline_extraction_post_probe_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=(
            ExtractionDecisionStatus(
                criterion_id="baseline_native_object",
                verdict="satisfied",
                note="The probe establishes a baseline-native extraction summary rather than another bridge-fit analog object.",
            ),
            ExtractionDecisionStatus(
                criterion_id="reproducible_hashes",
                verdict="satisfied",
                note="Retained output, unresolved residual, and full extraction summary are all reproducible via exact hashes.",
            ),
            ExtractionDecisionStatus(
                criterion_id="proof_relevance_gain",
                verdict="satisfied",
                note="The current summary is more proof-relevant than the bridge comparison layer because it is defined directly on baseline-side data.",
            ),
            ExtractionDecisionStatus(
                criterion_id="residual_elimination",
                verdict="not_yet_satisfied",
                note="The residual `zeta(3)` channel remains explicit and unresolved, so extraction has not yet reached a baseline remainder or P_n object.",
            ),
        ),
        outcome="continue_baseline_extraction",
        rationale=(
            "The first bounded extraction probe crossed the threshold for continuing: it produced a baseline-native, "
            "reproducible summary object on `n=1..80` without relying on bridge-fit identities. That is enough progress "
            "to justify one deeper extraction step."
        ),
        next_step=(
            "Implement the next bounded extraction rule as a strictly baseline-side refinement of the retained pair, "
            "with the goal of reducing or reclassifying the residual `zeta(3)` structure without claiming elimination prematurely."
        ),
        non_claims=(
            "This does not claim a baseline `P_n` extraction.",
            "This does not claim a proved baseline remainder pipeline.",
            "This does not justify reopening broad bridge-map experimentation as the main line.",
        ),
    )


def render_baseline_extraction_post_probe_decision_gate() -> str:
    gate = build_baseline_extraction_post_probe_decision_gate()
    lines = [
        "# Phase 2 baseline extraction post-probe decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{BASELINE_EXTRACTION_PROBE_REPORT_PATH}`",
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


def write_baseline_extraction_post_probe_decision_gate_report(
    output_path: str | Path = BASELINE_EXTRACTION_POST_PROBE_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_extraction_post_probe_decision_gate(), encoding="utf-8")
    return output


def write_baseline_extraction_post_probe_decision_gate_json(
    output_path: str | Path = BASELINE_EXTRACTION_POST_PROBE_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_baseline_extraction_post_probe_decision_gate()
    payload = asdict(gate)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_extraction_post_probe_decision_gate_report()
    write_baseline_extraction_post_probe_decision_gate_json()


if __name__ == "__main__":
    main()
