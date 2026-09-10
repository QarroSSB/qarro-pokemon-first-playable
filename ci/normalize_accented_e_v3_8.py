#!/usr/bin/env python3
"""Normalize literal accented e in game text after localization.

User choice: do not use a dedicated é glyph. Convert source text é/É to e/E
only after all localization passes have completed, so exact English anchors
used by the localization scripts remain valid during their own execution.

Charmap/font tables are deliberately excluded; the legacy FireRed slot stays
untouched but no authored game text should reference it after this pass.
After normalization, run the read-only RU font/localization foundation audit,
consolidated QoL/RU regression bundle, and protected Ash feature guard.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_NORMALIZE_E_V3_8"
ROOTS = ("data", "src", "include")
SUFFIXES = {".c", ".h", ".inc", ".s"}


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    changed_files: list[str] = []
    replaced = 0

    for dirname in ROOTS:
        base = root / dirname
        if not base.exists():
            raise RuntimeError(f"missing source root: {base}")
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            count = text.count("é") + text.count("É")
            if not count:
                continue
            new = text.replace("é", "e").replace("É", "E")
            path.write_text(new, encoding="utf-8")
            changed_files.append(str(path.relative_to(root)))
            replaced += count

    remaining: list[str] = []
    for dirname in ROOTS:
        base = root / dirname
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "é" in text or "É" in text:
                remaining.append(str(path.relative_to(root)))

    if remaining:
        raise RuntimeError(f"accented e remained in authored source: {remaining[:20]}")

    audit = {
        "marker": MARKER,
        "replacement": "é/É -> e/E",
        "replacements": replaced,
        "changedFiles": len(changed_files),
        "sampleFiles": changed_files[:50],
        "charmapTouched": False,
        "fontTablesTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_normalize_e_v3_8_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: normalized {replaced} accented-e literals in "
        f"{len(changed_files)} authored source files; charmap/font/Ash untouched"
    )

    here = Path(__file__).resolve().parent
    ru_audit = here / "audit_ru_foundation_v3_9.py"
    if not ru_audit.is_file():
        raise RuntimeError(f"missing RU foundation audit: {ru_audit}")
    subprocess.run([sys.executable, str(ru_audit), str(root)], check=True)

    bundle_audit = here / "audit_regression_bundle_v3_11.py"
    if not bundle_audit.is_file():
        raise RuntimeError(f"missing consolidated regression audit: {bundle_audit}")
    subprocess.run([sys.executable, str(bundle_audit), str(root)], check=True)

    protected_audit = here / "audit_protected_features_v3_13.py"
    if not protected_audit.is_file():
        raise RuntimeError(f"missing protected-feature audit: {protected_audit}")
    subprocess.run([sys.executable, str(protected_audit), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
