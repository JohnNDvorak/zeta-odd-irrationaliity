# Brown-Zudilin baseline modular recurrence certificates

- Exact baseline `Q_n` terms computed through `n=73` from the published double-sum formula.
- Search family: polynomial recurrences supported on shifts `(2, 1, 0, -1, -2)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Term generation time: `205.696s`.
- Modular rank scan time: `0.066s`.
- Certified consequence: no rational recurrence of this shape exists through degree `13`.
- First unresolved degree in this scan: `14`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 13 | 1000003 | 70 | 70 | 70 | 0 | yes |
| 13 | 1000033 | 70 | 70 | 70 | 0 | yes |
| 13 | 1000037 | 70 | 70 | 70 | 0 | yes |
| 14 | 1000003 | 70 | 75 | 70 | 5 | no |
| 14 | 1000033 | 70 | 75 | 70 | 5 | no |
| 14 | 1000037 | 70 | 75 | 70 | 5 | no |
