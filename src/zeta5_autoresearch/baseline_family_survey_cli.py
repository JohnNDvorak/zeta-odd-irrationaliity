from __future__ import annotations

import argparse
from pathlib import Path

from .baseline_family_survey import write_baseline_family_survey_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a modular recurrence-family survey for the Brown-Zudilin baseline sequence.")
    parser.add_argument("survey", type=Path, help="Path to a baseline family survey YAML file.")
    parser.add_argument("--output", type=Path, default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    output = write_baseline_family_survey_report(args.survey, output_path=args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
