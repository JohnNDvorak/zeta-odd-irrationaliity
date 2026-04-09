# Brown-Zudilin baseline modular recurrence certificates

- Exact baseline `Q_n` terms computed through `n=70` from the published double-sum formula.
- Search family: polynomial recurrences supported on shifts `(2, 1, 0, -1, -2, -3)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Term generation time: `124.831s`.
- Modular rank scan time: `0.057s`.
- Certified consequence: no rational recurrence of this shape exists through degree `10`.
- First unresolved degree in this scan: `11`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | 1000003 | 66 | 66 | 66 | 0 | yes |
| 10 | 1000033 | 66 | 66 | 66 | 0 | yes |
| 10 | 1000037 | 66 | 66 | 66 | 0 | yes |
| 11 | 1000003 | 66 | 72 | 66 | 6 | no |
| 11 | 1000033 | 66 | 72 | 66 | 6 | no |
| 11 | 1000037 | 66 | 72 | 66 | 6 | no |
