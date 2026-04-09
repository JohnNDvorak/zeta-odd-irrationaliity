# Brown-Zudilin baseline shift-catalog survey

- Survey ID: `bz_baseline_shift_catalog_survey_v1`
- Label: `Baseline asymmetric and non-consecutive shift supports`
- Modular baseline cache window: through `n=100`
- Modular certificate primes: `(1000003, 1000033, 1000037)`
- Search logic: for a fixed support, full column rank at degree `d` implies the same for all lower degrees, so each family is certified with a monotone frontier search.

| Catalog | Order | Shift Window | Families | Frontier Degree Range | Fully Ruled Out | Survivors |
| --- | --- | --- | --- | --- | --- | --- |
| Order 4 supports in [-4, 4] | 4 | `[-4, 4]` | 67 | `17..18` | 67 | 0 |
| Order 5 supports in [-4, 4] | 5 | `[-4, 4]` | 56 | `14..15` | 56 | 0 |

## Findings

- `order4_span4`: all `67` normalized supports are ruled out through their full certifiable frontier.
- `order5_span4`: all `56` normalized supports are ruled out through their full certifiable frontier.

## Frontier Samples

- `order4_span4` sample frontier support `(4, 3, 2, 0, -1)`: frontier degree `18`, certified cap `18`, first gap `None`.
- `order5_span4` sample frontier support `(4, 3, 2, 1, 0, -1)`: frontier degree `15`, certified cap `15`, first gap `None`.
