from __future__ import annotations

import argparse
import json
from pathlib import Path

from .campaigns import run_campaign_structural_dry_run


def main() -> int:
    parser = argparse.ArgumentParser(description="Expand and structurally validate a fixed-sequence campaign.")
    parser.add_argument("campaign", type=Path, help="Path to a campaign YAML file")
    parser.add_argument("--log", action="store_true", help="Log each generated candidate to the results ledger.")
    args = parser.parse_args()

    payload = run_campaign_structural_dry_run(args.campaign, log_results=args.log)
    print(json.dumps(payload, indent=2, sort_keys=True))
    accepted = all(item["gate1_accepted"] for item in payload["variants"])
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
