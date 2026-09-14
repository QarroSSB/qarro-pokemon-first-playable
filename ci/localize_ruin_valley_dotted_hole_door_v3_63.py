#!/usr/bin/env python3
"""Qarro v3.63 mandatory Ruin Valley / Dotted Hole door localization.

Translates only the verified Dotted Hole door interaction required for Sapphire
progression on Six Island. The Braille CUT clue stays English because move names
remain English by project policy. Optional Ruin Valley NPC/trainer text, later
Dotted Hole/Sapphire scenes, Ash Bond, and Ash Cap remain untouched.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_RUIN_VALLEY_DOTTED_HOLE_DOOR_V3_63"
REL = Path("data/maps/SixIsland_RuinValley_Frlg/scripts.inc")

PATCHES = {
    "SixIsland_RuinValley_Text_CheckDoorMoreThoroughly": {
        "needles": ("The door doesn't budge at all", "Check it more thoroughly"),
        "ru": '''SixIsland_RuinValley_Text_CheckDoorMoreThoroughly::
\t.string "Дверь совсем не поддаётся.\\n"
\t.string "Осмотреть её внимательнее?$"
''',
    },
    "SixIsland_RuinValley_Text_LeftDoorAlone": {
        "needles": ("{PLAYER} left the door alone",),
        "ru": '''SixIsland_RuinValley_Text_LeftDoorAlone::
\t.string "{PLAYER} оставил дверь в покое.$"
''',
    },
    "SixIsland_RuinValley_Text_SeveralDotsOnTheDoor": {
        "needles": ("On closer inspection", "several dots on the door"),
        "ru": '''SixIsland_RuinValley_Text_SeveralDotsOnTheDoor::
\t.string "При внимательном осмотре на двери\\n"
\t.string "видно несколько точек...$"
''',
    },
    "SixIsland_RuinValley_Text_DoorIsOpen": {
        "needles": ("The door is open",),
        "ru": '''SixIsland_RuinValley_Text_DoorIsOpen::
\t.string "Дверь открыта.$"
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
        raise SystemExit("usage: localize_ruin_valley_dotted_hole_door_v3_63.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_ruin_valley_dotted_hole_door_v3_63_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Six Island Ruin Valley Dotted Hole door interaction",
        "moveNamePolicy": "Braille CUT clue intentionally remains English",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Dotted Hole door blocks; CUT/Ash Bond/Ash Cap untouched")

    next_script = Path(__file__).with_name("localize_dotted_hole_sapphire_theft_v3_64.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
