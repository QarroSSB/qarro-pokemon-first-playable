#!/usr/bin/env python3
"""Qarro v3.84 S.S. Anne Deck localization.

Translates the nine verified English-only runtime text blocks on the S.S. Anne
Deck from pinned upstream. Gameplay logic, flags, trainer data, Ash Bond, and
Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_SSANNE_DECK_V3_84"
REL = Path("data/maps/SSAnne_Deck_Frlg/scripts.inc")
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

REPLACEMENTS = {
    "SSAnne_Deck_Text_ShipDepartingSoon": (("The party's over.", "The ship will be departing soon."), '''SSAnne_Deck_Text_ShipDepartingSoon::
\t.string "Вечеринка окончена.\\n"
\t.string "Корабль скоро отправляется.$"
'''),
    "SSAnne_Deck_Text_ScrubbingDecksHardWork": (("Whew!", "Scrubbing decks is hard work!"), '''SSAnne_Deck_Text_ScrubbingDecksHardWork::
\t.string "Уф!\\n"
\t.string "Драить палубу — тяжёлая работа!$"
'''),
    "SSAnne_Deck_Text_FeelSeasick": (("I feel ill", "I got seasick", "get some air"), '''SSAnne_Deck_Text_FeelSeasick::
\t.string "Уф... Мне нехорошо...\\p"
\t.string "Меня укачало, и я вышел\\n"
\t.string "подышать свежим воздухом...$"
'''),
    "SSAnne_Deck_Text_EdmondIntro": (("Hey, matey!", "Let's do a little jig!"), '''SSAnne_Deck_Text_EdmondIntro::
\t.string "Эй, приятель!\\p"
\t.string "Давай немного попляшем!$"
'''),
    "SSAnne_Deck_Text_EdmondDefeat": (("You're impressive!",), '''SSAnne_Deck_Text_EdmondDefeat::
\t.string "Впечатляет!$"
'''),
    "SSAnne_Deck_Text_EdmondPostBattle": (("How many kinds of POKéMON", "this big world?"), '''SSAnne_Deck_Text_EdmondPostBattle::
\t.string "Как думаешь, сколько видов ПОКЕМОНОВ\\n"
\t.string "есть в этом огромном мире?$"
'''),
    "SSAnne_Deck_Text_TrevorIntro": (("Ahoy, there!", "Are you seasick?"), '''SSAnne_Deck_Text_TrevorIntro::
\t.string "Эй, на палубе!\\n"
\t.string "Тебя не укачало?$"
'''),
    "SSAnne_Deck_Text_TrevorDefeat": (("I was just careless!",), '''SSAnne_Deck_Text_TrevorDefeat::
\t.string "Я просто был неосторожен!$"
'''),
    "SSAnne_Deck_Text_TrevorPostBattle": (("My pa said there are 100 kinds", "I think there are more."), '''SSAnne_Deck_Text_TrevorPostBattle::
\t.string "Папа говорил, что есть 100 видов\\n"
\t.string "ПОКЕМОНОВ. Думаю, их больше.$"
'''),
}


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_ssanne_deck_v3_84.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    for label, (needles, replacement) in REPLACEMENTS.items():
        start, end, block = block_bounds(text, label)
        missing = [needle for needle in needles if needle not in block]
        if missing:
            raise SystemExit(f"{MARKER}: {label}: pinned evidence mismatch; missing {missing}")
        if re.search(r"[А-Яа-яЁё]", block):
            raise SystemExit(f"{MARKER}: {label}: already localized or unexpectedly contains Cyrillic")
        text = text[:start] + replacement + "\n" + text[end:]
    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_ssanne_deck_v3_84_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "file": str(REL), "translatedBlocks": list(REPLACEMENTS), "translatedBlockCount": len(REPLACEMENTS), "scope": "pinned-upstream S.S. Anne Deck runtime text only", "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English", "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(REPLACEMENTS)} S.S. Anne Deck blocks; Ash Bond/Ash Cap untouched")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
