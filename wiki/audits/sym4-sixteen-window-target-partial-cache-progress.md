---
title: Sym4 Sixteen-Window Target Partial Cache Progress
category: audit
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260410_061105.md
last_updated: '2026-04-10'
---

Audit record for the resumed target-side quartic cache path behind the draft [[sym4-sixteen-window-compute-wall]].

## Object and status

- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor target-side construction
- Status: `engineering progress`, not a banked quartic frontier object
- Cache file: `data/cache/bz_phase2_sym4_sixteen_window_target_partial_cache.json`
- Current banked progress in the latest raw follow-up note: `5 / 65` exact windows

## What is now established

- The target-side quartic path is no longer all-or-nothing.
- A persisted partial cache now stores:
  - rolling common-denominator inverse-row state
  - rolling coordinate numerators
  - exact recovered profile vectors
- The initialization state is now written immediately after it is constructed, so long runs bank usable quartic target-side state before the first profile completes.
- Bounded resume runs are now supported via a fixed per-run completed-window cap.

## Measured costs

- Quartic target-side initialization is about `103.23s`, dominated by the first basis inverse.
- The first completed cached profile was banked after that one-time initialization wall.
- A later ordinary resumed advance cost about `84.06s`.
- Singular-pivot recovery steps have now cost about `140.81s` and `154.61s`.

## New structural fact

The cached quartic target-side path exposed a nontrivial rolling obstruction:

- after the second completed window, the rolling state hit `coordinates[0] = 0`
- the naive codimension-one shift is singular there
- a controlled rebase to the next window basis is therefore necessary to continue the cached target-side construction
- by the fifth completed window, a second such singular-pivot recovery step had also been required

That rebase now exists, so the singular pivot is recoverable, but expensive.

## Interpretation

- This is real engineering progress, not yet a proof-side structural success.
- The quartic target-side path is now demonstrably resumable.
- The remaining wall is no longer “cannot checkpoint”:
  - it is expensive initialization
  - expensive ordinary rolling advances
  - and occasional even more expensive singular-pivot rebases

## Related pages

- [[frontier]]
- [[sym4-sixteen-window-compute-wall]]
- [[sym3-eleven-window-frontier]]
