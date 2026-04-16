---
title: Sym4 Sixteen-Window Affine Matrix Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_affine_matrix_recurrence_screen.md
last_updated: '2026-04-15'
---

Audit record for the affine matrix family on the [[sym4-sixteen-window-object]].

## Object and family

- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor sequence
- Family: affine matrix-valued recurrence ladder
- Orders tested: `1..3`
- Matrix size: `15`
- Sides tested independently: source and target
- Shared exact object window: `n=1..65`

## Certified failure mode

This screen is certified by finite-field obstruction across the full overdetermined affine ladder:

- source side is inconsistent mod prime `1009` for recurrence orders `1..3`
- target side is inconsistent mod prime `1451` for recurrence orders `1..3`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order affine matrix family is exhausted through order `3` on this lifted object.

## Boundary

Order `4` is the first non-overdetermined affine case:

- affine order `3` has `690` unknowns against `930` equations
- affine order `4` would have `915` unknowns against `915` equations

So further order escalation would stop being a strict overdetermined obstruction screen and would need a separate structural reason.

## Interpretation

Together with [[sym4-sixteen-window-matrix-recurrence-screen]], this banks both natural low-order matrix ladders on the quartic object as hard walls. It does not create a recurrence-level transfer, identify a baseline `P_n`, or reopen the frozen exact `n=435` lane.
