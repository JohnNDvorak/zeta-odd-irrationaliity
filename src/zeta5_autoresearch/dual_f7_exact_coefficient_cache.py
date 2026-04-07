from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from .bz_dual_f7 import (
    DUAL_F7_COMPONENTS,
    compute_f7_exact_component_term_from_a,
    dual_b_vector_from_a,
    extract_f7_linear_form,
    scale_b_vector,
)
from .bz_q_sequence import baseline_a_vector, totally_symmetric_a_vector
from .config import CACHE_DIR
from .models import fraction_from_scalar, fraction_to_canonical_string

BASELINE_DUAL_F7_CONSTANT_CACHE_PATH = CACHE_DIR / "bz_baseline_dual_f7_constant_terms.json"
BASELINE_DUAL_F7_ZETA3_CACHE_PATH = CACHE_DIR / "bz_baseline_dual_f7_zeta3_terms.json"
SYMMETRIC_DUAL_F7_CONSTANT_CACHE_PATH = CACHE_DIR / "bz_totally_symmetric_dual_f7_constant_terms.json"
SYMMETRIC_DUAL_F7_ZETA3_CACHE_PATH = CACHE_DIR / "bz_totally_symmetric_dual_f7_zeta3_terms.json"


def get_cached_baseline_dual_f7_exact_component_terms(
    max_n: int,
    *,
    component: str,
    cache_path: str | Path | None = None,
) -> tuple[Fraction, ...]:
    return _get_cached_dual_f7_exact_component_terms(
        baseline_a_vector(),
        max_n=max_n,
        component=component,
        cache_path=_default_cache_path("baseline", component) if cache_path is None else Path(cache_path),
        sequence_name=f"bz_baseline_dual_f7_{_normalize_component(component)}_terms",
    )


def get_cached_symmetric_dual_f7_exact_component_terms(
    max_n: int,
    *,
    component: str,
    cache_path: str | Path | None = None,
) -> tuple[Fraction, ...]:
    return _get_cached_dual_f7_exact_component_terms(
        totally_symmetric_a_vector(),
        max_n=max_n,
        component=component,
        cache_path=_default_cache_path("symmetric", component) if cache_path is None else Path(cache_path),
        sequence_name=f"bz_totally_symmetric_dual_f7_{_normalize_component(component)}_terms",
    )


def get_cached_baseline_dual_f7_constant_terms(
    max_n: int,
    *,
    cache_path: str | Path = BASELINE_DUAL_F7_CONSTANT_CACHE_PATH,
) -> tuple[Fraction, ...]:
    return get_cached_baseline_dual_f7_exact_component_terms(max_n, component="constant", cache_path=cache_path)


def get_cached_baseline_dual_f7_zeta3_terms(
    max_n: int,
    *,
    cache_path: str | Path = BASELINE_DUAL_F7_ZETA3_CACHE_PATH,
) -> tuple[Fraction, ...]:
    return get_cached_baseline_dual_f7_exact_component_terms(max_n, component="zeta3", cache_path=cache_path)


def get_cached_symmetric_dual_f7_constant_terms(
    max_n: int,
    *,
    cache_path: str | Path = SYMMETRIC_DUAL_F7_CONSTANT_CACHE_PATH,
) -> tuple[Fraction, ...]:
    return get_cached_symmetric_dual_f7_exact_component_terms(max_n, component="constant", cache_path=cache_path)


def get_cached_symmetric_dual_f7_zeta3_terms(
    max_n: int,
    *,
    cache_path: str | Path = SYMMETRIC_DUAL_F7_ZETA3_CACHE_PATH,
) -> tuple[Fraction, ...]:
    return get_cached_symmetric_dual_f7_exact_component_terms(max_n, component="zeta3", cache_path=cache_path)


