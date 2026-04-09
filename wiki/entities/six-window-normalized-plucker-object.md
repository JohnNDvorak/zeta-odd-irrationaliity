---
title: Six-Window Normalized Plucker Object
category: entity
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_six_window_plucker_followup_screen.md
- raw/logs/bz_phase2_normalized_plucker_window_invariant_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_probe.md
- raw/logs/bz_phase2_six_window_normalized_plucker_decision_gate.md
last_updated: '2026-04-09'
---

Current strongest surviving nonlinear transfer object, built from six-term packet windows in normalized Plücker coordinates.

## Status

This is the current best surviving object class.

- It improves the cheap frontier beyond the five-term normalized Plücker object.
- Its quotient continuation is weaker.
- It is now established exactly as a paired invariant on `n=1..75` with coordinate count `19`.
- Its first bounded recurrence-level family is not predictive:
  - same-index constant map fails first at `20`
  - first-difference map fails first at `21`
  - canonical free-zero support-1 map is inconsistent on the fit block
- Short local-annihilator families on the invariant itself are also exhausted:
  - relation lengths `4`, `5`, and `6` all fail immediately at the first source and target window
- Low-order global shared-scalar vector recurrences are also exhausted:
  - orders `2` through `10` are inconsistent on both source and target
- Low-order constant matrix recurrence is also exhausted:
  - source side has modular inconsistency witness `1013` for orders `1`, `2`, and `3`
  - target side has modular inconsistency witness `1447` for orders `1`, `2`, and `3`
  - order `4` is the first underdetermined case

## Next move

Try a different recurrence-level family on this object, not another quotient or support-depth escalation. See
[[six-window-normalized-plucker-hard-wall]], [[six-window-normalized-plucker-annihilator-screen]], and
[[six-window-normalized-plucker-global-recurrence-screen]], and [[six-window-normalized-plucker-matrix-recurrence-screen]].
