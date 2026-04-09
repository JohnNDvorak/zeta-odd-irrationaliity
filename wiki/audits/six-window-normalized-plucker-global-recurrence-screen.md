---
title: Six-Window Normalized Plucker Global Recurrence Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_six_window_normalized_plucker_global_recurrence_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_probe.md
last_updated: '2026-04-09'
---

Audit record for low-order global shared-scalar vector recurrences tested on the [[six-window-normalized-plucker-object]].

## Object and family

- Object: six-window normalized `Gr(3,6)` Plücker sequence
- Family: one global scalar recurrence relation shared across all `19` coordinates of the vector sequence
- Sides tested independently: source and target
- Shared exact object window: `n=1..75`

## Orders screened

Orders `2` through `10` were tested exactly on both source and target.

## Certified failure mode

Every tested order is inconsistent:

- source: orders `2,3,4,5,6,7,8,9,10`
- target: orders `2,3,4,5,6,7,8,9,10`

So the outcome is `low_order_global_vector_recurrence_exhausted_through_order_10`.

## Interpretation

This closes the most natural nonlocal scalar recurrence family on the current six-window object. The remaining live
families on this object, if any, need to be richer than:

- local transfer ladders
- short local annihilator relations
- global shared-scalar recurrences

## Next move

Do not keep increasing scalar recurrence order mechanically. The next plausible internal family would have to be
structurally richer, for example matrix-valued or otherwise non-scalar.
