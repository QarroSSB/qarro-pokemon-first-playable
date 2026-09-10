#!/usr/bin/env python3
"""TEST ONLY: unified Moniqa-derived Latin + Cyrillic FireRed raster font.

Runs after ci/install_cyrillic_v3_3.py. The user-supplied font binary is not
stored in the repository; only derived monochrome raster masks are stored in
ci/moniqa_raster_v3_6.part*. English letters, Russian letters, digits and é
are redrawn in one style. All other atlas cells and width entries are verified
byte-identical. No Ash Bond / Ash Cap code is touched.
"""
from __future__ import annotations
import base64, json, re, sys, zlib
from pathlib import Path
try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required") from exc

CELL_W = CELL_H = COLS = 16
FONT_BG, FONT_FG, FONT_SHADOW = 0, 1, 2
LATIN_UPPER_A, LATIN_LOWER_A = 0xBB, 0xD5
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
EXPECTED_TABLES = set(FONT_FILE_TO_WIDTH_TABLE.values())
CYRILLIC = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
UPPER = set("ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789")
LOWER = set("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюяé")
FONT_SHA = "b00f55647a9305597bcc8c77ac93cda9cd45b25f87069a477a42df9f68ff116f"


def load_payload() -> dict:
    here = Path(__file__).resolve().parent
    parts = sorted(here.glob("moniqa_raster_v3_6.part*"))
    if [p.name for p in parts] != [f"moniqa_raster_v3_6.part{i:02d}" for i in range(5)]:
        raise RuntimeError("Moniqa raster payload parts missing or unexpected")
    enc = "".join(p.read_text(encoding="ascii").strip() for p in parts)
    data = json.loads(zlib.decompress(base64.b85decode(enc)).decode("utf-8"))
    if data.get("font_sha256") != FONT_SHA:
        raise RuntimeError("Moniqa raster source fingerprint mismatch")
    return data["glyphs"]

GLYPHS = load_payload()
TARGETS = {ch: int(meta["c"]) for ch, meta in GLYPHS.items()}
if len(TARGETS) != 129 or len(set(TARGETS.values())) != len(TARGETS):
    raise RuntimeError("unexpected Moniqa target mapping")
if not set(CYRILLIC).issubset(TARGETS):
    raise RuntimeError("incomplete Cyrillic Moniqa payload")


