from __future__ import annotations

import csv
import json
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path
from typing import Any

from ..config import RESULT_COLUMNS, RESULTS_PATH
from ..models import fraction_to_canonical_string


def _serialize_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, Fraction):
        return fraction_to_canonical_string(value)
    if isinstance(value, (tuple, list, dict)):
        return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def initialize_results_store(path: Path | None = RESULTS_PATH) -> Path:
    results_path = RESULTS_PATH if path is None else Path(path)
    results_path.parent.mkdir(parents=True, exist_ok=True)
    if results_path.exists():
        return results_path
    with results_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(RESULT_COLUMNS), delimiter="\t")
        writer.writeheader()
    return results_path


def append_result(row: Mapping[str, Any], path: Path | None = RESULTS_PATH) -> Path:
    results_path = initialize_results_store(path)
    unknown_keys = set(row) - set(RESULT_COLUMNS)
    if unknown_keys:
        unknown_text = ", ".join(sorted(unknown_keys))
        raise ValueError(f"result row contains unknown columns: {unknown_text}")

    serialized_row = {column: _serialize_value(row.get(column)) for column in RESULT_COLUMNS}
    with results_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(RESULT_COLUMNS), delimiter="\t")
        writer.writerow(serialized_row)
    return results_path
