#!/usr/bin/env python3
"""Qarro v3.41 mandatory Pokemon League / Lance Russian runtime localization.

Translates only the verified pinned first-clear Lance progression chain:
intro, defeat, and post-battle dialogue. Rematch intro is intentionally left
untouched. Pokemon species / move / ability proper names remain English.
Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEMON_LEAGUE_LANCE_V3_41"
REL = Path("data/maps/PokemonLeague_LancesRoom_Frlg/scripts.inc")

PATCHES = {
    "PokemonLeague_LancesRoom_Text_Intro": (
        "PokemonLeague_LancesRoom_Text_Intro::\n"
        "\t.string \"Ah! I've heard about you,\\n\"\n"
        "\t.string \"{PLAYER}!\\p\"\n"
        "\t.string \"I lead the ELITE FOUR.\\p\"\n"
        "\t.string \"You can call me LANCE the dragon\\n\"\n"
        "\t.string \"TRAINER.\\p\"\n"
        "\t.string \"You know that dragons are\\n\"\n"
        "\t.string \"mythical POKéMON.\\p\"\n"
        "\t.string \"They're hard to catch and raise,\\n\"\n"
        "\t.string \"but their powers are superior.\\p\"\n"
        "\t.string \"They're virtually indestructible.\\n\"\n"
        "\t.string \"There's no being clever with them.\\p\"\n"
        "\t.string \"Well, are you ready to lose?\\p\"\n"
        "\t.string \"Your LEAGUE challenge ends with\\n\"\n"
        "\t.string \"me, {PLAYER}!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "PokemonLeague_LancesRoom_Text_Intro::\n"
        "\t.string \"А! Я слышал о тебе,\\n\"\n"
        "\t.string \"{PLAYER}!\\p\"\n"
        "\t.string \"Я возглавляю ЭЛИТНУЮ ЧЕТВЁРКУ.\\p\"\n"
        "\t.string \"Зови меня LANCE, ТРЕНЕРОМ\\n\"\n"
        "\t.string \"драконов.\\p\"\n"
        "\t.string \"Ты знаешь, драконы -\\n\"\n"
        "\t.string \"мифические ПОКЕМОНЫ.\\p\"\n"
        "\t.string \"Их трудно поймать и вырастить,\\n\"\n"
        "\t.string \"но их сила огромна.\\p\"\n"
        "\t.string \"Они почти неуязвимы.\\n\"\n"
        "\t.string \"Хитростью их не одолеть.\\p\"\n"
        "\t.string \"Ну что, готов проиграть?\\p\"\n"
        "\t.string \"Твой путь в ЛИГЕ закончится\\n\"\n"
        "\t.string \"на мне, {PLAYER}!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "PokemonLeague_LancesRoom_Text_Defeat": (
        "PokemonLeague_LancesRoom_Text_Defeat::\n"
        "\t.string \"That's it!\\p\"\n"
        "\t.string \"I hate to admit it, but you are a\\n\"\n"
        "\t.string \"POKéMON master!$\"\n",
        "PokemonLeague_LancesRoom_Text_Defeat::\n"
        "\t.string \"Вот и всё!\\p\"\n"
        "\t.string \"Не хочу признавать, но ты\\n\"\n"
        "\t.string \"настоящий мастер ПОКЕМОНОВ!$\"\n",
    ),
    "PokemonLeague_LancesRoom_Text_PostBattle": (
        "PokemonLeague_LancesRoom_Text_PostBattle::\n"
        "\t.string \"I still can't believe my dragons\\n\"\n"
        "\t.string \"lost to you, {PLAYER}.\\p\"\n"
        "\t.string \"You are now the POKéMON LEAGUE\\n\"\n"
        "\t.string \"CHAMPION!\\p\"\n"
        "\t.string \"…Or, you would have been, but\\n\"\n"
        "\t.string \"you have one more challenge left.\\p\"\n"
        "\t.string \"There is one more TRAINER to face!\\n\"\n"
        "\t.string \"His name is…\\p\"\n"
        "\t.string \"{RIVAL}!\\p\"\n"
        "\t.string \"He beat the ELITE FOUR before\\n\"\n"
        "\t.string \"you.\\p\"\n"
        "\t.string \"He is the real POKéMON LEAGUE\\n\"\n"
        "\t.string \"CHAMPION.$\"\n",
        "PokemonLeague_LancesRoom_Text_PostBattle::\n"
        "\t.string \"Не верится, что мои драконы\\n\"\n"
        "\t.string \"проиграли тебе, {PLAYER}.\\p\"\n"
        "\t.string \"Теперь ты ЧЕМПИОН\\n\"\n"
        "\t.string \"ЛИГИ ПОКЕМОНОВ!\\p\"\n"
        "\t.string \"...Точнее, был бы им, но\\n\"\n"
        "\t.string \"осталось последнее испытание.\\p\"\n"
        "\t.string \"Тебя ждёт ещё один ТРЕНЕР!\\n\"\n"
        "\t.string \"Его имя...\\p\"\n"
        "\t.string \"{RIVAL}!\\p\"\n"
        "\t.string \"Он победил ЭЛИТНУЮ ЧЕТВЁРКУ\\n\"\n"
        "\t.string \"раньше тебя.\\p\"\n"
        "\t.string \"Именно он настоящий ЧЕМПИОН\\n\"\n"
        "\t.string \"ЛИГИ ПОКЕМОНОВ.$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_league_lance_v3_41.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_pokemon_league_lance_v3_41_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "rematchTouched": False,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory first-clear Lance runtime blocks; rematch and Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
