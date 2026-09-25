#!/usr/bin/env python3
"""Qarro v3.51 mandatory Two Island Lostelle return localization.

Translates only the verified forced post-rescue scene that runs when the player
returns with Lostelle to the Joyful Game Corner: her father's thanks and
Lostelle's reply. Meteorite handoff, Moon Stone reward, optional NPC/game-corner
text, and later Sevii postgame remain untouched by this pass. Pokemon species /
move / ability proper names remain English. Ash Bond / Ash Cap are not
referenced or changed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_TWO_ISLAND_LOSTELLE_RETURN_V3_51"
REL = Path("data/maps/TwoIsland_JoyfulGameCorner_Frlg/scripts.inc")

PATCHES = {
    "TwoIsland_JoyfulGameCorner_Text_YouRescuedLostelle": (
        '''TwoIsland_JoyfulGameCorner_Text_YouRescuedLostelle::
\t.string "So you rescued LOSTELLE?\\n"
\t.string "How can I thank you?\\p"
\t.string "LOSTELLE, darling, forgive me!\\p"
\t.string "Daddy didn't know you were scared\\n"
\t.string "and in trouble!$"
''',
        '''TwoIsland_JoyfulGameCorner_Text_YouRescuedLostelle::
\t.string "Так это ты спас LOSTELLE?\\n"
\t.string "Как мне тебя отблагодарить?\\p"
\t.string "LOSTELLE, милая, прости меня!\\p"
\t.string "Папа не знал, что тебе было страшно\\n"
\t.string "и ты попала в беду!$"
''',
    ),
    "TwoIsland_JoyfulGameCorner_Text_LostelleItsOkayDaddy": (
        '''TwoIsland_JoyfulGameCorner_Text_LostelleItsOkayDaddy::
\t.string "LOSTELLE: It's okay, Daddy.\\n"
\t.string "I got to be friends with {PLAYER}!$"
''',
        '''TwoIsland_JoyfulGameCorner_Text_LostelleItsOkayDaddy::
\t.string "LOSTELLE: Всё хорошо, папа.\\n"
\t.string "Мы с {PLAYER} теперь друзья!$"
''',
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_two_island_lostelle_return_v3_51.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied = []

    for label, (pinned, ru) in PATCHES.items():
        variants = [pinned]
        normalized = pinned.replace("é", "e").replace("É", "E")
        if normalized != pinned:
            variants.append(normalized)
        hits = [(variant, text.count(variant)) for variant in variants]
        total = sum(count for _, count in hits)
        if total != 1:
            raise SystemExit(f"{MARKER}: {label}: expected exactly one pinned/normalized anchor, found {total}")
        source = next(variant for variant, count in hits if count == 1)
        text = text.replace(source, ru, 1)
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_two_island_lostelle_return_v3_51_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory forced Two Island post-rescue Lostelle return scene",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} forced Two Island Lostelle return blocks; Ash Bond/Ash Cap untouched")

    meteorite_script = Path(__file__).with_name("localize_two_island_meteorite_handoff_v3_52.py")
    subprocess.run([sys.executable, str(meteorite_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
