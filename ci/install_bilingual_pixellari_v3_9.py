#!/usr/bin/env python3
"""Qarro v3.9 bilingual Pixellari Cyrillic font pass.

Replaces visible English letters, Russian letters and digits in all nine
FireRed Latin font atlases with a readability-first raster derived from the
user-supplied Pixellari Cyrillic font (SIL Open Font License 1.1).

Only monochrome raster masks are embedded here; the original TTF is not
committed or redistributed by this build script. Punctuation and all unrelated
font cells remain native FireRed. The user chose ordinary e/E instead of a
special accented e; literal é/É normalization is handled by the existing
post-localization pass, and byte 0x1B stays outside the target set.

No Ash Bond / Ash Cap changes.
"""
from __future__ import annotations

import base64
import json
import re
import sys
import zlib
from pathlib import Path

from PIL import Image

MARKER = "QARRO_BILINGUAL_PIXELLARI_V3_9"
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
    raise RuntimeError("0x1B/é must remain outside Pixellari target cells")

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

VARIANT_PROFILE = {
    "latin_normal.png": (1.00, 1.00, 11),
    "latin_narrow.png": (0.85, 1.00, 11),
    "latin_narrower.png": (0.72, 1.00, 11),
    "latin_short.png": (1.00, 0.90, 10),
    "latin_short_narrow.png": (0.82, 0.90, 10),
    "latin_short_narrower.png": (0.70, 0.90, 10),
    "latin_small.png": (0.85, 0.85, 10),
    "latin_small_narrow.png": (0.76, 0.85, 10),
    "latin_small_narrower.png": (0.66, 0.85, 10),
}

_GLYPH_PACK_B64 = 'eNqtWVe33DQQ/i9+1oMlW1r7vgGh994ODwlcSCAFcoEL5OQcEnon9N4h9N5D+QvyP2JG1tqWRyN7dzmWzvruud+MZjQzmk97LDsr2zqW7WZbRmT7s61KZEeP7O5kWzcXuTCF0BJH96LlLSLbt3dn++CBw9vw38dFdjaD7zCF7MDwTvDn8PoR4B98zQl2z5RundZ9rsfrsW6vuNNPoefNhRLk+RNIxKoFDlkS8AWMxZ2VoekEf6HHFyP8ovM0PguCu4hZtKqEVOEohCHwi7lN1kLWQkqxgAc+4I9CE/QlnMeCRUc26VIPrEZAWWuh0M2ovNbjSeRc5uUsRnJqgOdFO3H1uGeqcLOuiZTLV4pWGu1X8IHTxguq10zUXcmYMFZeYwRJRbfwqlXyPBJ5V/N4fIwSZYUjbvs1PHocfzgI/tqpvJnw/XWz8VC3IvqvT0Sii0aIxOGUFTiFbsINzC5KgOgSnVgJSEn4hL8iIXjjDLx/CPYmxgSltagNJAAoNahdgiAB3xIJe4MANr32sg9gGCP3G0DuS1QACPkhWlK9tyb1ogxabFHrbVzRA1yJG51YNerdTuuVrOLbmSptsDb3BY8ovINz03ipuP6Ro1Dv/rSbpRyKIdoPeLQi6HxYpgnuTo8rHU7mvZ+UyKPpHTmg7uJOmLZ5aEtja0CkOB1kl14kl34oyInBDoOaWo6zmvj7MBcgSV8j8si8VIrE1t3MHpM0IgYj+p5VIkxR7Ud5i9Ui6mZE7TCoAgMLTK6YeL6XyaMiyCNaZu9j9A1NVCZWqO6fgYQIp47ZZSJpfDAoCcZqin+Ac2zdnkg48IUG4YNclQviyI1x4iH8IW5vsB+Cg8DQ1gxheaILJiPSCEsGj42k6Z5IT6gSXZSr68sTbBFDF1NosNmLifbvJVOmWr2ts6Gn8SIoXk/SjpR2w+X+8iCUbOlA+CLRwrn2rbWfbcKqpHpIiwn99VQDvCw7DN6+uCHXtacmmtgiSTftSxtyZfvyJHdkDir7SlBfBoesgaIARaIOBzZ1HBuyr65Pm+2JAFv3MZCLCXiN8Nc8HA0IqRh4rCyQPmC1y90nTvyukrQTtq8n7x2GmRxnBPYNnhQiL8QzPF90/NB9S4W8GQgZbAuYkDsBs2TJHIW9tRHLtm9z5ACdgW7NFZkxm975n1i3fXfDyw773oaM276/ioDYCj6YIWAZ8BT9IR+jhe6zXUfX/tGGlNl+PMP9LWeHEcv1TzjGiMllKOfF7yJV+9MNSa/9LEwymWb/rnc37aCyTq/ilJKyaPs55xTS6A1mhEzbL8JSODCrhHduQtJC72uq5aRyv+TSV/tYURpmXnZTxjbtKy+lHoduBce0n2UJE6K3mxHubr9OELvpE/cb7tpLuSpq3Fnhd7uGEKISvmUM0VCQe8fqwMmqjCTzd1OlAAM4VUu+5zlf4e6dMH+i1yf2h9SJjVQv3XjZH5O0raOrEQpmf+L5QcESPvszt+sBLe62nwr4Zd27l+YU16W6EzkFd676NYi4gWJZuNICuwxDugM5YvhviXW7BKzcJ123/Z2nnh2Ril8m2D/4xjwXabyz+U9eNcSG6zp0VPGZYJvNMD2hlvcjEld/MdC2BHNdvIP+nSTpgxCj0H/Wvnex//KJENwrUK3Nw/ydTc99JHdn05xY8/6zOckvuePYFPXIZhcKzaMcVVkybHe7PDwcfesQ6x6ax9a+GGken2GID5joZVfzxGSglRz0ydn3QbQ9cAKeWqXPcGxP4aSCnuYKmu8HYEfyyk1DT57mGQbtWdLgFzMpaao2z3IRGPxOGjH/OaY8tPQOSG/0pyYHfZ671JU+6GCxXc8a0/0Cf13pLynimX78P3KuO1o='
GLYPHS = json.loads(zlib.decompress(base64.b64decode(_GLYPH_PACK_B64)).decode("utf-8"))
if set(GLYPHS) != set(CHAR_TO_CODE):
    raise RuntimeError("embedded Pixellari raster pack does not match target set")


