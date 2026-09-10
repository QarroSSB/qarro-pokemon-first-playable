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

# Horizontal scale, vertical scale, target baseline. Normal dialogue uses the
# full readability-oriented Pixellari raster; constrained UI variants are
# reduced only as much as their role requires.
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

_GLYPH_PACK_B85 = """c-rmSNLh@h4D1>=E{@HaqSPIN+r4+o46N@6v?O2F5<n_tl!ps%^_?9MI95*rqo$j03Jbh<F}
3{@)xKFFG6ePCy0NTv%+-Ms*DKV~C1xX4*1teA4~kK2h!~?qJlG72=mOB3Lo)N<ByB$wvz63d&lDUG5OXA!0#n#u<7tuWmr|3
k!y^Jv7J0MI}c6RDNE;ChFZ=$P?G`n*%+BL;0Agu$?<_qXJkJ9I(6#S<5JIWSEPfV_t_e1N=k(r8i-f1PyfPB1<PY7lO`w2
zG6^sqQ-{2v*%_ea>1We4{N-7nC_(d3HHdo!yWmJQ!WFf^l7s}7Sb;C3jA6$X`Q4qR~Dj2^wZ+;`qW&^nDx&qQ0!;+Pa6lX
5Y{u=WJ^^mE5eL-W}5v4;qKI$=TDxHft+6rX1B?{v#r?USg~a7C1$1Oe`ql6dco;W0KiE2Q}H5-s$4^Q)z0<$M#4A8YGH3$p
<wZtb#VpV3aT&JkD+s6=xSr_zjNVb(v5NTnAC!2FPv5&^t;fVg}GT8vI-!X+S94#c1ax`Q2rjK;AW;x<^4oQE<Q_B%=4HJhG
C=qN2+>3Q+1_9AvpFA-ffuCM<1Fr1@x&e79>Kk1CO^X)6e*qW}NX4Pskkg=PdbX%NFGo;C|reIv9hOr&c13wa85_XmJKfP)gL
bH!QxdwHp$g>qdsR0N6tLWdTyTR9UymAoD7jW!70Bs5z4|Ef{#1tr@2<!OBX&_Avpa+a<1>1^*G1r#xqheSE1q}nL84_JtmZ
@;)@K0x_WzIhd7=NN#wv*tB@|3lB~{?HkCNn@<l1T7*z+wXAzIs*8IK)*<N-PtOQ_n8wj$yqq+usYS1*;CoOnAR~DT#MSy&
p@aT4L=bK<f8s<d{@rbWIw8Z$eIE9TY1v%V_+~R1xbNO@PP;0n>xNWuK{x@+knsXIlXEG=P!?V^TAbN0?OluCl4A@+5kL{ahR
lj~x&dCAQBJgaYXf&2Gd=JbSb#F&@&;AJa1H7C97xW*?ILJ_B#gK`Y;+?2n_9@Jguc(;%76<<ej%+5XH;f$4v#1g>9k#9nMGV
J4LJ4P8n91DW=eO9f{T%t~%^ozzc}+j4GvQD7+#1R9BxR5`v39c~|SpORt%~X5!sp+WX7u`lH4$T|vQwF!6!1v(*{M3S^b>f
3wRNR+d{5Oai8^ITN<WBp=$jc8S{`6!U{dmQHD%h-%i{XjTnR-|BOo@43+YcfGYz6Kza+Q!(^x!4lP1BKa~m4A~k>v})>}d
wMlDs5wJu$$j8W1H2Y@FP2i0om?|`%p6a_5It6pgT8rgISeO?7)M;=`-u@4HoCnsnIE&j3UUG-}B1un`KlCr5$?R8`K8bmj8V
%a0%=>1q<`BrZ6o{{NJFXw5k2pWcfwW9~tA&`~?1?gdM#0pZ;k6i@e@UJs<KCRvy|^08~Z3l&Uz=`zT=BITo!B@f1Dq%)Tc<
#{Pu6+Se#s%6D3R+9O6!mJH_<vkmJ!8P=X1eIdJ`@N7iaLpMyHUevZDP$hhkK+gH>3c|kI0?Acm1sAXO1}Mg3!i9anxpEBZs
qV)%P_~6jgR$<2+XV06LIzyAp#^wsWN<R*1Y`)fkIU27nPiYRBdu>Oq+q8C^Jh<&bn8BOb4+`gsvC}M;B7>2#Skq)&7!s}#O
uB5Q!?!^^jmGVCR45a!uRO2{E@^ezkFWt8sZ&?X8XkwY4=ft6nYfoP2<Wl>^i?JzT;aRxrQ)w=^6X*oJ#Q#65j1lT1nxx<gb
xW8GC`NuS6VI?v6H%R58Q34aV&-RUfo>wp^>nDt+O5Dss-f)`@cy(=P9@Yb}<0Y=9)wI5t!G=P)T<JFP-Di`4z`E@bDuLL
F%3QF%_B0-}EHC#VQf-;*JM4Y(9xQ#p#b@2o@e#mv}4O&j!t6nV#fOP|Pr|F8wP%w4`9h=aKcAKw?%+^ft1)N6{+^a^{1A
w?Fw""".replace("\n", "")
GLYPHS = json.loads(zlib.decompress(base64.b85decode(_GLYPH_PACK_B85)).decode("utf-8"))
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
