#!/usr/bin/env python3
"""Qarro v3.23 mandatory Cerulean Rival Russian runtime localization.

Translates only the verified pinned Cerulean Rival progression chain: intro,
defeat, post-battle Bill direction, gift setup, and Fame Checker explanation.
Pokemon species / move / ability proper names remain English. Ash Bond / Ash
Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_CERULEAN_RIVAL_V3_23"
REL = Path("data/maps/CeruleanCity_Frlg/scripts.inc")

PATCHES = {
    "CeruleanCity_Text_RivalIntro": (
        "CeruleanCity_Text_RivalIntro::\n"
        "\t.string \"{RIVAL}: Yo! {PLAYER}!\\p\"\n"
        "\t.string \"You're still struggling along back\\n\"\n"
        "\t.string \"here?\\p\"\n"
        "\t.string \"I'm doing great! I caught a bunch\\n\"\n"
        "\t.string \"of strong and smart POKéMON!\\p\"\n"
        "\t.string \"Here, let me see what you caught,\\n\"\n"
        "\t.string \"{PLAYER}!$\"\n",
        "CeruleanCity_Text_RivalIntro::\n"
        "\t.string \"{RIVAL}: Эй, {PLAYER}!\\p\"\n"
        "\t.string \"Ты всё ещё плетёшься где-то\\n\"\n"
        "\t.string \"позади?\\p\"\n"
        "\t.string \"А у меня всё отлично! Я поймал\\n\"\n"
        "\t.string \"кучу сильных и умных ПОКЕМОНОВ!\\p\"\n"
        "\t.string \"Ну-ка покажи, кого поймал ты,\\n\"\n"
        "\t.string \"{PLAYER}!$\"\n",
    ),
    "CeruleanCity_Text_RivalDefeat": (
        "CeruleanCity_Text_RivalDefeat::\n"
        "\t.string \"Hey!\\n\"\n"
        "\t.string \"Take it easy!\\l\"\n"
        "\t.string \"You won already!$\"\n",
        "CeruleanCity_Text_RivalDefeat::\n"
        "\t.string \"Эй!\\n\"\n"
        "\t.string \"Полегче!\\l\"\n"
        "\t.string \"Ты уже победил!$\"\n",
    ),
    "CeruleanCity_Text_RivalPostBattle": (
        "CeruleanCity_Text_RivalPostBattle::\n"
        "\t.string \"{RIVAL}: Hey, guess what?\\p\"\n"
        "\t.string \"I went to BILL's and got him to\\n\"\n"
        "\t.string \"show me his rare POKéMON.\\p\"\n"
        "\t.string \"That added a lot of pages to my\\n\"\n"
        "\t.string \"POKéDEX!\\p\"\n"
        "\t.string \"After all, BILL's world famous as a\\n\"\n"
        "\t.string \"POKéMANIAC.\\p\"\n"
        "\t.string \"He invented the POKéMON Storage\\n\"\n"
        "\t.string \"System on PC, too.\\p\"\n"
        "\t.string \"Since you're using his system,\\n\"\n"
        "\t.string \"you should go thank him.\\p\"\n"
        "\t.string \"Well, I better get rolling!\\n\"\n"
        "\t.string \"Smell ya later!$\"\n",
        "CeruleanCity_Text_RivalPostBattle::\n"
        "\t.string \"{RIVAL}: Эй, знаешь что?\\p\"\n"
        "\t.string \"Я был у БИЛЛА, и он показал мне\\n\"\n"
        "\t.string \"своих редких ПОКЕМОНОВ.\\p\"\n"
        "\t.string \"Мой ПОКЕДЕКС здорово пополнился!\\p\"\n"
        "\t.string \"БИЛЛ ведь всемирно известный\\n\"\n"
        "\t.string \"ПОКЕМАНЬЯК.\\p\"\n"
        "\t.string \"Он ещё и создал систему хранения\\n\"\n"
        "\t.string \"ПОКЕМОНОВ на ПК.\\p\"\n"
        "\t.string \"Раз уж ты пользуешься его системой,\\n\"\n"
        "\t.string \"сходи и поблагодари его.\\p\"\n"
        "\t.string \"Ладно, мне пора!\\n\"\n"
        "\t.string \"Ещё увидимся!$\"\n",
    ),
    "CeruleanCity_Text_OhRightLittlePresentAsFavor": (
        "CeruleanCity_Text_OhRightLittlePresentAsFavor::\n"
        "\t.string \"Oh, yeah, right.\\p\"\n"
        "\t.string \"I feel sorry for you. No, really.\\n\"\n"
        "\t.string \"You're always plodding behind me.\\p\"\n"
        "\t.string \"So here, I'll give you a little\\n\"\n"
        "\t.string \"present as a favor.$\"\n",
        "CeruleanCity_Text_OhRightLittlePresentAsFavor::\n"
        "\t.string \"А, да, чуть не забыл.\\p\"\n"
        "\t.string \"Мне даже жаль тебя. Серьёзно.\\n\"\n"
        "\t.string \"Ты вечно тащишься позади меня.\\p\"\n"
        "\t.string \"Так что держи небольшой подарок.$\"\n",
    ),
    "CeruleanCity_Text_ExplainFameCheckerSmellYa": (
        "CeruleanCity_Text_ExplainFameCheckerSmellYa::\n"
        "\t.string \"A chatty gossip like you…\\n\"\n"
        "\t.string \"That thing's perfect.\\p\"\n"
        "\t.string \"I don't need it because I don't\\n\"\n"
        "\t.string \"give a hoot about others.\\p\"\n"
        "\t.string \"All right, this time I really am\\n\"\n"
        "\t.string \"gone. Smell ya!$\"\n",
        "CeruleanCity_Text_ExplainFameCheckerSmellYa::\n"
        "\t.string \"Для такого любителя сплетен, как ты,\\n\"\n"
        "\t.string \"эта штука подходит идеально.\\p\"\n"
        "\t.string \"Мне она не нужна - мне нет дела\\n\"\n"
        "\t.string \"до остальных.\\p\"\n"
        "\t.string \"Ну всё, теперь я точно пошёл.\\n\"\n"
        "\t.string \"Ещё увидимся!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_cerulean_rival_v3_23.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_cerulean_rival_v3_23_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names may remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Cerulean Rival runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
