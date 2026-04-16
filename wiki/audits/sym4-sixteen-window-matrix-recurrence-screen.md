---
title: Sym4 Sixteen-Window Matrix Recurrence Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_matrix_recurrence_screen.md
last_updated: '2026-04-15'
---

Audit record for the homogeneous matrix family on the [[sym4-sixteen-window-object]].

## Object and family

- Object: `Sym^4`-lifted sixteen-window normalized maximal-minor sequence
- Family: homogeneous constant matrix-valued recurrence ladder
- Orders tested: `1..4`
- Matrix size: `15`
- Sides tested independently: source and target
- Shared exact object window: `n=1..65`

## Certified failure mode

This screen is certified by finite-field obstruction across the full overdetermined homogeneous ladder:

- source side is inconsistent mod prime `1009` for recurrence orders `1..4`
- target side is inconsistent mod prime `1451` for recurrence orders `1..4`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order homogeneous matrix family is exhausted through order `4` on this lifted object.

## Boundary

Order `5` is the first underdetermined case:

- homogeneous order `4` has `900` unknowns against `915` equations
- homogeneous order `5` would have `1125` unknowns against `900` equations

So further order escalation would stop being an overdetermined obstruction screen and would become interpolation territory.

## Interpretation

This closes the first recurrence-level follow-up on the banked quartic object. It does not produce a transfer recurrence, identify a baseline `P_n`, or reopen the frozen exact `n=435` lane; it narrows the quartic continuation to the affine matrix screen or to a genuinely different recurrence family.
