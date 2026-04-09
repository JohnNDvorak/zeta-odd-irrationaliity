# Brown-Zudilin dual F_7 exact probe

- Fixture: `bz_dual_f7_exact_probe_v1`
- Source: `Brown and Zudilin, On cellular rational approximations to zeta(5)` (https://arxiv.org/abs/2210.03391)
- Source version: `v3`
- Numeric precision for exact-value verification: `120` decimal digits
- The exact extractor follows the displayed summand formula in equation (10), performs exact partial fractions in `mu`, and sums them into a rational term plus zeta values.
- The canonical `evaluate_f7` path follows that displayed-series normalization.
- The literal hypergeometric-line evaluation differs from the displayed summand by a factor `b0 + 2`; this report records that factor explicitly.

## Totally symmetric dual anchor

- Case id: `totally_symmetric`
- Base `a`: `(1, 1, 1, 1, 1, 1, 1, 1)`
- Base `b`: `(3, 1, 1, 1, 1, 1, 1, 1)`

| n | scaled b0 | constant term | zeta(3) coeff | zeta(5) coeff | log10|F_7| | log10|hyper line| | series/hyper |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | -98 | 66 | 18 | -3.341797 | -4.040767 | 5 |
| exact linear form |  | `F_7 = -98 + 66*zeta(3) + 18*zeta(5)` |  |  |  |  |  |
| 2 | 6 | -74463/16 | 6125/2 | 938 | -6.600779 | -7.503869 | 8 |
| exact linear form |  | `F_7 = -74463/16 + 6125/2*zeta(3) + 938*zeta(5)` |  |  |  |  |  |

## Brown-Zudilin baseline seed

- Case id: `baseline_bz`
- Base `a`: `(8, 16, 10, 15, 12, 16, 18, 13)`
- Base `b`: `(41, 17, 16, 15, 14, 13, 12, 11)`

| n | scaled b0 | constant term | zeta(3) coeff | zeta(5) coeff | log10|F_7| | log10|hyper line| | series/hyper |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 41 | 57993101249962008127812740936483643927138591089/680932458439833600000 | -3367966716871959076170056761/60 | -17062318711073217087874368 | -39.791136 | -41.424604 | 43 |
| exact linear form |  | `F_7 = 57993101249962008127812740936483643927138591089/680932458439833600000 - 3367966716871959076170056761/60*zeta(3) - 17062318711073217087874368*zeta(5)` |  |  |  |  |  |

