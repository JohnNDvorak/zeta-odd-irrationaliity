---
title: Sym2 Eight-Window Object
category: entity
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym2_eight_window_object_spec.md
- raw/logs/bz_phase2_sym2_eight_window_probe.md
- raw/logs/bz_phase2_sym2_eight_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_eight_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_eight_window_affine_decision_gate.md
last_updated: '2026-04-09'
---

Banked wider continuation of the [[sym2-seven-window-object]], built by keeping the same `Sym^2` lift but widening the normalized maximal-minor window from `7` to `8`.

## Status

This is not the strongest deep-ladder object in the current program, but it is the cleanest wider-window continuation of the `Sym^2` family.

- It is established exactly as a paired lifted invariant on `n=1..73` with coordinate count `27`.
- The homogeneous constant-matrix ladder closes through the full overdetermined range:
  - source orders `1..2` are inconsistent mod `1009`
  - target orders `1..2` are inconsistent mod `1447`
  - order `3` is the first underdetermined case
- The affine matrix ladder also closes through the full overdetermined range:
  - source orders `1..2` are inconsistent mod `1009`
  - target orders `1..2` are inconsistent mod `1447`
  - order `3` is again the first underdetermined case

## Reading

This object matters because it tests whether widening the lifted `Sym^2` geometry itself buys a useful new matrix ladder. The answer is no: the object is real and exact, but both natural low-order matrix families are exhausted immediately after the last overdetermined order.

See [[sym2-eight-window-matrix-recurrence-screen]], [[sym2-eight-window-affine-matrix-screen]], [[sym2-eight-window-frontier]], and [[sym2-seven-window-object]].
