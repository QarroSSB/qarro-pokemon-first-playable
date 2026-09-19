#!/usr/bin/env python3
"""Qarro v3.167: localize the next safe Pokémon Storage message subset.

Targets ten short MSG_VAR_NONE strings in src/pokemon_storage_system.c that
remain English after FULL GREEN v3.166 / RU audit #321. Every replacement is
anchored to its exact MSG_* key and pinned English source text. Text-only pass:
no gameplay, trainer, reward, inventory, flag, progression, Ash Bond or Ash Cap
logic is touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_PSS_MESSAGES_V3_167"
REL = Path("src/pokemon_storage_system.c")
PINNED_UPSTREAM = "e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7"

TRANSLATIONS = {
    "MSG_HOLDING_POKE": ("You're holding a POKeMON!", "Ты держишь ПОКЕМОНА!"),
    "MSG_WHICH_ONE_WILL_TAKE": ("Which one will you take?", "Кого ты возьмёшь?"),
    "MSG_CANT_RELEASE_EGG": ("You can't release an EGG.", "Нельзя отпустить ЯЙЦО."),
    "MSG_CONTINUE_BOX": ("Continue BOX operations?", "Продолжить работу с БОКСОМ?"),
    "MSG_WORRIED": ("Was it worried about you?", "Он переживал за тебя?"),
    "MSG_PLEASE_REMOVE_MAIL": ("Please remove the MAIL.", "Убери ПОЧТУ."),
    "MSG_GIVE_TO_MON": ("GIVE to a POKeMON?", "ДАТЬ ПОКЕМОНУ?"),
    "MSG_BAG_FULL": ("The BAG is full.", "СУМКА заполнена."),
    "MSG_PUT_IN_BAG": ("Put this item in the BAG?", "Положить предмет в СУМКУ?"),
    "MSG_CANT_STORE_MAIL": ("MAIL can't be stored!", "ПОЧТУ нельзя хранить!"),
}

TOKEN_RE = re.compile(r"\\[npl]|\$|\{[^{}]+\}")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_storage_messages_v3_167.py <upstream-root>")

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    translated = []

    for key, (old, new) in TRANSLATIONS.items():
        if TOKEN_RE.findall(old) != TOKEN_RE.findall(new):
            raise RuntimeError(
                f"FireRed control/brace token mismatch for {key}: "
                f"{TOKEN_RE.findall(old)!r} != {TOKEN_RE.findall(new)!r}"
            )
        pat = re.compile(
            rf'(?m)^(?P<prefix>\\s*\\[{re.escape(key)}\\]\\s*=\\s*\\{{COMPOUND_STRING\\(")'
            rf'{re.escape(old)}'
            rf'(?P<suffix>"\\),\\s*MSG_VAR_NONE\\}},\\s*)$'
        )
        matches = list(pat.finditer(text))
        if len(matches) != 1:
            raise RuntimeError(
                f"expected exactly one pinned MSG_VAR_NONE anchor for {key}; found {len(matches)}"
            )
        match = matches[0]
        text = (
            text[:match.start()]
            + match.group("prefix")
            + new
            + match.group("suffix")
            + text[match.end():]
        )
        translated.append({"key": key, "old": old, "new": new})

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_pss_messages_v3_167_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "pinnedUpstream": PINNED_UPSTREAM,
        "translated": translated,
        "translatedCount": len(translated),
        "scope": "ten additional Pokemon Storage MSG_VAR_NONE runtime messages only",
        "policy": "Pokemon/Move/Ability proper names English; descriptions/UI/dialogue/system text Russian",
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: translated {len(translated)} additional Pokémon Storage runtime messages; "
        "gameplay/logic/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
