from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_decay_audit import (
    AUDIT_JSON_PATH,
    AUDIT_REPORT_PATH,
    build_phase2_baseline_decay_audit,
)
from .config import CACHE_DIR, DATA_DIR
from .decay_probe import DecayProbeSummary

BRIDGE_REPORT_PATH = DATA_DIR / "logs" / "bz_phase2_baseline_decay_bridge_report.md"
BRIDGE_JSON_PATH = CACHE_DIR / "bz_phase2_baseline_decay_bridge.json"


@dataclass(frozen=True)
class BaselineDecayBridge:
    bridge_id: str
    anchor_summary: DecayProbeSummary
    target_family: str
    target_object_id: str
    missing_prerequisites: tuple[str, ...]
    bridge_steps: tuple[str, ...]
    recommendation: str


def build_phase2_baseline_decay_bridge() -> BaselineDecayBridge:
    audit = build_phase2_baseline_decay_audit()
    return BaselineDecayBridge(
        bridge_id="bz_phase2_baseline_decay_readiness_bridge",
        anchor_summary=audit.symmetric_decay_probe,
        target_family="baseline",
        target_object_id=audit.baseline_decay_placeholder.object_id,
        missing_prerequisites=audit.baseline_decay_placeholder.missing_prerequisites,
        bridge_steps=(
            "Keep the totally symmetric remainder pipeline as the only source-backed decay anchor.",
            "Reuse the generic decay-probe summary shape and metrics for any future baseline remainder object.",
            "Wait for a repo-local baseline `P_n` formula, recurrence, or remainder fixture before claiming a baseline decay pipeline.",
        ),
        recommendation=(
            "Treat the totally symmetric remainder pipeline as the calibration anchor and leave the baseline family on the readiness bridge until a source-backed baseline decay object is available locally."
        ),
    )


def render_phase2_baseline_decay_bridge_report() -> str:
    bridge = build_phase2_baseline_decay_bridge()
    lines = [
        "# Phase 2 baseline decay-readiness bridge",
        "",
        f"- Bridge id: `{bridge.bridge_id}`",
        f"- Anchor object id: `{bridge.anchor_summary.object_id}`",
        f"- Bridge target family: `{bridge.anchor_summary.bridge_target_family}`",
        f"- Target family: `{bridge.target_family}`",
        f"- Target object id: `{bridge.target_object_id}`",
        f"- Audit report: `{AUDIT_REPORT_PATH}`",
        f"- Audit json: `{AUDIT_JSON_PATH}`",
        "",
        "## Missing prerequisites",
        "",
    ]
    for item in bridge.missing_prerequisites:
        lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Bridge steps",
            "",
        ]
    )
    for step in bridge.bridge_steps:
        lines.append(f"- {step}")
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            f"- {bridge.recommendation}",
            "",
        ]
    )
    return "\n".join(lines)


def write_phase2_baseline_decay_bridge_report(output_path: str | Path = BRIDGE_REPORT_PATH) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_phase2_baseline_decay_bridge_report(), encoding="utf-8")
    return output


def write_phase2_baseline_decay_bridge_json(output_path: str | Path = BRIDGE_JSON_PATH) -> Path:
    bridge = build_phase2_baseline_decay_bridge()
    payload = {
        "bridge_id": bridge.bridge_id,
        "anchor_summary": asdict(bridge.anchor_summary),
        "target_family": bridge.target_family,
        "target_object_id": bridge.target_object_id,
        "missing_prerequisites": list(bridge.missing_prerequisites),
        "bridge_steps": list(bridge.bridge_steps),
        "recommendation": bridge.recommendation,
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output
