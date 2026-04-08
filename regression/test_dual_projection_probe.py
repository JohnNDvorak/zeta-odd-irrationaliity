from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.dual_projection_probe import (
    build_phase2_dual_projection_probe,
    render_phase2_dual_projection_probe,
    write_phase2_dual_projection_probe_report,
)


def test_dual_projection_probe_uses_shared_exact_window() -> None:
    probe = build_phase2_dual_projection_probe()

    assert probe.target_id == "baseline_dual_f7_exact_coefficient_packet"
    assert probe.calibration_anchor_id == "zudilin_2002_third_order_zeta5_bridge"
    assert probe.shared_window_start == 1
    assert probe.shared_window_end == 80
    assert len(probe.packet_hash) == 64
    assert [component.component_id for component in probe.components] == ["constant", "zeta3", "zeta5"]
    assert probe.components[0].max_verified_index == 434
    assert probe.components[2].max_verified_index == 80


def test_dual_projection_probe_report_renders_and_writes(tmp_path: Path) -> None:
    report = render_phase2_dual_projection_probe()

    assert "Phase 2 dual projection probe" in report
    assert "Shared exact window: `n=1..80`" in report
    assert "Projection-ready packet hash" in report
    assert "Calibration departures" in report
    assert "pre-projection coefficient packet" in report

    output = write_phase2_dual_projection_probe_report(tmp_path / "probe.md")
    assert output.exists()
    assert "zudilin_2002_third_order_zeta5_bridge" in output.read_text(encoding="utf-8")
