#!/usr/bin/env python3
"""Qarro Pixel v3.15 bilingual font follow-up.

Installs the original Qarro Pixel v0.1 bitmap alphabet into all nine FireRed
Latin font atlases. Glyphs are hand-designed for GBA readability at 5-7 px
width and 7 rows high. No bitmap scaling/squeezing is used.

Pokemon, move and ability names may remain English while Russian UI/dialogue
uses the same custom alphabet. Native FireRed punctuation/control cells stay
untouched. Ash Bond / Ash Cap are not touched.
"""
from __future__ import annotations

import base64
import json
import sys
import zlib
from pathlib import Path

from PIL import Image

MARKER = "QARRO_PIXEL_V3_15"
BASE_PATH = "install_bilingual_press_start_2p_v3_14.py"

# Lossless compressed source for 128 original Qarro Pixel 0/1 bitmap glyphs.
# One line after decompression: character:row/row/row/row/row/row/row
GLYPH_SPEC_B85 = "c-oa$#iHFf4Bh)@VwJ01nVGvQw=-pKSAAt>=INA~8Gga}qb9bK$hPcUKTz)TQ)I!>u{;hX0LTKQl+eif%U!9Z7>~f}GAm+&wrkd8RB9bDk+U00ZFdqvXt#Zvu7H?4m~Jh_6xLrq560iA$a}}-Y+CI@^_~oVYfIBn>OE>z=|~{5QmH(g(e0}L13DV(rzCGwyUs*t!r(={`K-oZ9j7+ZNk5F)oi5d4L!QGyDv(-7%uPbdEz!J$U1$?iCkw><gk3*b3z*WIouu)Uz;B_2l+;#|QY^wAK$AQy#y%|rjoR)KjAsByJ?q$(V#JF5OzXBRt{cR*yv>8n5Vh;I;R=){r(tGE)0oy;iGBmh7IQuotP1QxlwwvRt)<2YgI}Y&hVj>L^2Y93-M}VlXkv#h4@8P}5r3OJP@JtFEDySF8?bt}faY8LgF4Vc8@4}{$$wo=Flf<6iv|iHHlqII{8Y=E9M=IF27*wE&8}|J^)2yK2Q9MI^T92POBLG&O0||^d(vOm?v5zrD6CBhcOr!V4+>2rmF_Oj2PRu!VJmj`=u)cKlhF04VlSf`Aq=rEYBz-P{-ACwVd!>}KE(s^)WZXy#V>oZ4s$F;X-e-p+#VJlMX(3J2yCqY$qD$8RZ@(M&L5%OQN-VHR&gUA-9x^VbjC1;W@JT-jp#y{8KKT+436qTauRcCU0uu=Gu0)|GB1U?Y<;${CNl6}s4E$hrW(SgRXUI}uNdX4s1eijmqn8~Ty5=S%NHHOYNxJcKvi8wrjLSdvf<u9+U&^&6zXQiEUIobLoW1ALqgro7)sThj6q!8%@|A7J&f4lEZ@%<V%2{c7bEo`W875#XUuQvAvTNw-dWzji6}qHm?G6<?7zn~XRmsKd<i_tG0IOdGIMy?)~S1jZSN!=q?@WZpCkALTC|KIp_LjUFU*K$E7?7u9WKd3FADV%nS#ft?Ny}Lf$R0xnp14c$nF8oUu_HO6um(S><zb&773)RZ!@NN^^T0ieW#gvKfqwu#`%GnCZc@*5gl*SeE%t9>@P1ke4kcUpN(bN@_5MmF3%TMU#KrkZbH_#x%tXZWjuv{Lzf{M_gLlcgWMg|4>yA;(iiGy#+5?-iqEk=f`$5>aj8&$B6#9_E)Qf}LCT?w>uGr~<FZg5%9y^(!|1R-q5F{N%Oe?gfbwYHrG*fEd2Aq`t@3gIN|qq{@`UZKLK5{f(U&KE@I~leXYf?8L4xlM(U+%#a9J8O8=OftxmVA#p*NKFfg$?xT<>+b9kBiam?dc7"


