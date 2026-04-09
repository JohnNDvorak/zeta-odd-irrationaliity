# Brown-Zudilin baseline modular recurrence certificates

- Baseline `Q_n mod p` values computed directly from the published double-sum formula through `n=100`.
- Search family: polynomial recurrences supported on shifts `(2, 1, 0, -1, -2, -3)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Sequence source: `modular_double_sum_cache`.
- Modular sequence generation time: `0.000s`.
- Modular rank scan time: `0.223s`.
- Certified consequence: no rational recurrence of this shape exists through degree `15`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 13 | 1000003 | 96 | 84 | 84 | 0 | yes |
| 13 | 1000033 | 96 | 84 | 84 | 0 | yes |
| 13 | 1000037 | 96 | 84 | 84 | 0 | yes |
| 14 | 1000003 | 96 | 90 | 90 | 0 | yes |
| 14 | 1000033 | 96 | 90 | 90 | 0 | yes |
| 14 | 1000037 | 96 | 90 | 90 | 0 | yes |
| 15 | 1000003 | 96 | 96 | 96 | 0 | yes |
| 15 | 1000033 | 96 | 96 | 96 | 0 | yes |
| 15 | 1000037 | 96 | 96 | 96 | 0 | yes |
