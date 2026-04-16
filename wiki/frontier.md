---
title: Research Frontier
category: frontier
phase: '2'
direction: frontier
sources:
- raw/logs/bz_dual_f7_companion_normalization_report.md
- raw/logs/bz_phase2_dual_companion_checkpoint.md
- raw/logs/bz_phase2_normalized_plucker_window_invariant_screen.md
- raw/logs/bz_phase2_six_window_plucker_followup_screen.md
- raw/logs/bz_phase2_sym2_seven_window_probe.md
- raw/logs/bz_phase2_sym2_seven_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_seven_window_affine_decision_gate.md
- raw/logs/bz_phase2_sym2_eight_window_probe.md
- raw/logs/bz_phase2_sym2_eight_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_eight_window_affine_decision_gate.md
- raw/logs/bz_phase2_sym3_eleven_window_probe.md
- raw/logs/bz_phase2_sym3_eleven_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym3_eleven_window_affine_decision_gate.md
- raw/logs/bz_phase2_sym4_sixteen_window_object_spec.md
- raw/logs/bz_phase2_sym4_sixteen_window_probe.md
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_ladder_decision_gate.md
- raw/logs/bz_phase2_sym4_sixteen_window_polynomial_matrix_recurrence_screen.md
- raw/logs/bz_phase2_autonomous_directed_iteration_loop.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup.md
- raw/logs/bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup__20260416_123223.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_target_nullspace_fingerprint.md
- raw/logs/bz_phase2_sym4_sixteen_window_compute_wall_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_engineering_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_gmp_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_133336.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_140253.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_142300.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260414_144700.md
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
- raw/logs/bz_phase2_six_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_six_window_normalized_plucker_annihilator_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_global_recurrence_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_matrix_recurrence_screen.md
last_updated: '2026-04-16'
---

Current live frontier: frozen exact-side obstruction through degree 106, plus the beyond-Plücker higher-Schur frontier, where the `Sym^4` sixteen-window object is now the strongest banked nonlinear invariant and a non-monic polynomial matrix screen has produced structured-nullspace target cases.

## Current live frontier

- Exact-side frozen frontier: dual companion caches banked through `n=434`, with the exact cleared-window
  `(1,0,-1,-2)` recurrence family ruled out through degree `106` on window `n<=431`.
- Current strongest lifted object: the [[sym4-sixteen-window-object]] is a repo-native exact paired object on
  `n=1..65`, with coordinate count `15`.
- Current recurrence-screen status: the Sym4 homogeneous matrix ladder is closed through order `4`, and the affine ladder
  is closed through order `3`, on source and target separately.
- Current polynomial-matrix status: every strict overdetermined low-degree polynomial-coefficient extension of those
  matrix ladders is closed on source and target separately.
- Current generalized polynomial-matrix status: the non-monic screen closes most strict overdetermined cases; its three
  target-side order-1 cases survived a bounded independent prime sweep with corrected nullities `150`, `360`, and `150`.
- Current quartic engineering subfrontier: the target-side cached continuation is tracked in
  [[sym4-sixteen-window-target-partial-cache-progress]], with persisted exact progress through `65 / 65` windows and final target sequence cache materialized.
- Immediate predecessor higher-Schur object: the [[sym3-eleven-window-object]] is a repo-native exact paired object on
  `n=1..70`, with coordinate count `10`, and already has homogeneous and affine hard-wall screens through order `6`.
- Immediate predecessor lifted object: the [[sym2-seven-window-object]] is a repo-native exact paired object on
  `n=1..74`, with coordinate count `6`.
- Current banked wider continuation: the [[sym2-eight-window-object]] is a repo-native exact paired object on
  `n=1..73`, with coordinate count `27`.

## Operating mode

Continuation now follows the [[autonomous-directed-iteration-loop]]: snapshot state, run one bounded action, assess, recommend, act on auto-allowed recommendations, then bank and push before the next iteration.

## Active interpretation

