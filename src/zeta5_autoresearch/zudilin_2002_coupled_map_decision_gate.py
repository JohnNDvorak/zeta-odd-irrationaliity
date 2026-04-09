from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .zudilin_2002_coupled_linear_map_probe import build_zudilin_2002_coupled_linear_map_probe
from .zudilin_2002_normalization_decision_gate import build_zudilin_2002_normalization_decision_gate

ZUDILIN_2002_COUPLED_MAP_DECISION_GATE_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_zudilin_2002_coupled_map_decision_gate.md"
)
ZUDILIN_2002_COUPLED_MAP_DECISION_GATE_JSON_PATH = (
    CACHE_DIR / "bz_phase2_zudilin_2002_coupled_map_decision_gate.json"
)


@dataclass(frozen=True)
class CoupledMapDecisionStatus:
    layer_id: str
    verdict: str
    implication: str


@dataclass(frozen=True)
class Zudilin2002CoupledMapDecisionGate:
    gate_id: str
    shared_window_start: int
    shared_window_end: int
    statuses: tuple[CoupledMapDecisionStatus, ...]
    overall_verdict: str
    recommendation: str
    non_claims: tuple[str, ...]


def build_zudilin_2002_coupled_map_decision_gate(*, max_n: int = 7) -> Zudilin2002CoupledMapDecisionGate:
    normalization_gate = build_zudilin_2002_normalization_decision_gate(max_n=max_n)
    coupled_probe = build_zudilin_2002_coupled_linear_map_probe(max_n=max_n)

    return Zudilin2002CoupledMapDecisionGate(
        gate_id="bz_phase2_zudilin_2002_coupled_map_decision_gate",
        shared_window_start=1,
        shared_window_end=min(normalization_gate.shared_window_end, coupled_probe.shared_window_end),
        statuses=(
            CoupledMapDecisionStatus(
                layer_id="one_channel_polynomial_maps",
                verdict="closed",
                implication=(
                    "Scalar, affine-in-n, and quadratic-in-n one-channel normalization families all fail exactly on the shared window."
                ),
            ),
            CoupledMapDecisionStatus(
                layer_id="constant_coupled_linear_map",
                verdict="closed",
                implication=(
                    "A constant rational 2x2 transformation fitted from n=1,2 does not carry the bridge pair to the baseline pair on the full shared window."
                ),
            ),
        ),
        overall_verdict=(
            "The bounded constant-form ansatz layer is now closed. Both the one-channel polynomial-rescaling line and the simplest coupled constant-matrix line fail on the shared window."
        ),
        recommendation=(
            "Do not keep enlarging the ansatz mechanically. The next bounded move should either test one structured n-dependent two-channel map family or pivot to a different paired object / projection target."
        ),
        non_claims=(
            "This does not rule out all coupled transformations.",
            "This does not prove the baseline pair and bridge pair are unrelated in every stronger sense.",
            "This only closes the bounded constant-form ansatz layer tested so far.",
        ),
    )


def render_zudilin_2002_coupled_map_decision_gate(*, max_n: int = 7) -> str:
    gate = build_zudilin_2002_coupled_map_decision_gate(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 coupled-map decision gate",
        "",
        f"- Gate id: `{gate.gate_id}`",
        f"- Shared exact window: `n={gate.shared_window_start}..{gate.shared_window_end}`",
        "",
        "| layer | verdict | implication |",
        "| --- | --- | --- |",
    ]
    for item in gate.statuses:
        lines.append(f"| `{item.layer_id}` | `{item.verdict}` | {item.implication} |")
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


def write_zudilin_2002_coupled_map_decision_gate_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COUPLED_MAP_DECISION_GATE_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_coupled_map_decision_gate(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_coupled_map_decision_gate_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COUPLED_MAP_DECISION_GATE_JSON_PATH,
) -> Path:
    gate = build_zudilin_2002_coupled_map_decision_gate(max_n=max_n)
    payload = asdict(gate)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_zudilin_2002_coupled_map_decision_gate_report()
    write_zudilin_2002_coupled_map_decision_gate_json()


if __name__ == "__main__":
    main()
