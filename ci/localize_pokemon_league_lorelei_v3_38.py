#!/usr/bin/env python3
"""Qarro v3.38 mandatory Pokemon League / Lorelei Russian runtime localization.

Translates only the verified pinned first-clear Lorelei progression chain:
intro, defeat, and post-battle dialogue. Rematch text is intentionally left
untouched. Pokemon species / move / ability proper names remain English.
Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEMON_LEAGUE_LORELEI_V3_38"
REL = Path("data/maps/PokemonLeague_LoreleisRoom_Frlg/scripts.inc")

PATCHES = {
    "PokemonLeague_LoreleisRoom_Text_Intro": (
        "PokemonLeague_LoreleisRoom_Text_Intro::\n"
        "\t.string \"Welcome to the POKéMON LEAGUE.\\p\"\n"
        "\t.string \"I am LORELEI of the ELITE FOUR.\\p\"\n"
        "\t.string \"No one can best me when it comes\\n\"\n"
        "\t.string \"to icy POKéMON.\\p\"\n"
        "\t.string \"Freezing moves are powerful.\\p\"\n"
        "\t.string \"Your POKéMON will be at my mercy\\n\"\n"
        "\t.string \"when they are frozen solid.\\p\"\n"
        "\t.string \"Hahaha!\\n\"\n"
        "\t.string \"Are you ready?{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "PokemonLeague_LoreleisRoom_Text_Intro::\n"
        "\t.string \"Добро пожаловать в ЛИГУ ПОКЕМОНОВ.\\p\"\n"
        "\t.string \"Я LORELEI из ЭЛИТНОЙ ЧЕТВЁРКИ.\\p\"\n"
        "\t.string \"Никто не сравнится со мной\\n\"\n"
        "\t.string \"в битвах ледяных ПОКЕМОНОВ.\\p\"\n"
        "\t.string \"Замораживающие приёмы очень сильны.\\p\"\n"
        "\t.string \"Твои ПОКЕМОНЫ будут беспомощны,\\n\"\n"
        "\t.string \"когда замёрзнут насквозь.\\p\"\n"
        "\t.string \"Ха-ха-ха!\\n\"\n"
        "\t.string \"Ты готов?{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "PokemonLeague_LoreleisRoom_Text_Defeat": (
        "PokemonLeague_LoreleisRoom_Text_Defeat::\n"
        "\t.string \"…Things shouldn't be this way!$\"\n",
        "PokemonLeague_LoreleisRoom_Text_Defeat::\n"
        "\t.string \"Так не должно было случиться!$\"\n",
    ),
    "PokemonLeague_LoreleisRoom_Text_PostBattle": (
        "PokemonLeague_LoreleisRoom_Text_PostBattle::\n"
        "\t.string \"You're better than I thought.\\n\"\n"
        "\t.string \"Go on ahead.\\p\"\n"
        "\t.string \"You only got a taste of the\\n\"\n"
        "\t.string \"POKéMON LEAGUE's power.$\"\n",
        "PokemonLeague_LoreleisRoom_Text_PostBattle::\n"
        "\t.string \"Ты сильнее, чем я думала.\\n\"\n"
        "\t.string \"Иди дальше.\\p\"\n"
        "\t.string \"Ты увидел лишь малую часть силы\\n\"\n"
        "\t.string \"ЛИГИ ПОКЕМОНОВ.$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_league_lorelei_v3_38.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_pokemon_league_lorelei_v3_38_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory first-clear Lorelei runtime blocks; rematch and Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
