# Phase 2 baseline full-packet object spec

- Spec id: `bz_phase2_baseline_full_packet_object_spec`
- Baseline seed: `a=(8,16,10,15,12,16,18,13)`
- Source packet spec: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_projection_target_spec.md`
- Source packet id: `baseline_dual_f7_exact_coefficient_packet`
- Object label: `Baseline full coefficient packet object`
- Object kind: `baseline_side_exact_full_coefficient_packet`

## Object semantics

The active baseline-side object is the full exact coefficient packet `(constant, zeta(3), zeta(5))` on the shared exact window. No channel is demoted to residual at object-definition time.

## Rationale

Both pair-object tranches hit hard walls. The next honest packet-level move is to keep the full coefficient packet active and treat pairwise compression as a bounded experiment rather than choosing a privileged pair up front.

## Components

| component | role | max verified index | exact status |
| --- | --- | --- | --- |
| `constant` | exact rational constant channel retained in the active full packet | `434` | `exact` |
| `zeta3` | exact zeta(3) channel retained in the active full packet | `434` | `exact` |
| `zeta5` | exact zeta(5) channel retained in the active full packet | `80` | `exact` |

## Component notes

- `constant`: This remains exact far beyond the shared window and is kept active to avoid premature demotion.
- `zeta3`: This remains exact far beyond the shared window and is kept active as part of the odd-weight content.
- `zeta5`: This remains the shortest verified frontier and caps the shared exact window at n=1..80.

## Bridge boundary

The Zudilin 2002 bridge stack remains calibration-only. It may not redefine the packet or choose a preferred compression route.

## Non-claims

- This spec does not claim that the full packet is already a baseline decay object.
- This spec does not claim any published baseline P_n or remainder sequence has been extracted.
- This spec does not privilege one pairwise compression route before exact testing.

## Recommended next step

Hash and probe the full packet first, then run one bounded pairwise compression layer across all three residual orientations.
