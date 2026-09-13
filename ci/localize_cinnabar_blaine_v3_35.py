#!/usr/bin/env python3
"""Qarro v3.35 mandatory Cinnabar Gym / Blaine Russian runtime localization.

Translates only the verified pinned Blaine progression chain: intro, defeat,
Volcano Badge explanation, TM38 receipt/explanation, no-bag-space line, and
post-battle dialogue. Pokemon species / move / ability proper names remain
English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_CINNABAR_BLAINE_V3_35"
REL = Path("data/maps/CinnabarIsland_Gym_Frlg/scripts.inc")

PATCHES = {
    "CinnabarIsland_Gym_Text_BlaineIntro": (
        "CinnabarIsland_Gym_Text_BlaineIntro::\n\t.string \"Hah!\\p\"\n\t.string \"I am BLAINE, the red-hot LEADER\\n\"\n\t.string \"of CINNABAR GYM!\\p\"\n\t.string \"My fiery POKéMON are all rough\\n\"\n\t.string \"and ready with intense heat!\\p\"\n\t.string \"They incinerate all challengers!\\p\"\n\t.string \"Hah!\\n\"\n\t.string \"You better have BURN HEAL!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "CinnabarIsland_Gym_Text_BlaineIntro::\n\t.string \"Ха!\\p\"\n\t.string \"Я БЛЕЙН, огненный ЛИДЕР\\n\"\n\t.string \"ГИМА ОСТРОВА СИННАБАР!\\p\"\n\t.string \"Мои огненные ПОКЕМОНЫ суровы\\n\"\n\t.string \"и пылают жаром!\\p\"\n\t.string \"Они испепеляют всех соперников!\\p\"\n\t.string \"Ха!\\n\"\n\t.string \"Надеюсь, у тебя есть BURN HEAL!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "CinnabarIsland_Gym_Text_BlaineDefeat": (
        "CinnabarIsland_Gym_Text_BlaineDefeat::\n\t.string \"I have burned down to nothing!\\n\"\n\t.string \"Not even ashes remain!\\p\"\n\t.string \"You have earned the VOLCANOBADGE.$\"\n",
        "CinnabarIsland_Gym_Text_BlaineDefeat::\n\t.string \"Я сгорел дотла!\\n\"\n\t.string \"Даже пепла не осталось!\\p\"\n\t.string \"Ты заслужил ВУЛКАНИЧЕСКИЙ ЗНАЧОК.$\"\n",
    ),
    "CinnabarIsland_Gym_Text_FireBlastIsUltimateFireMove": (
        "CinnabarIsland_Gym_Text_FireBlastIsUltimateFireMove::\n\t.string \"FIRE BLAST is the ultimate fire\\n\"\n\t.string \"technique.\\p\"\n\t.string \"Don't waste it on WATER POKéMON.$\"\n",
        "CinnabarIsland_Gym_Text_FireBlastIsUltimateFireMove::\n\t.string \"FIRE BLAST - мощнейшая огненная\\n\"\n\t.string \"техника.\\p\"\n\t.string \"Не трать её на WATER ПОКЕМОНОВ.$\"\n",
    ),
    "CinnabarIsland_Gym_Text_ExplainVolcanoBadge": (
        "CinnabarIsland_Gym_Text_ExplainVolcanoBadge::\n\t.string \"Hah!\\p\"\n\t.string \"The VOLCANOBADGE heightens the\\n\"\n\t.string \"SPECIAL stats of your POKéMON.\\p\"\n\t.string \"Here, you can have this, too!$\"\n",
        "CinnabarIsland_Gym_Text_ExplainVolcanoBadge::\n\t.string \"Ха!\\p\"\n\t.string \"ВУЛКАНИЧЕСКИЙ ЗНАЧОК повышает\\n\"\n\t.string \"SPECIAL параметры твоих ПОКЕМОНОВ.\\p\"\n\t.string \"Вот, возьми ещё и это!$\"\n",
    ),
    "CinnabarIsland_Gym_Text_ReceivedTM38FromBlaine": (
        "CinnabarIsland_Gym_Text_ReceivedTM38FromBlaine::\n\t.string \"{PLAYER} received TM38\\n\"\n\t.string \"from BLAINE.$\"\n",
        "CinnabarIsland_Gym_Text_ReceivedTM38FromBlaine::\n\t.string \"{PLAYER} получил TM38\\n\"\n\t.string \"от БЛЕЙНА.$\"\n",
    ),
    "CinnabarIsland_Gym_Text_BlainePostBattle": (
        "CinnabarIsland_Gym_Text_BlainePostBattle::\n\t.string \"TM38 contains FIRE BLAST.\\n\"\n\t.string \"Teach it to FIRE-type POKéMON.\\p\"\n\t.string \"VULPIX or CHARMELEON would be\\n\"\n\t.string \"ideal for that move.$\"\n",
        "CinnabarIsland_Gym_Text_BlainePostBattle::\n\t.string \"TM38 содержит FIRE BLAST.\\n\"\n\t.string \"Научи ей FIRE-type ПОКЕМОНА.\\p\"\n\t.string \"VULPIX или CHARMELEON отлично\\n\"\n\t.string \"подойдут для этой атаки.$\"\n",
    ),
    "CinnabarIsland_Gym_Text_MakeSpaceForThis": (
        "CinnabarIsland_Gym_Text_MakeSpaceForThis::\n\t.string \"Make space for this, child!$\"\n",
        "CinnabarIsland_Gym_Text_MakeSpaceForThis::\n\t.string \"Освободи для этого место!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_cinnabar_blaine_v3_35.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_cinnabar_blaine_v3_35_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Blaine runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
