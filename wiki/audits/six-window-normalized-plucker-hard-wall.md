---
title: Six-Window Normalized Plucker Hard Wall
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_six_window_normalized_plucker_object_spec.md
- raw/logs/bz_phase2_six_window_normalized_plucker_probe.md
- raw/logs/bz_phase2_six_window_normalized_plucker_family_probe.md
- raw/logs/bz_phase2_six_window_normalized_plucker_decision_gate.md
last_updated: '2026-04-09'
---

Audit record for the first recurrence-level family tested on the [[six-window-normalized-plucker-object]].

## Object and window

- Object: normalized `Gr(3,6)` Plücker invariant built from six consecutive packet vectors
- Source packet: symmetric-dual full packet `(constant, zeta(3), zeta(5))`
- Target packet: baseline-dual full packet `(constant, zeta(3), zeta(5))`
- Shared exact window: `n=1..75`
- Coordinate count: `19`

## Family class

Three bounded families were tested on the same exact object:

- `constant_six_plucker_map`
- `difference_six_plucker_map`
- `support1_free_zero_six_plucker_map`

The third family is the new part of this tranche: it is not just a support-depth escalation, but a canonical
fit-block resolution that uses exact RREF and sets free variables to zero.

## Certified failure mode

- `constant_six_plucker_map`: `fails_after_fit_window`, first mismatch `20`
- `difference_six_plucker_map`: `fails_after_fit_window`, first mismatch `21`
- `support1_free_zero_six_plucker_map`: `inconsistent_fit_block`, feature rank `31`, nullity `7`

The decision gate outcome is `hard_wall_six_window_plucker_support1_inconsistent`.

## Interpretation

This is a hard wall on the family, not on the object.

- The six-window normalized Plücker object remains the strongest live nonlinear object.
- The object is now established exactly and reproducibly.
- The failed lane is specifically the cheap constant/difference family plus the canonical free-zero support-1 family.

## Next move

Stay on the same object class, but choose a genuinely different recurrence-level family. Do not spend more time on:

- quotient continuations
- support-depth escalation on the old ladder
- rerunning the same free-zero support-1 family
