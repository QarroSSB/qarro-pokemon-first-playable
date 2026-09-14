#!/usr/bin/env python3
"""Qarro v3.67 mandatory Rocket Warehouse third Grunt localization.

Translates only the verified third Rocket Grunt battle on the required spinner-
maze route toward the first Rocket Admin. Both Admins, Gideon, optional
signs/items, Ash Bond, and Ash Cap remain untouched. Pokemon species / move /
ability proper names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROCKET_WAREHOUSE_GRUNT3_V3_67"
REL = Path("data/maps/FiveIsland_RocketWarehouse_Frlg/scripts.inc")

PATCHES = {
    "FiveIsland_RocketWarehouse_Text_Grunt3Intro": {
        "needles": ("I got word about you from the", "know our BOSS GIOVANNI!"),
        "ru": '''FiveIsland_RocketWarehouse_Text_Grunt3Intro::
\t.string "Мне уже рассказали о тебе.\\p"
\t.string "Но такой ребёнок не может\\n"
\t.string "знать нашего БОССА GIOVANNI!$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_Grunt3Defeat": {
        "needles": ("Don't…you…dare…laugh…",),
        "ru": '''FiveIsland_RocketWarehouse_Text_Grunt3Defeat::
\t.string "Не... смей... смеяться...$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_Grunt3PostBattle": {
        "needles": ("Don't mess in the doings of adults,", "you jumped-up pip-squeak!"),
        "ru": '''FiveIsland_RocketWarehouse_Text_Grunt3PostBattle::
\t.string "Не лезь в дела взрослых,\\n"
\t.string "мелкий выскочка!$"
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
        raise SystemExit("usage: localize_rocket_warehouse_grunt3_v3_67.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_rocket_warehouse_grunt3_v3_67_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory third Rocket Warehouse Grunt battle before first Admin",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Rocket Warehouse Grunt3 blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
