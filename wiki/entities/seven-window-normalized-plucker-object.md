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
last_updated: '2026-04-09'
---

Current strongest surviving nonlinear transfer object, built from seven-term packet windows in normalized Plücker coordinates.

## Status

This is now the active frontier object, superseding the [[six-window-normalized-plucker-object]].

- It widens the normalized Grassmannian packet geometry from `Gr(3,6)` to `Gr(3,7)`.
- It is established exactly as a paired invariant on `n=1..74` with coordinate count `34`.
- The first nonlocal family tested on it already closes cleanly:
  - source side has modular inconsistency witness `1013` for constant matrix recurrence orders `1` and `2`
  - target side has modular inconsistency witness `1447` for constant matrix recurrence orders `1` and `2`
  - order `3` is the first underdetermined case on this object
- So the first low-order constant matrix ladder is exhausted immediately, but in an obstruction-grade way rather than by interpolation.

## Reading

The seven-window object is a genuine frontier upgrade because it keeps the full normalized invariant and increases the window size again. But the first bounded matrix ladder already closes, so the next continuation on this object has to be a genuinely different nonlocal family, not just order escalation of the same constant matrix ansatz.

See [[seven-window-normalized-plucker-matrix-recurrence-screen]], [[seven-window-normalized-plucker-frontier]], and [[six-window-normalized-plucker-object]].
