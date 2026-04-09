# Phase 2 symmetric-dual to baseline-dual chart transfer decision gate

- Gate id: `bz_phase2_symmetric_dual_baseline_chart_transfer_decision_gate`
- Source probe: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_symmetric_dual_baseline_chart_transfer_family_probe.md`
- Source probe id: `bz_phase2_symmetric_dual_baseline_chart_transfer_family_probe`
- Shared exact window: `n=1..76`
- Outcome: `hard_wall_chart_transfer_support_ladder_is_interpolation_only`

| family | verdict | note |
| --- | --- | --- |
| `constant_chart_map` | `fails_after_fit_window` | This bounded chart-profile transfer family fails after its fit window. |
| `difference_chart_map` | `fails_after_fit_window` | This bounded chart-profile transfer family fails after its fit window. |
| `support1_chart_map` | `fails_after_fit_window` | This bounded chart-profile transfer family fails after its fit window. |
| `support2_chart_map` | `fails_after_fit_window` | This bounded chart-profile transfer family fails after its fit window. |
| `support3_chart_map` | `fails_after_fit_window` | This bounded chart-profile transfer family fails after its fit window. |
| `support4_chart_map` | `fails_after_fit_window` | This bounded chart-profile transfer family fails after its fit window. |

## Rationale

The richer chart-profile ladder is interpolation-only: it improves the first mismatch frontier, but only by extending the fit window. Constant, difference, and support-1 through support-4 all fail immediately after their exact fit blocks.

## Next step

Stop autonomous execution and ask for the next pivot.

## Source boundary

A chart-profile transfer success would still be a bounded relation on `n=1..76`, not a proof of common recurrence or packet equivalence.

## Pivot options

- `richer_chart_transfer_family`
- `different_object_class`
