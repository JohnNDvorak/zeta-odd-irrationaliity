from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_sym2_eight_window_decision_gate import (
    build_sym2_eight_window_decision_gate,
    render_sym2_eight_window_decision_gate,
    write_sym2_eight_window_decision_gate_json,
    write_sym2_eight_window_decision_gate_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_sym2_eight_window_matrix_recurrence_screen import (
    build_sym2_eight_window_matrix_recurrence_screen,
    render_sym2_eight_window_matrix_recurrence_screen,
    write_sym2_eight_window_matrix_recurrence_screen_json,
    write_sym2_eight_window_matrix_recurrence_screen_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_sym2_eight_window_object_spec import (
    build_sym2_eight_window_object_spec,
    render_sym2_eight_window_object_spec,
    write_sym2_eight_window_object_spec_json,
    write_sym2_eight_window_object_spec_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_sym2_eight_window_probe import (
    build_sym2_eight_window_probe,
    render_sym2_eight_window_probe,
    write_sym2_eight_window_probe_json,
    write_sym2_eight_window_probe_report,
)


def test_sym2_eight_window_object_spec_pairs_dual_packets() -> None:
    spec = build_sym2_eight_window_object_spec()

    assert spec.spec_id == "bz_phase2_sym2_eight_window_object_spec"
    assert spec.source_packet.packet_id == "bz_phase2_symmetric_dual_full_packet"
    assert spec.target_packet.packet_id == "bz_phase2_baseline_full_packet"


def test_sym2_eight_window_object_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_sym2_eight_window_object_spec()

    assert "Phase 2 Sym^2-lifted eight-window object spec" in report
    assert "Sym^2" in report

    report_path = write_sym2_eight_window_object_spec_report(tmp_path / "spec.md")
    json_path = write_sym2_eight_window_object_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["target_packet"]["packet_id"] == "bz_phase2_baseline_full_packet"


def test_sym2_eight_window_probe_establishes_object() -> None:
    probe = build_sym2_eight_window_probe()

    assert probe.probe_id == "bz_phase2_sym2_eight_window_probe"
    assert probe.coordinate_count == 27
    assert probe.shared_window_end == 73
    assert probe.verdict == "sym2_eight_window_object_established"
    assert len(probe.paired_object_hash) == 64


def test_sym2_eight_window_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_sym2_eight_window_probe()

    assert "Phase 2 Sym^2-lifted eight-window probe" in report
    assert "Coordinate count" in report

    report_path = write_sym2_eight_window_probe_report(tmp_path / "probe.md")
    json_path = write_sym2_eight_window_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 73


def test_sym2_eight_window_matrix_recurrence_screen_records_orders_one_and_two() -> None:
    screen = build_sym2_eight_window_matrix_recurrence_screen()

    assert screen.screen_id == "bz_phase2_sym2_eight_window_matrix_recurrence_screen"
    assert len(screen.order_results) == 4
    assert tuple(item.recurrence_order for item in screen.order_results) == (1, 1, 2, 2)
    assert all(item.matrix_size == 27 for item in screen.order_results)
    assert all(item.equation_count > item.unknown_count for item in screen.order_results)
    assert all(item.verdict == "inconsistent_mod_prime" for item in screen.order_results)
    assert screen.overall_verdict == "low_order_matrix_recurrence_exhausted_through_order_2"


def test_sym2_eight_window_matrix_recurrence_screen_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_sym2_eight_window_matrix_recurrence_screen()

    assert "Phase 2 Sym^2-lifted eight-window matrix recurrence screen" in report
    assert "underdetermined" in report

    report_path = write_sym2_eight_window_matrix_recurrence_screen_report(tmp_path / "screen.md")
    json_path = write_sym2_eight_window_matrix_recurrence_screen_json(tmp_path / "screen.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert len(payload["order_results"]) == 4


def test_sym2_eight_window_decision_gate_tracks_boundary() -> None:
    gate = build_sym2_eight_window_decision_gate()

    assert gate.gate_id == "bz_phase2_sym2_eight_window_decision_gate"
    assert gate.outcome == "hard_wall_sym2_eight_window_low_order_matrix_ladder_exhausted"
    assert gate.pivot_options == (
        "different_nonlocal_family_on_sym2_eight_window_lift",
        "different_higher_schur_or_nonlinear_invariant_family",
    )


def test_sym2_eight_window_decision_gate_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_sym2_eight_window_decision_gate()

    assert "Phase 2 Sym^2-lifted eight-window decision gate" in report
    assert "different_nonlocal_family_on_sym2_eight_window_lift" in report

    report_path = write_sym2_eight_window_decision_gate_report(tmp_path / "gate.md")
    json_path = write_sym2_eight_window_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["gate_id"] == "bz_phase2_sym2_eight_window_decision_gate"
