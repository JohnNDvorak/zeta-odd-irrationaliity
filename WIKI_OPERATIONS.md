# Wiki Operations

Operator procedure for the repo-native research wiki.

Use this file for process. Use `CODEX_TRANSITION.md` for research state.

## Purpose

The wiki is the cumulative memory layer for this project.

It exists to ensure:

- a fresh Codex can resume work without rereading long chat history;
- hard walls and exhausted ansatz classes are not retried accidentally;
- frontier claims remain source-backed;
- repo memory lives in git, not only in conversation.

## Directory Model

### `wiki/raw/`

Immutable source snapshots.

Use this for:

- copied reports from `data/logs/`
- literature notes
- code snapshots when needed for citation
- checkpoint memos
- decision-gate artifacts

Rules:

- never edit an existing raw snapshot;
- create a new snapshot instead;
- wiki synthesis pages should cite these files, not live working files.

### `wiki/`

LLM-maintained synthesized markdown.

Use this for:

- audit pages
- frontier pages
- entity pages
- concept pages
- source summaries
- conclusion pages
- computation pages

### `wiki/index.md`

Catalog of pages.

This should be rebuilt whenever the wiki changes materially.

### `wiki/log.md`

Append-only operational log.

The ingest tool updates this automatically.

## Required Reading Order

When resuming work:

1. `README.md`
2. `CODEX_TRANSITION.md`
3. `WIKI_OPERATIONS.md`
4. `wiki/index.md`
5. `wiki/frontier.md`
6. relevant audit/conclusion/object pages

Do not start by reading random raw logs.

## Canonical Current Pages

These are the most important live pages right now:

- `wiki/frontier.md`
- `wiki/audits/completed-directions.md`
- `wiki/conclusions/exhausted-ansatz-classes.md`
- `wiki/computation/exact-side-frozen-frontier.md`
- `wiki/computation/sym3-eleven-window-frontier.md`
- `wiki/audits/sym4-sixteen-window-compute-wall.md`
- `wiki/audits/sym4-sixteen-window-target-partial-cache-progress.md`
- `wiki/literature/brown-zudilin-2210-03391v3.md`
- `wiki/literature/zudilin-2002.md`

## Working Principle

For research work:

- `data/logs/` is the mutable working layer;
- `wiki/raw/` is the immutable citation layer;
- `wiki/` is the synthesized memory layer.

That means:

- you can read and write `data/logs/` while working;
- but when updating the wiki, you should ingest the log so the wiki points to a raw snapshot;
- do not let synthesis pages cite live mutable logs directly.

## Standard Workflows

### 1. Query workflow

When answering a substantive question:

1. Read `wiki/index.md`.
2. Read `wiki/frontier.md`.
3. Read the most relevant audit, conclusion, entity, and literature pages.
4. Check `wiki/conclusions/exhausted-ansatz-classes.md` before suggesting any new family.
5. If the answer adds genuine durable value, consider filing a new wiki page or updating an existing one.

### 2. Autonomous directed loop

Use this when the user says `continue` or asks the agent to keep searching autonomously.

1. Read [[autonomous-directed-iteration-loop]] and the current [[frontier]].
2. Snapshot git state and ignored drafts.
3. Select one bounded candidate that is not a disguised retry of an exhausted class.
4. Run one bounded action.
5. Assess the result and write the assessment into `data/logs/` if it is meaningful.
6. Make exactly one recommendation.
7. If the recommendation is auto-allowed by the loop, act on it immediately.
8. Bank, ingest, patch synthesis, rebuild index, lint, commit, and push before the next loop iteration.

Do not use the loop to bypass guardrails. A recommendation that needs non-symmetric `P_n`, exact `n=435`, an exhausted ansatz class, or an interpolation search must stop for user input.

### 3. Ingest workflow

Use this when you produced or received a new report in `data/logs/`.

#### Step A: make sure the source file is correct

Edit the working file in `data/logs/` until it says exactly what you want banked.

Typical examples:

- a decision gate
- a checkpoint note
- a probe report
- a literature verification memo
- a quartic progress note

#### Step B: ingest it

```bash
uv run python -m zeta5_autoresearch.wiki_cli ingest data/logs/<filename>.md
```

This creates:

- a timestamped raw snapshot under `wiki/raw/logs/`
- a source summary page under `wiki/sources/`
- index/log updates

#### Step C: identify the new raw snapshot

```bash
ls -1t wiki/raw/logs/<stem>* | head -3
```

Use the newest timestamped file for citations in synthesis pages.

#### Step D: patch synthesis pages manually

The ingest step does not update all high-level pages automatically.

Typical targets:

