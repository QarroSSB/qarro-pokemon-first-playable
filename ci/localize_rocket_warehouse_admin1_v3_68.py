#!/usr/bin/env python3
"""Qarro v3.68 mandatory Rocket Warehouse first Admin localization.

Translates only the verified first Rocket Admin battle and its mandatory
post-battle shortcut dialogue. Admin2, Gideon, optional signs/items, Ash Bond,
and Ash Cap remain untouched. Pokemon species / move / ability proper names
remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROCKET_WAREHOUSE_ADMIN1_V3_68"
REL = Path("data/maps/FiveIsland_RocketWarehouse_Frlg/scripts.inc")

PATCHES = {
    "FiveIsland_RocketWarehouse_Text_Admin1Intro": {
        "needles": ("I don't know or care if what I'm", "and do as I am told."),
        "ru": '''FiveIsland_RocketWarehouse_Text_Admin1Intro::
\t.string "Мне всё равно, правильно ли я\\n"
\t.string "поступаю или нет...\\p"
\t.string "Я просто верю GIOVANNI\\n"
\t.string "и выполняю его приказы.$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_Admin1Defeat": {
        "needles": ("I'm shattered",),
        "ru": '''FiveIsland_RocketWarehouse_Text_Admin1Defeat::
\t.string "Я...\\n"
\t.string "Я разбит...$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_Admin1PostBattle": {
        "needles": ("according to", "beliefs and morals", "I understand now"),
        "ru": '''FiveIsland_RocketWarehouse_Text_Admin1PostBattle::
\t.string "Ты действуешь согласно своим\\n"
\t.string "убеждениям и принципам.\\p"
\t.string "Теперь я понимаю...$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_MadeItSoYouCanComeBackThrough": {
        "needles": ("I've made it so you can come back", "The ADMIN after me outranks me", "harsh challenge."),
        "ru": '''FiveIsland_RocketWarehouse_Text_MadeItSoYouCanComeBackThrough::
\t.string "Я открыл тебе обратный путь\\n"
\t.string "через этот проход.\\p"
\t.string "Отдохни и подготовься к тому,\\n"
\t.string "что ждёт тебя впереди.\\p"
\t.string "Следующий ADMIN намного выше\\n"
\t.string "меня по уровню как тренер.\\p"
\t.string "Приготовься к очень тяжёлому\\n"
\t.string "испытанию.$"
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
        raise SystemExit("usage: localize_rocket_warehouse_admin1_v3_68.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_rocket_warehouse_admin1_v3_68_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory first Rocket Warehouse Admin battle and post-battle shortcut dialogue",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Rocket Warehouse Admin1 blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
