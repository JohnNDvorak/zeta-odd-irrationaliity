# Phase 2 Sym^4-lifted sixteen-window generalized polynomial matrix follow-up

- Follow-up id: `bz_phase2_sym4_sixteen_window_generalized_polynomial_matrix_followup`
- Source probe id: `bz_phase2_sym4_sixteen_window_probe`
- Shared exact window: `n=1..65`
- Tested primes: `1451, 1009, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493`
- Overall verdict: `generalized_polynomial_target_cases_require_exact_nullspace_followup`

## Case summary

| family | side | recurrence order | polynomial degree | matrix size | equation count | unknown count | case verdict | witness prime |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `homogeneous` | `target` | `1` | `2` | `15` | `960` | `678` | `modular_nullity_persists_on_bounded_prime_set` | `None` |
| `homogeneous` | `target` | `1` | `3` | `15` | `960` | `904` | `modular_nullity_persists_on_bounded_prime_set` | `None` |
| `affine` | `target` | `1` | `2` | `15` | `960` | `723` | `modular_nullity_persists_on_bounded_prime_set` | `None` |

## Prime ranks

| family | recurrence order | polynomial degree | prime | rank | nullity | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `homogeneous` | `1` | `2` | `1451` | `528` | `150` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `2` | `1009` | `None` | `None` | `skipped_denominator_singular_mod_prime` |
| `homogeneous` | `1` | `2` | `1453` | `528` | `150` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `2` | `1459` | `None` | `None` | `skipped_denominator_singular_mod_prime` |
| `homogeneous` | `1` | `2` | `1471` | `528` | `150` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `2` | `1481` | `528` | `150` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `2` | `1483` | `528` | `150` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `2` | `1487` | `528` | `150` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `2` | `1489` | `528` | `150` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `2` | `1493` | `528` | `150` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `3` | `1451` | `544` | `360` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `3` | `1009` | `None` | `None` | `skipped_denominator_singular_mod_prime` |
| `homogeneous` | `1` | `3` | `1453` | `544` | `360` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `3` | `1459` | `None` | `None` | `skipped_denominator_singular_mod_prime` |
| `homogeneous` | `1` | `3` | `1471` | `544` | `360` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `3` | `1481` | `544` | `360` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `3` | `1483` | `544` | `360` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `3` | `1487` | `544` | `360` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `3` | `1489` | `544` | `360` | `rank_deficient_mod_prime` |
| `homogeneous` | `1` | `3` | `1493` | `544` | `360` | `rank_deficient_mod_prime` |
| `affine` | `1` | `2` | `1451` | `573` | `150` | `rank_deficient_mod_prime` |
| `affine` | `1` | `2` | `1009` | `None` | `None` | `skipped_denominator_singular_mod_prime` |
| `affine` | `1` | `2` | `1453` | `573` | `150` | `rank_deficient_mod_prime` |
| `affine` | `1` | `2` | `1459` | `None` | `None` | `skipped_denominator_singular_mod_prime` |
| `affine` | `1` | `2` | `1471` | `573` | `150` | `rank_deficient_mod_prime` |
| `affine` | `1` | `2` | `1481` | `573` | `150` | `rank_deficient_mod_prime` |
| `affine` | `1` | `2` | `1483` | `573` | `150` | `rank_deficient_mod_prime` |
| `affine` | `1` | `2` | `1487` | `573` | `150` | `rank_deficient_mod_prime` |
| `affine` | `1` | `2` | `1489` | `573` | `150` | `rank_deficient_mod_prime` |
| `affine` | `1` | `2` | `1493` | `573` | `150` | `rank_deficient_mod_prime` |

## Interpretation

This bounded follow-up revisits only the three target-side generalized polynomial matrix cases left open by the first screen. A full column rank over any good prime would obstruct an exact rational recurrence in that case. Persistent modular nullity across this finite prime set is a lead for exact nullspace extraction, not a proof of a rational recurrence.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^4-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Extract and certify exact nullspace data for the persistent target-side generalized polynomial matrix cases before trying another recurrence family.
