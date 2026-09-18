#!/usr/bin/env python3
"""Qarro v3.163: localize the remaining audited FireRed Pokédex order descriptions.

Targets five English-only Pokédex runtime descriptions confirmed by RU runtime
surface audit #313 on the f29f598a GREEN checkpoint and verified against pinned
upstream e8bd1cd7. Text-only pass: no gameplay, trainer, reward, inventory,
flag, progression, Ash Bond or Ash Cap logic is touched. Pokemon/Move/Ability
proper names remain English by policy.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEDEX_ORDER_RESIDUAL_V3_163"
REL = Path("src/pokedex.c")
REPLACEMENTS = [
    (
        "Spotted and owned POKéMON are listed\\nalphabetically.",
        "Замеченные и пойманные ПОКЕМОНЫ\\nперечислены по алфавиту.",
    ),
    (
        "Owned POKéMON are listed from the\\nheaviest to the lightest.",
        "Пойманные ПОКЕМОНЫ: от самых\\nтяжелых к самым легким.",
    ),
    (
        "Owned POKéMON are listed from the\\nlightest to the heaviest.",
        "Пойманные ПОКЕМОНЫ: от самых\\nлегких к самым тяжелым.",
    ),
    (
        "Owned POKéMON are listed from the\\ntallest to the smallest.",
        "Пойманные ПОКЕМОНЫ: от самых\\nвысоких к самым низким.",
    ),
    (
        "Owned POKéMON are listed from the\\nsmallest to the tallest.",
        "Пойманные ПОКЕМОНЫ: от самых\\nнизких к самым высоким.",
    ),
]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokedex_order_residual_v3_163.py <upstream-root>")

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied = []

    for old, new in REPLACEMENTS:
        old_expr = f'COMPOUND_STRING("{old}")'
        new_expr = f'COMPOUND_STRING("{new}")'
        count = text.count(old_expr)
        if count != 1:
            raise RuntimeError(
                f"expected exactly one pinned Pokédex order anchor; found {count}: {old!r}"
            )
        text = text.replace(old_expr, new_expr, 1)
        applied.append({"old": old, "new": new})

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_pokedex_order_residual_v3_163_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translated": applied,
        "translatedCount": len(applied),
        "policy": "Pokemon/Move/Ability proper names English; descriptions/UI/dialogue/system text Russian",
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: translated {len(applied)} Pokédex order descriptions; "
        "gameplay/logic/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
