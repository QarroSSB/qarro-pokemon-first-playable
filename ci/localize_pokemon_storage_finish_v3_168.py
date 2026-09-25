#!/usr/bin/env python3
"""Qarro v3.168: finish the remaining audited Pokémon Storage English UI.

Fresh FULL GREEN v3.167 / RU audit #326 reports exactly 50 broader English
candidates in src/pokemon_storage_system.c. This pass targets those 50 as one
homogeneous text-only block: five global labels/messages, seven dynamic storage
messages, and 38 direct menu/wallpaper labels. Every replacement is fail-closed
on an exact symbol/key plus pinned English source text. Gameplay, trainer data,
rewards, flags, progression, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_PSS_FINISH_V3_168"
REL = Path("src/pokemon_storage_system.c")
PINNED_UPSTREAM = "e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7"

GLOBALS = {
    "gText_JustOnePkmn": ("There is just one POKéMON with you.", "С тобой только один ПОКЕМОН."),
    "gText_PartyFull": ("Your party is full!", "Твоя команда заполнена!"),
    "gText_Box": ("BOX", "БОКС"),
    "gText_PkmnIsSelected": ("{DYNAMIC 0} is selected.", "{DYNAMIC 0} выбран."),
    "gPCText_Give": ("GIVE", "ДАТЬ"),
}

MESSAGES = {
    "MSG_WAS_DEPOSITED": ("{DYNAMIC 0} was deposited.", "{DYNAMIC 0} отправлен в БОКС."),
    "MSG_WAS_RELEASED": ("{DYNAMIC 0} was released.", "{DYNAMIC 0} отпущен."),
    "MSG_BYE_BYE": ("Bye-bye, {DYNAMIC 0}!", "Прощай, {DYNAMIC 0}!"),
    "MSG_CAME_BACK": ("{DYNAMIC 0} came back!", "{DYNAMIC 0} вернулся!"),
    "MSG_PLACED_IN_BAG": ("Placed item in the BAG.", "Предмет убран в СУМКУ."),
    "MSG_ITEM_IS_HELD": ("{DYNAMIC 0} is now held.", "Теперь держит {DYNAMIC 0}."),
    "MSG_CHANGED_TO_ITEM": ("Changed to {DYNAMIC 0}.", "Сменено на {DYNAMIC 0}."),
}

MENUS = {
    "MENU_CANCEL": ("CANCEL", "ОТМЕНА"),
    "MENU_STORE": ("STORE", "УБРАТЬ"),
    "MENU_WITHDRAW": ("WITHDRAW", "ЗАБРАТЬ"),
    "MENU_MOVE": ("MOVE", "ДВИГАТЬ"),
    "MENU_SHIFT": ("SHIFT", "СДВИНУТЬ"),
    "MENU_PLACE": ("PLACE", "ПОЛОЖИТЬ"),
    "MENU_SUMMARY": ("SUMMARY", "СВОДКА"),
    "MENU_RELEASE": ("RELEASE", "ОТПУСТИТЬ"),
    "MENU_MARK": ("MARK", "МЕТКА"),
    "MENU_JUMP": ("JUMP", "ПЕРЕЙТИ"),
    "MENU_WALLPAPER": ("WALLPAPER", "ОБОИ"),
    "MENU_NAME": ("NAME", "ИМЯ"),
    "MENU_TAKE": ("TAKE", "ВЗЯТЬ"),
    "MENU_SWITCH": ("SWITCH", "СМЕНИТЬ"),
    "MENU_BAG": ("BAG", "СУМКА"),
    "MENU_INFO": ("INFO", "ИНФО"),
    "MENU_SCENERY_1": ("SCENERY 1", "ПЕЙЗАЖ 1"),
    "MENU_SCENERY_2": ("SCENERY 2", "ПЕЙЗАЖ 2"),
    "MENU_SCENERY_3": ("SCENERY 3", "ПЕЙЗАЖ 3"),
    "MENU_ETCETERA": ("ETCETERA", "ПРОЧЕЕ"),
    "MENU_FRIENDS": ("FRIENDS", "ДРУЗЬЯ"),
    "MENU_FOREST": ("FOREST", "ЛЕС"),
    "MENU_CITY": ("CITY", "ГОРОД"),
    "MENU_DESERT": ("DESERT", "ПУСТЫНЯ"),
    "MENU_SAVANNA": ("SAVANNA", "САВАННА"),
    "MENU_CRAG": ("CRAG", "СКАЛЫ"),
    "MENU_VOLCANO": ("VOLCANO", "ВУЛКАН"),
    "MENU_SNOW": ("SNOW", "СНЕГ"),
    "MENU_CAVE": ("CAVE", "ПЕЩЕРА"),
    "MENU_BEACH": ("BEACH", "ПЛЯЖ"),
    "MENU_SEAFLOOR": ("SEAFLOOR", "ДНО МОРЯ"),
    "MENU_RIVER": ("RIVER", "РЕКА"),
    "MENU_SKY": ("SKY", "НЕБО"),
    "MENU_POLKADOT": ("POLKA-DOT", "ГОРОШЕК"),
    "MENU_POKECENTER": ("POKéCENTER", "ПОКЕЦЕНТР"),
    "MENU_MACHINE": ("MACHINE", "МЕХАНИЗМ"),
    "MENU_SIMPLE": ("SIMPLE", "ПРОСТО"),
    "MENU_SELECT": ("SELECT", "ВЫБРАТЬ"),
}

TOKEN_RE = re.compile(r"\\[npl]|\$|\{[^{}]+\}")


def check_tokens(label: str, old: str, new: str) -> None:
    if TOKEN_RE.findall(old) != TOKEN_RE.findall(new):
        raise RuntimeError(
            f"FireRed control/brace token mismatch for {label}: "
            f"{TOKEN_RE.findall(old)!r} != {TOKEN_RE.findall(new)!r}"
        )


def replace_one(text: str, pattern: re.Pattern[str], label: str, old: str, new: str) -> str:
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one pinned anchor for {label}; found {len(matches)}")
    match = matches[0]
    return text[:match.start()] + match.group("prefix") + new + match.group("suffix") + text[match.end():]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_storage_finish_v3_168.py <upstream-root>")

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    translated = []

    for symbol, (old, new) in GLOBALS.items():
        check_tokens(symbol, old, new)
        pat = re.compile(
            rf'(?m)^(?P<prefix>\s*static const u8 {re.escape(symbol)}\[\]\s*=\s*_\(")'
            rf'{re.escape(old)}'
            rf'(?P<suffix>"\);\s*)$'
        )
        text = replace_one(text, pat, symbol, old, new)
        translated.append({"kind": "global", "key": symbol, "old": old, "new": new})

    for key, (old, new) in MESSAGES.items():
        check_tokens(key, old, new)
        pat = re.compile(
            rf'(?m)^(?P<prefix>\s*\[{re.escape(key)}\]\s*=\s*\{{COMPOUND_STRING\(")'
            rf'{re.escape(old)}'
            rf'(?P<suffix>"\),\s*MSG_VAR_[A-Z0-9_]+\}},\s*)$'
        )
        text = replace_one(text, pat, key, old, new)
        translated.append({"kind": "message", "key": key, "old": old, "new": new})

    for key, (old, new) in MENUS.items():
        check_tokens(key, old, new)
        pat = re.compile(
            rf'(?m)^(?P<prefix>\s*\[{re.escape(key)}\]\s*=\s*COMPOUND_STRING\(")'
            rf'{re.escape(old)}'
            rf'(?P<suffix>"\),\s*)$'
        )
        text = replace_one(text, pat, key, old, new)
        translated.append({"kind": "menu", "key": key, "old": old, "new": new})

    expected = len(GLOBALS) + len(MESSAGES) + len(MENUS)
    if expected != 50 or len(translated) != 50:
        raise RuntimeError(f"v3.168 scope drift: expected 50 replacements, got {len(translated)}")

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_pss_finish_v3_168_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "pinnedUpstream": PINNED_UPSTREAM,
        "translated": translated,
        "translatedCount": len(translated),
        "scope": "all 50 remaining audited Pokemon Storage English UI candidates after v3.167",
        "expectedRemainingCandidatesInFile": 0,
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: translated {len(translated)} remaining Pokémon Storage UI strings; "
        "expected file candidate count 50->0; gameplay/logic/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
