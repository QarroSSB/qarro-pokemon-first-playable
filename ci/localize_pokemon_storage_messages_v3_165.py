#!/usr/bin/env python3
"""Qarro v3.165: localize a safe Pokémon Storage runtime-message subset.

Targets ten short MSG_VAR_NONE strings in src/pokemon_storage_system.c that
remain English after FULL GREEN v3.164 / RU audit #315. Every replacement is
anchored to its exact MSG_* key and pinned English source text. Text-only pass:
no gameplay, trainer, reward, inventory, flag, progression, Ash Bond or Ash Cap
logic is touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_PSS_MESSAGES_V3_165"
REL = Path("src/pokemon_storage_system.c")
PINNED_UPSTREAM = "e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7"

TRANSLATIONS = {
    "MSG_EXIT_BOX": ("Exit from the BOX?", "Выйти из БОКСА?"),
    "MSG_WHAT_YOU_DO": ("What do you want to do?", "Что хочешь сделать?"),
    "MSG_PICK_A_THEME": ("Please pick a theme.", "Выбери тему."),
    "MSG_PICK_A_WALLPAPER": ("Pick the wallpaper.", "Выбери обои."),
    "MSG_JUMP_TO_WHICH_BOX": ("Jump to which BOX?", "К какому БОКСУ перейти?"),
    "MSG_DEPOSIT_IN_WHICH_BOX": ("Deposit in which BOX?", "В какой БОКС убрать?"),
    "MSG_BOX_IS_FULL": ("The BOX is full.", "БОКС заполнен."),
    "MSG_RELEASE_POKE": ("Release this POKéMON?", "Отпустить этого ПОКЕМОНА?"),
    "MSG_MARK_POKE": ("Mark your POKéMON.", "Отметь своего ПОКЕМОНА."),
    "MSG_LAST_POKE": ("That's your last POKéMON!", "Это твой последний ПОКЕМОН!"),
}

TOKEN_RE = re.compile(r"\\[npl]|\$|\{[^{}]+\}")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_storage_messages_v3_165.py <upstream-root>")

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
            rf'(?m)^(?P<prefix>\s*\[{re.escape(key)}\]\s*=\s*\{{COMPOUND_STRING\(")'
            rf'{re.escape(old)}'
            rf'(?P<suffix>"\),\s*MSG_VAR_NONE\}},\s*)$'
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

    out = root / "build" / "qarro_ru_pss_messages_v3_165_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "pinnedUpstream": PINNED_UPSTREAM,
        "translated": translated,
        "translatedCount": len(translated),
        "scope": "ten Pokemon Storage MSG_VAR_NONE runtime messages only",
        "policy": "Pokemon/Move/Ability proper names English; descriptions/UI/dialogue/system text Russian",
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: translated {len(translated)} Pokémon Storage runtime messages; "
        "gameplay/logic/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
