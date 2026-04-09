---
title: Seven-Window Normalized Plucker Matrix Recurrence Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_seven_window_normalized_plucker_matrix_recurrence_screen.md
- raw/logs/bz_phase2_seven_window_normalized_plucker_decision_gate.md
last_updated: '2026-04-09'
---

Audit record for the first bounded nonlocal family tested on the [[seven-window-normalized-plucker-object]].

## Object and family

- Object: seven-window normalized `Gr(3,7)` Plücker sequence
- Family: constant matrix-valued recurrence ladder
- Orders tested: `1` and `2`
- Sides tested independently: source and target
- Shared exact object window: `n=1..74`

## Certified failure mode

This screen is certified by finite-field obstruction across the entire overdetermined low-order ladder:

- source side is inconsistent mod prime `1013` for recurrence orders `1` and `2`
- target side is inconsistent mod prime `1447` for recurrence orders `1` and `2`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order constant matrix family is exhausted through order `2` on this object.

## Boundary

Order `3` is the first underdetermined case:

- order `2` has `2312` unknowns against `2448` equations
- order `3` would have `3468` unknowns against `2414` equations

So any further increase in order would stop being an overdetermined obstruction screen and start becoming an interpolation-style search.

## Interpretation

This closes the first nonlocal matrix ladder on the seven-window object immediately. That is a negative result, but it is also a useful calibration: the new object is real and exact, but it will only earn its keep if the next family is structurally richer than a constant-coefficient matrix recurrence.

## Next move

If the program stays on this object, the next family should be a genuinely different nonlocal family rather than a higher order constant matrix ladder. Otherwise the next move is another nonlinear invariant pivot beyond the current normalized Plücker family.