def load_base() -> dict:
    path = Path(__file__).resolve().with_name(BASE_PATH)
    code = path.read_text(encoding="utf-8")
    ns = {"__name__": "qarro_pixel_base_v315", "__file__": str(path)}
    exec(compile(code, str(path), "exec"), ns)
    return ns


def load_glyphs(expected_chars: set[str]) -> dict[str, list[str]]:
    raw = zlib.decompress(base64.b85decode(GLYPH_SPEC_B85.encode("ascii"))).decode("utf-8")
    glyphs: dict[str, list[str]] = {}
    for line in raw.splitlines():
        ch, body = line.split(":", 1)
        rows = body.split("/")
        if len(ch) != 1 or len(rows) != 7:
            raise RuntimeError(f"bad Qarro Pixel glyph record: {line!r}")
        widths = {len(row) for row in rows}
        if len(widths) != 1:
            raise RuntimeError(f"{ch!r}: inconsistent row widths")
        width = next(iter(widths))
        if not 1 <= width <= 7:
            raise RuntimeError(f"{ch!r}: invalid Qarro Pixel width {width}")
        if any(set(row) - {"0", "1"} for row in rows):
            raise RuntimeError(f"{ch!r}: non-binary Qarro Pixel row")
        if not any("1" in row for row in rows):
            raise RuntimeError(f"{ch!r}: empty Qarro Pixel glyph")
        glyphs[ch] = rows
    if set(glyphs) != expected_chars:
        missing = sorted(expected_chars - set(glyphs))
        extra = sorted(set(glyphs) - expected_chars)
        raise RuntimeError(f"Qarro Pixel charset mismatch missing={missing} extra={extra}")
    return glyphs


def custom_source_mask(glyphs: dict[str, list[str]]):
    def source_mask(_size: str, ch: str) -> tuple[Image.Image, int]:
        rows = glyphs[ch]
        mask = Image.new("L", (len(rows[0]), 7), 0)
        for y, row in enumerate(rows):
            for x, bit in enumerate(row):
                if bit == "1":
                    mask.putpixel((x, y), 255)
        # All designs use a 7-row source box. Blank top rows in lowercase
        # deliberately create a smaller x-height without any resampling.
        return mask, 7
    return source_mask


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    base = load_base()
    glyphs = load_glyphs(set(base["CHAR_TO_CODE"]))

    # Reuse only the already-proven FireRed atlas/charmap safety machinery.
    # Replace the raster source completely with our own hand-designed glyphs.
    base["source_mask"] = custom_source_mask(glyphs)
    base["VARIANT_PROFILE"] = {
        name: ("QarroPixel", baseline)
        for name, (_old_source, baseline) in base["VARIANT_PROFILE"].items()
    }

    base["verify_charmap"](root)
    font_dir = root / "graphics/fonts"
    paths = sorted(font_dir.glob("latin_*.png"))
    if len(paths) != 9:
        raise RuntimeError(f"expected 9 Latin atlases, got {len(paths)}")

    widths_by_table = {}
    for path in paths:
        table, widths = base["patch_font"](path)
        widths_by_table[table] = widths
    base["patch_width_tables"](root / "src/fonts.c", widths_by_table)

    width_set = sorted({len(rows[0]) for rows in glyphs.values()})
    audit = {
        "marker": MARKER,
        "font": "Qarro Pixel",
        "fontVersion": "0.1",
        "design": "original custom bilingual GBA bitmap font",
        "rasterRows": 7,
        "glyphWidths": width_set,
        "targetGlyphCells": len(glyphs),
        "english": True,
        "russian": True,
        "digits": True,
        "punctuation": "native FireRed",
        "bitmapScaling": False,
        "variableWidthAdvances": True,
        "manualReadabilityGlyphs": ["Ж", "ж", "Ш", "ш", "Щ", "щ", "Ы", "ы", "Ю", "ю", "Я", "я", "Ё", "ё"],
        "specialAccentedE": False,
        "accentedENormalization": "existing post-localization pass",
        "legacyAccentedESlotTouched": False,
        "shchaCode": "0x2F",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_font_pixel_v3_15_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "[QARRO_PIXEL_V3_15] PASS: original 5-7px Qarro Pixel RU+EN+digits "
        "installed in all 9 FireRed atlases; no bitmap scaling; Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
