from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.baseline_family_survey import (
    load_baseline_family_survey,
    render_baseline_family_survey_report,
    run_baseline_family_survey,
    write_baseline_family_survey_report,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SURVEY_PATH = REPO_ROOT / "specs" / "campaigns" / "bz_baseline_modular_family_survey.yaml"


def test_baseline_family_survey_spec_loads() -> None:
    survey = load_baseline_family_survey(SURVEY_PATH)

    assert survey.id == "bz_baseline_modular_family_survey_v1"
    assert survey.max_n == 100
    assert len(survey.families) >= 4


def test_baseline_family_survey_report_renders_for_small_window(tmp_path: Path) -> None:
    survey_path = tmp_path / "mini_survey.yaml"
    survey_path.write_text(
        "\n".join(
            (
                "survey:",
                '  id: "mini"',
                '  label: "Mini baseline survey"',
                "  max_n: 12",
                "  families:",
                '    - id: "order3_consecutive"',
                '      label: "Order 3 consecutive"',
                "      shifts: [1, 0, -1, -2]",
                "      degree_min: 0",
                "      degree_max: 2",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    spec, results = run_baseline_family_survey(survey_path)
    report = render_baseline_family_survey_report(survey_path)
    output = write_baseline_family_survey_report(survey_path, output_path=tmp_path / "report.md")

    assert spec.id == "mini"
    assert len(results) == 1
    assert results[0].certified_degree_cap == 1
    assert results[0].first_uncertified_degree == 2
    assert "# Brown-Zudilin baseline recurrence family survey" in report
    assert output.exists()
    assert "Order 3 consecutive" in output.read_text(encoding="utf-8")
