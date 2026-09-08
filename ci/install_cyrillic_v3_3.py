#!/usr/bin/env python3
"""Qarro v3.3.3: make Cyrillic match each native Latin font variant.

Loads the proven v3.3.2 Cyrillic/charmap installer from commit 76c3201, keeps
its exact 66-character mapping, then replaces only glyph rendering/width
metrics. The previous installer drew the same 8x12 Cyrillic bitmap into all
nine Latin atlases, which made Russian text look oversized/deformed in
small/short/narrow UI fonts.

This pass derives uppercase/lowercase size and baseline from the untouched
Latin A/a glyphs in each atlas, scales Cyrillic per variant, measures the
rendered widths per atlas, and patches the matching width table. English and
all non-Cyrillic cells/widths are fail-closed and must remain byte-identical.

No Ash Bond / Ash Cap changes.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "76c3201fdf17391ad807308a9089491a5b7c03e1"
BASE_PATH = "ci/install_cyrillic_v3_3.py"


def load_base() -> dict:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )
    ns = {
        "__name__": "qarro_cyrillic_v332_base",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    return ns


NS = load_base()
Image = NS["Image"]
CYRILLIC = NS["CYRILLIC"]
CYR_CODES = NS["CYR_CODES"]
GLYPH_HEX = NS["GLYPH_HEX"]
CELL_W = NS["CELL_W"]
CELL_H = NS["CELL_H"]
COLS = NS["COLS"]
FONT_BG = NS["FONT_BG"]
FONT_FG = NS["FONT_FG"]
FONT_SHADOW = NS["FONT_SHADOW"]
EXPECTED_WIDTH_ARRAYS = NS["EXPECTED_WIDTH_ARRAYS"]
cell_box = NS["cell_box"]
cell_pixels = NS["cell_pixels"]

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

LATIN_UPPER_A = 0xBB
LATIN_LOWER_A = 0xD5
CYR_UPPER_A = CYRILLIC.index("А")
CYR_LOWER_A = CYRILLIC.index("а")


def source_bbox(hex_rows: str) -> tuple[int, int, int, int]:
    rows12 = bytes.fromhex(hex_rows)
    points = [
        (xx, yy)
        for yy, row in enumerate(rows12)
        for xx in range(8)
        if row & (1 << (7 - xx))
    ]
    if not points:
        raise RuntimeError("empty Cyrillic source glyph")
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    return min(xs), min(ys), max(xs), max(ys)


SOURCE_BBOXES = [source_bbox(glyph) for glyph in GLYPH_HEX]
SOURCE_UPPER_BASELINE = SOURCE_BBOXES[CYR_UPPER_A][3]
SOURCE_LOWER_BASELINE = SOURCE_BBOXES[CYR_LOWER_A][3]


def visible_bbox(img, code: int, total_cells: int) -> tuple[int, int, int, int]:
    cell = img.crop(cell_box(code, total_cells))
    points = [
        (x, y)
        for y in range(CELL_H)
        for x in range(CELL_W)
        if cell.getpixel((x, y)) != FONT_BG
    ]
    if not points:
        raise RuntimeError(f"empty reference Latin glyph 0x{code:02X} in {img.filename}")
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    return min(xs), min(ys), max(xs), max(ys)


def binary_source_mask(hex_rows: str, bbox: tuple[int, int, int, int]):
    left, top, right, bottom = bbox
    rows12 = bytes.fromhex(hex_rows)
    mask = Image.new("1", (right - left + 1, bottom - top + 1), 0)
    for yy in range(top, bottom + 1):
        row = rows12[yy]
        for xx in range(left, right + 1):
            if row & (1 << (7 - xx)):
                mask.putpixel((xx - left, yy - top), 1)
    return mask


def patch_font(path: Path) -> tuple[str, dict[int, int]]:
    img = Image.open(path)
    if img.mode != "P":
        raise RuntimeError(f"expected indexed P-mode font, got {img.mode}: {path}")
    if img.width != COLS * CELL_W or img.height % CELL_H:
        raise RuntimeError(f"unexpected Latin font atlas geometry {img.size}: {path}")
    if path.name not in FONT_FILE_TO_WIDTH_TABLE:
        raise RuntimeError(f"unmapped Latin font variant: {path.name}")

    total_cells = COLS * (img.height // CELL_H)
    target_codes = set(CYR_CODES)
    protected_before = {
        code: cell_pixels(img, code, total_cells)
        for code in range(total_cells)
        if code not in target_codes
    }
    english_before = {
        code: cell_pixels(img, code, total_cells)
        for code in range(0xA1, min(0xEF, total_cells))
    }

    upper_ref = visible_bbox(img, LATIN_UPPER_A, total_cells)
    lower_ref = visible_bbox(img, LATIN_LOWER_A, total_cells)

    # Reference boxes include native one-pixel down/right shadow.
    upper_fg_w = max(1, upper_ref[2] - upper_ref[0])
    upper_fg_h = max(1, upper_ref[3] - upper_ref[1])
    lower_fg_w = max(1, lower_ref[2] - lower_ref[0])
    lower_fg_h = max(1, lower_ref[3] - lower_ref[1])

    src_upper = SOURCE_BBOXES[CYR_UPPER_A]
    src_lower = SOURCE_BBOXES[CYR_LOWER_A]
    sx_upper = upper_fg_w / (src_upper[2] - src_upper[0] + 1)
    sy_upper = upper_fg_h / (src_upper[3] - src_upper[1] + 1)
    sx_lower = lower_fg_w / (src_lower[2] - src_lower[0] + 1)
    sy_lower = lower_fg_h / (src_lower[3] - src_lower[1] + 1)

    upper_target_baseline = upper_ref[3] - 1
    lower_target_baseline = lower_ref[3] - 1
    rendered_widths: dict[int, int] = {}

    for ch, code, hex_rows, bbox in zip(CYRILLIC, CYR_CODES, GLYPH_HEX, SOURCE_BBOXES):
        x0, y0, x1, y1 = cell_box(code, total_cells)
        for y in range(y0, y1):
            for x in range(x0, x1):
                img.putpixel((x, y), FONT_BG)

        lower = ch.islower()
        sx = sx_lower if lower else sx_upper
        sy = sy_lower if lower else sy_upper
        source_baseline = SOURCE_LOWER_BASELINE if lower else SOURCE_UPPER_BASELINE
        target_baseline = lower_target_baseline if lower else upper_target_baseline

        left, top, right, bottom = bbox
        dst_w = max(1, int(round((right - left + 1) * sx)))
        dst_h = max(1, int(round((bottom - top + 1) * sy)))
        mask = binary_source_mask(hex_rows, bbox).resize(
            (dst_w, dst_h), Image.Resampling.NEAREST
        )

        # Baseline-relative placement preserves accents above and real
        # descenders below the ordinary А/а body.
        bottom_offset = source_baseline - bottom
        dst_bottom = target_baseline - int(round(bottom_offset * sy))
        dst_top = dst_bottom - dst_h + 1

        if dst_w + 1 > CELL_W:
            raise RuntimeError(
                f"{path.name}: horizontal overflow {ch}/0x{code:02X}: width={dst_w + 1}"
            )
        if dst_top < 0 or dst_bottom + 1 >= CELL_H:
            raise RuntimeError(
                f"{path.name}: vertical overflow {ch}/0x{code:02X}: "
                f"y={dst_top}..{dst_bottom + 1}"
            )

        for shadow_pass, color in ((True, FONT_SHADOW), (False, FONT_FG)):
            off = 1 if shadow_pass else 0
            for yy in range(dst_h):
                for xx in range(dst_w):
                    if mask.getpixel((xx, yy)):
                        img.putpixel((x0 + xx + off, y0 + dst_top + yy + off), color)

        cell = img.crop((x0, y0, x1, y1))
        visible = [
            (x, y)
            for y in range(CELL_H)
            for x in range(CELL_W)
            if cell.getpixel((x, y)) in (FONT_FG, FONT_SHADOW)
        ]
        if not visible:
            raise RuntimeError(f"empty rendered Cyrillic glyph {ch}/0x{code:02X}")
        min_x = min(x for x, _ in visible)
        max_x = max(x for x, _ in visible)
        if min_x != 0:
            raise RuntimeError(
                f"{path.name}: Cyrillic origin drift {ch}/0x{code:02X}: min_x={min_x}"
            )
        rendered_widths[code] = max_x + 1

    for code, before in protected_before.items():
        if cell_pixels(img, code, total_cells) != before:
            raise RuntimeError(
                f"SAFETY FAIL: non-Cyrillic glyph 0x{code:02X} changed in {path.name}"
            )
    for code, before in english_before.items():
        if cell_pixels(img, code, total_cells) != before:
            raise RuntimeError(
                f"SAFETY FAIL: English glyph 0x{code:02X} changed in {path.name}"
            )

    img.save(path, optimize=False)
    table = FONT_FILE_TO_WIDTH_TABLE[path.name]
    print(
        f"[cyrillic-v333] {path.name}: upperRef={upper_ref} lowerRef={lower_ref} "
        f"scaleU={sx_upper:.2f}/{sy_upper:.2f} scaleL={sx_lower:.2f}/{sy_lower:.2f} "
        f"advances={sorted(set(rendered_widths.values()))}"
    )
    return table, rendered_widths


def patch_width_tables(path: Path, widths_by_table: dict[str, dict[int, int]]) -> None:
    text = path.read_text(encoding="utf-8")
    array_rx = re.compile(
        r"(?ms)^(?P<head>(?:ALIGNED\(4\)\s+)?const u8 "
        r"(?P<name>gFont[A-Za-z0-9_]*LatinGlyphWidths)\[\]\s*=\s*\{)"
        r"(?P<body>.*?)(?P<tail>^\};)"
    )
    matches = list(array_rx.finditer(text))
    names = {m.group("name") for m in matches}
    if names != EXPECTED_WIDTH_ARRAYS or set(widths_by_table) != EXPECTED_WIDTH_ARRAYS:
        raise RuntimeError(
            f"width-table/profile mismatch: tables={sorted(names)}, "
            f"profiles={sorted(widths_by_table)}"
        )

    replacements = []
    target_codes = set(CYR_CODES)
    protected_codes = set(range(0xA1, 0xEF))
    for match in matches:
        name = match.group("name")
        tokens = list(re.finditer(r"\b\d+\b", match.group("body")))
        if len(tokens) != 512:
            raise RuntimeError(f"{name}: expected 512 widths, got {len(tokens)}")
        before = [int(t.group()) for t in tokens]
        after = list(before)
        per_font = widths_by_table[name]
        if set(per_font) != target_codes:
            raise RuntimeError(f"{name}: incomplete Cyrillic metrics")
        for code in CYR_CODES:
            after[code] = per_font[code]
        for code in range(512):
            if code not in target_codes and after[code] != before[code]:
                raise RuntimeError(
                    f"SAFETY FAIL: non-Cyrillic width 0x{code:02X} changed in {name}"
                )
        for code in protected_codes:
            if after[code] != before[code]:
                raise RuntimeError(
                    f"SAFETY FAIL: English width 0x{code:02X} changed in {name}"
                )
        body_start = match.start("body")
        for code in CYR_CODES:
            tok = tokens[code]
            replacements.append(
                (body_start + tok.start(), body_start + tok.end(), str(after[code]))
            )

    for start, end, value in sorted(replacements, reverse=True):
        text = text[:start] + value + text[end:]
    path.write_text(text, encoding="utf-8")
    print("[cyrillic-v333] 9 per-font width tables patched; English widths unchanged")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    # Keep proven mapping; render metrics are replaced below.
    NS["patch_charmap"](root)

    font_dir = root / "graphics/fonts"
    paths = sorted(font_dir.glob("latin_*.png"))
    if len(paths) != 9:
        raise RuntimeError(f"expected 9 Latin atlases, got {len(paths)}")

    widths_by_table = {}
    for path in paths:
        table, widths = patch_font(path)
        if table in widths_by_table:
            raise RuntimeError(f"duplicate font table mapping: {table}")
        widths_by_table[table] = widths

    patch_width_tables(root / "src/fonts.c", widths_by_table)
    print(
        "[QARRO_CYRILLIC_V3_3_3] PASS: native per-variant Cyrillic "
        "size/baseline/width metrics installed; English/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
