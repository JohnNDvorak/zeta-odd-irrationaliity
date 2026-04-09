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

Current strongest surviving nonlinear transfer object, built from eight-term packet windows in normalized Plücker coordinates.

## Status

This is now the active frontier object, superseding the [[seven-window-normalized-plucker-object]].

- It widens the normalized Grassmannian packet geometry from `Gr(3,7)` to `Gr(3,8)`.
- It is established exactly as a paired invariant on `n=1..73` with coordinate count `55`.
- The last overdetermined constant-matrix family on it already closes cleanly:
  - source side order-`1` constant matrix recurrence is inconsistent mod `1013`
  - target side order-`1` constant matrix recurrence is inconsistent mod `1447`
  - order `2` is already underdetermined on this object
- That means normalized Plücker width alone is still improving the object class, but not yet unlocking a predictive low-order matrix family.

## Reading

The eight-window object is the cleanest current frontier because it preserves exactness while pushing the nonlinear invariant width again. But the cheap matrix family is already exhausted at the first overdetermined order, so the next continuation on this object must be a genuinely different nonlocal family, not a higher-order constant matrix ladder.

See [[eight-window-normalized-plucker-matrix-recurrence-screen]], [[eight-window-normalized-plucker-frontier]], and [[seven-window-normalized-plucker-object]].
