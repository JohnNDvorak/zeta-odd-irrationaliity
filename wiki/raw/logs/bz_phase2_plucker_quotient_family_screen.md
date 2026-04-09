# Phase 2 Plucker quotient family screen

- Base invariant family: `normalized_plucker_window_invariant`
- Source family: `totally_symmetric_dual_f7_packet`
- Target family: `baseline_dual_f7_packet`
- Shared exact window: `n=1..76`

## Screened quotient objects

### 1. Fixed-anchor projective quotient

Use the stable nonzero Plucker coordinate `124` as a global anchor and divide the remaining eight
non-pivot Plucker coordinates by `124`.

Bounded ladder:

| family | first mismatch after fit |
| --- | --- |
| `constant_projective_quotient_map` | `9` |
| `difference_projective_quotient_map` | `10` |
| `support1_projective_quotient_map` | `18` |
| `support2_projective_quotient_map` | `27` |

This is weaker than the full normalized Plucker invariant, whose ladder began at `10, 11, 20, 30, 40`.

### 2. Small canonical cross-ratio vector

Use the exact cross-ratio style vector

- `(125 * 234) / (124 * 235)`
- `(125 * 134) / (124 * 135)`
- `(135 * 234) / (134 * 235)`
- `(145 * 234) / (124 * 245)`

Bounded ladder:

| family | first mismatch after fit |
| --- | --- |
| `constant_cross_ratio_map` | `5` |
| `difference_cross_ratio_map` | `6` |
| `support1_cross_ratio_map` | `10` |
| `support2_cross_ratio_map` | `15` |

This is strictly weaker than both the fixed-anchor projective quotient and the full normalized Plucker invariant.

## Additional recurrence-profile check

As a follow-up, the local-annihilator recurrence profile of the full normalized Plucker sequence was screened at the
cheap end of its ladder:

| family | first mismatch after fit |
| --- | --- |
| `constant_plucker_profile_map` | `10` |
| `difference_plucker_profile_map` | `11` |

That matches the direct normalized Plucker transfer at the low-complexity end rather than improving it.

## Verdict

The projective/cross-ratio quotient lane is exhausted as a promising extension of the normalized Plucker family:

- fixed-anchor projective quotients are weaker than the full normalized Plucker vector
- simple cross-ratio vectors are weaker still
- recurrence-profile work on the normalized Plucker sequence does not improve the low-complexity frontier at its cheap end

## Recommendation

Stop the Grassmannian quotient family here.

The next object class should leave the current quotient/invariant family rather than adding more quotient depth.
A plausible next move would be a genuinely different nonlinear recurrence object built from wider window geometry, not
another Plucker-coordinate quotient or support-depth escalation.
