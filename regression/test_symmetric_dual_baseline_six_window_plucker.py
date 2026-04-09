from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.symmetric_dual_baseline_six_window_plucker_decision_gate import (
    build_six_window_normalized_plucker_decision_gate,
    render_six_window_normalized_plucker_decision_gate,
    write_six_window_normalized_plucker_decision_gate_json,
    write_six_window_normalized_plucker_decision_gate_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_six_window_plucker_family_probe import (
    build_six_window_normalized_plucker_family_probe,
    render_six_window_normalized_plucker_family_probe,
    write_six_window_normalized_plucker_family_probe_json,
    write_six_window_normalized_plucker_family_probe_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_six_window_plucker_object_spec import (
    build_six_window_normalized_plucker_object_spec,
    render_six_window_normalized_plucker_object_spec,
    write_six_window_normalized_plucker_object_spec_json,
    write_six_window_normalized_plucker_object_spec_report,
)
from zeta5_autoresearch.symmetric_dual_baseline_six_window_plucker_probe import (
    build_six_window_normalized_plucker_probe,
    render_six_window_normalized_plucker_probe,
    write_six_window_normalized_plucker_probe_json,
    write_six_window_normalized_plucker_probe_report,
)


def test_six_window_normalized_plucker_object_spec_pairs_dual_packets() -> None:
    spec = build_six_window_normalized_plucker_object_spec()

    assert spec.spec_id == "bz_phase2_six_window_normalized_plucker_object_spec"
    assert spec.source_packet.packet_id == "bz_phase2_symmetric_dual_full_packet"
    assert spec.target_packet.packet_id == "bz_phase2_baseline_full_packet"
    assert spec.source_packet.shared_window_end == 80
    assert spec.target_packet.shared_window_end == 80


def test_six_window_normalized_plucker_object_spec_report_and_json_render(tmp_path: Path) -> None:
    report = render_six_window_normalized_plucker_object_spec()

    assert "Phase 2 six-window normalized Plucker object spec" in report
    assert "Gr(3,6)" in report

    report_path = write_six_window_normalized_plucker_object_spec_report(tmp_path / "spec.md")
    json_path = write_six_window_normalized_plucker_object_spec_json(tmp_path / "spec.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["source_packet"]["packet_id"] == "bz_phase2_symmetric_dual_full_packet"


def test_six_window_normalized_plucker_probe_establishes_object() -> None:
    probe = build_six_window_normalized_plucker_probe()

    assert probe.probe_id == "bz_phase2_six_window_normalized_plucker_probe"
    assert probe.coordinate_count == 19
    assert probe.shared_window_end == 75
    assert probe.verdict == "six_window_normalized_plucker_object_established"
    assert len(probe.source_invariant_hash) == 64
    assert len(probe.target_invariant_hash) == 64
    assert len(probe.paired_object_hash) == 64


def test_six_window_normalized_plucker_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_six_window_normalized_plucker_probe()

    assert "Phase 2 six-window normalized Plucker probe" in report
    assert "Paired object hash" in report

    report_path = write_six_window_normalized_plucker_probe_report(tmp_path / "probe.md")
    json_path = write_six_window_normalized_plucker_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["shared_window_end"] == 75


def test_six_window_normalized_plucker_family_probe_records_three_families() -> None:
    probe = build_six_window_normalized_plucker_family_probe()

    assert probe.probe_id == "bz_phase2_six_window_normalized_plucker_family_probe"
    assert probe.coordinate_count == 19
    assert tuple(item.family_id for item in probe.family_results) == (
        "constant_six_plucker_map",
        "difference_six_plucker_map",
        "support1_free_zero_six_plucker_map",
    )
    assert tuple(item.verdict for item in probe.family_results) == (
        "fails_after_fit_window",
        "fails_after_fit_window",
        "inconsistent_fit_block",
    )
    assert tuple(item.first_mismatch_index for item in probe.family_results) == (
        20,
        21,
        None,
    )
    assert tuple(item.rank for item in probe.family_results) == (361, 361, 31)
    assert tuple(item.nullity for item in probe.family_results) == (0, 0, 7)
    assert probe.overall_verdict == "six_window_plucker_family_exhausted_on_current_ladder"


def test_six_window_normalized_plucker_family_probe_report_and_json_render(tmp_path: Path) -> None:
    report = render_six_window_normalized_plucker_family_probe()

    assert "Phase 2 six-window normalized Plucker family probe" in report
    assert "support1_free_zero_six_plucker_map" in report

    report_path = write_six_window_normalized_plucker_family_probe_report(tmp_path / "probe.md")
    json_path = write_six_window_normalized_plucker_family_probe_json(tmp_path / "probe.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert len(payload["family_results"]) == 3


def test_six_window_normalized_plucker_decision_gate_records_next_pivot() -> None:
    gate = build_six_window_normalized_plucker_decision_gate()

    assert gate.gate_id == "bz_phase2_six_window_normalized_plucker_decision_gate"
    assert gate.outcome == "hard_wall_six_window_plucker_support1_inconsistent"
    assert gate.pivot_options == (
        "different_recurrence_family_on_six_window_plucker",
        "different_wider_window_nonlinear_object",
    )


def test_six_window_normalized_plucker_decision_gate_report_and_json_render(
    tmp_path: Path,
) -> None:
    report = render_six_window_normalized_plucker_decision_gate()

    assert "Phase 2 six-window normalized Plucker decision gate" in report
    assert "different_recurrence_family_on_six_window_plucker" in report

    report_path = write_six_window_normalized_plucker_decision_gate_report(tmp_path / "gate.md")
    json_path = write_six_window_normalized_plucker_decision_gate_json(tmp_path / "gate.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["gate_id"] == "bz_phase2_six_window_normalized_plucker_decision_gate"
