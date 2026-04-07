from __future__ import annotations

import json
from pathlib import Path

from zeta5_autoresearch.baseline_decay_audit import (
    build_phase2_baseline_decay_audit,
    build_phase2_dual_companion_checkpoint,
    build_phase2_pivot_decision,
    load_phase2_local_object_catalog,
    render_phase2_pivot_report,
    write_phase2_baseline_decay_audit_json,
)


def test_phase2_catalog_has_required_rows_and_real_paths() -> None:
    catalog = load_phase2_local_object_catalog()
    ids = {entry.object_id for entry in catalog}

    assert "baseline_bz_pn" in ids
    assert "baseline_bz_remainder" in ids
    assert "totally_symmetric_remainder_pipeline" in ids

    baseline_pn = next(entry for entry in catalog if entry.object_id == "baseline_bz_pn")
    baseline_remainder = next(entry for entry in catalog if entry.object_id == "baseline_bz_remainder")
    assert baseline_pn.source_status == "missing_local"
    assert baseline_pn.exact_status == "missing"
    assert baseline_remainder.source_status == "missing_local"
    assert baseline_remainder.exact_status == "missing"

    repo_root = Path("/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch")
    for entry in catalog:
        if entry.local_source_path:
            assert (repo_root / entry.local_source_path).exists()


def test_phase2_checkpoint_matches_frozen_frontier() -> None:
    checkpoint = build_phase2_dual_companion_checkpoint()

    assert checkpoint.constant_cache_max_n == 434
    assert checkpoint.zeta3_cache_max_n == 434
    assert checkpoint.certified_window_max_n == 431
    assert checkpoint.certified_degree == 106
    assert checkpoint.certified_rank == 428


def test_phase2_audit_and_pivot_decision_reflect_repo_local_gap(tmp_path: Path) -> None:
    audit = build_phase2_baseline_decay_audit()
    decision = build_phase2_pivot_decision()
    json_path = write_phase2_baseline_decay_audit_json(tmp_path / "audit.json")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert audit.symmetric_decay_probe.object_id == "bz_totally_symmetric_remainder_pipeline"
    assert audit.symmetric_decay_probe.bridge_target_family == "baseline"
    assert audit.baseline_decay_placeholder.object_id == "baseline_bz_remainder_pipeline"
    assert decision.outcome == "build_baseline_decay_readiness_bridge"
    assert "baseline decay-readiness bridge" in decision.rationale
    assert payload["baseline_decay_placeholder"]["exact_status"] == "missing"


def test_phase2_pivot_report_mentions_deferred_kernel_fight() -> None:
    report = render_phase2_pivot_report()

    assert "build_baseline_decay_readiness_bridge" in report
    assert "Deferred: the `n=435` dual-companion kernel fight" in report


def test_phase2_audit_report_mentions_bridge_target() -> None:
    report = build_phase2_baseline_decay_audit().symmetric_decay_probe

    assert report.bridge_target_family == "baseline"
