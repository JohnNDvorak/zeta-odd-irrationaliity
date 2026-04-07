from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.campaigns import expand_campaign, load_campaign_spec, run_campaign_structural_dry_run


REPO_ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_PATH = REPO_ROOT / "specs" / "campaigns" / "bz_fixed_sequence_campaign.yaml"


def test_campaign_spec_loads() -> None:
    campaign = load_campaign_spec(CAMPAIGN_PATH)
    assert campaign.id == "bz_fixed_sequence_campaign_v1"
    assert campaign.base_candidate.name == "baseline_bz_seed.yaml"
    assert len(campaign.variants) >= 5


def test_campaign_expansion_produces_structurally_valid_variants() -> None:
    campaign, expanded = expand_campaign(CAMPAIGN_PATH)
    assert campaign.id == "bz_fixed_sequence_campaign_v1"
    assert len(expanded) == len(campaign.variants)
    assert all(item.gate1_accepted for item in expanded)
    assert len({item.candidate.routing_hash for item in expanded}) == len(expanded)
    assert all(item.candidate.configuration.label == "8pi8v" for item in expanded)
    assert all(item.candidate.affine_family.u == expanded[0].candidate.affine_family.u for item in expanded)
    assert len({item.candidate.sequence_hash for item in expanded}) == 1
    assert all(item.candidate.sequence_hash is not None for item in expanded)
    assert len({item.candidate.certificate_hash for item in expanded}) == len(expanded)


def test_campaign_dry_run_summary_reports_modes() -> None:
    payload = run_campaign_structural_dry_run(CAMPAIGN_PATH, log_results=False)
    assert payload["campaign_id"] == "bz_fixed_sequence_campaign_v1"
    assert {item["mode"] for item in payload["variants"]} == {"Mode A-fast", "Mode A-slow"}
    assert all(item["gate1_accepted"] for item in payload["variants"])
    assert len({item["sequence_hash"] for item in payload["variants"]}) == 1