def cell_box(code: int, total: int):
    if not 0 <= code < total:
        raise RuntimeError(f"glyph 0x{code:02X} outside atlas")
    x, y = (code % COLS) * CELL_W, (code // COLS) * CELL_H
    return x, y, x + CELL_W, y + CELL_H


def cell_pixels(img, code: int, total: int) -> bytes:
    return bytes(img.crop(cell_box(code, total)).getdata())


def visible_bbox(img, code: int, total: int):
    cell = img.crop(cell_box(code, total))
    pts = [(x, y) for y in range(CELL_H) for x in range(CELL_W)
           if cell.getpixel((x, y)) != FONT_BG]
    if not pts:
        raise RuntimeError(f"empty reference 0x{code:02X} in {img.filename}")
    xs, ys = zip(*pts)
    return min(xs), min(ys), max(xs), max(ys)


def src_bbox(ch: str):
    return tuple(GLYPHS[ch]["b"])


def source_image(ch: str):
    meta = GLYPHS[ch]
    w, h = map(int, meta["s"])
    packed = base64.b85decode(meta["m"])
    raw = bytearray(w * h)
    for i in range(w * h):
        if packed[i >> 3] & (1 << (7 - (i & 7))):
            raw[i] = 255
    return Image.frombytes("L", (w, h), bytes(raw))


def base_scale(ch: str, target_h: int) -> float:
    _, top, _, bottom = src_bbox(ch)
    h = bottom - top
    if h <= 0:
        raise RuntimeError(f"bad source height for {ch}")
    return target_h / h


def fit_scale(chars: set[str], scale: float, baseline: int) -> float:
    out, max_fg = scale, CELL_H - 2
    for ch in chars:
        if ch not in TARGETS:
            continue
        left, top, right, bottom = src_bbox(ch)
        if top < 0:
            out = min(out, baseline / (-top))
        if bottom > 0:
            out = min(out, (max_fg - baseline) / bottom)
        if right > left:
            out = min(out, (CELL_W - 1) / (right - left))
    if out <= 0:
        raise RuntimeError("Moniqa scale collapsed")
    return out


def check_charmap(root: Path) -> None:
    text = (root / "charmap.txt").read_text(encoding="utf-8")
    checks = {"'A'":"BB", "'Z'":"D4", "'a'":"D5", "'z'":"EE",
              "'0'":"A1", "'9'":"AA", "'é'":"1B", "'Щ'":"2F"}
    for token, code in checks.items():
        if not re.search(rf"(?m)^{re.escape(token)}\s*=\s*{code}\s*$", text):
            raise RuntimeError(f"charmap drift: expected {token} = {code}")


def patch_font(path: Path):
    img = Image.open(path)
    if img.mode != "P" or img.width != COLS * CELL_W or img.height % CELL_H:
        raise RuntimeError(f"unexpected Latin atlas geometry/mode: {path}")
    if path.name not in FONT_FILE_TO_WIDTH_TABLE:
        raise RuntimeError(f"unmapped Latin atlas: {path.name}")
    total = COLS * (img.height // CELL_H)
    target_codes = set(TARGETS.values())
    protected = {code: cell_pixels(img, code, total) for code in range(total)
                 if code not in target_codes}

    upper_ref = visible_bbox(img, LATIN_UPPER_A, total)
    lower_ref = visible_bbox(img, LATIN_LOWER_A, total)
    upper_h = max(1, upper_ref[3] - upper_ref[1])
    lower_h = max(1, lower_ref[3] - lower_ref[1])
    baseline = max(upper_ref[3], lower_ref[3]) - 1
    upper_scale = fit_scale(UPPER, base_scale("A", upper_h), baseline)
    lower_scale = fit_scale(LOWER, base_scale("a", lower_h), baseline)
    resampling = getattr(Image, "Resampling", Image).LANCZOS
    widths = {}

    for ch, code in TARGETS.items():
        x0, y0, x1, y1 = cell_box(code, total)
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                img.putpixel((xx, yy), FONT_BG)
        left, top, right, bottom = src_bbox(ch)
        scale = lower_scale if ch in LOWER else upper_scale
        src = source_image(ch)
        dw, dh = max(1, round(src.width * scale)), max(1, round(src.height * scale))
        mask_l = src.resize((dw, dh), resampling)
        mask = mask_l.point(lambda p: 255 if p >= 32 else 0)
        if mask.getbbox() is None:
            mask = mask_l.point(lambda p: 255 if p >= 8 else 0)
        if mask.getbbox() is None:
            raise RuntimeError(f"empty scaled Moniqa glyph {ch} in {path.name}")
        dst_top = baseline + round(top * scale)
        if dst_top < 0 or dst_top + dh + 1 > CELL_H:
            raise RuntimeError(f"{path.name}: vertical overflow {ch}/0x{code:02X} top={dst_top} h={dh}")
        if dw + 1 > CELL_W:
            raise RuntimeError(f"{path.name}: horizontal overflow {ch}/0x{code:02X} w={dw+1}")
        for shadow, color in ((True, FONT_SHADOW), (False, FONT_FG)):
            off = 1 if shadow else 0
            for yy in range(dh):
                for xx in range(dw):
                    if mask.getpixel((xx, yy)):
                        img.putpixel((x0 + xx + off, y0 + dst_top + yy + off), color)
        cell = img.crop((x0, y0, x1, y1))
        pts = [(x,y) for y in range(CELL_H) for x in range(CELL_W)
               if cell.getpixel((x,y)) in (FONT_FG, FONT_SHADOW)]
        if not pts:
            raise RuntimeError(f"empty final Moniqa glyph {ch}")
        xs = [x for x,_ in pts]
        if min(xs) != 0:
            raise RuntimeError(f"{path.name}: origin drift {ch}/0x{code:02X} min_x={min(xs)}")
        widths[code] = max(xs) + 1

    for code, before in protected.items():
        if cell_pixels(img, code, total) != before:
            raise RuntimeError(f"SAFETY FAIL: non-target glyph 0x{code:02X} changed in {path.name}")
    img.save(path, optimize=False)
    print(f"[moniqa] {path.name}: refs={upper_ref}/{lower_ref} baseline={baseline} "
          f"scales={upper_scale:.3f}/{lower_scale:.3f} targets={len(widths)}")
    return FONT_FILE_TO_WIDTH_TABLE[path.name], widths


def patch_widths(path: Path, profiles: dict) -> None:
    text = path.read_text(encoding="utf-8")
    rx = re.compile(r"(?ms)^(?P<head>(?:ALIGNED\(4\)\s+)?const u8 "
                    r"(?P<name>gFont[A-Za-z0-9_]*LatinGlyphWidths)\[\]\s*=\s*\{)"
                    r"(?P<body>.*?)(?P<tail>^\};)")
    matches = list(rx.finditer(text))
    names = {m.group("name") for m in matches}
    if names != EXPECTED_TABLES or set(profiles) != EXPECTED_TABLES:
        raise RuntimeError("width-table/profile mismatch")
    target_codes = set(TARGETS.values())
    replacements = []
    for m in matches:
        tokens = list(re.finditer(r"\b\d+\b", m.group("body")))
        if len(tokens) != 512:
            raise RuntimeError(f"{m.group('name')}: expected 512 widths")
        before = [int(t.group()) for t in tokens]
        after = list(before)
        profile = profiles[m.group("name")]
        if set(profile) != target_codes:
            raise RuntimeError(f"{m.group('name')}: incomplete Moniqa widths")
        for code, width in profile.items(): after[code] = width
        for code in range(512):
            if code not in target_codes and after[code] != before[code]:
                raise RuntimeError(f"SAFETY FAIL: non-target width 0x{code:02X} changed")
        base = m.start("body")
        for code in target_codes:
            tok = tokens[code]
            replacements.append((base + tok.start(), base + tok.end(), str(after[code])))
    for start, end, value in sorted(replacements, reverse=True):
        text = text[:start] + value + text[end:]
    path.write_text(text, encoding="utf-8")
    print(f"[moniqa] 9 width tables patched at {len(target_codes)} text cells")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr); return 2
    root = Path(sys.argv[1]).resolve()
    check_charmap(root)
    paths = sorted((root / "graphics/fonts").glob("latin_*.png"))
    if len(paths) != 9: raise RuntimeError(f"expected 9 Latin atlases, got {len(paths)}")
    profiles = dict(patch_font(path) for path in paths)
    patch_widths(root / "src/fonts.c", profiles)
    print("[QARRO_MONIQA_UNIFIED_FONT_TEST] PASS: English + Russian letters, digits and é "
          "share one Moniqa-derived raster style; non-target symbols/Ash untouched")
    return 0

if __name__ == "__main__": raise SystemExit(main())
