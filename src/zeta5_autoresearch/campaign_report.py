from __future__ import annotations

from pathlib import Path

from .campaigns import run_campaign_structural_dry_run
from .config import DATA_DIR


def render_campaign_report(campaign_path: str | Path) -> str:
    payload = run_campaign_structural_dry_run(campaign_path, log_results=False)
    variants = payload["variants"]
    sequence_hashes = sorted({item["sequence_hash"] for item in variants})

    lines = [
        f"# {payload['label']}",
        "",
        f"- Campaign ID: `{payload['campaign_id']}`",
        f"- Variant count: `{len(variants)}`",
        f"- Shared sequence hash count: `{len(sequence_hashes)}`",
        f"- Shared sequence hash: `{sequence_hashes[0]}`" if len(sequence_hashes) == 1 else f"- Sequence hashes: `{', '.join(sequence_hashes)}`",
        "",
        "| Variant | Mode | Representation | Certificate | Equality Witness | Human Review | Routing Hash | Certificate Hash |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for item in variants:
        human_review = "yes" if item["certificate_template"] != "BZ_standard" or item["mode"] == "Mode A-slow" else "no"
        lines.append(
            "| "
            f"`{item['variant_id']}` | `{item['mode']}` | `{item['representation']}` | `{item['certificate_template']}` | "
            f"`{_equality_witness_for_variant(item)}` | `{human_review}` | `{item['routing_hash']}` | `{item['certificate_hash']}` |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
        ]
    )
    for item in variants:
        lines.append(f"- `{item['variant_id']}`: {item['notes']}")
    return "\n".join(lines) + "\n"


def write_campaign_report(campaign_path: str | Path, *, output_path: str | Path | None = None) -> Path:
    campaign_file = Path(campaign_path)
    output = Path(output_path) if output_path is not None else DATA_DIR / "logs" / f"{campaign_file.stem}_report.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_campaign_report(campaign_file), encoding="utf-8")
    return output


def _equality_witness_for_variant(item: dict[str, str]) -> str:
    if item["mode"] == "Mode A-fast":
        return "published_seed_identity"
    return "none"
