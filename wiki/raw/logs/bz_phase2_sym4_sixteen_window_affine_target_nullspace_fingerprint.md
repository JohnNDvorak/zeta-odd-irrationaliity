# Phase 2 Sym^4-lifted affine target nullspace fingerprint

- Fingerprint id: `bz_phase2_sym4_sixteen_window_affine_target_nullspace_fingerprint`
- Shared exact window: `n=1..65`
- Case: `affine` `target` `(order, degree) = (1, 2)`
- Matrix size: `15`
- Equations / unknowns: `960` / `723`
- Tested primes: `1451, 1453, 1471, 1481, 1483, 1487, 1489, 1493`
- Minimum good-prime nullity: `150`
- Minimum-nullity primes: `1451, 1453, 1471, 1481, 1483, 1487, 1489, 1493`
- Overall verdict: `affine_target_modular_nullspace_has_stable_free_column_profile`

## Prime fingerprints

| prime | rank | nullity | pivot count | free columns | nullspace rows | nullspace row rank | support range | verified | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1451` | `573` | `150` | `573` | `488..497, 503..512, 518..527, 533..542, 548..557, 563..572, 578..587, 593..602, 608..617, 623..632, 638..647, 653..662, 668..677, 683..692, 698..707` | `150` | `150` | `32..33` | `True` | `verified_nullspace_basis_mod_prime` |
| `1453` | `573` | `150` | `573` | `488..497, 503..512, 518..527, 533..542, 548..557, 563..572, 578..587, 593..602, 608..617, 623..632, 638..647, 653..662, 668..677, 683..692, 698..707` | `150` | `150` | `33..33` | `True` | `verified_nullspace_basis_mod_prime` |
| `1471` | `573` | `150` | `573` | `488..497, 503..512, 518..527, 533..542, 548..557, 563..572, 578..587, 593..602, 608..617, 623..632, 638..647, 653..662, 668..677, 683..692, 698..707` | `150` | `150` | `33..33` | `True` | `verified_nullspace_basis_mod_prime` |
| `1481` | `573` | `150` | `573` | `488..497, 503..512, 518..527, 533..542, 548..557, 563..572, 578..587, 593..602, 608..617, 623..632, 638..647, 653..662, 668..677, 683..692, 698..707` | `150` | `150` | `33..33` | `True` | `verified_nullspace_basis_mod_prime` |
| `1483` | `573` | `150` | `573` | `488..497, 503..512, 518..527, 533..542, 548..557, 563..572, 578..587, 593..602, 608..617, 623..632, 638..647, 653..662, 668..677, 683..692, 698..707` | `150` | `150` | `33..33` | `True` | `verified_nullspace_basis_mod_prime` |
| `1487` | `573` | `150` | `573` | `488..497, 503..512, 518..527, 533..542, 548..557, 563..572, 578..587, 593..602, 608..617, 623..632, 638..647, 653..662, 668..677, 683..692, 698..707` | `150` | `150` | `32..33` | `True` | `verified_nullspace_basis_mod_prime` |
| `1489` | `573` | `150` | `573` | `488..497, 503..512, 518..527, 533..542, 548..557, 563..572, 578..587, 593..602, 608..617, 623..632, 638..647, 653..662, 668..677, 683..692, 698..707` | `150` | `150` | `33..33` | `True` | `verified_nullspace_basis_mod_prime` |
| `1493` | `573` | `150` | `573` | `488..497, 503..512, 518..527, 533..542, 548..557, 563..572, 578..587, 593..602, 608..617, 623..632, 638..647, 653..662, 668..677, 683..692, 698..707` | `150` | `150` | `33..33` | `True` | `verified_nullspace_basis_mod_prime` |

## Stable free columns

- Count: `150`
- Column runs: `488..497, 503..512, 518..527, 533..542, 548..557, 563..572, 578..587, 593..602, 608..617, 623..632, 638..647, 653..662, 668..677, 683..692, 698..707`
- Label pattern: `M[2,0,i,j]` for target index `i=0..14` and source index `j=5..14`.
- The full column and label list is preserved in the JSON cache artifact.

## Hashes

| prime | pivot columns hash | DomainMatrix nullspace hash |
| --- | --- | --- |
| `1451` | `3eeca89c66e1a58cdc21b533992615bbe8df7248a5b1367d08fb3c2afe707066` | `1c58df7b2127b93fb33cb8653ac83747c2e4f5c354c1b8403751acccd61b9e77` |
| `1453` | `3eeca89c66e1a58cdc21b533992615bbe8df7248a5b1367d08fb3c2afe707066` | `7203ae5cb068104299b81a4799d22441fda888888da1b6a39644bf9f4c163a7a` |
| `1471` | `3eeca89c66e1a58cdc21b533992615bbe8df7248a5b1367d08fb3c2afe707066` | `6e56bc5cfc13bb9bd7fe94d95b20fc751d7f0f9f01134d7703c4032dc7cf540e` |
| `1481` | `3eeca89c66e1a58cdc21b533992615bbe8df7248a5b1367d08fb3c2afe707066` | `945a892f1c1523478d523a203968b2b03115cae89950084a6a151e7c3dc30b85` |
| `1483` | `3eeca89c66e1a58cdc21b533992615bbe8df7248a5b1367d08fb3c2afe707066` | `3eccfae9f4a7ee005bed0319befd4d48fb9ddd4d8735e96c6e5c416934d071d4` |
| `1487` | `3eeca89c66e1a58cdc21b533992615bbe8df7248a5b1367d08fb3c2afe707066` | `475daac8ce23aec440b662601b3cda33d28163a3c8d27b4b7773642a9a441ce5` |
| `1489` | `3eeca89c66e1a58cdc21b533992615bbe8df7248a5b1367d08fb3c2afe707066` | `67e87a09896160aa0b465280932c154aa7fe1dd346a55f01b6fe52c345ef9387` |
| `1493` | `3eeca89c66e1a58cdc21b533992615bbe8df7248a5b1367d08fb3c2afe707066` | `851d0f6962501d57f7d58ad2ce84962476b26d856109eb12f50677466dc7ee3b` |

## Interpretation

This is a modular nullspace fingerprint for the smallest persistent generalized target-side case. It does not certify an exact rational recurrence. Its purpose is to identify whether the modular nullspaces have a stable shape suitable for a separately verified canonical modular basis, CRT/rational reconstruction, and exact residual verification.

## Source boundary

A success on this object would still be a bounded exact transfer statement on the shared Sym^4-lifted invariant. It would not by itself identify a baseline `P_n`, prove a common recurrence, or reopen the frozen `n=435` lane.

## Recommendation

Build a verified canonical modular basis from the stable pivot/free-column profile, then attempt CRT/rational reconstruction and exact residual verification for affine target `(order, degree) = (1, 2)`.
