# Brown-Zudilin totally symmetric linear-form probe

- Fixture: `bz_totally_symmetric_linear_forms_v1`
- Shared recurrence evidence: `bz_totally_symmetric_q_recurrence_v1`
- Source: `Brown and Zudilin, On cellular rational approximations to zeta(5)` (https://arxiv.org/abs/2210.03391)
- Source version: `v3`
- Exact recurrence generation through `n=14`
- Precision for numeric remainders: `80` decimal digits
- `P_n` recurrence residuals: `pass`
- `hat P_n` recurrence residuals: `pass`
- Latest `log|d_n^5 Q_n|/n`: `10.28521347` at `n=14`
- Latest `log|d_n^5(Q_n zeta(5)-P_n)|/n`: `1.59962451` at `n=14`
- Latest worthiness estimate: `0.84447338`
- Published worthiness for the totally symmetric anchor: `0.77795976`
- The finite-n worthiness estimates converge slowly and oscillate; treat them as calibration, not certification.
- The probe trusts the shared recurrence and the published initial values; it does not enforce the paper's separate experimental denominator claims.
- This is an exact remainder pipeline for the totally symmetric anchor, not yet for the Brown-Zudilin baseline seed.

| n | q digits | P numerator digits | P denominator | phat numerator digits | phat denominator | p residual zero | phat residual zero | log|d_n^5 Q_n|/n | log|d_n^5 I'_n|/n | gamma est |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 | 1 | yes | yes |  |  |  |
| 1 | 2 | 2 | 4 | 3 | 4 | yes | yes | 3.04452244 | -3.66974929 | 2.20536122 |
| 2 | 4 | 7 | 384 | 6 | 96 | yes | yes | 5.73421503 | -2.02537306 | 1.35320843 |
| 3 | 6 | 10 | 10368 | 10 | 4320 | yes | yes | 7.47940140 | -0.62081564 | 1.08300339 |
| 4 | 9 | 14 | 110592 | 12 | 2304 | yes | yes | 7.90557848 | -0.37476378 | 1.04740498 |
| 5 | 11 | 20 | 1036800000 | 18 | 6048000 | yes | yes | 9.10555764 | 0.71456134 | 0.92152470 |
| 6 | 14 | 24 | 9331200000 | 22 | 28512000 | yes | yes | 8.57955679 | 0.11360812 | 0.98675828 |
| 7 | 17 | 30 | 17425497600000 | 27 | 14126112000 | yes | yes | 9.60295515 | 1.08287301 | 0.88723544 |
| 8 | 19 | 34 | 716934758400000 | 30 | 145297152000 | yes | yes | 9.59348640 | 1.03247021 | 0.89237800 |
| 9 | 22 | 38 | 19357238476800000 | 34 | 2020951296000 | yes | yes | 9.81546745 | 1.22241225 | 0.87546062 |
| 10 | 25 | 41 | 45166889779200000 | 39 | 89595507456000 | yes | yes | 9.44667062 | 0.82785556 | 0.91236536 |
| 11 | 27 | 49 | 3117502613927116800000 | 44 | 51107837324544000 | yes | yes | 10.23704447 | 1.59706716 | 0.84399138 |
| 12 | 30 | 52 | 7274172765829939200000 | 47 | 210983636134656000 | yes | yes | 9.89821280 | 1.24054063 | 0.87467024 |
| 13 | 33 | 60 | 900283142914431871795200000 | 53 | 154510349529279744000 | yes | yes | 10.59930963 | 1.92662221 | 0.81823135 |
| 14 | 35 | 60 | 5010852372436541030400000 | 55 | 42139186235258112000 | yes | yes | 10.28521347 | 1.59962451 | 0.84447338 |
