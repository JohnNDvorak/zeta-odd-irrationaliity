---
title: Six-Window Normalized Plucker Annihilator Screen
category: audit
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_six_window_normalized_plucker_annihilator_screen.md
- raw/logs/bz_phase2_six_window_normalized_plucker_probe.md
last_updated: '2026-04-09'
---

Audit record for short local-annihilator families tested directly on the [[six-window-normalized-plucker-object]].

## Object and window

- Object: six-window normalized `Gr(3,6)` Plücker sequence
- Shared exact object window: `n=1..75`
- Tested family: local annihilator relations on consecutive Plücker vectors themselves, not transfer-map residuals

## Orders screened

The screen tests three short orders on both the source and target six-window sequences:

- relation length `4`
- relation length `5`
- relation length `6`

## Certified failure mode

For both source and target:

- relation length `4`: first inconsistent index `1`
- relation length `5`: first inconsistent index `1`
- relation length `6`: first inconsistent index `1`

No short order showed a nonunique-but-consistent fit. They fail immediately by inconsistency.

## Interpretation

This closes the natural short local-annihilator continuation on the current six-window object. It is stronger than
saying “support-1 transfer failed”: it says the object does not even admit a short direct annihilator profile of the
most obvious local kinds.

## Next move

Do not retry short local-annihilator orders on this object without a new structural reason. The remaining live options
are:

- a more structural nonlocal family on the same object
- a different nonlinear invariant family beyond the current Plücker object
