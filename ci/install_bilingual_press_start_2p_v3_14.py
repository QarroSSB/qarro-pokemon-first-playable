#!/usr/bin/env python3
"""Qarro v3.14 bilingual Press Start 2P font pass.

Replaces visible English letters, Russian letters and digits in all nine
FireRed Latin font atlases with compact, readability-first monochrome rasters
derived from the user-supplied Press Start 2P font (SIL Open Font License 1.1).

The TTF itself is not committed or redistributed by this installer. Exact
7 px / 8 px raster masks generated from the user-supplied TTF are stored as
compact glyph data and verified by SHA-256 before use. Punctuation and
unrelated/control cells remain native FireRed.

Pokemon, move and ability names can stay English while Russian UI/dialogue
uses the same visual alphabet. Literal é/É normalization remains handled by
the existing post-localization pass. Ash Bond / Ash Cap are not touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image

MARKER = "QARRO_BILINGUAL_PRESS_START_2P_V3_14"
CELL_W = 16
CELL_H = 16
COLS = 16
FONT_BG = 0
FONT_FG = 1
FONT_SHADOW = 2

EN_UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EN_LOW = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
RU = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"

EN_CODES = {**{ch: 0xBB + i for i, ch in enumerate(EN_UP)},
            **{ch: 0xD5 + i for i, ch in enumerate(EN_LOW)},
            **{ch: 0xA1 + i for i, ch in enumerate(DIGITS)}}
CYR_CODES_LIST = list(range(0x01, 0x2A)) + list(range(0x3B, 0x51)) + [0x5A, 0x68, 0x6F]
CYR_CODES_LIST[RU.index("Щ")] = 0x2F
RU_CODES = dict(zip(RU, CYR_CODES_LIST))
CHAR_TO_CODE = {**EN_CODES, **RU_CODES}
TARGET_CODES = set(CHAR_TO_CODE.values())

if len(TARGET_CODES) != len(CHAR_TO_CODE):
    raise RuntimeError("bilingual target code collision")
if RU_CODES["Щ"] != 0x2F:
    raise RuntimeError("expected Щ runtime mapping changed")
if 0x1B in TARGET_CODES:
    raise RuntimeError("0x1B/é must remain outside Press Start 2P target cells")

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
EXPECTED_WIDTH_ARRAYS = set(FONT_FILE_TO_WIDTH_TABLE.values())

# Real-device feedback: the shape/readability is right, but the font is
# slightly too large throughout the UI. Use the exact native 7 px raster in
# all nine FireRed Latin atlases and tighten the variable-width advance by
# one pixel. This reduces the footprint everywhere without distorting glyphs.
VARIANT_PROFILE = {
    "latin_normal.png": ("7", 11),
    "latin_narrow.png": ("7", 11),
    "latin_narrower.png": ("7", 11),
    "latin_short.png": ("7", 10),
    "latin_short_narrow.png": ("7", 10),
    "latin_short_narrower.png": ("7", 10),
    "latin_small.png": ("7", 10),
    "latin_small_narrow.png": ("7", 10),
    "latin_small_narrower.png": ("7", 10),
}

GLYPH_DATA_FILE = "press_start_2p_glyphs_v3_14.json"
GLYPH_DATA_SHA256 = "8e476e84956a1170b4c144b624590eae84792246a48ac58f58ea8355086a5f38"

_GLYPH_PACKS: dict[str, dict[str, str]] | None = None

def load_glyph_packs() -> dict[str, dict[str, str]]:
    """Load exact 7/8px rasters generated from the user's supplied TTF."""
    global _GLYPH_PACKS
    if _GLYPH_PACKS is not None:
        return _GLYPH_PACKS
    path = Path(__file__).resolve().with_name(GLYPH_DATA_FILE)
    data = path.read_bytes()
    digest = __import__("hashlib").sha256(data).hexdigest()
    if digest != GLYPH_DATA_SHA256:
        raise RuntimeError(
            f"Press Start 2P glyph-data SHA256 mismatch: {digest} != {GLYPH_DATA_SHA256}"
        )
    packs = json.loads(data.decode("utf-8"))
    if set(packs) != {"7", "8"}:
        raise RuntimeError(f"unexpected Press Start 2P raster sizes: {sorted(packs)}")
    for size, pack in packs.items():
        if set(pack) != set(CHAR_TO_CODE):
            raise RuntimeError(
                f"Press Start 2P {size}px raster character set does not match target set"
            )
    _GLYPH_PACKS = packs
    print(f"[press-start-2p-v314] verified exact user raster sha256={digest}")
    return packs


