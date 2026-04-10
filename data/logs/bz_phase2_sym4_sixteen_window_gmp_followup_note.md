# Phase 2 Sym^4-lifted sixteen-window GMP follow-up note

- Date: `2026-04-09`
- Status: `target_side_compute_wall_persists`
- Draft object: `Sym^4`-lifted sixteen-window normalized maximal-minor object

## Engineering continuation

This follow-up resumes the quartic sixteen-window line after the rolling common-denominator rewrite.

The exact rolling state in `dual_packet_window_plucker.py` was pushed onto a GMP-backed big-integer path when `gmpy2` is available:

- integerized column entries are stored as `gmpy2.mpz` in the rolling codimension-one state
- common-denominator row numerators and coordinate numerators stay on the GMP-backed path
- the one-time initial basis inversion remains on plain integer / `Fraction` arithmetic to avoid `mpz * Fraction` interop failures during back-substitution

## Exact regression status

Low-level exact arithmetic checks stayed green after the GMP-backed rolling rewrite:

- `uv run pytest regression/test_dual_packet_window_plucker.py regression/test_dual_packet_schur_functor.py`
- result: `11 passed`

## Runtime split

The GMP-backed path produced another real source-side speedup:

- source side:
  - `_build_sym4_sixteen_window_side("source")`
  - completed in approximately `2.990` seconds
  - previous measured post-rolling time was approximately `6.443` seconds

The target side still did not clear the practical wall:

- target side:
  - `_build_sym4_sixteen_window_side("target")`
  - still did **not** finish during a bounded run exceeding `180` seconds

## Current interpretation

- the quartic sixteen-window engineering line has improved materially on the source side
- the target-side exact sixteen-window normalized maximal-minor construction remains the active blocker even after:
  - row-scaled fraction-free elimination
  - rolling common-denominator state reuse
  - GMP-backed big-integer rolling numerators

So the remaining wall is now sharply localized.

## Recommended next move

If the quartic line is resumed again, the next engineering move should likely change execution strategy rather than just arithmetic backend:

- checkpointed target-side rolling state reuse across windows
- persisted partial target-side window caches
- or a target-specific representation that reduces denominator-growth pressure before the rolling update stage
