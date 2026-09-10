#!/usr/bin/env python3
"""Qarro v3.7 Oak-lab localization wrapper + accented-e normalization.

Runs the exact previously-green Oak lab localization from commit 0ddb5e3,
then, only after all core/Oak localization anchors have been consumed,
normalizes literal é/É in game source to ordinary e/E.

This ordering is intentional: earlier localization passes still match the
pinned FireRed source text containing POKéMON, while the final built ROM no
longer requests a dedicated é glyph.

Ash Bond / Ash Cap are untouched.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "0ddb5e33c653bc4550cecb18d5e0440232df7a8a"
BASE_PATH = "ci/localize_oaks_lab_starter_v3_5.py"
MARKER = "QARRO_POST_LOCALIZATION_E_V3_7"


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
        "__name__": "qarro_oak_lab_pre_e_normalization",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    return ns


def normalize_accented_e(root: Path) -> tuple[int, int]:
    roots = [root / "src", root / "data", root / "include"]
    suffixes = {".c", ".h", ".inc", ".s", ".txt"}
    changed_files = 0
    replacements = 0

    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            count = text.count("é") + text.count("É")
            if not count:
                continue

            path.write_text(
                text.replace("é", "e").replace("É", "E"),
                encoding="utf-8",
            )
            replacements += count
            changed_files += 1

    return replacements, changed_files


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    base = load_base(repo)
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    replacements, changed_files = normalize_accented_e(root)

    leftovers = []
    for base_dir in (root / "src", root / "data", root / "include"):
        if not base_dir.exists():
            continue
        for path in base_dir.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".c", ".h", ".inc", ".s", ".txt"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "é" in text or "É" in text:
                leftovers.append(str(path.relative_to(root)))
                if len(leftovers) >= 10:
                    break
        if leftovers:
            break

    if leftovers:
        raise RuntimeError(f"accented e remained after normalization: {leftovers}")

    audit_path = root / "build/qarro_ru_oak_lab_starter_v3_5_audit.json"
    audit = {}
    if audit_path.exists():
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
    audit.update(
        {
            "postLocalizationAccentedENormalized": True,
            "accentedEReplacements": replacements,
            "accentedEChangedFiles": changed_files,
            "specialAccentedEGlyphRequired": False,
        }
    )
    audit_path.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"[{MARKER}] PASS: {replacements} literal é/É -> e/E replacements "
        f"in {changed_files} files after localization; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
