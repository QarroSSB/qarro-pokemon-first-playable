#!/usr/bin/env python3
"""Qarro v3.6 bilingual Moniqa bitmap font pass.

Replaces both English and Russian alphabet glyphs in all nine FireRed Latin
font atlases with bitmap glyphs rasterized from the user-supplied
"Moniqa XLt Nr It Paragraph" typeface. The original TTF/OTF files are NOT
committed, redistributed, or modified; only rasterized glyph masks are embedded
below. Digits and FireRed's accented `é` are included so English names and
`POKéMON` use the same face as Russian dialogue.

This pass runs after the proven Cyrillic/charmap installer. It keeps the v3.6
Щ remap at 0x2F, preserves `é` at 0x1B, leaves every non-target glyph cell
byte-identical, and patches per-atlas width tables for exactly the replaced
English/Russian/digit cells.

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

MARKER = "QARRO_BILINGUAL_MONIQA_V3_6"
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
            **{ch: 0xA1 + i for i, ch in enumerate(DIGITS)},
            "é": 0x1B}
CYR_CODES_LIST = list(range(0x01, 0x2A)) + list(range(0x3B, 0x51)) + [0x5A, 0x68, 0x6F]
CYR_CODES_LIST[RU.index("Щ")] = 0x2F
RU_CODES = dict(zip(RU, CYR_CODES_LIST))
CHAR_TO_CODE = {**EN_CODES, **RU_CODES}
TARGET_CODES = set(CHAR_TO_CODE.values())
if len(TARGET_CODES) != len(CHAR_TO_CODE):
    raise RuntimeError("bilingual target code collision")
if CHAR_TO_CODE["é"] != 0x1B or CHAR_TO_CODE["Щ"] != 0x2F:
    raise RuntimeError("expected é/Щ runtime mapping changed")

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

_GLYPH_PACK_B85 = """c-pO5*OJ{t5dD|?JP#8T_l=x$hT_471sjYFUci9MRhXQ?<eZbqIfn;+VD2B$VKkb#yVADgTbf$OIqKY}TSphCEjErWjx06`wb-
}VFh(u*?%CQru>asD|LO3dBU_7&8yeLpW5a>pYGn%i*{b%&V`_1FKq<#jEL?B8qgAEg-&%SMqMRW_X_O6*Qzkq$0-QNRj3%f-
522hTGYJ@=6QhcPI0QI*20*6=8RDGDhA?H+fe_A}WeKNykC0!_3ovdRriyadT#@sIVic;0PZ1t6<pq=U&}7O=mEj>BE}X9eiEvT4
U+>~g4dK|}DGNN6QMRRH=xD^cSgcNeG$>+Rax5ZUB11A&=3raqp?;}Qo&=$y%uk(sSq@@{qcszy?ju%Jh;zA6rDj!{It|$?gvr<W
x=0?f$(1rOAXmC;ec({QTs15AY@WbZ%hbUC&#~_4iB7pD+^=@gqK2y>LJd|CKJ*~WwL+K*&7ebbNScIZr(7p@t>(^vPiEEYWs+1{
0YU{o8igLhk^p}}%IwK(+N20gT9so%fNU!{DE7+S5y}Ta#7Y_<ZW6vdDWQDvW_hZE%?g!j5Z}I;y}eB_+6YmQ*;)#M{{6RzGpbTH
x-BUXw~hd;8a}aF*|&jxQ_OEO9P}YV><<u@A#?_z69~OiBfBjZzzy8SnA1r?iN-
*T+b6{kicu@4l4LxPtFW6DwkdH(*2#t<5Z+uvDTENv-~pows4XA}g~CC32BnU~tB0m0Uku$lN8-Q9$dFbm3={BNr~O?MqA-zwJ&6
E^g&I@|Eu}YaWejBCB2qvXI}%0x-MPfWAxr#k8*#ZuB=1Vfk+1HR-0W_I#)J2cWHox=UO{w*xl!M6@cMn3qX({YmoaRn;4Qp-
|A?`+3vKdl`GDxnoZa2SJw*$fy;du{CF5a6#!>U45*&{At*kjhb8uj|CNzpBaF<ROCu}rU#a`2Jt7qO$suVI&Scvo>hBNpJ!jxhb
7JDv>L6Jf6Ux|5Xgs_;q>=yt=kXkH9$2fXENUmuzd$a>N>|kbyAyQyUnwr=;LbPLw*sS?%C&z3Ra?O7y<-
<Nw0V;$!7w|8vWnbV=OmwdeR!JDLe{n5K2mjLKX?>-
w`j_(w(G4Kf*wrCEG$tW1W;i9ycVYM@pBoy5{40~~({~+q)bSi47s{oDNvjc<R|8DDi;-
I_3g9BZYhVPf@BkMF1zYA5l#>26VWDbNRv;|#+E8&=u-B(di<ZV<G_|ALGX1>h-
^hWA45&!ywJl<XjRC$nac2?cojP4w__t(R2e37SRXiM3;eZ=BKHpyB2E)Izp3RbfcUI#xP2M>Dd-
I0vzW=f`@2_JK;y;+Yx3l@E=RZ8v<%9o7SkCkgqqYuue4J;g8*DhBNeQWH@n8`#tGfj1q5hNgY!UpYV>M0UY|Pe@35NenCKMz>7J
w}j$grv;n9l=Dvx~i<y*D--
tcO?<X}qEds~`gAPv&55E*Nzfw*42fh^j&;F$qFNO_F6_$|^_=;Z)%PI#W~>7bH_jT*h*MekBXgN~Oz`Jn6p{)7`X-*q--xP2?M~
Uct&pLNry$mZxGomZS6ASu0uBB_bP~kiMHeEBo(dT#;CEXI_eGQ)jH`he?yZ;T?4+#E-
IpH{EpcTYnnyN1M(LJ(o)9RAn*p9LL$u(v8;+G<SJIHhLF43GTp?f0683AbX7=o@A+(av?3)7Qc!-V7s9w;raeI;pE?RpA-
x)n&|THGSw-9hA{q+t{w{7aXBVGboEck4goEeoRCaxx4$H_eEbH%hbf$4hV!>nc+S4M-
<$Y<<|ppI)2=3K!R3SNS&%J{&)rZjACe|~^5K>)J}eTw7q|Pumkij;N5%+zK9Ul*z>jKeAGL65#v`;xPh|<Ud`z^3>Vt>fSa&PN<
>SKG>%UIKt51lQZ&YDQmr*sxc6>7Ls(KOv_gKPtN}>Zhutp_f4lJLRs1Wuf;4_wiUCAmuBZ)(1-QBoF&0_hisA$-
@stN^{#ePmCHceK6Fp%WfbouSiPiVF}q;19Nf9!u3AEF8""".replace("\n", "")
GLYPHS = json.loads(zlib.decompress(base64.b85decode(_GLYPH_PACK_B85)).decode("utf-8"))
if set(GLYPHS) != set(CHAR_TO_CODE):
    raise RuntimeError("embedded Moniqa raster pack does not match bilingual target set")


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
    pts = [(x, y) for y in range(CELL_H) for x in range(CELL_W) if cell.getpixel((x, y)) != FONT_BG]
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
    shrinking = w < mask.width or h < mask.height
    resample = Image.Resampling.BOX if shrinking else Image.Resampling.NEAREST
    out = mask.resize((w, h), resample)
    # Preserve this extra-light face when shrinking to tiny GBA variants.
    threshold = 24 if shrinking else 64
    out = out.point(lambda p: 255 if p >= threshold else 0)
    if out.getbbox() is None:
        # Deterministic fallback: nearest keeps at least one source stroke.
        out = mask.resize((w, h), Image.Resampling.NEAREST).point(lambda p: 255 if p else 0)
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


def patch_font(path: Path, refs: dict[str, dict[str, tuple[int, int, int, int]]]) -> tuple[str, dict[int, int]]:
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
    normal_upper = refs["latin_normal.png"]["upper"]
    normal_lower = refs["latin_normal.png"]["lower"]

    def fg_dims(box):
        # Reference includes native one-pixel down/right shadow.
        return max(1, box[2] - box[0]), max(1, box[3] - box[1])

    up_w, up_h = fg_dims(upper_ref)
    lo_w, lo_h = fg_dims(lower_ref)
    nup_w, nup_h = fg_dims(normal_upper)
    nlo_w, nlo_h = fg_dims(normal_lower)
    up_aspect_factor = (up_w / up_h) / (nup_w / nup_h)
    lo_aspect_factor = (lo_w / lo_h) / (nlo_w / nlo_h)

    src_A = GLYPHS["A"]
    sy_up = up_h / int(src_A["h"])
    # Preserve Moniqa's real x-height instead of stretching lowercase to the
    # stock FireRed `a` cell height. This keeps English/Russian lowercase
    # visibly smaller than capitals and avoids oversized descenders.
    sy_lo = sy_up
    sx_up = sy_up * up_aspect_factor
    sx_lo = sy_lo * lo_aspect_factor
    baseline_up = upper_ref[3] - 1
    baseline_lo = lower_ref[3] - 1

    rendered_widths: dict[int, int] = {}
    for ch, code in CHAR_TO_CODE.items():
        src, src_baseline = source_mask(ch)
        lower = ch.islower()
        sx = sx_lo if lower else sx_up
        sy = sy_lo if lower else sy_up
        target_baseline = baseline_lo if lower else baseline_up

        # Digits and é use uppercase body scale; Russian/English lowercase use lowercase.
        if ch in DIGITS or ch == "é":
            sx, sy, target_baseline = sx_up, sy_up, baseline_up

        dw = max(1, int(round(src.width * sx)))
        dh = max(1, int(round(src.height * sy)))
        scaled_baseline = int(round(src_baseline * sy))

        # Reserve one pixel for the FireRed shadow. If an accent or descender
        # is taller than the 15-pixel drawable body, shrink proportionally.
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
        # Clamp only the vertical origin; this preserves shape while allowing
        # tall Cyrillic forms such as ф/Щ and accented Ё/й to fit cleanly.
        top = min(max(desired_top, 0), max_top)
        for shadow_pass, color in ((True, FONT_SHADOW), (False, FONT_FG)):
            off = 1 if shadow_pass else 0
            for yy in range(mask.height):
                for xx in range(mask.width):
                    if mask.getpixel((xx, yy)):
                        img.putpixel((x0 + xx + off, y0 + top + yy + off), color)

        cell = img.crop((x0, y0, x1, y1))
        pts = [(x, y) for y in range(CELL_H) for x in range(CELL_W) if cell.getpixel((x, y)) in (FONT_FG, FONT_SHADOW)]
        if not pts:
            raise RuntimeError(f"empty rendered bilingual glyph {ch}/0x{code:02X}")
        min_x = min(x for x, _ in pts)
        max_x = max(x for x, _ in pts)
        if min_x != 0:
            raise RuntimeError(f"{path.name}: left origin drift {ch}/0x{code:02X} min_x={min_x}")
        rendered_widths[code] = min(CELL_W, max_x + 2)

    for code, before in protected_before.items():
        if cell_pixels(img, code, total) != before:
            raise RuntimeError(f"SAFETY FAIL: non-target glyph 0x{code:02X} changed in {path.name}")

    img.save(path, optimize=False)
    print(
        f"[moniqa-v36] {path.name}: {len(TARGET_CODES)} bilingual targets; "
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
        raise RuntimeError(f"width-table mismatch tables={sorted(names)} profiles={sorted(widths_by_table)}")

    repl = []
    for m in matches:
        tokens = list(re.finditer(r"\b\d+\b", m.group("body")))
        if len(tokens) != 512:
            raise RuntimeError(f"{m.group('name')}: expected 512 widths, got {len(tokens)}")
        before = [int(t.group()) for t in tokens]
        after = list(before)
        widths = widths_by_table[m.group("name")]
        if set(widths) != TARGET_CODES:
            raise RuntimeError(f"{m.group('name')}: incomplete bilingual widths")
        for code, width in widths.items():
            after[code] = width
        for code in range(512):
            if code not in TARGET_CODES and after[code] != before[code]:
                raise RuntimeError(f"SAFETY FAIL: non-target width 0x{code:02X} changed")
        base = m.start("body")
        for code in TARGET_CODES:
            tok = tokens[code]
            repl.append((base + tok.start(), base + tok.end(), str(after[code])))

    for start, end, value in sorted(repl, reverse=True):
        text = text[:start] + value + text[end:]
    path.write_text(text, encoding="utf-8")
    print(f"[moniqa-v36] 9 width tables patched at {len(TARGET_CODES)} bilingual target codes")


def verify_charmap(root: Path) -> None:
    text = (root / "charmap.txt").read_text(encoding="utf-8")
    required = ["'é'         = 1B", "'Щ' = 2F"]
    for needle in required:
        if needle not in text:
            raise RuntimeError(f"required bilingual charmap entry missing: {needle!r}")


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
    print(
        f"[{MARKER}] PASS: Moniqa raster face installed for English + Russian + digits; "
        "é/Щ split preserved; non-target glyphs and Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
