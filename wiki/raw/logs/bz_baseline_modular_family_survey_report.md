# Brown-Zudilin baseline recurrence family survey

- Survey ID: `bz_baseline_modular_family_survey_v1`
- Label: `Baseline modular recurrence family frontier`
- Modular baseline cache window: through `n=100`
- Modular certificate primes: `(1000003, 1000033, 1000037)`

| Family | Shifts | Degree Window | Equations | Certified Cap | First Gap |
| --- | --- | --- | --- | --- | --- |
| Order 3 consecutive | `(1, 0, -1, -2)` | `0..23` | 98 | 23 |  |
| Order 3 shifted by +1 | `(2, 1, 0, -1)` | `0..23` | 98 | 23 |  |
| Order 4 backward consecutive | `(1, 0, -1, -2, -3)` | `0..18` | 97 | 18 |  |
| Order 4 centered | `(2, 1, 0, -1, -2)` | `0..18` | 97 | 18 |  |
| Order 4 forward shifted | `(3, 2, 1, 0, -1)` | `0..18` | 97 | 18 |  |
| Order 5 centered | `(2, 1, 0, -1, -2, -3)` | `0..15` | 96 | 15 |  |

## Notes

- `order3_consecutive`: ruled out through the full scanned window `0..23`.
- `order3_shift2`: ruled out through the full scanned window `0..23`.
- `order4_backward_consecutive`: ruled out through the full scanned window `0..18`.
- `order4_centered`: ruled out through the full scanned window `0..18`.
- `order4_forward_shifted`: ruled out through the full scanned window `0..18`.
- `order5_centered`: ruled out through the full scanned window `0..15`.
