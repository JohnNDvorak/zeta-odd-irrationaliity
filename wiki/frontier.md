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
- raw/logs/bz_phase2_seven_window_normalized_plucker_affine_matrix_decision_gate.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_probe.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_six_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_six_window_normalized_plucker_annihilator_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_global_recurrence_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_matrix_recurrence_screen.md
last_updated: '2026-04-09'
---

Current live frontier: frozen exact-side obstruction through degree 106, plus the eight-window normalized Plücker nonlinear frontier, with the last overdetermined constant-matrix screen already closed at order 1.

## Current live frontier

- Exact-side frozen frontier: dual companion caches banked through `n=434`, with the exact cleared-window
  `(1,0,-1,-2)` recurrence family ruled out through degree `106` on window `n<=431`.
- Current nonlinear frontier: the [[eight-window-normalized-plucker-object]] is now a repo-native exact paired object on
  `n=1..73`, with coordinate count `55`.

## Active interpretation

- The old exact lane is [[exact-side-frozen-frontier|frozen]], not active.
- The strongest live object is now the eight-window normalized Plücker invariant, not the seven-window object and not any quotient of any normalized Plücker variant.
- The eight-window object already closes its last overdetermined constant-matrix family:
  - source-side order `1` is inconsistent mod `1013`
  - target-side order `1` is inconsistent mod `1447`
  - order `2` is already underdetermined, so the cheap constant-matrix ladder is over as an obstruction screen on this object
- The seven-window object remains valuable as the immediate predecessor frontier, and it already closed:
  - low-order homogeneous constant-matrix recurrence through order `2`
  - low-order affine constant-matrix recurrence through order `2`
- The six-window object remains valuable as the earlier predecessor frontier, and it already closed:
  - bounded transfer-ladder families
  - short local-annihilator families
  - low-order global shared-scalar vector recurrences
  - low-order constant matrix recurrence through order `3`
- The next defensible move is now either a genuinely different nonlocal family on the eight-window object, or another nonlinear invariant family beyond the current normalized Plücker layer. Another cheap local, scalar, quotient, affine, or order-escalated constant-matrix family is not justified.

## Related pages

- [[exact-side-frozen-frontier]]
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
