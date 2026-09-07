#!/usr/bin/env python3
"""Install Russian Cyrillic aliases and glyphs into Expansion Latin fonts.

This is the source-migration version of the previously verified RU font work.
It deliberately reuses obsolete accented Latin byte slots so ordinary English
Pokemon / Move / Ability / Trainer names remain untouched.
"""
from __future__ import annotations

import argparse
from collections import Counter
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
assert all(len(bytes.fromhex(glyph)) == 12 for glyph in GLYPH_HEX)

MARKER_START = "@ QARRO_RUSSIAN_CYRILLIC_START"
MARKER_END = "@ QARRO_RUSSIAN_CYRILLIC_END"


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


def _ranked_non_bg_pixels(img: Image.Image, bg, cell_w: int, cell_h: int, code: int):
    x0 = (code % 16) * cell_w
    y0 = (code // 16) * cell_h
    counts = Counter(
        img.getpixel((x, y))
        for y in range(y0, min(y0 + cell_h, img.height))
        for x in range(x0, min(x0 + cell_w, img.width))
        if img.getpixel((x, y)) != bg
    )
    return [p for p, _ in counts.most_common()]


def sample_colors(img: Image.Image, cell_w: int, cell_h: int):
    """Find usable ink/shadow indices even on sparse Latin font sheets."""
    bg = img.getpixel((0, 0))

    # Common glyphs: A, a, 0, !, ?, O, o. Different sheets populate different sets.
    for code in (0xBB, 0xD5, 0xA1, 0xAB, 0xAC, 0xC9, 0xE3):
        ranked = _ranked_non_bg_pixels(img, bg, cell_w, cell_h, code)
        if ranked:
            ink = ranked[0]
            shadow = ranked[1] if len(ranked) > 1 else ranked[0]
            return bg, ink, shadow

    # Sparse sheet fallback: use colors that occur anywhere in the actual image.
    counts = Counter(pixel for pixel in img.getdata() if pixel != bg)
    if counts:
        ranked = [p for p, _ in counts.most_common()]
        ink = ranked[0]
        shadow = ranked[1] if len(ranked) > 1 else ranked[0]
        return bg, ink, shadow

    # Completely blank indexed sheet fallback: derive usable indices from its palette.
    palette = img.getpalette()
    if palette is not None and isinstance(bg, int):
        bg_rgb = tuple(palette[bg * 3:bg * 3 + 3])
        distinct = []
        for idx in range(len(palette) // 3):
            if idx == bg:
                continue
            rgb = tuple(palette[idx * 3:idx * 3 + 3])
            if rgb != bg_rgb:
                distinct.append(idx)
            if len(distinct) >= 2:
                break
        if distinct:
            ink = distinct[0]
            shadow = distinct[1] if len(distinct) > 1 else distinct[0]
            print("[cyrillic] sparse blank font sheet: using palette fallback")
            return bg, ink, shadow

    raise RuntimeError("could not determine usable ink colors from font sheet or palette")


def patch_font(path: Path) -> None:
    img = Image.open(path)
    if img.mode != "P":
        img = img.convert("P")
    if img.width % 16 or img.height % 16:
        raise RuntimeError(f"unexpected font grid {img.size}: {path}")
    cell_w, cell_h = img.width // 16, img.height // 16
    if cell_w < 8 or cell_h < 12:
        raise RuntimeError(f"font cells too small {cell_w}x{cell_h}: {path}")
    bg, ink, shadow = sample_colors(img, cell_w, cell_h)
    scale = max(1, min(cell_w // 8, cell_h // 12))
    glyph_w, glyph_h = 8 * scale, 12 * scale

    for code, hex_rows in zip(CYR_CODES, GLYPH_HEX):
        rows = bytes.fromhex(hex_rows)
        x0, y0 = (code % 16) * cell_w, (code // 16) * cell_h
        for y in range(y0, y0 + cell_h):
            for x in range(x0, x0 + cell_w):
                img.putpixel((x, y), bg)
        ox = x0 + max(0, (cell_w - glyph_w) // 2)
        oy = y0 + max(0, (cell_h - glyph_h) // 2)
        for shadow_pass, color in ((True, shadow), (False, ink)):
            off = scale if shadow_pass else 0
            for yy, row in enumerate(rows):
                for xx in range(8):
                    if not (row & (1 << (7 - xx))):
                        continue
                    px, py = ox + xx * scale + off, oy + yy * scale + off
                    for dy in range(scale):
                        for dx in range(scale):
                            tx, ty = px + dx, py + dy
                            if x0 <= tx < x0 + cell_w and y0 <= ty < y0 + cell_h:
                                img.putpixel((tx, ty), color)
    img.save(path, optimize=False)
    print(f"[cyrillic] patched {path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("upstream", type=Path)
    root = ap.parse_args().upstream.resolve()
    patch_charmap(root)
    font_dir = root / "graphics/fonts"
    paths = sorted(font_dir.glob("latin_*.png"))
    if not paths:
        raise SystemExit(f"no latin_*.png in {font_dir}")
    for path in paths:
        patch_font(path)
    print(f"[QARRO_CYRILLIC_V3_3] PASS: {len(paths)} Latin font sheets patched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
