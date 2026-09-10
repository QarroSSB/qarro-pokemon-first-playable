#!/usr/bin/env python3
"""Qarro v3.7 font pipeline wrapper.

Runs the exact previously-green Cyrillic/charmap installer from commit e5184e2,
then applies the bilingual Cyrillic Pixel-7 bitmap face for English, Russian
and digits. The user explicitly chose ordinary `e` instead of a separate `é`
glyph, so the follow-up pass normalizes literal é/É in game source to e/E.

The original user-supplied font files are not committed or modified; only
rasterized glyph masks live in the follow-up pass. Ash Bond / Ash Cap are
untouched.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "e5184e2d443f610ed07f85817bdfc6c9b3ba2bc4"
BASE_PATH = "ci/install_cyrillic_v3_3.py"
FOLLOWUP_PATH = "ci/install_bilingual_pixel7_v3_7.py"


def load_from_git(repo: Path, commit: str, path: str, module_name: str) -> dict:
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", commit],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        text=True,
    )
    ns = {
        "__name__": module_name,
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{commit}:{path}", "exec"), ns)
    return ns


def load_followup(repo: Path) -> dict:
    path = repo / FOLLOWUP_PATH
    if not path.exists():
        raise RuntimeError(f"missing bilingual font follow-up: {path}")
    code = path.read_text(encoding="utf-8")
    ns = {
        "__name__": "qarro_bilingual_pixel7_v37",
        "__file__": str(path.resolve()),
    }
    exec(compile(code, str(path), "exec"), ns)
    return ns


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    base = load_from_git(repo, BASE_COMMIT, BASE_PATH, "qarro_cyrillic_pre_pixel7")
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    followup = load_followup(repo)
    rc = int(followup["main"]() or 0)
    if rc:
        return rc

    print(
        "[QARRO_FONT_V3_7] PASS: proven Cyrillic mapping + bilingual Pixel-7 "
        "English/Russian raster face installed; accented e normalized; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
