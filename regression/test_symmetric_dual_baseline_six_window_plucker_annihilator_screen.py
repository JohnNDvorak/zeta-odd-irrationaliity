from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_six_window_plucker_annihilator_screen import (
    build_six_window_normalized_plucker_annihilator_screen,
    render_six_window_normalized_plucker_annihilator_screen,
    write_six_window_normalized_plucker_annihilator_screen_json,
    write_six_window_normalized_plucker_annihilator_screen_report,
)


def test_six_window_normalized_plucker_annihilator_screen_exhausts_short_orders() -> None:
    screen = build_six_window_normalized_plucker_annihilator_screen()

    assert screen.screen_id == "bz_phase2_six_window_normalized_plucker_annihilator_screen"
    assert screen.overall_verdict == "short_order_local_annihilator_family_exhausted_up_to_order_6"
    assert tuple((item.packet_side, item.relation_length) for item in screen.order_results) == (
        ("source", 4),
        ("target", 4),
        ("source", 5),
        ("target", 5),
        ("source", 6),
        ("target", 6),
    )
    assert tuple(item.first_inconsistent_index for item in screen.order_results) == (1, 1, 1, 1, 1, 1)
    assert tuple(item.first_nonunique_index for item in screen.order_results) == (None, None, None, None, None, None)


def test_six_window_normalized_plucker_annihilator_screen_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_six_window_normalized_plucker_annihilator_screen()

    assert "Phase 2 six-window normalized Plucker annihilator screen" in report
    assert "short_order_local_annihilator_family_exhausted_up_to_order_6" in report

    report_path = write_six_window_normalized_plucker_annihilator_screen_report(tmp_path / "screen.md")
    json_path = write_six_window_normalized_plucker_annihilator_screen_json(tmp_path / "screen.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["order_results"][0]["first_inconsistent_index"] == 1
