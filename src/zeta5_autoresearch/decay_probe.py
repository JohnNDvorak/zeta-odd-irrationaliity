from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecayMetric:
    name: str
    latest_value: float | None
    published_value: float | None
    description: str


@dataclass(frozen=True)
class DecayProbeSummary:
    object_id: str
    family: str
    object_kind: str
    bridge_target_family: str | None
    source_status: str
    exact_status: str
    provenance_title: str
    provenance_url: str
    provenance_version: str
    exact_indices: tuple[int, ...]
    numeric_indices: tuple[int, ...]
    max_verified_index: int | None
    available_metrics: tuple[DecayMetric, ...]
    missing_prerequisites: tuple[str, ...]
    recommendation: str


def build_decay_probe_summary(
    *,
    object_id: str,
    family: str,
    object_kind: str,
    bridge_target_family: str | None = None,
    source_status: str,
    exact_status: str,
    provenance_title: str,
    provenance_url: str,
    provenance_version: str,
    exact_indices: tuple[int, ...],
    numeric_indices: tuple[int, ...],
    max_verified_index: int | None,
    available_metrics: tuple[DecayMetric, ...],
    missing_prerequisites: tuple[str, ...] = (),
    recommendation: str,
) -> DecayProbeSummary:
    return DecayProbeSummary(
        object_id=object_id,
        family=family,
        object_kind=object_kind,
        bridge_target_family=bridge_target_family,
        source_status=source_status,
        exact_status=exact_status,
        provenance_title=provenance_title,
        provenance_url=provenance_url,
        provenance_version=provenance_version,
        exact_indices=exact_indices,
        numeric_indices=numeric_indices,
        max_verified_index=max_verified_index,
        available_metrics=available_metrics,
        missing_prerequisites=missing_prerequisites,
        recommendation=recommendation,
    )


def build_missing_decay_probe_summary(
    *,
    object_id: str,
    family: str,
    object_kind: str,
    bridge_target_family: str | None = None,
    provenance_title: str,
    provenance_url: str,
    provenance_version: str = "",
    missing_prerequisites: tuple[str, ...],
    recommendation: str,
) -> DecayProbeSummary:
    return build_decay_probe_summary(
        object_id=object_id,
        family=family,
        object_kind=object_kind,
        bridge_target_family=bridge_target_family,
        source_status="missing_local",
        exact_status="missing",
        provenance_title=provenance_title,
        provenance_url=provenance_url,
        provenance_version=provenance_version,
        exact_indices=(),
        numeric_indices=(),
        max_verified_index=None,
        available_metrics=(),
        missing_prerequisites=missing_prerequisites,
        recommendation=recommendation,
    )
