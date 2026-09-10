#!/usr/bin/env python3
"""TEST ONLY: readable Moniqa-derived unified Latin+Cyrillic FireRed font.

Second-pass rasterizer after the first Moniqa test proved too condensed on real
GBA output. Reuses the derived Moniqa masks from v3_6, but applies controlled
horizontal expansion and one-pixel horizontal stem reinforcement. Vertical
metrics, charmap, non-target glyphs and all non-font gameplay code remain
untouched. No Ash Bond / Ash Cap code is touched.
"""
from __future__ import annotations
import statistics
import sys
from pathlib import Path
from PIL import Image

import install_moniqa_unified_font_v3_6 as base

# Moniqa is naturally very condensed. At FireRed's 16x16 cell size its
# horizontal features collapsed in actual gameplay. Stretch only X; keep Y
# metrics from the already-green v3_6 implementation.
X_STRETCH = {
    "latin_normal.png": 1.70,
    "latin_short.png": 1.65,
    "latin_small.png": 1.65,
    "latin_narrow.png": 1.55,
    "latin_small_narrow.png": 1.55,
    "latin_short_narrow.png": 1.55,
    "latin_narrower.png": 1.48,
    "latin_small_narrower.png": 1.48,
    "latin_short_narrower.png": 1.48,
}
# Only intrinsically broad glyphs belong in the per-glyph wide guard.  A is a
# normal-width Latin capital in FireRed and is covered by the median guard.
READABILITY_WIDE = "MWЖШЩЫЮ"
NATURALLY_NARROW = set("Iil1")


def reinforce_horizontal(mask: Image.Image) -> Image.Image:
    """Add one pixel of horizontal ink without increasing glyph height."""
    out = Image.new("L", (mask.width + 1, mask.height), 0)
    out.paste(mask, (0, 0))
    for y in range(mask.height):
        for x in range(mask.width):
            if mask.getpixel((x, y)):
                out.putpixel((x + 1, y), 255)
    return out


def readability_floors(path_name: str) -> tuple[int, int]:
    """Return (broad-glyph floor, median floor) for each native FireRed profile.

    The narrow/narrower atlases are intentionally compressed by the engine, so
    forcing the normal-font floor on them is a false failure.  Keep the strong
    guard on normal/short/small while requiring each compact profile to retain
    a footprint appropriate to its stock class.
    """
    if "narrower" in path_name:
        return 3, 3
    if "narrow" in path_name:
        return 4, 4
    return 6, 5


