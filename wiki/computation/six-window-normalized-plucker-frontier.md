---
title: Six-Window Normalized Plucker Frontier
category: computation
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_normalized_plucker_window_invariant_screen.md
- raw/logs/bz_phase2_plucker_quotient_family_screen.md
- raw/logs/bz_phase2_six_window_plucker_followup_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_probe.md
- raw/logs/bz_phase2_six_window_normalized_plucker_family_probe.md
- raw/logs/bz_phase2_six_window_normalized_plucker_decision_gate.md
- raw/logs/bz_phase2_six_window_normalized_plucker_annihilator_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_global_recurrence_screen.md
last_updated: '2026-04-09'
---

Current nonlinear frontier: the full six-window normalized Plücker object is now a repo-native exact paired invariant, and three different recurrence-level family classes have been certified as hard walls.

## Screen summary

- Five-term normalized Plücker object improved the old chart frontier to `10, 11, 20, 30, 40`.
- Quotient and cross-ratio variants on the five-term object were weaker.
- Full six-window normalized Plücker improved the cheap frontier again to `20, 21`.
- The six-window projective quotient dropped back to `19, 20`.
- The object is now established exactly on `n=1..75` with coordinate count `19`.
- On the first recurrence-level family:
  - `constant_six_plucker_map` fails first at `20`
  - `difference_six_plucker_map` fails first at `21`
  - `support1_free_zero_six_plucker_map` is inconsistent on the fit block, with feature rank `31` and nullity `7`
- On short local-annihilator families of the six-window invariant itself:
  - relation lengths `4`, `5`, and `6` are all inconsistent at the first source window
  - relation lengths `4`, `5`, and `6` are all inconsistent at the first target window
- On global shared-scalar vector recurrences:
  - orders `2` through `10` are all inconsistent on the source six-window sequence
  - orders `2` through `10` are all inconsistent on the target six-window sequence

## Reading

The live promise is still in the full wider-window invariant, not in its projective quotients. The current wall is no
longer “find the object”; it is “find a structurally different family on the object, or leave the current invariant
family entirely.” The remaining plausible internal families are no longer cheap scalar ones.
