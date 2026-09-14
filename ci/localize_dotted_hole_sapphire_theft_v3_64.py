#!/usr/bin/env python3
"""Qarro v3.64 mandatory Dotted Hole Sapphire theft localization.

Translates only the verified forced Sapphire pickup/theft scene in the Six Island
Dotted Hole Sapphire room. Optional Braille text, Rocket Warehouse follow-up,
Ash Bond, and Ash Cap remain untouched. Pokemon species / move / ability proper
names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_DOTTED_HOLE_SAPPHIRE_THEFT_V3_64"
REL = Path("data/maps/SixIsland_DottedHole_SapphireRoom_Frlg/scripts.inc")

PATCHES = {
    "SixIsland_DottedHole_SapphireRoom_Text_FoundSapphire": {
        "needles": ("{PLAYER} found a SAPPHIRE!",),
        "ru": '''SixIsland_DottedHole_SapphireRoom_Text_FoundSapphire::
\t.string "{PLAYER} нашел САПФИР!$"
''',
    },
    "SixIsland_DottedHole_SapphireRoom_Text_IWasRightInTailingYou": {
        "needles": ("I guessed right", "I was right in tailing you"),
        "ru": '''SixIsland_DottedHole_SapphireRoom_Text_IWasRightInTailingYou::
\t.string "Фуфу... Фуфуфу...\\n"
\t.string "Я не ошибся.\\p"
\t.string "Не зря я шёл за тобой!$"
''',
    },
    "SixIsland_DottedHole_SapphireRoom_Text_SellToTeamRocketTellPassword": {
        "needles": ("there was a SAPPHIRE", "sell it to TEAM ROCKET", "WAREHOUSE password I know", "Yes, nah, CHANSEY"),
        "ru": '''SixIsland_DottedHole_SapphireRoom_Text_SellToTeamRocketTellPassword::
\t.string "Я знал, что здесь есть САПФИР,\\n"
\t.string "так что теперь он мой!\\p"
\t.string "Продам его КОМАНДЕ ROCKET\\n"
\t.string "за большие деньги.\\p"
\t.string "...Н-не смотри на меня так!\\p"
\t.string "Хочешь вернуть его - забери,\\n"
\t.string "когда я его продам.\\p"
\t.string "Я даже скажу один пароль от\\n"
\t.string "СКЛАДА КОМАНДЫ ROCKET.\\p"
\t.string "Пароль, который я знаю:\\n"
\t.string "“Да, нет, CHANSEY”.\\p"
\t.string "Всё. Не держи на меня зла!$"
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
        raise SystemExit("usage: localize_dotted_hole_sapphire_theft_v3_64.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_dotted_hole_sapphire_theft_v3_64_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Six Island Dotted Hole Sapphire pickup/theft/password scene",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} forced Dotted Hole Sapphire theft blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