def patch_font(path: Path):
    img = Image.open(path)
    if img.mode != "P" or img.width != base.COLS * base.CELL_W or img.height % base.CELL_H:
        raise RuntimeError(f"unexpected Latin atlas geometry/mode: {path}")
    if path.name not in base.FONT_FILE_TO_WIDTH_TABLE or path.name not in X_STRETCH:
        raise RuntimeError(f"unmapped Latin atlas: {path.name}")

    total = base.COLS * (img.height // base.CELL_H)
    target_codes = set(base.TARGETS.values())
    protected = {code: base.cell_pixels(img, code, total) for code in range(total)
                 if code not in target_codes}

    upper_ref = base.visible_bbox(img, base.LATIN_UPPER_A, total)
    lower_ref = base.visible_bbox(img, base.LATIN_LOWER_A, total)
    upper_h = max(1, upper_ref[3] - upper_ref[1])
    lower_h = max(1, lower_ref[3] - lower_ref[1])
    baseline = max(upper_ref[3], lower_ref[3]) - 1
    upper_scale = base.fit_scale(base.UPPER, base.base_scale("A", upper_h), baseline)
    lower_scale = base.fit_scale(base.LOWER, base.base_scale("a", lower_h), baseline)
    resampling = getattr(Image, "Resampling", Image).LANCZOS
    widths = {}
    stretch = X_STRETCH[path.name]

    for ch, code in base.TARGETS.items():
        x0, y0, x1, y1 = base.cell_box(code, total)
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                img.putpixel((xx, yy), base.FONT_BG)

        left, top, right, bottom = base.src_bbox(ch)
        scale = lower_scale if ch in base.LOWER else upper_scale
        src = base.source_image(ch)
        dh = max(1, round(src.height * scale))
        # Leave one pixel for reinforcement and one for FireRed shadow.
        core_w = max(1, round(src.width * scale * stretch))
        core_w = min(base.CELL_W - 2, core_w)
        mask_l = src.resize((core_w, dh), resampling)
        mask = mask_l.point(lambda p: 255 if p >= 28 else 0)
        if mask.getbbox() is None:
            mask = mask_l.point(lambda p: 255 if p >= 8 else 0)
        if mask.getbbox() is None:
            raise RuntimeError(f"empty scaled Moniqa glyph {ch} in {path.name}")

        # Real-device readability pass: keep the Moniqa silhouette but ensure
        # 1px-thin stems do not disappear at GBA scale.
        mask = reinforce_horizontal(mask)
        glyph_w = mask.width
        dst_top = baseline + round(top * scale)
        if dst_top < 0 or dst_top + dh + 1 > base.CELL_H:
            raise RuntimeError(f"{path.name}: vertical overflow {ch}/0x{code:02X} top={dst_top} h={dh}")
        if glyph_w + 1 > base.CELL_W:
            raise RuntimeError(f"{path.name}: horizontal overflow {ch}/0x{code:02X} w={glyph_w+1}")

        for shadow, color in ((True, base.FONT_SHADOW), (False, base.FONT_FG)):
            off = 1 if shadow else 0
            for yy in range(dh):
                for xx in range(glyph_w):
                    if mask.getpixel((xx, yy)):
                        img.putpixel((x0 + xx + off, y0 + dst_top + yy + off), color)

        cell = img.crop((x0, y0, x1, y1))
        pts = [(x, y) for y in range(base.CELL_H) for x in range(base.CELL_W)
               if cell.getpixel((x, y)) in (base.FONT_FG, base.FONT_SHADOW)]
        if not pts:
            raise RuntimeError(f"empty final Moniqa glyph {ch}")
        xs = [x for x, _ in pts]
        if min(xs) != 0:
            raise RuntimeError(f"{path.name}: origin drift {ch}/0x{code:02X} min_x={min(xs)}")
        widths[code] = max(xs) + 1

    for code, before in protected.items():
        if base.cell_pixels(img, code, total) != before:
            raise RuntimeError(f"SAFETY FAIL: non-target glyph 0x{code:02X} changed in {path.name}")

    # Fail closed on the exact failure mode seen on-device, while respecting
    # FireRed's deliberately compact narrow/narrower atlas classes.
    wide_floor, median_floor = readability_floors(path.name)
    for ch in READABILITY_WIDE:
        w = widths[base.TARGETS[ch]]
        if w < wide_floor:
            raise RuntimeError(f"{path.name}: readability collapse {ch} width={w} < {wide_floor}")
    ordinary = [w for ch, code in base.TARGETS.items() if ch not in NATURALLY_NARROW for w in [widths[code]]]
    median_w = statistics.median(ordinary)
    if median_w < median_floor:
        raise RuntimeError(f"{path.name}: readability median width collapsed to {median_w} < {median_floor}")

    img.save(path, optimize=False)
    print(f"[moniqa-r2] {path.name}: stretch={stretch:.2f} median={median_w:.1f} "
          f"floors={wide_floor}/{median_floor} refs={upper_ref}/{lower_ref} "
          f"baseline={baseline} targets={len(widths)}")
    return base.FONT_FILE_TO_WIDTH_TABLE[path.name], widths


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    base.check_charmap(root)
    paths = sorted((root / "graphics/fonts").glob("latin_*.png"))
    if len(paths) != 9:
        raise RuntimeError(f"expected 9 Latin atlases, got {len(paths)}")
    profiles = dict(patch_font(path) for path in paths)
    base.patch_widths(root / "src/fonts.c", profiles)
    print("[QARRO_MONIQA_READABLE_R2] PASS: unified English + Russian Moniqa style "
          "with GBA-scale horizontal hinting; protected symbols/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
