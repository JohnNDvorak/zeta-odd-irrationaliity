---
title: Eight-Window Normalized Plucker Object
category: entity
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_eight_window_normalized_plucker_object_spec.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_probe.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_matrix_recurrence_screen.md
- raw/logs/bz_phase2_eight_window_normalized_plucker_decision_gate.md
last_updated: '2026-04-09'
---

Banked predecessor frontier object, built from eight-term packet windows in normalized Plücker coordinates.

## Status

This is no longer the live frontier object; it is now the immediate predecessor to the [[sym2-seven-window-object]].

- It widens the normalized Grassmannian packet geometry from `Gr(3,7)` to `Gr(3,8)`.
- It is established exactly as a paired invariant on `n=1..73` with coordinate count `55`.
- The last overdetermined constant-matrix family on it already closes cleanly:
  - source side order-`1` constant matrix recurrence is inconsistent mod `1013`
  - target side order-`1` constant matrix recurrence is inconsistent mod `1447`
  - order `2` is already underdetermined on this object
- That means normalized Plücker width alone is still improving the object class, but not yet unlocking a predictive low-order matrix family.

## Reading

The eight-window object was the last width-only normalized Plücker frontier before the program moved beyond that family. It remains important because it shows that simply widening the original normalized Plücker object no longer buys a useful matrix obstruction ladder.

See [[eight-window-normalized-plucker-matrix-recurrence-screen]], [[eight-window-normalized-plucker-frontier]], [[sym2-seven-window-object]], and [[seven-window-normalized-plucker-object]].
