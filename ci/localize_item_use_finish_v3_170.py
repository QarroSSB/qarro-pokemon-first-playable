#!/usr/bin/env python3
"""Qarro v3.170: finish the 13 audited English candidates in src/item_use.c.

Prepared from the fresh audit chain after v3.169. Text-only, fail-closed exact
symbol anchors; existing earlier translations in this file are intentionally
left untouched. Gameplay/item effects, inventory, battle logic, Ash Bond and
Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ITEM_USE_FINISH_V3_170"
REL = Path("src/item_use.c")
PINNED_UPSTREAM = "e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7"

TRANSLATIONS = {
    "sText_CantDismountBike": (
        "You can't dismount your BIKE here.{PAUSE_UNTIL_PRESS}",
        "Здесь нельзя слезть с ВЕЛОСИПЕДА.{PAUSE_UNTIL_PRESS}",
    ),
    "sText_ItemFinderOnTop": (
        "Oh!\\nThe ITEMFINDER's shaking wildly!{PAUSE_UNTIL_PRESS}",
        "О!\\nITEMFINDER сильно трясётся!{PAUSE_UNTIL_PRESS}",
    ),
    "sText_ItemFinderNothing": (
        "… … … …Nope!\\nThere's no response.{PAUSE_UNTIL_PRESS}",
        "… … … …Нет!\\nНет сигнала.{PAUSE_UNTIL_PRESS}",
    ),
    "sText_CoinCase": (
        "Your COINS:\\n{STR_VAR_1}{PAUSE_UNTIL_PRESS}",
        "МОНЕТЫ:\\n{STR_VAR_1}{PAUSE_UNTIL_PRESS}",
    ),
    "sText_PowderQty": (
        "POWDER QTY: {STR_VAR_1}{PAUSE_UNTIL_PRESS}",
        "ПОРОШОК: {STR_VAR_1}{PAUSE_UNTIL_PRESS}",
    ),
    "sText_BootedUpTM": ("Booted up a TM.", "Открыт TM."),
    "sText_BootedUpHM": ("Booted up an HM.", "Открыт HM."),
    "sText_TMHMContainedVar1": (
        "It contained\\n{STR_VAR_1}.\\pTeach {STR_VAR_1}\\nto a POKéMON?",
        "Внутри было\\n{STR_VAR_1}.\\pОбучить {STR_VAR_1}\\nПОКЕМОНА?",
    ),
    "sText_UsedVar2WildLured": (
        "{PLAYER} used the\\n{STR_VAR_2}.\\pWild POKéMON will be lured.{PAUSE_UNTIL_PRESS}",
        "{PLAYER} использует\\n{STR_VAR_2}.\\pДикие ПОКЕМОНЫ будут приманены.{PAUSE_UNTIL_PRESS}",
    ),
    "sText_UsedVar2WildRepelled": (
        "{PLAYER} used the\\n{STR_VAR_2}.\\pWild POKéMON will be repelled.{PAUSE_UNTIL_PRESS}",
        "{PLAYER} использует\\n{STR_VAR_2}.\\pДикие ПОКЕМОНЫ будут отпугнуты.{PAUSE_UNTIL_PRESS}",
    ),
    "sText_PlayedPokeFlute": (
        "Played the POKé FLUTE.",
        "Сыграна мелодия на POKé FLUTE.",
    ),
    "sText_PokeFluteAwakenedMon": (
        "The POKé FLUTE awakened sleeping\\nPOKéMON.{PAUSE_UNTIL_PRESS}",
        "POKé FLUTE разбудила спящих\\nПОКЕМОНОВ.{PAUSE_UNTIL_PRESS}",
    ),
    "sText_CantThrowPokeBall_Disabled": (
        "POKé BALLS cannot be used\\nright now!\\p",
        "Сейчас нельзя использовать\\nПОКЕБОЛЫ!\\p",
    ),
}

TOKEN_RE = re.compile(r"\\[npl]|\$|\{[^{}]+\}")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_item_use_finish_v3_170.py <upstream-root>")

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    translated = []

    for symbol, (old, new) in TRANSLATIONS.items():
        if TOKEN_RE.findall(old) != TOKEN_RE.findall(new):
            raise RuntimeError(
                f"FireRed control/brace token mismatch for {symbol}: "
                f"{TOKEN_RE.findall(old)!r} != {TOKEN_RE.findall(new)!r}"
            )
        pat = re.compile(
            rf'(?m)^(?P<prefix>\s*static const u8 {re.escape(symbol)}\[\]\s*=\s*_\(")'
            rf'{re.escape(old)}'
            rf'(?P<suffix>"\);\s*)$'
        )
        matches = list(pat.finditer(text))
        if len(matches) != 1:
            raise RuntimeError(f"expected exactly one pinned anchor for {symbol}; found {len(matches)}")
        match = matches[0]
        text = text[:match.start()] + match.group("prefix") + new + match.group("suffix") + text[match.end():]
        translated.append({"key": symbol, "old": old, "new": new})

    if len(TRANSLATIONS) != 13 or len(translated) != 13:
        raise RuntimeError(f"v3.170 scope drift: expected 13 replacements, got {len(translated)}")

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_item_use_finish_v3_170_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "pinnedUpstream": PINNED_UPSTREAM,
        "translated": translated,
        "translatedCount": len(translated),
        "scope": "all 13 audited English candidates in src/item_use.c after v3.169",
        "expectedRemainingCandidatesInFile": 0,
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: translated {len(translated)} item-use strings; "
        "expected file candidate count 13->0; gameplay/logic/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
