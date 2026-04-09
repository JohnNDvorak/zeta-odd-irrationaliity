---
title: Seven-Window Normalized Plucker Affine Matrix Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_seven_window_normalized_plucker_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_affine_matrix_decision_gate.md
last_updated: '2026-04-09'
---

Audit record for the affine-chart matrix family tested on the [[seven-window-normalized-plucker-object]].

## Object and family

- Object: seven-window normalized `Gr(3,7)` Plücker sequence
- Family: affine matrix-valued recurrence ladder
- Orders tested: `1` and `2`
- Sides tested independently: source and target
- Shared exact object window: `n=1..74`

## Certified failure mode

This screen is certified by finite-field obstruction across the full overdetermined affine ladder:

- source side is inconsistent mod prime `1013` for recurrence orders `1` and `2`
- target side is inconsistent mod prime `1447` for recurrence orders `1` and `2`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order affine matrix family is exhausted through order `2` on this object.

## Boundary

Order `3` is the first underdetermined case:

- order `2` has `2346` unknowns against `2448` equations
- order `3` would have `3502` unknowns against `2414` equations

So any further increase in order would stop being an overdetermined obstruction screen and start becoming an interpolation-style search.

## Interpretation

This matters because it closes the first structurally justified affine-chart continuation on the seven-window object. The object was not just hostile to homogeneous matrix recurrences; it is also hostile to the first affine extension that naturally respects the chart normalization.

## Next move

Treat the seven-window object as a banked predecessor frontier. If the program returns to it, the next family must be richer than both the homogeneous and affine constant-matrix ladders. Otherwise the program should continue by changing the nonlinear object again.