- The old exact lane is [[exact-side-frozen-frontier|frozen]], not active.
- The strongest surviving object is now the Sym^4-lifted sixteen-window invariant, not the cubic Sym^3 predecessor or the earlier Sym^2/Plücker lines.
- The Sym^4 sixteen-window object is now banked as a mathematical object, and the target-side cache path is complete:
  - the new rolling codimension-one rewrite makes the source side tractable:
    - `_build_sym4_sixteen_window_side("source")` now completes in about `6.443` seconds
  - the GMP-backed rolling rewrite improves the source side again:
    - `_build_sym4_sixteen_window_side("source")` now completes in about `2.990` seconds
  - the target side was too expensive to bank by an all-or-nothing build, but the resumable cache has now completed:
    - quartic target-side initialization takes about `103.23` seconds
    - cached exact progress has now reached `65 / 65` windows
    - ordinary resumed advances are now about `84.06`, `93.39`, `111.81`, `124.94`, `136.17`, `160.05`, `166.79`, `191.74`, `202.42`, `230.96`, `251.87`, `272.83`, `299.93`, `293.86`, `340.60`, `417.41`, `424.29`, `442.24`, `476.93`, `514.80`, `532.76`, `550.08`, `606.79`, `709.99`, `733.21`, `763.19`, and `822.92` seconds
    - singular-pivot rebases are now about `140.81`, `154.61`, `188.13`, `221.46`, `238.43`, `254.55`, `265.43`, `306.43`, `320.45`, `359.54`, `381.81`, `418.63`, `458.46`, `477.21`, `512.50`, `584.00`, `632.52`, `680.27`, `730.43`, `779.59`, `813.01`, `1110.89`, `1225.92`, and `1177.09` seconds
    - the final `64 / 65 -> 65 / 65` rebase completed the partial cache, but its exact one-window elapsed value is unavailable because final-cache materialization hit Python's integer digit-limit guard after the complete partial-cache write
    - a retry with Python's integer digit guard disabled materialized the final target sequence cache in about `592.86` seconds
    - the final sequence cache exists at `data/cache/bz_phase2_sym4_sixteen_window_target_sequence_cache.json` and is `131681112` bytes
  - the cache path is now resilient against the first discovered singular rolling pivot:
    - after the second completed window the naive codimension-one shift becomes singular
    - a controlled rebase to the next window basis keeps the quartic target-side run alive
    - after the sixth completed window the cached lead was zero again, and the seventh completed window did confirm that next rebase case
    - after the eighth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the ninth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the tenth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the eleventh completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the twelfth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the thirteenth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the fourteenth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the fifteenth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the sixteenth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the seventeenth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the eighteenth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the nineteenth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the twentieth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the twenty-first completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the twenty-second completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the twenty-third completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the twenty-fourth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the twenty-fifth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the twenty-sixth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the twenty-seventh completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the twenty-eighth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the twenty-ninth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the thirtieth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the thirty-first completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the thirty-second completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the thirty-third completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
    - after the thirty-fifth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is expected to be a rebase
    - after the thirty-sixth completed window the cached lead returned to zero again, so the observed alternating pattern still holds and the next quartic step is expected to be a rebase case
    - after the thirty-seventh completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is expected to be an ordinary advance
    - after the thirty-eighth completed window the cached lead returned to zero again, so the observed alternating pattern still holds and the next quartic step is expected to be a rebase case
    - after the thirty-ninth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is expected to be an ordinary advance
    - after the fortieth completed window the cached lead returned to zero again, so the observed alternating pattern still holds and the next quartic step is expected to be a rebase case
    - after the forty-first completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is expected to be an ordinary advancement
    - after the forty-second completed window the cached lead returned to zero again, so the observed alternating pattern still holds and the next quartic step is expected to be a rebase
    - after the forty-third completed window the cached lead became nonzero again, so the observed alternating pattern still holds and the next quartic step is now ordinary
    - after the forty-fourth completed window the cached lead returned to zero again, so the observed alternating pattern still holds and the next quartic step is now a rebase
    - after the forty-fifth completed window the cached lead became nonzero again, so the observed alternating pattern still holds and the next quartic step is now an ordinary advance
    - after the forty-sixth completed window the cached lead returned to zero again, so the observed alternating pattern still holds and the next quartic step was a rebase
    - after the forty-seventh completed window the cached lead became nonzero again, so the observed alternating pattern still holds and the next quartic step was ordinary
    - after the forty-eighth completed window the cached lead became zero again, so the observed alternating pattern still holds and the next quartic step is now expected to be a rebase
    - after the fifty-fourth completed window the cached lead remained at zero, with a new ordinary high-water mark at about `606.79` seconds
    - at continuation resume, the persisted cache was directly verified at `57 / 65`, with `state_window_index = 56`, `next_window_index = 57`, and nonzero lead
    - the latest measured ordinary step advanced `57 / 65 -> 58 / 65` in about `709.99` seconds, leaving `state_window_index = 57`, `next_window_index = 58`, and `lead = 0`
    - the latest measured rebase step advanced `58 / 65 -> 59 / 65` in about `1110.89` seconds, leaving `state_window_index = 58`, `next_window_index = 59`, and nonzero lead
    - the latest measured ordinary step advanced `59 / 65 -> 60 / 65` in about `733.21` seconds, leaving `state_window_index = 59`, `next_window_index = 60`, and `lead = 0`
    - the latest measured rebase step advanced `60 / 65 -> 61 / 65` in about `1225.92` seconds, leaving `state_window_index = 60`, `next_window_index = 61`, and nonzero lead
    - the latest measured ordinary step advanced `61 / 65 -> 62 / 65` in about `763.19` seconds, leaving `state_window_index = 61`, `next_window_index = 62`, and `lead = 0`
    - the latest measured rebase step advanced `62 / 65 -> 63 / 65` in about `1177.09` seconds, leaving `state_window_index = 62`, `next_window_index = 63`, and nonzero lead
    - the latest measured ordinary step advanced `63 / 65 -> 64 / 65` in about `822.92` seconds, leaving `state_window_index = 63`, `next_window_index = 64`, and `lead = 0`
    - the final rebase advanced `64 / 65 -> 65 / 65`, leaving `state_window_index = 65`, `next_window_index = 65`, `status = complete`, and `65` stored profiles after final materialization
  - live timing therefore narrows the quartic wall further:
    - the remaining blocker is not target-side cache completion
    - it is recurrence-level screening of the full paired quartic object
    - the final rebase exceeded the prior `1225.92` second rebase high-water by live wall-clock observation, but exact elapsed time was not printed because of the post-write digit-limit exception
    - the latest ordinary step rose to about `822.92` seconds, extending the new higher ordinary-step band
  - so `Sym^4` is promoted at the object level, with both natural low-order matrix hard walls now banked
