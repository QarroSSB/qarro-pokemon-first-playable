#!/usr/bin/env python3
"""Install Russian Cyrillic aliases, glyphs and matching text metrics.

Qarro v3.3.2 runtime font fix:
- Expansion Latin font PNGs are 16x16 pixels per glyph, 16 glyphs per row.
- Russian aliases reuse obsolete accented-Latin byte slots only.
- Cyrillic masks are left-aligned to the Latin glyph origin instead of centered.
- Hard-coded Latin glyph-width tables are updated for the 66 Cyrillic byte slots.
- Every non-Cyrillic glyph cell and width entry must remain unchanged.

This deliberately preserves ordinary English Pokemon / Move / Ability / Trainer
names and all other non-target glyphs. No Ash Bond / Ash Cap code is touched.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required: install python3-pil or Pillow") from exc

CYRILLIC = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
CYR_CODES = list(range(0x01, 0x2A)) + list(range(0x3B, 0x51)) + [0x5A, 0x68, 0x6F]
GLYPH_HEX = [
    "000000080814141c22220000","0000003e20203c22223c0000","0000003c22223c22223c0000",
    "0000003e2020202020200000","0000003c24242424247e4242","0000003e20203e20203e0000",
    "0014003e20203e20203e0000","000000545438385454540000","0000001c22021c02221c0000",
    "00000026262e2a3a32320000","0028380026262e2a3a323200","000000444850605048440000",
    "0000003c2424242424440000","0000002236362a2222220000","0000002222223e2222220000",
    "0000001c22222222221c0000","0000003e2222222222220000","0000003c22223c2020200000",
    "0000001e32202020321e0000","0000003e0808080808080000","0000002214141c0818300000",
    "000000081c2a2a2a1c080000","000000221414081414220000","0000004444444444447e0202",
    "0000002222223e0202020000","0000002a2a2a2a2a2a3e0000","0000005454545454547e0202",
    "00000060203c2222223c0000","0000004242724a4a4a720000","0000002020203c22223c0000",
    "0000003c26021e02263c0000","000000242a2a3a2a2a240000","0000003c44443c2424440000",
    "00000000003c021e223e0000","0000001e303c2222221c0000","00000000003c2438243c0000",
    "00000000003c202020200000","00000000003c2424247e4200","00000000001c223e201e0000",
    "00001400001c223e201e0000","000000000054383854540000","00000000001c2418043c0000",
    "0000000000242c2c34240000","0000283800242c2c34240000","000000000048507048440000",
    "00000000003c242424640000","00000000002236363e220000","000000000024243c24240000",
    "00000000001c2222221c0000","00000000003c242424240000","00000000003c2222223c2020",
    "00000000001c2020201c0000","00000000003e080808080000","000000000022141408080830",
    "00000808081c2a2a2a1c0808","000000000036140814360000","0000000000242424243e0200",
    "000000000024243c04040000","00000000002a2a2a2a3e0000","0000000000545454547e0200",
    "000000000060203e223e0000","000000000022223a2a3a0000","000000000020203c243c0000",
    "000000000038043c04380000","0000000000242a3a2a240000","00000000003c241c14240000",
]
assert len(CYRILLIC) == len(CYR_CODES) == len(GLYPH_HEX) == 66
assert len(set(CYR_CODES)) == len(CYR_CODES)
assert all(len(bytes.fromhex(glyph)) == 12 for glyph in GLYPH_HEX)

CELL_W = 16
CELL_H = 16
COLS = 16
FONT_BG = 0
FONT_FG = 1
FONT_SHADOW = 2

MARKER_START = "@ QARRO_RUSSIAN_CYRILLIC_START"
MARKER_END = "@ QARRO_RUSSIAN_CYRILLIC_END"
EXPECTED_WIDTH_ARRAYS = {
    "gFontSmallNarrowLatinGlyphWidths",
    "gFontSmallLatinGlyphWidths",
    "gFontNormalLatinGlyphWidths",
    "gFontShortLatinGlyphWidths",
    "gFontNarrowLatinGlyphWidths",
    "gFontNarrowerLatinGlyphWidths",
    "gFontSmallNarrowerLatinGlyphWidths",
    "gFontShortNarrowLatinGlyphWidths",
    "gFontShortNarrowerLatinGlyphWidths",
}


def glyph_geometry(hex_rows: str) -> tuple[int, int]:
    """Return source left edge and runtime advance including 1px shadow."""
    rows12 = bytes.fromhex(hex_rows)
    xs = [
        xx
        for row in rows12
        for xx in range(8)
        if row & (1 << (7 - xx))
    ]
    if not xs:
        raise RuntimeError("empty Cyrillic source glyph")
    left = min(xs)
    right = max(xs)
    width = (right - left + 1) + 1
    if not 1 <= width <= 8:
        raise RuntimeError(f"invalid calculated Cyrillic width {width}")
    return left, width


CYR_METRICS = {
    code: glyph_geometry(hex_rows)
    for code, hex_rows in zip(CYR_CODES, GLYPH_HEX)
}


def patch_charmap(root: Path) -> None:
    path = root / "charmap.txt"
    text = path.read_text(encoding="utf-8")
    lines = [MARKER_START, "@ 66 Russian aliases; obsolete Latin accent slots are reused intentionally."]
    lines.extend(f"'{ch}' = {code:02X}" for ch, code in zip(CYRILLIC, CYR_CODES))
    lines.append(MARKER_END)
    block = "\n".join(lines)
    if MARKER_START in text:
        start = text.index(MARKER_START)
        end = text.index(MARKER_END, start) + len(MARKER_END)
        text = text[:start] + block + text[end:]
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")
    print("[cyrillic] charmap: 66 Russian aliases installed")


def cell_box(code: int, total_cells: int) -> tuple[int, int, int, int]:
    if not 0 <= code < total_cells:
        raise RuntimeError(f"glyph code 0x{code:02X} outside atlas with {total_cells} cells")
    x0 = (code % COLS) * CELL_W
    y0 = (code // COLS) * CELL_H
    return x0, y0, x0 + CELL_W, y0 + CELL_H


def cell_pixels(img: Image.Image, code: int, total_cells: int) -> bytes:
    return bytes(img.crop(cell_box(code, total_cells)).getdata())


def patch_font(path: Path) -> None:
    img = Image.open(path)
    if img.mode != "P":
        raise RuntimeError(f"expected indexed P-mode font, got {img.mode}: {path}")
    if img.width != COLS * CELL_W or img.height % CELL_H:
        raise RuntimeError(f"unexpected Latin font atlas geometry {img.size}: {path}")

    rows = img.height // CELL_H
    total_cells = COLS * rows
    target_codes = set(CYR_CODES)
    if max(target_codes) >= total_cells:
        raise RuntimeError(f"atlas too small ({total_cells} cells) for Cyrillic mapping: {path}")

    protected_before = {
        code: cell_pixels(img, code, total_cells)
        for code in range(total_cells)
        if code not in target_codes
    }
    english_before = {
        code: cell_pixels(img, code, total_cells)
        for code in range(0xA1, min(0xEF, total_cells))
    }

    for ch, code, hex_rows in zip(CYRILLIC, CYR_CODES, GLYPH_HEX):
        rows12 = bytes.fromhex(hex_rows)
        source_left, expected_width = CYR_METRICS[code]
        x0, y0, x1, y1 = cell_box(code, total_cells)

        for y in range(y0, y1):
            for x in range(x0, x1):
                img.putpixel((x, y), FONT_BG)

        # Latin runtime glyphs begin at x=0 inside each cell. Normalize the
        # 8px source mask so its first foreground pixel also lands at x=0.
        ox = x0 - source_left
        # Source masks already contain vertical padding. Lowercase gets one
        # extra row to match the Latin lowercase baseline more closely.
        oy = y0 + (1 if ch.islower() else 0)

        for shadow_pass, color in ((True, FONT_SHADOW), (False, FONT_FG)):
            off = 1 if shadow_pass else 0
            for yy, row in enumerate(rows12):
                for xx in range(8):
                    if not (row & (1 << (7 - xx))):
                        continue
                    tx = ox + xx + off
                    ty = oy + yy + off
                    if x0 <= tx < x1 and y0 <= ty < y1:
                        img.putpixel((tx, ty), color)

        cell = img.crop((x0, y0, x1, y1))
        visible = [
            (x, y)
            for y in range(CELL_H)
            for x in range(CELL_W)
            if cell.getpixel((x, y)) in (FONT_FG, FONT_SHADOW)
        ]
        if not visible:
            raise RuntimeError(f"empty rendered Cyrillic glyph {ch} / 0x{code:02X}")
        min_x = min(x for x, _ in visible)
        max_x = max(x for x, _ in visible)
        if min_x != 0 or max_x + 1 != expected_width:
            raise RuntimeError(
                f"glyph geometry mismatch {ch} / 0x{code:02X}: "
                f"x={min_x}..{max_x}, expected width={expected_width}"
            )

    for code, before in protected_before.items():
        after = cell_pixels(img, code, total_cells)
        if after != before:
            raise RuntimeError(
                f"SAFETY FAIL: non-Cyrillic glyph 0x{code:02X} changed in {path.name}"
            )
    for code, before in english_before.items():
        after = cell_pixels(img, code, total_cells)
        if after != before:
            raise RuntimeError(
                f"SAFETY FAIL: protected English glyph 0x{code:02X} changed in {path.name}"
            )

    img.save(path, optimize=False)
    print(
        f"[cyrillic] patched {path.name}: {img.width}x{img.height}, "
        "66 left-aligned targets; non-target cells unchanged"
    )


def patch_width_tables(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    array_rx = re.compile(
        r"(?ms)^(?P<head>(?:ALIGNED\(4\)\s+)?const u8 "
        r"(?P<name>gFont[A-Za-z0-9_]*LatinGlyphWidths)\[\]\s*=\s*\{)"
        r"(?P<body>.*?)(?P<tail>^\};)"
    )
    matches = list(array_rx.finditer(text))
    names = {m.group("name") for m in matches}
    if names != EXPECTED_WIDTH_ARRAYS:
        raise RuntimeError(
            f"unexpected Latin width tables in {path}: "
            f"found={sorted(names)}, expected={sorted(EXPECTED_WIDTH_ARRAYS)}"
        )

    replacements: list[tuple[int, int, str]] = []
    target_codes = set(CYR_CODES)
    protected_codes = set(range(0xA1, 0xEF))

    for match in matches:
        body = match.group("body")
        tokens = list(re.finditer(r"\b\d+\b", body))
        if len(tokens) != 512:
            raise RuntimeError(
                f"{match.group('name')}: expected 512 width entries, got {len(tokens)}"
            )
        before = [int(t.group()) for t in tokens]
        after = list(before)
        for code in CYR_CODES:
            after[code] = CYR_METRICS[code][1]

        for code in range(512):
            if code not in target_codes and after[code] != before[code]:
                raise RuntimeError(
                    f"SAFETY FAIL: non-Cyrillic width 0x{code:02X} changed in {match.group('name')}"
                )
        for code in protected_codes:
            if after[code] != before[code]:
                raise RuntimeError(
                    f"SAFETY FAIL: English width 0x{code:02X} changed in {match.group('name')}"
                )

        body_start = match.start("body")
        for code in CYR_CODES:
            token = tokens[code]
            replacements.append(
                (body_start + token.start(), body_start + token.end(), str(after[code]))
            )

    for start, end, value in sorted(replacements, reverse=True):
        text = text[:start] + value + text[end:]

    path.write_text(text, encoding="utf-8")
    widths = sorted({CYR_METRICS[code][1] for code in CYR_CODES})
    print(
        f"[cyrillic] widths: patched {len(matches)} Latin tables at 66 target codes; "
        f"advances={widths}; English/non-target widths unchanged"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("upstream", type=Path)
    root = ap.parse_args().upstream.resolve()
    patch_charmap(root)

    font_dir = root / "graphics/fonts"
    paths = sorted(font_dir.glob("latin_*.png"))
    if len(paths) != 9:
        raise SystemExit(f"expected 9 latin_*.png font sheets in {font_dir}, got {len(paths)}")
    for path in paths:
        patch_font(path)

    patch_width_tables(root / "src/fonts.c")
    print(
        "[QARRO_CYRILLIC_V3_3_2] PASS: Cyrillic glyph origin + width metrics corrected; "
        "every non-target glyph/width verified unchanged; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
