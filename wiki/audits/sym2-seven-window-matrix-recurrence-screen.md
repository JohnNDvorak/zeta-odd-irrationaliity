---
title: Sym2 Seven-Window Matrix Recurrence Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym2_seven_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_seven_window_decision_gate.md
last_updated: '2026-04-09'
---

Audit record for the homogeneous matrix family on the [[sym2-seven-window-object]].

## Object and family

- Object: `Sym^2`-lifted seven-window normalized maximal-minor sequence
- Family: constant matrix-valued recurrence ladder
- Orders tested: `1..10`
- Sides tested independently: source and target
- Shared exact object window: `n=1..74`

## Certified failure mode

This screen is certified by finite-field obstruction across the full overdetermined ladder:

- source side is inconsistent mod prime `1009` for recurrence orders `1..10`
- target side is inconsistent mod prime `1447` for recurrence orders `1..10`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order constant matrix family is exhausted through order `10` on this lifted object.

## Boundary

Order `11` is the first underdetermined case:

- order `10` has `360` unknowns against `384` equations
- order `11` would have `396` unknowns against `378` equations

So any further increase in order would stop being an overdetermined obstruction screen and start becoming an interpolation-style search.

## Interpretation

This is the strongest homogeneous matrix obstruction we have banked on any beyond-Plücker object so far.
