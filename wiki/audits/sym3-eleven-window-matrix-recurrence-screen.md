---
title: Sym3 Eleven-Window Matrix Recurrence Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym3_eleven_window_matrix_recurrence_screen.md
- raw/logs/bz_phase2_sym3_eleven_window_decision_gate.md
last_updated: '2026-04-09'
---

Audit record for the homogeneous matrix family on the [[sym3-eleven-window-object]].

## Object and family

- Object: `Sym^3`-lifted eleven-window normalized maximal-minor sequence
- Family: homogeneous constant matrix-valued recurrence ladder
- Orders tested: `1..6`
- Sides tested independently: source and target
- Shared exact object window: `n=1..70`

## Certified failure mode

This screen is certified by finite-field obstruction across the full overdetermined homogeneous ladder:

- source side is inconsistent mod prime `1009` for recurrence orders `1..6`
- target side is inconsistent mod prime `1447` for recurrence orders `1..6`

Since inconsistency mod `p` implies inconsistency over `Q`, the low-order homogeneous matrix family is exhausted through order `6` on this lifted object.

## Boundary

Order `7` is the first underdetermined case:

- homogeneous order `6` has `600` unknowns against `640` equations
- homogeneous order `7` would have `700` unknowns against `630` equations

So any further increase in order would stop being an overdetermined obstruction screen and start becoming an interpolation-style search.

## Interpretation

This matters because it shows the higher-Schur continuation is structurally real, not just a speculative next object. The cubic lift supports a full overdetermined ladder and then closes it cleanly.
