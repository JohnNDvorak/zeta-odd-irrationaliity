# zeta5-autoresearch

Conservative research scaffold for improved rational approximations to `zeta(5)`.

This repository implements the Python-only structural core described by the Brown–Zudilin engine plan:

- exact candidate parsing,
- exact `a <-> s` translation,
- joint `(u, v)` canonicalization under `S7`,
- all-`n` parity checks,
- convergence filtering for the baseline cellular family,
- `routing_hash`,
- seed and fixture storage,
- and append-only result logging.

The repository does **not** yet implement Gate 2 / Gate 3 scoring or certification. Those modules are stubbed deliberately until a validated CAS backend is available.

## Status

Implemented now:

- repo scaffold,
- baseline Brown–Zudilin seed,
- structural parser and Gate 0 / Gate 1,
- normalized sequence-identity hashing interfaces for exact recurrence or exact term data,
- sequence-evidence ingestion with seeded Brown–Zudilin baseline `Q_n` evidence,
- a published totally symmetric recurrence-backed anchor with a verified `sequence_hash`,
- an exact totally symmetric `Q_n / \hat P_n / P_n` linear-form probe with worthiness estimates,
- a dual very-well-poised `F_7(b)` evaluator and numeric probe for the totally symmetric and baseline Brown-Zudilin families,
- an exact dual `F_7(b)` coefficient extractor from partial fractions of the displayed summand formula,
- an exact fast extractor for the dual `zeta(5)` coefficient sequence with provisional sequence hashes,
- exact cached baseline/symmetric companion sequences for the dual `zeta(3)` coefficient and rational constant term,
- a published report for the missing exact dual companion sequences on the baseline Brown-Zudilin family,
- an exact finite-window recurrence report on the baseline dual companion sequences,
- a window-normalized exact recurrence report on cleared baseline dual companion sequences,
- baseline cache, growth calibration, and first modular recurrence certificates for the exact dual `zeta(5)` coefficient sequence,
- baseline `Q_n` growth calibration against the published `C1` constant,
- exact recurrence-degree mining for the baseline `Q_n` sequence,
- modular rank certificates that can rule out baseline recurrence degrees over `Q`,
- persistent caching of exact baseline `Q_n` terms for long scans,
- YAML-driven modular family surveys over competing recurrence ansatze,
- YAML-driven modular shift-catalog surveys over normalized asymmetric/non-consecutive supports,
- fixed-sequence campaign expansion for BZ representation/certificate variants,
- results-store interface,
- candidate snapshot archiving and structural dry-run logging,
- mode separation stubs,
- active unit tests for exact arithmetic and filtering.

Intentionally deferred:

- recurrence derivation and exact `P_n` / remainder generation,
- BZ numeric regression reproduction,
- Mathematica / CAS integration.

## Quickstart

```bash
cd /Users/john.n.dvorak/Documents/Git/zeta5-autoresearch
uv run pytest
uv run python -m zeta5_autoresearch.orchestrator specs/baseline_bz_seed.yaml
uv run python -m zeta5_autoresearch.orchestrator specs/baseline_bz_seed.yaml --log --mode "Mode A-fast" --notes "baseline structural dry run"
uv run python -m zeta5_autoresearch.orchestrator specs/totally_symmetric_bz_seed.yaml --log --notes "verified totally symmetric recurrence anchor"
uv run python -m zeta5_autoresearch.campaign_cli specs/campaigns/bz_fixed_sequence_campaign.yaml
uv run python -m zeta5_autoresearch.campaign_report_cli specs/campaigns/bz_fixed_sequence_campaign.yaml
uv run python -m zeta5_autoresearch.bz_growth_probe_cli --max-n 20
uv run python -m zeta5_autoresearch.bz_symmetric_recurrence_probe_cli --max-n 10
uv run python -m zeta5_autoresearch.bz_symmetric_linear_forms_probe_cli --max-n 12 --precision 80
uv run python -m zeta5_autoresearch.bz_dual_f7_probe_cli --precision 120 --pslq-precision 180
uv run python -m zeta5_autoresearch.bz_dual_f7_exact_probe_cli --precision 120
uv run python -m zeta5_autoresearch.bz_dual_f7_companion_probe_cli --baseline-term-count 6 --symmetric-term-count 4
uv run python -m zeta5_autoresearch.bz_dual_f7_companion_recurrence_probe_cli --max-n 12 --degree-max 2
uv run python -m zeta5_autoresearch.bz_dual_f7_companion_normalization_probe_cli --max-n 20 --degree-max 4
uv run python -m zeta5_autoresearch.bz_dual_f7_zeta5_probe_cli
uv run python -m zeta5_autoresearch.bz_dual_f7_zeta5_growth_probe_cli --max-n 20
uv run python -m zeta5_autoresearch.bz_dual_f7_zeta5_modular_recurrence_probe_cli --max-n 30 --degrees 0 1 2 3 4 5 6
uv run python -m zeta5_autoresearch.baseline_recurrence_probe_cli --max-n 34 --degree-max 8
uv run python -m zeta5_autoresearch.baseline_modular_recurrence_probe_cli --max-n 38 --degrees 8 9
uv run python -m zeta5_autoresearch.baseline_family_survey_cli specs/campaigns/bz_baseline_modular_family_survey.yaml
uv run python -m zeta5_autoresearch.baseline_shift_catalog_survey_cli specs/campaigns/bz_baseline_shift_catalog_survey.yaml
```

## Overnight Loop

Unattended self-drive scripts live in [`tools/`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/tools):

```bash
cd /Users/john.n.dvorak/Documents/Git/zeta5-autoresearch
tools/z5_self_drive_start.sh
tools/z5_self_drive_status.sh
tools/z5_self_drive_stop.sh
```

Default state directory:

```bash
~/.codex/self_drives/zeta5_autoresearch
```

## Research policy

- Do not run open search until regressions are real and passing.
- Do not treat numerical agreement as certification.
- Do not compute `certificate_hash` before `sequence_hash`.
- Prefer fixed-sequence certificate mining before broad parameter search.