def cell_box(code: int, total_cells: int) -> tuple[int, int, int, int]:
    if not 0 <= code < total_cells:
        raise RuntimeError(f"glyph code 0x{code:02X} outside atlas")
    x0 = (code % COLS) * CELL_W
    y0 = (code // COLS) * CELL_H
    return x0, y0, x0 + CELL_W, y0 + CELL_H


def cell_pixels(img: Image.Image, code: int, total_cells: int) -> bytes:
    return bytes(img.crop(cell_box(code, total_cells)).getdata())


def source_mask(size: str, ch: str) -> tuple[Image.Image, int]:
    spec = load_glyph_packs()[size][ch]
    w_text, h_text, baseline_text, row_hex = spec.split(",", 3)
    w, h, baseline = int(w_text), int(h_text), int(baseline_text)
    rows = [int(v, 16) for v in row_hex.split(".")]
    if len(rows) != h:
        raise RuntimeError(f"bad Press Start 2P raster row count: {size}px {ch!r}")
    mask = Image.new("L", (w, h), 0)
    for y, row in enumerate(rows):
        for x in range(w):
            if row & (1 << x):
                mask.putpixel((x, y), 255)
    if mask.getbbox() is None:
        raise RuntimeError(f"empty Press Start 2P glyph {size}px {ch!r}")
    if mask.width > CELL_W - 1 or mask.height > CELL_H - 1:
        raise RuntimeError(
            f"Press Start 2P glyph too large for FireRed cell: {size}px {ch!r} {mask.size}"
        )
    return mask, baseline


def patch_font(path: Path) -> tuple[str, dict[int, int]]:
    img = Image.open(path)
    if img.mode != "P" or img.width != COLS * CELL_W or img.height % CELL_H:
        raise RuntimeError(f"unexpected font atlas geometry/mode: {path} {img.mode} {img.size}")
    if path.name not in FONT_FILE_TO_WIDTH_TABLE or path.name not in VARIANT_PROFILE:
        raise RuntimeError(f"unmapped font variant {path.name}")

    total = COLS * (img.height // CELL_H)
    if max(TARGET_CODES) >= total:
        raise RuntimeError(f"atlas too small for bilingual target set: {path.name}")

    protected_before = {
        code: cell_pixels(img, code, total)
        for code in range(total)
        if code not in TARGET_CODES
    }

    source_size, target_baseline = VARIANT_PROFILE[path.name]
    rendered_widths: dict[int, int] = {}

    for ch, code in CHAR_TO_CODE.items():
        mask, source_baseline = source_mask(source_size, ch)
        top = target_baseline - source_baseline

        x0, y0, x1, y1 = cell_box(code, total)
        for y in range(y0, y1):
            for x in range(x0, x1):
                img.putpixel((x, y), FONT_BG)

        # +1 is the FireRed-style shadow offset.
        if mask.width + 1 > CELL_W:
            raise RuntimeError(
                f"{path.name}: horizontal overflow {ch}/0x{code:02X} width={mask.width + 1}"
            )
        if top < 0 or top + mask.height + 1 > CELL_H:
            raise RuntimeError(
                f"{path.name}: vertical overflow {ch}/0x{code:02X} y={top}..{top + mask.height + 1}"
            )

        for shadow_pass, color in ((True, FONT_SHADOW), (False, FONT_FG)):
            off = 1 if shadow_pass else 0
            for yy in range(mask.height):
                for xx in range(mask.width):
                    if mask.getpixel((xx, yy)):
                        img.putpixel((x0 + xx + off, y0 + top + yy + off), color)

        cell = img.crop((x0, y0, x1, y1))
        pts = [
            (x, y)
            for y in range(CELL_H)
            for x in range(CELL_W)
            if cell.getpixel((x, y)) in (FONT_FG, FONT_SHADOW)
        ]
        if not pts:
            raise RuntimeError(f"empty rendered Press Start 2P glyph {ch}/0x{code:02X}")
        min_x = min(x for x, _ in pts)
        max_x = max(x for x, _ in pts)
        if min_x != 0:
            raise RuntimeError(f"{path.name}: left origin drift {ch}/0x{code:02X} min_x={min_x}")

        # Variable advances keep the characteristic glyph shape while avoiding
        # the excessive width of the original monospaced desktop font.
        rendered_widths[code] = min(CELL_W, max(4, max_x + 1))

    for code, before in protected_before.items():
        if cell_pixels(img, code, total) != before:
            raise RuntimeError(
                f"SAFETY FAIL: non-target glyph 0x{code:02X} changed in {path.name}"
            )

    img.save(path, optimize=False)
    print(
        f"[press-start-2p-v314] {path.name}: {len(TARGET_CODES)} targets; "
        f"source={source_size}px baseline={target_baseline} "
        f"advances={sorted(set(rendered_widths.values()))}"
    )
    return FONT_FILE_TO_WIDTH_TABLE[path.name], rendered_widths


def patch_width_tables(path: Path, widths_by_table: dict[str, dict[int, int]]) -> None:
    text = path.read_text(encoding="utf-8")
    rx = re.compile(
        r"(?ms)^(?P<head>(?:ALIGNED\(4\)\s+)?const u8 "
        r"(?P<name>gFont[A-Za-z0-9_]*LatinGlyphWidths)\[\]\s*=\s*\{)"
        r"(?P<body>.*?)(?P<tail>^\};)"
    )
    matches = list(rx.finditer(text))
    names = {m.group("name") for m in matches}
    if names != EXPECTED_WIDTH_ARRAYS or set(widths_by_table) != EXPECTED_WIDTH_ARRAYS:
        raise RuntimeError(
            f"width-table mismatch tables={sorted(names)} profiles={sorted(widths_by_table)}"
        )

    replacements = []
    for m in matches:
        tokens = list(re.finditer(r"\b\d+\b", m.group("body")))
        if len(tokens) != 512:
            raise RuntimeError(f"{m.group('name')}: expected 512 widths, got {len(tokens)}")
        before = [int(t.group()) for t in tokens]
        after = list(before)
        widths = widths_by_table[m.group("name")]
        if set(widths) != TARGET_CODES:
            raise RuntimeError(f"{m.group('name')}: incomplete Press Start 2P widths")
        for code, width in widths.items():
            after[code] = width
        for code in range(512):
            if code not in TARGET_CODES and after[code] != before[code]:
                raise RuntimeError(f"SAFETY FAIL: non-target width 0x{code:02X} changed")
        base = m.start("body")
        for code in TARGET_CODES:
            tok = tokens[code]
            replacements.append((base + tok.start(), base + tok.end(), str(after[code])))

    for start, end, value in sorted(replacements, reverse=True):
        text = text[:start] + value + text[end:]
    path.write_text(text, encoding="utf-8")
    print(
        f"[press-start-2p-v314] 9 width tables patched at {len(TARGET_CODES)} English/Russian/digit codes"
    )


def verify_charmap(root: Path) -> None:
    text = (root / "charmap.txt").read_text(encoding="utf-8")
    if "'Щ' = 2F" not in text:
        raise RuntimeError("required Щ=0x2F charmap entry missing")
    if 0x1B in TARGET_CODES:
        raise RuntimeError("Press Start 2P target set unexpectedly includes legacy é slot")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    verify_charmap(root)
    font_dir = root / "graphics/fonts"
    paths = sorted(font_dir.glob("latin_*.png"))
    if len(paths) != 9:
        raise RuntimeError(f"expected 9 Latin atlases, got {len(paths)}")

    widths_by_table = {}
    for path in paths:
        table, widths = patch_font(path)
        widths_by_table[table] = widths

    patch_width_tables(root / "src/fonts.c", widths_by_table)

    audit = {
        "marker": MARKER,
        "font": "Press Start 2P compact GBA raster",
        "sourceLicense": "SIL Open Font License 1.1",
        "rasterSizes": [7],
        "rasterSource": "exact user-supplied PressStart2P-Regular.ttf",
        "rasterDataSha256": GLYPH_DATA_SHA256,
        "english": True,
        "russian": True,
        "digits": True,
        "punctuation": "native FireRed",
        "specialAccentedE": False,
        "accentedENormalization": "existing post-localization pass",
        "legacyAccentedESlotTouched": False,
        "shchaCode": "0x2F",
        "targetGlyphCells": len(TARGET_CODES),
        "variableWidthAdvances": True,
        "globalSizeAdjustment": "all 9 atlases use 7px source; advance padding reduced by 1px",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_font_press_start_2p_v3_14_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: Press Start 2P raster installed for English + Russian + digits; "
        "ordinary e policy preserved; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
