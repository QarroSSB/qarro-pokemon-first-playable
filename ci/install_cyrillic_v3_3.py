#!/usr/bin/env python3
"""Targeted narrow-font fixes for the v3.3.3 per-font Cyrillic scaler.

Reuses the exact per-font scaler from commit 6593ba7. Only while rendering
latin_narrow.png, uppercase Cyrillic Д, Ё and Й use compact source masks. Their
full source forms remain unchanged in all other eight font atlases.

CI history:
- run #50: full Д overflowed latin_narrow to y=18;
- run #51: first compact Д still reached y=16 including shadow;
- run #52: narrow Д passed; Ё failed at y=-4..14;
- run #53: narrow Д and Ё passed; Й failed at y=-4..16.

The narrow Й compresses its breve and body into the native capital-height
window without clipping. All fail-closed checks remain active. English, every
other Cyrillic glyph, Ash Bond and Ash Cap are untouched.
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
FULL_SHORT_I = "0028380026262e2a3a323200"
NARROW_SHORT_I = "00000038262e2a3a32320000"


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
    specials = {
        "Д": (FULL_D, NARROW_D),
        "Ё": (FULL_YO, NARROW_YO),
        "Й": (FULL_SHORT_I, NARROW_SHORT_I),
    }
    indices = {ch: ns["CYRILLIC"].index(ch) for ch in specials}
    for ch, (full, _) in specials.items():
        if ns["GLYPH_HEX"][indices[ch]] != full:
            raise RuntimeError(f"uppercase {ch} changed from verified v3.3.3 source")

    original_patch_font = ns["patch_font"]

    def patch_font_narrow_specials(path):
        if path.name != "latin_narrow.png":
            return original_patch_font(path)

        saved = {
            idx: (ns["GLYPH_HEX"][idx], ns["SOURCE_BBOXES"][idx])
            for idx in indices.values()
        }
        try:
            for ch, (_, narrow) in specials.items():
                idx = indices[ch]
                ns["GLYPH_HEX"][idx] = narrow
                ns["SOURCE_BBOXES"][idx] = ns["source_bbox"](narrow)
            print(
                "[cyrillic-v3334] latin_narrow: compact Д + Ё + Й masks enabled; "
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
