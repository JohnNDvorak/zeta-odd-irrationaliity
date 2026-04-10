from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_sym3_eleven_window_affine_decision_gate import (
    build_sym3_eleven_window_affine_decision_gate,
    render_sym3_eleven_window_affine_decision_gate,
    write_sym3_eleven_window_affine_decision_gate_json,
    write_sym3_eleven_window_affine_decision_gate_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_sym3_eleven_window_affine_matrix_recurrence_screen import (
    build_sym3_eleven_window_affine_matrix_recurrence_screen,
    render_sym3_eleven_window_affine_matrix_recurrence_screen,
    write_sym3_eleven_window_affine_matrix_recurrence_screen_json,
    write_sym3_eleven_window_affine_matrix_recurrence_screen_report,
)


def test_sym3_eleven_window_affine_matrix_recurrence_screen_records_orders_one_through_six() -> None:
    screen = build_sym3_eleven_window_affine_matrix_recurrence_screen()

    assert screen.screen_id == "bz_phase2_sym3_eleven_window_affine_matrix_recurrence_screen"
    assert len(screen.order_results) == 12
    assert screen.order_results[0].recurrence_order == 1
    assert screen.order_results[-1].recurrence_order == 6
    assert all(item.matrix_size == 10 for item in screen.order_results)
    assert all(item.equation_count > item.unknown_count for item in screen.order_results)
    assert all(item.verdict == "inconsistent_mod_prime" for item in screen.order_results)
    assert all(
        item.witness_prime == (1009 if item.packet_side == "source" else 1447)
        for item in screen.order_results
    )
    assert [(item.equation_count, item.unknown_count) for item in screen.order_results] == [
        (690, 110),
        (690, 110),
        (680, 210),
        (680, 210),
        (670, 310),
        (670, 310),
        (660, 410),
        (660, 410),
        (650, 510),
        (650, 510),
        (640, 610),
        (640, 610),
    ]
    assert screen.overall_verdict == "low_order_affine_matrix_recurrence_exhausted_through_order_6"


def test_sym3_eleven_window_affine_matrix_recurrence_screen_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_sym3_eleven_window_affine_matrix_recurrence_screen()

    assert "Phase 2 Sym^3-lifted eleven-window affine matrix recurrence screen" in report
    assert "underdetermined" in report

    report_path = write_sym3_eleven_window_affine_matrix_recurrence_screen_report(tmp_path / "screen.md")
    json_path = write_sym3_eleven_window_affine_matrix_recurrence_screen_json(tmp_path / "screen.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert len(payload["order_results"]) == 12


def test_sym3_eleven_window_affine_decision_gate_tracks_boundary() -> None:
    gate = build_sym3_eleven_window_affine_decision_gate()

    assert gate.gate_id == "bz_phase2_sym3_eleven_window_affine_decision_gate"
    assert gate.outcome == "hard_wall_sym3_eleven_window_low_order_affine_matrix_ladder_exhausted"
    assert gate.pivot_options == (
        "different_nonlocal_family_on_sym3_eleven_window_lift",
        "different_higher_schur_or_nonlinear_invariant_family",
    )


def test_sym3_eleven_window_affine_decision_gate_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_sym3_eleven_window_affine_decision_gate()

    assert "Phase 2 Sym^3-lifted eleven-window affine decision gate" in report
    assert "different_nonlocal_family_on_sym3_eleven_window_lift" in report

    report_path = write_sym3_eleven_window_affine_decision_gate_report(tmp_path / "gate.md")
    json_path = write_sym3_eleven_window_affine_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["gate_id"] == "bz_phase2_sym3_eleven_window_affine_decision_gate"
