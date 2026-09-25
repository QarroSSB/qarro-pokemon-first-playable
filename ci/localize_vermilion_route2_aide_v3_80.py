#!/usr/bin/env python3
"""Qarro v3.80 Vermilion Route 2 aide localization.

Translates exactly the next verified English-only Vermilion runtime block from
the fresh RU runtime inventory: Professor Oak's aide pointing the player back to
Route 2. Gameplay logic, trainer data, Ash Bond, and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_VERMILION_ROUTE2_AIDE_V3_80"
REL = Path("data/maps/VermilionCity_Frlg/scripts.inc")
LABEL = "VermilionCity_Text_Route2AideHasPackageForYou"
NEEDLES = (
    "Oh, hello, {PLAYER}!",
    "one of PROF. OAK's AIDES.",
    "He had a package from PROF. OAK",
    "He said he'd look for you around",
    "If you're in the ROUTE 2 area,",
)
REPLACEMENT = '''VermilionCity_Text_Route2AideHasPackageForYou::
\t.string "О, привет, {PLAYER}!\\n"
\t.string "Как твои дела?\\p"
\t.string "Это я, один из ПОМОЩНИКОВ\\n"
\t.string "PROF. OAK.\\p"
\t.string "Ты встречал другого ПОМОЩНИКА?\\p"
\t.string "У него была посылка от PROF. OAK\\n"
\t.string "для тебя, {PLAYER}.\\p"
\t.string "Он сказал, что будет искать тебя\\n"
\t.string "возле ROUTE 2, {PLAYER}.\\p"
\t.string "Если будешь в районе ROUTE 2,\\n"
\t.string "пожалуйста, найди его.$"
'''
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_vermilion_route2_aide_v3_80.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(rf"(?m)^{re.escape(LABEL)}::\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {LABEL}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    block = text[start:end]
    missing = [needle for needle in NEEDLES if needle not in block]
    if missing:
        raise SystemExit(f"{MARKER}: pinned evidence mismatch; missing {missing}")
    if re.search(r"[А-Яа-яЁё]", block):
        raise SystemExit(f"{MARKER}: target block is already localized or unexpectedly contains Cyrillic")
    text = text[:start] + REPLACEMENT + "\n" + text[end:]
    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_vermilion_route2_aide_v3_80_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "file": str(REL), "translatedBlocks": [LABEL], "translatedBlockCount": 1, "scope": "fresh-audit Vermilion Professor Oak aide Route 2 direction only", "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English", "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {LABEL}; Ash Bond/Ash Cap untouched")
    next_script = Path(__file__).with_name("localize_vermilion_fanclub_bike_voucher_v3_81.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
