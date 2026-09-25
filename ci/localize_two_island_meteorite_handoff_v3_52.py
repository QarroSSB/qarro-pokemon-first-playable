#!/usr/bin/env python3
"""Qarro v3.52 mandatory Two Island Meteorite handoff localization.

Translates only the verified progression interaction with Lostelle's father after
her rescue: giving him Bill's Meteorite, his response, the Moon Stone reward,
and the reachable no-bag-space branch. Optional Game Corner/NPC dialogue and
later Sevii postgame remain untouched. Pokemon species / move / ability proper
names remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_TWO_ISLAND_METEORITE_HANDOFF_V3_52"
REL = Path("data/maps/TwoIsland_JoyfulGameCorner_Frlg/scripts.inc")

PATCHES = {
    "TwoIsland_JoyfulGameCorner_Text_ThisIsForMe": (
        '''TwoIsland_JoyfulGameCorner_Text_ThisIsForMe::
\t.string "Oh, what's that?\\n"
\t.string "You're saying that this is for me?\\p"
\t.string "How did you know that I love rare\\n"
\t.string "rocks and gems?\\p"
\t.string "You sure know how to make a guy\\n"
\t.string "happy.$"
''',
        '''TwoIsland_JoyfulGameCorner_Text_ThisIsForMe::
\t.string "О, что это?\\n"
\t.string "Говоришь, это для меня?\\p"
\t.string "Откуда ты знаешь, что я люблю\\n"
\t.string "редкие камни и самоцветы?\\p"
\t.string "Ты точно знаешь, как поднять\\n"
\t.string "человеку настроение.$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_HandedMeteoriteToLostellesDaddy": (
        '''TwoIsland_JoyfulGameCorner_Text_HandedMeteoriteToLostellesDaddy::
\t.string "{PLAYER} handed the METEORITE\\n"
\t.string "to LOSTELLE's daddy.$"
''',
        '''TwoIsland_JoyfulGameCorner_Text_HandedMeteoriteToLostellesDaddy::
\t.string "{PLAYER} передал МЕТЕОРИТ\\n"
\t.string "папе LOSTELLE.$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_OhThisIsFromBill": (
        '''TwoIsland_JoyfulGameCorner_Text_OhThisIsFromBill::
\t.string "Oh, I see, this is from BILL!\\n"
\t.string "You have to thank him for me!\\p"
\t.string "You know, you've been fantastic.\\n"
\t.string "I want you to have this.$"
''',
        '''TwoIsland_JoyfulGameCorner_Text_OhThisIsFromBill::
\t.string "А, понятно, это от BILL!\\n"
\t.string "Обязательно поблагодари его!\\p"
\t.string "Ты очень мне помог.\\n"
\t.string "Хочу отдать тебе вот это.$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_ReceivedMoonStoneFromLostellesDaddy": (
        '''TwoIsland_JoyfulGameCorner_Text_ReceivedMoonStoneFromLostellesDaddy::
\t.string "{PLAYER} received a MOON STONE\\n"
\t.string "from LOSTELLE's daddy.$"
''',
        '''TwoIsland_JoyfulGameCorner_Text_ReceivedMoonStoneFromLostellesDaddy::
\t.string "{PLAYER} получил ЛУННЫЙ КАМЕНЬ\\n"
\t.string "от папы LOSTELLE.$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_NotGoingToFitInBag": (
        '''TwoIsland_JoyfulGameCorner_Text_NotGoingToFitInBag::
\t.string "Your BAG's not going to fit another\\n"
\t.string "thing…$"
''',
        '''TwoIsland_JoyfulGameCorner_Text_NotGoingToFitInBag::
\t.string "В твоей СУМКЕ больше нет\\n"
\t.string "свободного места…$"
''',
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_two_island_meteorite_handoff_v3_52.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_two_island_meteorite_handoff_v3_52_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Two Island Meteorite handoff, Moon Stone reward, and reachable full-bag branch",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Two Island Meteorite handoff blocks; Ash Bond/Ash Cap untouched")

    return_script = Path(__file__).with_name("localize_one_island_return_kanto_v3_53.py")
    subprocess.run([sys.executable, str(return_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
