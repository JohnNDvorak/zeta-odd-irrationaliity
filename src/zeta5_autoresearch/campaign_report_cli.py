from __future__ import annotations

import argparse
from pathlib import Path

from .campaign_report import write_campaign_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a markdown report for a fixed-sequence campaign.")
    parser.add_argument("campaign", type=Path, help="Path to a campaign YAML file")
    parser.add_argument("--output", type=Path, default=None, help="Optional output markdown path")
    args = parser.parse_args()

    output = write_campaign_report(args.campaign, output_path=args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
