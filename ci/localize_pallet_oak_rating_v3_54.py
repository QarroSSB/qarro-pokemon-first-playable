#!/usr/bin/env python3
"""Qarro v3.54 mandatory Pallet Town Oak Pokédex-rating localization.

Translates only the verified forced Oak rating scene that fires in Pallet Town
post-Elite Four after the initial Sevii trip: Oak checks the player's Pokédex,
handles the reachable <60 caught branch, and leads the player to his lab when
the National Dex threshold is met. Later lab/National Dex dialogue and optional
NPC text remain untouched. Pokemon species / move / ability proper names remain
English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_PALLET_OAK_RATING_V3_54"
REL = Path("data/maps/PalletTown_Frlg/scripts.inc")

PATCHES = {
    "PalletTown_Text_OakLetMeSeePokedex": {
        "needles": ("OAK: Ah, {PLAYER}!", "May I see it?", "Let's see"),
        "ru": '''PalletTown_Text_OakLetMeSeePokedex::
\t.string "OAK: А, {PLAYER}!\\n"
\t.string "Ты вернулся?\\p"
\t.string "Насколько ты заполнил свой\\n"
\t.string "POKeDEX?\\p"
\t.string "Можно взглянуть?\\p"
\t.string "Посмотрим…$"
''',
    },
    "PalletTown_Text_CaughtXPuttingInHonestEffort": {
        "needles": ("You've caught {STR_VAR_2}", "honest effort", "come show me"),
        "ru": '''PalletTown_Text_CaughtXPuttingInHonestEffort::
\t.string "Ты поймал {STR_VAR_2}…\\p"
\t.string "Хм, вижу, ты действительно\\n"
\t.string "стараешься.\\p"
\t.string "Когда заполнишь его ещё немного,\\n"
\t.string "покажи мне снова.$"
''',
    },
    "PalletTown_Text_CaughtXImpressiveFollowMe": {
        "needles": ("You've caught", "this is impressive", "wanted to ask"),
        "ru": '''PalletTown_Text_CaughtXImpressiveFollowMe::
\t.string "Ты поймал… {STR_VAR_2}!?\\n"
\t.string "Вот это впечатляет!\\p"
\t.string "Я хотел кое о чём тебя попросить.\\n"
\t.string "Иди за мной.$"
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
    if any(needle not in block for needle in needles):
        missing = [needle for needle in needles if needle not in block]
        raise SystemExit(f"{MARKER}: {label}: pinned evidence mismatch; missing {missing}")
    if re.search(r"[А-Яа-яЁё]", block):
        raise SystemExit(f"{MARKER}: {label}: block is already localized or unexpectedly contains Cyrillic")
    return text[:start] + replacement + "\n" + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pallet_oak_rating_v3_54.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_pallet_oak_rating_v3_54_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory post-Elite Four Pallet Town Oak Pokédex rating and reachable threshold branch",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Pallet Town Oak rating blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
