# Brown-Zudilin baseline modular recurrence certificates

- Exact baseline `Q_n` terms computed through `n=82` from the published double-sum formula.
- Search family: polynomial recurrences supported on shifts `(2, 1, 0, -1, -2)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Term generation time: `0.001s`.
- Modular rank scan time: `0.086s`.
- Certified consequence: no rational recurrence of this shape exists through degree `14`.
- First unresolved degree in this scan: `15`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 14 | 1000003 | 79 | 75 | 75 | 0 | yes |
| 14 | 1000033 | 79 | 75 | 75 | 0 | yes |
| 14 | 1000037 | 79 | 75 | 75 | 0 | yes |
| 15 | 1000003 | 79 | 80 | 79 | 1 | no |
| 15 | 1000033 | 79 | 80 | 79 | 1 | no |
| 15 | 1000037 | 79 | 80 | 79 | 1 | no |
