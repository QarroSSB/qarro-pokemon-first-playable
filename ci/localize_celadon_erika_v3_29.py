#!/usr/bin/env python3
"""Qarro v3.29 mandatory Celadon Gym / Erika Russian runtime localization.

Translates only the verified pinned Erika progression chain: intro, defeat,
Rainbow Badge explanation, TM19 receipt/explanation, no-bag-space line, and
post-battle dialogue. Pokemon species / move / ability proper names remain
English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_CELADON_ERIKA_V3_29"
REL = Path("data/maps/CeladonCity_Gym_Frlg/scripts.inc")

PATCHES = {
    "CeladonCity_Gym_Text_ErikaIntro": (
        "CeladonCity_Gym_Text_ErikaIntro::\n"
        "\t.string \"Hello…\\n\"\n"
        "\t.string \"Lovely weather, isn't it?\\l\"\n"
        "\t.string \"It's so pleasant…\\p\"\n"
        "\t.string \"…Oh, dear…\\n\"\n"
        "\t.string \"I must have dozed off. Welcome.\\p\"\n"
        "\t.string \"My name is ERIKA.\\n\"\n"
        "\t.string \"I am the LEADER of CELADON GYM.\\p\"\n"
        "\t.string \"I am a student of the art of\\n\"\n"
        "\t.string \"flower arranging.\\p\"\n"
        "\t.string \"My POKéMON are solely of the\\n\"\n"
        "\t.string \"GRASS type.\\p\"\n"
        "\t.string \"…Oh, I'm sorry, I had no idea that\\n\"\n"
        "\t.string \"you wished to challenge me.\\p\"\n"
        "\t.string \"Very well, but I shall not lose.{PLAY_BGM MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "CeladonCity_Gym_Text_ErikaIntro::\n"
        "\t.string \"Здравствуйте…\\n\"\n"
        "\t.string \"Какая чудесная погода, правда?\\l\"\n"
        "\t.string \"Так приятно…\\p\"\n"
        "\t.string \"…Ох, простите…\\n\"\n"
        "\t.string \"Кажется, я задремала. Добро пожаловать.\\p\"\n"
        "\t.string \"Меня зовут ЭРИКА.\\n\"\n"
        "\t.string \"Я ЛИДЕР СТАДИОНА СЕЛАДОНА.\\p\"\n"
        "\t.string \"Я изучаю искусство\\n\"\n"
        "\t.string \"составления цветов.\\p\"\n"
        "\t.string \"Мои ПОКЕМОНЫ только\\n\"\n"
        "\t.string \"ТРАВЯНОГО типа.\\p\"\n"
        "\t.string \"…Ох, простите, я не знала, что\\n\"\n"
        "\t.string \"вы хотите бросить мне вызов.\\p\"\n"
        "\t.string \"Хорошо. Но я не проиграю.{PLAY_BGM MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "CeladonCity_Gym_Text_ErikaDefeat": (
        "CeladonCity_Gym_Text_ErikaDefeat::\n"
        "\t.string \"Oh!\\n\"\n"
        "\t.string \"I concede defeat.\\l\"\n"
        "\t.string \"You are remarkably strong.\\p\"\n"
        "\t.string \"I must confer on you the\\n\"\n"
        "\t.string \"RAINBOWBADGE.$\"\n",
        "CeladonCity_Gym_Text_ErikaDefeat::\n"
        "\t.string \"Ох!\\n\"\n"
        "\t.string \"Я признаю поражение.\\l\"\n"
        "\t.string \"Вы удивительно сильны.\\p\"\n"
        "\t.string \"Я должна вручить вам\\n\"\n"
        "\t.string \"РАДУЖНЫЙ ЗНАЧОК.$\"\n",
    ),
    "CeladonCity_Gym_Text_ExplainRainbowBadgeTakeThis": (
        "CeladonCity_Gym_Text_ExplainRainbowBadgeTakeThis::\n"
        "\t.string \"The RAINBOWBADGE will make\\n\"\n"
        "\t.string \"POKéMON up to Lv. 50 obey.\\p\"\n"
        "\t.string \"It also allows POKéMON to use\\n\"\n"
        "\t.string \"STRENGTH in and out of battle.\\p\"\n"
        "\t.string \"Please also take this with you.$\"\n",
        "CeladonCity_Gym_Text_ExplainRainbowBadgeTakeThis::\n"
        "\t.string \"РАДУЖНЫЙ ЗНАЧОК заставит\\n\"\n"
        "\t.string \"ПОКЕМОНОВ до 50 ур. слушаться.\\p\"\n"
        "\t.string \"Он также позволяет использовать\\n\"\n"
        "\t.string \"STRENGTH в бою и вне его.\\p\"\n"
        "\t.string \"И ещё возьмите это.$\"\n",
    ),
    "CeladonCity_Gym_Text_ReceivedTM19FromErika": (
        "CeladonCity_Gym_Text_ReceivedTM19FromErika::\n"
        "\t.string \"{PLAYER} received TM19\\n\"\n"
        "\t.string \"from ERIKA.$\"\n",
        "CeladonCity_Gym_Text_ReceivedTM19FromErika::\n"
        "\t.string \"{PLAYER} получил TM19\\n\"\n"
        "\t.string \"от ЭРИКИ.$\"\n",
    ),
    "CeladonCity_Gym_Text_ExplainTM19": (
        "CeladonCity_Gym_Text_ExplainTM19::\n"
        "\t.string \"TM19 contains GIGA DRAIN.\\p\"\n"
        "\t.string \"Half the damage it inflicts is\\n\"\n"
        "\t.string \"drained to heal your POKéMON.\\p\"\n"
        "\t.string \"Wouldn't you agree that it's a\\n\"\n"
        "\t.string \"wonderful move?$\"\n",
        "CeladonCity_Gym_Text_ExplainTM19::\n"
        "\t.string \"TM19 содержит GIGA DRAIN.\\p\"\n"
        "\t.string \"Половина нанесённого урона\\n\"\n"
        "\t.string \"восстанавливает здоровье ПОКЕМОНА.\\p\"\n"
        "\t.string \"Разве это не замечательная\\n\"\n"
        "\t.string \"атака?$\"\n",
    ),
    "CeladonCity_Gym_Text_ShouldMakeRoomForThis": (
        "CeladonCity_Gym_Text_ShouldMakeRoomForThis::\n"
        "\t.string \"You should make room for this.$\"\n",
        "CeladonCity_Gym_Text_ShouldMakeRoomForThis::\n"
        "\t.string \"Освободите для этого место.$\"\n",
    ),
    "CeladonCity_Gym_Text_ErikaPostBattle": (
        "CeladonCity_Gym_Text_ErikaPostBattle::\n"
        "\t.string \"You are cataloging POKéMON?\\n\"\n"
        "\t.string \"I must say I'm impressed.\\p\"\n"
        "\t.string \"I would never collect POKéMON if\\n\"\n"
        "\t.string \"they were unattractive.$\"\n",
        "CeladonCity_Gym_Text_ErikaPostBattle::\n"
        "\t.string \"Вы составляете каталог ПОКЕМОНОВ?\\n\"\n"
        "\t.string \"Должна сказать, я впечатлена.\\p\"\n"
        "\t.string \"Я бы не стала собирать ПОКЕМОНОВ,\\n\"\n"
        "\t.string \"если бы они были непривлекательны.$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_celadon_erika_v3_29.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_celadon_erika_v3_29_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Erika runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
