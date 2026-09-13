#!/usr/bin/env python3
"""Qarro v3.56 mandatory One Island Celio Ruby-request localization.

Translates only the verified post-National-Dex Celio request that starts the
Ruby/Mt. Ember progression: Celio notices the expanded Pokédex, explains the
long-distance Network Machine work, and says a special gemstone is required.
The Ruby handoff, Rainbow Pass, Sapphire quest, optional NPC dialogue, Ash Bond,
and Ash Cap remain untouched. Pokemon species / move / ability proper names
remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ONE_ISLAND_CELIO_RUBY_REQUEST_V3_56"
REL = Path("data/maps/OneIsland_PokemonCenter_1F_Frlg/scripts.inc")

PATCHES = {
    "OneIsland_PokemonCenter_1F_Text_CelioCaughtMoreMonMaybeICanBeUseful": {
        "needles": ("CELIO: {PLAYER}", "You've caught more POKéMON", "Maybe I can be useful"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_CelioCaughtMoreMonMaybeICanBeUseful::
\t.string "CELIO: {PLAYER}, как твои дела?\\p"
\t.string "Вот как?\\p"
\t.string "Ты поймал ещё больше POKeMON.\\p"
\t.string "Знаешь что?\\n"
\t.string "Кажется, я могу тебе помочь.$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_YoullBeTradingFromTrainersFarAway": {
        "needles": ("modifying the Network Machine", "trades over long distances", "TRAINERS far away"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_YoullBeTradingFromTrainersFarAway::
\t.string "Сейчас я дорабатываю\\n"
\t.string "NETWORK MACHINE.\\p"
\t.string "Хочу, чтобы она поддерживала\\n"
\t.string "обмены на большие расстояния.\\p"
\t.string "Когда закончу, ты сможешь\\n"
\t.string "обмениваться редкими POKeMON\\l"
\t.string "с ТРЕНЕРАМИ издалека.$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_NeedsSpecialGemstone": {
        "needles": ("slight catch", "needs a special gemstone", "ONE ISLAND"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_NeedsSpecialGemstone::
\t.string "Но есть небольшая проблема.\\p"
\t.string "Чтобы связь заработала, машине\\n"
\t.string "нужен особый драгоценный камень.\\p"
\t.string "Говорят, он находится на\\n"
\t.string "ONE ISLAND, но я его не нашёл.\\p"
\t.string "Кто знает, где он может быть.$"
''',
    },
}

LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")


def replace_label_block(text: str, label: str, needles: tuple[str, ...], replacement: str) -> str:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    block = text[start:end]
    missing = [needle for needle in needles if needle not in block]
    if missing:
        raise SystemExit(f"{MARKER}: {label}: pinned evidence mismatch; missing {missing}")
    if re.search(r"[А-Яа-яЁё]", block):
        raise SystemExit(f"{MARKER}: {label}: block is already localized or unexpectedly contains Cyrillic")
    return text[:start] + replacement + "\n" + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_one_island_celio_ruby_request_v3_56.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_one_island_celio_ruby_request_v3_56_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory post-National-Dex Celio request that enables Mt. Ember Ruby progression",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Celio Ruby-request blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
