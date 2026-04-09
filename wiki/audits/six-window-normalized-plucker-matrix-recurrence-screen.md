---
title: Six-Window Normalized Plucker Matrix Recurrence Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_six_window_normalized_plucker_matrix_recurrence_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_probe.md
last_updated: '2026-04-09'
---

Audit record for the low-order constant matrix-valued family tested on the [[six-window-normalized-plucker-object]].

## Object and family

- Object: six-window normalized `Gr(3,6)` Plücker sequence
- Family: constant order-1 matrix recurrence `v_{n+1} = M v_n`
- Sides tested independently: source and target
- Shared exact object window: `n=1..75`

## Certified failure mode

This screen is certified by finite-field obstruction across the low-order ladder:

- source side is inconsistent mod prime `1013` for recurrence orders `1`, `2`, and `3`
- target side is inconsistent mod prime `1447` for recurrence orders `1`, `2`, and `3`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order constant matrix family is exhausted through
order `3` on this object.

## Boundary

Order `4` is the first underdetermined case:

- order `3` has `1083` unknowns against `1368` equations
- order `4` would have `1444` unknowns against `1349` equations

So any further increase in order would stop being an overdetermined obstruction screen and start becoming an
interpolation-style search.

## Interpretation

This closes the first low-order genuinely matrix-valued family on the six-window object. Combined with the earlier screens, the
following families are now banked as exhausted on the same object:

- bounded transfer-ladder families
- short local-annihilator families
- low-order global shared-scalar vector recurrences
- low-order constant matrix recurrence through order `3`

## Next move

If the program stays on this object, the next internal family must be richer than the low-order constant-coefficient
matrix ladder. Otherwise the next move is to change the nonlinear invariant family entirely.
