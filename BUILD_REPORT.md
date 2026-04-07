# Build Report

Implemented in this first pass:

- repository scaffold and packaging,
- baseline Brown–Zudilin seed and regression fixtures,
- exact candidate parser with rational normalization,
- exact `a <-> s` translation,
- joint `(u, v)` canonicalization under `S7`,
- all-`n` parity checks,
- convergence filtering for the baseline cellular family,
- `routing_hash`,
- normalized sequence-identity hashing interfaces,
- sequence-evidence ingestion for published Brown-Zudilin exact coefficient data,
- fixed-sequence campaign expansion for representation mining,
- fixed-sequence campaign markdown reporting,
- append-only TSV results store,
- candidate snapshot archiving plus structural dry-run logging,
- explicit Gate 2 / Gate 3 mode stubs.

Blocked on later CAS integration:

- numeric reproduction of the Brown–Zudilin constants,
- arithmetic-loss reproduction,
- Brown `N=8` census recovery,
- Tosi regression checks,
- recurrence derivation / exact term generation,
- Gate 2 scoring and Gate 3 certification.

Current command surface:

```bash
uv run pytest
uv run python -m zeta5_autoresearch.orchestrator specs/baseline_bz_seed.yaml
uv run python -m zeta5_autoresearch.orchestrator specs/baseline_bz_seed.yaml --log --mode "Mode A-fast"
```
