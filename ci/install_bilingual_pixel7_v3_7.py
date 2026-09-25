#!/usr/bin/env python3
"""Qarro v3.7 bilingual Cyrillic Pixel-7 bitmap font pass.

Replaces the visible English/Russian alphabet and digits in all nine FireRed
Latin font atlases with bitmap glyphs rasterized from the user-supplied
"cyrillic_pixel-7.ttf" at a native pixel-friendly size.

The original font file is NOT committed or redistributed. Only rasterized
monochrome glyph masks are embedded here.

User decision for accented e:
- do NOT create/use a special é glyph;
- a post-localization pass normalizes literal é/É to ordinary e/E;
- leave FireRed's legacy 0x1B charmap slot untouched and unused.

This pass runs after the proven Cyrillic/charmap installer, keeps Щ at 0x2F,
patches per-atlas width tables only for English/Russian/digit cells, and leaves
all other glyph cells byte-identical.

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

MARKER = "QARRO_BILINGUAL_PIXEL7_V3_7"
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
    raise RuntimeError("0x1B/é must remain outside Pixel-7 target cells")

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

_GLYPH_PACK_B85 = """c-pO4SF_zT5dJTI)`KKB`MyDb&^si+@Q}cT1VRG2zy&gyA&pK7z4zWp==Cqi|0r5X$CiBTb9b#fN6y%pyQ|&Rx2xUnNOnoKb|l-
()+(0m%hno}?cKAneqjH>b^CGn(B?+Ac2||NQm{h7swBL-RpoadW!a@z6%CU$6M~5nUd*RiPQ?zq6?ylA4*}AbVWh)Ny9M@?pyG0
x0Y+J5!4<Q_%@2fk5`~-
o0CElruEZz^4y~8B3shX?RTNu<u!?>zc2`p&6mIW4xCZ4xGY+A$0TtI`ROBp=0p#F!otG7SrTbiRri3z2GxdPB>j}qE+JBqjaom6
p>GE=ryb+(3i$n-
Pc~c|~fuWdS{y&$X=H`^z;12c{N_t2pRgW?kiCeL!o7+<?)bau~w~?}JDIlQYc09~S3Y87$E|fDX5NZ(&PzG(gNj@1Paz2FW9n`R
x3uJIWcTx+8DB}Fx;}w)vK^-cn``ot<$ilALI%9X=8wsx{9JLqgmXp5+zq!k=PV!#N&fZ`(zWF-A^P1J+?)Rbm=C;g-
RUc&UCv6MH7yZWjW(Qo>Aip1TS5=J1cDuXk0c6Pe!swz$jI;hhto5DMLPX{tz?ff;-
n0*SQMD@UvNYD3JRf;L$3e`|O+@|>MphI<VQ2iqWT^V9=#e>Kg9XBeiMxjGZcs8i#`vQclvKmqa?Q|Vm~G|q5!qYn@p-
~FR+}hzjYEqW*ny5GNc#s^0pTY}!lpKbA%BW=38=6Xa$399Ec&*f-4gS&TFw~3qU$e5wZ6{q3Y-
@bUSKue{DO9in_Gbo`=gRL!v)iTbE6_F7_?V4HIU0qo+2T^A$VX#L+#zehRCVVXVa&0eJ(Ye`jzy-UcWkLviF5wzvhMO)k6peKrZ
*(!q`&T4AZZtjraOkR9lRvfdcsIOA}{(tLN2pWk$b2YTk2hZUpnEvXu6HFlOpE)6-
tRMacUmm{@}WK))T2ic`TcyK}aMs&~?P0R1lNtS2zz?Raln2?70nIzgj9NT&q!hbcO|9UrCf3i{(Ds!xBiJ;S{IG<|H<pP_6i1z!
S2&dm@jd0@}y>65tr0>#-(Qxu-F(O;%F1NtjeZ0cI9N*>@T9BRIf)lK=9E7Qv6<>X^=Q933?e-
qs<TeNHtZc{;lJAp^qF<5`=RWvJ0urVrn8iPxo_m67>^>-
8obL6W1p4>F>B}o5(OfNAww><tX8dvy!BorJIV9DaTY<2vULhk6FDKlI*se9q`q~UQWeSu00ElT7s5ir%bAY9``v<xU0{m!rRX`%
KUiX!PdouLB#8+D9SYDiM(--*LqI0))LW)9GH2GxIJ{1=uYno{u>Z3vF}A^kT>T21Wz&o*#G`d`{0K5*c_6q-
o?PosNc_uHrEvP|u<**tE092fJ_#W-XYEoai6NZ~!&lhN)GU{%Oznhs{{%qzYy<5UWF(>@c`dWFrpuI*@_ofCyFhR>yuR~CEi^U-
~-Xi7>*<kB_<?F&&bCRtYKETr`HyK-
T85#xwxOf%yjX?lpx4%aWWFQLHfI*It&YG0<^w{h)lPvcTSgcb+K;FO#pGrk=Vk6r|55Pt3""".replace("\n", "")
GLYPHS = json.loads(zlib.decompress(base64.b85decode(_GLYPH_PACK_B85)).decode("utf-8"))
if set(GLYPHS) != set(CHAR_TO_CODE):
    raise RuntimeError("embedded Cyrillic Pixel-7 raster pack does not match target set")


def cell_box(code: int, total_cells: int) -> tuple[int, int, int, int]:
    if not 0 <= code < total_cells:
        raise RuntimeError(f"glyph code 0x{code:02X} outside atlas")
    x0 = (code % COLS) * CELL_W
    y0 = (code // COLS) * CELL_H
    return x0, y0, x0 + CELL_W, y0 + CELL_H


def cell_pixels(img: Image.Image, code: int, total_cells: int) -> bytes:
    return bytes(img.crop(cell_box(code, total_cells)).getdata())


def visible_bbox(img: Image.Image, code: int, total_cells: int) -> tuple[int, int, int, int]:
    cell = img.crop(cell_box(code, total_cells))
    pts = [
        (x, y)
        for y in range(CELL_H)
        for x in range(CELL_W)
        if cell.getpixel((x, y)) != FONT_BG
    ]
    if not pts:
        raise RuntimeError(f"empty reference glyph 0x{code:02X} in {img.filename}")
    xs = [x for x, _ in pts]
    ys = [y for _, y in pts]
    return min(xs), min(ys), max(xs), max(ys)


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


def resized_binary(mask: Image.Image, w: int, h: int) -> Image.Image:
    w = max(1, w)
    h = max(1, h)
    out = mask.resize((w, h), Image.Resampling.NEAREST)
    out = out.point(lambda p: 255 if p else 0)
    if out.getbbox() is None:
        raise RuntimeError("empty Pixel-7 mask after resize")
    return out


def variant_reference(paths: list[Path]) -> dict[str, dict[str, tuple[int, int, int, int]]]:
    refs = {}
    for path in paths:
        img = Image.open(path)
        total = COLS * (img.height // CELL_H)
        refs[path.name] = {
            "upper": visible_bbox(img, 0xBB, total),
            "lower": visible_bbox(img, 0xD5, total),
        }
    return refs


def dims(box: tuple[int, int, int, int]) -> tuple[int, int]:
    return max(1, box[2] - box[0]), max(1, box[3] - box[1])


def patch_font(
    path: Path,
    refs: dict[str, dict[str, tuple[int, int, int, int]]],
) -> tuple[str, dict[int, int]]:
    img = Image.open(path)
    if img.mode != "P" or img.width != COLS * CELL_W or img.height % CELL_H:
        raise RuntimeError(f"unexpected font atlas geometry/mode: {path} {img.mode} {img.size}")
    if path.name not in FONT_FILE_TO_WIDTH_TABLE:
        raise RuntimeError(f"unmapped font variant {path.name}")

    total = COLS * (img.height // CELL_H)
    if max(TARGET_CODES) >= total:
        raise RuntimeError(f"atlas too small for bilingual target set: {path.name}")

    protected_before = {
        code: cell_pixels(img, code, total)
        for code in range(total)
        if code not in TARGET_CODES
    }

    upper_ref = refs[path.name]["upper"]
    lower_ref = refs[path.name]["lower"]
    up_w, up_h = dims(upper_ref)
    lo_w, lo_h = dims(lower_ref)

    src_A_w = int(GLYPHS["A"]["w"])
    src_A_h = int(GLYPHS["A"]["h"])
    src_a_w = int(GLYPHS["a"]["w"])
    src_a_h = int(GLYPHS["a"]["h"])

    # Pixel-7 is already designed for a tiny raster. Never enlarge it.
    sx_up = min(1.0, up_w / src_A_w)
    sy_up = min(1.0, up_h / src_A_h)
    sx_lo = min(1.0, lo_w / src_a_w)
    sy_lo = min(1.0, lo_h / src_a_h)

    baseline_up = upper_ref[3] - 1
    baseline_lo = lower_ref[3] - 1

    rendered_widths: dict[int, int] = {}
    for ch, code in CHAR_TO_CODE.items():
        src, src_baseline = source_mask(ch)
        lower = ch.islower()
        sx = sx_lo if lower else sx_up
        sy = sy_lo if lower else sy_up
        target_baseline = baseline_lo if lower else baseline_up

        if ch in DIGITS:
            sx, sy, target_baseline = sx_up, sy_up, baseline_up

        dw = max(1, int(round(src.width * sx)))
        dh = max(1, int(round(src.height * sy)))
        scaled_baseline = max(0, int(round(src_baseline * sy)))

        if dw + 1 > CELL_W or dh + 1 > CELL_H:
            fit = min((CELL_W - 1) / dw, (CELL_H - 1) / dh)
            dw = max(1, int(round(dw * fit)))
            dh = max(1, int(round(dh * fit)))
            scaled_baseline = max(0, int(round(scaled_baseline * fit)))

        mask = resized_binary(src, dw, dh)
        x0, y0, x1, y1 = cell_box(code, total)

        for yy in range(y0, y1):
            for xx in range(x0, x1):
                img.putpixel((xx, yy), FONT_BG)

        desired_top = target_baseline - scaled_baseline
        max_top = CELL_H - mask.height - 1
        if max_top < 0:
            raise RuntimeError(f"{path.name}: rendered glyph too tall {ch}/0x{code:02X}")
        top = min(max(desired_top, 0), max_top)

        for shadow_pass, color in ((True, FONT_SHADOW), (False, FONT_FG)):
            off = 1 if shadow_pass else 0
            for yy in range(mask.height):
                for xx in range(mask.width):
                    if mask.getpixel((xx, yy)):
                        px = x0 + xx + off
                        py = y0 + top + yy + off
                        if px >= x1 or py >= y1:
                            raise RuntimeError(
                                f"{path.name}: Pixel-7 overflow {ch}/0x{code:02X} at {px-x0},{py-y0}"
                            )
                        img.putpixel((px, py), color)

        cell = img.crop((x0, y0, x1, y1))
        pts = [
            (x, y)
            for y in range(CELL_H)
            for x in range(CELL_W)
            if cell.getpixel((x, y)) in (FONT_FG, FONT_SHADOW)
        ]
        if not pts:
            raise RuntimeError(f"empty rendered Pixel-7 glyph {ch}/0x{code:02X}")
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
        f"[pixel7-v37] {path.name}: {len(TARGET_CODES)} targets; "
        f"scaleU={sx_up:.2f}/{sy_up:.2f} scaleL={sx_lo:.2f}/{sy_lo:.2f} "
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
            raise RuntimeError(f"{m.group('name')}: incomplete Pixel-7 widths")
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
        f"[pixel7-v37] 9 width tables patched at {len(TARGET_CODES)} English/Russian/digit codes"
    )


def verify_charmap(root: Path) -> None:
    text = (root / "charmap.txt").read_text(encoding="utf-8")
    if "'Щ' = 2F" not in text:
        raise RuntimeError("required Щ=0x2F charmap entry missing")
    if 0x1B in TARGET_CODES:
        raise RuntimeError("Pixel-7 target set unexpectedly includes legacy é slot")


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

    refs = variant_reference(paths)
    widths_by_table = {}
    for path in paths:
        table, widths = patch_font(path, refs)
        widths_by_table[table] = widths

    patch_width_tables(root / "src/fonts.c", widths_by_table)

    audit = {
        "marker": MARKER,
        "font": "Cyrillic Pixel-7 raster",
        "english": True,
        "russian": True,
        "digits": True,
        "specialAccentedE": False,
        "accentedENormalization": "deferred until after localization",
        "legacyAccentedESlotTouched": False,
        "shchaCode": "0x2F",
        "targetGlyphCells": len(TARGET_CODES),
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_font_pixel7_v3_7_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: Cyrillic Pixel-7 installed for English + Russian + digits; "
        "special é glyph excluded; post-localization normalization pending; legacy 0x1B and Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
