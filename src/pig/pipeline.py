from __future__ import annotations

from pathlib import Path
import json


def generate_stub_ocel(raw_dir: Path, out_path: Path) -> None:
    """Generate a minimal object-centric event log stub for MVP demo."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "meta": {
            "source": str(raw_dir),
            "format": "OCEL-JSON (stub)",
        },
        "objects": [
            {"id": "order-1", "type": "order", "attributes": {"region": "KR"}},
            {"id": "invoice-1", "type": "invoice", "attributes": {"amount": 12000}},
        ],
        "events": [
            {
                "id": "evt-1",
                "activity": "Create Order",
                "timestamp": "2026-01-01T09:00:00Z",
                "omap": ["order-1"],
            },
            {
                "id": "evt-2",
                "activity": "Issue Invoice",
                "timestamp": "2026-01-01T10:00:00Z",
                "omap": ["order-1", "invoice-1"],
            },
        ],
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
