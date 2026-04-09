# Brown-Zudilin dual F_7 companion exact-cost profile

- Context: repeated shared-cache extensions stall at the first unseen paired baseline term around `n=126`, even though the cache/checkpoint path is working correctly.
- Goal: isolate whether the bottleneck sits in setup, factorial normalization, or per-pole regular-series construction.

## Baseline `n=126` geometry

- Scaled baseline `b0`: `5166`
- Reduced-data build time: `0.000668s`
- Arithmetic renormalization time: `0.006637s`
- Pole count: `2143`
- Leftover-factor count: `2772`
- Central shift: `2584`
- Pole-order histogram: `[(1, 252), (2, 252), (3, 252), (4, 252), (5, 253), (6, 882)]`

## Representative pole-series timings

Measured with `_pole_regular_series(...)` on the first shift of each pole order.

| order | sample shift | wall time (s) | series length |
| --- | --- | --- | --- |
| 1 | 1513 | 0.083658 | 1 |
| 2 | 1639 | 0.099724 | 2 |
| 3 | 1765 | 0.121856 | 3 |
| 4 | 1891 | 0.176841 | 4 |
| 5 | 2017 | 0.257009 | 5 |
| 6 | 2143 | 0.355024 | 6 |

## Consequence

- Setup is negligible; the wall clock is dominated by repeated per-pole regular-series construction.
- The order-`6` block alone is the likely main cost center: there are `882` such poles, and the representative sample already costs about `0.355s`.
- Using the representative timings above as a rough extrapolation gives a total pole-construction cost on the order of `500s`, which matches the observed multi-minute stalls at the first unseen baseline paired term.

## Next optimization target

- Replace the current per-pole loop over all denominator/leftover factors inside `_pole_regular_series(...)` with shift-global reciprocal-power aggregates, so each pole can reuse precomputed sums instead of rebuilding the same log-series data from scratch.
- Resume the shared baseline extension to `n=127` only after that reduction in per-pole cost is in place or otherwise validated.
