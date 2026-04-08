from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .dual_projection_experiment import DUAL_PROJECTION_PLAN_REPORT_PATH
from .dual_projection_probe import DUAL_PROJECTION_PROBE_REPORT_PATH, build_phase2_dual_projection_probe
from .dual_projection_rule_experiment import (
    DUAL_PROJECTION_RULE_REPORT_PATH,
    build_phase2_dual_projection_rule_experiment,
)
from .external_calibration_check import (
    EXTERNAL_CALIBRATION_REPORT_PATH,
    build_phase2_external_calibration_check,
)

DUAL_PROJECTION_DECISION_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_dual_projection_decision_gate.md"
DUAL_PROJECTION_DECISION_JSON_PATH = CACHE_DIR / "bz_phase2_dual_projection_decision_gate.json"


@dataclass(frozen=True)
class DualProjectionDecisionGate:
    gate_id: str
    outcome: str
    rationale: str
    evidence: tuple[str, ...]
    rejected_next_steps: tuple[str, ...]
    next_main_line: str


def build_phase2_dual_projection_decision_gate() -> DualProjectionDecisionGate:
    probe = build_phase2_dual_projection_probe()
    rule = build_phase2_dual_projection_rule_experiment()
    calibration = build_phase2_external_calibration_check()

    return DualProjectionDecisionGate(
        gate_id="bz_phase2_dual_projection_decision_gate",
        outcome="switch_to_external_bridge_calibration",
        rationale=(
            "The bounded projection program succeeded as a specification exercise: it produced a stable exact packet on "
            "n<=80 and one honest retained-pair/residual split. But the first rule experiment is still bookkeeping-only "
            "and does not provide an elimination mechanism for the zeta(3) residual channel. At this point, proposing "
            "stronger projection identities would be more speculative than informative, so the next main line should "
            "fall back to the explicit external bridge path rather than invent more baseline projection rules."
        ),
        evidence=(
            (
                "The shared exact baseline packet exists and is reproducible on n=1.."
                f"{probe.shared_window_end}, with packet hash `{probe.packet_hash}`."
            ),
            (
                "The first rule experiment produces separate retained-pair and residual-channel hashes but explicitly "
                "states that it is bookkeeping-only and does not eliminate the residual channel."
            ),
            (
                "The calibration contract from "
                f"`{EXTERNAL_CALIBRATION_REPORT_PATH}` has been met at the bookkeeping level, but not at the level of a "
                "published linear-form identity comparable to Zudilin 2002."
            ),
        ),
        rejected_next_steps=(
            "Do not stack more ad hoc projection rules onto the retained-pair/residual split without a new source-backed identity to test.",
            "Do not reopen the old n=435 dual-companion kernel engineering lane; that remains a separate deferred engineering task.",
            "Do not broaden literature search again before using the already-verified external bridge objects more concretely.",
        ),
        next_main_line=(
            "Switch to the external hypergeometric bridge path. The next artifact should specify one explicit bridge object "
            "from Zudilin 2002 or Zudilin 2018 as the first implementation-calibration target for a stronger coefficient-side comparison."
        ),
    )


def render_phase2_dual_projection_decision_gate() -> str:
    gate = build_phase2_dual_projection_decision_gate()
    lines = [
        "# Phase 2 dual projection decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Dual projection plan: `{DUAL_PROJECTION_PLAN_REPORT_PATH}`",
        f"- Projection probe: `{DUAL_PROJECTION_PROBE_REPORT_PATH}`",
        f"- Projection rule experiment: `{DUAL_PROJECTION_RULE_REPORT_PATH}`",
        f"- External calibration check: `{EXTERNAL_CALIBRATION_REPORT_PATH}`",
        f"- Outcome: `{gate.outcome}`",
        "",
        "## Rationale",
        "",
        gate.rationale,
        "",
        "## Evidence",
        "",
    ]
    for item in gate.evidence:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Rejected next steps",
            "",
        ]
    )
    for item in gate.rejected_next_steps:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Next main line",
            "",
            gate.next_main_line,
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_dual_projection_decision_gate_report(
    output_path: str | Path = DUAL_PROJECTION_DECISION_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_dual_projection_decision_gate(), encoding="utf-8")
    return output


def write_phase2_dual_projection_decision_gate_json(
    output_path: str | Path = DUAL_PROJECTION_DECISION_JSON_PATH,
) -> Path:
    gate = build_phase2_dual_projection_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_phase2_dual_projection_decision_gate_report()
    write_phase2_dual_projection_decision_gate_json()


if __name__ == "__main__":
    main()
