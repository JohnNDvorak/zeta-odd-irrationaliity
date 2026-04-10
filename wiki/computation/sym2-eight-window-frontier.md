---
title: Sym2 Eight-Window Frontier
category: computation
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym2_eight_window_object_spec.md
- raw/logs/bz_phase2_sym2_eight_window_probe.md
- raw/logs/bz_phase2_sym2_eight_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_eight_window_decision_gate.md
- raw/logs/bz_phase2_sym2_eight_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_eight_window_affine_decision_gate.md
last_updated: '2026-04-09'
---

Banked wider-window `Sym^2` continuation: the exact lifted object exists, but both natural low-order matrix ladders are now certified hard walls through the last overdetermined order.

## Screen summary

- The `Sym^2`-lifted eight-window object is established exactly on `n=1..73`.
- It has coordinate count `27`.
- On the homogeneous matrix ladder:
  - source orders `1..2` are inconsistent mod `1009`
  - target orders `1..2` are inconsistent mod `1447`
- On the affine matrix ladder:
  - source orders `1..2` are inconsistent mod `1009`
  - target orders `1..2` are inconsistent mod `1447`
- Order `3` is the first underdetermined case on the lifted object:
  - homogeneous order `2` has `1458` unknowns against `1917` equations
  - affine order `2` has `1485` unknowns against `1917` equations
  - order `3` passes into interpolation territory for both families

## Reading

This object is important because it shows that widening the `Sym^2` family once does not unlock a predictive recurrence-level family. The next move should not be more order escalation on this object; it should be a different higher Schur or nonlinear invariant family.
