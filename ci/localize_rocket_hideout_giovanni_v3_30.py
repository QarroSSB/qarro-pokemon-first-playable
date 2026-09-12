#!/usr/bin/env python3
"""Qarro v3.30 mandatory Rocket Hideout / Giovanni Russian runtime localization.

Translates only the verified pinned Rocket Hideout progression chain required
for the Silph Scope: Giovanni intro, defeat, and post-battle dialogue. Pokemon
species / move / ability proper names remain English. Ash Bond / Ash Cap are
not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROCKET_HIDEOUT_GIOVANNI_V3_30"
REL = Path("data/maps/RocketHideout_B4F_Frlg/scripts.inc")

PATCHES = {
    "RocketHideout_B4F_Text_GiovanniIntro": (
        "RocketHideout_B4F_Text_GiovanniIntro::\n"
        "\t.string \"So! I must say, I am impressed you\\n\"\n"
        "\t.string \"got here.\\p\"\n"
        "\t.string \"TEAM ROCKET captures POKéMON from\\n\"\n"
        "\t.string \"around the world.\\p\"\n"
        "\t.string \"They're important tools for keeping\\n\"\n"
        "\t.string \"our criminal enterprise going.\\p\"\n"
        "\t.string \"I am the leader, GIOVANNI!\\p\"\n"
        "\t.string \"For your insolence, you will feel a\\n\"\n"
        "\t.string \"world of pain!$\"\n",
        "RocketHideout_B4F_Text_GiovanniIntro::\n"
        "\t.string \"Что ж! Признаю, я впечатлён, что\\n\"\n"
        "\t.string \"ты смог добраться сюда.\\p\"\n"
        "\t.string \"КОМАНДА R собирает ПОКЕМОНОВ\\n\"\n"
        "\t.string \"со всего мира.\\p\"\n"
        "\t.string \"Они нужны для процветания нашего\\n\"\n"
        "\t.string \"преступного дела.\\p\"\n"
        "\t.string \"Я их лидер - ДЖОВАННИ!\\p\"\n"
        "\t.string \"За свою дерзость ты узнаешь, что\\n\"\n"
        "\t.string \"такое настоящая боль!$\"\n",
    ),
    "RocketHideout_B4F_Text_GiovanniDefeat": (
        "RocketHideout_B4F_Text_GiovanniDefeat::\n"
        "\t.string \"WHAT!\\n\"\n"
        "\t.string \"This can't be!$\"\n",
        "RocketHideout_B4F_Text_GiovanniDefeat::\n"
        "\t.string \"ЧТО?!\\n\"\n"
        "\t.string \"Этого не может быть!$\"\n",
    ),
    "RocketHideout_B4F_Text_GiovanniPostBattle": (
        "RocketHideout_B4F_Text_GiovanniPostBattle::\n"
        "\t.string \"I see that you raise POKéMON with\\n\"\n"
        "\t.string \"utmost care.\\p\"\n"
        "\t.string \"A child like you would never\\n\"\n"
        "\t.string \"understand what I hope to achieve.\\p\"\n"
        "\t.string \"I shall step aside this time!\\p\"\n"
        "\t.string \"I hope we meet again…$\"\n",
        "RocketHideout_B4F_Text_GiovanniPostBattle::\n"
        "\t.string \"Вижу, ты заботливо растишь своих\\n\"\n"
        "\t.string \"ПОКЕМОНОВ.\\p\"\n"
        "\t.string \"Но ребёнку вроде тебя не понять,\\n\"\n"
        "\t.string \"чего я стремлюсь достичь.\\p\"\n"
        "\t.string \"На этот раз я отступлю!\\p\"\n"
        "\t.string \"Надеюсь, мы ещё встретимся…$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_rocket_hideout_giovanni_v3_30.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_rocket_hideout_giovanni_v3_30_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Rocket Hideout Giovanni runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
