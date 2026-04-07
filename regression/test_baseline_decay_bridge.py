from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_decay_bridge import (
    build_phase2_baseline_decay_bridge,
    render_phase2_baseline_decay_bridge_report,
    write_phase2_baseline_decay_bridge_json,
    write_phase2_baseline_decay_bridge_report,
)


def test_baseline_decay_bridge_reuses_symmetric_anchor() -> None:
    bridge = build_phase2_baseline_decay_bridge()

    assert bridge.anchor_summary.object_id == "bz_totally_symmetric_remainder_pipeline"
    assert bridge.anchor_summary.bridge_target_family == "baseline"
    assert bridge.target_family == "baseline"
    assert bridge.target_object_id == "baseline_bz_remainder_pipeline"


def test_baseline_decay_bridge_report_and_json_render(tmp_path: Path) -> None:
    report = render_phase2_baseline_decay_bridge_report()
    assert "baseline decay-readiness bridge" in report
    assert "Bridge target family" in report

    report_path = write_phase2_baseline_decay_bridge_report(tmp_path / "bridge.md")
    json_path = write_phase2_baseline_decay_bridge_json(tmp_path / "bridge.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert report_path.exists()
    assert payload["anchor_summary"]["bridge_target_family"] == "baseline"
