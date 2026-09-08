#!/usr/bin/env python3
"""Targeted follow-up for the first v3.3.3 per-font Cyrillic overflow.

Reuses the exact per-font scaler from commit 6593ba7. Only while rendering
latin_narrow.png, uppercase Cyrillic Д uses a compact narrow-font source mask.
The original full Д remains unchanged in all other eight font atlases.

Run #50 proved the full glyph overflowed latin_narrow to y=18. Run #51 proved
removing one body row still reached y=16 including shadow. This narrow-only
mask removes the final excess row without clipping or weakening fail-closed
checks. English, all other Cyrillic glyphs, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

BASE_COMMIT = "6593ba731a84d565b70d5e712a5ab7f0e01e90dd"
BASE_PATH = "ci/install_cyrillic_v3_3.py"
FULL_D = "0000003c24242424247e4242"
NARROW_D = "0000003c2424247e42420000"


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
    idx = ns["CYRILLIC"].index("Д")
    if ns["GLYPH_HEX"][idx] != FULL_D:
        raise RuntimeError("uppercase Д changed from verified v3.3.3 source")

    original_patch_font = ns["patch_font"]

    def patch_font_narrow_d(path):
        if path.name != "latin_narrow.png":
            return original_patch_font(path)

        old_hex = ns["GLYPH_HEX"][idx]
        old_bbox = ns["SOURCE_BBOXES"][idx]
        try:
            ns["GLYPH_HEX"][idx] = NARROW_D
            ns["SOURCE_BBOXES"][idx] = ns["source_bbox"](NARROW_D)
            print(
                "[cyrillic-v3332] latin_narrow: compact uppercase Д mask "
                "enabled; other font variants keep full Д"
            )
            return original_patch_font(path)
        finally:
            ns["GLYPH_HEX"][idx] = old_hex
            ns["SOURCE_BBOXES"][idx] = old_bbox

    ns["patch_font"] = patch_font_narrow_d
    return int(ns["main"]() or 0)


if __name__ == "__main__":
    raise SystemExit(main())
