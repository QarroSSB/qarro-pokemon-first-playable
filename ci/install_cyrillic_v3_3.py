#!/usr/bin/env python3
"""Qarro v3.8 readable bilingual FireRed-style font wrapper.

The Pixel-7 face was technically valid but proved too dense/condensed on a
real phone screen.  For readability, return to the previously-green Cyrillic
renderer from commit e5184e2 and keep FireRed's native English/digit glyphs.

That renderer scales the custom Cyrillic alphabet separately for each of the
nine native Latin atlas variants using the untouched FireRed A/a metrics and
baseline, so Russian text follows the same UI proportions without replacing
or deforming the original English face.

User decision for accented e is handled separately *after* localization:
literal é/É in game text is normalized to ordinary e/E.  The legacy glyph
slot remains untouched and unused.

No Ash Bond / Ash Cap changes.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "e5184e2d443f610ed07f85817bdfc6c9b3ba2bc4"
BASE_PATH = "ci/install_cyrillic_v3_3.py"


def load_base(repo: Path) -> dict:
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )
    ns = {
        "__name__": "qarro_readable_frlg_cyrillic_v38",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    return ns


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    base = load_base(repo)
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    print(
        "[QARRO_FONT_V3_8] PASS: native FireRed English/digits preserved; "
        "readable per-atlas Cyrillic installed; Pixel-7 disabled; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
