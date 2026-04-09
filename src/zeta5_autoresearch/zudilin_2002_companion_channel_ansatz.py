from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .external_bridge_comparison_implementation_note import (
    EXTERNAL_BRIDGE_COMPARISON_IMPLEMENTATION_NOTE_REPORT_PATH,
    build_phase2_external_bridge_comparison_implementation_note,
)
from .zudilin_2002_normalization_decision_gate import (
    ZUDILIN_2002_NORMALIZATION_DECISION_GATE_REPORT_PATH,
    build_zudilin_2002_normalization_decision_gate,
)

ZUDILIN_2002_COMPANION_CHANNEL_ANSATZ_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_zudilin_2002_companion_channel_ansatz.md"
)
ZUDILIN_2002_COMPANION_CHANNEL_ANSATZ_JSON_PATH = (
    CACHE_DIR / "bz_phase2_zudilin_2002_companion_channel_ansatz.json"
)


@dataclass(frozen=True)
class CompanionAwareField:
    field_id: str
    baseline_object: str
    bridge_object: str
    role: str


@dataclass(frozen=True)
class Zudilin2002CompanionChannelAnsatz:
    ansatz_id: str
    bridge_id: str
    shared_window_start: int
    shared_window_end: int
    ansatz_label: str
    ansatz_statement: str
    why_this_follows: tuple[str, ...]
    fields: tuple[CompanionAwareField, ...]
    allowed_outcome: str
    forbidden_outcome: str
    recommendation: str


def build_zudilin_2002_companion_channel_ansatz(*, max_n: int = 7) -> Zudilin2002CompanionChannelAnsatz:
    implementation_note = build_phase2_external_bridge_comparison_implementation_note()
    normalization_gate = build_zudilin_2002_normalization_decision_gate(max_n=max_n)

    return Zudilin2002CompanionChannelAnsatz(
        ansatz_id="bz_phase2_zudilin_2002_companion_channel_ansatz",
        bridge_id="zudilin_2002_third_order_zeta5_bridge",
        shared_window_start=1,
        shared_window_end=normalization_gate.shared_window_end,
        ansatz_label="Companion-channel-aware two-channel bridge ansatz",
        ansatz_statement=(
            "Treat the baseline retained `ζ(5)` channel and the baseline residual `ζ(3)` channel as a coupled two-channel "
            "object, and compare that pair directly against the published Zudilin 2002 pair `(q_n ζ(5)-p_n, q_n ζ(3)-p̃_n)` "
            "instead of trying to normalize the `ζ(5)` channel alone by a low-degree scalar map."
        ),
        why_this_follows=(
            "The implementation note already requires the companion `ζ(3)` channel to remain explicit rather than hidden.",
            "The normalization decision gate closes the scalar/affine/quadratic one-channel rescaling line on the shared window.",
            "The external bridge object is itself naturally two-channel, so a coupled ansatz matches the published bridge shape better than another one-channel map.",
        ),
        fields=(
            CompanionAwareField(
                field_id="target_channel",
                baseline_object="baseline retained `ζ(5)` channel",
                bridge_object="published `q_n ζ(5) - p_n` channel",
                role="Primary odd-zeta target channel carried explicitly inside the coupled comparison.",
            ),
            CompanionAwareField(
                field_id="companion_channel",
                baseline_object="baseline residual `ζ(3)` channel",
                bridge_object="published `q_n ζ(3) - p̃_n` channel",
                role="Companion channel that must remain visible and may participate in the transformation instead of being normalized away.",
            ),
            CompanionAwareField(
                field_id="coupled_object",
                baseline_object="finite-window exact ordered pair `(ζ(5), ζ(3))`",
                bridge_object="published ordered bridge pair `(ℓ_n, ℓ̃_n)`",
                role="The real comparison object for the next phase: a two-channel ordered pair, not a single normalized scalar sequence.",
            ),
        ),
        allowed_outcome=(
            "A future probe may report that the baseline pair and bridge pair are compatible with some coupled finite-window "
            "transformation ansatz without claiming recurrence-level equivalence."
        ),
        forbidden_outcome=(
            "Do not claim that the baseline residual `ζ(3)` channel has been eliminated or that the baseline pair has already "
            "been converted into the published Zudilin recurrence object."
        ),
        recommendation=(
            "The next concrete artifact should be a coupled two-channel comparison target or probe, built on the ordered pair "
            "`(baseline ζ(5), baseline ζ(3))` versus `(bridge ζ(5), bridge ζ(3))`, with the finite-window asymmetry kept explicit."
        ),
    )


def render_zudilin_2002_companion_channel_ansatz(*, max_n: int = 7) -> str:
    ansatz = build_zudilin_2002_companion_channel_ansatz(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 companion-channel-aware bridge ansatz",
        "",
        f"- Ansatz id: `{ansatz.ansatz_id}`",
        f"- Bridge id: `{ansatz.bridge_id}`",
        f"- Shared exact window: `n={ansatz.shared_window_start}..{ansatz.shared_window_end}`",
        f"- Comparison implementation note: `{EXTERNAL_BRIDGE_COMPARISON_IMPLEMENTATION_NOTE_REPORT_PATH}`",
        f"- Normalization decision gate: `{ZUDILIN_2002_NORMALIZATION_DECISION_GATE_REPORT_PATH}`",
        "",
        f"- Ansatz label: {ansatz.ansatz_label}",
        "",
        "## Statement",
        "",
        ansatz.ansatz_statement,
        "",
        "## Why this follows",
        "",
    ]
    for item in ansatz.why_this_follows:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Coupled fields",
            "",
            "| field | baseline object | bridge object | role |",
            "| --- | --- | --- | --- |",
        ]
    )
    for field in ansatz.fields:
        lines.append(
            f"| `{field.field_id}` | {field.baseline_object} | {field.bridge_object} | {field.role} |"
        )
    lines.extend(
        [
            "",
            "## Allowed outcome",
            "",
            ansatz.allowed_outcome,
            "",
            "## Forbidden outcome",
            "",
            ansatz.forbidden_outcome,
            "",
            "## Recommendation",
            "",
            ansatz.recommendation,
            "",
        ]
    )
    return "\n".join(lines)


def write_zudilin_2002_companion_channel_ansatz_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COMPANION_CHANNEL_ANSATZ_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_companion_channel_ansatz(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_companion_channel_ansatz_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_COMPANION_CHANNEL_ANSATZ_JSON_PATH,
) -> Path:
    ansatz = build_zudilin_2002_companion_channel_ansatz(max_n=max_n)
    payload = asdict(ansatz)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_zudilin_2002_companion_channel_ansatz_report()
    write_zudilin_2002_companion_channel_ansatz_json()


if __name__ == "__main__":
    main()
