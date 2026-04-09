# Brown-Zudilin baseline shift-catalog survey

- Survey ID: `bz_baseline_shift_catalog_survey_wide_v1`
- Label: `Baseline wide-support shift catalogs`
- Modular baseline cache window: through `n=100`
- Modular certificate primes: `(1000003, 1000033, 1000037)`
- Search logic: for a fixed support, full column rank at degree `d` implies the same for all lower degrees, so each family is certified with a monotone frontier search.

| Catalog | Order | Shift Window | Families | Frontier Degree Range | Fully Ruled Out | Survivors |
| --- | --- | --- | --- | --- | --- | --- |
| Order 4 supports in [-5, 5] | 4 | `[-5, 5]` | 199 | `17..18` | 199 | 0 |
| Order 5 supports in [-5, 5] | 5 | `[-5, 5]` | 250 | `14..15` | 250 | 0 |
| Order 6 supports in [-4, 4] | 6 | `[-4, 4]` | 28 | `12..12` | 28 | 0 |

## Findings

- `order4_span5`: all `199` normalized supports are ruled out through their full certifiable frontier.
- `order5_span5`: all `250` normalized supports are ruled out through their full certifiable frontier.
- `order6_span4`: all `28` normalized supports are ruled out through their full certifiable frontier.

## Frontier Samples

- `order4_span5` sample frontier support `(5, 4, 3, 0, -1)`: frontier degree `18`, certified cap `18`, first gap `None`.
- `order5_span5` sample frontier support `(4, 3, 2, 1, 0, -1)`: frontier degree `15`, certified cap `15`, first gap `None`.
- `order6_span4` sample frontier support `(4, 3, 2, 1, 0, -1, -2)`: frontier degree `12`, certified cap `12`, first gap `None`.
