from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.zudilin_2002_path_selection_memo import (
    build_zudilin_2002_path_selection_memo,
    render_zudilin_2002_path_selection_memo,
    write_zudilin_2002_path_selection_memo_json,
    write_zudilin_2002_path_selection_memo_report,
)


def test_zudilin_2002_path_selection_memo_prefers_baseline_extraction_path() -> None:
    memo = build_zudilin_2002_path_selection_memo(max_n=7)

    assert memo.memo_id == "bz_phase2_zudilin_2002_path_selection_memo"
    assert memo.shared_window_end == 7
    assert len(memo.options) == 3
    assert memo.chosen_path == "baseline_extraction_path"
    assert any(option.recommendation_level == "primary" for option in memo.options)


def test_zudilin_2002_path_selection_memo_report_and_json_render(tmp_path: Path) -> None:
    report = render_zudilin_2002_path_selection_memo(max_n=7)

    assert "Phase 2 Zudilin 2002 path-selection memo" in report
    assert "Chosen path" in report
    assert "baseline_extraction_path" in report

    report_path = write_zudilin_2002_path_selection_memo_report(
        max_n=7, output_path=tmp_path / "memo.md"
    )
    json_path = write_zudilin_2002_path_selection_memo_json(max_n=7, output_path=tmp_path / "memo.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 7
    assert payload["options"][0]["option_id"] == "n_dependent_coupled_map"
