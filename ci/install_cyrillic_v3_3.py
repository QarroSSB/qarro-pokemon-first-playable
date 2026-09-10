#!/usr/bin/env python3
"""Qarro v3.17 approved Qarro Pixel Variant 2 wrapper.

Runs the exact previously-green Cyrillic/charmap installer from commit e5184e2,
then overlays English, Russian and digit glyphs with the approved Qarro Pixel
Variant 2: a crisp custom GBA bitmap font with only a very light top-row slant
and dedicated Cyrillic readability forms.

Literal é/É is still normalized to ordinary e/E after localization.
No Ash Bond / Ash Cap changes.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "e5184e2d443f610ed07f85817bdfc6c9b3ba2bc4"
BASE_PATH = "ci/install_cyrillic_v3_3.py"
FOLLOWUP_PATH = "ci/install_bilingual_qarro_pixel_light_slant_v3_17.py"


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
        raise RuntimeError(f"missing Qarro Pixel Variant 2 follow-up: {path}")
    code = path.read_text(encoding="utf-8")
    ns = {
        "__name__": "qarro_bilingual_pixel_variant2_v317",
        "__file__": str(path.resolve()),
    }
    exec(compile(code, str(path), "exec"), ns)
    return ns


def main() -> int:
    repo = Path(__file__).resolve().parents[1]

    base = load_from_git(
        repo,
        BASE_COMMIT,
        BASE_PATH,
        "qarro_cyrillic_pre_pixel_variant2_v317",
    )
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    followup = load_followup(repo)
    rc = int(followup["main"]() or 0)
    if rc:
        return rc

    print(
        "[QARRO_FONT_V3_17] PASS: approved Qarro Pixel Variant 2 English/Russian/digits "
        "installed; light top-row slant; Cyrillic т/У distinct; ordinary e policy preserved; Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
