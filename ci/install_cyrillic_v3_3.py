#!/usr/bin/env python3
"""Targeted follow-up for the first v3.3.3 per-font Cyrillic CI overflow.

Reuses the exact per-font scaler from commit 6593ba7 and changes only the
source bitmap for uppercase Cyrillic Д. In latin_narrow the original Д is two
source rows deeper than the ordinary uppercase baseline and scaled to y=0..18,
which correctly tripped the fail-closed 16px cell check.

The replacement removes one duplicated vertical body row while preserving the
same Д shape and one-row descender relative to А. No other glyph, charmap slot,
width rule, English text, Ash Bond or Ash Cap code is changed.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

BASE_COMMIT = "6593ba731a84d565b70d5e712a5ab7f0e01e90dd"
BASE_PATH = "ci/install_cyrillic_v3_3.py"
OLD_D = "0000003c24242424247e4242"
NEW_D = "0000003c242424247e424200"


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
    if ns["GLYPH_HEX"][idx] != OLD_D:
        raise RuntimeError(
            "uppercase Д source bitmap changed from the verified v3.3.3 baseline"
        )

    ns["GLYPH_HEX"][idx] = NEW_D
    ns["SOURCE_BBOXES"][idx] = ns["source_bbox"](NEW_D)

    print(
        "[cyrillic-v3331] uppercase Д: removed one duplicated body row to fit "
        "native narrow-font cell; all other glyph sources unchanged"
    )
    return int(ns["main"]() or 0)


if __name__ == "__main__":
    raise SystemExit(main())