- The Sym^4-lifted object now closes both natural low-order nonlocal ladders:
  - homogeneous source-side orders `1..4` are inconsistent mod `1009`
  - homogeneous target-side orders `1..4` are inconsistent mod `1451`
  - order `5` is the first underdetermined homogeneous case
  - affine source-side orders `1..3` are inconsistent mod `1009`
  - affine target-side orders `1..3` are inconsistent mod `1451`
  - affine order `4` is the first non-overdetermined affine case
- The Sym^4-lifted object also closes the strict overdetermined polynomial-coefficient matrix extension:
  - homogeneous `(order, degree) = (1,1)`, `(1,2)`, `(1,3)`, and `(2,1)` close on source and target
  - affine `(order, degree) = (1,1)`, `(1,2)`, and `(2,1)` close on source and target
  - source-side witness prime is `1009`
  - target-side witness prime is `1451`
- The Sym^4-lifted generalized, non-monic polynomial matrix screen now gives the live exact-follow-up lead:
  - homogeneous target-side `(order, degree) = (1,2)`
  - homogeneous target-side `(order, degree) = (1,3)`
  - affine target-side `(order, degree) = (1,2)`
  - a bounded follow-up over primes `1451`, `1009`, `1453`, `1459`, `1471`, `1481`, `1483`, `1487`, `1489`, and `1493` did not find a full-column-rank obstruction
  - corrected good-prime nullities are `150` for homogeneous `(1,2)`, `360` for homogeneous `(1,3)`, and `150` for affine `(1,2)`; primes `1009` and `1459` were denominator-singular for the target data
  - the affine target fingerprint has stable free columns `M[2,0,i,j]` for `i=0..14`, `j=5..14`
  - these are not banked recurrences; they are structured-nullspace follow-up targets
- The Sym^3-lifted object already closes both natural low-order nonlocal ladders:
  - homogeneous source-side orders `1..6` are inconsistent mod `1009`
  - homogeneous target-side orders `1..6` are inconsistent mod `1447`
  - affine source-side orders `1..6` are inconsistent mod `1009`
  - affine target-side orders `1..6` are inconsistent mod `1447`
  - order `7` is the first underdetermined case for both ladders
