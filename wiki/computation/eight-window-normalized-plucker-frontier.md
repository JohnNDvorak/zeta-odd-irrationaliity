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

Banked predecessor frontier: the full eight-window normalized Plücker object remains an exact paired invariant, but the live frontier has now moved to the [[sym2-seven-window-object]].

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

This was the last live normalized Plücker frontier before the program moved beyond that family. Its role now is to certify that width-only escalation had reached the point where the constant-matrix obstruction screen collapsed after a single order.
