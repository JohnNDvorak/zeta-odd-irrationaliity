# LLM Wiki — ζ(5) Irrationality via Brown–Zudilin M₀,₈

This wiki is the agent-managed knowledge layer for the `zeta5-autoresearch` repo.

## Core Rules

- `wiki/raw/` is immutable source material.
- The agent may update `wiki/` pages, `wiki/index.md`, `wiki/log.md`, and `wiki/frontier.md`.
- Wiki pages cite only `wiki/raw/...` snapshots.
- All cross-references between pages use `[[wikilinks]]`.
- Every page carries YAML frontmatter with:
  - `title`
  - `category`
  - `phase`
  - `direction`
  - `sources`
  - `last_updated`

## Program Goal

Prove the irrationality of `ζ(5)` using Brown–Zudilin's `M₀,₈` cellular integral framework by constructing an
Apéry-type linear form with exponentially small value relative to denominator growth.

## Banked Program History

- Phase 1: build infrastructure, extract exact objects, run recurrence obstruction campaigns, and hit the exact
  `n = 435` kernel wall.
- Phase 2: freeze the blocked lane, pivot to source-backed decay-side objects, build bridges and transfer objects,
  and map the structural landscape via exact decision gates.

## Operational Rules

- Never cite `data/logs/`, `src/`, or `refs/` directly from the wiki; ingest through `wiki/raw/`.
- Track hard walls and exhausted ansatz classes as carefully as positive results.
- Keep the non-symmetric baseline `P_n` marked as `not source-backed` unless a raw source proves otherwise.
- Treat the Zudilin 2002 recurrence as a calibration anchor, not as the Brown–Zudilin baseline object.
- Treat the six-window normalized Plücker object as the current nonlinear frontier.
