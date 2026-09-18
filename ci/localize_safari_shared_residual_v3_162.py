#!/usr/bin/env python3
"""Qarro v3.162: localize shared FireRed Safari Zone runtime messages.

Targets only the three shared Safari Zone messages proven reachable by the FRLG
branches in pinned upstream e8bd1cd7. Hoenn Route121/Pokeblock content is left
untouched. Text-only pass: no gameplay, reward, trainer, progression, Ash Bond
or Ash Cap logic is touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_SAFARI_SHARED_RESIDUAL_V3_162"
REL = Path("data/scripts/safari_zone.inc")
TRANSLATIONS = {
    "SafariZone_Text_WouldYouLikeToExit": (
        "Would you like to exit the SAFARI\\nZONE right now?$",
        "Хотите выйти из САФАРИ-ЗОНЫ\\nпрямо сейчас?$",
    ),
    "SafariZone_Text_TimesUp": (
        "Ding-dong! Time's up!\\nYour SAFARI Game is over.$",
        "Динь-дон! Время вышло!\\nИгра в САФАРИ окончена.$",
    ),
    "SafariZone_Text_OutOfBalls": (
        "You've run out of SAFARI BALLS.\\nYour SAFARI Game is over.$",
        "САФАРИ-БОЛЛЫ закончились.\\nИгра в САФАРИ окончена.$",
    ),
}
TOKEN_RE = re.compile(r"\\[npl]|\$")
STRING_RE = re.compile(r'^\s*\.string\s+"((?:\\.|[^"\\])*)"\s*$', re.M)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_safari_shared_residual_v3_162.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    translated = []
    for label, (old, new) in TRANSLATIONS.items():
        if TOKEN_RE.findall(old) != TOKEN_RE.findall(new):
            raise RuntimeError(f"FireRed control-token mismatch for {label}")
        block_re = re.compile(rf"(?ms)^(?P<label>{re.escape(label)}:\n)(?P<body>(?:[ \t]*\.string[^\n]*(?:\n|$))+)")
        matches = list(block_re.finditer(text))
        exact = []
        for m in matches:
            joined = "".join(STRING_RE.findall(m.group("body")))
            if joined == old:
                exact.append(m)
        if len(exact) != 1:
            observed = ["".join(STRING_RE.findall(m.group("body"))) for m in matches]
            raise RuntimeError(f"expected one exact pinned block for {label}; found {len(exact)}; observed={observed!r}")
        m = exact[0]
        body = '\t.string "' + new.replace('"', '\\"') + '"\n'
        text = text[:m.start()] + m.group("label") + body + text[m.end():]
        translated.append(label)
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_safari_shared_residual_v3_162_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "labels": translated,
        "translatedCount": len(translated),
        "scope": "shared FRLG Safari Zone messages only; Hoenn/Pokeblock labels untouched",
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(translated)} shared FRLG Safari Zone blocks; Hoenn/gameplay/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
