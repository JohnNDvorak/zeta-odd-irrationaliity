# Phase 2 six-window normalized Plucker global recurrence screen

- Screen id: `bz_phase2_six_window_normalized_plucker_global_recurrence_screen`
- Source probe id: `bz_phase2_six_window_normalized_plucker_probe`
- Shared exact window: `n=1..75`
- Overall verdict: `low_order_global_vector_recurrence_exhausted_through_order_10`

| side | order | equation count | verdict | rank | nullity | coefficient preview |
| --- | --- | --- | --- | --- | --- | --- |
| `source` | `2` | `1387` | `inconsistent` | `None` | `None` | `` |
| `target` | `2` | `1387` | `inconsistent` | `None` | `None` | `` |
| `source` | `3` | `1368` | `inconsistent` | `None` | `None` | `` |
| `target` | `3` | `1368` | `inconsistent` | `None` | `None` | `` |
| `source` | `4` | `1349` | `inconsistent` | `None` | `None` | `` |
| `target` | `4` | `1349` | `inconsistent` | `None` | `None` | `` |
| `source` | `5` | `1330` | `inconsistent` | `None` | `None` | `` |
| `target` | `5` | `1330` | `inconsistent` | `None` | `None` | `` |
| `source` | `6` | `1311` | `inconsistent` | `None` | `None` | `` |
| `target` | `6` | `1311` | `inconsistent` | `None` | `None` | `` |
| `source` | `7` | `1292` | `inconsistent` | `None` | `None` | `` |
| `target` | `7` | `1292` | `inconsistent` | `None` | `None` | `` |
| `source` | `8` | `1273` | `inconsistent` | `None` | `None` | `` |
| `target` | `8` | `1273` | `inconsistent` | `None` | `None` | `` |
| `source` | `9` | `1254` | `inconsistent` | `None` | `None` | `` |
| `target` | `9` | `1254` | `inconsistent` | `None` | `None` | `` |
| `source` | `10` | `1235` | `inconsistent` | `None` | `None` | `` |
| `target` | `10` | `1235` | `inconsistent` | `None` | `None` | `` |

## Interpretation

This screen tests whether the full six-window normalized Plucker sequence satisfies a single global shared-scalar vector recurrence at low order, separately on the source and target side.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared six-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Do not keep enlarging low-order global shared-scalar vector recurrence order on the six-window normalized Plucker object without a new structural reason.
