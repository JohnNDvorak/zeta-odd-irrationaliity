---
title: Eight-Window Normalized Plucker Matrix Recurrence Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_decision_gate.md
last_updated: '2026-04-09'
---

Audit record for the first bounded nonlocal family tested on the [[eight-window-normalized-plucker-object]].

## Object and family

- Object: eight-window normalized `Gr(3,8)` Plücker sequence
- Family: last overdetermined constant matrix-valued recurrence
- Orders tested: `1` only
- Sides tested independently: source and target
- Shared exact object window: `n=1..73`

## Certified failure mode

This screen is certified by finite-field obstruction on the full overdetermined matrix family:

- source side is inconsistent mod prime `1013`
- target side is inconsistent mod prime `1447`

Since inconsistency mod `p` implies inconsistency over `Q`, the last overdetermined constant matrix family is exhausted on this object.

## Boundary

Order `2` is already underdetermined:

- order `1` has `3025` unknowns against `3960` equations
- order `2` would have `6050` unknowns against `3905` equations

So there is no order-`2` obstruction ladder on this object; escalating order from here would be interpolation-style search immediately.

## Interpretation

This is a sharper wall than the seven-window one: widening the normalized Plücker object again still did not rescue the cheap constant-matrix family, and on this object the overdetermined ladder collapses after a single order.

## Next move

If the program stays on this object, the next family must be genuinely different and nonlocal. Otherwise the next move is to leave the current normalized Plücker family altogether.
