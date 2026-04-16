# Phase 2 Sym^4-lifted affine target block quotient screen

- Screen id: `bz_phase2_sym4_sixteen_window_affine_target_block_quotient_screen`
- Shared exact window: `n=1..65`
- Case: `affine` `target` `(order, degree) = (1, 2)`
- Equations / full unknowns: `960` / `723`
- Removed columns: `150`
- Quotient unknowns: `573`
- Removed pattern: `M[2,0,i,j] for target index i=0..14 and source index j=5..14`
- Tested primes: `1451, 1453, 1471, 1481, 1483, 1487, 1489, 1493`
- Overall verdict: `affine_target_nullspace_collapses_after_degree2_source_tail_block_quotient`

## Prime results

| prime | quotient unknowns | quotient rank | quotient nullity | verdict |
| --- | --- | --- | --- | --- |
| `1451` | `573` | `573` | `0` | `quotient_full_column_rank_mod_prime` |
| `1453` | `573` | `573` | `0` | `quotient_full_column_rank_mod_prime` |
| `1471` | `573` | `573` | `0` | `quotient_full_column_rank_mod_prime` |
| `1481` | `573` | `573` | `0` | `quotient_full_column_rank_mod_prime` |
| `1483` | `573` | `573` | `0` | `quotient_full_column_rank_mod_prime` |
| `1487` | `573` | `573` | `0` | `quotient_full_column_rank_mod_prime` |
| `1489` | `573` | `573` | `0` | `quotient_full_column_rank_mod_prime` |
| `1493` | `573` | `573` | `0` | `quotient_full_column_rank_mod_prime` |

## Interpretation

The affine target `(order, degree) = (1, 2)` case has a stable `150`-dimensional modular nullspace before quotienting. Removing exactly the stable free degree-2 matrix block leaves a quotient system with full column rank at every tested good prime.

This does not prove an exact rational statement, but it strongly indicates that the affine target modular nullspace is accounted for by the visible parity-sparse block freedom rather than by a smaller hidden recurrence-bearing subspace.

## Recommendation

Treat the affine target `(order, degree) = (1, 2)` nullspace as explained by the visible parity-sparse degree-2 matrix block, and shift classification to the homogeneous target cases.
