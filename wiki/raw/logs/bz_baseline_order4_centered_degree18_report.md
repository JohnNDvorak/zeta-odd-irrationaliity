# Brown-Zudilin baseline modular recurrence certificates

- Baseline `Q_n mod p` values computed directly from the published double-sum formula through `n=100`.
- Search family: polynomial recurrences supported on shifts `(2, 1, 0, -1, -2)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Sequence source: `modular_double_sum_cache`.
- Modular sequence generation time: `0.000s`.
- Modular rank scan time: `0.289s`.
- Certified consequence: no rational recurrence of this shape exists through degree `18`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 15 | 1000003 | 97 | 80 | 80 | 0 | yes |
| 15 | 1000033 | 97 | 80 | 80 | 0 | yes |
| 15 | 1000037 | 97 | 80 | 80 | 0 | yes |
| 16 | 1000003 | 97 | 85 | 85 | 0 | yes |
| 16 | 1000033 | 97 | 85 | 85 | 0 | yes |
| 16 | 1000037 | 97 | 85 | 85 | 0 | yes |
| 17 | 1000003 | 97 | 90 | 90 | 0 | yes |
| 17 | 1000033 | 97 | 90 | 90 | 0 | yes |
| 17 | 1000037 | 97 | 90 | 90 | 0 | yes |
| 18 | 1000003 | 97 | 95 | 95 | 0 | yes |
| 18 | 1000033 | 97 | 95 | 95 | 0 | yes |
| 18 | 1000037 | 97 | 95 | 95 | 0 | yes |
