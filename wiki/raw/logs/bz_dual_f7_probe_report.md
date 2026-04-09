# Brown-Zudilin dual F_7 probe

- Fixture: `bz_dual_f7_probe_v1`
- Source: `Brown and Zudilin, On cellular rational approximations to zeta(5)` (https://arxiv.org/abs/2210.03391)
- Source version: `v3`
- Numeric precision for `F_7(b)`: `120` decimal digits
- Numeric precision for PSLQ search: `180` decimal digits
- The evaluator follows the displayed-series normalization for `F_7(b)` together with the affine map from `a` to `b`.
- The literal hypergeometric-line evaluation differs by a factor `b0 + 2`; this report uses the displayed-series normalization because it matches the exact coefficient extractor.
- Any recovered decomposition into `1`, `zeta(3)`, and `zeta(5)` is an uncertified numeric PSLQ witness, not an exact proof object.
- A missing PSLQ relation means no low-height relation was found at the tested coefficient bound; it does not certify nonexistence.

## Totally symmetric dual anchor

- Case id: `totally_symmetric`
- Base `a`: `(1, 1, 1, 1, 1, 1, 1, 1)`
- Base `b`: `(3, 1, 1, 1, 1, 1, 1, 1)`

| n | scaled b0 | F_7(b*n) | log10|F_7| | log|F_7|/n | PSLQ status |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0.0004552011138815103 | -3.341797 | -7.69477123 | F_7 = -98 + 66*zeta(3) + 18*zeta(5) (log10 residual -124.2) |
| 2 | 6 | 2.507384899355189e-7 | -6.600779 | -7.59942766 | F_7 = -74463/16 + 6125/2*zeta(3) + 938*zeta(5) (log10 residual -126.3) |
| 3 | 9 | 1.954620061217874e-10 | -9.708938 | -7.45188503 | no low-height relation found |
| 4 | 12 | 1.829314854687396e-13 | -12.737712 | -7.33241618 | no low-height relation found |
| 5 | 15 | 1.916561365466114e-16 | -15.717477 | -7.23816577 | no low-height relation found |

## Brown-Zudilin baseline seed

- Case id: `baseline_bz`
- Base `a`: `(8, 16, 10, 15, 12, 16, 18, 13)`
- Base `b`: `(41, 17, 16, 15, 14, 13, 12, 11)`

| n | scaled b0 | F_7(b*n) | log10|F_7| | log|F_7|/n | PSLQ status |
| --- | --- | --- | --- | --- | --- |
| 1 | 41 | 1.617574207720887e-40 | -39.791136 | -91.62247610 | no low-height relation found |
| 2 | 82 | 3.40516185124174e-78 | -77.467862 | -89.18817239 | no low-height relation found |
| 3 | 123 | 1.408011137812775e-115 | -114.851394 | -88.15170251 | no low-height relation found |

