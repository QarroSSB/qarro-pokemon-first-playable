#!/usr/bin/env python3
"""Targeted narrow-font fixes for the v3.3.3 per-font Cyrillic scaler.

Reuses the exact per-font scaler from commit 6593ba7. Only while rendering
latin_narrow.png, uppercase Cyrillic Д and Ё use compact source masks. Their
full source forms remain unchanged in all other eight font atlases.

CI history:
- run #50: full Д overflowed latin_narrow to y=18;
- run #51: first compact Д still reached y=16 including shadow;
- run #52: narrow Д passed and the next real failure was Ё at y=-4..14.

The narrow Ё keeps the diaeresis visible but compresses it into the native
capital-height envelope instead of clipping four pixels above the cell.
All fail-closed checks remain active. English, every other Cyrillic glyph,
Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

BASE_COMMIT = "6593ba731a84d565b70d5e712a5ab7f0e01e90dd"
BASE_PATH = "ci/install_cyrillic_v3_3.py"
FULL_D = "0000003c24242424247e4242"
NARROW_D = "0000003c2424247e42420000"
FULL_YO = "0014003e20203e20203e0000"
NARROW_YO = "000000143e20203e203e0000"


def load_base() -> dict:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )
    ns = {
        "__name__": "qarro_cyrillic_v333_base",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    return ns


def main() -> int:
    ns = load_base()
    idx_d = ns["CYRILLIC"].index("Д")
    idx_yo = ns["CYRILLIC"].index("Ё")
    if ns["GLYPH_HEX"][idx_d] != FULL_D:
        raise RuntimeError("uppercase Д changed from verified v3.3.3 source")
    if ns["GLYPH_HEX"][idx_yo] != FULL_YO:
        raise RuntimeError("uppercase Ё changed from verified v3.3.3 source")

    original_patch_font = ns["patch_font"]

    def patch_font_narrow_specials(path):
        if path.name != "latin_narrow.png":
            return original_patch_font(path)

        saved = {
            idx_d: (ns["GLYPH_HEX"][idx_d], ns["SOURCE_BBOXES"][idx_d]),
            idx_yo: (ns["GLYPH_HEX"][idx_yo], ns["SOURCE_BBOXES"][idx_yo]),
        }
        try:
            ns["GLYPH_HEX"][idx_d] = NARROW_D
            ns["SOURCE_BBOXES"][idx_d] = ns["source_bbox"](NARROW_D)
            ns["GLYPH_HEX"][idx_yo] = NARROW_YO
            ns["SOURCE_BBOXES"][idx_yo] = ns["source_bbox"](NARROW_YO)
            print(
                "[cyrillic-v3333] latin_narrow: compact Д + Ё masks enabled; "
                "other font variants keep full forms"
            )
            return original_patch_font(path)
        finally:
            for idx, (old_hex, old_bbox) in saved.items():
                ns["GLYPH_HEX"][idx] = old_hex
                ns["SOURCE_BBOXES"][idx] = old_bbox

    ns["patch_font"] = patch_font_narrow_specials
    return int(ns["main"]() or 0)


if __name__ == "__main__":
    raise SystemExit(main())
