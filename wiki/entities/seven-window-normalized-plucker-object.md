---
title: Seven-Window Normalized Plucker Object
category: entity
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_seven_window_normalized_plucker_object_spec.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_probe.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_matrix_recurrence_screen.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_affine_matrix_decision_gate.md
last_updated: '2026-04-09'
---

Banked predecessor frontier object, built from seven-term packet windows in normalized Plücker coordinates.

## Status

This is no longer the live frontier object; it is now the immediate predecessor to the [[eight-window-normalized-plucker-object]].

- It widens the normalized Grassmannian packet geometry from `Gr(3,6)` to `Gr(3,7)`.
- It is established exactly as a paired invariant on `n=1..74` with coordinate count `34`.
- The first homogeneous nonlocal family tested on it already closes cleanly:
  - source side has modular inconsistency witness `1013` for constant matrix recurrence orders `1` and `2`
  - target side has modular inconsistency witness `1447` for constant matrix recurrence orders `1` and `2`
  - order `3` is the first underdetermined case on this object
- The first affine-chart extension also closes cleanly:
  - source side has modular inconsistency witness `1013` for affine matrix recurrence orders `1` and `2`
  - target side has modular inconsistency witness `1447` for affine matrix recurrence orders `1` and `2`
  - order `3` is again the first underdetermined case
- So both the homogeneous and affine low-order constant-matrix ladders are exhausted on this object.

## Reading

The seven-window object was a genuine frontier upgrade over the six-window one, but it has now been superseded by the eight-window continuation. It remains important because it banked both the homogeneous and affine low-order matrix hard walls in a fully exact setting.

See [[seven-window-normalized-plucker-matrix-recurrence-screen]], [[seven-window-normalized-plucker-affine-matrix-screen]], [[eight-window-normalized-plucker-object]], and [[six-window-normalized-plucker-object]].
