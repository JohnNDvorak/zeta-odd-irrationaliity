from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.construction_memo import (
    build_phase2_construction_memo,
    render_phase2_construction_memo,
    write_phase2_construction_memo_json,
    write_phase2_construction_memo_report,
)


def test_construction_memo_captures_baseline_gap_and_paths() -> None:
    memo = build_phase2_construction_memo()

    assert memo.baseline_seed == "a=(8,16,10,15,12,16,18,13)"
    assert any("totally symmetric Brown-Zudilin specialization" in asset for asset in memo.banked_assets)
    assert any("No checked explicit baseline non-symmetric P_n sequence" in item for item in memo.missing_objects)
    assert [path.path_id for path in memo.construction_paths] == [
        "baseline_dual_projection_path",
        "hypergeometric_bridge_path",
        "cellular_contiguity_path",
    ]
    assert "dual cellular projection path" in memo.next_step.lower()


def test_construction_memo_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_construction_memo()

    assert "Phase 2 construction memo" in report
    assert "Brown-Zudilin baseline non-symmetric seed" in report
    assert "Dual cellular projection path" in report
    assert "External hypergeometric bridge comparison path" in report
    assert "Generalized cellular contiguity / denominator-side reconstruction path" in report

    report_path = write_phase2_construction_memo_report(tmp_path / "memo.md")
    json_path = write_phase2_construction_memo_json(tmp_path / "memo.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["memo_id"] == "bz_phase2_construction_memo"
    assert payload["construction_paths"][0]["path_id"] == "baseline_dual_projection_path"
