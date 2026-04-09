# Brown-Zudilin baseline modular recurrence certificates

- Baseline `Q_n mod p` values computed directly from the published double-sum formula through `n=100`.
- Search family: polynomial recurrences supported on shifts `(1, 0, -1, -2)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Sequence source: `modular_double_sum_cache`.
- Modular sequence generation time: `0.000s`.
- Modular rank scan time: `0.236s`.
- Certified consequence: no rational recurrence of this shape exists through degree `23`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 21 | 1000003 | 98 | 88 | 88 | 0 | yes |
| 21 | 1000033 | 98 | 88 | 88 | 0 | yes |
| 21 | 1000037 | 98 | 88 | 88 | 0 | yes |
| 22 | 1000003 | 98 | 92 | 92 | 0 | yes |
| 22 | 1000033 | 98 | 92 | 92 | 0 | yes |
| 22 | 1000037 | 98 | 92 | 92 | 0 | yes |
| 23 | 1000003 | 98 | 96 | 96 | 0 | yes |
| 23 | 1000033 | 98 | 96 | 96 | 0 | yes |
| 23 | 1000037 | 98 | 96 | 96 | 0 | yes |