def cell_box(code: int, total_cells: int) -> tuple[int, int, int, int]:
    if not 0 <= code < total_cells:
        raise RuntimeError(f"glyph code 0x{code:02X} outside atlas")
    x0 = (code % COLS) * CELL_W
    y0 = (code // COLS) * CELL_H
    return x0, y0, x0 + CELL_W, y0 + CELL_H


def cell_pixels(img: Image.Image, code: int, total_cells: int) -> bytes:
    return bytes(img.crop(cell_box(code, total_cells)).getdata())


def source_mask(ch: str) -> tuple[Image.Image, int]:
    g = GLYPHS[ch]
    w, h = int(g["w"]), int(g["h"])
    m = Image.new("L", (w, h), 0)
    for y, row in enumerate(g["rows"]):
        row = int(row)
        for x in range(w):
            if row & (1 << x):
                m.putpixel((x, y), 255)
    return m, int(g["baseline"])


def resize_binary(mask: Image.Image, sx: float, sy: float) -> Image.Image:
    w = max(1, int(round(mask.width * sx)))
    h = max(1, int(round(mask.height * sy)))
    out = mask.resize((w, h), Image.Resampling.NEAREST)
    out = out.point(lambda p: 255 if p else 0)
    if out.getbbox() is None:
        raise RuntimeError("empty Pixellari mask after resize")
    return out


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

    sx, sy, target_baseline = VARIANT_PROFILE[path.name]
    rendered_widths: dict[int, int] = {}

    for ch, code in CHAR_TO_CODE.items():
        src, src_baseline = source_mask(ch)
        mask = resize_binary(src, sx, sy)
        scaled_baseline = max(0, int(round(src_baseline * sy)))
        top = target_baseline - scaled_baseline

        x0, y0, x1, y1 = cell_box(code, total)
        for y in range(y0, y1):
            for x in range(x0, x1):
                img.putpixel((x, y), FONT_BG)

        if mask.width + 1 > CELL_W:
            raise RuntimeError(
                f"{path.name}: horizontal overflow {ch}/0x{code:02X} width={mask.width + 1}"
            )
        if top < 0 or top + mask.height >= CELL_H:
            raise RuntimeError(
                f"{path.name}: vertical overflow {ch}/0x{code:02X} y={top}..{top + mask.height}"
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
            raise RuntimeError(f"empty rendered Pixellari glyph {ch}/0x{code:02X}")
        min_x = min(x for x, _ in pts)
        max_x = max(x for x, _ in pts)
        if min_x != 0:
            raise RuntimeError(f"{path.name}: left origin drift {ch}/0x{code:02X} min_x={min_x}")
        rendered_widths[code] = min(CELL_W, max_x + 2)

    for code, before in protected_before.items():
        if cell_pixels(img, code, total) != before:
            raise RuntimeError(
                f"SAFETY FAIL: non-target glyph 0x{code:02X} changed in {path.name}"
            )

    img.save(path, optimize=False)
    print(
        f"[pixellari-v39] {path.name}: {len(TARGET_CODES)} targets; "
        f"scale={sx:.2f}/{sy:.2f} baseline={target_baseline} "
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
            raise RuntimeError(f"{m.group('name')}: incomplete Pixellari widths")
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
        f"[pixellari-v39] 9 width tables patched at {len(TARGET_CODES)} English/Russian/digit codes"
    )


def verify_charmap(root: Path) -> None:
    text = (root / "charmap.txt").read_text(encoding="utf-8")
    if "'Щ' = 2F" not in text:
        raise RuntimeError("required Щ=0x2F charmap entry missing")
    if 0x1B in TARGET_CODES:
        raise RuntimeError("Pixellari target set unexpectedly includes legacy é slot")


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
        "font": "Pixellari Cyrillic readability raster",
        "license": "SIL Open Font License 1.1",
        "english": True,
        "russian": True,
        "digits": True,
        "punctuation": "native FireRed",
        "specialAccentedE": False,
        "accentedENormalization": "existing post-localization pass",
        "legacyAccentedESlotTouched": False,
        "shchaCode": "0x2F",
        "targetGlyphCells": len(TARGET_CODES),
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_font_pixellari_v3_9_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: Pixellari raster installed for English + Russian + digits; "
        "ordinary e policy preserved; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
