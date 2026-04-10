---
title: Sym3 Eleven-Window Object
category: entity
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym3_eleven_window_object_spec.md
- raw/logs/bz_phase2_sym3_eleven_window_probe.md
- raw/logs/bz_phase2_sym3_eleven_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym3_eleven_window_affine_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym3_eleven_window_affine_decision_gate.md
last_updated: '2026-04-09'
---

Current strongest higher-Schur frontier object, built by lifting each packet vector through `Sym^3` and then taking an eleven-window normalized maximal-minor invariant in dimension `10`.

## Status

This is now the live beyond-Plücker frontier object, superseding the [[sym2-seven-window-object]].

- It changes the invariant family itself again, from the quadratic `Sym^2` lift to a cubic `Sym^3` lift.
- It is established exactly as a paired lifted invariant on `n=1..70` with coordinate count `10`.
- The homogeneous constant-matrix ladder closes completely:
  - source orders `1..6` are inconsistent mod `1009`
  - target orders `1..6` are inconsistent mod `1447`
  - order `7` is the first underdetermined case
- The affine matrix ladder also closes completely:
  - source orders `1..6` are inconsistent mod `1009`
  - target orders `1..6` are inconsistent mod `1447`
  - order `7` is again the first underdetermined case

## Reading

This object matters because it confirms that the higher-Schur continuation is real, exact, and bankable. The cubic lift did not break the program into interpolation immediately; it supported a full overdetermined matrix ladder through order `6` before underdetermination began at order `7`.

See [[sym3-eleven-window-matrix-recurrence-screen]], [[sym3-eleven-window-affine-matrix-screen]], [[sym3-eleven-window-frontier]], and [[sym2-seven-window-object]].
