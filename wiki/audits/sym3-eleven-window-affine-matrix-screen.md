---
title: Sym3 Eleven-Window Affine Matrix Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym3_eleven_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym3_eleven_window_affine_decision_gate.md
last_updated: '2026-04-09'
---

Audit record for the affine matrix family on the [[sym3-eleven-window-object]].

## Object and family

- Object: `Sym^3`-lifted eleven-window normalized maximal-minor sequence
- Family: affine matrix-valued recurrence ladder
- Orders tested: `1..6`
- Sides tested independently: source and target
- Shared exact object window: `n=1..70`

## Certified failure mode

This screen is certified by finite-field obstruction across the full overdetermined affine ladder:

- source side is inconsistent mod prime `1009` for recurrence orders `1..6`
- target side is inconsistent mod prime `1447` for recurrence orders `1..6`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order affine matrix family is exhausted through order `6` on this lifted object.

## Boundary

Order `7` is the first underdetermined case:

- affine order `6` has `610` unknowns against `640` equations
- affine order `7` would have `710` unknowns against `630` equations

So any further increase in order would stop being an overdetermined obstruction screen and start becoming an interpolation-style search.

## Interpretation

This matters because it shows the cubic lift does not rescue the affine family any more than it rescues the homogeneous one. The higher-Schur continuation is now banked through both natural low-order nonlocal ladders.
