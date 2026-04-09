from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_six_window_plucker_matrix_recurrence_screen import (
    build_six_window_normalized_plucker_matrix_recurrence_screen,
    render_six_window_normalized_plucker_matrix_recurrence_screen,
    write_six_window_normalized_plucker_matrix_recurrence_screen_json,
    write_six_window_normalized_plucker_matrix_recurrence_screen_report,
)


def test_six_window_normalized_plucker_matrix_recurrence_screen_records_both_sides() -> None:
    screen = build_six_window_normalized_plucker_matrix_recurrence_screen()

    assert screen.screen_id == "bz_phase2_six_window_normalized_plucker_matrix_recurrence_screen"
    assert tuple((item.packet_side, item.recurrence_order) for item in screen.order_results) == (
        ("source", 1),
        ("target", 1),
        ("source", 2),
        ("target", 2),
        ("source", 3),
        ("target", 3),
    )
    assert tuple(item.matrix_size for item in screen.order_results) == (19, 19, 19, 19, 19, 19)
    assert screen.overall_verdict == "low_order_matrix_recurrence_exhausted_through_order_3"
    assert tuple(item.verdict for item in screen.order_results) == (
        "inconsistent_mod_prime",
        "inconsistent_mod_prime",
        "inconsistent_mod_prime",
        "inconsistent_mod_prime",
        "inconsistent_mod_prime",
        "inconsistent_mod_prime",
    )
    assert tuple(item.witness_prime for item in screen.order_results) == (
        1013,
        1447,
        1013,
        1447,
        1013,
        1447,
    )


def test_six_window_normalized_plucker_matrix_recurrence_screen_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_six_window_normalized_plucker_matrix_recurrence_screen()

    assert "Phase 2 six-window normalized Plucker matrix recurrence screen" in report
    assert "recurrence order" in report

    report_path = write_six_window_normalized_plucker_matrix_recurrence_screen_report(tmp_path / "screen.md")
    json_path = write_six_window_normalized_plucker_matrix_recurrence_screen_json(tmp_path / "screen.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert len(payload["order_results"]) == 6
