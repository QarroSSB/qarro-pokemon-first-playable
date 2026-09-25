#!/usr/bin/env python3
"""Qarro v3.164: localize the FireRed Pokémon Storage main-menu surface.

Targets the five main-menu labels and five paired descriptions in
src/pokemon_storage_system.c, confirmed English-only in RU runtime surface
audit #314 on the FULL GREEN 5313457a checkpoint and verified against pinned
upstream e8bd1cd7. Text-only pass: no gameplay, trainer, reward, inventory,
flag, progression, Ash Bond or Ash Cap logic is touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_PSS_MAIN_MENU_V3_164"
REL = Path("src/pokemon_storage_system.c")
PINNED_UPSTREAM = "e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7"

OLD_BLOCK = r'''    [OPTION_WITHDRAW]   = {COMPOUND_STRING("WITHDRAW POKéMON"), COMPOUND_STRING("Move POKéMON stored in BOXES to\nyour party.")},
    [OPTION_DEPOSIT]    = {COMPOUND_STRING("DEPOSIT POKéMON"),  COMPOUND_STRING("Store POKéMON in your party in BOXES.")},
    [OPTION_MOVE_MONS]  = {COMPOUND_STRING("MOVE POKéMON"),     COMPOUND_STRING("Organize the POKéMON in BOXES and\nin your party.")},
    [OPTION_MOVE_ITEMS] = {COMPOUND_STRING("MOVE ITEMS"),       COMPOUND_STRING("Move items held by any POKéMON\nin a BOX or your party.")},
    [OPTION_EXIT]       = {COMPOUND_STRING("SEE YA!"),          COMPOUND_STRING("Return to the previous menu.")}
'''

NEW_BLOCK = r'''    [OPTION_WITHDRAW]   = {COMPOUND_STRING("ЗАБРАТЬ ПОКЕМОНА"), COMPOUND_STRING("Перенести ПОКЕМОНОВ из БОКСОВ\nв команду.")},
    [OPTION_DEPOSIT]    = {COMPOUND_STRING("УБРАТЬ ПОКЕМОНА"),  COMPOUND_STRING("Убрать ПОКЕМОНОВ из команды в БОКСЫ.")},
    [OPTION_MOVE_MONS]  = {COMPOUND_STRING("ДВИГАТЬ ПОКЕМОНА"), COMPOUND_STRING("Перемещать ПОКЕМОНОВ между\nБОКСАМИ и командой.")},
    [OPTION_MOVE_ITEMS] = {COMPOUND_STRING("ДВИГАТЬ ПРЕДМЕТЫ"), COMPOUND_STRING("Перемещать предметы у ПОКЕМОНОВ\nв БОКСАХ и команде.")},
    [OPTION_EXIT]       = {COMPOUND_STRING("ВЫХОД"),            COMPOUND_STRING("Вернуться в предыдущее меню.")}
'''

STRING_RE = re.compile(r'COMPOUND_STRING\("((?:\\.|[^"\\])*)"\)')
TOKEN_RE = re.compile(r"\\[npl]|\$|\{[^{}]+\}")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_storage_main_menu_v3_164.py <upstream-root>")

    old_strings = STRING_RE.findall(OLD_BLOCK)
    new_strings = STRING_RE.findall(NEW_BLOCK)
    if len(old_strings) != 10 or len(new_strings) != 10:
        raise RuntimeError(
            f"expected 10 old/new PSS strings; got {len(old_strings)}/{len(new_strings)}"
        )
    for index, (old, new) in enumerate(zip(old_strings, new_strings), start=1):
        if TOKEN_RE.findall(old) != TOKEN_RE.findall(new):
            raise RuntimeError(
                f"FireRed control/brace token mismatch in PSS string {index}: "
                f"{TOKEN_RE.findall(old)!r} != {TOKEN_RE.findall(new)!r}"
            )

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    count = text.count(OLD_BLOCK)
    if count != 1:
        raise RuntimeError(
            f"expected exactly one pinned Pokémon Storage main-menu block; found {count}"
        )

    path.write_text(text.replace(OLD_BLOCK, NEW_BLOCK, 1), encoding="utf-8")

    translated = [
        {"old": old, "new": new}
        for old, new in zip(old_strings, new_strings)
    ]
    out = root / "build" / "qarro_ru_pss_main_menu_v3_164_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "pinnedUpstream": PINNED_UPSTREAM,
        "translated": translated,
        "translatedCount": len(translated),
        "scope": "Pokemon Storage main-menu labels/descriptions only",
        "policy": "Pokemon/Move/Ability proper names English; descriptions/UI/dialogue/system text Russian",
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: translated {len(translated)} Pokémon Storage main-menu strings; "
        "gameplay/logic/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
