from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.dual_f7_zeta5_shift_catalog_survey import (
    load_dual_f7_zeta5_shift_catalog_survey,
    render_dual_f7_zeta5_shift_catalog_survey_report,
    run_dual_f7_zeta5_shift_catalog_survey,
    write_dual_f7_zeta5_shift_catalog_survey_report,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SURVEY_PATH = REPO_ROOT / "specs" / "campaigns" / "bz_dual_f7_zeta5_shift_catalog_survey.yaml"


def test_dual_f7_zeta5_shift_catalog_survey_spec_loads() -> None:
    survey = load_dual_f7_zeta5_shift_catalog_survey(SURVEY_PATH)

    assert survey.id == "bz_dual_f7_zeta5_shift_catalog_survey_v1"
    assert survey.max_n == 80
    assert len(survey.catalogs) == 3


def test_dual_f7_zeta5_shift_catalog_survey_report_renders_for_small_window(tmp_path: Path) -> None:
    survey_path = tmp_path / "mini_dual_shift_catalog.yaml"
    survey_path.write_text(
        "\n".join(
            (
                "survey:",
                '  id: "mini_dual_shift_catalog"',
                '  label: "Mini dual shift catalog"',
                "  max_n: 18",
                "  catalogs:",
                '    - id: "order3_span2"',
                '      label: "Order 3 supports in [-2, 2]"',
                "      order: 3",
                "      min_shift: -2",
                "      max_shift: 2",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    spec, results = run_dual_f7_zeta5_shift_catalog_survey(survey_path)
    report = render_dual_f7_zeta5_shift_catalog_survey_report(survey_path)
    output = write_dual_f7_zeta5_shift_catalog_survey_report(survey_path, output_path=tmp_path / "report.md")

    assert spec.id == "mini_dual_shift_catalog"
    assert len(results) == 1
    assert results[0].family_count >= 1
    assert "# Brown-Zudilin dual F_7 zeta(5)-coefficient shift-catalog survey" in report
    assert output.exists()
    assert "Mini dual shift catalog" in output.read_text(encoding="utf-8")
