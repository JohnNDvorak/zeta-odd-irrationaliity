# Phase 2 baseline residual refinement decision gate

- Gate id: `bz_phase2_baseline_residual_refinement_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_residual_refinement_probe.md`
- Source probe id: `bz_phase2_baseline_residual_refinement_probe`
- Shared exact window: `n=1..80`
- Outcome: `hard_wall_low_complexity_baseline_refinement_exhausted`
- Winner family id: `None`

| family | verdict | note |
| --- | --- | --- |
| `support0_same_index` | `fails_after_fit_window` | Fit window solves exactly but the family fails on the larger validation window. |
| `difference_pair` | `fails_after_fit_window` | Fit window solves exactly but the family fails on the larger validation window. |
| `support1_lagged_pair` | `fails_after_fit_window` | Fit window solves exactly but the family fails on the larger validation window. |

## Rationale

All fixed low-complexity baseline-native residual-refinement families either fail after their fit windows or would be ill-posed. The bridge stack remains calibration-only, and this ladder is now exhausted on the exact shared window.

## Next step

Stop autonomous execution and ask the user to choose the next pivot. Do not add richer baseline-side families or change the target object without that decision.

## Bridge boundary

The Zudilin 2002 bridge stack may be used only as calibration to sanity-check bookkeeping conventions and failure modes. It may not redefine the active baseline object or supply hidden identities for it.

## Pivot options

- `richer_baseline_family`
- `different_target_object`
