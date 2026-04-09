# Brown-Zudilin baseline recurrence search

- Exact baseline `Q_n` terms computed through `n=34` from the published double-sum formula.
- Search family: consecutive-shift order-3 polynomial recurrences with shifts `(1, 0, -1, -2)`.
- Degree scan: `0` through `8`.
- Term generation time: `29.286s`.
- Linear-algebra search time: `79.525s`.
- Exact lower bound on the compatible degree over this window: no solution through degree `7`.
- First compatible degree on the exact window: `8`.
- Interpretation: this is a finite-window exact search result, not yet a verified recurrence for the baseline sequence.

| degree | equations | variables | rank | nullity | first basis max digits |
| --- | --- | --- | --- | --- | --- |
| 0 | 32 | 4 | 4 | 0 |  |
| 1 | 32 | 8 | 8 | 0 |  |
| 2 | 32 | 12 | 12 | 0 |  |
| 3 | 32 | 16 | 16 | 0 |  |
| 4 | 32 | 20 | 20 | 0 |  |
| 5 | 32 | 24 | 24 | 0 |  |
| 6 | 32 | 28 | 28 | 0 |  |
| 7 | 32 | 32 | 32 | 0 |  |
| 8 | 32 | 36 | 32 | 4 | 15206 |

## First Compatible Basis Sample

- Degree: `8`
- Maximum coefficient size: about `15206` decimal digits
- Shift `1` summary: `degree=8, nonzero_coeffs=9, max_digits~15102`
- Shift `0` summary: `degree=8, nonzero_coeffs=9, max_digits~15139`
- Shift `-1` summary: `degree=8, nonzero_coeffs=9, max_digits~15176`
- Shift `-2` summary: `degree=5, nonzero_coeffs=6, max_digits~15206`
