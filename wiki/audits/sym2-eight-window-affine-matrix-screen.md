---
title: Sym2 Eight-Window Affine Matrix Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym2_eight_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_eight_window_affine_decision_gate.md
last_updated: '2026-04-09'
---

Audit record for the affine matrix family on the [[sym2-eight-window-object]].

## Object and family

- Object: `Sym^2`-lifted eight-window normalized maximal-minor sequence
- Family: affine matrix-valued recurrence ladder
- Orders tested: `1..2`
- Sides tested independently: source and target
- Shared exact object window: `n=1..73`

## Certified failure mode

This screen is certified by finite-field obstruction across the full overdetermined affine ladder:

- source side is inconsistent mod prime `1009` for recurrence orders `1` and `2`
- target side is inconsistent mod prime `1447` for recurrence orders `1` and `2`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order affine matrix family is exhausted through order `2` on this lifted object.

## Boundary

Order `3` is the first underdetermined case:

- affine order `2` has `1485` unknowns against `1917` equations
- affine order `3` would have `2214` unknowns against `1890` equations

So any further increase in order would stop being an overdetermined obstruction screen and start becoming an interpolation-style search.

## Interpretation

This matters because it closes the first affine extension on the widened `Sym^2` object as well. The widened lift does not rescue the affine family any more than it rescues the homogeneous one.
