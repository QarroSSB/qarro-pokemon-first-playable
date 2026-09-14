#!/usr/bin/env python3
"""Qarro v3.79 Vermilion Gym advice localization.

Translates exactly the next verified English-only Vermilion runtime block from
the fresh RU runtime inventory: the Gym Guy pre-Surge advice. Gameplay logic,
trainer data, Ash Bond, and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_VERMILION_GYM_ADVICE_V3_79"
REL = Path("data/maps/VermilionCity_Gym_Frlg/scripts.inc")
LABEL = "VermilionCity_Gym_Text_GymGuyAdvice"
NEEDLES = (
    "Champ in the making!",
    "Lightning American!",
    "He's an expert on electric",
    "Beware of paralysis, too.",
    "He's locked himself in",
)
REPLACEMENT = '''VermilionCity_Gym_Text_GymGuyAdvice::
\t.string "Йо!\\n"
\t.string "Будущий чемпион!\\p"
\t.string "У LT. SURGE есть прозвище.\\p"
\t.string "Его зовут Электрическим\\n"
\t.string "Американцем!\\p"
\t.string "Он эксперт по электрическим\\n"
\t.string "ПОКЕМОНАМ.\\p"
\t.string "ПОКЕМОНАМ типов BIRD/WATER\\n"
\t.string "тяжело против ELECTRIC.\\p"
\t.string "Остерегайся и паралича.\\p"
\t.string "LT. SURGE очень осторожен.\\p"
\t.string "Он заперся внутри, так что\\n"
\t.string "добраться до него будет нелегко.$"
'''
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_vermilion_gym_advice_v3_79.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_vermilion_gym_advice_v3_79_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "file": str(REL), "translatedBlocks": [LABEL], "translatedBlockCount": 1, "scope": "fresh-audit Vermilion Gym Guy pre-Surge advice only", "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English", "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {LABEL}; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
