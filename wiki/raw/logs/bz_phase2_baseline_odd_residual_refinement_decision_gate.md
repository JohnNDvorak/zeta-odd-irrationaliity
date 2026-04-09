# Phase 2 baseline odd residual refinement decision gate

- Gate id: `bz_phase2_baseline_odd_residual_refinement_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_odd_residual_refinement_probe.md`
- Source probe id: `bz_phase2_baseline_odd_residual_refinement_probe`
- Shared exact window: `n=1..80`
- Outcome: `hard_wall_low_complexity_odd_refinement_exhausted`

| family | verdict | note |
| --- | --- | --- |
| `support0_same_index` | `fails_after_fit_window` | Fit window solves exactly but the family fails on the larger validation window. |
| `difference_pair` | `fails_after_fit_window` | Fit window solves exactly but the family fails on the larger validation window. |
| `support1_lagged_pair` | `fails_after_fit_window` | Fit window solves exactly but the family fails on the larger validation window. |

## Rationale

All fixed low-complexity odd-pair residual-refinement families fail after their fit windows. The odd-pair object is well-defined and projection-aligned, but this ladder is exhausted on the exact shared window.

## Next step

Stop autonomous execution and ask the user to choose the next pivot. Do not add richer odd-family ladders or change the target object again without that decision.

## Bridge boundary

The Zudilin 2002 bridge stack may be used only as calibration for conventions and failure modes. It may not redefine the active odd-pair object or supply hidden identities for it.

## Pivot options

- `richer_odd_projection_family`
- `different_baseline_packet`
