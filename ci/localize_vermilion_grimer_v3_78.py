#!/usr/bin/env python3
"""Qarro v3.78 Vermilion city first remaining runtime localization.

Translates exactly one verified English-only Vermilion City NPC block after the
v3.77 boarding pass. No gameplay logic, trainer data, Ash Bond, or Ash Cap paths
are touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_VERMILION_GRIMER_V3_78"
REL = Path("data/maps/VermilionCity_Frlg/scripts.inc")
LABEL = "VermilionCity_Text_GrimerMultipliesInSludge"
NEEDLES = ("We're careful about pollution here.", "GRIMER multiplies in", "toxic sludge.")
REPLACEMENT = '''VermilionCity_Text_GrimerMultipliesInSludge::
\t.string "Мы здесь внимательно следим за\\n"
\t.string "загрязнением.\\p"
\t.string "Говорят, GRIMER размножается\\n"
\t.string "в токсичных отходах.$"
'''
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_vermilion_grimer_v3_78.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_vermilion_grimer_v3_78_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "file": str(REL), "translatedBlocks": [LABEL], "translatedBlockCount": 1, "scope": "first verified remaining English-only Vermilion City runtime block after v3.77", "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English", "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {LABEL}; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
