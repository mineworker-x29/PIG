from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
import csv
import json
from pathlib import Path
from typing import Any

from pig.visualize import render_oc_dfg_png, render_oc_pn_png


def _parse_timestamp(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _resolve_default_file(raw_dir: Path, pattern: str) -> Path:
    matches = sorted(raw_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No file matched pattern '{pattern}' in {raw_dir}")
    return matches[0]


def _load_event_log_rows(event_log_path: Path) -> list[dict[str, str]]:
    with event_log_path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        return [dict(row) for row in reader]


def _load_ocel(ocel_path: Path) -> dict[str, Any]:
    return json.loads(ocel_path.read_text(encoding="utf-8"))


def _build_oc_dfg(ocel_payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    objects: list[dict[str, Any]] = ocel_payload.get("objects", [])
    events: list[dict[str, Any]] = ocel_payload.get("events", [])

    object_types = {obj["id"]: obj["type"] for obj in objects}
    events_by_object: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for event in events:
        for obj_id in event.get("omap", []):
            if obj_id in object_types:
                events_by_object[obj_id].append(event)

    transitions_by_type: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)

    for obj_id, obj_events in events_by_object.items():
        obj_type = object_types[obj_id]
        ordered = sorted(
            obj_events,
            key=lambda e: (_parse_timestamp(e["timestamp"]), e.get("id", "")),
        )
        activities = [e["activity"] for e in ordered]
        for source, target in zip(activities, activities[1:]):
            transitions_by_type[obj_type][(source, target)] += 1

    dfg_payload: dict[str, list[dict[str, Any]]] = {}
    for obj_type, transitions in transitions_by_type.items():
        edges = [
            {"from": source, "to": target, "count": count}
            for (source, target), count in transitions.items()
        ]
        edges.sort(key=lambda edge: (-edge["count"], edge["from"], edge["to"]))
        dfg_payload[obj_type] = edges

    return dfg_payload


def _build_basic_report(
    event_log_path: Path,
    ocel_path: Path,
    event_log_rows: list[dict[str, str]],
    ocel_payload: dict[str, Any],
    oc_dfg: dict[str, list[dict[str, Any]]],
) -> str:
    objects = ocel_payload.get("objects", [])
    events = ocel_payload.get("events", [])

    object_type_counts = Counter(obj.get("type", "unknown") for obj in objects)
    lines = [
        "# PIG 기본 OC-DFG 리포트",
        "",
        f"- Event log: `{event_log_path}`",
        f"- OCEL: `{ocel_path}`",
        f"- Event log rows: {len(event_log_rows)}",
        f"- OCEL objects: {len(objects)}",
        f"- OCEL events: {len(events)}",
        "",
        "## Object Type 분포",
    ]

    for obj_type, count in sorted(object_type_counts.items()):
        lines.append(f"- {obj_type}: {count}")

    lines.append("")
    lines.append("## OC-DFG (상위 엣지)")

    if not oc_dfg:
        lines.append("- 생성된 전이가 없습니다.")

    for obj_type, edges in sorted(oc_dfg.items()):
        lines.append(f"### {obj_type}")
        for edge in edges[:10]:
            lines.append(f"- {edge['from']} -> {edge['to']} (count={edge['count']})")
        if not edges:
            lines.append("- 전이 없음")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def run_default_ocdfg_pipeline(
    raw_dir: Path,
    dfg_out_path: Path,
    report_out_path: Path,
    event_log_path: Path | None = None,
    ocel_path: Path | None = None,
) -> tuple[Path, Path]:
    raw_dir = raw_dir.resolve()
    event_log_path = (event_log_path or _resolve_default_file(raw_dir, "*.csv")).resolve()
    ocel_path = (ocel_path or _resolve_default_file(raw_dir, "*.ocel.json")).resolve()

    event_log_rows = _load_event_log_rows(event_log_path)
    ocel_payload = _load_ocel(ocel_path)
    oc_dfg = _build_oc_dfg(ocel_payload)

    dfg_out_path.parent.mkdir(parents=True, exist_ok=True)
    report_out_path.parent.mkdir(parents=True, exist_ok=True)

    dfg_payload = {
        "meta": {
            "event_log_path": str(event_log_path),
            "ocel_path": str(ocel_path),
            "object_types": sorted(oc_dfg.keys()),
        },
        "oc_dfg": oc_dfg,
    }
    dfg_out_path.write_text(json.dumps(dfg_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    report = _build_basic_report(event_log_path, ocel_path, event_log_rows, ocel_payload, oc_dfg)
    report_out_path.write_text(report, encoding="utf-8")

    return dfg_out_path, report_out_path


def run_graph_samples(
    raw_dir: Path,
    out_dir: Path,
    event_log_path: Path | None = None,
    ocel_path: Path | None = None,
) -> tuple[Path, Path]:
    raw_dir = raw_dir.resolve()
    event_log_path = (event_log_path or _resolve_default_file(raw_dir, "*.csv")).resolve()
    ocel_path = (ocel_path or _resolve_default_file(raw_dir, "*.ocel.json")).resolve()

    ocel_payload = _load_ocel(ocel_path)
    oc_dfg = _build_oc_dfg(ocel_payload)

    log_name = event_log_path.stem
    oc_dfg_png_path = out_dir / f"{log_name}_oc-dfg.png"
    oc_pn_png_path = out_dir / f"{log_name}_oc-pn.png"

    render_oc_dfg_png(oc_dfg, oc_dfg_png_path, title=f"{log_name} - OC-DFG")
    render_oc_pn_png(ocel_payload, oc_pn_png_path, title=f"{log_name} - OC-PN")

    return oc_dfg_png_path, oc_pn_png_path
