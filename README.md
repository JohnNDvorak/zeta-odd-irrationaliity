# zeta5-autoresearch

Fresh Codex/operator handoff: see [`CODEX_TRANSITION.md`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/CODEX_TRANSITION.md).

Research code for exact and source-backed experiments around irrationality constructions for `zeta(5)`, centered on the Brown-Zudilin cellular framework.

This repo is not a proof claim. It is a working research environment for:
- exact sequence extraction,
- recurrence obstruction and family surveys,
- source-backed regression anchors,
- dual-hypergeometric coefficient experiments,
- and literature-driven pivot work when the direct exact lane stalls.

## Current Status

The project has two main banked outcomes so far:

1. A large exact-arithmetic exploration of the Brown-Zudilin baseline denominator and dual companion sequences.
2. A phase-2 pivot that freezes the expensive blocked lane and refocuses the repo on proof-relevant decay-side objects.

Current frozen checkpoint:
- baseline dual companion caches are banked through `n=434`
- the exact cleared-window `(1,0,-1,-2)` recurrence family is ruled out through degree `106`
- the blocking step is the final `n=435` exact extension in the old mixed fraction-pair / `mpq` kernel

Current proof-side pivot:
- the totally symmetric linear-form pipeline is the active source-backed decay anchor
- the baseline non-symmetric case still has no repo-local `P_n` or remainder object to ingest honestly
- the repo now carries an explicit phase-2 audit, checkpoint, and decay-readiness bridge

See:
- [data/logs/bz_phase2_dual_companion_checkpoint.md](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_dual_companion_checkpoint.md)
- [data/logs/bz_phase2_baseline_decay_audit_report.md](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_decay_audit_report.md)
- [data/logs/bz_phase2_pivot_report.md](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_pivot_report.md)
- [data/logs/bz_phase2_baseline_decay_bridge_report.md](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs/bz_phase2_baseline_decay_bridge_report.md)

## Repo Layout

- [`src/zeta5_autoresearch`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch): research code
- [`regression`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/regression): regression tests and fixtures
- [`specs`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/specs): seeds, evidence, and survey campaign specs
- [`refs`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/refs): compact local research notes
- [`data/logs`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/logs): generated reports
- [`data/cache`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/data/cache): cached exact sequence data
- [`tools`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/tools): unattended self-drive scripts and prompts

## Most Useful Entry Points

Structural / orchestration:
- [`orchestrator.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/orchestrator.py)
- [`gate0_parse.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/gate0_parse.py)
- [`gate1_filter.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/gate1_filter.py)

Baseline / dual exact work:
- [`bz_q_sequence.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/bz_q_sequence.py)
- [`bz_dual_f7.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/bz_dual_f7.py)
- [`dual_f7_exact_coefficient_cache.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/dual_f7_exact_coefficient_cache.py)
- [`bz_dual_f7_companion_normalization_probe.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/bz_dual_f7_companion_normalization_probe.py)

Phase-2 decay pivot:
- [`decay_probe.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/decay_probe.py)
- [`baseline_decay_audit.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/baseline_decay_audit.py)
- [`baseline_decay_bridge.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/baseline_decay_bridge.py)
- [`bz_symmetric_linear_forms_probe.py`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/src/zeta5_autoresearch/bz_symmetric_linear_forms_probe.py)

## Quick Start

Run the full regression suite:

```bash
cd /Users/john.n.dvorak/Documents/Git/zeta5-autoresearch
uv run pytest
```

Generate the main phase-2 reports:

```bash
uv run python -m zeta5_autoresearch.baseline_decay_audit
uv run python -m zeta5_autoresearch.baseline_decay_bridge
```

Regenerate the totally symmetric decay anchor:

```bash
uv run python -m zeta5_autoresearch.bz_symmetric_linear_forms_probe_cli --max-n 14 --precision 80
```

Run a structural dry run on the baseline seed:

```bash
uv run python -m zeta5_autoresearch.orchestrator specs/baseline_bz_seed.yaml --log --notes "baseline structural dry run"
```

## Self-Drive Loop

The unattended loop scripts live in [`tools`](/Users/john.n.dvorak/Documents/Git/zeta5-autoresearch/tools).

```bash
cd /Users/john.n.dvorak/Documents/Git/zeta5-autoresearch
tools/z5_self_drive_start.sh
tools/z5_self_drive_status.sh
tools/z5_self_drive_stop.sh
```

The loop is currently configured to prefer the phase-2 audit / decay queue over the blocked `n=435` kernel fight.

## Research Guardrails

- Do not treat numerical agreement as certification.
- Do not invent baseline `P_n` or remainder data.
- Keep the totally symmetric and baseline non-symmetric cases separate.
- Prefer primary-source or clearly source-backed objects over speculative derivations.
- Reopen the old `n=435` kernel lane only if a stronger reason emerges than “one more degree.”
