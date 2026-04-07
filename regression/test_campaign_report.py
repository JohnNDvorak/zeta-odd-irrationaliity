from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.campaign_report import render_campaign_report, write_campaign_report


REPO_ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_PATH = REPO_ROOT / "specs" / "campaigns" / "bz_fixed_sequence_campaign.yaml"


def test_campaign_report_renders_shared_sequence_hash() -> None:
    report = render_campaign_report(CAMPAIGN_PATH)
    assert "# Brown-Zudilin fixed-sequence representation campaign" in report
    assert "Shared sequence hash count: `1`" in report
    assert "very_well_poised_7f6" in report


def test_campaign_report_writes_markdown_file(tmp_path: Path) -> None:
    output = write_campaign_report(CAMPAIGN_PATH, output_path=tmp_path / "report.md")
    contents = output.read_text(encoding="utf-8")
    assert output.exists()
    assert "| Variant | Mode | Representation | Certificate | Equality Witness | Human Review | Routing Hash | Certificate Hash |" in contents
