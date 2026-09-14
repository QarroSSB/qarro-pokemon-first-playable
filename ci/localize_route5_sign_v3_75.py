#!/usr/bin/env python3
"""Qarro v3.75 Route 5 sign Russian runtime localization.

Translates the single verified English-only Route 5 runtime text block remaining
in the current RU audit: the Underground Path sign. No gameplay logic, trainer
data, Ash Bond, or Ash Cap paths are touched. Pokemon species / move / ability
proper names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTE5_SIGN_V3_75"
REL = Path("data/maps/Route5_Frlg/scripts.inc")
LABEL = "Route5_Text_UndergroundPathSign"
NEEDLES = ("UNDERGROUND PATH", "CERULEAN CITY - VERMILION CITY")
REPLACEMENT = '''Route5_Text_UndergroundPathSign::
\t.string "ПОДЗЕМНЫЙ ПЕРЕХОД\\n"
\t.string "CERULEAN CITY - VERMILION CITY$"
'''

LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")


def replace_label_block(text: str) -> str:
    matches = list(re.finditer(rf"(?m)^{re.escape(LABEL)}::\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {LABEL}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    block = text[start:end]
    missing = [needle for needle in NEEDLES if needle not in block]
    if missing:
        raise SystemExit(f"{MARKER}: {LABEL}: pinned evidence mismatch; missing {missing}")
    if re.search(r"[А-Яа-яЁё]", block):
        raise SystemExit(f"{MARKER}: {LABEL}: block is already localized or unexpectedly contains Cyrillic")
    return text[:start] + REPLACEMENT + "\n" + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_route5_sign_v3_75.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    text = replace_label_block(text)
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_route5_sign_v3_75_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": [LABEL],
        "translatedBlockCount": 1,
        "scope": "single English-only Route 5 Underground Path sign from current RU runtime inventory",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "route5EnglishRuntimeClosed": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated Route 5 Underground Path sign; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
