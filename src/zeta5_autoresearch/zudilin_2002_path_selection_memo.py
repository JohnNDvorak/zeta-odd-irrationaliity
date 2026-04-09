from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import CACHE_DIR, DATA_DIR
from .construction_memo import CONSTRUCTION_MEMO_REPORT_PATH
from .zudilin_2002_coupled_map_decision_gate import (
    ZUDILIN_2002_COUPLED_MAP_DECISION_GATE_REPORT_PATH,
    build_zudilin_2002_coupled_map_decision_gate,
)

ZUDILIN_2002_PATH_SELECTION_MEMO_REPORT_PATH = (
    DATA_DIR / "logs" / "bz_phase2_zudilin_2002_path_selection_memo.md"
)
ZUDILIN_2002_PATH_SELECTION_MEMO_JSON_PATH = (
    CACHE_DIR / "bz_phase2_zudilin_2002_path_selection_memo.json"
)


@dataclass(frozen=True)
class PathOption:
    option_id: str
    title: str
    objective: str
    upside: str
    downside: str
    recommendation_level: str


@dataclass(frozen=True)
class Zudilin2002PathSelectionMemo:
    memo_id: str
    shared_window_start: int
    shared_window_end: int
    premise: str
    options: tuple[PathOption, ...]
    chosen_path: str
    rationale: str
    stop_rules: tuple[str, ...]


def build_zudilin_2002_path_selection_memo(*, max_n: int = 7) -> Zudilin2002PathSelectionMemo:
    gate = build_zudilin_2002_coupled_map_decision_gate(max_n=max_n)
    return Zudilin2002PathSelectionMemo(
        memo_id="bz_phase2_zudilin_2002_path_selection_memo",
        shared_window_start=gate.shared_window_start,
        shared_window_end=gate.shared_window_end,
        premise=(
            "The bounded constant-form ansatz layer is closed on the shared window. The next move should maximize "
            "research signal rather than continue ansatz inflation by momentum."
        ),
        options=(
            PathOption(
                option_id="n_dependent_coupled_map",
                title="Structured n-dependent 2x2 map",
                objective=(
                    "Test one bounded two-channel family with explicit n-dependence, such as an affine-in-n 2x2 matrix, "
                    "against the ordered pair `(ζ(5), ζ(3))`."
                ),
                upside=(
                    "Natural next escalation from the constant coupled map and still close to the current bridge-comparison machinery."
                ),
                downside=(
                    "High risk of turning into another mechanical ansatz climb without improving proof relevance."
                ),
                recommendation_level="secondary",
            ),
            PathOption(
                option_id="different_paired_object",
                title="Different paired object / projection target",
                objective=(
                    "Change the compared paired object itself instead of changing only the map family, for example by altering "
                    "the baseline-side retained/residual packaging or the bridge-side target object."
                ),
                upside=(
                    "Could reveal that the current pair is simply the wrong abstraction, avoiding uninformative map-fitting."
                ),
                downside=(
                    "Requires a fresh design choice and may partially reset comparison continuity."
                ),
                recommendation_level="secondary",
            ),
            PathOption(
                option_id="baseline_extraction_path",
                title="Return to baseline extraction / projection construction",
                objective=(
                    "Use the bridge work as calibration only, and shift back toward building a baseline-family extraction step "
                    "that is more proof-relevant than further bridge-map fitting."
                ),
                upside=(
                    "Best alignment with the long-term goal: explicit baseline decay-side structure rather than more indirect analogies."
                ),
                downside=(
                    "Harder engineering and math, with a less immediate bounded experiment than the map-fitting line."
                ),
                recommendation_level="primary",
            ),
        ),
        chosen_path="baseline_extraction_path",
        rationale=(
            "The bridge program has now done what it needed to do: it produced a disciplined comparison object and closed several "
            "low-complexity map families. That is enough calibration. The next best use of cycles is to redirect toward baseline-side "
            "extraction or projection construction, not to keep expanding the bridge ansatz catalog."
        ),
        stop_rules=(
            "Do not add cubic or higher one-channel normalization maps unless a new structural reason appears.",
            "Do not add arbitrary n-dependent 2x2 map families without first stating a bounded motivating principle.",
            "If a new bridge-side experiment is proposed, it must explain why it advances baseline extraction rather than only enlarging the ansatz catalog.",
        ),
    )


def render_zudilin_2002_path_selection_memo(*, max_n: int = 7) -> str:
    memo = build_zudilin_2002_path_selection_memo(max_n=max_n)
    lines = [
        "# Phase 2 Zudilin 2002 path-selection memo",
        "",
        f"- Memo id: `{memo.memo_id}`",
        f"- Shared exact window: `n={memo.shared_window_start}..{memo.shared_window_end}`",
        f"- Coupled-map decision gate: `{ZUDILIN_2002_COUPLED_MAP_DECISION_GATE_REPORT_PATH}`",
        f"- Construction memo: `{CONSTRUCTION_MEMO_REPORT_PATH}`",
        "",
        "## Premise",
        "",
        memo.premise,
        "",
        "## Options",
        "",
        "| option | recommendation | objective | upside | downside |",
        "| --- | --- | --- | --- | --- |",
    ]
    for option in memo.options:
        lines.append(
            f"| `{option.option_id}` | `{option.recommendation_level}` | {option.objective} | {option.upside} | {option.downside} |"
        )
    lines.extend(
        [
            "",
            "## Chosen path",
            "",
            f"- `{memo.chosen_path}`",
            "",
            "## Rationale",
            "",
            memo.rationale,
            "",
            "## Stop rules",
            "",
        ]
    )
    for item in memo.stop_rules:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def write_zudilin_2002_path_selection_memo_report(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_PATH_SELECTION_MEMO_REPORT_PATH,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_zudilin_2002_path_selection_memo(max_n=max_n), encoding="utf-8")
    return output


def write_zudilin_2002_path_selection_memo_json(
    *,
    max_n: int = 7,
    output_path: str | Path = ZUDILIN_2002_PATH_SELECTION_MEMO_JSON_PATH,
) -> Path:
    memo = build_zudilin_2002_path_selection_memo(max_n=max_n)
    payload = asdict(memo)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output


def main() -> None:
    write_zudilin_2002_path_selection_memo_report()
    write_zudilin_2002_path_selection_memo_json()


if __name__ == "__main__":
    main()
