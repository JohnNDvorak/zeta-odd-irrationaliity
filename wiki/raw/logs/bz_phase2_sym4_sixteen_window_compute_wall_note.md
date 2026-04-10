# Phase 2 Sym^4-lifted sixteen-window compute wall note

- Date: `2026-04-09`
- Status: `compute_wall_not_banked`
- Draft object: `Sym^4`-lifted sixteen-window normalized maximal-minor object
- Draft coordinate count target: `15`
- Draft shared exact window target: `n=1..65`

## Draft lane

The active exploratory draft consists of:

- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_object_spec.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_probe.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_matrix_recurrence_screen.py`
- `src/zeta5_autoresearch/symmetric_dual_baseline_sym4_sixteen_window_affine_matrix_recurrence_screen.py`

with the supporting quartic lift added to:

- `src/zeta5_autoresearch/dual_packet_schur_functor.py`

## Stable result before the wall

The generic codimension-one normalized maximal-minor solver in `dual_packet_window_plucker.py` was improved from direct `Fraction` elimination to a row-scaled integer system followed by fraction-free elimination and rational back-substitution.

Low-level exact arithmetic checks remained clean after that change:

- `uv run pytest regression/test_dual_packet_window_plucker.py regression/test_dual_packet_schur_functor.py`
- result: `10 passed`

## Runtime observation

The first full `Sym^4` tranche command was:

- `uv run pytest regression/test_symmetric_dual_baseline_sym4_sixteen_window.py regression/test_symmetric_dual_baseline_sym4_sixteen_window_affine.py`

Observed behavior:

- before the solver rewrite, the tranche ran at saturated CPU for more than `9` minutes without completing
- after the solver rewrite, the tranche still ran at saturated CPU for more than `9` minutes without completing
- in both cases there was no immediate structural test failure; the wall is computational

## Sampled hotspot

Live process sampling on the post-rewrite run showed the dominant cost inside the exact codimension-one solver path:

- repeated big-integer `//` work inside fraction-free elimination
- heavy integer multiply / divide inside the quartic sixteen-window normalized maximal-minor construction

So the current wall is not the modular screen logic. It is exact invariant construction cost on the quartic lifted object.

## Current decision

- `Sym^4` sixteen-window is **not banked** as a frontier object
- the stable frontier remains the banked `Sym^3` eleven-window object
- the quartic line is currently an engineering blocker, not a certified mathematical screen result

## Recommended next move

If this line is resumed, it should resume as an engineering continuation, not as a new mathematical conclusion:

- stronger determinant / minor reuse
- cached elimination structure across adjacent windows
- or a cheaper nonlinear invariant family than the full quartic sixteen-window object
