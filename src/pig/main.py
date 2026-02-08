from __future__ import annotations

import argparse
from pathlib import Path

from pig.pipeline import run_default_ocdfg_pipeline, run_graph_samples


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pig",
        description="PIG 기본 데이터 로드 + OC-DFG/리포트 생성기",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("data/raw"),
        help="기본 event log(.csv)와 OCEL(.ocel.json)을 찾을 디렉터리",
    )
    parser.add_argument(
        "--event-log",
        type=Path,
        default=None,
        help="event log 파일 경로 (기본값: raw-dir 내 첫 *.csv)",
    )
    parser.add_argument(
        "--ocel",
        type=Path,
        default=None,
        help="OCEL 파일 경로 (기본값: raw-dir 내 첫 *.ocel.json)",
    )
    parser.add_argument(
        "--dfg-out",
        type=Path,
        default=Path("data/processed/oc_dfg.json"),
        help="생성할 OC-DFG JSON 출력 경로",
    )
    parser.add_argument(
        "--report-out",
        type=Path,
        default=Path("data/processed/basic_report.md"),
        help="기본 레포트 출력 경로",
    )
    parser.add_argument(
        "--sample-graphs",
        action="store_true",
        help="event log를 활용해 sample OC-DFG/OC-PN PNG를 생성",
    )
    parser.add_argument(
        "--graph-out-dir",
        type=Path,
        default=Path("data/processed"),
        help="sample 그래프 PNG 출력 디렉터리",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    dfg_path, report_path = run_default_ocdfg_pipeline(
        raw_dir=args.raw_dir,
        dfg_out_path=args.dfg_out,
        report_out_path=args.report_out,
        event_log_path=args.event_log,
        ocel_path=args.ocel,
    )
    print(f"[PIG] OC-DFG generated: {dfg_path}")
    print(f"[PIG] Report generated: {report_path}")

    if args.sample_graphs:
        dfg_png, ocpn_png = run_graph_samples(
            raw_dir=args.raw_dir,
            out_dir=args.graph_out_dir,
            event_log_path=args.event_log,
            ocel_path=args.ocel,
        )
        print(f"[PIG] Sample OC-DFG image generated: {dfg_png}")
        print(f"[PIG] Sample OC-PN image generated: {ocpn_png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
