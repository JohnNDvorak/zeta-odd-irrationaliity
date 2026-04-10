# Phase 2 Sym^2-lifted seven-window matrix recurrence screen

- Screen id: `bz_phase2_sym2_seven_window_matrix_recurrence_screen`
- Source probe id: `bz_phase2_sym2_seven_window_probe`
- Shared exact window: `n=1..74`
- Overall verdict: `low_order_matrix_recurrence_exhausted_through_order_10`

| side | recurrence order | matrix size | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- |
| `source` | `1` | `6` | `438` | `36` | `inconsistent_mod_prime` | `1009` |
| `target` | `1` | `6` | `438` | `36` | `inconsistent_mod_prime` | `1447` |
| `source` | `2` | `6` | `432` | `72` | `inconsistent_mod_prime` | `1009` |
| `target` | `2` | `6` | `432` | `72` | `inconsistent_mod_prime` | `1447` |
| `source` | `3` | `6` | `426` | `108` | `inconsistent_mod_prime` | `1009` |
| `target` | `3` | `6` | `426` | `108` | `inconsistent_mod_prime` | `1447` |
| `source` | `4` | `6` | `420` | `144` | `inconsistent_mod_prime` | `1009` |
| `target` | `4` | `6` | `420` | `144` | `inconsistent_mod_prime` | `1447` |
| `source` | `5` | `6` | `414` | `180` | `inconsistent_mod_prime` | `1009` |
| `target` | `5` | `6` | `414` | `180` | `inconsistent_mod_prime` | `1447` |
| `source` | `6` | `6` | `408` | `216` | `inconsistent_mod_prime` | `1009` |
| `target` | `6` | `6` | `408` | `216` | `inconsistent_mod_prime` | `1447` |
| `source` | `7` | `6` | `402` | `252` | `inconsistent_mod_prime` | `1009` |
| `target` | `7` | `6` | `402` | `252` | `inconsistent_mod_prime` | `1447` |
| `source` | `8` | `6` | `396` | `288` | `inconsistent_mod_prime` | `1009` |
| `target` | `8` | `6` | `396` | `288` | `inconsistent_mod_prime` | `1447` |
| `source` | `9` | `6` | `390` | `324` | `inconsistent_mod_prime` | `1009` |
| `target` | `9` | `6` | `390` | `324` | `inconsistent_mod_prime` | `1447` |
| `source` | `10` | `6` | `384` | `360` | `inconsistent_mod_prime` | `1009` |
| `target` | `10` | `6` | `384` | `360` | `inconsistent_mod_prime` | `1447` |

## Interpretation

This screen tests constant matrix-valued recurrences on the Sym^2-lifted seven-window normalized maximal-minor sequence, for recurrence orders `1` through `10`, separately on the source and target side. Order `11` is the first underdetermined case on this lifted object.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^2-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not keep increasing matrix recurrence order mechanically. Order 11 is the first underdetermined case on this lifted object, so further escalation would cross from obstruction screening into interpolation territory.
