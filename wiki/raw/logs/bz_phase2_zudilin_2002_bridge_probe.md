# Phase 2 Zudilin 2002 bridge probe

- Probe id: `bz_phase2_zudilin_2002_bridge_probe`
- Source: `Zudilin, A third-order Apéry-like recursion for ζ(5) (2002)`
- Location: `Theorem 1, equations (1) and (2)`
- This probe encodes the published third-order recurrence and initial data for the explicit bridge object.
- `q_n`, `p_n`, and `p̃_n` are generated exactly from the theorem statement.

| n | q_n | p_n / q_n | p̃_n / q_n | |ζ(5)-p_n/q_n| | |ζ(3)-p̃_n/q_n| |
| --- | --- | --- | --- | --- | --- |
| 0 | -1 | 0 | 0 | 1.036928e+00 | 1.202057e+00 |
| 1 | 42 | 29/28 | 101/84 | 1.213469e-03 | 3.240492e-04 |
| 2 | -17934 | 24289/23424 | 344923/286944 | 1.820151e-07 | 5.583050e-08 |
| 3 | 14290980 | 7682021239/7408444032 | 3710571371/3086851680 | 2.794868e-11 | 8.490551e-12 |
| 4 | -15226085070 | 24943788950905/24055474286592 | 602417685937/501155714304 | 4.126408e-15 | 1.254321e-15 |
| 5 | 19191613019292 | 81875586674776013003/78959779279372800000 | 553665861902579821/460598712463008000 | 6.014272e-19 | 1.828116e-19 |
| 6 | -26992352388411564 | 282653756112686336975107/272587704119854963200000 | 1001201457219628615259/832906873699556832000 | 8.703847e-23 | 2.645653e-23 |
| 7 | 41008495771961165448 | 215903781003833520407770175189/208214873150908926517286400000 | 202896348993489544115868841/168790968597392156983968000 | 1.254375e-26 | 3.812843e-27 |

## Notes

- This is the first repo-native encoding of the external bridge object chosen by the phase-2 decision gate.
- It is recurrence-explicit, unlike the current baseline dual packet, and is therefore stronger at the sequence-object level.
