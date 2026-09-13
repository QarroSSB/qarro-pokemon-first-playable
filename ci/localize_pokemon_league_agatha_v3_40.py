#!/usr/bin/env python3
"""Qarro v3.40 mandatory Pokemon League / Agatha Russian runtime localization.

Translates only the verified pinned first-clear Agatha progression chain:
intro, defeat, and post-battle dialogue. Rematch intro is intentionally left
untouched. Pokemon species / move / ability proper names remain English.
Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEMON_LEAGUE_AGATHA_V3_40"
REL = Path("data/maps/PokemonLeague_AgathasRoom_Frlg/scripts.inc")

PATCHES = {
    "PokemonLeague_AgathasRoom_Text_Intro": (
        "PokemonLeague_AgathasRoom_Text_Intro::\n"
        "\t.string \"I am AGATHA of the ELITE FOUR.\\p\"\n"
        "\t.string \"I hear OAK's taken a lot of\\n\"\n"
        "\t.string \"interest in you, child.\\p\"\n"
        "\t.string \"That old duff was once tough and\\n\"\n"
        "\t.string \"handsome.\\p\"\n"
        "\t.string \"But that was decades ago.\\n\"\n"
        "\t.string \"He's a shadow of his former self.\\p\"\n"
        "\t.string \"Now he just wants to fiddle with\\n\"\n"
        "\t.string \"his POKéDEX.\\p\"\n"
        "\t.string \"He's wrong.\\n\"\n"
        "\t.string \"POKéMON are for battling!\\p\"\n"
        "\t.string \"{PLAYER}! I'll show you how a real\\n\"\n"
        "\t.string \"TRAINER battles!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "PokemonLeague_AgathasRoom_Text_Intro::\n"
        "\t.string \"Я AGATHA из ЭЛИТНОЙ ЧЕТВЁРКИ.\\p\"\n"
        "\t.string \"Слышала, OAK очень заинтересовался\\n\"\n"
        "\t.string \"тобой, дитя.\\p\"\n"
        "\t.string \"Когда-то этот старик был сильным\\n\"\n"
        "\t.string \"и статным.\\p\"\n"
        "\t.string \"Но это было десятки лет назад.\\n\"\n"
        "\t.string \"Теперь он лишь тень прежнего себя.\\p\"\n"
        "\t.string \"Сейчас ему нужен только его\\n\"\n"
        "\t.string \"POKEDEX.\\p\"\n"
        "\t.string \"Он ошибается.\\n\"\n"
        "\t.string \"ПОКЕМОНЫ созданы для битв!\\p\"\n"
        "\t.string \"{PLAYER}! Я покажу тебе, как\\n\"\n"
        "\t.string \"сражается настоящий ТРЕНЕР!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "PokemonLeague_AgathasRoom_Text_Defeat": (
        "PokemonLeague_AgathasRoom_Text_Defeat::\n"
        "\t.string \"Oh, my!\\n\"\n"
        "\t.string \"You're something special, child!$\"\n",
        "PokemonLeague_AgathasRoom_Text_Defeat::\n"
        "\t.string \"Вот это да!\\n\"\n"
        "\t.string \"Ты особенный ребёнок!$\"\n",
    ),
    "PokemonLeague_AgathasRoom_Text_PostBattle": (
        "PokemonLeague_AgathasRoom_Text_PostBattle::\n"
        "\t.string \"You win!\\p\"\n"
        "\t.string \"I see what the old duff sees in\\n\"\n"
        "\t.string \"you now.\\p\"\n"
        "\t.string \"I have nothing else to say.\\n\"\n"
        "\t.string \"Run along now, child!$\"\n",
        "PokemonLeague_AgathasRoom_Text_PostBattle::\n"
        "\t.string \"Ты победил!\\p\"\n"
        "\t.string \"Теперь я понимаю, что старик\\n\"\n"
        "\t.string \"увидел в тебе.\\p\"\n"
        "\t.string \"Мне больше нечего сказать.\\n\"\n"
        "\t.string \"Иди дальше, дитя!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_league_agatha_v3_40.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_pokemon_league_agatha_v3_40_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory first-clear Agatha runtime blocks; rematch and Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
