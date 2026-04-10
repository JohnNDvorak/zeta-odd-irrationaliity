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
- raw/logs/bz_phase2_six_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_six_window_normalized_plucker_annihilator_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_global_recurrence_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_matrix_recurrence_screen.md
last_updated: '2026-04-09'
---

Current live frontier: frozen exact-side obstruction through degree 106, plus the beyond-Plücker higher-Schur frontier, where the `Sym^3` eleven-window object is now banked as the strongest live nonlinear invariant.

## Current live frontier

- Exact-side frozen frontier: dual companion caches banked through `n=434`, with the exact cleared-window
  `(1,0,-1,-2)` recurrence family ruled out through degree `106` on window `n<=431`.
- Current strongest lifted object: the [[sym3-eleven-window-object]] is a repo-native exact paired object on
  `n=1..70`, with coordinate count `10`.
- Immediate predecessor lifted object: the [[sym2-seven-window-object]] is a repo-native exact paired object on
  `n=1..74`, with coordinate count `6`.
- Current banked wider continuation: the [[sym2-eight-window-object]] is a repo-native exact paired object on
  `n=1..73`, with coordinate count `27`.

## Active interpretation

- The old exact lane is [[exact-side-frozen-frontier|frozen]], not active.
- The strongest surviving object is now the Sym^3-lifted eleven-window invariant, not the width-only normalized Plücker objects or the earlier Sym^2 line.
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
- The next defensible move is now either a genuinely different nonlocal family on the Sym^2-lifted object, or another beyond-Plücker invariant family. Another cheap local, scalar, quotient, affine, or order-escalated constant-matrix family is not justified.
- The strongest recommendation after the cubic Schur screen is now either a genuinely different nonlocal family on the Sym^3 object or another higher nonlinear invariant family, not more order escalation on the current matrix ladders.

## Related pages

- [[exact-side-frozen-frontier]]
- [[sym3-eleven-window-object]]
- [[sym3-eleven-window-frontier]]
- [[sym3-eleven-window-matrix-recurrence-screen]]
- [[sym3-eleven-window-affine-matrix-screen]]
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
