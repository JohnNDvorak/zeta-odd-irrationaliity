---
title: Sym4 Sixteen-Window Compute Wall
category: audit
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_compute_wall_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_object_spec.md
- raw/logs/bz_phase2_sym4_sixteen_window_probe.md
- raw/logs/bz_phase2_sym4_sixteen_window_engineering_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_gmp_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_133336.md
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
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_matrix_recurrence_screen.md
last_updated: '2026-04-15'
---

Audit record for the attempted quartic higher-Schur continuation beyond the banked [[sym3-eleven-window-object]].

## Object and status

- Draft object: `Sym^4`-lifted sixteen-window normalized maximal-minor object
- Intended coordinate count: `15`
- Intended shared exact window: `n=1..65`
- Status: target cache completed; object-level probe banked; homogeneous recurrence screen closed through order `4`; affine screen closed through order `3`

## What was established

- The quartic lift support was added to the higher-Schur helper layer.
- The codimension-one normalized maximal-minor solver was improved from direct `Fraction` elimination to row-scaled integer elimination with rational back-substitution.
- The rolling codimension-one path was then strengthened again by:
  - per-column integerization
  - common-denominator row encoding
  - common-denominator coordinate updates with `Fraction` reconstruction deferred to output only
- Low-level exact arithmetic checks stayed green after the new rolling rewrite, with `11` passing checks.
- The rolling integer state was then pushed onto a GMP-backed big-integer path when `gmpy2` is available.

## Failure mode

The first full quartic tranche did not produce a banked object within practical turn-time:

- before the solver rewrite, the quartic pytest tranche ran at saturated CPU for more than `9` minutes without completing
- after the first solver rewrite, the quartic pytest tranche again ran at saturated CPU for more than `9` minutes without completing
- after the rolling rewrite, the quartic line split asymmetrically:
  - source-side `_build_sym4_sixteen_window_side("source")` completed in approximately `6.443` seconds
  - target-side `_build_sym4_sixteen_window_side("target")` still did not finish during a bounded run exceeding `180` seconds
- after the GMP-backed rolling rewrite, the split sharpened further:
  - source-side `_build_sym4_sixteen_window_side("source")` improved again to approximately `2.990` seconds
  - target-side `_build_sym4_sixteen_window_side("target")` still did not finish during a bounded run exceeding `180` seconds
- after the persisted target-side partial-cache follow-up:
  - the quartic target-side path became resumable instead of all-or-nothing
  - initialization was timed at approximately `103.23` seconds
