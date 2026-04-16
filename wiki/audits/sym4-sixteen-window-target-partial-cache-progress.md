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
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_182422.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_183904.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_190150.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_191647.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_194016.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_195648.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_203158.md
last_updated: '2026-04-15'
---

Audit record for the resumed target-side quartic cache path behind the draft [[sym4-sixteen-window-compute-wall]].

## Object and status

- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor target-side construction
- Status: `engineering progress`, not a banked quartic frontier object
- Cache file: `data/cache/bz_phase2_sym4_sixteen_window_target_partial_cache.json`
- Current banked progress in the latest raw follow-up note: `65 / 65` exact windows, with partial-cache status `complete`

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
- Singular-pivot recovery steps have now cost about `140.81s`, `154.61s`, `188.13s`, `221.46s`, `238.43s`, `254.55s`, `265.43s`, `306.43s`, `320.45s`, `359.54s`, `381.81s`, `418.63s`, `458.46s`, `477.21s`, `512.50s`, `584.00s`, `632.52s`, `680.27s`, `730.43s`, `779.59s`, `813.01s`, `1110.89s`, `1225.92s`, and `1177.09s`.
- Nonsingular resumed advances have now cost about `84.06s`, `93.39s`, `111.81s`, `124.94s`, `136.17s`, `160.05s`, `166.79s`, `191.74s`, `202.42s`, `230.96s`, `251.87s`, `272.83s`, `299.93s`, `293.86s`, `340.60s`, `417.41s`, `424.29s`, `442.24s`, `476.93s`, `514.80s`, `532.76s`, `550.08s`, `606.79s`, `709.99s`, `733.21s`, `763.19s`, and `822.92s`.
- The most recent continuation completed the partial cache, advancing `64 / 65 -> 65 / 65`; its one-window `perf_counter` elapsed value is unavailable because a post-write digit-limit exception occurred before the wrapper printed it.
- A follow-up final sequence-cache materialization run with Python's integer digit guard disabled returned clean `complete` status in about `592.86s`.

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
- the next bounded continuation confirmed the predicted rebase case to `59 / 65`, with `state_window_index = 58`, `next_window_index = 59`, and nonzero lead
- the next bounded continuation confirmed the predicted ordinary case to `60 / 65`, with `state_window_index = 59`, `next_window_index = 60`, and lead `0`
- the next bounded continuation confirmed the predicted rebase case to `61 / 65`, with `state_window_index = 60`, `next_window_index = 61`, and nonzero lead
- the next bounded continuation confirmed the predicted ordinary case to `62 / 65`, with `state_window_index = 61`, `next_window_index = 62`, and lead `0`
- the next bounded continuation confirmed the predicted rebase case to `63 / 65`, with `state_window_index = 62`, `next_window_index = 63`, and nonzero lead
- the next bounded continuation confirmed the predicted ordinary case to `64 / 65`, with `state_window_index = 63`, `next_window_index = 64`, and lead `0`
- the final continuation confirmed the predicted rebase case to `65 / 65`; after the digit-limit materialization retry, the cache had `state_window_index = 65`, `next_window_index = 65`, `status = complete`, and `65` stored profiles

The target-side rebase path therefore reaches the full cached window count, but at high exact-arithmetic cost.

## Interpretation

- This is real engineering progress, not yet a proof-side structural success.
- The quartic target-side path is now demonstrably resumable.
- Through the completed `65 / 65` checkpoint, the observed cache pattern remains compatible with:
  - rebase step
  - ordinary step
  - rebase step
  - ordinary step
  - rebase step
  - ordinary step
  - rebase step
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
- The measured `58 / 65 -> 59 / 65` continuation was the predicted rebase and took about `1110.89s`.
- The measured `59 / 65 -> 60 / 65` continuation was the predicted ordinary advance and took about `733.21s`.
- The measured `60 / 65 -> 61 / 65` continuation was the predicted rebase and took about `1225.92s`.
- The measured `61 / 65 -> 62 / 65` continuation was the predicted ordinary advance and took about `763.19s`.
- The measured `62 / 65 -> 63 / 65` continuation was the predicted rebase and took about `1177.09s`.
- The measured `63 / 65 -> 64 / 65` continuation was the predicted ordinary advance and took about `822.92s`.
- The final `64 / 65 -> 65 / 65` continuation was the predicted rebase and completed the partial cache; exact one-window timing is unavailable because the post-write final-cache materialization hit Python's integer digit-limit guard before the wrapper printed elapsed time.
- At `65 / 65`, there is no remaining target-side cache window to advance.
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
- The fifty-ninth completed window lifts the rebase high-water mark again, to about `1110.89s`.
- The sixtieth completed window lifts the ordinary high-water mark again, to about `733.21s`.
- The sixty-first completed window lifts the rebase high-water mark again, to about `1225.92s`.
- The sixty-second completed window lifts the ordinary high-water mark again, to about `763.19s`.
- The sixty-third completed window was another rebase case, landing below the current rebase high-water mark at about `1177.09s`.
- The sixty-fourth completed window lifts the ordinary high-water mark again, to about `822.92s`.
- The sixty-fifth completed window finished the target-side partial cache as another rebase case; live wall-clock observation showed it exceeded the prior `1225.92s` rebase high-water, but the exact elapsed value was not printed because of the post-write digit-limit exception.
- The final sequence cache now exists at `data/cache/bz_phase2_sym4_sixteen_window_target_sequence_cache.json`, with size `131681112` bytes.
- The target-cache wall has now been crossed, but this is still not proof-side promotion:
  - the completed target cache needs audit inside the full quartic paired-object construction
  - final sequence-cache materialization requires Python's integer digit guard disabled, or equivalent internal parsing support
  - `Sym^4` remains unbanked as a mathematical frontier object until that audit succeeds

## Related pages

- [[frontier]]
- [[sym4-sixteen-window-compute-wall]]
- [[sym3-eleven-window-frontier]]
