#!/usr/bin/env python3
"""Qarro v3.34 mandatory Saffron Gym / Sabrina Russian runtime localization.

Translates only the verified pinned Sabrina progression chain: intro, defeat,
Marsh Badge explanation, TM04 receipt/explanation, no-bag-space line, and
post-battle dialogue. Pokemon species / move / ability proper names remain
English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_SAFFRON_SABRINA_V3_34"
REL = Path("data/maps/SaffronCity_Gym_Frlg/scripts.inc")

PATCHES = {
    "SaffronCity_Gym_Text_SabrinaIntro": (
        "SaffronCity_Gym_Text_SabrinaIntro::\n\t.string \"I had a vision of your arrival.\\p\"\n\t.string \"I have had psychic powers since\\n\"\n\t.string \"I was a child.\\p\"\n\t.string \"It started when a spoon I\\n\"\n\t.string \"carelessly tossed, bent.\\p\"\n\t.string \"I dislike battling, but if you wish,\\n\"\n\t.string \"I will show you my powers!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "SaffronCity_Gym_Text_SabrinaIntro::\n\t.string \"Я видела твоё прибытие.\\p\"\n\t.string \"Психические силы у меня с детства.\\p\"\n\t.string \"Всё началось, когда брошенная мной\\n\"\n\t.string \"ложка внезапно согнулась.\\p\"\n\t.string \"Я не люблю сражаться, но если хочешь,\\n\"\n\t.string \"покажу тебе свою силу!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "SaffronCity_Gym_Text_SabrinaDefeat": (
        "SaffronCity_Gym_Text_SabrinaDefeat::\n\t.string \"This loss shocks me!\\n\"\n\t.string \"But, a loss is a loss.\\p\"\n\t.string \"I admit, I didn't work hard enough\\n\"\n\t.string \"to win.\\p\"\n\t.string \"Your victory has earned you the\\n\"\n\t.string \"MARSHBADGE.$\"\n",
        "SaffronCity_Gym_Text_SabrinaDefeat::\n\t.string \"Это поражение потрясло меня!\\n\"\n\t.string \"Но поражение есть поражение.\\p\"\n\t.string \"Признаю: я старалась недостаточно,\\n\"\n\t.string \"чтобы победить.\\p\"\n\t.string \"За победу ты получаешь\\n\"\n\t.string \"БОЛОТНЫЙ ЗНАЧОК.$\"\n",
    ),
    "SaffronCity_Gym_Text_SabrinaPostBattle": (
        "SaffronCity_Gym_Text_SabrinaPostBattle::\n\t.string \"Psychic power isn't something that\\n\"\n\t.string \"only a few people have.\\p\"\n\t.string \"Everyone has psychic power.\\n\"\n\t.string \"People just don't realize it.$\"\n",
        "SaffronCity_Gym_Text_SabrinaPostBattle::\n\t.string \"Психическая сила есть не только\\n\"\n\t.string \"у избранных.\\p\"\n\t.string \"Она есть у каждого.\\n\"\n\t.string \"Просто люди этого не осознают.$\"\n",
    ),
    "SaffronCity_Gym_Text_ExplainMarshBadgeTakeThis": (
        "SaffronCity_Gym_Text_ExplainMarshBadgeTakeThis::\n\t.string \"The MARSHBADGE makes POKéMON up\\n\"\n\t.string \"to Lv. 70 obey you.\\p\"\n\t.string \"Stronger POKéMON will become wild,\\n\"\n\t.string \"ignoring your orders in battle.\\p\"\n\t.string \"Just don't raise your POKéMON too\\n\"\n\t.string \"much to avoid that problem.\\p\"\n\t.string \"Wait, please take this TM with you.$\"\n",
        "SaffronCity_Gym_Text_ExplainMarshBadgeTakeThis::\n\t.string \"С БОЛОТНЫМ ЗНАЧКОМ ПОКЕМОНЫ\\n\"\n\t.string \"до ур. 70 будут слушаться тебя.\\p\"\n\t.string \"Более сильные могут ослушаться\\n\"\n\t.string \"приказов в бою.\\p\"\n\t.string \"Не перекачивай ПОКЕМОНОВ,\\n\"\n\t.string \"и этой проблемы не будет.\\p\"\n\t.string \"Постой, возьми ещё эту TM.$\"\n",
    ),
    "SaffronCity_Gym_Text_ReceivedTM04FromSabrina": (
        "SaffronCity_Gym_Text_ReceivedTM04FromSabrina::\n\t.string \"{PLAYER} received TM04 from\\n\"\n\t.string \"SABRINA.$\"\n",
        "SaffronCity_Gym_Text_ReceivedTM04FromSabrina::\n\t.string \"{PLAYER} получил TM04 от\\n\"\n\t.string \"САБРИНЫ.$\"\n",
    ),
    "SaffronCity_Gym_Text_ExplainTM04": (
        "SaffronCity_Gym_Text_ExplainTM04::\n\t.string \"TM04 is CALM MIND.\\p\"\n\t.string \"It makes the POKéMON concentrate\\n\"\n\t.string \"to raise both SP. ATK and SP. DEF.$\"\n",
        "SaffronCity_Gym_Text_ExplainTM04::\n\t.string \"TM04 - это CALM MIND.\\p\"\n\t.string \"Он помогает ПОКЕМОНУ сосредоточиться,\\n\"\n\t.string \"повышая SP. ATK и SP. DEF.$\"\n",
    ),
    "SaffronCity_Gym_Text_BagFullOfOtherItems": (
        "SaffronCity_Gym_Text_BagFullOfOtherItems::\n\t.string \"Your BAG is full of other items.$\"\n",
        "SaffronCity_Gym_Text_BagFullOfOtherItems::\n\t.string \"В СУМКЕ нет свободного места.$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_saffron_sabrina_v3_34.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_saffron_sabrina_v3_34_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Sabrina runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
