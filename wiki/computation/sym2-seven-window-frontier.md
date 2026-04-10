---
title: Sym2 Seven-Window Frontier
category: computation
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym2_seven_window_object_spec.md
- raw/logs/bz_phase2_sym2_seven_window_probe.md
- raw/logs/bz_phase2_sym2_seven_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_seven_window_decision_gate.md
- raw/logs/bz_phase2_sym2_seven_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_seven_window_affine_decision_gate.md
last_updated: '2026-04-09'
---

Current strongest beyond-Plucker frontier: the `Sym^2`-lifted seven-window object is a repo-native exact paired invariant, and both its homogeneous and affine low-order matrix ladders are certified hard walls through the last overdetermined order.

## Screen summary

- The `Sym^2`-lifted seven-window object is established exactly on `n=1..74`.
- It has coordinate count `6`.
- On the homogeneous matrix ladder:
  - source orders `1..10` are inconsistent mod `1009`
  - target orders `1..10` are inconsistent mod `1447`
- On the affine matrix ladder:
  - source orders `1..10` are inconsistent mod `1009`
  - target orders `1..10` are inconsistent mod `1447`
- Order `11` is the first underdetermined case on the lifted object:
  - homogeneous order `10` has `360` unknowns against `384` equations
  - affine order `10` has `366` unknowns against `384` equations
  - order `11` passes into interpolation territory for both families

## Reading

This remains the strongest live lifted frontier because it goes beyond the original normalized Plücker family and still stays exact and reproducible. The strongest current conclusion is that the first two natural nonlocal ladders on this lifted object are both closed through the full overdetermined range, and the wider [[sym2-eight-window-object]] continuation also closes quickly. Any continuation here has to be structurally richer than both constant and affine matrix recurrence.