- The Sym^2-lifted object already closes both natural low-order nonlocal ladders:
  - homogeneous source-side orders `1..10` are inconsistent mod `1009`
  - homogeneous target-side orders `1..10` are inconsistent mod `1447`
  - affine source-side orders `1..10` are inconsistent mod `1009`
  - affine target-side orders `1..10` are inconsistent mod `1447`
  - order `11` is the first underdetermined case for both ladders
- The wider Sym^2 eight-window continuation is also now banked:
  - homogeneous source-side orders `1..2` are inconsistent mod `1009`
  - homogeneous target-side orders `1..2` are inconsistent mod `1447`
  - affine source-side orders `1..2` are inconsistent mod `1009`
  - affine target-side orders `1..2` are inconsistent mod `1447`
  - order `3` is the first underdetermined case for both ladders
- The eight-window normalized Plücker object remains valuable as the immediate predecessor frontier, and it already closed:
  - the last overdetermined constant-matrix screen at order `1`
- The seven-window normalized Plücker object remains valuable as the earlier predecessor frontier, and it already closed:
  - low-order homogeneous constant-matrix recurrence through order `2`
  - low-order affine constant-matrix recurrence through order `2`
- The six-window object remains valuable as the earlier predecessor frontier, and it already closed:
  - bounded transfer-ladder families
  - short local-annihilator families
  - low-order global shared-scalar vector recurrences
  - low-order constant matrix recurrence through order `3`
- The [[sym4-matrix-ladders-exhausted]] decision gate now blocks mechanical order escalation on the quartic matrix ladders:
  - the target-side cached build is complete
  - the quartic object is banked
  - the homogeneous and affine low-order matrix ladders are both exhausted
  - the low-degree polynomial-coefficient matrix extension is exhausted over its strict overdetermined range
  - the next defensible move requires a genuinely different structural family or a new source-backed identity
- Another cheap local, scalar, quotient, affine, order-escalated constant-matrix, or polynomial-degree-escalated matrix family is still not justified on the banked frontier objects.

## Related pages

- [[exact-side-frozen-frontier]]
- [[sym3-eleven-window-object]]
- [[sym3-eleven-window-frontier]]
- [[sym3-eleven-window-matrix-recurrence-screen]]
- [[sym3-eleven-window-affine-matrix-screen]]
- [[sym4-sixteen-window-matrix-recurrence-screen]]
- [[sym4-sixteen-window-affine-matrix-screen]]
- [[sym4-sixteen-window-polynomial-matrix-screen]]
- [[sym4-sixteen-window-generalized-polynomial-matrix-screen]]
- [[sym4-sixteen-window-generalized-polynomial-matrix-followup]]
- [[sym4-sixteen-window-affine-target-nullspace-fingerprint]]
- [[sym4-generalized-polynomial-matrix-lead]]
- [[sym4-matrix-ladders-exhausted]]
- [[autonomous-directed-iteration-loop]]
- [[sym4-sixteen-window-compute-wall]]
- [[sym4-sixteen-window-target-partial-cache-progress]]
- [[sym2-seven-window-object]]
- [[sym2-seven-window-frontier]]
- [[sym2-seven-window-matrix-recurrence-screen]]
- [[sym2-seven-window-affine-matrix-screen]]
- [[sym2-eight-window-object]]
- [[sym2-eight-window-frontier]]
- [[sym2-eight-window-matrix-recurrence-screen]]
- [[sym2-eight-window-affine-matrix-screen]]
- [[eight-window-normalized-plucker-object]]
- [[eight-window-normalized-plucker-frontier]]
- [[eight-window-normalized-plucker-matrix-recurrence-screen]]
- [[seven-window-normalized-plucker-object]]
- [[seven-window-normalized-plucker-affine-matrix-screen]]
- [[six-window-normalized-plucker-object]]
- [[six-window-normalized-plucker-hard-wall]]
- [[six-window-normalized-plucker-annihilator-screen]]
- [[six-window-normalized-plucker-global-recurrence-screen]]
- [[six-window-normalized-plucker-matrix-recurrence-screen]]
- [[exhausted-ansatz-classes]]
- [[completed-directions]]
