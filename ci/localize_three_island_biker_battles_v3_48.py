#!/usr/bin/env python3
"""Qarro v3.48 mandatory Three Island biker battle-chain Russian localization.

Translates only the verified pinned battle prompt plus Biker 1/2/3 and Paxton
intro/defeat/post-battle runtime text that gates Three Island progression.
Reward, Lostelle/Bond Bridge hint, optional NPC dialogue, and later Sevii
postgame text are intentionally untouched. Pokemon species / move / ability
proper names remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_THREE_ISLAND_BIKER_BATTLES_V3_48"
REL = Path("data/maps/ThreeIsland_Frlg/scripts.inc")

PATCHES = {
    "ThreeIsland_Text_WannaMakeSomethingOfYourStaring": (
        '''ThreeIsland_Text_WannaMakeSomethingOfYourStaring::
\t.string "You, what are you staring at?\\n"
\t.string "Don't you know it's not polite?\\p"
\t.string "You wanna make something of it\\n"
\t.string "or what?$"
''',
        '''ThreeIsland_Text_WannaMakeSomethingOfYourStaring::
\t.string "Эй, чего уставился?\\n"
\t.string "Не знаешь, что это невежливо?\\p"
\t.string "Хочешь со мной разобраться\\n"
\t.string "или как?$"
''',
    ),
    "ThreeIsland_Text_ThatsSmart": (
        '''ThreeIsland_Text_ThatsSmart::
\t.string "That's smart.\\n"
\t.string "Keep your nose out of this.$"
''',
        '''ThreeIsland_Text_ThatsSmart::
\t.string "Умное решение.\\n"
\t.string "Не суй нос не в своё дело.$"
''',
    ),
    "ThreeIsland_Text_Biker1Intro": (
        '''ThreeIsland_Text_Biker1Intro::
\t.string "Heh, I like your guts.\\n"
\t.string "You'll be losing money to me, but…$"
''',
        '''ThreeIsland_Text_Biker1Intro::
\t.string "Хех, мне нравится твоя смелость.\\n"
\t.string "Но деньги ты проиграешь мне…$"
''',
    ),
    "ThreeIsland_Text_Biker1Defeat": (
        '''ThreeIsland_Text_Biker1Defeat::
\t.string "Wha…\\n"
\t.string "What is this kid?!$"
''',
        '''ThreeIsland_Text_Biker1Defeat::
\t.string "Ч-что…\\n"
\t.string "Что это за ребёнок?!$"
''',
    ),
    "ThreeIsland_Text_Biker1PostBattle": (
        '''ThreeIsland_Text_Biker1PostBattle::
\t.string "Aww, man…\\n"
\t.string "Don't you dare laugh!$"
''',
        '''ThreeIsland_Text_Biker1PostBattle::
\t.string "Вот же…\\n"
\t.string "Только не смей смеяться!$"
''',
    ),
    "ThreeIsland_Text_Biker2Intro": (
        '''ThreeIsland_Text_Biker2Intro::
\t.string "Aren't you from KANTO?\\n"
\t.string "You should be on our side!$"
''',
        '''ThreeIsland_Text_Biker2Intro::
\t.string "Разве ты не из KANTO?\\n"
\t.string "Ты должен быть на нашей стороне!$"
''',
    ),
    "ThreeIsland_Text_Biker2Defeat": (
        '''ThreeIsland_Text_Biker2Defeat::
\t.string "Stop fooling around!$"
''',
        '''ThreeIsland_Text_Biker2Defeat::
\t.string "Хватит валять дурака!$"
''',
    ),
    "ThreeIsland_Text_Biker2PostBattle": (
        '''ThreeIsland_Text_Biker2PostBattle::
\t.string "What's the matter with you,\\n"
\t.string "getting all hot like that?\\p"
\t.string "Totally uncool, man!$"
''',
        '''ThreeIsland_Text_Biker2PostBattle::
\t.string "Что с тобой такое,\\n"
\t.string "чего ты так завёлся?\\p"
\t.string "Совсем не круто, приятель!$"
''',
    ),
    "ThreeIsland_Text_Biker3Intro": (
        '''ThreeIsland_Text_Biker3Intro::
\t.string "We invited the boss out here,\\n"
\t.string "but you had to mess it up!\\p"
\t.string "You embarrassed us, man!$"
''',
        '''ThreeIsland_Text_Biker3Intro::
\t.string "Мы позвали сюда босса,\\n"
\t.string "а ты всё испортил!\\p"
\t.string "Ты нас опозорил, приятель!$"
''',
    ),
    "ThreeIsland_Text_Biker3Defeat": (
        '''ThreeIsland_Text_Biker3Defeat::
\t.string "… … …   … … …$"
''',
        '''ThreeIsland_Text_Biker3Defeat::
\t.string "… … …   … … …$"
''',
    ),
    "ThreeIsland_Text_Biker3PostBattle": (
        '''ThreeIsland_Text_Biker3PostBattle::
\t.string "Boss, I'm telling you, you've gotta\\n"
\t.string "do something about this kid!$"
''',
        '''ThreeIsland_Text_Biker3PostBattle::
\t.string "Босс, говорю тебе, надо что-то\\n"
\t.string "сделать с этим ребёнком!$"
''',
    ),
    "ThreeIsland_Text_PaxtonIntro": (
        '''ThreeIsland_Text_PaxtonIntro::
\t.string "I've been watching you, and I'd say\\n"
\t.string "you've done enough.\\p"
\t.string "What are you, their friend or\\n"
\t.string "something?\\p"
\t.string "Then I guess you'll be battling me\\n"
\t.string "in their place.$"
''',
        '''ThreeIsland_Text_PaxtonIntro::
\t.string "Я наблюдал за тобой, и, по-моему,\\n"
\t.string "ты уже достаточно натворил.\\p"
\t.string "Ты что, их друг или\\n"
\t.string "кто-то вроде того?\\p"
\t.string "Тогда, похоже, вместо них\\n"
\t.string "сразишься со мной.$"
''',
    ),
    "ThreeIsland_Text_PaxtonDefeat": (
        '''ThreeIsland_Text_PaxtonDefeat::
\t.string "All right, enough!\\n"
\t.string "We'll leave like you wanted!\\p"
\t.string "We'll be happy to see the last of\\n"
\t.string "this boring island!$"
''',
        '''ThreeIsland_Text_PaxtonDefeat::
\t.string "Ладно, хватит!\\n"
\t.string "Мы уйдём, как ты и хотел!\\p"
\t.string "Будем рады больше не видеть\\n"
\t.string "этот скучный остров!$"
''',
    ),
    "ThreeIsland_Text_PaxtonPostBattle": (
        '''ThreeIsland_Text_PaxtonPostBattle::
\t.string "Humph! Yeah, go right on hanging\\n"
\t.string "around with these hayseeds!$"
''',
        '''ThreeIsland_Text_PaxtonPostBattle::
\t.string "Хмф! Ну и оставайся тут\\n"
\t.string "с этими деревенщинами!$"
''',
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_three_island_biker_battles_v3_48.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_three_island_biker_battles_v3_48_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Three Island Biker 1/2/3 and Paxton battle chain",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Three Island biker battle runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
