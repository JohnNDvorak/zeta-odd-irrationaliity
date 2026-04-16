---
title: Sym4 Matrix Ladders Exhausted
category: conclusion
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_ladder_decision_gate.md
last_updated: '2026-04-15'
---

Banked conclusion: the [[sym4-sixteen-window-object]] closes both natural low-order constant-matrix recurrence ladders through their overdetermined ranges.

## Closed ladders

- Homogeneous source-side orders `1..4` are inconsistent mod prime `1009`.
- Homogeneous target-side orders `1..4` are inconsistent mod prime `1451`.
- Affine source-side orders `1..3` are inconsistent mod prime `1009`.
- Affine target-side orders `1..3` are inconsistent mod prime `1451`.

## Boundary

- Homogeneous order `5` is underdetermined, with `1125` unknowns against `900` equations.
- Affine order `4` is not overdetermined, with `915` unknowns against `915` equations.

## Rule

Do not keep increasing homogeneous or affine matrix order mechanically on the quartic object. A continuation needs a genuinely different structural reason, not a larger fit family.
