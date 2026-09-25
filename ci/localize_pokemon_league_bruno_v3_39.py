#!/usr/bin/env python3
"""Qarro v3.39 mandatory Pokemon League / Bruno Russian runtime localization.

Translates only the verified pinned first-clear Bruno progression chain:
intro, defeat, and post-battle dialogue. Rematch intro is intentionally left
untouched. Pokemon species / move / ability proper names remain English.
Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEMON_LEAGUE_BRUNO_V3_39"
REL = Path("data/maps/PokemonLeague_BrunosRoom_Frlg/scripts.inc")

PATCHES = {
    "PokemonLeague_BrunosRoom_Text_Intro": (
        "PokemonLeague_BrunosRoom_Text_Intro::\n"
        "\t.string \"I am BRUNO of the ELITE FOUR!\\p\"\n"
        "\t.string \"Through rigorous training, people\\n\"\n"
        "\t.string \"and POKéMON can become stronger\\l\"\n"
        "\t.string \"without limit.\\p\"\n"
        "\t.string \"I've lived and trained with my\\n\"\n"
        "\t.string \"fighting POKéMON!\\l\"\n"
        "\t.string \"And that will never change!\\p\"\n"
        "\t.string \"{PLAYER}!\\p\"\n"
        "\t.string \"We will grind you down with our\\n\"\n"
        "\t.string \"superior power!\\p\"\n"
        "\t.string \"Hoo hah!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "PokemonLeague_BrunosRoom_Text_Intro::\n"
        "\t.string \"Я BRUNO из ЭЛИТНОЙ ЧЕТВЁРКИ!\\p\"\n"
        "\t.string \"Упорные тренировки делают людей\\n\"\n"
        "\t.string \"и ПОКЕМОНОВ сильнее без предела.\\p\"\n"
        "\t.string \"Я жил и тренировался вместе\\n\"\n"
        "\t.string \"со своими боевыми ПОКЕМОНАМИ!\\p\"\n"
        "\t.string \"И это никогда не изменится!\\p\"\n"
        "\t.string \"{PLAYER}!\\p\"\n"
        "\t.string \"Мы сокрушим тебя нашей\\n\"\n"
        "\t.string \"превосходящей силой!\\p\"\n"
        "\t.string \"Ха!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "PokemonLeague_BrunosRoom_Text_Defeat": (
        "PokemonLeague_BrunosRoom_Text_Defeat::\n"
        "\t.string \"Why?\\n\"\n"
        "\t.string \"How could I lose?$\"\n",
        "PokemonLeague_BrunosRoom_Text_Defeat::\n"
        "\t.string \"Почему?\\n\"\n"
        "\t.string \"Как я мог проиграть?$\"\n",
    ),
    "PokemonLeague_BrunosRoom_Text_PostBattle": (
        "PokemonLeague_BrunosRoom_Text_PostBattle::\n"
        "\t.string \"My job is done.\\n\"\n"
        "\t.string \"Go face your next challenge.$\"\n",
        "PokemonLeague_BrunosRoom_Text_PostBattle::\n"
        "\t.string \"Моя работа закончена.\\n\"\n"
        "\t.string \"Иди к следующему испытанию.$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_league_bruno_v3_39.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_pokemon_league_bruno_v3_39_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory first-clear Bruno runtime blocks; rematch and Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
