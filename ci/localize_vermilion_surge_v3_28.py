#!/usr/bin/env python3
"""Qarro v3.28 mandatory Vermilion Gym / Lt. Surge Russian runtime localization.

Translates only the verified pinned Lt. Surge progression chain: intro, defeat,
Thunder Badge explanation, TM34 receipt/explanation, no-bag-space line, and the
post-battle advice. Pokemon species / move / ability proper names remain
English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_VERMILION_SURGE_V3_28"
REL = Path("data/maps/VermilionCity_Gym_Frlg/scripts.inc")

PATCHES = {
    "VermilionCity_Gym_Text_LtSurgeIntro": (
        "VermilionCity_Gym_Text_LtSurgeIntro::\n"
        "\t.string \"Hey, kid! What do you think you're\\n\"\n"
        "\t.string \"doing here?\\p\"\n"
        "\t.string \"You won't live long in combat!\\n\"\n"
        "\t.string \"Not with your puny power!\\p\"\n"
        "\t.string \"I tell you, kid, electric POKéMON\\n\"\n"
        "\t.string \"saved me during the war!\\p\"\n"
        "\t.string \"They zapped my enemies into\\n\"\n"
        "\t.string \"paralysis!\\p\"\n"
        "\t.string \"The same as I'll do to you!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "VermilionCity_Gym_Text_LtSurgeIntro::\n"
        "\t.string \"Эй, малыш! Ты что здесь\\n\"\n"
        "\t.string \"забыл?\\p\"\n"
        "\t.string \"В настоящем бою ты бы долго\\n\"\n"
        "\t.string \"не протянул с такой силой!\\p\"\n"
        "\t.string \"Электрические ПОКЕМОНЫ спасли\\n\"\n"
        "\t.string \"меня во время войны!\\p\"\n"
        "\t.string \"Они парализовали моих врагов!\\p\"\n"
        "\t.string \"То же самое я сделаю с тобой!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "VermilionCity_Gym_Text_LtSurgeDefeat": (
        "VermilionCity_Gym_Text_LtSurgeDefeat::\n"
        "\t.string \"Now that's a shocker!\\p\"\n"
        "\t.string \"You're the real deal, kid!\\p\"\n"
        "\t.string \"Fine, then, take the THUNDERBADGE!$\"\n",
        "VermilionCity_Gym_Text_LtSurgeDefeat::\n"
        "\t.string \"Вот это удар током!\\p\"\n"
        "\t.string \"Ты настоящий боец, малыш!\\p\"\n"
        "\t.string \"Ладно, бери ГРОМОВОЙ ЗНАЧОК!$\"\n",
    ),
    "VermilionCity_Gym_Text_ExplainThunderBadgeTakeThis": (
        "VermilionCity_Gym_Text_ExplainThunderBadgeTakeThis::\n"
        "\t.string \"The THUNDERBADGE cranks up your\\n\"\n"
        "\t.string \"POKéMON's SPEED!\\p\"\n"
        "\t.string \"It also lets your POKéMON FLY\\n\"\n"
        "\t.string \"lightning-quick anytime, kid!\\p\"\n"
        "\t.string \"You're special, kid!\\n\"\n"
        "\t.string \"Take this!$\"\n",
        "VermilionCity_Gym_Text_ExplainThunderBadgeTakeThis::\n"
        "\t.string \"ГРОМОВОЙ ЗНАЧОК повышает SPEED\\n\"\n"
        "\t.string \"твоих ПОКЕМОНОВ!\\p\"\n"
        "\t.string \"А ещё позволяет использовать FLY\\n\"\n"
        "\t.string \"вне боя, малыш!\\p\"\n"
        "\t.string \"Ты особенный, малыш!\\n\"\n"
        "\t.string \"Возьми это!$\"\n",
    ),
    "VermilionCity_Gym_Text_ReceivedTM34FromLtSurge": (
        "VermilionCity_Gym_Text_ReceivedTM34FromLtSurge::\n"
        "\t.string \"{PLAYER} received TM34\\n\"\n"
        "\t.string \"from LT. SURGE.$\"\n",
        "VermilionCity_Gym_Text_ReceivedTM34FromLtSurge::\n"
        "\t.string \"{PLAYER} получил TM34\\n\"\n"
        "\t.string \"от ЛТ. СЕРЖА.$\"\n",
    ),
    "VermilionCity_Gym_Text_ExplainTM34": (
        "VermilionCity_Gym_Text_ExplainTM34::\n"
        "\t.string \"TM34 contains SHOCK WAVE!\\p\"\n"
        "\t.string \"Teach it to an ELECTRIC POKéMON!$\"\n",
        "VermilionCity_Gym_Text_ExplainTM34::\n"
        "\t.string \"TM34 содержит SHOCK WAVE!\\p\"\n"
        "\t.string \"Обучи ей ЭЛЕКТРИЧЕСКОГО ПОКЕМОНА!$\"\n",
    ),
    "VermilionCity_Gym_Text_MakeRoomInYourBag": (
        "VermilionCity_Gym_Text_MakeRoomInYourBag::\n"
        "\t.string \"Yo, kid, make room in your BAG!$\"\n",
        "VermilionCity_Gym_Text_MakeRoomInYourBag::\n"
        "\t.string \"Эй, малыш, освободи место в СУМКЕ!$\"\n",
    ),
    "VermilionCity_Gym_Text_LtSurgePostBattle": (
        "VermilionCity_Gym_Text_LtSurgePostBattle::\n"
        "\t.string \"A little word of advice, kid!\\p\"\n"
        "\t.string \"Electricity is sure powerful!\\p\"\n"
        "\t.string \"But, it's useless against GROUND-\\n\"\n"
        "\t.string \"type POKéMON!$\"\n",
        "VermilionCity_Gym_Text_LtSurgePostBattle::\n"
        "\t.string \"Небольшой совет, малыш!\\p\"\n"
        "\t.string \"Электричество очень мощное!\\p\"\n"
        "\t.string \"Но против ЗЕМЛЯНЫХ ПОКЕМОНОВ\\n\"\n"
        "\t.string \"оно бесполезно!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_vermilion_surge_v3_28.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_vermilion_surge_v3_28_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Lt. Surge runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
