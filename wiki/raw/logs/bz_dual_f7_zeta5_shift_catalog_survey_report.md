# Brown-Zudilin dual F_7 zeta(5)-coefficient shift-catalog survey

- Survey ID: `bz_dual_f7_zeta5_shift_catalog_survey_v1`
- Label: `Baseline dual F_7 zeta(5) coefficient shift catalog`
- Exact baseline dual zeta(5) coefficient cache window: through `n=80`
- Modular certificate primes: `(1000003, 1000033, 1000037)`
- Search logic: for a fixed support, full column rank at degree `d` implies the same for all lower degrees, so each family is certified with a monotone frontier search.

| Catalog | Order | Shift Window | Families | Frontier Degree Range | Fully Ruled Out | Survivors |
| --- | --- | --- | --- | --- | --- | --- |
| Order 3 supports in [-4, 4] | 3 | `[-4, 4]` | 44 | `17..18` | 32 | 12 |
| Order 4 supports in [-4, 4] | 4 | `[-4, 4]` | 67 | `13..14` | 49 | 18 |
| Order 5 supports in [-4, 4] | 5 | `[-4, 4]` | 56 | `11..11` | 56 | 0 |

## Findings

- `order3_span4`: `12` of `44` supports survive past the monotone frontier search.
- unresolved `(1, 0, -3, -4)`: certified through degree `17`, first gap `18`, frontier `18`, equations `76`.
- unresolved `(1, 0, -2, -4)`: certified through degree `17`, first gap `18`, frontier `18`, equations `76`.
- unresolved `(1, 0, -1, -4)`: certified through degree `17`, first gap `18`, frontier `18`, equations `76`.
- unresolved `(2, 0, -2, -3)`: certified through degree `17`, first gap `18`, frontier `18`, equations `76`.
- unresolved `(2, 0, -1, -3)`: certified through degree `17`, first gap `18`, frontier `18`, equations `76`.
- unresolved `(2, 1, 0, -3)`: certified through degree `17`, first gap `18`, frontier `18`, equations `76`.
- unresolved `(3, 0, -1, -2)`: certified through degree `17`, first gap `18`, frontier `18`, equations `76`.
- unresolved `(3, 1, 0, -2)`: certified through degree `17`, first gap `18`, frontier `18`, equations `76`.
- `order4_span4`: `18` of `67` supports survive past the monotone frontier search.
- unresolved `(2, 0, -2, -3, -4)`: certified through degree `13`, first gap `14`, frontier `14`, equations `75`.
- unresolved `(2, 0, -1, -3, -4)`: certified through degree `13`, first gap `14`, frontier `14`, equations `75`.
- unresolved `(2, 0, -1, -2, -4)`: certified through degree `13`, first gap `14`, frontier `14`, equations `75`.
- unresolved `(2, 1, 0, -3, -4)`: certified through degree `13`, first gap `14`, frontier `14`, equations `75`.
- unresolved `(2, 1, 0, -2, -4)`: certified through degree `13`, first gap `14`, frontier `14`, equations `75`.
- unresolved `(2, 1, 0, -1, -4)`: certified through degree `13`, first gap `14`, frontier `14`, equations `75`.
- unresolved `(3, 0, -1, -2, -3)`: certified through degree `13`, first gap `14`, frontier `14`, equations `75`.
- unresolved `(3, 1, 0, -2, -3)`: certified through degree `13`, first gap `14`, frontier `14`, equations `75`.
- `order5_span4`: all `56` normalized supports are ruled out through their full certifiable frontier.

## Frontier Samples

- `order3_span4` sample frontier support `(4, 3, 0, -1)`: frontier degree `18`, certified cap `17`, first gap `18`.
- `order4_span4` sample frontier support `(4, 3, 2, 0, -1)`: frontier degree `14`, certified cap `14`, first gap `None`.
- `order5_span4` sample frontier support `(4, 3, 2, 1, 0, -1)`: frontier degree `11`, certified cap `11`, first gap `None`.
