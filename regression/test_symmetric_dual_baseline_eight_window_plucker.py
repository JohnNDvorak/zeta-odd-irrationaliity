from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_eight_window_plucker_decision_gate import (
    build_eight_window_normalized_plucker_decision_gate,
    render_eight_window_normalized_plucker_decision_gate,
    write_eight_window_normalized_plucker_decision_gate_json,
    write_eight_window_normalized_plucker_decision_gate_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_eight_window_plucker_matrix_recurrence_screen import (
    build_eight_window_normalized_plucker_matrix_recurrence_screen,
    render_eight_window_normalized_plucker_matrix_recurrence_screen,
    write_eight_window_normalized_plucker_matrix_recurrence_screen_json,
    write_eight_window_normalized_plucker_matrix_recurrence_screen_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_eight_window_plucker_object_spec import (
    build_eight_window_normalized_plucker_object_spec,
    render_eight_window_normalized_plucker_object_spec,
    write_eight_window_normalized_plucker_object_spec_json,
    write_eight_window_normalized_plucker_object_spec_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_eight_window_plucker_probe import (
    build_eight_window_normalized_plucker_probe,
    render_eight_window_normalized_plucker_probe,
    write_eight_window_normalized_plucker_probe_json,
    write_eight_window_normalized_plucker_probe_report,
)


def test_eight_window_normalized_plucker_object_spec_pairs_dual_packets() -> None:
    spec = build_eight_window_normalized_plucker_object_spec()

    assert spec.spec_id == "bz_phase2_eight_window_normalized_plucker_object_spec"
    assert spec.source_packet.packet_id == "bz_phase2_symmetric_dual_full_packet"
    assert spec.target_packet.packet_id == "bz_phase2_baseline_full_packet"


def test_eight_window_normalized_plucker_object_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_eight_window_normalized_plucker_object_spec()

    assert "Phase 2 eight-window normalized Plucker object spec" in report
    assert "Gr(3,8)" in report

    report_path = write_eight_window_normalized_plucker_object_spec_report(tmp_path / "spec.md")
    json_path = write_eight_window_normalized_plucker_object_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["target_packet"]["packet_id"] == "bz_phase2_baseline_full_packet"


def test_eight_window_normalized_plucker_probe_establishes_object() -> None:
    probe = build_eight_window_normalized_plucker_probe()

    assert probe.probe_id == "bz_phase2_eight_window_normalized_plucker_probe"
    assert probe.coordinate_count == 55
    assert probe.shared_window_end == 73
    assert probe.verdict == "eight_window_normalized_plucker_object_established"
    assert len(probe.paired_object_hash) == 64


def test_eight_window_normalized_plucker_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_eight_window_normalized_plucker_probe()

    assert "Phase 2 eight-window normalized Plucker probe" in report
    assert "Coordinate count" in report

    report_path = write_eight_window_normalized_plucker_probe_report(tmp_path / "probe.md")
    json_path = write_eight_window_normalized_plucker_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 73


def test_eight_window_normalized_plucker_matrix_recurrence_screen_records_last_overdetermined_order() -> None:
    screen = build_eight_window_normalized_plucker_matrix_recurrence_screen()

    assert screen.screen_id == "bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen"
    assert tuple((item.packet_side, item.recurrence_order) for item in screen.order_results) == (
        ("source", 1),
        ("target", 1),
    )
    assert all(item.matrix_size == 55 for item in screen.order_results)
    assert all(item.equation_count > item.unknown_count for item in screen.order_results)
    assert tuple(item.verdict for item in screen.order_results) == (
        "inconsistent_mod_prime",
        "inconsistent_mod_prime",
    )
    assert tuple(item.witness_prime for item in screen.order_results) == (1013, 1447)
    assert screen.overall_verdict == "order1_matrix_recurrence_exhausted"


def test_eight_window_normalized_plucker_matrix_recurrence_screen_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_eight_window_normalized_plucker_matrix_recurrence_screen()

    assert "Phase 2 eight-window normalized Plucker matrix recurrence screen" in report
    assert "underdetermined" in report

    report_path = write_eight_window_normalized_plucker_matrix_recurrence_screen_report(tmp_path / "screen.md")
    json_path = write_eight_window_normalized_plucker_matrix_recurrence_screen_json(tmp_path / "screen.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert len(payload["order_results"]) == 2


def test_eight_window_normalized_plucker_decision_gate_tracks_boundary() -> None:
    gate = build_eight_window_normalized_plucker_decision_gate()

    assert gate.gate_id == "bz_phase2_eight_window_normalized_plucker_decision_gate"
    assert gate.outcome == "hard_wall_eight_window_plucker_order1_matrix_exhausted"
    assert gate.pivot_options == (
        "different_nonlocal_family_on_eight_window_plucker",
        "different_wider_nonlinear_invariant_family",
    )


def test_eight_window_normalized_plucker_decision_gate_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_eight_window_normalized_plucker_decision_gate()

    assert "Phase 2 eight-window normalized Plucker decision gate" in report
    assert "different_nonlocal_family_on_eight_window_plucker" in report

    report_path = write_eight_window_normalized_plucker_decision_gate_report(tmp_path / "gate.md")
    json_path = write_eight_window_normalized_plucker_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["gate_id"] == "bz_phase2_eight_window_normalized_plucker_decision_gate"