- `wiki/frontier.md`
- the relevant audit page
- a computation page
- a conclusion page
- occasionally an entity or literature page

When patching:

- update `sources:` frontmatter to include the newest raw snapshot if appropriate;
- update `last_updated:`;
- update the claims that changed;
- keep wording honest and source-backed.

#### Step E: rebuild the index

```bash
uv run python - <<'PY'
from pathlib import Path
from zeta5_autoresearch.wiki_cli import build_index
build_index(Path('.').resolve())
PY
```

#### Step F: lint the wiki

```bash
uv run python -m zeta5_autoresearch.wiki_cli lint
```

Expected healthy output:

```text
Wiki lint clean.
```

#### Step G: commit and push

Commit:

- the changed synthesis pages
- the new raw snapshot
- the new source summary
- `wiki/index.md`
- `wiki/log.md`

Then push.

### 4. Lint workflow

Run this:

```bash
uv run python -m zeta5_autoresearch.wiki_cli lint
```

Use it:

- after any ingest;
- after major page edits;
- before committing wiki-heavy changes;
- when resuming after a long gap.

## What Must Be Updated After Common Events

### After a new frontier checkpoint

Example: quartic target cache advances from `18 / 65` to `20 / 65`.

Update:

- the working note in `data/logs/`
- ingest it
- `wiki/audits/sym4-sixteen-window-target-partial-cache-progress.md`
- `wiki/audits/sym4-sixteen-window-compute-wall.md`
- `wiki/frontier.md`
- rebuild index
- lint
- commit/push

### After a new hard wall

Update:

- the decision-gate log in `data/logs/`
- ingest it
- the relevant audit page
- `wiki/conclusions/exhausted-ansatz-classes.md` if an ansatz class is now truly exhausted
- `wiki/audits/completed-directions.md` if a direction has finished
- `wiki/frontier.md` if the live frontier changed

### After a literature clarification

Update:

- the literature verification log
- ingest it
- the relevant literature page
- any entity/conclusion pages affected

Critical example:

- if anything touches baseline non-symmetric `P_n`, make sure every relevant page still marks it as not source-backed unless a real primary source changes that fact.

## Current Non-Negotiable Wiki Facts

These facts should stay consistent across pages.

- The explicit non-symmetric baseline `P_n` is not source-backed in the checked primary-source neighborhood.
- The exact-side `n=435` wall is architectural and frozen.
- The strongest banked mathematical object is `Sym^4` sixteen-window.
- The quartic `Sym^4` homogeneous recurrence screen is closed through order `4`.
- The quartic `Sym^4` affine recurrence screen is closed through order `3`.
- The quartic `Sym^4` low-degree polynomial matrix screen is closed over the strict overdetermined range.
- The quartic `Sym^4` generalized non-monic polynomial matrix screen has three target-side exact-follow-up cases.
- The quartic `Sym^4` object-level success and matrix hard walls are not recurrence-level proof.
- Quotient and cross-ratio variants are weaker than normalized invariants in the tested lanes.
- The bounded refinement ladder recurs across packet and transfer directions.

If a page contradicts any of these, fix it.

## Common Commands

### Read current frontier

```bash
sed -n '1,260p' wiki/frontier.md
```

### Inspect recent wiki log entries

```bash
grep '^## \[' wiki/log.md | tail -10
```

### Find newest quartic raw snapshots

```bash
ls -1t wiki/raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note*.md | head -5
```

### Rebuild and lint in one sequence

```bash
uv run python - <<'PY'
from pathlib import Path
from zeta5_autoresearch.wiki_cli import build_index
build_index(Path('.').resolve())
PY
uv run python -m zeta5_autoresearch.wiki_cli lint
```

## Commit Scope Guidance

A wiki commit should usually be narrow and legible.

Good examples:

- `Advance Sym4 target cache through 20 of 65`
- `Add Codex transition handoff`
- `Bank seven-window Plucker decision gate`

Do not mix unrelated wiki maintenance with experimental code unless there is a good reason.

## What Not To Do

- Do not edit files inside `wiki/raw/` by hand.
- Do not leave important research state only in chat.
- Do not update `wiki/frontier.md` without a source-backed raw snapshot behind the change.
- Do not cite mutable `data/logs/` files from synthesized wiki pages when a raw snapshot exists.
- Do not suggest retrying exhausted families before checking the conclusion pages.

## Minimal Resume Checklist

If you only have a minute:

1. Read `wiki/frontier.md`.
2. Read `wiki/conclusions/exhausted-ansatz-classes.md`.
3. Read the audit page for the live object.
4. Check whether the latest `data/logs/` change was already ingested.
5. If not, ingest, patch, rebuild index, lint, commit, and push.
