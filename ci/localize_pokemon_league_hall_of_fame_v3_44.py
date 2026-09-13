#!/usr/bin/env python3
"""Qarro v3.44 mandatory Hall of Fame Russian runtime localization.

Translates only the verified pinned Professor Oak Hall of Fame speech reached
immediately after the first Champion clear. Pokemon species / move / ability
proper names remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEMON_LEAGUE_HALL_OF_FAME_V3_44"
REL = Path("data/maps/PokemonLeague_HallOfFame_Frlg/scripts.inc")

PINNED = (
    "PokemonLeague_HallOfFame_Text_OakCongratulations::\n"
    "\t.string \"OAK: Er-hem!\\n\"\n"
    "\t.string \"Congratulations, {PLAYER}!\\p\"\n"
    "\t.string \"This floor is the POKéMON HALL OF\\n\"\n"
    "\t.string \"FAME.\\p\"\n"
    "\t.string \"POKéMON LEAGUE CHAMPIONS are\\n\"\n"
    "\t.string \"honored for their exploits here.\\p\"\n"
    "\t.string \"Their POKéMON are also recorded in\\n\"\n"
    "\t.string \"the HALL OF FAME.\\p\"\n"
    "\t.string \"{PLAYER}!\\p\"\n"
    "\t.string \"You have worked hard to become\\n\"\n"
    "\t.string \"the new LEAGUE CHAMPION.\\p\"\n"
    "\t.string \"Congratulations, {PLAYER}, you and\\n\"\n"
    "\t.string \"your POKéMON are HALL OF FAMERS!$\"\n"
)

RU = (
    "PokemonLeague_HallOfFame_Text_OakCongratulations::\n"
    "\t.string \"OAK: Кхм!\\n\"\n"
    "\t.string \"Поздравляю, {PLAYER}!\\p\"\n"
    "\t.string \"Это ЗАЛ СЛАВЫ ЛИГИ\\n\"\n"
    "\t.string \"ПОКЕМОНОВ.\\p\"\n"
    "\t.string \"Здесь чествуют ЧЕМПИОНОВ ЛИГИ\\n\"\n"
    "\t.string \"за их великие победы.\\p\"\n"
    "\t.string \"Их ПОКЕМОНЫ тоже остаются\\n\"\n"
    "\t.string \"в истории ЗАЛА СЛАВЫ.\\p\"\n"
    "\t.string \"{PLAYER}!\\p\"\n"
    "\t.string \"Ты много трудился, чтобы стать\\n\"\n"
    "\t.string \"новым ЧЕМПИОНОМ ЛИГИ.\\p\"\n"
    "\t.string \"Поздравляю, {PLAYER}! Ты и твои\\n\"\n"
    "\t.string \"ПОКЕМОНЫ теперь в ЗАЛЕ СЛАВЫ!$\"\n"
)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_league_hall_of_fame_v3_44.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")

    variants = [PINNED]
    normalized = PINNED.replace("é", "e").replace("É", "E")
    if normalized != PINNED:
        variants.append(normalized)
    hits = [(variant, text.count(variant)) for variant in variants]
    total = sum(count for _, count in hits)
    if total != 1:
        raise SystemExit(f"{MARKER}: expected exactly one pinned/normalized Hall of Fame anchor, found {total}")
    source = next(variant for variant, count in hits if count == 1)
    text = text.replace(source, RU, 1)
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_pokemon_league_hall_of_fame_v3_44_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": ["PokemonLeague_HallOfFame_Text_OakCongratulations"],
        "translatedBlockCount": 1,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated 1 mandatory Hall of Fame Oak runtime block; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
