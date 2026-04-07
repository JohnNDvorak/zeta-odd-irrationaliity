from __future__ import annotations

from itertools import permutations

from .models import AffineFamily


def canonicalize_affine_family(affine_family: AffineFamily) -> tuple[AffineFamily, tuple[int, ...]]:
    u = affine_family.u
    v = affine_family.v
    fixed = (0,)

    best_key: tuple[tuple, tuple] | None = None
    best_u = u
    best_v = v
    best_permutation = tuple(range(8))

    for perm_tail in permutations(range(1, 8)):
        permutation = fixed + perm_tail
        candidate_u = tuple(u[index] for index in permutation)
        candidate_v = tuple(v[index] for index in permutation)
        key = (candidate_u[1:], candidate_v[1:])
        if best_key is None or key < best_key:
            best_key = key
            best_u = candidate_u
            best_v = candidate_v
            best_permutation = permutation

    return AffineFamily(u=best_u, v=best_v), best_permutation
