#!/usr/bin/env python3
"""Qarro v3.69 mandatory Rocket Warehouse second Admin localization.

Translates only the verified second Rocket Admin battle and mandatory post-
battle dialogue that clears the Rocket Warehouse. Gideon, optional signs/items,
Ash Bond, and Ash Cap remain untouched. Pokemon species / move / ability proper
names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROCKET_WAREHOUSE_ADMIN2_V3_69"
REL = Path("data/maps/FiveIsland_RocketWarehouse_Frlg/scripts.inc")

PATCHES = {
    "FiveIsland_RocketWarehouse_Text_Admin2Intro": {
        "needles": ("playing the hero, kid.", "ROCKET has disbanded", "an angry adult can be!"),
        "ru": '''FiveIsland_RocketWarehouse_Text_Admin2Intro::
\t.string "Хватит изображать героя,\\n"
\t.string "малыш.\\p"
\t.string "Ты распускаешь ложь, будто TEAM\\n"
\t.string "ROCKET распалась...\\p"
\t.string "Хочешь посеять смуту в наших\\n"
\t.string "рядах.\\p"
\t.string "Но мы не настолько глупы, чтобы\\n"
\t.string "поверить ребёнку!\\p"
\t.string "А теперь я покажу, насколько\\n"
\t.string "страшен разъярённый взрослый!$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_Admin2Defeat": {
        "needles": ("You were too strong", "GIOVANNI's BADGE", "TEAM ROCKET really has disbanded?"),
        "ru": '''FiveIsland_RocketWarehouse_Text_Admin2Defeat::
\t.string "Ургх...\\n"
\t.string "Ты слишком силён...\\p"
\t.string "...\\n"
\t.string "Э-это ЗНАЧОК GIOVANNI!\\p"
\t.string "Значит, это правда?\\n"
\t.string "TEAM ROCKET действительно\\n"
\t.string "распалась?$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_Admin2PostBattle": {
        "needles": ("We will abandon this WAREHOUSE", "I will find GIOVANNI.", "Until then, farewell!"),
        "ru": '''FiveIsland_RocketWarehouse_Text_Admin2PostBattle::
\t.string "Мы покинем этот WAREHOUSE...\\p"
\t.string "Но не думай, что всё кончено.\\n"
\t.string "Я не позволю этому стать концом.\\p"
\t.string "Я найду GIOVANNI.\\n"
\t.string "И возрожу TEAM ROCKET!\\l"
\t.string "Я обязательно...\\p"
\t.string "А пока — прощай!$"
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
        raise SystemExit("usage: localize_rocket_warehouse_admin2_v3_69.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_rocket_warehouse_admin2_v3_69_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory second Rocket Warehouse Admin battle and Rocket-clearing post-battle dialogue",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Rocket Warehouse Admin2 blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
