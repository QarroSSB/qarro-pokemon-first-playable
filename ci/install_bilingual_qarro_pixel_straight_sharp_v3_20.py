#!/usr/bin/env python3
"""Qarro Pixel Straight Sharp v3.20 bilingual font follow-up.

Device-test refinement of the approved straight Qarro Pixel design:
- no slant;
- no bitmap resampling/scaling;
- remove the FireRed-style 1px gray shadow from all target letter/digit glyphs;
- keep the same variable-width advances as the shadowed straight build so
  this test isolates clarity/sharpness instead of changing spacing at once;
- retain dedicated Cyrillic readability forms.

Pokemon / Move / Ability names remain supported in English. Native FireRed
punctuation/control cells and protected Ash features are untouched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

MARKER = "QARRO_PIXEL_STRAIGHT_SHARP_V3_20"
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


def patch_font_no_shadow(base: dict, path: Path) -> tuple[str, dict[int, int]]:
    img = Image.open(path)
    cols = base["COLS"]
    cell_w = base["CELL_W"]
    cell_h = base["CELL_H"]
    bg = base["FONT_BG"]
    fg = base["FONT_FG"]
    target_codes = base["TARGET_CODES"]
    char_to_code = base["CHAR_TO_CODE"]
    file_to_width = base["FONT_FILE_TO_WIDTH_TABLE"]
    variant_profile = base["VARIANT_PROFILE"]

    if img.mode != "P" or img.width != cols * cell_w or img.height % cell_h:
        raise RuntimeError(f"unexpected font atlas geometry/mode: {path} {img.mode} {img.size}")
    if path.name not in file_to_width or path.name not in variant_profile:
        raise RuntimeError(f"unmapped font variant {path.name}")

    total = cols * (img.height // cell_h)
    if max(target_codes) >= total:
        raise RuntimeError(f"atlas too small for bilingual target set: {path.name}")

    protected_before = {
        code: base["cell_pixels"](img, code, total)
        for code in range(total)
        if code not in target_codes
    }

    source_size, target_baseline = variant_profile[path.name]
    rendered_widths: dict[int, int] = {}

    for ch, code in char_to_code.items():
        mask, source_baseline = base["source_mask"](source_size, ch)
        top = target_baseline - source_baseline
        x0, y0, x1, y1 = base["cell_box"](code, total)

        for y in range(y0, y1):
            for x in range(x0, x1):
                img.putpixel((x, y), bg)

        if mask.width > cell_w:
            raise RuntimeError(f"{path.name}: horizontal overflow {ch}/0x{code:02X} width={mask.width}")
        if top < 0 or top + mask.height > cell_h:
            raise RuntimeError(
                f"{path.name}: vertical overflow {ch}/0x{code:02X} y={top}..{top + mask.height}"
            )

        # Sharp mode: foreground pixels only. No 1px gray shadow pass.
        for yy in range(mask.height):
            for xx in range(mask.width):
                if mask.getpixel((xx, yy)):
                    img.putpixel((x0 + xx, y0 + top + yy), fg)

        cell = img.crop((x0, y0, x1, y1))
        pts = [
            (x, y)
            for y in range(cell_h)
            for x in range(cell_w)
            if cell.getpixel((x, y)) == fg
        ]
        if not pts:
            raise RuntimeError(f"empty rendered sharp glyph {ch}/0x{code:02X}")
        min_x = min(x for x, _ in pts)
        max_x = max(x for x, _ in pts)
        if min_x != 0:
            raise RuntimeError(f"{path.name}: left origin drift {ch}/0x{code:02X} min_x={min_x}")

        # Keep the same apparent advance as the prior shadowed build:
        # glyph body width + one blank pixel. Only visual shadow is removed.
        rendered_widths[code] = min(cell_w, max(4, max_x + 2))

    for code, before in protected_before.items():
        if base["cell_pixels"](img, code, total) != before:
            raise RuntimeError(
                f"SAFETY FAIL: non-target glyph 0x{code:02X} changed in {path.name}"
            )

    img.save(path, optimize=False)
    print(
        f"[QARRO_PIXEL_SHARP] {path.name}: {len(target_codes)} targets; "
        f"baseline={target_baseline}; shadow=OFF; advances={sorted(set(rendered_widths.values()))}"
    )
    return file_to_width[path.name], rendered_widths


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

    base["source_mask"] = custom_source_mask(glyphs)
    base["VARIANT_PROFILE"] = {
        name: ("QarroPixelStraightSharp", baseline)
        for name, (_old_source, baseline) in base["VARIANT_PROFILE"].items()
    }

    base["verify_charmap"](root)
    paths = sorted((root / "graphics/fonts").glob("latin_*.png"))
    if len(paths) != 9:
        raise RuntimeError(f"expected 9 Latin atlases, got {len(paths)}")

    widths_by_table = {}
    for path in paths:
        table, widths = patch_font_no_shadow(base, path)
        widths_by_table[table] = widths
    base["patch_width_tables"](root / "src/fonts.c", widths_by_table)

    audit = {
        "marker": MARKER,
        "font": "Qarro Pixel Straight Sharp",
        "fontVersion": "0.7-test",
        "design": "straight bilingual GBA pixel font with shadow removed",
        "rasterRows": 7,
        "rowShift": [0, 0, 0, 0, 0, 0, 0],
        "bitmapScaling": False,
        "letterShadow": False,
        "foregroundOnly": True,
        "spacingPolicy": "same advance as v0.6 shadowed build",
        "variableWidthAdvances": True,
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
    out = root / "build/qarro_font_straight_sharp_v3_20_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "[QARRO_PIXEL_STRAIGHT_SHARP_V3_20] PASS: RU+EN+digits installed in all 9 "
        "FireRed atlases; straight/no scaling; letter shadow OFF; spacing preserved; "
        "т/У distinct; Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
