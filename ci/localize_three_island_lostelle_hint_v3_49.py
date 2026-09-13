#!/usr/bin/env python3
"""Qarro v3.49 mandatory Three Island Lostelle/Bond Bridge hint localization.

Translates only the verified post-biker progression hint given by the island
defender after VAR_MAP_SCENE_THREE_ISLAND reaches 4. Optional reward/NPC text and
later Sevii postgame text remain untouched. Pokemon species / move / ability
proper names remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_THREE_ISLAND_LOSTELLE_HINT_V3_49"
REL = Path("data/maps/ThreeIsland_Frlg/scripts.inc")

PINNED = '''ThreeIsland_Text_LostelleWentOffTowardsBondBridge::
\t.string "It'd be fantastic if someone as\\n"
\t.string "strong as you lived here.\\p"
\t.string "I hope you'll at least stay here\\n"
\t.string "a while.\\p"
\t.string "…I beg your pardon?\\n"
\t.string "You're looking for LOSTELLE?\\p"
\t.string "LOSTELLE went off towards BOND\\n"
\t.string "BRIDGE a while ago.$"
'''

RU = '''ThreeIsland_Text_LostelleWentOffTowardsBondBridge::
\t.string "Было бы здорово, если бы такой\\n"
\t.string "сильный тренер жил здесь.\\p"
\t.string "Надеюсь, ты хотя бы ненадолго\\n"
\t.string "останешься у нас.\\p"
\t.string "…Прошу прощения?\\n"
\t.string "Ты ищешь LOSTELLE?\\p"
\t.string "LOSTELLE недавно ушла в сторону\\n"
\t.string "BOND BRIDGE.$"
'''


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_three_island_lostelle_hint_v3_49.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")

    variants = [PINNED]
    normalized = PINNED.replace("é", "e").replace("É", "E")
    if normalized != PINNED:
        variants.append(normalized)
    hits = [(variant, text.count(variant)) for variant in variants]
    total = sum(count for _, count in hits)
    if total != 1:
        raise SystemExit(f"{MARKER}: expected exactly one pinned/normalized anchor, found {total}")
    source = next(variant for variant, count in hits if count == 1)
    text = text.replace(source, RU, 1)
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_three_island_lostelle_hint_v3_49_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": ["ThreeIsland_Text_LostelleWentOffTowardsBondBridge"],
        "translatedBlockCount": 1,
        "scope": "mandatory post-biker Lostelle to Bond Bridge progression hint",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated mandatory Lostelle/Bond Bridge hint; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
