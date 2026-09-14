#!/usr/bin/env python3
"""Qarro v3.61 mandatory Four Island rival arrival localization.

Translates only the forced Rival scene shown on the player's first arrival on
Four Island after the Rainbow Pass opens the remaining Sevii Islands. Day Care,
Lorelei, optional NPC text, Sapphire progression, Ash Bond, and Ash Cap remain
untouched. Pokemon species / move / ability proper names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FOUR_ISLAND_RIVAL_ARRIVAL_V3_61"
REL = Path("data/maps/FourIsland_Frlg/scripts.inc")
LABEL = "FourIsland_Text_RivalAlreadyGotEggBeSmellingYa"
NEEDLES = (
    "What are you doing here in the",
    "SEVII ISLANDS",
    "already got my POKéMON",
    "NATIONAL",
    "POKéDEX",
    "someone we both",
    "Be smelling ya!",
)
RU = '''FourIsland_Text_RivalAlreadyGotEggBeSmellingYa::
\t.string "{RIVAL}: Эй!\\n"
\t.string "{PLAYER}!\\p"
\t.string "Что ты делаешь здесь, на\\n"
\t.string "островах СЕВИИ?\\p"
\t.string "Хватит уже всё за мной\\n"
\t.string "повторять!\\p"
\t.string "В общем, я уже получил ЯЙЦО\\n"
\t.string "ПОКЕМОНА и закончил с островом.\\p"
\t.string "Хех, спорю, ты даже не знаешь\\n"
\t.string "про ЯЙЦА ПОКЕМОНОВ.\\p"
\t.string "Так НАЦИОНАЛЬНЫЙ ПОКЕДЕКС\\n"
\t.string "ты никогда не заполнишь.\\p"
\t.string "Кстати, я видел здесь кое-кого,\\n"
\t.string "кого мы оба знаем.\\p"
\t.string "Если интересно - пойди\\n"
\t.string "и поищи вокруг.\\p"
\t.string "А у меня нет времени\\n"
\t.string "здесь торчать.\\p"
\t.string "Ещё увидимся!$"
'''
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\\s*$")


def replace_label_block(text: str) -> str:
    matches = list(re.finditer(rf"(?m)^{re.escape(LABEL)}::\\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {LABEL}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    block = text[start:end]
    missing = [needle for needle in NEEDLES if needle not in block]
    if missing:
        raise SystemExit(f"{MARKER}: {LABEL}: pinned evidence mismatch; missing {missing}")
    if re.search(r"[А-Яа-яЁё]", block):
        raise SystemExit(f"{MARKER}: {LABEL}: block is already localized or unexpectedly contains Cyrillic")
    return text[:start] + RU + "\n" + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_four_island_rival_arrival_v3_61.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    text = replace_label_block(text)
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_four_island_rival_arrival_v3_61_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": [LABEL],
        "translatedBlockCount": 1,
        "scope": "mandatory first-arrival Four Island Rival scene",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated forced Four Island Rival arrival scene; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
