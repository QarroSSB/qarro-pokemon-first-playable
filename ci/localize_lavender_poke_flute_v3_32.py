#!/usr/bin/env python3
"""Qarro v3.32 mandatory Lavender Mr. Fuji / Poke Flute Russian runtime localization.

Translates only the verified pinned Mr. Fuji progression dialogue used to receive
and explain the Poke Flute after Pokemon Tower. Pokemon species / move / ability
proper names remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_LAVENDER_POKE_FLUTE_V3_32"
REL = Path("data/maps/LavenderTown_VolunteerPokemonHouse_Frlg/scripts.inc")

PATCHES = {
    "LavenderTown_VolunteerPokemonHouse_Text_IdLikeYouToHaveThis": (
        "LavenderTown_VolunteerPokemonHouse_Text_IdLikeYouToHaveThis::\n"
        "\t.string \"MR. FUJI: {PLAYER}…\\p\"\n"
        "\t.string \"Your POKéDEX quest is one that\\n\"\n"
        "\t.string \"requires strong dedication.\\p\"\n"
        "\t.string \"Without deep love for POKéMON,\\n\"\n"
        "\t.string \"your quest may fail.\\p\"\n"
        "\t.string \"I'm not sure if this will help you,\\n\"\n"
        "\t.string \"but I'd like you to have it.$\"\n",
        "LavenderTown_VolunteerPokemonHouse_Text_IdLikeYouToHaveThis::\n"
        "\t.string \"МР. ФУДЗИ: {PLAYER}…\\p\"\n"
        "\t.string \"Твой путь с POKéDEX требует\\n\"\n"
        "\t.string \"большой самоотдачи.\\p\"\n"
        "\t.string \"Без искренней любви к ПОКЕМОНОМ\\n\"\n"
        "\t.string \"твой путь может закончиться.\\p\"\n"
        "\t.string \"Не знаю, поможет ли это,\\n\"\n"
        "\t.string \"но я хочу отдать это тебе.$\"\n",
    ),
    "LavenderTown_VolunteerPokemonHouse_Text_ReceivedPokeFluteFromMrFuji": (
        "LavenderTown_VolunteerPokemonHouse_Text_ReceivedPokeFluteFromMrFuji::\n"
        "\t.string \"{PLAYER} received a POKé FLUTE\\n\"\n"
        "\t.string \"from MR. FUJI.$\"\n",
        "LavenderTown_VolunteerPokemonHouse_Text_ReceivedPokeFluteFromMrFuji::\n"
        "\t.string \"{PLAYER} получает POKé FLUTE\\n\"\n"
        "\t.string \"от МР. ФУДЗИ.$\"\n",
    ),
    "LavenderTown_VolunteerPokemonHouse_Text_ExplainPokeFlute": (
        "LavenderTown_VolunteerPokemonHouse_Text_ExplainPokeFlute::\n"
        "\t.string \"Upon hearing the POKé FLUTE,\\n\"\n"
        "\t.string \"sleeping POKéMON will spring awake.\\p\"\n"
        "\t.string \"Try using it on POKéMON that are\\n\"\n"
        "\t.string \"sleeping obstacles.$\"\n",
        "LavenderTown_VolunteerPokemonHouse_Text_ExplainPokeFlute::\n"
        "\t.string \"Услышав POKé FLUTE, спящие\\n\"\n"
        "\t.string \"ПОКЕМОНЫ сразу проснутся.\\p\"\n"
        "\t.string \"Попробуй её на ПОКЕМОНАХ,\\n\"\n"
        "\t.string \"которые преграждают путь во сне.$\"\n",
    ),
    "LavenderTown_VolunteerPokemonHouse_Text_MustMakeRoomForThis": (
        "LavenderTown_VolunteerPokemonHouse_Text_MustMakeRoomForThis::\n"
        "\t.string \"You must make room for this!$\"\n",
        "LavenderTown_VolunteerPokemonHouse_Text_MustMakeRoomForThis::\n"
        "\t.string \"Освободи место для этого!$\"\n",
    ),
    "LavenderTown_VolunteerPokemonHouse_Text_HasPokeFluteHelpedYou": (
        "LavenderTown_VolunteerPokemonHouse_Text_HasPokeFluteHelpedYou::\n"
        "\t.string \"MR. FUJI: Has my POKé FLUTE\\n\"\n"
        "\t.string \"helped you?$\"\n",
        "LavenderTown_VolunteerPokemonHouse_Text_HasPokeFluteHelpedYou::\n"
        "\t.string \"МР. ФУДЗИ: Моя POKé FLUTE\\n\"\n"
        "\t.string \"помогла тебе?$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_lavender_poke_flute_v3_32.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_lavender_poke_flute_v3_32_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Lavender Mr. Fuji / Poke Flute runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
