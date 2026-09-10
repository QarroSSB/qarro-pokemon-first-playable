#!/usr/bin/env python3
"""Qarro v3.21 Qarro Pixel Straight Solid wrapper.

Runs the exact previously-green Cyrillic/charmap installer from commit e5184e2,
then overlays English, Russian and digit glyphs with Qarro Pixel Straight Solid:
crisp 7-row custom GBA bitmap glyphs, no slant, no bitmap scaling, no gray
letter shadow, and a same-colour 1px lower-right support pass for solid strokes.
Dedicated Cyrillic readability forms are preserved.

Literal é/É is still normalized to ordinary e/E after localization.
No Ash Bond / Ash Cap changes.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "e5184e2d443f610ed07f85817bdfc6c9b3ba2bc4"
BASE_PATH = "ci/install_cyrillic_v3_3.py"
FOLLOWUP_PATH = "ci/install_bilingual_qarro_pixel_straight_solid_v3_21.py"


def load_from_git(repo: Path, commit: str, path: str, module_name: str) -> dict:
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", commit],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        text=True,
    )
    ns = {"__name__": module_name, "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{commit}:{path}", "exec"), ns)
    return ns


def load_followup(repo: Path) -> dict:
    path = repo / FOLLOWUP_PATH
    if not path.exists():
        raise RuntimeError(f"missing Qarro Pixel Straight Solid follow-up: {path}")
    code = path.read_text(encoding="utf-8")
    ns = {"__name__": "qarro_bilingual_pixel_straight_solid_v321", "__file__": str(path.resolve())}
    exec(compile(code, str(path), "exec"), ns)
    return ns


def main() -> int:
    repo = Path(__file__).resolve().parents[1]

    base = load_from_git(repo, BASE_COMMIT, BASE_PATH, "qarro_cyrillic_pre_pixel_straight_solid_v321")
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    followup = load_followup(repo)
    rc = int(followup["main"]() or 0)
    if rc:
        return rc

    print(
        "[QARRO_FONT_V3_21] PASS: Qarro Pixel Straight Solid English/Russian/digits installed; "
        "upright/no scaling; gray shadow OFF; same-colour support ON; Cyrillic т/У distinct; "
        "ordinary e policy preserved; Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
