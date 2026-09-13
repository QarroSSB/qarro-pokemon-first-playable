#!/usr/bin/env python3
"""Qarro v3.47 mandatory Three Island biker confrontation Russian localization.

Translates only the verified pinned biker/anti-biker argument and Paxton arrival
scene that gates the next Three Island progression step toward Lostelle. The
subsequent battle sequence, rewards, optional NPC dialogue, and later Sevii
postgame text are intentionally untouched. Pokemon species / move / ability
proper names remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_THREE_ISLAND_BIKER_INTRO_V3_47"
REL = Path("data/maps/ThreeIsland_Frlg/scripts.inc")

PATCHES = {
    "ThreeIsland_Text_GoBackToKanto": (
        '''ThreeIsland_Text_GoBackToKanto::
\t.string "We don't need you people bringing\\n"
\t.string "your noise and trouble here!\\p"
\t.string "We're asking you to go back to\\n"
\t.string "KANTO!$"
''',
        '''ThreeIsland_Text_GoBackToKanto::
\t.string "Нам не нужны ваш шум и\\n"
\t.string "неприятности!\\p"
\t.string "Мы просим вас вернуться\\n"
\t.string "в KANTO!$"
''',
    ),
    "ThreeIsland_Text_BossIsOnHisWay": (
        '''ThreeIsland_Text_BossIsOnHisWay::
\t.string "Hey, go cry somewhere else.\\n"
\t.string "Our boss is on his way.\\p"
\t.string "When he gets here, we'll give you\\n"
\t.string "a k-rad motorbike show you won't\\l"
\t.string "soon forget!$"
''',
        '''ThreeIsland_Text_BossIsOnHisWay::
\t.string "Эй, иди плачь в другом месте.\\n"
\t.string "Наш босс уже едет.\\p"
\t.string "Когда он приедет, устроим вам\\n"
\t.string "такое байк-шоу, которое вы\\l"
\t.string "долго не забудете!$"
''',
    ),
    "ThreeIsland_Text_GetOffIslandNow": (
        '''ThreeIsland_Text_GetOffIslandNow::
\t.string "W-what!? Not on your life!\\n"
\t.string "Get off the island now!$"
''',
        '''ThreeIsland_Text_GetOffIslandNow::
\t.string "Ч-что!? Ещё чего!\\n"
\t.string "Убирайтесь с острова сейчас же!$"
''',
    ),
    "ThreeIsland_Text_WhosGonnaMakeMe": (
        '''ThreeIsland_Text_WhosGonnaMakeMe::
\t.string "Who's gonna make me?$"
''',
        '''ThreeIsland_Text_WhosGonnaMakeMe::
\t.string "И кто меня заставит?$"
''',
    ),
    "ThreeIsland_Text_AreYouBossGoBackToKanto": (
        '''ThreeIsland_Text_AreYouBossGoBackToKanto::
\t.string "Are you the boss?\\n"
\t.string "Go back to KANTO right now!$"
''',
        '''ThreeIsland_Text_AreYouBossGoBackToKanto::
\t.string "Ты их босс?\\n"
\t.string "Возвращайся в KANTO немедленно!$"
''',
    ),
    "ThreeIsland_Text_JustGotHerePal": (
        '''ThreeIsland_Text_JustGotHerePal::
\t.string "Hah?\\p"
\t.string "I just got here, pal.\\p"
\t.string "What's with the hostile attitude?\\n"
\t.string "It's mighty cold of you!$"
''',
        '''ThreeIsland_Text_JustGotHerePal::
\t.string "А?\\p"
\t.string "Я только приехал, приятель.\\p"
\t.string "Что за враждебный приём?\\n"
\t.string "Не слишком-то гостеприимно!$"
''',
    ),
    "ThreeIsland_Text_FollowersRaisingHavoc": (
        '''ThreeIsland_Text_FollowersRaisingHavoc::
\t.string "Your gang of followers have been\\n"
\t.string "raising havoc on their bikes.\\p"
\t.string "Do you have any idea how much\\n"
\t.string "trouble they've caused us on the\\l"
\t.string "island?$"
''',
        '''ThreeIsland_Text_FollowersRaisingHavoc::
\t.string "Твоя шайка носится на байках\\n"
\t.string "и устраивает беспорядки.\\p"
\t.string "Ты хоть представляешь, сколько\\n"
\t.string "неприятностей они устроили\\l"
\t.string "на острове?$"
''',
    ),
    "ThreeIsland_Text_OughtToBeThankingUs": (
        '''ThreeIsland_Text_OughtToBeThankingUs::
\t.string "No, man, I don't get it at all.\\p"
\t.string "Look at this place.\\n"
\t.string "What do you do for entertainment?\\p"
\t.string "You ought to be thanking us for\\n"
\t.string "livening up this sleepy village.\\p"
\t.string "But hey, if you insist, you can try\\n"
\t.string "making us leave.$"
''',
        '''ThreeIsland_Text_OughtToBeThankingUs::
\t.string "Нет, приятель, я вообще не понимаю.\\p"
\t.string "Посмотри на это место.\\n"
\t.string "Как вы тут развлекаетесь?\\p"
\t.string "Вы должны благодарить нас за то,\\n"
\t.string "что мы оживили эту сонную деревню.\\p"
\t.string "Но если настаиваешь, попробуй\\n"
\t.string "заставить нас уйти.$"
''',
    ),
    "ThreeIsland_Text_YouCowardsToughInPack": (
        '''ThreeIsland_Text_YouCowardsToughInPack::
\t.string "Grr… You cowards…\\n"
\t.string "So tough in a pack…$"
''',
        '''ThreeIsland_Text_YouCowardsToughInPack::
\t.string "Грр… Трусы…\\n"
\t.string "Смелые только толпой…$"
''',
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_three_island_biker_intro_v3_47.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_three_island_biker_intro_v3_47_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Three Island biker/anti-biker argument and Paxton arrival scene",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Three Island biker intro runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
