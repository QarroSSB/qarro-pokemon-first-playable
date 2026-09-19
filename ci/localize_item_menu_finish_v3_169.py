#!/usr/bin/env python3
"""Qarro v3.169: finish the 22 audited English candidates in src/item_menu.c.

Selected from fresh FULL GREEN v3.168 / RU audit #327. Text-only pass with
fail-closed exact anchors. The duplicate local sText_NothingToSort definition is
required to occur exactly twice. Gameplay, item behavior, inventory logic,
rewards, flags, progression, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ITEM_MENU_FINISH_V3_169"
REL = Path("src/item_menu.c")
PINNED_UPSTREAM = "e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7"

GLOBALS = {
    "sText_Var1CantBeHeldHere": ("The {STR_VAR_1} can't be held\\nhere.", "{STR_VAR_1} нельзя держать\\nздесь."),
    "sText_DepositHowManyVar1": ("Deposit how many\\n{STR_VAR_1}?", "Сколько убрать\\n{STR_VAR_1}?"),
    "sText_DepositedVar2Var1s": ("Deposited {STR_VAR_2}\\n{STR_VAR_1}.", "Убрано {STR_VAR_2}\\n{STR_VAR_1}."),
    "sText_NoRoomForItems": ("There's no room to\\nstore items.", "Нет места для\\nхранения предметов."),
    "sText_CantStoreImportantItems": ("Important items\\ncan't be stored in\\nthe PC!", "Важные предметы\\nнельзя хранить\\nв ПК!"),
    "sText_SortItemsHow": ("Sort items how?", "Как сортировать?"),
    "sText_ItemsSorted": ("Items sorted by {STR_VAR_1}!", "Сортировка: {STR_VAR_1}!"),
}

ACTIONS = {
    "ACTION_CHECK": ("CHECK", "ОСМОТР"),
    "ACTION_WALK": ("WALK", "ИДТИ"),
    "ACTION_DESELECT": ("DESELECT", "СНЯТЬ"),
    "ACTION_CHECK_TAG": ("CHECK TAG", "ЯРЛЫК"),
    "ACTION_SHOW": ("SHOW", "ПОКАЗАТЬ"),
    "ACTION_BY_NAME": ("Name", "Имя"),
    "ACTION_BY_TYPE": ("Type", "Тип"),
    "ACTION_BY_AMOUNT": ("Amount", "Кол-во"),
    "ACTION_BY_INDEX": ("Index", "Номер"),
}

SORT_TYPES = {
    "SORT_ALPHABETICALLY": ("name", "имя"),
    "SORT_BY_TYPE": ("type", "тип"),
    "SORT_BY_AMOUNT": ("amount", "кол-во"),
    "SORT_BY_INDEX": ("index", "номер"),
}

DUPLICATE_NOTHING = ("There's nothing to sort!", "Нечего сортировать!")
TOKEN_RE = re.compile(r"\\[npl]|\$|\{[^{}]+\}")


def check_tokens(label: str, old: str, new: str) -> None:
    if TOKEN_RE.findall(old) != TOKEN_RE.findall(new):
        raise RuntimeError(
            f"FireRed control/brace token mismatch for {label}: "
            f"{TOKEN_RE.findall(old)!r} != {TOKEN_RE.findall(new)!r}"
        )


def replace_one(text: str, pattern: re.Pattern[str], label: str, new: str) -> str:
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one pinned anchor for {label}; found {len(matches)}")
    match = matches[0]
    return text[:match.start()] + match.group("prefix") + new + match.group("suffix") + text[match.end():]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_item_menu_finish_v3_169.py <upstream-root>")

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
        text = replace_one(text, pat, symbol, new)
        translated.append({"kind": "global", "key": symbol, "old": old, "new": new})

    old, new = DUPLICATE_NOTHING
    check_tokens("sText_NothingToSort", old, new)
    dup_pat = re.compile(
        rf'(?m)^(?P<prefix>\s*static const u8 sText_NothingToSort\[\]\s*=\s*_\(")'
        rf'{re.escape(old)}'
        rf'(?P<suffix>"\);\s*)$'
    )
    matches = list(dup_pat.finditer(text))
    if len(matches) != 2:
        raise RuntimeError(f"expected exactly two pinned sText_NothingToSort anchors; found {len(matches)}")
    text, count = dup_pat.subn(lambda m: m.group("prefix") + new + m.group("suffix"), text)
    if count != 2:
        raise RuntimeError(f"duplicate replacement drift: expected 2, got {count}")
    for occurrence in (1, 2):
        translated.append({"kind": "duplicate_global", "key": f"sText_NothingToSort#{occurrence}", "old": old, "new": new})

    for key, (old, new) in ACTIONS.items():
        check_tokens(key, old, new)
        pat = re.compile(
            rf'(?m)^(?P<prefix>\s*\[{re.escape(key)}\]\s*=\s*\{{COMPOUND_STRING\(")'
            rf'{re.escape(old)}'
            rf'(?P<suffix>"\),\s*\{{[A-Za-z0-9_]+\}}\}},\s*)$'
        )
        text = replace_one(text, pat, key, new)
        translated.append({"kind": "action", "key": key, "old": old, "new": new})

    for key, (old, new) in SORT_TYPES.items():
        check_tokens(key, old, new)
        pat = re.compile(
            rf'(?m)^(?P<prefix>\s*\[{re.escape(key)}\]\s*=\s*COMPOUND_STRING\(")'
            rf'{re.escape(old)}'
            rf'(?P<suffix>"\),?\s*)$'
        )
        text = replace_one(text, pat, key, new)
        translated.append({"kind": "sort_type", "key": key, "old": old, "new": new})

    expected = len(GLOBALS) + 2 + len(ACTIONS) + len(SORT_TYPES)
    if expected != 22 or len(translated) != 22:
        raise RuntimeError(f"v3.169 scope drift: expected 22 replacements, got {len(translated)}")

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_item_menu_finish_v3_169_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "pinnedUpstream": PINNED_UPSTREAM,
        "translated": translated,
        "translatedCount": len(translated),
        "scope": "all 22 audited English candidates in src/item_menu.c after v3.168",
        "expectedRemainingCandidatesInFile": 0,
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: translated {len(translated)} item-menu strings; "
        "expected file candidate count 22->0; gameplay/logic/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