- exact cached progress reached `65 / 65` windows, completing the target-side partial cache
  - ordinary resumed advances still cost approximately `84.06`, `93.39`, `111.81`, `124.94`, `136.17`, `160.05`, `166.79`, `191.74`, `202.42`, `230.96`, `251.87`, `272.83`, `299.93`, `293.86`, `340.60`, `417.41`, `424.29`, `442.24`, `476.93`, `514.80`, `532.76`, `550.08`, `606.79`, `709.99`, `733.21`, `763.19`, and `822.92` seconds
  - singular-pivot recovery rebases cost approximately `140.81`, `154.61`, `188.13`, `221.46`, `238.43`, `254.55`, `265.43`, `306.43`, `320.45`, `359.54`, `381.81`, `418.63`, `458.46`, `477.21`, `512.50`, `584.00`, `632.52`, `680.27`, `730.43`, `779.59`, `813.01`, `1110.89`, `1225.92`, and `1177.09` seconds
  - the next predicted rebase after the sixth completed window did occur, and the lead became nonzero again afterward
  - the next predicted ordinary step after the seventh completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the eighth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the ninth completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the tenth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the eleventh completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the twelfth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the thirteenth completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the fourteenth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the fifteenth completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the sixteenth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the seventeenth completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the eighteenth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the nineteenth completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the twentieth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the twenty-first completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the twenty-second completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the twenty-third completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the twenty-fourth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the twenty-fifth completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the twenty-sixth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the twenty-seventh completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the twenty-eighth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the twenty-ninth completed window also occurred, and the lead returned to zero afterward
  - the next predicted rebase after the thirtieth completed window also occurred, and the lead became nonzero again afterward
  - the next predicted ordinary step after the thirty-first completed window also occurred, and the lead returned to zero afterward
  - the thirty-third completed window also required a rebase, and the lead became nonzero again afterward
  - the thirty-fifth completed window required rebase-state alignment before profile write, and the lead remained nonzero again afterward
  - the thirty-sixth completed window required ordinary advancement, and the lead returned to zero again afterward
  - the thirty-seventh completed window required rebase advancement, and the lead became nonzero again afterward
  - the thirty-eighth completed window required ordinary advancement, and the lead returned to zero again afterward
  - the thirty-ninth completed window required rebase advancement, and the lead became nonzero again afterward
  - the fortieth completed window required ordinary advancement, and the lead returned to zero again afterward
  - the forty-first completed window required rebase advancement, and the lead became nonzero again afterward
  - the forty-second completed window required ordinary advancement, and the lead returned to zero again afterward
  - the forty-third completed window required rebase advancement, and the lead remained nonzero again afterward
  - the forty-fourth completed window required ordinary advancement, and the lead returned to zero again afterward
  - the forty-fifth completed window required rebase advancement, and the lead became nonzero again afterward
  - the forty-sixth completed window required ordinary advancement, and the lead returned to zero again afterward
  - the forty-seventh completed window required rebase advancement, and the lead became nonzero again afterward
  - the forty-eighth completed window required ordinary advancement, and the lead returned to zero again afterward
  - the fifty-fourth completed window required ordinary advancement, and the lead returned to zero again.
  - at continuation resume, the persisted cache was directly verified at `57 / 65`, with `state_window_index = 56`, `next_window_index = 57`, and nonzero lead
  - the latest measured continuation advanced `57 / 65 -> 58 / 65` as an ordinary step in approximately `709.99` seconds, returning the lead to zero
  - the next measured continuation advanced `58 / 65 -> 59 / 65` as a rebase step in approximately `1110.89` seconds, returning the lead to nonzero
  - the next measured continuation advanced `59 / 65 -> 60 / 65` as an ordinary step in approximately `733.21` seconds, returning the lead to zero
  - the next measured continuation advanced `60 / 65 -> 61 / 65` as a rebase step in approximately `1225.92` seconds, returning the lead to nonzero
  - the next measured continuation advanced `61 / 65 -> 62 / 65` as an ordinary step in approximately `763.19` seconds, returning the lead to zero
  - the next measured continuation advanced `62 / 65 -> 63 / 65` as a rebase step in approximately `1177.09` seconds, returning the lead to nonzero
  - the next measured continuation advanced `63 / 65 -> 64 / 65` as an ordinary step in approximately `822.92` seconds, returning the lead to zero
  - the final continuation advanced `64 / 65 -> 65 / 65` as a rebase step, completing the partial cache; exact one-window elapsed time is unavailable because final-cache materialization failed after the complete partial-cache write and before elapsed printing
  - a retry with Python's integer digit guard disabled materialized the final target sequence cache in approximately `592.86` seconds
- the current persisted point is now `65 / 65`, with `state_window_index = 65`, `next_window_index = 65`, `status = complete`, and `65` stored profiles

Live process sampling and timing now point to a narrower blocker:

