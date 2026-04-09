from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_six_window_plucker_global_recurrence_screen import (
    build_six_window_normalized_plucker_global_recurrence_screen,
    render_six_window_normalized_plucker_global_recurrence_screen,
    write_six_window_normalized_plucker_global_recurrence_screen_json,
    write_six_window_normalized_plucker_global_recurrence_screen_report,
)


def test_six_window_normalized_plucker_global_recurrence_screen_exhausts_orders_through_10() -> None:
    screen = build_six_window_normalized_plucker_global_recurrence_screen()

    assert screen.screen_id == "bz_phase2_six_window_normalized_plucker_global_recurrence_screen"
    assert screen.overall_verdict == "low_order_global_vector_recurrence_exhausted_through_order_10"
    assert len(screen.order_results) == 18
    assert all(item.verdict == "inconsistent" for item in screen.order_results)
    assert tuple(item.recurrence_order for item in screen.order_results[:4]) == (2, 2, 3, 3)


def test_six_window_normalized_plucker_global_recurrence_screen_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_six_window_normalized_plucker_global_recurrence_screen()

    assert "Phase 2 six-window normalized Plucker global recurrence screen" in report
    assert "low_order_global_vector_recurrence_exhausted_through_order_10" in report

    report_path = write_six_window_normalized_plucker_global_recurrence_screen_report(tmp_path / "screen.md")
    json_path = write_six_window_normalized_plucker_global_recurrence_screen_json(tmp_path / "screen.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["order_results"][0]["verdict"] == "inconsistent"
