#!/usr/bin/env python3
"""Fail-closed audit for the Qarro FireRed RU+EN foundation.

Read-only verification after all localization/font installers have run.
It checks the Cyrillic charmap, every FireRed Latin font atlas, final glyph
advance tables, UTF-8 health, and that the localized early-game surface
actually contains Russian text. It never changes gameplay data and never
touches Ash Bond / Ash Cap.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required") from exc

CYRILLIC = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
FONT_NAMES = (
    "latin_small_narrow.png", "latin_small.png", "latin_normal.png",
    "latin_short.png", "latin_narrow.png", "latin_narrower.png",
    "latin_small_narrower.png", "latin_short_narrow.png",
    "latin_short_narrower.png",
)
FONT_FILE_TO_WIDTH_TABLE = {
    "latin_small_narrow.png": "gFontSmallNarrowLatinGlyphWidths",
    "latin_small.png": "gFontSmallLatinGlyphWidths",
    "latin_normal.png": "gFontNormalLatinGlyphWidths",
    "latin_short.png": "gFontShortLatinGlyphWidths",
    "latin_narrow.png": "gFontNarrowLatinGlyphWidths",
    "latin_narrower.png": "gFontNarrowerLatinGlyphWidths",
    "latin_small_narrower.png": "gFontSmallNarrowerLatinGlyphWidths",
    "latin_short_narrow.png": "gFontShortNarrowLatinGlyphWidths",
    "latin_short_narrower.png": "gFontShortNarrowerLatinGlyphWidths",
}
TEXT_ROOTS = ("src", "data/maps", "data/text")
EARLY_MARKERS = (
    "Привет", "ПОКЕМОН", "ПАЛЛЕТ", "ОУК", "МАМА", "Пора идти",
)
BAD_TEXT = ("\ufffd", "Р�", "С�")


def parse_charmap(path: Path) -> dict[str, int]:
    text = path.read_text(encoding="utf-8")
    out: dict[str, int] = {}
    for ch in CYRILLIC:
        m = re.search(rf"(?m)^'{re.escape(ch)}'\s*=\s*([0-9A-Fa-f]{{2,4}})\s*$", text)
        if not m:
            raise RuntimeError(f"missing Cyrillic charmap entry: {ch}")
        out[ch] = int(m.group(1), 16)
    if len(set(out.values())) != len(out):
        raise RuntimeError("duplicate Cyrillic charmap codes")
    return out


def parse_width_tables(path: Path) -> dict[str, list[int]]:
    text = path.read_text(encoding="utf-8")
    rx = re.compile(
        r"(?ms)^(?:ALIGNED\(4\)\s+)?const u8 "
        r"(?P<name>gFont[A-Za-z0-9_]*LatinGlyphWidths)\[\]\s*=\s*\{"
        r"(?P<body>.*?)^\};"
    )
    out: dict[str, list[int]] = {}
    for m in rx.finditer(text):
        name = m.group("name")
        if name not in set(FONT_FILE_TO_WIDTH_TABLE.values()):
            continue
        vals = [int(x) for x in re.findall(r"\b\d+\b", m.group("body"))]
        if len(vals) != 512:
            raise RuntimeError(f"{name}: expected 512 width entries, got {len(vals)}")
        out[name] = vals
    expected = set(FONT_FILE_TO_WIDTH_TABLE.values())
    if set(out) != expected:
        missing = sorted(expected - set(out))
        extra = sorted(set(out) - expected)
        raise RuntimeError(f"font width-table set mismatch missing={missing} extra={extra}")
    return out


def audit_fonts(root: Path, codes: dict[str, int]) -> dict[str, dict[str, int]]:
    width_tables = parse_width_tables(root / "src/fonts.c")
    result = {}
    for name in FONT_NAMES:
        path = root / "graphics/fonts" / name
        if not path.is_file():
            raise RuntimeError(f"missing font atlas: {path}")
        img = Image.open(path)
        if img.mode != "P" or img.width != 256 or img.height % 16:
            raise RuntimeError(f"unexpected atlas geometry/mode: {name} {img.mode} {img.size}")
        cells = (img.width // 16) * (img.height // 16)
        widths = width_tables[FONT_FILE_TO_WIDTH_TABLE[name]]
        nonempty = 0
        min_ink = None
        min_advance = None
        max_advance = None
        for ch, code in codes.items():
            if code >= cells:
                raise RuntimeError(f"{name}: {ch} code 0x{code:X} outside atlas ({cells} cells)")
            x = (code % 16) * 16
            y = (code // 16) * 16
            cell = img.crop((x, y, x + 16, y + 16))
            pts = [
                (px, py)
                for py in range(16)
                for px in range(16)
                if cell.getpixel((px, py)) != 0
            ]
            ink = len(pts)
            if ink == 0:
                raise RuntimeError(f"{name}: empty Cyrillic glyph {ch}/0x{code:X}")
            max_x = max(px for px, _ in pts)
            expected_advance = max(4, max_x + 1)
            actual_advance = widths[code]
            if actual_advance != expected_advance:
                raise RuntimeError(
                    f"{name}: Cyrillic advance/raster mismatch {ch}/0x{code:X}: "
                    f"width_table={actual_advance}, raster_expected={expected_advance}"
                )
            if not 4 <= actual_advance <= 16:
                raise RuntimeError(
                    f"{name}: invalid Cyrillic advance {ch}/0x{code:X}: {actual_advance}"
                )
            nonempty += 1
            min_ink = ink if min_ink is None else min(min_ink, ink)
            min_advance = actual_advance if min_advance is None else min(min_advance, actual_advance)
            max_advance = actual_advance if max_advance is None else max(max_advance, actual_advance)
        result[name] = {
            "cyrillic_nonempty": nonempty,
            "min_ink_pixels": int(min_ink or 0),
            "min_advance": int(min_advance or 0),
            "max_advance": int(max_advance or 0),
            "advance_raster_matches": nonempty,
        }
    return result


def iter_text_files(root: Path):
    exts = {".c", ".h", ".inc", ".s", ".txt"}
    for rel in TEXT_ROOTS:
        base = root / rel
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in exts:
                yield path


def visible_text_surface(path: Path, text: str) -> str:
    """Remove source comments before runtime-facing localization checks.

    The pinned Expansion source already contains legacy replacement characters
    in a few developer comments (for example POK�MON in src/contest_effect.c).
    Comments are not compiled strings and must not satisfy Russian coverage or
    early-game marker gates either. Keep the gate fail-closed for actual
    source/string content while ignoring non-runtime comments.
    """
    if path.suffix.lower() in {".c", ".h", ".inc", ".s"}:
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        text = re.sub(r"//.*?$", "", text, flags=re.M)
        if path.suffix.lower() == ".s":
            text = re.sub(r"(?m)^\s*@.*$", "", text)
    return text


def audit_text(root: Path) -> dict[str, object]:
    files = 0
    cyr_files = 0
    cyr_chars = 0
    marker_hits = {m: 0 for m in EARLY_MARKERS}
    accented_e = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError(f"non-UTF8 text file: {path.relative_to(root)}") from exc
        files += 1
        runtime_text = visible_text_surface(path, text)
        for bad in BAD_TEXT:
            if bad in runtime_text:
                raise RuntimeError(
                    f"mojibake/replacement marker {bad!r} in runtime text of {path.relative_to(root)}"
                )
        count = sum(runtime_text.count(ch) for ch in CYRILLIC)
        if count:
            cyr_files += 1
            cyr_chars += count
        for marker in EARLY_MARKERS:
            marker_hits[marker] += runtime_text.count(marker)
        if "é" in text:
            accented_e.append(str(path.relative_to(root)))
    missing = [m for m, n in marker_hits.items() if n == 0]
    if missing:
        raise RuntimeError(f"expected localized early-game markers missing: {missing}")
    if cyr_files < 4 or cyr_chars < 100:
        raise RuntimeError(f"Russian localization unexpectedly sparse: files={cyr_files}, chars={cyr_chars}")
    return {
        "scanned_text_files": files,
        "files_with_cyrillic": cyr_files,
        "cyrillic_characters": cyr_chars,
        "early_marker_hits": marker_hits,
        "files_still_containing_accented_e": accented_e[:100],
        "accented_e_file_count": len(accented_e),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    codes = parse_charmap(root / "charmap.txt")
    report = {
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability names may remain English",
        "cyrillic_glyph_count": len(codes),
        "fonts": audit_fonts(root, codes),
        "text": audit_text(root),
    }
    out = root / "build" / "qarro_ru_foundation_v3_9_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[QARRO_RU_FOUNDATION_AUDIT_V3_9] PASS: {len(codes)} Cyrillic glyphs across "
        f"{len(FONT_NAMES)} atlases; raster/advance tables aligned; Russian text/UTF-8 baseline healthy"
    )
    print(f"audit: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())