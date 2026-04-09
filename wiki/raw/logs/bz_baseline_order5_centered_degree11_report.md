# Brown-Zudilin baseline modular recurrence certificates

- Exact baseline `Q_n` terms computed through `n=76` from the published double-sum formula.
- Search family: polynomial recurrences supported on shifts `(2, 1, 0, -1, -2, -3)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Term generation time: `244.292s`.
- Modular rank scan time: `0.073s`.
- Certified consequence: no rational recurrence of this shape exists through degree `11`.
- First unresolved degree in this scan: `12`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 11 | 1000003 | 72 | 72 | 72 | 0 | yes |
| 11 | 1000033 | 72 | 72 | 72 | 0 | yes |
| 11 | 1000037 | 72 | 72 | 72 | 0 | yes |
| 12 | 1000003 | 72 | 78 | 72 | 6 | no |
| 12 | 1000033 | 72 | 78 | 72 | 6 | no |
| 12 | 1000037 | 72 | 78 | 72 | 6 | no |
