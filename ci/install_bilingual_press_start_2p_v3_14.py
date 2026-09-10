#!/usr/bin/env python3
"""Qarro v3.14 bilingual Press Start 2P font pass.

Replaces visible English letters, Russian letters and digits in all nine
FireRed Latin font atlases with compact, readability-first monochrome rasters
derived from the user-supplied Press Start 2P font (SIL Open Font License 1.1).

The TTF itself is not committed or redistributed by this installer. Two
pixel-sized raster packs (7 px and 8 px) are embedded so the build is fully
reproducible and does not depend on host font rendering. Punctuation and
unrelated/control cells remain native FireRed.

Pokemon, move and ability names can stay English while Russian UI/dialogue
uses the same visual alphabet. Literal é/É normalization remains handled by
the existing post-localization pass. Ash Bond / Ash Cap are not touched.
"""
from __future__ import annotations

import base64
import json
import re
import sys
import zlib
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

# Use true pixel-size rasters rather than squeezing one bitmap horizontally.
# Normal/short text gets the clearer 8 px source. Narrow/small contexts use
# the native 7 px raster so long Russian strings stay practical on 240x160.
VARIANT_PROFILE = {
    "latin_normal.png": ("8", 11),
    "latin_narrow.png": ("7", 11),
    "latin_narrower.png": ("7", 11),
    "latin_short.png": ("8", 10),
    "latin_short_narrow.png": ("7", 10),
    "latin_short_narrower.png": ("7", 10),
    "latin_small.png": ("7", 10),
    "latin_small_narrow.png": ("7", 10),
    "latin_small_narrower.png": ("7", 10),
}

