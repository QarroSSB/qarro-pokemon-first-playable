#!/usr/bin/env python3
"""Qarro v3.66 mandatory Rocket Warehouse second Grunt localization.

Translates only the verified Grunt2 trainer dialogue in Five Island Rocket
Warehouse. Grunt3, both Admins, Gideon, optional signs/items, Ash Bond, and
Ash Cap remain untouched. Pokemon species / move / ability proper names remain
English.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROCKET_WAREHOUSE_GRUNT2_V3_66"
REL = Path("data/maps/FiveIsland_RocketWarehouse_Frlg/scripts.inc")

PATCHES = {
    "FiveIsland_RocketWarehouse_Text_Grunt2Intro": {
        "needles": ("Did you come here knowing it's", "TEAM ROCKET's WAREHOUSE?"),
        "ru": '''FiveIsland_RocketWarehouse_Text_Grunt2Intro::
\t.string "Ты пришёл сюда, зная, что это\\n"
\t.string "СКЛАД TEAM ROCKET?$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_Grunt2Defeat": {
        "needles": ("What do you think you're doing?!",),
        "ru": '''FiveIsland_RocketWarehouse_Text_Grunt2Defeat::
\t.string "Что ты творишь?!$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_Grunt2PostBattle": {
        "needles": ("TEAM ROCKET broke up?", "What planet are you from?"),
        "ru": '''FiveIsland_RocketWarehouse_Text_Grunt2PostBattle::
\t.string "TEAM ROCKET распалась?\\n"
\t.string "Ты с какой планеты?$"
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
        raise SystemExit("usage: localize_rocket_warehouse_grunt2_v3_66.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_rocket_warehouse_grunt2_v3_66_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "Rocket Warehouse Grunt2 trainer dialogue on Sapphire recovery route",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Rocket Warehouse Grunt2 blocks; Ash Bond/Ash Cap untouched")

    next_script = Path(__file__).with_name("localize_rocket_warehouse_grunt3_v3_67.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
