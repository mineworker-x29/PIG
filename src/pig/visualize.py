from __future__ import annotations

from collections import Counter, defaultdict
import math
from pathlib import Path
import struct
import zlib
from typing import Any


_COLOR_PALETTE = [
    (31, 119, 180),
    (255, 127, 14),
    (44, 160, 44),
    (214, 39, 40),
    (148, 103, 189),
    (140, 86, 75),
]


def _write_png(path: Path, width: int, height: int, pixels: bytearray) -> None:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack('!I', len(data)) + tag + data + struct.pack('!I', zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        start = y * stride
        raw.extend(pixels[start:start + stride])

    ihdr = struct.pack('!IIBBBBB', width, height, 8, 2, 0, 0, 0)
    data = zlib.compress(bytes(raw), 9)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', data) + chunk(b'IEND', b'')
    path.write_bytes(png)


def _set_px(p: bytearray, w: int, h: int, x: int, y: int, c: tuple[int, int, int]) -> None:
    if 0 <= x < w and 0 <= y < h:
        i = (y * w + x) * 3
        p[i:i+3] = bytes(c)


def _line(p: bytearray, w: int, h: int, x0: int, y0: int, x1: int, y1: int, c: tuple[int, int, int]) -> None:
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        _set_px(p, w, h, x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def _rect(p: bytearray, w: int, h: int, x0: int, y0: int, x1: int, y1: int, c: tuple[int, int, int]) -> None:
    for y in range(max(0, y0), min(h, y1)):
        for x in range(max(0, x0), min(w, x1)):
            _set_px(p, w, h, x, y, c)


def _circle_outline(p: bytearray, w: int, h: int, cx: int, cy: int, r: int, c: tuple[int, int, int]) -> None:
    for deg in range(360):
        rad = math.radians(deg)
        x = int(cx + r * math.cos(rad))
        y = int(cy + r * math.sin(rad))
        _set_px(p, w, h, x, y, c)


def _arrow(p: bytearray, w: int, h: int, x0: int, y0: int, x1: int, y1: int, c: tuple[int, int, int]) -> None:
    _line(p, w, h, x0, y0, x1, y1, c)
    angle = math.atan2(y1 - y0, x1 - x0)
    for delta in (2.6, -2.6):
        hx = int(x1 + 8 * math.cos(angle + delta))
        hy = int(y1 + 8 * math.sin(angle + delta))
        _line(p, w, h, x1, y1, hx, hy, c)


def _text_block(p: bytearray, w: int, h: int, x: int, y: int, text: str, c: tuple[int, int, int]) -> None:
    # very minimal pseudo-text renderer using blocky glyphs
    for i, ch in enumerate(text[:30]):
        if ch == ' ':
            continue
        _rect(p, w, h, x + i * 6, y, x + i * 6 + 4, y + 6, c)


def render_oc_dfg_png(oc_dfg: dict[str, list[dict[str, Any]]], out_path: Path, title: str) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    acts = sorted({e['from'] for edges in oc_dfg.values() for e in edges} | {e['to'] for edges in oc_dfg.values() for e in edges})
    width, height = 1200, 520
    px = bytearray([255] * (width * height * 3))

    _text_block(px, width, height, 20, 20, title, (20, 20, 20))
    if not acts:
        _write_png(out_path, width, height, px)
        return out_path

    y = 330
    pos = {a: int(100 + i * ((width - 200) / max(1, len(acts)-1))) for i, a in enumerate(acts)}
    for a, x in pos.items():
        _circle_outline(px, width, height, x, y, 30, (45, 45, 45))
        _text_block(px, width, height, x - 20, y - 6, a, (50, 50, 50))

    for i, (typ, edges) in enumerate(sorted(oc_dfg.items())):
        color = _COLOR_PALETTE[i % len(_COLOR_PALETTE)]
        _rect(px, width, height, 20, 80 + i*22, 40, 95 + i*22, color)
        _text_block(px, width, height, 45, 82 + i*22, typ, (20, 20, 20))
        for e in edges:
            _arrow(px, width, height, pos[e['from']], y - (40 + i*16), pos[e['to']], y - (40 + i*16), color)

    _write_png(out_path, width, height, px)
    return out_path


def _build_ocpn_edges(ocel_payload: dict[str, Any]) -> dict[str, Counter[tuple[str, str]]]:
    objects: list[dict[str, Any]] = ocel_payload.get('objects', [])
    events: list[dict[str, Any]] = ocel_payload.get('events', [])
    type_by_object = {o['id']: o['type'] for o in objects}
    by_object: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in events:
        for oid in e.get('omap', []):
            if oid in type_by_object:
                by_object[oid].append(e)
    out: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)
    for oid, seq in by_object.items():
        typ = type_by_object[oid]
        ordered = sorted(seq, key=lambda x: (x.get('timestamp', ''), x.get('id', '')))
        acts = [ev.get('activity', '') for ev in ordered if ev.get('activity')]
        for a, b in zip(acts, acts[1:]):
            out[typ][(a, b)] += 1
    return out


def render_oc_pn_png(ocel_payload: dict[str, Any], out_path: Path, title: str) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    by_type = _build_ocpn_edges(ocel_payload)
    acts = sorted({a for cnt in by_type.values() for edge in cnt for a in edge})
    width, height = 1200, 540
    px = bytearray([255] * (width * height * 3))
    _text_block(px, width, height, 20, 20, title, (20, 20, 20))

    if acts:
        y_t, y_p = 340, 240
        pos = {a: int(110 + i * ((width - 220) / max(1, len(acts)-1))) for i, a in enumerate(acts)}
        for i, a in enumerate(acts):
            x = pos[a]
            _rect(px, width, height, x-35, y_t-20, x+35, y_t+20, (245, 247, 250))
            _line(px, width, height, x-35, y_t-20, x+35, y_t-20, (40,40,40))
            _line(px, width, height, x-35, y_t+20, x+35, y_t+20, (40,40,40))
            _line(px, width, height, x-35, y_t-20, x-35, y_t+20, (40,40,40))
            _line(px, width, height, x+35, y_t-20, x+35, y_t+20, (40,40,40))
            _text_block(px, width, height, x-18, y_t-5, a, (50,50,50))
            if i < len(acts)-1:
                nx = pos[acts[i+1]]
                cx = (x + nx)//2
                _circle_outline(px, width, height, cx, y_p, 10, (70,70,70))
                _arrow(px, width, height, x, y_t-20, cx, y_p+10, (90,90,90))
                _arrow(px, width, height, cx, y_p-10, nx, y_t-20, (90,90,90))

        for i, (typ, cnt) in enumerate(sorted(by_type.items())):
            color = _COLOR_PALETTE[i % len(_COLOR_PALETTE)]
            _rect(px, width, height, 20, 80 + i*22, 40, 95 + i*22, color)
            _text_block(px, width, height, 45, 82 + i*22, typ, (20,20,20))
            for (s, d), _n in cnt.items():
                _arrow(px, width, height, pos[s], 150 + i*16, pos[d], 150 + i*16, color)

    _write_png(out_path, width, height, px)
    return out_path
