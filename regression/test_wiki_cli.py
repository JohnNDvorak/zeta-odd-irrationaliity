from __future__ import annotations

from pathlib import Path

from zeta5_autoresearch.wiki_cli import (
    PageSpec,
    bootstrap,
    build_index,
    ensure_wiki_skeleton,
    lint_wiki,
    snapshot_source,
    wiki_root,
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _minimal_repo(tmp_path: Path, monkeypatch) -> Path:
    repo = tmp_path / "repo"
    _write(repo / "data" / "logs" / "sample_report.md", "# Sample Report\n\nBody.\n")
    _write(repo / "refs" / "notes_sample.md", "# Sample Notes\n\nBody.\n")
    _write(repo / "src" / "zeta5_autoresearch" / "sample_code.py", "VALUE = 1\n")
    monkeypatch.setattr(
        "zeta5_autoresearch.wiki_cli.KEY_CODE_SNAPSHOTS",
        ("src/zeta5_autoresearch/sample_code.py",),
    )
    monkeypatch.setattr(
        "zeta5_autoresearch.wiki_cli.build_core_pages",
        lambda repo_root: (
            PageSpec(
                relative_path="frontier.md",
                title="Frontier",
                category="frontier",
                phase="2",
                direction="frontier",
                sources=("raw/logs/sample_report.md",),
                summary="Current frontier summary.",
                body="See [[non-symmetric-baseline-pn]] and [Exhausted](conclusions/exhausted-ansatz-classes.md).",
            ),
            PageSpec(
                relative_path="entities/non-symmetric-baseline-pn.md",
                title="Baseline Pn",
                category="entity",
                phase="2",
                direction="8",
                sources=("raw/logs/sample_report.md",),
                summary="Baseline Pn status.",
                body="This object is not source-backed.",
            ),
            PageSpec(
                relative_path="conclusions/exhausted-ansatz-classes.md",
                title="Exhausted",
                category="conclusion",
                phase="2",
                direction="frontier",
                sources=("raw/logs/sample_report.md",),
                summary="Exhausted list.",
                body="Linked from [[frontier]].",
            ),
        ),
    )
    return repo


def test_bootstrap_creates_wiki_and_index(tmp_path: Path, monkeypatch) -> None:
    repo = _minimal_repo(tmp_path, monkeypatch)
    bootstrap(repo)

    root = wiki_root(repo)
    assert (root / "schema.md").exists()
    assert (root / "index.md").exists()
    assert (root / "log.md").exists()
    assert (root / "frontier.md").exists()
    assert (root / "raw" / "logs" / "sample_report.md").exists()
    assert (root / "raw" / "refs" / "notes_sample.md").exists()
    assert (root / "raw" / "code" / "sample_code.py").exists()
    assert (root / "sources" / "sample-report.md").exists()

    index_text = (root / "index.md").read_text(encoding="utf-8")
    assert "Current frontier summary." in index_text
    log_text = (root / "log.md").read_text(encoding="utf-8")
    assert "ingest | Bootstrap raw logs, refs, code, and core synthesis pages" in log_text


def test_snapshot_source_versions_changed_input(tmp_path: Path) -> None:
    source = tmp_path / "input.md"
    destination_root = tmp_path / "wiki" / "raw" / "logs"
    _write(source, "v1\n")
    first = snapshot_source(source, destination_root)
    _write(source, "v2\n")
    second = snapshot_source(source, destination_root)

    assert first.exists()
    assert second.exists()
    assert first != second
    assert len(list(destination_root.glob("input*.md"))) == 2


def test_lint_accepts_bootstrap_shape(tmp_path: Path, monkeypatch) -> None:
    repo = _minimal_repo(tmp_path, monkeypatch)
    bootstrap(repo)
    build_index(repo)

    assert lint_wiki(repo) == []


def test_lint_flags_missing_not_source_backed_marker(tmp_path: Path, monkeypatch) -> None:
    repo = _minimal_repo(tmp_path, monkeypatch)
    ensure_wiki_skeleton(repo)
    frontier = PageSpec(
        relative_path="frontier.md",
        title="Frontier",
        category="frontier",
        phase="2",
        direction="frontier",
        sources=("raw/logs/sample_report.md",),
        summary="Current frontier summary.",
        body="See [[non-symmetric-baseline-pn]].",
    )
    from zeta5_autoresearch.wiki_cli import write_page

    write_page(repo, frontier)
    write_page(
        repo,
        PageSpec(
            relative_path="entities/non-symmetric-baseline-pn.md",
            title="Baseline Pn",
            category="entity",
            phase="2",
            direction="8",
            sources=("raw/logs/sample_report.md",),
            summary="Baseline Pn status.",
            body="This object is unresolved.",
        ),
    )
    write_page(
        repo,
        PageSpec(
            relative_path="conclusions/exhausted-ansatz-classes.md",
            title="Exhausted",
            category="conclusion",
            phase="2",
            direction="frontier",
            sources=("raw/logs/sample_report.md",),
            summary="Exhausted list.",
            body="Linked from [[frontier]].",
        ),
    )
    build_index(repo)

    issues = lint_wiki(repo)
    assert any("not source-backed" in item for item in issues)
