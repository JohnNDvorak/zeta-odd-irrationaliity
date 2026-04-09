# Brown-Zudilin baseline modular recurrence certificates

- Exact baseline `Q_n` terms computed through `n=82` from the published double-sum formula.
- Search family: polynomial recurrences supported on shifts `(2, 1, 0, -1, -2, -3)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Term generation time: `596.596s`.
- Modular rank scan time: `0.092s`.
- Certified consequence: no rational recurrence of this shape exists through degree `12`.
- First unresolved degree in this scan: `13`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 12 | 1000003 | 78 | 78 | 78 | 0 | yes |
| 12 | 1000033 | 78 | 78 | 78 | 0 | yes |
| 12 | 1000037 | 78 | 78 | 78 | 0 | yes |
| 13 | 1000003 | 78 | 84 | 78 | 6 | no |
| 13 | 1000033 | 78 | 84 | 78 | 6 | no |
| 13 | 1000037 | 78 | 84 | 78 | 6 | no |
