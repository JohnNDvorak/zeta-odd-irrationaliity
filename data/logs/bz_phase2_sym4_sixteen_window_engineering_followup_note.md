# Phase 2 Sym^4-lifted sixteen-window engineering follow-up note

- Date: `2026-04-09`
- Status: `asymmetric_compute_wall`
- Draft object: `Sym^4`-lifted sixteen-window normalized maximal-minor object
- Draft coordinate count target: `15`
- Draft shared exact window target: `n=1..65`

## Engineering continuation

This follow-up resumes the quartic sixteen-window line after the earlier compute-wall checkpoint.

The exact codimension-one rolling path in `dual_packet_window_plucker.py` was strengthened in three ways:

- per-column integerization for the rolling codimension-one chart
- common-denominator row encoding for the rolling inverse rows
- common-denominator coordinate updates, with `Fraction` reconstruction deferred to output only

This changed the hot path from repeated exact rational row updates to integer-only rolling state updates plus output-boundary reconstruction.

## Exact regression status

Low-level exact arithmetic checks remained clean after the new rolling rewrite:

- `uv run pytest regression/test_dual_packet_window_plucker.py regression/test_dual_packet_schur_functor.py`
- result: `11 passed`

The new regression explicitly checks a fractional codimension-one multi-window case against a direct Gaussian-elimination oracle.

## Runtime split

Bounded direct timing on the quartic side-specific builders now shows a real asymmetry:

- source side:
  - `_build_sym4_sixteen_window_side("source")`
  - completed in approximately `6.443` seconds
  - produced `65` windows with coordinate count `15`
- target side:
  - `_build_sym4_sixteen_window_side("target")`
  - did **not** finish during a bounded run exceeding `180` seconds

So the earlier generic quartic compute wall has narrowed:

- source-side quartic exact invariant construction is now tractable
- target-side quartic exact invariant construction remains the active wall

## Additional screen

The quartic target vectors do not appear to admit an obviously cheaper per-vector integer chart:

- direct base-derived quartic integerization was checked against the generic lifted-vector integerization on early target samples
- the representations matched exactly on those samples

So there is no immediate easy win from replacing the lifted-vector integerization formula alone.

## Current interpretation

- `Sym^4` sixteen-window is still **not banked** as a frontier object
- the stable banked higher-Schur frontier remains the `Sym^3` eleven-window object
- the current quartic blocker is now more precise:
  - not a blanket quartic failure
  - specifically the target-side exact sixteen-window normalized maximal-minor construction

## Recommended next move

If the quartic line is resumed again, the next engineering move should target the remaining target-side window solve directly:

- stronger reuse or caching inside the rolling integer state
- or a target-specific representation change that reduces big-integer growth during the common-denominator update path
