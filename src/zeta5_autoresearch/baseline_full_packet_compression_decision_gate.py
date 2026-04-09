from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline_full_packet_compression_probe import (
    BASELINE_FULL_PACKET_COMPRESSION_PROBE_REPORT_PATH,
    build_baseline_full_packet_compression_probe,
)
from .config import CACHE_DIR, DATA_DIR

BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_baseline_full_packet_compression_decision_gate.md"
)
BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_baseline_full_packet_compression_decision_gate.json"
)


@dataclass(frozen=True)
class BaselineFullPacketCompressionStatus:
    route_id: str
    route_verdict: str
    note: str


@dataclass(frozen=True)
class BaselineFullPacketCompressionDecisionGate:
    gate_id: str
    source_probe_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[BaselineFullPacketCompressionStatus, ...]
    outcome: str
    rationale: str
    next_step: str
    pivot_options: tuple[str, ...]
    bridge_boundary: str


def build_baseline_full_packet_compression_decision_gate() -> BaselineFullPacketCompressionDecisionGate:
    probe = build_baseline_full_packet_compression_probe()
    statuses = tuple(
        BaselineFullPacketCompressionStatus(
            route_id=item.route_id,
            route_verdict=item.route_verdict,
            note="Closed by a hard-wall gate or an exact full-window failure of the fixed low-complexity ladder.",
        )
        for item in probe.route_results
    )
    return BaselineFullPacketCompressionDecisionGate(
        gate_id="bz_phase2_baseline_full_packet_compression_decision_gate",
        source_probe_id=probe.probe_id,
        shared_window_start=probe.shared_window_start,
        shared_window_end=probe.shared_window_end,
        statuses=statuses,
        outcome="hard_wall_full_packet_pairwise_compression_exhausted",
        rationale=(
            "All three pairwise low-complexity compression routes from the full packet are now closed: two by prior hard-wall gates "
            "and one by the newly computed zeta(5)-residual route."
        ),
        next_step=(
            "Stop autonomous execution and ask the user for the next pivot. Do not enlarge the compression family or choose a new packet source without that decision."
        ),
        pivot_options=(
            "richer_full_packet_projection_family",
            "different_baseline_family_source",
        ),
        bridge_boundary=probe.bridge_boundary,
    )


def render_baseline_full_packet_compression_decision_gate() -> str:
    gate = build_baseline_full_packet_compression_decision_gate()
    lines = [
        "# Phase 2 baseline full-packet compression decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Source probe: `{BASELINE_FULL_PACKET_COMPRESSION_PROBE_REPORT_PATH}`",
        f"- Source probe id: `{gate.source_probe_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        f"- Outcome: `{gate.outcome}`",
        "",
        "| route | verdict | note |",
        "| --- | --- | --- |",
    ]
    for item in gate.statuses:
        lines.append(f"| `{item.route_id}` | `{item.route_verdict}` | {item.note} |")
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
            "## Bridge boundary",
            "",
            gate.bridge_boundary,
            "",
            "## Pivot options",
            "",
        ]
    )
    for item in gate.pivot_options:
        lines.append(f"- `{item}`")
    lines.append("")
    return "\n".join(lines)


def write_baseline_full_packet_compression_decision_gate_report(
    output_path: str | Path = BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_baseline_full_packet_compression_decision_gate(), encoding="utf-8")
    return output


def write_baseline_full_packet_compression_decision_gate_json(
    output_path: str | Path = BASELINE_FULL_PACKET_COMPRESSION_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_baseline_full_packet_compression_decision_gate()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(gate), indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_baseline_full_packet_compression_decision_gate_report()
    write_baseline_full_packet_compression_decision_gate_json()


if __name__ == "__main__":
    main()
