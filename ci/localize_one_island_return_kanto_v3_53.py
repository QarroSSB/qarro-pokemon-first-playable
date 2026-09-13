#!/usr/bin/env python3
"""Qarro v3.53 mandatory One Island return-to-Kanto localization.

Translates only the verified forced LeaveOneIslandScene that fires after the
Meteorite handoff sets One Island Pokemon Center scene 2: Bill/Celio wrap up
their work and return the player to Kanto. Optional NPC dialogue and later
Ruby/Sapphire postgame remain untouched. Pokemon species / move / ability
proper names remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_ONE_ISLAND_RETURN_KANTO_V3_53"
REL = Path("data/maps/OneIsland_PokemonCenter_1F_Frlg/scripts.inc")

PATCHES = {
    "OneIsland_PokemonCenter_1F_Text_BillOhHeyPlayer": (
        '''OneIsland_PokemonCenter_1F_Text_BillOhHeyPlayer::
\t.string "BILL: Oh, hey!\\n"
\t.string "{PLAYER}!$"
''',
        '''OneIsland_PokemonCenter_1F_Text_BillOhHeyPlayer::
\t.string "BILL: О, привет!\\n"
\t.string "{PLAYER}!$"
''',
    ),
    "OneIsland_PokemonCenter_1F_Text_BillWeGotItDone": (
        '''OneIsland_PokemonCenter_1F_Text_BillWeGotItDone::
\t.string "BILL: What kept you so long?\\n"
\t.string "Been out having a good time?\\p"
\t.string "We got it done.\\n"
\t.string "The PCs are up and running!$"
''',
        '''OneIsland_PokemonCenter_1F_Text_BillWeGotItDone::
\t.string "BILL: Что так долго?\\n"
\t.string "Хорошо погулял?\\p"
\t.string "Мы всё закончили.\\n"
\t.string "PC снова работают!$"
''',
    ),
    "OneIsland_PokemonCenter_1F_Text_CelioJobWentQuick": (
        '''OneIsland_PokemonCenter_1F_Text_CelioJobWentQuick::
\t.string "CELIO: The job went incredibly\\n"
\t.string "quick.\\p"
\t.string "BILL is one amazing guy…$"
''',
        '''OneIsland_PokemonCenter_1F_Text_CelioJobWentQuick::
\t.string "CELIO: Работа пошла невероятно\\n"
\t.string "быстро.\\p"
\t.string "BILL просто потрясающий…$"
''',
    ),
    "OneIsland_PokemonCenter_1F_Text_BillYouveLearnedALot": (
        '''OneIsland_PokemonCenter_1F_Text_BillYouveLearnedALot::
\t.string "BILL: No, no! There was almost\\n"
\t.string "nothing left for me to do.\\p"
\t.string "CELIO, I have to hand it to you.\\n"
\t.string "You've learned a lot.$"
''',
        '''OneIsland_PokemonCenter_1F_Text_BillYouveLearnedALot::
\t.string "BILL: Нет-нет! Мне почти\\n"
\t.string "нечего было делать.\\p"
\t.string "CELIO, должен признать.\\n"
\t.string "Ты многому научился.$"
''',
    ),
    "OneIsland_PokemonCenter_1F_Text_CelioOhReallyEhehe": (
        '''OneIsland_PokemonCenter_1F_Text_CelioOhReallyEhehe::
\t.string "CELIO: Oh, really?\\n"
\t.string "Ehehe…$"
''',
        '''OneIsland_PokemonCenter_1F_Text_CelioOhReallyEhehe::
\t.string "CELIO: Правда?\\n"
\t.string "Хе-хе…$"
''',
    ),
    "OneIsland_PokemonCenter_1F_Text_BillWeShouldHeadBackToKanto": (
        '''OneIsland_PokemonCenter_1F_Text_BillWeShouldHeadBackToKanto::
\t.string "BILL: Well, there you have it.\\n"
\t.string "I'm finished with the job.\\l"
\t.string "We should head back to KANTO.\\p"
\t.string "CELIO, I'll be seeing you again.$"
''',
        '''OneIsland_PokemonCenter_1F_Text_BillWeShouldHeadBackToKanto::
\t.string "BILL: Ну вот и всё.\\n"
\t.string "Я закончил работу.\\l"
\t.string "Нам пора обратно в KANTO.\\p"
\t.string "CELIO, ещё увидимся.$"
''',
    ),
    "OneIsland_PokemonCenter_1F_Text_CelioPromiseIllShowYouAroundSometime": (
        '''OneIsland_PokemonCenter_1F_Text_CelioPromiseIllShowYouAroundSometime::
\t.string "CELIO: {PLAYER}, I'm really sorry\\n"
\t.string "that we sent you off alone today.\\p"
\t.string "I promise, I will show you around\\n"
\t.string "these islands sometime.$"
''',
        '''OneIsland_PokemonCenter_1F_Text_CelioPromiseIllShowYouAroundSometime::
\t.string "CELIO: {PLAYER}, прости, что сегодня\\n"
\t.string "мы отправили тебя одного.\\p"
\t.string "Обещаю, как-нибудь я покажу тебе\\n"
\t.string "эти острова.$"
''',
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_one_island_return_kanto_v3_53.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_one_island_return_kanto_v3_53_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory forced One Island Bill/Celio wrap-up and return-to-Kanto scene",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} One Island return-to-Kanto blocks; Ash Bond/Ash Cap untouched")

    next_script = Path(__file__).with_name("localize_pallet_oak_rating_v3_54.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
