# Brown-Zudilin baseline modular recurrence certificates

- Exact baseline `Q_n` terms computed through `n=66` from the published double-sum formula.
- Search family: polynomial recurrences supported on shifts `(1, 0, -1, -2)`.
- Modular certificate primes: `(1000003, 1000033, 1000037)`.
- Term generation time: `0.001s`.
- Modular rank scan time: `0.090s`.
- Certified consequence: no rational recurrence of this shape exists through degree `15`.
- Logic: if one prime gives full column rank, the same degree is impossible over `Q`.

| degree | modulus | equations | variables | rank | nullity upper bound | certifies no solution |
| --- | --- | --- | --- | --- | --- | --- |
| 12 | 1000003 | 64 | 52 | 52 | 0 | yes |
| 12 | 1000033 | 64 | 52 | 52 | 0 | yes |
| 12 | 1000037 | 64 | 52 | 52 | 0 | yes |
| 13 | 1000003 | 64 | 56 | 56 | 0 | yes |
| 13 | 1000033 | 64 | 56 | 56 | 0 | yes |
| 13 | 1000037 | 64 | 56 | 56 | 0 | yes |
| 14 | 1000003 | 64 | 60 | 60 | 0 | yes |
| 14 | 1000033 | 64 | 60 | 60 | 0 | yes |
| 14 | 1000037 | 64 | 60 | 60 | 0 | yes |
| 15 | 1000003 | 64 | 64 | 64 | 0 | yes |
| 15 | 1000033 | 64 | 64 | 64 | 0 | yes |
| 15 | 1000037 | 64 | 64 | 64 | 0 | yes |
