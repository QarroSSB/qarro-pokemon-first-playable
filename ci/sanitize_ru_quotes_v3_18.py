#!/usr/bin/env python3
"""Normalize unsupported Unicode punctuation after Russian localization.

The verified localization passes intentionally fail closed against pinned source
blocks, but translated prose can still introduce typographic characters that
FireRed's assembler/charmap does not accept. Keep the proven Pallet guillemet
normalization and additionally normalize U+2014 EM DASH in event-script .inc
files to an ASCII hyphen before the real ARM build.

No gameplay, font raster, trainer data, or protected Ash features are touched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_QUOTES_V3_19"
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

    # U+2014 is rejected by the pinned FireRed assembler/charmap. Normalize it
    # after all verified localization layers so future Russian prose cannot
    # reintroduce the same late make-firered failure.
    em_dash_replacements = 0
    data_root = root / "data"
    for p in data_root.rglob("*.inc"):
        s = p.read_text(encoding="utf-8")
        count = s.count("—")
        if count:
            p.write_text(s.replace("—", "-"), encoding="utf-8")
            em_dash_replacements += count

    # Guard the full event-script tree against reintroducing unsupported
    # guillemets or em dashes later in the same CI run.
    offenders = []
    for p in data_root.rglob("*.inc"):
        s = p.read_text(encoding="utf-8")
        if "«" in s or "»" in s or "—" in s:
            offenders.append(str(p.relative_to(root)))
    if offenders:
        raise RuntimeError(f"unsupported punctuation remains: {offenders[:20]}")

    audit = {
        "marker": MARKER,
        "target": str(TARGET),
        "replacedLeftGuillemet": left,
        "replacedRightGuillemet": right,
        "guillemetReplacement": "U+201C/U+201D FireRed-supported curly quotes",
        "replacedEmDash": em_dash_replacements,
        "emDashReplacement": "ASCII hyphen",
        "fontTouched": False,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_quotes_v3_18_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: guillemets normalized; {em_dash_replacements} unsupported "
        "em dash(es) normalized; font/gameplay/trainer/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