- the original elimination hotspot was reduced enough for the source side to become tractable
- the remaining active wall is target-side exact sixteen-window normalized maximal-minor construction
- more precisely, it is the cost of target-side rolling advancement and occasional singular-pivot rebasing inside that construction
- the persisted path through sixty-five completed windows is consistent with an alternating rebase / ordinary-step pattern rather than a one-off singularity
- the seventeenth completed window is the first rebase case to break above the previous high-water mark, so the rebase-cost curve is still rising rather than flat
- the eighteenth completed window is the first ordinary case to break above the previous high-water mark, so ordinary-step cost is also still rising rather than flat
- the nineteenth completed window lifted the rebase high-water mark again to about `320.45` seconds
- the twentieth completed window lifted the ordinary high-water mark again to about `202.42` seconds
- the twenty-first completed window lifted the rebase high-water mark again to about `359.54` seconds
- the twenty-second completed window lifted the ordinary high-water mark again to about `230.96` seconds
- the twenty-third completed window lifted the rebase high-water mark again to about `381.81` seconds
- the twenty-fourth completed window lifted the ordinary high-water mark again to about `251.87` seconds
- the twenty-fifth completed window lifted the rebase high-water mark again to about `418.63` seconds
- the twenty-sixth completed window lifted the ordinary high-water mark again to about `272.83` seconds
- the twenty-seventh completed window lifted the rebase high-water mark again to about `458.46` seconds
- the twenty-eighth completed window lifted the ordinary high-water mark again to about `299.93` seconds
- the twenty-ninth completed window lifted the rebase high-water mark again to about `477.21` seconds
- the thirtieth completed window was another ordinary advance, landing below the current ordinary high-water mark at about `293.86` seconds
- the thirty-first completed window lifted the rebase high-water mark again to about `512.50` seconds
- the thirty-second completed window lifted the ordinary high-water mark again to about `340.60` seconds
- the thirty-third completed window lifted the rebase high-water mark again to about `584.00` seconds
- the thirty-fifth completed window lifted the rebase high-water mark again to about `632.52` seconds
- the thirty-sixth completed window lifted the ordinary high-water mark again to about `417.41` seconds
- the thirty-eighth completed window lifted the ordinary high-water mark again to about `424.29` seconds
- the thirty-ninth completed window lifted the rebase high-water mark again to about `680.27` seconds
- the fortieth completed window lifted the ordinary high-water mark again to about `442.24` seconds
- the forty-first completed window lifted the rebase high-water mark again to about `730.43` seconds
- the forty-second completed window lifted the ordinary high-water mark again to about `476.93` seconds
- the forty-third completed window lifted the rebase high-water mark again to about `779.59` seconds
- the forty-fourth completed window lifted the ordinary high-water mark again to about `514.80` seconds
- the forty-sixth completed window lifted the ordinary high-water mark again to about `532.76` seconds
- the forty-seventh completed window lifted the rebase high-water mark again to about `813.01` seconds
- the forty-eighth completed window lifted the ordinary high-water mark again to about `550.08` seconds
- the fifty-fourth completed window lifted the ordinary high-water mark again to about `606.79` seconds
- the fifty-eighth completed window lifted the ordinary high-water mark again to about `709.99` seconds
- the fifty-ninth completed window lifted the rebase high-water mark again to about `1110.89` seconds
- the sixtieth completed window lifted the ordinary high-water mark again to about `733.21` seconds
- the sixty-first completed window lifted the rebase high-water mark again to about `1225.92` seconds
- the sixty-second completed window lifted the ordinary high-water mark again to about `763.19` seconds
- the sixty-third completed window was another rebase case, landing below the current rebase high-water mark at about `1177.09` seconds
- the sixty-fourth completed window lifted the ordinary high-water mark again to about `822.92` seconds
- the sixty-fifth completed window completed the target-side partial cache as another rebase case; live wall-clock observation showed it exceeded the prior `1225.92` second rebase high-water, but the exact elapsed value was not printed because of a post-write digit-limit exception
- the final target sequence cache now exists at `data/cache/bz_phase2_sym4_sixteen_window_target_sequence_cache.json` and is `131681112` bytes
- there is no immediate easy win from changing the quartic lifted-vector integerization formula alone; early target samples matched the direct base-derived quartic integer chart exactly

## Interpretation

This is engineering progress, not yet a mathematical obstruction result:

- `Sym^4` sixteen-window has now been certified as a repo-native exact paired object
- the object-level higher-Schur frontier has moved to [[sym4-sixteen-window-object]]
- homogeneous and affine hard-wall certificates have now been banked on the quartic object itself
- the quartic wall has moved:
  - source side tractable and materially faster after the GMP-backed rolling rewrite
  - target side no longer blocked at the cache-construction level
  - final target sequence-cache materialization requires handling Python's large integer-string guard
- resuming the quartic line now requires a genuinely different structural family, not pushing another target window or mechanically increasing matrix order

The current best continuation inside the quartic lane is now recorded separately in [[sym4-sixteen-window-target-partial-cache-progress]].
