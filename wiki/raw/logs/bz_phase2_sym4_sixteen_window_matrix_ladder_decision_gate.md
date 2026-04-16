# Phase 2 Sym^4-lifted sixteen-window matrix-ladder decision gate

- Gate id: `bz_phase2_sym4_sixteen_window_matrix_ladder_decision_gate`
- Homogeneous source: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_sym4_sixteen_window_matrix_recurrence_screen.md`
- Affine source: `/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_sym4_sixteen_window_affine_matrix_recurrence_screen.md`
- Source probe id: `bz_phase2_sym4_sixteen_window_probe`
- Shared exact window: `n=1..65`
- Outcome: `hard_wall_sym4_sixteen_window_natural_matrix_ladders_exhausted`

## Homogeneous ladder

| side | recurrence order | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- |
| `source` | `1` | `960` | `225` | `inconsistent_mod_prime` | `1009` |
| `target` | `1` | `960` | `225` | `inconsistent_mod_prime` | `1451` |
| `source` | `2` | `945` | `450` | `inconsistent_mod_prime` | `1009` |
| `target` | `2` | `945` | `450` | `inconsistent_mod_prime` | `1451` |
| `source` | `3` | `930` | `675` | `inconsistent_mod_prime` | `1009` |
| `target` | `3` | `930` | `675` | `inconsistent_mod_prime` | `1451` |
| `source` | `4` | `915` | `900` | `inconsistent_mod_prime` | `1009` |
| `target` | `4` | `915` | `900` | `inconsistent_mod_prime` | `1451` |

## Affine ladder

| side | recurrence order | equation count | unknown count | verdict | witness prime |
| --- | --- | --- | --- | --- | --- |
| `source` | `1` | `960` | `240` | `inconsistent_mod_prime` | `1009` |
| `target` | `1` | `960` | `240` | `inconsistent_mod_prime` | `1451` |
| `source` | `2` | `945` | `465` | `inconsistent_mod_prime` | `1009` |
| `target` | `2` | `945` | `465` | `inconsistent_mod_prime` | `1451` |
| `source` | `3` | `930` | `690` | `inconsistent_mod_prime` | `1009` |
| `target` | `3` | `930` | `690` | `inconsistent_mod_prime` | `1451` |

## Rationale

The banked Sym^4-lifted sixteen-window object is the strongest exact paired higher-Schur invariant in the repo, but both natural constant matrix-valued recurrence ladders now fail through the full overdetermined range:

- homogeneous order `4` is still overdetermined, with `900` unknowns against `915` equations, and is inconsistent on both sides
- homogeneous order `5` is underdetermined, with `1125` unknowns against `900` equations
- affine order `3` is overdetermined, with `690` unknowns against `930` equations, and is inconsistent on both sides
- affine order `4` is not overdetermined, with `915` unknowns against `915` equations

## Decision

Do not keep increasing homogeneous or affine matrix recurrence order mechanically on the Sym^4-lifted sixteen-window object. The next order in each ladder is no longer a strict overdetermined obstruction screen, so it would be an interpolation-style search unless a new structural reason changes the family.

## Source boundary

This hard wall does not identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` dual-companion lane. It says only that the natural low-order homogeneous and affine constant-matrix recurrence families do not hold for the banked Sym^4 paired invariant through their overdetermined ranges.

## Pivot options

- `different_structural_family_on_sym4_sixteen_window_lift`
- `different_higher_schur_or_nonlinear_invariant_family_with_new_reason`
- `external_source_backed_identity_or_bridge_not_in_exhausted_classes`
