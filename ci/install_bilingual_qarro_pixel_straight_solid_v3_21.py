#!/usr/bin/env python3
"""Qarro Pixel Straight Solid v3.21 bilingual font follow-up.

Real-device correction after v3.20 proved too thin without FireRed's shadow.
This version keeps the approved upright Qarro Pixel source and removes the
*gray* shadow, but uses the same one-pixel lower-right support geometry in the
same foreground colour. Result: crisp, solid strokes without gray blur.

No slant. No bitmap scaling/resampling. Dedicated Cyrillic readability forms
remain. Pokemon / Move / Ability names stay supported in English. Native
FireRed punctuation/control cells and protected Ash features are untouched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from PIL import Image

MARKER = "QARRO_PIXEL_STRAIGHT_SOLID_V3_21"
SOURCE_PATH = "install_bilingual_qarro_pixel_v3_15.py"
SHARP_PATH = "install_bilingual_qarro_pixel_straight_sharp_v3_20.py"


def load_namespace(path: Path, name: str) -> dict:
    code = path.read_text(encoding="utf-8")
    ns = {"__name__": name, "__file__": str(path.resolve())}
    exec(compile(code, str(path), "exec"), ns)
    return ns


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


def patch_font_solid(base: dict, path: Path) -> tuple[str, dict[int, int]]:
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

        if mask.width + 1 > cell_w:
            raise RuntimeError(f"{path.name}: horizontal overflow {ch}/0x{code:02X}")
        if top < 0 or top + mask.height + 1 > cell_h:
            raise RuntimeError(f"{path.name}: vertical overflow {ch}/0x{code:02X}")

        # Solid crisp mode: original pixels + lower-right support pixels,
        # both use the SAME foreground palette index. No gray shadow index.
        for yy in range(mask.height):
            for xx in range(mask.width):
                if not mask.getpixel((xx, yy)):
                    continue
                img.putpixel((x0 + xx, y0 + top + yy), fg)
                img.putpixel((x0 + xx + 1, y0 + top + yy + 1), fg)

        cell = img.crop((x0, y0, x1, y1))
        pts = [
            (x, y)
            for y in range(cell_h)
            for x in range(cell_w)
            if cell.getpixel((x, y)) == fg
        ]
        if not pts:
            raise RuntimeError(f"empty rendered solid glyph {ch}/0x{code:02X}")
        min_x = min(x for x, _ in pts)
        max_x = max(x for x, _ in pts)
        if min_x != 0:
            raise RuntimeError(f"{path.name}: left origin drift {ch}/0x{code:02X} min_x={min_x}")
        rendered_widths[code] = min(cell_w, max(4, max_x + 1))

    for code, before in protected_before.items():
        if base["cell_pixels"](img, code, total) != before:
            raise RuntimeError(f"SAFETY FAIL: non-target glyph 0x{code:02X} changed in {path.name}")

    img.save(path, optimize=False)
    print(
        f"[QARRO_PIXEL_SOLID] {path.name}: {len(target_codes)} targets; "
        f"baseline={target_baseline}; gray-shadow=OFF; solid-support=ON; "
        f"advances={sorted(set(rendered_widths.values()))}"
    )
    return file_to_width[path.name], rendered_widths


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    here = Path(__file__).resolve().parent
    source = load_namespace(here / SOURCE_PATH, "qarro_pixel_source_v315")
    sharp = load_namespace(here / SHARP_PATH, "qarro_pixel_sharp_source_v320")
    base = source["load_base"]()

    glyphs = source["load_glyphs"](set(base["CHAR_TO_CODE"]))
    manual = sharp["MANUAL"]
    validate_rows = sharp["validate_rows"]
    for ch, rows in manual.items():
        if ch not in glyphs:
            raise RuntimeError(f"manual glyph {ch!r} outside runtime charset")
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
        name: ("QarroPixelStraightSolid", baseline)
        for name, (_old_source, baseline) in base["VARIANT_PROFILE"].items()
    }

    base["verify_charmap"](root)
    paths = sorted((root / "graphics/fonts").glob("latin_*.png"))
    if len(paths) != 9:
        raise RuntimeError(f"expected 9 Latin atlases, got {len(paths)}")

    widths_by_table = {}
    for path in paths:
        table, widths = patch_font_solid(base, path)
        widths_by_table[table] = widths
    base["patch_width_tables"](root / "src/fonts.c", widths_by_table)

    audit = {
        "marker": MARKER,
        "font": "Qarro Pixel Straight Solid",
        "fontVersion": "0.8-test",
        "design": "upright bilingual GBA pixel font; gray shadow replaced by same-colour support",
        "rasterRows": 7,
        "rowShift": [0, 0, 0, 0, 0, 0, 0],
        "bitmapScaling": False,
        "grayLetterShadow": False,
        "solidSupportOffset": [1, 1],
        "supportUsesForegroundColour": True,
        "variableWidthAdvances": True,
        "targetGlyphCells": len(glyphs),
        "cyrillicTeDistinctFromLatinT": glyphs["т"] != glyphs["t"],
        "cyrillicUDistinctFromLatinY": glyphs["У"] != glyphs["Y"],
        "manualReadabilityGlyphs": sorted(manual),
        "english": True,
        "russian": True,
        "digits": True,
        "punctuation": "native FireRed",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_font_straight_solid_v3_21_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "[QARRO_PIXEL_STRAIGHT_SOLID_V3_21] PASS: RU+EN+digits installed in all 9 "
        "FireRed atlases; upright/no scaling; gray shadow OFF; same-colour 1px support ON; "
        "т/У distinct; Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