_GLYPH_PACKS_B64 = {
    "7": 'eNqlWNm21UQQ/Zc890PSnXSS86aIIjgz6/IB8CrIpFz1oizWAnFABQXFCcQRAed5AoVf6PwRXV2dpHMOx7s7Z51e6+Zl36quYVftPpLckUyOJCvJRItkdzIpRbJzx/LSvj0HlpJJJZJDB1eWk8ljmRQqFUVGRyv+ePyoSO5EwCrzyOCDwGsQsKxEkQvlfvZDVoS8C/K5ELL0Bu3JapEVBF6LgDVbtB7TH60IeHc80OHugXCp0HTF2rmbC50SdB0C7a7YZsYn514PLlZJTt79OC/rEaN5JcJDSXUebwA9tqnJbFIK4dNUE/g+yGMR/JzD94M2tXIhqtsoO/ADaIiL24AfhOo/7avQ178L1UNRzcP940vq4Wi7NUU51wR+JM5uPUjRRtyyIs4Ia2NTdEHmBNsc1QRTQd4SBy7IZ8t2jma2QthadIcLLHPgbbhhNtmmi8DbkUjZnPDJgmA9CpJUoYXMyawFl57gdgywRYjVYW5tTrV0hCMJthMqCSbFqezsQixaW9ztbO4JnJ7YS0+ODrwEXpHZQnk3n4TSUTkGDSv3qYE1Pfd6rYfkM1vcPSamXDt7EGdzQfMmZP2nPSx3sCruHuBqNTwlofei/raTmGczQfch/uqZKbUfyqSNan8IdgCETQX1IF43YX0/gxSAmuX3Z0cUTu5o59AgmvPvV/b7yTJ4t5bPOf7PYWU23RLPI8ZCGue+fQG51oAQCbUCGQsInLN2GPRRyo63CfYikrTgXn23vwTRoOoZm/k6BVd3qftwOp8JnGH501NtJyM2DztiqnC+KGg2SbpmRdBwd8ghsUACgRIiyST9H+nqoAA3HkenUwutBlWKDsmYoSU6izO+ckuphK2g3OZEplJRkAu73rUFXEeth1yJmbb/hcDmzCKK0JzFYz0tCM27i8hJ8x64XtqQdfrBAc95YPl/o88KtEK2J6eT2Sqr3VJs3h+rKc1xMFWp30eyHvoBvp5aBvA8UPs93nyI10g+043mo4i1ul2N7XLta+Rj+NJDvAOfj1WYPBO86QugGB/kunP8k0WUprm4iJo3ny6iNc1nOBcVM9uP+Xy8VDVfjH7mMV+OE4zmq7hAy2FtX0LQbswEewMrRvP1IqrPXB6gq1VkX3ds2nj5M1dGXLxbHc3VWL3btqZDf4Ow6Czasah7lzDfIvZLmrSpp2CqGU7ad/jN+87sfP9+lITlpP0ATmp6f6l8zN2O6tA/Qt1RtBpG+Q/JXPgTuFF1rxuaI8fon8fpffMLaFU53i2GRPQrLsBUGObfQGHTTncH+n1Qk/N0VNpTfTDT/xj1VNCchWfbDNb8ieuVln0c7i/cVbto9rn4GxVj3C7dGPwnfn734Gug0azf8BzuOiSS0pmZ/S9ozw+/usX9hyvVwQJ8Y9xTgbkJisCp2dwcQ2TnoBEz7o7mOO6p6h1tXgY7MZjIzYnR2rh5ZX6xlauM4+bVcUq+eQ2M6ewIbl6PKJvg3aY5GftWwaOreQOhuNsP3OZNxGY/cH1C3oprjM7TU1C5dUOWeb85HdFOOqjStxGcH6yqH6nNO+CTNOfPt+HRW8DSy50=',
    "8": 'eNqlWNly1UYQ/Rc960GjZXTlNwjZNyAha+XBTpyYhOAEAw5QVAWy73H2FbKvkAQStpDlF0Z/RHfPSJqR78VHumXJyFSd6ZlezumeY9G2aOFYtB4tlHG0Ir+XFteW9+3dvxwtTOLowOr6WrTwcDqJizyuKn5UWtqvR47H0XYErTMH9T4YfAMETmKVpHEmP/ylE8buQLCZigvlTNJD35li8I0ImM/JNrUznZYMvWkEVA57MwbMY83GVCGupuPSfzH8FgTenrSNkQvTrQ6ttwiTSoPHhuk2yLSOg4dinDL4dnDfFBvaMx2bY1axAxh9B7Jv52TncYbdCRpVyrpKJfZt/XUXukDCsVK0SBszu8DdUGqnXW66uhCf7RxUVLauXJbtGmqXd841Ikm2e5Bh1Y/WPbhxilQa5Mm94zJUCXjPoOLoefu+YZWlGBcTIU4YfD9U1UmXYvJyytE6mTj9Adw+cbDHxAx+EHFbITTI7JcEbnsI5TJFkEKzbZXHZUOFiwG88OE6CLcmhLbJphm4BHG35c9esB5FbLK1hrTF4GM4g7mdNsUh8GX0oJZNMrfXx6HYaEu0/ZR+IrCpZx+03Snv3hpeGeNfm097kT3TJhPOhJ5OPOmwhWAnMzqJnLCUSPRv+1j2eArddaPkVtsZug/adT5d3p6Gosu9R+W/DN0PQntOXsXzyc/9Z5CU8HstpwnPjkqlSlL/QODZGVslBSi7RmcNPF0jATYKB8HEm1oshxCTPvO7wj4MnS5gT4atQyTUI/1CyP45cKce0zPsCBJC/3QdGRzFGLPsCN7Re4IOBknn14wKW3RRoeHMp1RkivcRrEw0IVBoWlnKMFXTcS4sRGi/D8kRNLmKYBSdQgnj00q5HLsAGyhLvWGnrMFpSPvEbaElKuSEsKf2q2cCES85mdq9ylYBEW/pbFeDOk6XmrSJTMY48+5c46fZgB2e9adP8948s6t5H2xY2WuxNweaDxxwcj2Z5EFQJYn3pvKmRRGrSvTSfDh+ijUnoDRnrXYdjQ/+aEjTm0uznKcNEcoKHw9IGt0vUfMJ3jHzjGKHMyXDmkubT0H7yZQ1ZIHP8LFWNb1K266Yz9G7gM0p0B7hi3lnXPPlXFcK5tQ8I645PYCywkfgX40fkc3Xc1w7mW/mmVPNtwNdHiqE+Q6BT7iv8jsP+lPEyXw/z6RpfgjQky1GzfaRGEq3ZX4cdfqmFTU/jZq1u5lbFvkZYt8Zi1j2tbH4BdkNOd9Go3tdKH8dwmEq3ImSS0xzZtQYbWvgLKj5zFm6CYX0wAL/DZKPspuX5Aj2u7CB+B1t05wT+KZNGDFtSfiPsRcQ5hxqPJPrrSRst8x5fO5rfgvuT2Te8HoGAf0VZOzM8S0PhMLvEy6Mu76oN+AeYTPYXBwyI+mwO7iEb7jw6fEyOFyJoIu9Vk2vDG4IQvzfqOmukRTcVWw6y6d1AP/Ax6089Rfov/jAHPbb/427ujD/o1NoT+jr55HJN6xRVzj1CXyvWbfV+iRYpD1tr18YP6PXL85Ov3JrYa9fGnerUL8MOXeqmNevDEkhT8brV8fcnjj5rl+DyHC2bNevI9Y92XYBemPAaRu5tjJdv4lAO5m2UlG/NYS0Ey9930aAjTQ7WbaSXL+DXq43MbVVevwaFgMF6w==',
}
GLYPH_PACKS = {
    size: json.loads(zlib.decompress(base64.b64decode(payload)).decode("utf-8"))
    for size, payload in _GLYPH_PACKS_B64.items()
}
for size, pack in GLYPH_PACKS.items():
    if set(pack) != set(CHAR_TO_CODE):
        raise RuntimeError(f"embedded Press Start 2P {size}px raster pack does not match target set")


def cell_box(code: int, total_cells: int) -> tuple[int, int, int, int]:
    if not 0 <= code < total_cells:
        raise RuntimeError(f"glyph code 0x{code:02X} outside atlas")
    x0 = (code % COLS) * CELL_W
    y0 = (code // COLS) * CELL_H
    return x0, y0, x0 + CELL_W, y0 + CELL_H


def cell_pixels(img: Image.Image, code: int, total_cells: int) -> bytes:
    return bytes(img.crop(cell_box(code, total_cells)).getdata())


def source_mask(size: str, ch: str) -> tuple[Image.Image, int]:
    g = GLYPH_PACKS[size][ch]
    w, h = int(g["w"]), int(g["h"])
    m = Image.new("L", (w, h), 0)
    for y, row in enumerate(g["rows"]):
        row = int(row)
        for x in range(w):
            if row & (1 << x):
                m.putpixel((x, y), 255)
    if m.getbbox() is None:
        raise RuntimeError(f"empty embedded glyph {size}px {ch!r}")
    return m, int(g["baseline"])


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

        rendered_widths[code] = min(CELL_W, max(4, max_x + 2))

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
        "embeddedRasterSizes": [7, 8],
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
