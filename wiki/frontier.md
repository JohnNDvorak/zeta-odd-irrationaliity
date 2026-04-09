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
- raw/logs/bz_phase2_six_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_six_window_normalized_plucker_annihilator_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_global_recurrence_screen.md
last_updated: '2026-04-09'
---

Current live frontier: frozen exact-side obstruction through degree 106, plus the six-window normalized Plücker nonlinear frontier with three recurrence-level family classes now explicitly screened.

## Current live frontier

- Exact-side frozen frontier: dual companion caches banked through `n=434`, with the exact cleared-window
  `(1,0,-1,-2)` recurrence family ruled out through degree `106` on window `n<=431`.
- Current nonlinear frontier: the [[six-window-normalized-plucker-object]] is now a repo-native exact paired object on
  `n=1..75`, with coordinate count `19`.

## Active interpretation

- The old exact lane is [[exact-side-frozen-frontier|frozen]], not active.
- The strongest live object is the six-window normalized Plücker invariant, not any quotient of it.
- The cheap six-window families are now certified: constant map fails first at `20`, difference map fails first at
  `21`, and the canonical free-zero support-1 family is inconsistent on its fit block.
- Short local-annihilator families on the same object are also now closed: relation lengths `4`, `5`, and `6` are
  all inconsistent at the first source and target window.
- Low-order global shared-scalar vector recurrences are also closed: orders `2` through `10` are inconsistent on both
  source and target six-window sequences.
- The next defensible move is now either a matrix-valued or otherwise richer nonlocal family on the same object, or a
  genuinely new nonlinear invariant family beyond Plücker. Another cheap local or scalar recurrence family is not justified.

## Related pages

- [[exact-side-frozen-frontier]]
- [[six-window-normalized-plucker-object]]
- [[six-window-normalized-plucker-hard-wall]]
- [[six-window-normalized-plucker-annihilator-screen]]
- [[six-window-normalized-plucker-global-recurrence-screen]]
- [[exhausted-ansatz-classes]]
- [[completed-directions]]
