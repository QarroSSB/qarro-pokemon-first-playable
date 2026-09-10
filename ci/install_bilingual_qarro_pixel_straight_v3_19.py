#!/usr/bin/env python3
"""Qarro Pixel Straight v3.19 bilingual font follow-up.

Approved device-test direction after comparing the slanted build with the
straight mockup: remove slant completely. Keep the Qarro Pixel custom bitmap
on the native 7-row grid, preserve variable-width advances, and retain manual
Cyrillic readability forms for letters that were ambiguous on-device.

No bitmap resampling/scaling is used. Pokemon / Move / Ability names remain
supported in English. Native FireRed punctuation/control cells and protected
Ash features are untouched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

MARKER = "QARRO_PIXEL_STRAIGHT_V3_19"
SOURCE_PATH = "install_bilingual_qarro_pixel_v3_15.py"

MANUAL = {
    "т": ["00000", "00000", "11111", "10101", "10101", "10101", "10101"],
    "У": ["10001", "10001", "01010", "00100", "00100", "01000", "10000"],
    "у": ["00000", "00000", "10001", "10001", "01111", "00001", "11110"],
    "Ж": ["1001001", "0101010", "0011100", "0001000", "0011100", "0101010", "1001001"],
    "ж": ["0000000", "0000000", "1001001", "0101010", "0011100", "0101010", "1001001"],
    "Ш": ["10101", "10101", "10101", "10101", "10101", "10101", "11111"],
    "ш": ["00000", "00000", "10101", "10101", "10101", "10101", "11111"],
    "Щ": ["101010", "101010", "101010", "101010", "101010", "111110", "000010"],
    "щ": ["000000", "000000", "101010", "101010", "101010", "111110", "000010"],
    "Ы": ["100001", "100001", "100001", "111101", "100101", "100101", "111101"],
    "ы": ["000000", "000000", "100001", "100001", "111101", "100101", "111101"],
    "Ю": ["100111", "101001", "101001", "111001", "101001", "101001", "100111"],
    "ю": ["000000", "000000", "100111", "101001", "111001", "101001", "100111"],
    "Я": ["01111", "10001", "10001", "01111", "00101", "01001", "10001"],
    "я": ["00000", "00000", "01111", "10001", "01111", "00101", "10001"],
    "Д": ["01110", "01010", "01010", "01010", "10001", "11111", "10001"],
    "д": ["00000", "01110", "01010", "01010", "10001", "11111", "10001"],
    "Л": ["00111", "01001", "10001", "10001", "10001", "10001", "10001"],
    "л": ["00000", "00000", "00111", "01001", "10001", "10001", "10001"],
    "Ф": ["00100", "01110", "10101", "10101", "01110", "00100", "00100"],
    "ф": ["00100", "00100", "01110", "10101", "01110", "00100", "00100"],
}


def load_namespace(path: Path, name: str) -> dict:
    code = path.read_text(encoding="utf-8")
    ns = {"__name__": name, "__file__": str(path.resolve())}
    exec(compile(code, str(path), "exec"), ns)
    return ns


def validate_rows(ch: str, rows: list[str]) -> None:
    if len(rows) != 7:
        raise RuntimeError(f"{ch!r}: expected 7 rows")
    widths = {len(r) for r in rows}
    if len(widths) != 1:
        raise RuntimeError(f"{ch!r}: inconsistent row widths")
    width = next(iter(widths))
    if not 1 <= width <= 7:
        raise RuntimeError(f"{ch!r}: invalid source width {width}")
    if any(set(r) - {"0", "1"} for r in rows):
        raise RuntimeError(f"{ch!r}: non-binary row")


def custom_source_mask(glyphs: dict[str, list[str]]):
    def source_mask(_size: str, ch: str) -> tuple[Image.Image, int]:
        rows = glyphs[ch]
        mask = Image.new("L", (len(rows[0]), 7), 0)
        for y, row in enumerate(rows):
            for x, bit in enumerate(row):
                if bit == "1":
                    mask.putpixel((x, y), 255)
        return mask, 7
    return source_mask


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    here = Path(__file__).resolve().parent
    source = load_namespace(here / SOURCE_PATH, "qarro_pixel_source_v315")
    base = source["load_base"]()

    glyphs = source["load_glyphs"](set(base["CHAR_TO_CODE"]))
    for ch, rows in MANUAL.items():
        if ch not in glyphs:
            raise RuntimeError(f"manual glyph {ch!r} is outside runtime charset")
        validate_rows(ch, rows)
        glyphs[ch] = rows

    for ch, rows in glyphs.items():
        validate_rows(ch, rows)

    if glyphs["т"] == glyphs["t"]:
        raise RuntimeError("SAFETY FAIL: Cyrillic т equals Latin t")
    if glyphs["У"] == glyphs["Y"]:
        raise RuntimeError("SAFETY FAIL: Cyrillic У equals Latin Y")
    if max(len(rows[0]) for rows in glyphs.values()) > 7:
        raise RuntimeError("straight source unexpectedly wider than 7 pixels")

    base["source_mask"] = custom_source_mask(glyphs)
    base["VARIANT_PROFILE"] = {
        name: ("QarroPixelStraight", baseline)
        for name, (_old_source, baseline) in base["VARIANT_PROFILE"].items()
    }

    base["verify_charmap"](root)
    paths = sorted((root / "graphics/fonts").glob("latin_*.png"))
    if len(paths) != 9:
        raise RuntimeError(f"expected 9 Latin atlases, got {len(paths)}")

    widths_by_table = {}
    for path in paths:
        table, widths = base["patch_font"](path)
        widths_by_table[table] = widths
    base["patch_width_tables"](root / "src/fonts.c", widths_by_table)

    audit = {
        "marker": MARKER,
        "font": "Qarro Pixel Straight",
        "fontVersion": "0.6-test",
        "sourceFont": "Qarro Pixel custom bitmap",
        "design": "approved straight bilingual GBA pixel font",
        "rasterRows": 7,
        "rowShift": [0, 0, 0, 0, 0, 0, 0],
        "bitmapScaling": False,
        "variableWidthAdvances": True,
        "glyphWidthRange": [min(len(r[0]) for r in glyphs.values()), max(len(r[0]) for r in glyphs.values())],
        "targetGlyphCells": len(glyphs),
        "cyrillicTeDistinctFromLatinT": glyphs["т"] != glyphs["t"],
        "cyrillicUDistinctFromLatinY": glyphs["У"] != glyphs["Y"],
        "manualReadabilityGlyphs": sorted(MANUAL),
        "english": True,
        "russian": True,
        "digits": True,
        "punctuation": "native FireRed",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_font_straight_v3_19_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "[QARRO_PIXEL_STRAIGHT_V3_19] PASS: approved straight RU+EN+digits "
        "installed in all 9 FireRed atlases; no slant/scaling; т/У distinct; Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
