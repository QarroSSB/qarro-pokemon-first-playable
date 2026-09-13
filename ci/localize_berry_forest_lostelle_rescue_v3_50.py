#!/usr/bin/env python3
"""Qarro v3.50 mandatory Berry Forest Lostelle rescue localization.

Translates only the verified Lostelle rescue runtime chain in Berry Forest:
help request, Hypno encounter warning, post-battle thanks, the conditional full
Berry Pouch message, and the return-home transition. Optional signs/NPC text and
later Sevii postgame remain untouched. Pokemon species / move / ability proper
names remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_BERRY_FOREST_LOSTELLE_RESCUE_V3_50"
REL = Path("data/maps/ThreeIsland_BerryForest_Frlg/scripts.inc")

PATCHES = {
    "ThreeIsland_BerryForest_Text_HelpScaryPokemon": (
        '''ThreeIsland_BerryForest_Text_HelpScaryPokemon::
\t.string "LOSTELLE: Whimper… Sniff…\\n"
\t.string "Oh! Please, help!\\p"
\t.string "A scary POKéMON appeared there\\n"
\t.string "a little while ago.\\p"
\t.string "It kept scaring.\\n"
\t.string "It made LOSTELLE scared.\\p"
\t.string "I'm too scared to move!\\n"
\t.string "But I want to go home…$"
''',
        '''ThreeIsland_BerryForest_Text_HelpScaryPokemon::
\t.string "LOSTELLE: Хнык… Всхлип…\\n"
\t.string "Ой! Пожалуйста, помоги!\\p"
\t.string "Недавно здесь появился страшный\\n"
\t.string "POKéMON.\\p"
\t.string "Он всё пугал меня.\\n"
\t.string "LOSTELLE очень страшно.\\p"
\t.string "Я так боюсь, что не могу идти!\\n"
\t.string "Но я хочу домой…$"
''',
    ),
    "ThreeIsland_BerryForest_Text_HereItComesAgain": (
        '''ThreeIsland_BerryForest_Text_HereItComesAgain::
\t.string "Oh! Here it comes again!\\n"
\t.string "No! Go away! It's scaring me!\\p"
\t.string "Waaaaaaah!\\n"
\t.string "I want my daddy!$"
''',
        '''ThreeIsland_BerryForest_Text_HereItComesAgain::
\t.string "Ой! Он снова идёт!\\n"
\t.string "Нет! Уходи! Мне страшно!\\p"
\t.string "А-а-а-а-а!\\n"
\t.string "Я хочу к папе!$"
''',
    ),
    "ThreeIsland_BerryForest_Text_ThankYouHaveThis": (
        '''ThreeIsland_BerryForest_Text_ThankYouHaveThis::
\t.string "Ohh! That was so scary!\\n"
\t.string "Thank you!\\p"
\t.string "LOSTELLE came to pick some\\n"
\t.string "BERRIES.\\p"
\t.string "You can have this!$"
''',
        '''ThreeIsland_BerryForest_Text_ThankYouHaveThis::
\t.string "Ох! Было так страшно!\\n"
\t.string "Спасибо тебе!\\p"
\t.string "LOSTELLE пришла сюда собирать\\n"
\t.string "ягоды.\\p"
\t.string "Возьми вот это!$"
''',
    ),
    "ThreeIsland_BerryForest_Text_LetsGoHome": (
        '''ThreeIsland_BerryForest_Text_LetsGoHome::
\t.string "What's your name?\\p"
\t.string "LOSTELLE's scared, so can I go\\n"
\t.string "with you to my daddy's house?\\p"
\t.string "Okay!\\n"
\t.string "Let's go home!$"
''',
        '''ThreeIsland_BerryForest_Text_LetsGoHome::
\t.string "Как тебя зовут?\\p"
\t.string "LOSTELLE всё ещё страшно. Можно я\\n"
\t.string "пойду с тобой к папе?\\p"
\t.string "Хорошо!\\n"
\t.string "Пойдём домой!$"
''',
    ),
    "ThreeIsland_BerryForest_Text_BerryPouchIsFull": (
        '''ThreeIsland_BerryForest_Text_BerryPouchIsFull::
\t.string "Your BERRY POUCH is full.\\n"
\t.string "I guess you don't want this.$"
''',
        '''ThreeIsland_BerryForest_Text_BerryPouchIsFull::
\t.string "Твой BERRY POUCH заполнен.\\n"
\t.string "Наверное, тебе это не нужно.$"
''',
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_berry_forest_lostelle_rescue_v3_50.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied = []

    for label, (pinned, ru) in PATCHES.items():
        variants = [pinned]
        normalized = pinned.replace("é", "e").replace("É", "E")
        if normalized != pinned:
            variants.append(normalized)
        hits = [(variant, text.count(variant)) for variant in variants]
        total = sum(count for _, count in hits)
        if total != 1:
            raise SystemExit(f"{MARKER}: {label}: expected exactly one pinned/normalized anchor, found {total}")
        source = next(variant for variant, count in hits if count == 1)
        text = text.replace(source, ru, 1)
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_berry_forest_lostelle_rescue_v3_50_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Berry Forest Lostelle rescue and conditional full-pouch runtime branch",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Berry Forest Lostelle rescue runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
