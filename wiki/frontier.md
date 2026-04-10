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
- raw/logs/bz_phase2_sym4_sixteen_window_compute_wall_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_engineering_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_gmp_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260410_123906.md
- raw/logs/bz_phase2_six_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_six_window_normalized_plucker_annihilator_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_global_recurrence_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_matrix_recurrence_screen.md
last_updated: '2026-04-10'
---

Current live frontier: frozen exact-side obstruction through degree 106, plus the beyond-Plücker higher-Schur frontier, where the `Sym^3` eleven-window object remains the strongest banked nonlinear invariant and the attempted `Sym^4` continuation has now advanced from a pure compute wall to a resumable but still expensive target-side cached construction.

## Current live frontier

- Exact-side frozen frontier: dual companion caches banked through `n=434`, with the exact cleared-window
  `(1,0,-1,-2)` recurrence family ruled out through degree `106` on window `n<=431`.
- Current strongest lifted object: the [[sym3-eleven-window-object]] is a repo-native exact paired object on
  `n=1..70`, with coordinate count `10`.
- Current blocked continuation: the attempted quartic sixteen-window continuation is tracked in
  [[sym4-sixteen-window-compute-wall]] and is not yet a banked frontier object.
- Current quartic engineering subfrontier: the target-side cached continuation is tracked in
  [[sym4-sixteen-window-target-partial-cache-progress]], with persisted exact progress through `9 / 65` windows.
- Immediate predecessor lifted object: the [[sym2-seven-window-object]] is a repo-native exact paired object on
  `n=1..74`, with coordinate count `6`.
- Current banked wider continuation: the [[sym2-eight-window-object]] is a repo-native exact paired object on
  `n=1..73`, with coordinate count `27`.

## Active interpretation

- The old exact lane is [[exact-side-frozen-frontier|frozen]], not active.
- The strongest surviving object is now the Sym^3-lifted eleven-window invariant, not the width-only normalized Plücker objects or the earlier Sym^2 line.
- The attempted Sym^4 sixteen-window continuation is currently an engineering blocker, but the target-side cache path is now real:
  - the new rolling codimension-one rewrite makes the source side tractable:
    - `_build_sym4_sixteen_window_side("source")` now completes in about `6.443` seconds
  - the GMP-backed rolling rewrite improves the source side again:
    - `_build_sym4_sixteen_window_side("source")` now completes in about `2.990` seconds
  - the target side remains too expensive to bank as a full object:
    - quartic target-side initialization takes about `103.23` seconds
    - cached exact progress has now reached `9 / 65` windows
    - ordinary resumed advances are now about `84.06`, `93.39`, and `111.81` seconds
    - singular-pivot rebases are now about `140.81`, `154.61`, `188.13`, and `221.46` seconds
  - the cache path is now resilient against the first discovered singular rolling pivot:
    - after the second completed window the naive codimension-one shift becomes singular
    - a controlled rebase to the next window basis keeps the quartic target-side run alive
    - after the sixth completed window the cached lead was zero again, and the seventh completed window did confirm that next rebase case
    - after the eighth completed window the cached lead is zero again, so the observed alternating pattern still holds and the next quartic step is again expected to be a rebase case
    - after the ninth completed window the cached lead is nonzero again, so the observed alternating pattern still holds and the next quartic step is again expected to be an ordinary advance
  - live timing therefore narrows the quartic wall further:
    - the remaining blocker is not “cannot checkpoint”
    - it is the cost of target-side rolling advancement and occasional rebasing inside the exact sixteen-window normalized maximal-minor construction
  - so `Sym^4` is not yet promoted into the banked frontier
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
- The next defensible move is now split:
  - if staying on the higher-Schur line, continue the `Sym^4` target-side cached build and measure whether the persisted progress slope is good enough to justify banking the quartic object
  - otherwise stay mathematically anchored on the banked `Sym^3` object and try a genuinely different nonlocal family there
- Another cheap local, scalar, quotient, affine, or order-escalated constant-matrix family is still not justified on the banked frontier objects.

## Related pages

- [[exact-side-frozen-frontier]]
- [[sym3-eleven-window-object]]
- [[sym3-eleven-window-frontier]]
- [[sym3-eleven-window-matrix-recurrence-screen]]
- [[sym3-eleven-window-affine-matrix-screen]]
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
