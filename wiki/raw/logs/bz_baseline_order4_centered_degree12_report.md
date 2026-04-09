# Brown-Zudilin baseline modular recurrence certificates

- Exact baseline `Q_n` terms computed through `n=68` from the published double-sum formula.
- Search family: polynomial recurrences supported on shifts `(2, 1, 0, -1, -2)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Term generation time: `111.122s`.
- Modular rank scan time: `0.055s`.
- Certified consequence: no rational recurrence of this shape exists through degree `12`.
- First unresolved degree in this scan: `13`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 12 | 1000003 | 65 | 65 | 65 | 0 | yes |
| 12 | 1000033 | 65 | 65 | 65 | 0 | yes |
| 12 | 1000037 | 65 | 65 | 65 | 0 | yes |
| 13 | 1000003 | 65 | 70 | 65 | 5 | no |
| 13 | 1000033 | 65 | 70 | 65 | 5 | no |
| 13 | 1000037 | 65 | 70 | 65 | 5 | no |
