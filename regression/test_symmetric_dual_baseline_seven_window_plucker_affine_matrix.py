from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_seven_window_plucker_affine_matrix_decision_gate import (
    build_seven_window_normalized_plucker_affine_matrix_decision_gate,
    render_seven_window_normalized_plucker_affine_matrix_decision_gate,
    write_seven_window_normalized_plucker_affine_matrix_decision_gate_json,
    write_seven_window_normalized_plucker_affine_matrix_decision_gate_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_seven_window_plucker_affine_matrix_recurrence_screen import (
    build_seven_window_normalized_plucker_affine_matrix_recurrence_screen,
    render_seven_window_normalized_plucker_affine_matrix_recurrence_screen,
    write_seven_window_normalized_plucker_affine_matrix_recurrence_screen_json,
    write_seven_window_normalized_plucker_affine_matrix_recurrence_screen_report,
)


def test_seven_window_affine_matrix_recurrence_screen_records_overdetermined_orders() -> None:
    screen = build_seven_window_normalized_plucker_affine_matrix_recurrence_screen()

    assert screen.screen_id == "bz_phase2_seven_window_normalized_plucker_affine_matrix_recurrence_screen"
    assert tuple((item.packet_side, item.recurrence_order) for item in screen.order_results) == (
        ("source", 1),
        ("target", 1),
        ("source", 2),
        ("target", 2),
    )
    assert all(item.matrix_size == 34 for item in screen.order_results)
    assert all(item.equation_count > item.unknown_count for item in screen.order_results)
    assert screen.overall_verdict in (
        "low_order_affine_matrix_recurrence_exhausted_through_order_2",
        "seven_window_affine_matrix_recurrence_requires_exact_followup",
    )


def test_seven_window_affine_matrix_recurrence_screen_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_seven_window_normalized_plucker_affine_matrix_recurrence_screen()

    assert "Phase 2 seven-window normalized Plucker affine matrix recurrence screen" in report
    assert "affine chart" in report

    report_path = write_seven_window_normalized_plucker_affine_matrix_recurrence_screen_report(tmp_path / "screen.md")
    json_path = write_seven_window_normalized_plucker_affine_matrix_recurrence_screen_json(tmp_path / "screen.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert len(payload["order_results"]) == 4


def test_seven_window_affine_matrix_decision_gate_tracks_boundary() -> None:
    gate = build_seven_window_normalized_plucker_affine_matrix_decision_gate()

    assert gate.gate_id == "bz_phase2_seven_window_normalized_plucker_affine_matrix_decision_gate"
    assert gate.outcome in (
        "continue_seven_window_plucker_exact_affine_followup",
        "hard_wall_seven_window_plucker_low_order_affine_matrix_ladder_exhausted",
    )
    assert gate.pivot_options == (
        "different_nonlocal_family_on_seven_window_plucker",
        "different_wider_window_nonlinear_object",
    )


def test_seven_window_affine_matrix_decision_gate_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_seven_window_normalized_plucker_affine_matrix_decision_gate()

    assert "Phase 2 seven-window normalized Plucker affine matrix decision gate" in report
    assert "different_nonlocal_family_on_seven_window_plucker" in report

    report_path = write_seven_window_normalized_plucker_affine_matrix_decision_gate_report(tmp_path / "gate.md")
    json_path = write_seven_window_normalized_plucker_affine_matrix_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["gate_id"] == "bz_phase2_seven_window_normalized_plucker_affine_matrix_decision_gate"
