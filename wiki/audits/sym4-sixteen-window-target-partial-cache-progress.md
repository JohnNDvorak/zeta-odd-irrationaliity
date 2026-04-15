---
title: Sym4 Sixteen-Window Target Partial Cache Progress
category: audit
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_140253.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_142300.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_144700.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_150211.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_151430.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_152257.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_153607.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_154502.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_155921.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_160833.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_200453.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_202010.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_203021.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_092259.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_101404.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_180051.md
last_updated: '2026-04-15'
---

Audit record for the resumed target-side quartic cache path behind the draft [[sym4-sixteen-window-compute-wall]].

## Object and status

- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor target-side construction
- Status: `engineering progress`, not a banked quartic frontier object
- Cache file: `data/cache/bz_phase2_sym4_sixteen_window_target_partial_cache.json`
- Current banked progress in the latest raw follow-up note: `58 / 65` exact windows

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
- Singular-pivot recovery steps have now cost about `140.81s`, `154.61s`, `188.13s`, `221.46s`, `238.43s`, `254.55s`, `265.43s`, `306.43s`, `320.45s`, `359.54s`, `381.81s`, `418.63s`, `458.46s`, `477.21s`, `512.50s`, `584.00s`, `632.52s`, `680.27s`, `730.43s`, `779.59s`, and `813.01s`.
- Nonsingular resumed advances have now cost about `84.06s`, `93.39s`, `111.81s`, `124.94s`, `136.17s`, `160.05s`, `166.79s`, `191.74s`, `202.42s`, `230.96s`, `251.87s`, `272.83s`, `299.93s`, `293.86s`, `340.60s`, `417.41s`, `424.29s`, `442.24s`, `476.93s`, `514.80s`, `532.76s`, `550.08s`, `606.79s`, and `709.99s`.
- The most recent measured continuation added one completed window, advancing `57 / 65 -> 58 / 65` with bounded resume time `709.99s`.

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
- the twenty-eighth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the twenty-ninth completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the thirtieth completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the thirty-first completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the thirty-second completed window was again a nonsingular ordinary advance, and the cached lead returned to zero afterward
- the thirty-third completed window again required a singular-pivot recovery step, and the cached lead became nonzero again afterward
- the thirty-fifth completed window required pre-step rebase-state alignment followed by a profile write, and the cached lead remained nonzero afterward
- the thirty-sixth completed window was again an ordinary advance, and the cached lead returned to zero afterward
- the thirty-seventh completed window required a rebase step, and the cached lead became nonzero again afterward
- the thirty-eighth completed window was another ordinary advance, and the cached lead returned to zero again afterward
- the thirty-ninth completed window was another rebase step, and the cached lead became nonzero again afterward
- the fortieth completed window was another ordinary advance, and the cached lead returned to zero again afterward
- the forty-first completed window was another rebase step, and the cached lead became nonzero again afterward
- the forty-second completed window was another ordinary advance, and the cached lead returned to zero again afterward
- the forty-third completed window was another rebase step, and the cached lead remained nonzero afterward
- the forty-fourth completed window was another ordinary advance, and the cached lead returned to zero again afterward
- the forty-fifth completed window was another rebase step, and the cached lead became nonzero again afterward
- the forty-sixth completed window was another ordinary advance, and the cached lead returned to zero again afterward
- the forty-seventh completed window was another rebase step, and the cached lead became nonzero again afterward
- the forty-eighth completed window was another ordinary advance, and the cached lead became zero again afterward
- the fifty-fourth completed window was another measured ordinary advance, and the cached lead became zero again afterward
- at the start of the latest continuation the persisted cache was directly verified at `57 / 65`, with `state_window_index = 56`, `next_window_index = 57`, and nonzero lead
- the latest bounded continuation was an ordinary advance to `58 / 65`, with `state_window_index = 57`, `next_window_index = 58`, and lead `0`

That rebase now exists, so the singular pivot is recoverable, but expensive.

## Interpretation

- This is real engineering progress, not yet a proof-side structural success.
- The quartic target-side path is now demonstrably resumable.
- Through the latest `58 / 65` checkpoint, the observed cache pattern remains compatible with:
  - rebase step
  - ordinary step
  - rebase step
  - ordinary step
- After the fortieth completed window, the cached lead returned to zero again, so the next quartic step was a rebase.
- After the forty-first completed window, the cached lead became nonzero again, so the next quartic step was ordinary.
- After the forty-second completed window, the cached lead returned to zero again, so the next quartic step was a rebase.
- After the forty-third completed window, the cached lead became nonzero again, so the next quartic step was ordinary.
- After the forty-fourth completed window, the cached lead returned to zero again, so the next quartic step was a rebase.
- After the forty-fifth completed window, the cached lead became nonzero again, so the next quartic step was ordinary.
- After the forty-sixth completed window, the cached lead returned to zero again, so the next quartic step was a rebase.
- After the forty-seventh completed window, the cached lead became nonzero again, so the next quartic step was an ordinary advance.
- After the forty-eighth completed window, the cached lead returned to zero again, so the next quartic step was a rebase.
- At resume, the persisted cache was verified at `57 / 65` with nonzero lead.
- The measured `57 / 65 -> 58 / 65` continuation was an ordinary advance taking about `709.99s`.
- At `58 / 65`, the cached lead is zero again, so the next quartic step is expected to be a rebase.
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
- The twenty-eighth completed window lifts the ordinary high-water mark again, to about `299.93s`.
- The twenty-ninth completed window lifts the rebase high-water mark again, to about `477.21s`.
- The thirtieth completed window was another ordinary advance, landing below the current ordinary high-water mark at about `293.86s`.
- The thirty-first completed window lifts the rebase high-water mark again, to about `512.50s`.
- The thirty-second completed window lifts the ordinary high-water mark again, to about `340.60s`.
- The thirty-third completed window lifts the rebase high-water mark again, to about `584.00s`.
- The thirty-fifth completed window lifts the rebase high-water mark again, to about `632.52s`.
- The thirty-sixth completed window lifts the ordinary high-water mark again, to about `417.41s`.
- The thirty-eighth completed window lifts the ordinary high-water mark again, to about `424.29s`.
- The thirty-ninth completed window lifts the rebase high-water mark again, to about `680.27s`.
- The fortieth completed window lifts the ordinary high-water mark again, to about `442.24s`.
- The forty-first completed window lifts the rebase high-water mark again, to about `730.43s`.
- The forty-second completed window lifts the ordinary high-water mark again, to about `476.93s`.
- The forty-third completed window lifts the rebase high-water mark again, to about `779.59s`.
- The forty-fourth completed window lifts the ordinary high-water mark again, to about `514.80s`.
- The forty-sixth completed window lifts the ordinary high-water mark again, to about `532.76s`.
- The forty-seventh completed window lifts the rebase high-water mark again, to about `813.01s`.
- The forty-eighth completed window lifts the ordinary high-water mark again, to about `550.08s`.
- The fifty-fourth completed window lifts the ordinary high-water mark again, to about `606.79s`.
- The fifty-eighth completed window lifts the ordinary high-water mark again, to about `709.99s`.
- The remaining wall is no longer “cannot checkpoint”:
  - it is expensive initialization
  - expensive ordinary rolling advances
  - and occasional even more expensive singular-pivot rebases

## Related pages

- [[frontier]]
- [[sym4-sixteen-window-compute-wall]]
- [[sym3-eleven-window-frontier]]
