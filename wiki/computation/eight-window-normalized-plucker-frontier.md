---
title: Eight-Window Normalized Plucker Frontier
category: computation
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_eight_window_normalized_plucker_object_spec.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_probe.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_decision_gate.md
last_updated: '2026-04-09'
---

Current nonlinear frontier: the full eight-window normalized Plücker object is now a repo-native exact paired invariant, and its last overdetermined constant-matrix screen is already certified as a hard wall.

## Screen summary

- The eight-window normalized Plücker object is established exactly on `n=1..73`.
- It has coordinate count `55`.
- On the last overdetermined constant-matrix family:
  - source side order-`1` constant matrix recurrence is inconsistent mod `1013`
  - target side order-`1` constant matrix recurrence is inconsistent mod `1447`
- Order `2` is already underdetermined on the eight-window object:
  - order `1` has `3025` unknowns against `3960` equations
  - order `2` would have `6050` unknowns against `3905` equations

## Reading

This is now the live normalized Plücker frontier. The object class is stronger again, but the last overdetermined constant-matrix family still dies immediately. So the current decision pressure is no longer “wider object or not”; it is “what genuinely different nonlocal family belongs on the eight-window object, if any?”
