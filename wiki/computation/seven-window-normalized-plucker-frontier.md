---
title: Seven-Window Normalized Plucker Frontier
category: computation
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_seven_window_normalized_plucker_object_spec.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_probe.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_matrix_recurrence_screen.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_decision_gate.md
last_updated: '2026-04-09'
---

Current nonlinear frontier: the full seven-window normalized Plücker object is now a repo-native exact paired invariant, and its first overdetermined constant-matrix family is already certified as a hard wall.

## Screen summary

- The seven-window normalized Plücker object is established exactly on `n=1..74`.
- It has coordinate count `34`.
- On the first nonlocal family:
  - source side order-`1` constant matrix recurrence is inconsistent mod `1013`
  - target side order-`1` constant matrix recurrence is inconsistent mod `1447`
  - source side order-`2` constant matrix recurrence is inconsistent mod `1013`
  - target side order-`2` constant matrix recurrence is inconsistent mod `1447`
- Order `3` is the first underdetermined case on the seven-window object:
  - order `2` has `2312` unknowns against `2448` equations
  - order `3` would have `3468` unknowns against `2414` equations

## Reading

This improves the object class while preserving exactness, but it does not yet improve the family picture: the low-order constant matrix ladder dies immediately again. That means the seven-window object is live, but only for a genuinely different nonlocal family. The object should not be abandoned yet, and the matrix order should not be inflated mechanically.
