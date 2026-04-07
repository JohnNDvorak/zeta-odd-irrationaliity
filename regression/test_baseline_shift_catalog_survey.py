from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.baseline_shift_catalog_survey import (
    ShiftCatalogGeneratorSpec,
    enumerate_normalized_shift_supports,
    load_baseline_shift_catalog_survey,
    render_baseline_shift_catalog_survey_report,
    run_baseline_shift_catalog_survey,
    write_baseline_shift_catalog_survey_report,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SURVEY_PATH = REPO_ROOT / "specs" / "campaigns" / "bz_baseline_shift_catalog_survey.yaml"


def test_enumerate_normalized_shift_supports_filters_imprimitive_supports() -> None:
    spec = ShiftCatalogGeneratorSpec(
        id="mini",
        label="Mini",
        order=2,
        min_shift=-2,
        max_shift=2,
        include_zero=True,
        require_positive=True,
        require_negative=True,
        primitive_only=True,
    )

    supports = enumerate_normalized_shift_supports(spec)

    assert supports == ((1, 0, -2), (1, 0, -1), (2, 0, -1))


def test_baseline_shift_catalog_survey_spec_loads() -> None:
    survey = load_baseline_shift_catalog_survey(SURVEY_PATH)

    assert survey.id == "bz_baseline_shift_catalog_survey_v1"
    assert survey.max_n == 100
    assert len(survey.catalogs) == 2


def test_baseline_shift_catalog_survey_report_renders_for_small_window(tmp_path: Path) -> None:
    survey_path = tmp_path / "mini_shift_catalog.yaml"
    survey_path.write_text(
        "\n".join(
            (
                "survey:",
                '  id: "mini_shift_catalog"',
                '  label: "Mini shift catalog"',
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

    spec, results = run_baseline_shift_catalog_survey(survey_path)
    report = render_baseline_shift_catalog_survey_report(survey_path)
    output = write_baseline_shift_catalog_survey_report(survey_path, output_path=tmp_path / "report.md")

    assert spec.id == "mini_shift_catalog"
    assert len(results) == 1
    assert results[0].family_count >= 1
    assert "# Brown-Zudilin baseline shift-catalog survey" in report
    assert output.exists()
    assert "Mini shift catalog" in output.read_text(encoding="utf-8")
