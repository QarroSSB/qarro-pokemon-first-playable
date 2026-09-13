#!/usr/bin/env python3
"""Qarro v3.37 mandatory Route 22 late Rival Russian runtime localization.

Translates only the verified pinned late Rival progression chain before the
Pokemon League: intro, defeat, and post-battle dialogue. Pokemon species /
move / ability proper names remain English. Ash Bond / Ash Cap are not
referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTE22_LATE_RIVAL_V3_37"
REL = Path("data/maps/Route22_Frlg/scripts.inc")

PATCHES = {
    "Route22_Text_LateRivalIntro": (
        "Route22_Text_LateRivalIntro::\n"
        "\t.string \"{RIVAL}: What? {PLAYER}!\\n\"\n"
        "\t.string \"What a surprise to see you here!\\p\"\n"
        "\t.string \"So you're going to the POKéMON\\n\"\n"
        "\t.string \"LEAGUE?\\p\"\n"
        "\t.string \"You collected all the BADGES, too?\\n\"\n"
        "\t.string \"That's cool!\\p\"\n"
        "\t.string \"Then I'll whip you, {PLAYER}, as a\\n\"\n"
        "\t.string \"warm-up for the POKéMON LEAGUE!\\p\"\n"
        "\t.string \"Come on!$\"\n",
        "Route22_Text_LateRivalIntro::\n"
        "\t.string \"{RIVAL}: Что? {PLAYER}!\\n\"\n"
        "\t.string \"Не ожидал увидеть тебя здесь!\\p\"\n"
        "\t.string \"Тоже идёшь в ЛИГУ ПОКЕМОНОВ?\\p\"\n"
        "\t.string \"И все ЗНАЧКИ уже собраны?\\n\"\n"
        "\t.string \"Неплохо!\\p\"\n"
        "\t.string \"Тогда я разомнусь на тебе, {PLAYER},\\n\"\n"
        "\t.string \"перед ЛИГОЙ ПОКЕМОНОВ!\\p\"\n"
        "\t.string \"Давай!$\"\n",
    ),
    "Route22_Text_LateRivalDefeat": (
        "Route22_Text_LateRivalDefeat::\n"
        "\t.string \"What!?\\p\"\n"
        "\t.string \"I was just careless, you!$\"\n",
        "Route22_Text_LateRivalDefeat::\n"
        "\t.string \"Что?!\\p\"\n"
        "\t.string \"Я просто потерял бдительность!$\"\n",
    ),
    "Route22_Text_LateRivalPostBattle": (
        "Route22_Text_LateRivalPostBattle::\n"
        "\t.string \"That loosened me up.\\n\"\n"
        "\t.string \"I'm ready for the POKéMON LEAGUE!\\p\"\n"
        "\t.string \"{PLAYER}, you need more practice.\\p\"\n"
        "\t.string \"But hey, you know that!\\n\"\n"
        "\t.string \"I'm out of here. Smell ya!$\"\n",
        "Route22_Text_LateRivalPostBattle::\n"
        "\t.string \"Отличная разминка.\\n\"\n"
        "\t.string \"Теперь я готов к ЛИГЕ ПОКЕМОНОВ!\\p\"\n"
        "\t.string \"{PLAYER}, тебе ещё надо тренироваться.\\p\"\n"
        "\t.string \"Хотя ты и сам это знаешь!\\n\"\n"
        "\t.string \"Я пошёл. Ещё увидимся!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_route22_late_rival_v3_37.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_route22_late_rival_v3_37_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Route 22 late Rival runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
