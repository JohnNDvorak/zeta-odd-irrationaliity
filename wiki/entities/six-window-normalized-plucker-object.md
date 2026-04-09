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

## Next move

Try a different recurrence-level family on this object, not another quotient or support-depth escalation. See
[[six-window-normalized-plucker-hard-wall]].
