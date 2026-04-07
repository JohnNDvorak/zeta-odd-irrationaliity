# program.md — ζ(5) autoresearch program for Codex

You are operating inside a repo whose purpose is to build and then run a discovery engine for better rational approximations to ζ(5).

Your priorities are ordered.

## 1. First priority: build a trustworthy engine
Do not start open search until the regression suite passes.

You must first implement:
- candidate spec parsing,
- exact `a <-> s` translation,
- joint `(u, v)` canonicalization under `S₇`,
- parity and convergence checks,
- `routing_hash`,
- the baseline Brown–Zudilin seed,
- the results store,
- and the regression harness.

## 2. Ground truth
Use these facts as fixed:
- Brown's `N=8` census gives 17 convergent configurations and 13 distinct families.
- `8π8` is the unique odd family giving `{1, ζ(3), ζ(5)}` only.
- `8π8∨` is the dual family giving `{1, ζ(2), 2ζ(5)+4ζ(3)ζ(2)}`.
- Brown–Zudilin's published baseline uses the `8π8∨` family and achieves
  `γ = 0.86597135...` with
  `C₀ = -31.55296934...`,
  `C₁ = 85.08768883...`,
  `C₂ = 49.60574814...`.
- The bottleneck is `C₂`, not `C₀`.
- Brown–Zudilin explicitly indicate that further gains may come from different integral representations with their own arithmetic.

## 3. Identity discipline
Use three hashes:
- `routing_hash` for spec-level queue identity before recurrence derivation,
- `sequence_hash` for semantic sequence identity,
- `certificate_hash` for denominator-argument identity.

Do not compute `certificate_hash` before `sequence_hash`.
Do not reuse `C₀, C₁` unless sequence identity is verified.

## 4. Modes
Use three modes:
- `Mode A-fast`: fixed sequence, explicit equality witness, compute `C₂` only.
- `Mode A-slow`: fixed intended sequence, no trusted witness, verify sequence first, then compute `C₂`.
- `Mode B`: new affine family / configuration / extraction, compute everything.

## 5. Gate discipline
Gate 1 must stay cheap and safe.
Gate 2 estimates or computes `C₀`, `C₁`, `C₂`, `γ`, `M_proof`.
Gate 3 is certification / high-confidence verification only.

Do not treat numerical agreement as a certificate.

## 6. Regression targets
You are not ready for open search until you can:
1. reproduce the BZ main example,
2. reproduce the BZ arithmetic-loss improvement example,
3. recover Brown's `N=8` census structure,
4. pass the Tosi regression checks.

## 7. First real campaign
After the regressions pass, your first campaign is **not** broad parameter search.

It is:
- lock the Brown–Zudilin sequence,
- vary the representation and certificate,
- mine for smaller `C₂`.

This is the first place where the literature says improvement is most likely.

## 8. Success thresholds
Treat the following as distinct:
- `γ >= 0.867` certified,
- `ΔC₂ >= 0.10` certified.

They are not equivalent.
A tiny increase above `0.866` is not enough.

## 9. Logging and honesty
For every candidate, record:
- mode,
- hashes,
- certification status,
- whether improvement came from `C₀/C₁` or from `C₂`,
- and uncertainty intervals where relevant.

Mark every result as one of:
- `certified_true`
- `certified_safe_bound`
- `uncertified_numeric`
- `invalidated`

Only `certified_true` counts as a publishable win.

## 10. First tasks now
Right now, build the repo scaffold and implement the pure-Python structural core.
Do not jump ahead.
