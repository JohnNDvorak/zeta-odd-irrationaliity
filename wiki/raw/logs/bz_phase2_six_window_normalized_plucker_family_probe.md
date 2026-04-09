# Phase 2 six-window normalized Plucker family probe

- Probe id: `bz_phase2_six_window_normalized_plucker_family_probe`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_six_window_normalized_plucker_probe.md`
- Source probe id: `bz_phase2_six_window_normalized_plucker_probe`
- Shared exact window: `n=1..75`
- Coordinate count: `19`
- Overall verdict: `six_window_plucker_family_exhausted_on_current_ladder`

| family | verdict | rank | nullity | first mismatch index | zero count | residual hash |
| --- | --- | --- | --- | --- | --- | --- |
| `constant_six_plucker_map` | `fails_after_fit_window` | `361` | `0` | `20` | `19` | `da3de9f47a31c165fc45c6e2d53cbfddf2e85e1a23435cb5f72871dd6ef3a16a` |
| `difference_six_plucker_map` | `fails_after_fit_window` | `361` | `0` | `21` | `19` | `ac967aa739c0fe13736ab371af114487258ede1b2222bb38a25d5f21cc18f6ea` |
| `support1_free_zero_six_plucker_map` | `inconsistent_fit_block` | `31` | `7` | `None` | `0` | `aaa749692a9b5dd9d5d6486aaf78ab580a9fed544d957ab4c67aee384b1c8f9a` |

## Notes

- `constant_six_plucker_map`: Cheap same-index family on the full six-window normalized Plucker object.
- `difference_six_plucker_map`: Cheap first-difference family on the full six-window normalized Plucker object.
- `support1_free_zero_six_plucker_map`: Canonical free-zero support-1 family is inconsistent on at least one target coordinate.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared six-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Use the family outcomes to choose whether the six-window object stays active or needs a different recurrence-level family.