def get_cached_baseline_dual_f7_companion_terms(
    max_n: int,
    *,
    constant_cache_path: str | Path = BASELINE_DUAL_F7_CONSTANT_CACHE_PATH,
    zeta3_cache_path: str | Path = BASELINE_DUAL_F7_ZETA3_CACHE_PATH,
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    return _get_cached_dual_f7_companion_terms(
        baseline_a_vector(),
        max_n=max_n,
        constant_cache_path=Path(constant_cache_path),
        zeta3_cache_path=Path(zeta3_cache_path),
        constant_sequence_name="bz_baseline_dual_f7_constant_terms",
        zeta3_sequence_name="bz_baseline_dual_f7_zeta3_terms",
    )


def get_cached_symmetric_dual_f7_companion_terms(
    max_n: int,
    *,
    constant_cache_path: str | Path = SYMMETRIC_DUAL_F7_CONSTANT_CACHE_PATH,
    zeta3_cache_path: str | Path = SYMMETRIC_DUAL_F7_ZETA3_CACHE_PATH,
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    return _get_cached_dual_f7_companion_terms(
        totally_symmetric_a_vector(),
        max_n=max_n,
        constant_cache_path=Path(constant_cache_path),
        zeta3_cache_path=Path(zeta3_cache_path),
        constant_sequence_name="bz_totally_symmetric_dual_f7_constant_terms",
        zeta3_sequence_name="bz_totally_symmetric_dual_f7_zeta3_terms",
    )


def _get_cached_dual_f7_exact_component_terms(
    a: tuple[int, ...],
    *,
    max_n: int,
    component: str,
    cache_path: str | Path,
    sequence_name: str,
) -> tuple[Fraction, ...]:
    if max_n <= 0:
        raise ValueError("max_n must be positive")

    normalized_component = _normalize_component(component)
    path = Path(cache_path)
    cached_terms = _load_cache(path, sequence_name=sequence_name, component=normalized_component)
    if len(cached_terms) >= max_n:
        return cached_terms[:max_n]

    extended = list(cached_terms)
    for n in range(len(cached_terms) + 1, max_n + 1):
        extended.append(compute_f7_exact_component_term_from_a(a, n, component=normalized_component))
        _write_cache(path, sequence_name=sequence_name, component=normalized_component, terms=tuple(extended))
    return tuple(extended)


def _get_cached_dual_f7_companion_terms(
    a: tuple[int, ...],
    *,
    max_n: int,
    constant_cache_path: Path,
    zeta3_cache_path: Path,
    constant_sequence_name: str,
    zeta3_sequence_name: str,
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    if max_n <= 0:
        raise ValueError("max_n must be positive")

    constant_terms = list(_load_cache(constant_cache_path, sequence_name=constant_sequence_name, component="constant"))
    zeta3_terms = list(_load_cache(zeta3_cache_path, sequence_name=zeta3_sequence_name, component="zeta3"))
    if len(constant_terms) >= max_n and len(zeta3_terms) >= max_n:
        return tuple(constant_terms[:max_n]), tuple(zeta3_terms[:max_n])

    base_b = dual_b_vector_from_a(a)
    for n in range(1, max_n + 1):
        need_constant = n > len(constant_terms)
        need_zeta3 = n > len(zeta3_terms)
        if not (need_constant or need_zeta3):
            continue

        linear_form = extract_f7_linear_form(scale_b_vector(base_b, n))
        if need_constant:
            constant_terms.append(linear_form.constant_term)
            _write_cache(
                constant_cache_path,
                sequence_name=constant_sequence_name,
                component="constant",
                terms=tuple(constant_terms),
            )
        if need_zeta3:
            zeta3_terms.append(linear_form.zeta_coefficient(3))
            _write_cache(
                zeta3_cache_path,
                sequence_name=zeta3_sequence_name,
                component="zeta3",
                terms=tuple(zeta3_terms),
            )

    return tuple(constant_terms[:max_n]), tuple(zeta3_terms[:max_n])


def _load_cache(path: Path, *, sequence_name: str, component: str) -> tuple[Fraction, ...]:
    if not path.exists():
        return ()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"invalid dual f7 exact-component cache format in {path}")
    if payload.get("sequence") != sequence_name:
        raise ValueError(f"dual f7 exact-component cache sequence mismatch in {path}")
    if payload.get("component") != component:
        raise ValueError(f"dual f7 exact-component cache component mismatch in {path}")
    raw_terms = payload.get("terms")
    if not isinstance(raw_terms, list):
        raise ValueError(f"dual f7 exact-component cache must contain a 'terms' list in {path}")
    return tuple(fraction_from_scalar(value) for value in raw_terms)


def _write_cache(path: Path, *, sequence_name: str, component: str, terms: tuple[Fraction, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "component": component,
        "max_n": len(terms),
        "sequence": sequence_name,
        "terms": [fraction_to_canonical_string(value) for value in terms],
    }
    path.write_text(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True), encoding="utf-8")


def _normalize_component(component: str) -> str:
    normalized = component.strip().lower().replace("(", "").replace(")", "").replace("_", "")
    if normalized not in DUAL_F7_COMPONENTS:
        if normalized == "c0":
            return "constant"
        raise ValueError(f"unsupported dual F_7 exact component {component!r}")
    return normalized


def _default_cache_path(case_id: str, component: str) -> Path:
    normalized_component = _normalize_component(component)
    if case_id == "baseline":
        if normalized_component == "constant":
            return BASELINE_DUAL_F7_CONSTANT_CACHE_PATH
        if normalized_component == "zeta3":
            return BASELINE_DUAL_F7_ZETA3_CACHE_PATH
    if case_id == "symmetric":
        if normalized_component == "constant":
            return SYMMETRIC_DUAL_F7_CONSTANT_CACHE_PATH
        if normalized_component == "zeta3":
            return SYMMETRIC_DUAL_F7_ZETA3_CACHE_PATH
    return CACHE_DIR / f"bz_{case_id}_dual_f7_{normalized_component}_terms.json"
