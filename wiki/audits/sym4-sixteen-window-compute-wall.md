---
title: Sym4 Sixteen-Window Compute Wall
category: audit
phase: '2'
direction: frontier
sources:
- raw/logs/bz_phase2_sym4_sixteen_window_compute_wall_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_engineering_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_gmp_followup_note.md
- raw/logs/bz_phase2_sym4_sixteen_window_target_partial_cache_followup_note__20260410_094652.md
last_updated: '2026-04-10'
---

Audit record for the attempted quartic higher-Schur continuation beyond the banked [[sym3-eleven-window-object]].

## Object and status

- Draft object: `Sym^4`-lifted sixteen-window normalized maximal-minor object
- Intended coordinate count: `15`
- Intended shared exact window: `n=1..65`
- Status: `compute wall`, not banked

## What was established

- The quartic lift support was added to the higher-Schur helper layer.
- The codimension-one normalized maximal-minor solver was improved from direct `Fraction` elimination to row-scaled integer elimination with rational back-substitution.
- The rolling codimension-one path was then strengthened again by:
  - per-column integerization
  - common-denominator row encoding
  - common-denominator coordinate updates with `Fraction` reconstruction deferred to output only
- Low-level exact arithmetic checks stayed green after the new rolling rewrite, with `11` passing checks.
- The rolling integer state was then pushed onto a GMP-backed big-integer path when `gmpy2` is available.

## Failure mode

The first full quartic tranche did not produce a banked object within practical turn-time:

- before the solver rewrite, the quartic pytest tranche ran at saturated CPU for more than `9` minutes without completing
- after the first solver rewrite, the quartic pytest tranche again ran at saturated CPU for more than `9` minutes without completing
- after the rolling rewrite, the quartic line split asymmetrically:
  - source-side `_build_sym4_sixteen_window_side("source")` completed in approximately `6.443` seconds
  - target-side `_build_sym4_sixteen_window_side("target")` still did not finish during a bounded run exceeding `180` seconds
- after the GMP-backed rolling rewrite, the split sharpened further:
  - source-side `_build_sym4_sixteen_window_side("source")` improved again to approximately `2.990` seconds
  - target-side `_build_sym4_sixteen_window_side("target")` still did not finish during a bounded run exceeding `180` seconds
- after the persisted target-side partial-cache follow-up:
  - the quartic target-side path became resumable instead of all-or-nothing
  - initialization was timed at approximately `103.23` seconds
  - exact cached progress reached `8 / 65` windows
  - ordinary resumed advances still cost approximately `84.06`, `93.39`, and `111.81` seconds
  - singular-pivot recovery rebases cost approximately `140.81`, `154.61`, and `188.13` seconds
  - the next predicted rebase after the sixth completed window did occur, and the lead became nonzero again afterward
  - the next predicted ordinary step after the seventh completed window also occurred, and the lead returned to zero afterward

Live process sampling and timing now point to a narrower blocker:

- the original elimination hotspot was reduced enough for the source side to become tractable
- the remaining active wall is target-side exact sixteen-window normalized maximal-minor construction
- more precisely, it is the cost of target-side rolling advancement and occasional singular-pivot rebasing inside that construction
- the first eight completed windows are consistent with an alternating rebase / ordinary-step pattern rather than a one-off singularity
- there is no immediate easy win from changing the quartic lifted-vector integerization formula alone; early target samples matched the direct base-derived quartic integer chart exactly

## Interpretation

This is an engineering blocker, not a mathematical obstruction result:

- `Sym^4` sixteen-window has **not** been certified as a new frontier object
- the stable banked higher-Schur frontier remains [[sym3-eleven-window-object]]
- the quartic wall is now asymmetric:
  - source side tractable and materially faster after the GMP-backed rolling rewrite
  - target side still blocked
- resuming the quartic line would now require a strategy change on the target side:
  - stronger reuse or growth control specifically on the target-side rolling integer state
  - continued checkpointed or persisted target-side window construction
  - or a cheaper nonlinear invariant family

The current best continuation inside the quartic lane is now recorded separately in [[sym4-sixteen-window-target-partial-cache-progress]].
