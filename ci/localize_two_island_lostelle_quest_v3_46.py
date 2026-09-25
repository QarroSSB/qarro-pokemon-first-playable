#!/usr/bin/env python3
"""Qarro v3.46 mandatory Two Island Lostelle quest Russian localization.

Translates only the verified pinned forced Joyful Game Corner scene that sends
the player from Two Island to search for Lostelle on Three Island. Optional
Game Corner dialogue, rescue-return rewards, and later postgame text are
intentionally untouched. Pokemon species / move / ability proper names remain
English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_TWO_ISLAND_LOSTELLE_QUEST_V3_46"
REL = Path("data/maps/TwoIsland_JoyfulGameCorner_Frlg/scripts.inc")

PATCHES = {
    "TwoIsland_JoyfulGameCorner_Text_WhereHasLostelleGottenTo": (
        r'''TwoIsland_JoyfulGameCorner_Text_WhereHasLostelleGottenTo::
	.string "Now, where's LOSTELLE gotten to\n"
	.string "today?\p"
	.string "She always brings me lunch every\n"
	.string "day right about now…$"
''',
        r'''TwoIsland_JoyfulGameCorner_Text_WhereHasLostelleGottenTo::
	.string "Куда же сегодня подевалась\n"
	.string "LOSTELLE?\p"
	.string "Обычно она приносит мне обед\n"
	.string "примерно в это время…$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_PleaseHelpFindLostelle": (
        r'''TwoIsland_JoyfulGameCorner_Text_PleaseHelpFindLostelle::
	.string "Hm? You, there!\n"
	.string "Are you a friend of LOSTELLE's?\p"
	.string "Have you seen LOSTELLE around?\n"
	.string "I don't know where she might be.\l"
	.string "She should've been here long ago.\p"
	.string "LOSTELLE's a cutie - she got my\n"
	.string "looks - so what if someone…\p"
	.string "What if something's happened to\n"
	.string "my LOSTELLE?!\p"
	.string "Please, help me find her!\n"
	.string "Please go search THREE ISLAND!$"
''',
        r'''TwoIsland_JoyfulGameCorner_Text_PleaseHelpFindLostelle::
	.string "Хм? Эй, ты!\n"
	.string "Ты друг LOSTELLE?\p"
	.string "Ты не видел её?\n"
	.string "Не знаю, где она может быть.\l"
	.string "Она давно должна была прийти.\p"
	.string "LOSTELLE такая милая - вся в меня.\n"
	.string "А вдруг кто-то…\p"
	.string "Вдруг с моей LOSTELLE\n"
	.string "что-то случилось?!\p"
	.string "Пожалуйста, помоги найти её!\n"
	.string "Ищи её на THREE ISLAND!$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_IsThisOnlyThreeIsland": (
        r'''TwoIsland_JoyfulGameCorner_Text_IsThisOnlyThreeIsland::
	.string "Hah? What is this GAME CORNER?\n"
	.string "How much sadder can this get?\p"
	.string "Those clowns…\p"
	.string "They said they'd be waiting on the\n"
	.string "island, so where are they?\p"
	.string "Hey, you! Is this the only THREE\n"
	.string "ISLAND around here?$"
''',
        r'''TwoIsland_JoyfulGameCorner_Text_IsThisOnlyThreeIsland::
	.string "А? Это что за GAME CORNER?\n"
	.string "Куда уж унылее?\p"
	.string "Эти клоуны…\p"
	.string "Сказали, что ждут на острове.\n"
	.string "И где они?\p"
	.string "Эй, ты! Это и есть\n"
	.string "THREE ISLAND?$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_ThisIsTwoIslandMoveIt": (
        r'''TwoIsland_JoyfulGameCorner_Text_ThisIsTwoIslandMoveIt::
	.string "Try waking up before you crawl out\n"
	.string "of bed, you punk.\p"
	.string "This is TWO ISLAND!\p"
	.string "Move it! Get your filthy motorbike\n"
	.string "out of my place!$"
''',
        r'''TwoIsland_JoyfulGameCorner_Text_ThisIsTwoIslandMoveIt::
	.string "Проснись сначала, прежде чем\n"
	.string "вылезать из постели, хулиган.\p"
	.string "Это TWO ISLAND!\p"
	.string "А ну убери свой грязный байк\n"
	.string "из моего заведения!$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_TheseIslandsAreConfusing": (
        r'''TwoIsland_JoyfulGameCorner_Text_TheseIslandsAreConfusing::
	.string "Huh…\n"
	.string "Oh, oh, gotcha.\p"
	.string "Tch…\n"
	.string "These islands are confusing…$"
''',
        r'''TwoIsland_JoyfulGameCorner_Text_TheseIslandsAreConfusing::
	.string "А…\n"
	.string "А, понял.\p"
	.string "Тц…\n"
	.string "Запутанные тут острова…$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_PunkScuffedUpMyFloor": (
        r'''TwoIsland_JoyfulGameCorner_Text_PunkScuffedUpMyFloor::
	.string "Would you look at that?\n"
	.string "That punk scuffed up my floor.$"
''',
        r'''TwoIsland_JoyfulGameCorner_Text_PunkScuffedUpMyFloor::
	.string "Ты только посмотри!\n"
	.string "Этот хулиган исцарапал мой пол.$"
''',
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_two_island_lostelle_quest_v3_46.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_two_island_lostelle_quest_v3_46_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Two Island Lostelle quest runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
