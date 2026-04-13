---
title: Sym4 Sixteen-Window Target Partial Cache Progress
category: audit
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260413_151907.md
last_updated: '2026-04-13'
---

Audit record for the resumed target-side quartic cache path behind the draft [[sym4-sixteen-window-compute-wall]].

## Object and status

- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor target-side construction
- Status: `engineering progress`, not a banked quartic frontier object
- Cache file: `data/cache/bz_phase2_sym4_sixteen_window_target_partial_cache.json`
- Current banked progress in the latest raw follow-up note: `27 / 65` exact windows

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
- Singular-pivot recovery steps have now cost about `140.81s`, `154.61s`, `188.13s`, `221.46s`, `238.43s`, `254.55s`, `265.43s`, `306.43s`, `320.45s`, `359.54s`, `381.81s`, `418.63s`, and `458.46s`.
- Nonsingular resumed advances have now cost about `84.06s`, `93.39s`, `111.81s`, `124.94s`, `136.17s`, `160.05s`, `166.79s`, `191.74s`, `202.42s`, `230.96s`, `251.87s`, and `272.83s`.

## New structural fact

The cached quartic target-side path exposed a nontrivial rolling obstruction:

- after the second completed window, the rolling state hit `coordinates[0] = 0`
- the naive codimension-one shift is singular there
- a controlled rebase to the next window basis is therefore necessary to continue the cached target-side construction
- by the fifth completed window, a second such singular-pivot recovery step had also been required
- after the sixth completed window, the cached lead returned to zero again
- the seventh completed window did require that next rebase, and the cached lead became nonzero again afterward
- the eighth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the ninth completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the tenth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the eleventh completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the twelfth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the thirteenth completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the fourteenth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the fifteenth completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the sixteenth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the seventeenth completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the eighteenth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the nineteenth completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the twentieth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the twenty-first completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the twenty-second completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the twenty-third completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the twenty-fourth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the twenty-fifth completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the twenty-sixth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the twenty-seventh completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward

That rebase now exists, so the singular pivot is recoverable, but expensive.

## Interpretation

- This is real engineering progress, not yet a proof-side structural success.
- The quartic target-side path is now demonstrably resumable.
- Through the first twenty-seven completed windows, the observed cache pattern still alternates:
  - rebase step
  - ordinary step
  - rebase step
  - ordinary step
- After the twenty-seventh completed window, the cached lead is nonzero again, so the next quartic step is predicted to be an ordinary advance.
- The seventeenth completed window is the first rebase case to break above the prior high-water mark, landing at about `306.43s`.
- The eighteenth completed window is the first ordinary case to break above the prior high-water mark, landing at about `191.74s`.
- The nineteenth completed window lifts the rebase high-water mark again, to about `320.45s`.
- The twentieth completed window lifts the ordinary high-water mark again, to about `202.42s`.
- The twenty-first completed window lifts the rebase high-water mark again, to about `359.54s`.
- The twenty-second completed window lifts the ordinary high-water mark again, to about `230.96s`.
- The twenty-third completed window lifts the rebase high-water mark again, to about `381.81s`.
- The twenty-fourth completed window lifts the ordinary high-water mark again, to about `251.87s`.
- The twenty-fifth completed window lifts the rebase high-water mark again, to about `418.63s`.
- The twenty-sixth completed window lifts the ordinary high-water mark again, to about `272.83s`.
- The twenty-seventh completed window lifts the rebase high-water mark again, to about `458.46s`.
- The remaining wall is no longer “cannot checkpoint”:
  - it is expensive initialization
  - expensive ordinary rolling advances
  - and occasional even more expensive singular-pivot rebases

## Related pages

- [[frontier]]
- [[sym4-sixteen-window-compute-wall]]
- [[sym3-eleven-window-frontier]]
