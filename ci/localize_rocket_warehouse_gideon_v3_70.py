#!/usr/bin/env python3
"""Qarro v3.70 mandatory Rocket Warehouse Gideon localization.

Translates only the verified Gideon battle and immediate post-battle Sapphire
return dialogue. Optional repeat dialogue, Giovanni's-child dialogue, signs,
items, Ash Bond, and Ash Cap remain untouched. Pokemon species / move / ability
proper names remain English.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROCKET_WAREHOUSE_GIDEON_V3_70"
REL = Path("data/maps/FiveIsland_RocketWarehouse_Frlg/scripts.inc")

PATCHES = {
    "FiveIsland_RocketWarehouse_Text_GideonIntro": {
        "needles": ("sell the", "SAPPHIRE for huge money", "blow the whole deal apart", "no forgiveness for you"),
        "ru": '''FiveIsland_RocketWarehouse_Text_GideonIntro::
\t.string "Я почти продал САПФИР\\n"
\t.string "за огромные деньги...\\p"
\t.string "Но тут появился ты и сорвал\\n"
\t.string "всю сделку!\\p"
\t.string "Фуфу... Фуфуфу...\\n"
\t.string "Я тебе этого не прощу!$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_GideonDefeat": {
        "needles": ("Gah! Darn!", "Darn! Darn!"),
        "ru": '''FiveIsland_RocketWarehouse_Text_GideonDefeat::
\t.string "Ах! Черт!\\n"
\t.string "Черт! Черт!$"
''',
    },
    "FiveIsland_RocketWarehouse_Text_GideonPostBattle": {
        "needles": ("If I can't sell it, it's worthless!", "Go ahead, take it!"),
        "ru": '''FiveIsland_RocketWarehouse_Text_GideonPostBattle::
\t.string "Если я не могу его продать,\\n"
\t.string "он мне ни к чему!\\p"
\t.string "Давай, забирай!$"
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
        raise SystemExit("usage: localize_rocket_warehouse_gideon_v3_70.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_rocket_warehouse_gideon_v3_70_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Gideon battle and immediate post-battle Sapphire return dialogue",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Gideon blocks; Ash Bond/Ash Cap untouched")

    next_script = Path(__file__).with_name("localize_celio_sapphire_network_v3_71.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
