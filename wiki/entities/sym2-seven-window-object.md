---
title: Sym2 Seven-Window Object
category: entity
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym2_seven_window_object_spec.md
- raw/logs/bz_phase2_sym2_seven_window_probe.md
- raw/logs/bz_phase2_sym2_seven_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_seven_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_seven_window_affine_decision_gate.md
last_updated: '2026-04-09'
---

Current strongest deep-ladder beyond-Plucker transfer object, built by lifting each packet vector through `Sym^2` and then taking a seven-window normalized maximal-minor invariant in dimension `6`.

## Status

This is no longer the live frontier object; it is now the immediate predecessor to the [[sym3-eleven-window-object]], after the wider [[sym2-eight-window-object]] continuation was also banked.

- It changes the invariant family itself rather than only widening the original normalized Plücker window.
- It is established exactly as a paired lifted invariant on `n=1..74` with coordinate count `6`.
- The homogeneous constant-matrix ladder closes completely:
  - source orders `1..10` are inconsistent mod `1009`
  - target orders `1..10` are inconsistent mod `1447`
  - order `11` is the first underdetermined case
- The affine matrix ladder also closes completely:
  - source orders `1..10` are inconsistent mod `1009`
  - target orders `1..10` are inconsistent mod `1447`
  - order `11` is again the first underdetermined case

## Reading

This object remains one of the most important predecessor frontiers because it was the first serious beyond-Plücker invariant family that was both exact and structurally justified, and it still carries a deeper obstruction ladder than the wider [[sym2-eight-window-object]]. But it is no longer the live frontier: the higher-Schur [[sym3-eleven-window-object]] has now been banked above it.

See [[sym2-seven-window-matrix-recurrence-screen]], [[sym2-seven-window-affine-matrix-screen]], [[sym2-seven-window-frontier]], [[sym3-eleven-window-object]], [[sym2-eight-window-object]], and [[eight-window-normalized-plucker-object]].
