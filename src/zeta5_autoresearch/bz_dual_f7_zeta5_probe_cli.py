from __future__ import annotations

import argparse
from pathlib import Path

from .bz_dual_f7_zeta5_probe import write_bz_dual_f7_zeta5_probe_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Brown-Zudilin dual F_7 zeta(5)-coefficient probe.")
    parser.add_argument("--output", type=Path, default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    output = write_bz_dual_f7_zeta5_probe_report(output_path=args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
