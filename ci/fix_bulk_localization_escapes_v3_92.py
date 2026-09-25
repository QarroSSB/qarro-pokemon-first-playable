#!/usr/bin/env python3
"""Repair doubled FireRed text-control escapes from v3.90/v3.91 bulk passes.

The first bulk writer used json.dumps, which preserved Russian text correctly but
escaped FireRed control sequences as two backslashes (\\\\n/\\\\p/\\\\l).
The FireRed text preprocessor requires one backslash (\\n/\\p/\\l).
This pass is deliberately scoped to the five maps produced by v3.90/v3.91.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_FIX_BULK_LOCALIZATION_ESCAPES_V3_92"
FILES = [
    Path("data/maps/Route11_Frlg/scripts.inc"),
    Path("data/maps/Route12_Frlg/scripts.inc"),
    Path("data/maps/Route13_Frlg/scripts.inc"),
    Path("data/maps/Route17_Frlg/scripts.inc"),
    Path("data/maps/Route20_Frlg/scripts.inc"),
]
CONTROLS = ("n", "p", "l")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    changed_files: list[str] = []
    replacements = 0

    for rel in FILES:
        path = root / rel
        if not path.is_file():
            raise SystemExit(f"[{MARKER}] ERROR: missing {rel}")
        text = path.read_text(encoding="utf-8")
        original = text
        for code in CONTROLS:
            bad = "\\\\" + code   # two backslashes + FireRed control letter
            good = "\\" + code      # one backslash + FireRed control letter
            count = text.count(bad)
            if count:
                replacements += count
                text = text.replace(bad, good)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files.append(str(rel))

    if replacements == 0:
        raise SystemExit(f"[{MARKER}] ERROR: expected doubled control escapes, found none")

    audit = {
        "marker": MARKER,
        "replacements": replacements,
        "changedFiles": changed_files,
        "scope": "v3.90/v3.91 bulk localization maps only",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_fix_bulk_localization_escapes_v3_92_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: normalized {replacements} control escapes in {len(changed_files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
