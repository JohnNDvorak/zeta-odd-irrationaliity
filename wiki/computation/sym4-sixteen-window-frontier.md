---
title: Sym4 Sixteen-Window Frontier
category: computation
phase: '2'
direction: '13'
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_object_spec.md
- raw/logs/bz_phase2_sym4_sixteen_window_probe.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260415_203158.md
last_updated: '2026-04-15'
---

Current higher-Schur frontier: the `Sym^4`-lifted sixteen-window object is now the strongest **banked** exact paired invariant. Its recurrence-level homogeneous and affine matrix ladders have not yet been screened.

## Object summary

- The `Sym^4`-lifted sixteen-window object is established exactly on `n=1..65`.
- It has coordinate count `15`.
- The paired object hash is `dfe18fe136e64e09be99280cd26919bb5e28219f81847e73d7dbfca7ee85b606`.
- The target-side cache reached `65 / 65` exact windows and materialized `data/cache/bz_phase2_sym4_sixteen_window_target_sequence_cache.json`.
- The final target sequence cache is `131681112` bytes.

## What Changed

The previous state was an engineering-only quartic continuation: the source side was tractable, but the target side had to be advanced by a persisted cache through alternating ordinary and rebase steps. That cache is now complete, and the default loader has been patched to parse the large cached fractions without requiring an external Python digit-limit override.

## Open Screens

- Homogeneous matrix ladder through order `4`, separately on source and target.
- Affine matrix ladder through order `3`, separately on source and target.
- Any transfer or recurrence claim must wait for those screens or an equally explicit follow-up certificate.

## Reading

This is a genuine mathematical frontier advance at the object level, not yet a proof-side recurrence success. The strongest banked object is now quartic, while the strongest banked hard-wall certificates remain on the predecessor [[sym3-eleven-window-object]] until the Sym4 screens are run.
