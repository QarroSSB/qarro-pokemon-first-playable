#!/usr/bin/env python3
"""Replace unsupported Russian guillemets with FireRed-supported curly quotes.

The early-Kanto localization intentionally runs fail-closed against pinned source
blocks. One translated Daisy/Clefairy flavor string used Unicode guillemets
(U+00AB/U+00BB), which the FireRed charmap rejects. The original game already
uses U+201C/U+201D curly quotes in the same string slot, so normalize only those
unsupported guillemets after the verified localization pass.

No gameplay, font raster, or protected Ash features are touched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_QUOTES_V3_18"
TARGET = Path("data/maps/PalletTown_RivalsHouse_Frlg/scripts.inc")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    text = path.read_text(encoding="utf-8")

    left = text.count("«")
    right = text.count("»")
    if left != 1 or right != 1:
        raise RuntimeError(
            f"fail-closed: expected exactly one guillemet pair in {TARGET}, "
            f"got left={left} right={right}"
        )

    text = text.replace("«", "“").replace("»", "”")
    path.write_text(text, encoding="utf-8")

    # Guard the full event-script tree against reintroducing either unsupported
    # guillemet later in the same CI run.
    offenders = []
    for p in (root / "data").rglob("*.inc"):
        s = p.read_text(encoding="utf-8")
        if "«" in s or "»" in s:
            offenders.append(str(p.relative_to(root)))
    if offenders:
        raise RuntimeError(f"unsupported guillemets remain: {offenders[:20]}")

    audit = {
        "marker": MARKER,
        "target": str(TARGET),
        "replacedLeftGuillemet": left,
        "replacedRightGuillemet": right,
        "replacement": "U+201C/U+201D FireRed-supported curly quotes",
        "fontTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_quotes_v3_18_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "[QARRO_RU_QUOTES_V3_18] PASS: one unsupported guillemet pair normalized "
        "to FireRed-supported curly quotes; font/gameplay/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
