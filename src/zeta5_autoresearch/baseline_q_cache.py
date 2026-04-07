from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from .bz_q_sequence import (
    baseline_a_vector,
    build_modular_binomial_table_for_a,
    compute_q_term_from_a,
    compute_q_term_from_a_mod,
)
from .config import CACHE_DIR

BASELINE_Q_CACHE_PATH = CACHE_DIR / "bz_baseline_q_terms.json"


def get_cached_baseline_q_terms(
    max_n: int,
    *,
    cache_path: str | Path = BASELINE_Q_CACHE_PATH,
) -> tuple[int, ...]:
    if max_n < 0:
        raise ValueError("max_n must be nonnegative")

    path = Path(cache_path)
    cached_terms = _load_cache(path)
    if len(cached_terms) > max_n:
        return cached_terms[: max_n + 1]

    a = baseline_a_vector()
    start_index = len(cached_terms)
    extended = list(cached_terms)
    for n in range(start_index, max_n + 1):
        extended.append(compute_q_term_from_a(a, n))
    _write_cache(path, tuple(extended))
    return tuple(extended)


def get_cached_baseline_q_terms_as_fractions(
    max_n: int,
    *,
    cache_path: str | Path = BASELINE_Q_CACHE_PATH,
) -> tuple[Fraction, ...]:
    return tuple(Fraction(value) for value in get_cached_baseline_q_terms(max_n, cache_path=cache_path))


def get_cached_baseline_q_terms_mod_prime(
    max_n: int,
    *,
    modulus: int,
    cache_path: str | Path | None = None,
) -> tuple[int, ...]:
    if max_n < 0:
        raise ValueError("max_n must be nonnegative")

    path = _default_mod_cache_path(modulus) if cache_path is None else Path(cache_path)
    cached_terms = _load_mod_cache(path, modulus)
    if len(cached_terms) > max_n:
        return cached_terms[: max_n + 1]

    a = baseline_a_vector()
    table = build_modular_binomial_table_for_a(a, max_n, modulus=modulus)
    extended = list(cached_terms)
    for n in range(len(cached_terms), max_n + 1):
        extended.append(compute_q_term_from_a_mod(a, n, modulus=modulus, table=table))
    _write_mod_cache(path, tuple(extended), modulus)
    return tuple(extended)


def _load_cache(path: Path) -> tuple[int, ...]:
    if not path.exists():
        return ()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"invalid baseline q cache format in {path}")
    raw_terms = payload.get("terms")
    if not isinstance(raw_terms, list):
        raise ValueError(f"baseline q cache must contain a 'terms' list in {path}")
    return tuple(int(value) for value in raw_terms)


def _write_cache(path: Path, terms: tuple[int, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "sequence": "bz_baseline_q_terms",
        "max_n": len(terms) - 1,
        "terms": [str(value) for value in terms],
    }
    path.write_text(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True), encoding="utf-8")


def _load_mod_cache(path: Path, modulus: int) -> tuple[int, ...]:
    if not path.exists():
        return ()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"invalid baseline modular q cache format in {path}")
    if int(payload.get("modulus", -1)) != modulus:
        raise ValueError(f"baseline modular q cache modulus mismatch in {path}")
    raw_terms = payload.get("terms")
    if not isinstance(raw_terms, list):
        raise ValueError(f"baseline modular q cache must contain a 'terms' list in {path}")
    return tuple(int(value) for value in raw_terms)


def _write_mod_cache(path: Path, terms: tuple[int, ...], modulus: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "modulus": modulus,
        "sequence": f"bz_baseline_q_terms_mod_{modulus}",
        "max_n": len(terms) - 1,
        "terms": terms,
    }
    path.write_text(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True), encoding="utf-8")


def _default_mod_cache_path(modulus: int) -> Path:
    return CACHE_DIR / f"bz_baseline_q_terms_mod_{modulus}.json"
