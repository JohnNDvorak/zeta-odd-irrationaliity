---
title: Sym3 Eleven-Window Frontier
category: computation
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym3_eleven_window_object_spec.md
- raw/logs/bz_phase2_sym3_eleven_window_probe.md
- raw/logs/bz_phase2_sym3_eleven_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym3_eleven_window_decision_gate.md
- raw/logs/bz_phase2_sym3_eleven_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym3_eleven_window_affine_decision_gate.md
- raw/logs/bz_phase2_sym4_sixteen_window_engineering_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_gmp_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_probe.md
last_updated: '2026-04-15'
---

Predecessor higher-Schur frontier: the `Sym^3`-lifted eleven-window object remains a banked exact paired invariant, and both its homogeneous and affine low-order matrix ladders are certified hard walls through the last overdetermined order. The strongest banked object has now moved to [[sym4-sixteen-window-object]].

## Screen summary

- The `Sym^3`-lifted eleven-window object is established exactly on `n=1..70`.
- It has coordinate count `10`.
- On the homogeneous matrix ladder:
  - source orders `1..6` are inconsistent mod `1009`
  - target orders `1..6` are inconsistent mod `1447`
- On the affine matrix ladder:
  - source orders `1..6` are inconsistent mod `1009`
  - target orders `1..6` are inconsistent mod `1447`
- Order `7` is the first underdetermined case on the lifted object:
  - homogeneous order `6` has `600` unknowns against `640` equations
  - affine order `6` has `610` unknowns against `640` equations
  - order `7` passes into interpolation territory for both families

## Reading

This remains important because it is the first higher-Schur object beyond the `Sym^2` line with both homogeneous and affine hard-wall certificates in the repo. The quartic continuation has now crossed the target-cache wall and banked [[sym4-sixteen-window-object]], but its recurrence-level screens are still pending. The strongest hard-wall conclusion therefore remains cubic until those Sym4 screens are run.
