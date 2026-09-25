#!/usr/bin/env python3
"""Qarro v3.27 mandatory S.S. Anne Rival Russian runtime localization.

Translates only the verified pinned Rival progression chain immediately before
the Captain: intro, defeat, and post-battle direction to the CUT master.
Pokemon species / move / ability proper names remain English. Ash Bond / Ash
Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_SSANNE_RIVAL_V3_27"
REL = Path("data/maps/SSAnne_2F_Corridor_Frlg/scripts.inc")

PATCHES = {
    "SSAnne_2F_Corridor_Text_RivalIntro": (
        "SSAnne_2F_Corridor_Text_RivalIntro::\n"
        "\t.string \"{RIVAL}: Bonjour!\\n\"\n"
        "\t.string \"{PLAYER}!\\p\"\n"
        "\t.string \"Imagine seeing you here!\\n\"\n"
        "\t.string \"{PLAYER}, were you really invited?\\p\"\n"
        "\t.string \"So how's your POKéDEX coming?\\p\"\n"
        "\t.string \"I already caught 40 kinds, pal.\\n\"\n"
        "\t.string \"Different kinds are everywhere.\\p\"\n"
        "\t.string \"Crawl around in grassy areas, and\\n\"\n"
        "\t.string \"look hard for them.$\"\n",
        "SSAnne_2F_Corridor_Text_RivalIntro::\n"
        "\t.string \"{RIVAL}: Бонжур!\\n\"\n"
        "\t.string \"{PLAYER}!\\p\"\n"
        "\t.string \"Не ожидал увидеть тебя здесь!\\n\"\n"
        "\t.string \"{PLAYER}, тебя правда пригласили?\\p\"\n"
        "\t.string \"Ну как там твой POKeDEX?\\p\"\n"
        "\t.string \"Я уже поймал 40 видов, приятель.\\n\"\n"
        "\t.string \"Разные виды встречаются повсюду.\\p\"\n"
        "\t.string \"Ищи в траве как следует -\\n\"\n"
        "\t.string \"там можно найти много нового.$\"\n",
    ),
    "SSAnne_2F_Corridor_Text_RivalDefeat": (
        "SSAnne_2F_Corridor_Text_RivalDefeat::\n"
        "\t.string \"Humph!\\p\"\n"
        "\t.string \"At least you're raising your\\n\"\n"
        "\t.string \"POKéMON!$\"\n",
        "SSAnne_2F_Corridor_Text_RivalDefeat::\n"
        "\t.string \"Хмф!\\p\"\n"
        "\t.string \"По крайней мере, своих\\n\"\n"
        "\t.string \"ПОКЕМОНОВ ты тренируешь!$\"\n",
    ),
    "SSAnne_2F_Corridor_Text_RivalPostBattle": (
        "SSAnne_2F_Corridor_Text_RivalPostBattle::\n"
        "\t.string \"{RIVAL}: I heard there was a CUT\\n\"\n"
        "\t.string \"master on board.\\p\"\n"
        "\t.string \"But he was just a seasick old man!\\p\"\n"
        "\t.string \"CUT itself is really useful.\\n\"\n"
        "\t.string \"Yup, it'll be handy.\\p\"\n"
        "\t.string \"You should go see him, too.\\n\"\n"
        "\t.string \"Smell ya!$\"\n",
        "SSAnne_2F_Corridor_Text_RivalPostBattle::\n"
        "\t.string \"{RIVAL}: Слышал, на борту есть\\n\"\n"
        "\t.string \"мастер CUT.\\p\"\n"
        "\t.string \"Но это просто старик с морской\\n\"\n"
        "\t.string \"болезнью!\\p\"\n"
        "\t.string \"Сама CUT очень полезна.\\n\"\n"
        "\t.string \"Да, точно пригодится.\\p\"\n"
        "\t.string \"Тебе тоже стоит к нему зайти.\\n\"\n"
        "\t.string \"Увидимся!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_ssanne_rival_v3_27.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_ssanne_rival_v3_27_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory S.S. Anne Rival runtime blocks; Ash Bond/Ash Cap untouched")

    surge_script = Path(__file__).with_name("localize_vermilion_surge_v3_28.py")
    subprocess.run([sys.executable, str(surge_script), str(root)], check=True)
    erika_script = Path(__file__).with_name("localize_celadon_erika_v3_29.py")
    subprocess.run([sys.executable, str(erika_script), str(root)], check=True)
    giovanni_script = Path(__file__).with_name("localize_rocket_hideout_giovanni_v3_30.py")
    subprocess.run([sys.executable, str(giovanni_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
