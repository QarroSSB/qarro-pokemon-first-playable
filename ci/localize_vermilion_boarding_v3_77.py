#!/usr/bin/env python3
"""Qarro v3.77 mandatory Vermilion S.S. Anne boarding localization.

Translates only the verified mandatory S.S. Anne access dialogue in Vermilion
City: welcome, ticket check, ticket flash, and no-ticket rejection. No gameplay
logic, trainer data, Ash Bond, or Ash Cap paths are touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_VERMILION_BOARDING_V3_77"
REL = Path("data/maps/VermilionCity_Frlg/scripts.inc")

PATCHES = {
    "VermilionCity_Text_WelcomeToTheSSAnne": {
        "needles": ("Welcome to the S.S. ANNE!",),
        "ru": '''VermilionCity_Text_WelcomeToTheSSAnne::
\t.string "Добро пожаловать на S.S. ANNE!$"
''',
    },
    "VermilionCity_Text_DoYouHaveATicket": {
        "needles": ("Welcome to the S.S. ANNE!", "Excuse me, do you have a ticket?"),
        "ru": '''VermilionCity_Text_DoYouHaveATicket::
\t.string "Добро пожаловать на S.S. ANNE!\\p"
\t.string "Извините, у вас есть билет?$"
''',
    },
    "VermilionCity_Text_FlashedSSTicket": {
        "needles": ("{PLAYER} flashed the S.S. TICKET!", "Great!", "Welcome to the S.S. ANNE!"),
        "ru": '''VermilionCity_Text_FlashedSSTicket::
\t.string "{FONT_NORMAL}{PLAYER} показал S.S. TICKET!\\p"
\t.string "{FONT_MALE}Отлично!\\n"
\t.string "Добро пожаловать на S.S. ANNE!$"
''',
    },
    "VermilionCity_Text_DontHaveNeededSSTicket": {
        "needles": ("doesn't have the needed", "S.S. TICKET.", "You need a ticket to get aboard."),
        "ru": '''VermilionCity_Text_DontHaveNeededSSTicket::
\t.string "{FONT_NORMAL}У {PLAYER} нет нужного\\n"
\t.string "S.S. TICKET.\\p"
\t.string "{FONT_MALE}Извините!\\p"
\t.string "Для посадки нужен билет.$"
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
        raise SystemExit("usage: localize_vermilion_boarding_v3_77.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []
    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)
    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_vermilion_boarding_v3_77_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "file": str(REL), "translatedBlocks": applied, "translatedBlockCount": len(applied), "scope": "mandatory Vermilion S.S. Anne boarding dialogue only", "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English", "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Vermilion boarding blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
