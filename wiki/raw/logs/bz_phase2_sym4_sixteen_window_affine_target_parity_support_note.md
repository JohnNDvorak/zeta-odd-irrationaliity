# Phase 2 Sym^4-lifted affine target parity support note

- Note id: `bz_phase2_sym4_sixteen_window_affine_target_parity_support_note`
- Object: `Sym^4` sixteen-window target sequence
- Shared exact window: `n=1..65`
- Related fingerprint: `bz_phase2_sym4_sixteen_window_affine_target_nullspace_fingerprint`
- Verdict: `affine_target_nullspace_has_parity_sparse_support_structure`

## Support pattern

The target sequence cache has a simple coordinate-support pattern:

- coordinate `0` is nonzero for all `65` target windows
- coordinates `1..14` are nonzero exactly on odd indices `n=1,3,5,...,65`
- coordinates `1..14` vanish on every even index

Equivalently, for the order-1 target-side recurrence rows, the history vector at `n-1` has coordinates `1..14` active only when the target index `n` is even.

## Relation to the affine target fingerprint

The affine target `(order, degree) = (1, 2)` nullspace fingerprint found stable free columns

`M[2,0,i,j]` for target index `i=0..14` and source index `j=5..14`.

Those source coordinates are not globally zero. They are parity-sparse: active on odd history indices and zero on even history indices. Therefore the `150`-dimensional affine target nullspace is not explained by a trivial unused-coordinate column block.

## Interpretation

The corrected affine target nullspace is large and structured. The visible free-column block should be treated as a parity/block-structure lead, not as immediate evidence of a small recurrence.

## Recommendation

Before attempting CRT/rational reconstruction, run a bounded parity/block classification of the affine target nullspace. In particular, test whether quotienting or freezing the degree-2 matrix block with source indices `5..14` collapses the nullspace, and test whether the even-target and odd-target row blocks behave differently.
