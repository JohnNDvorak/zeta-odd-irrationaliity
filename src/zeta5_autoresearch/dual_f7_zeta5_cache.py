from __future__ import annotations

import json
from pathlib import Path

from .bz_dual_f7 import compute_f7_zeta5_term_from_a
from .bz_q_sequence import baseline_a_vector, totally_symmetric_a_vector
from .config import CACHE_DIR

BASELINE_DUAL_F7_ZETA5_CACHE_PATH = CACHE_DIR / "bz_baseline_dual_f7_zeta5_terms.json"
SYMMETRIC_DUAL_F7_ZETA5_CACHE_PATH = CACHE_DIR / "bz_totally_symmetric_dual_f7_zeta5_terms.json"


def get_cached_baseline_dual_f7_zeta5_terms(
    max_n: int,
    *,
    cache_path: str | Path = BASELINE_DUAL_F7_ZETA5_CACHE_PATH,
) -> tuple[int, ...]:
    return _get_cached_dual_f7_zeta5_terms(baseline_a_vector(), max_n=max_n, cache_path=cache_path, sequence_name="bz_baseline_dual_f7_zeta5_terms")


def get_cached_symmetric_dual_f7_zeta5_terms(
    max_n: int,
    *,
    cache_path: str | Path = SYMMETRIC_DUAL_F7_ZETA5_CACHE_PATH,
) -> tuple[int, ...]:
    return _get_cached_dual_f7_zeta5_terms(
        totally_symmetric_a_vector(),
        max_n=max_n,
        cache_path=cache_path,
        sequence_name="bz_totally_symmetric_dual_f7_zeta5_terms",
    )


def _get_cached_dual_f7_zeta5_terms(
    a: tuple[int, ...],
    *,
    max_n: int,
    cache_path: str | Path,
    sequence_name: str,
) -> tuple[int, ...]:
    if max_n <= 0:
        raise ValueError("max_n must be positive")

    path = Path(cache_path)
    cached_terms = _load_cache(path, sequence_name=sequence_name)
    if len(cached_terms) >= max_n:
        return cached_terms[:max_n]

    extended = list(cached_terms)
    for n in range(len(cached_terms) + 1, max_n + 1):
        extended.append(compute_f7_zeta5_term_from_a(a, n))
    _write_cache(path, sequence_name=sequence_name, terms=tuple(extended))
    return tuple(extended)


def _load_cache(path: Path, *, sequence_name: str) -> tuple[int, ...]:
    if not path.exists():
        return ()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"invalid dual f7 zeta(5) cache format in {path}")
    if payload.get("sequence") != sequence_name:
        raise ValueError(f"dual f7 zeta(5) cache sequence mismatch in {path}")
    raw_terms = payload.get("terms")
    if not isinstance(raw_terms, list):
        raise ValueError(f"dual f7 zeta(5) cache must contain a 'terms' list in {path}")
    return tuple(int(value) for value in raw_terms)


def _write_cache(path: Path, *, sequence_name: str, terms: tuple[int, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "sequence": sequence_name,
        "max_n": len(terms),
        "terms": [str(value) for value in terms],
    }
    path.write_text(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True), encoding="utf-8")
