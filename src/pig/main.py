from __future__ import annotations

import argparse
from pathlib import Path

from pig.pipeline import generate_stub_ocel


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pig",
        description="PIG MVP pipeline runner",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("data/raw"),
        help="Directory containing raw data/logs",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/processed/ocel_stub.json"),
        help="Output OCEL JSON path",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    generate_stub_ocel(raw_dir=args.raw_dir, out_path=args.out)
    print(f"[PIG] OCEL stub generated: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
