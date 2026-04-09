# Phase 2 six-window normalized Plucker decision gate

- Gate id: `bz_phase2_six_window_normalized_plucker_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_six_window_normalized_plucker_family_probe.md`
- Source probe id: `bz_phase2_six_window_normalized_plucker_family_probe`
- Shared exact window: `n=1..75`
- Outcome: `hard_wall_six_window_plucker_support1_inconsistent`

| family | verdict | note |
| --- | --- | --- |
| `constant_six_plucker_map` | `fails_after_fit_window` | Cheap same-index family on the full six-window normalized Plucker object. |
| `difference_six_plucker_map` | `fails_after_fit_window` | Cheap first-difference family on the full six-window normalized Plucker object. |
| `support1_free_zero_six_plucker_map` | `inconsistent_fit_block` | Canonical free-zero support-1 family is inconsistent on at least one target coordinate. |

## Rationale

The cheap constant/difference families fail, and the canonical free-zero support-1 family is already inconsistent on the initial fit block.

## Next step

Stop this family ladder and choose a genuinely different recurrence-level family on the same six-window object.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared six-window invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Pivot options

- `different_recurrence_family_on_six_window_plucker`
- `different_wider_window_nonlinear_object`
