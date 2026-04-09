from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.zudilin_2002_companion_channel_ansatz import (
    build_zudilin_2002_companion_channel_ansatz,
    render_zudilin_2002_companion_channel_ansatz,
    write_zudilin_2002_companion_channel_ansatz_json,
    write_zudilin_2002_companion_channel_ansatz_report,
)


def test_zudilin_2002_companion_channel_ansatz_redirects_off_normalization_maps() -> None:
    ansatz = build_zudilin_2002_companion_channel_ansatz(max_n=7)

    assert ansatz.ansatz_id == "bz_phase2_zudilin_2002_companion_channel_ansatz"
    assert ansatz.shared_window_end == 7
    assert len(ansatz.fields) == 3
    assert "coupled two-channel object" in ansatz.ansatz_statement
    assert "baseline residual `ζ(3)` channel" in ansatz.forbidden_outcome


def test_zudilin_2002_companion_channel_ansatz_report_and_json_render(tmp_path: Path) -> None:
    report = render_zudilin_2002_companion_channel_ansatz(max_n=7)

    assert "Phase 2 Zudilin 2002 companion-channel-aware bridge ansatz" in report
    assert "Coupled fields" in report
    assert "Recommendation" in report

    report_path = write_zudilin_2002_companion_channel_ansatz_report(
        max_n=7, output_path=tmp_path / "ansatz.md"
    )
    json_path = write_zudilin_2002_companion_channel_ansatz_json(max_n=7, output_path=tmp_path / "ansatz.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 7
    assert payload["fields"][2]["field_id"] == "coupled_object"
