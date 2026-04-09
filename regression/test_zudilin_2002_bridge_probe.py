from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.zudilin_2002_bridge_probe import (
    build_zudilin_2002_bridge_probe,
    render_zudilin_2002_bridge_probe,
    write_zudilin_2002_bridge_probe_report,
)


def test_zudilin_2002_bridge_probe_reproduces_initial_window() -> None:
    probe = build_zudilin_2002_bridge_probe(max_n=3)

    assert probe.probe_id == "bz_phase2_zudilin_2002_bridge_probe"
    assert probe.samples[0].q_n == -1
    assert probe.samples[1].q_n == 42
    assert probe.samples[2].q_n == -17934
    assert probe.samples[3].q_n == 14290980


def test_zudilin_2002_bridge_probe_report_renders_and_writes(tmp_path: Path) -> None:
    report = render_zudilin_2002_bridge_probe(max_n=3)

    assert "Phase 2 Zudilin 2002 bridge probe" in report
    assert "third-order recurrence" in report
    assert "|ζ(5)-p_n/q_n|" in report

    output = write_zudilin_2002_bridge_probe_report(max_n=3, output_path=tmp_path / "zudilin.md")
    assert output.exists()
    assert "7408444032" in output.read_text(encoding="utf-8")
