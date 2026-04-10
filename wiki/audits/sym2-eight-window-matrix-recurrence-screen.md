---
title: Sym2 Eight-Window Matrix Recurrence Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym2_eight_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym2_eight_window_decision_gate.md
last_updated: '2026-04-09'
---

Audit record for the homogeneous matrix family on the [[sym2-eight-window-object]].

## Object and family

- Object: `Sym^2`-lifted eight-window normalized maximal-minor sequence
- Family: homogeneous constant matrix-valued recurrence ladder
- Orders tested: `1..2`
- Sides tested independently: source and target
- Shared exact object window: `n=1..73`

## Certified failure mode

This screen is certified by finite-field obstruction across the full overdetermined homogeneous ladder:

- source side is inconsistent mod prime `1009` for recurrence orders `1` and `2`
- target side is inconsistent mod prime `1447` for recurrence orders `1` and `2`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order homogeneous matrix family is exhausted through order `2` on this lifted object.

## Boundary

Order `3` is the first underdetermined case:

- homogeneous order `2` has `1458` unknowns against `1917` equations
- homogeneous order `3` would have `2187` unknowns against `1890` equations

So any further increase in order would stop being an overdetermined obstruction screen and start becoming an interpolation-style search.

## Interpretation

This matters because it shows that widening the `Sym^2` lift does not reopen a useful homogeneous matrix family. The object changes, but the first genuinely nontrivial overdetermined ladder still closes cleanly.
