#!/usr/bin/env python3
"""Qarro v3.83 S.S. Anne Kitchen localization.

Translates the ten verified English-only runtime text blocks in the S.S. Anne
Kitchen from pinned upstream. Gameplay logic, flags, trainer data, Ash Bond,
and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_SSANNE_KITCHEN_V3_83"
REL = Path("data/maps/SSAnne_Kitchen_Frlg/scripts.inc")
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

REPLACEMENTS = {
    "SSAnne_Kitchen_Text_BusyOutOfTheWay": (("You, mon petit!", "We're busy here!", "Out of the way!"), '''SSAnne_Kitchen_Text_BusyOutOfTheWay::
\t.string "Эй, mon petit!\\n"
\t.string "Мы тут заняты!\\l"
\t.string "Не мешай!$"
'''),
    "SSAnne_Kitchen_Text_SawOddBerryInTrash": (("I saw an odd BERRY in the trash.", "I wonder what that was?"), '''SSAnne_Kitchen_Text_SawOddBerryInTrash::
\t.string "Я видел странную BERRY в мусоре.\\n"
\t.string "Интересно, что это было?$"
'''),
    "SSAnne_Kitchen_Text_SoBusyImDizzy": (("I'm so busy I'm getting dizzy!", "You have to give me room here!"), '''SSAnne_Kitchen_Text_SoBusyImDizzy::
\t.string "Столько работы — голова кругом!\\n"
\t.string "Дай мне место работать!$"
'''),
    "SSAnne_Kitchen_Text_PeelSpudsEveryDay": (("I peel spuds every day!",), '''SSAnne_Kitchen_Text_PeelSpudsEveryDay::
\t.string "Хм-м, хм-м...\\p"
\t.string "Я каждый день чищу картошку!\\n"
\t.string "Хм-м...$"
'''),
    "SSAnne_Kitchen_Text_HearAboutSnorlaxItsAGlutton": (("Did you hear about SNORLAX?", "It's a glutton.", "No other POKéMON eats and sleeps"), '''SSAnne_Kitchen_Text_HearAboutSnorlaxItsAGlutton::
\t.string "Слышал про SNORLAX?\\n"
\t.string "Вот уж обжора.\\p"
\t.string "Ни один ПОКЕМОН не ест и не спит\\n"
\t.string "столько, сколько SNORLAX!$"
'''),
    "SSAnne_Kitchen_Text_OnlyGetToPeelOnions": (("I only get to peel onions",), '''SSAnne_Kitchen_Text_OnlyGetToPeelOnions::
\t.string "Всхлип... Шмыг...\\p"
\t.string "А мне дают чистить только лук...\\n"
\t.string "Всхлип...$"
'''),
    "SSAnne_Kitchen_Text_IAmLeChefMainCourseIs": (("Indeed I am le CHEF!", "Le main course is"), '''SSAnne_Kitchen_Text_IAmLeChefMainCourseIs::
\t.string "Кхм!\\n"
\t.string "Да, я le CHEF!\\p"
\t.string "Сегодня главное блюдо —$"
'''),
    "SSAnne_Kitchen_Text_SalmonDuSalad": (("Salmon du Salad!", "Les guests may gripe it's fish"), '''SSAnne_Kitchen_Text_SalmonDuSalad::
\t.string "Salmon du Salad!\\p"
\t.string "Les guests опять будут ворчать,\\n"
\t.string "что снова рыба!$"
'''),
    "SSAnne_Kitchen_Text_EelsAuBarbecue": (("Eels au Barbecue!", "Les guests will mutiny"), '''SSAnne_Kitchen_Text_EelsAuBarbecue::
\t.string "Eels au Barbecue!\\p"
\t.string "Боюсь, les guests взбунтуются.$"
'''),
    "SSAnne_Kitchen_Text_PrimeBeefsteak": (("Prime Beefsteak!", "have I enough fillets du", "beef?"), '''SSAnne_Kitchen_Text_PrimeBeefsteak::
\t.string "Prime Beefsteak!\\p"
\t.string "Но хватит ли у меня fillets du\\n"
\t.string "beef?$"
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
        raise SystemExit("usage: localize_ssanne_kitchen_v3_83.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_ssanne_kitchen_v3_83_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "file": str(REL), "translatedBlocks": list(REPLACEMENTS), "translatedBlockCount": len(REPLACEMENTS), "scope": "pinned-upstream S.S. Anne Kitchen runtime text only", "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English", "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(REPLACEMENTS)} S.S. Anne Kitchen blocks; Ash Bond/Ash Cap untouched")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
