#!/usr/bin/env python3
"""Qarro v3.161: localize one audited FireRed Trainer Card sticker dialogue.

Targets the first confirmed user-facing FRLG residual from RU runtime surface audit #299,
verified against pinned upstream e8bd1cd7. Text-only pass: no gameplay, trainer,
reward, inventory, progression, Ash Bond or Ash Cap logic is touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINER_CARD_STICKER_RESIDUAL_V3_161"
REL = Path("data/text/trainer_card_frlg.inc")
LABEL = "FourIsland_House2_Text_GiveYouStickerIfYouBrag"
OLD = "Oh, excellent!\\nYou've come to the right place!\\pLook, look! See? See?\\nThese are my STICKERS!\\lLook how many I got!\\pI bet you want some.\\nI bet you do!\\pI'll give a STICKER if you can tell\\nme something awesome about\\lyourself.\\pWhat will you brag about?$"
NEW = "О, отлично!\\nТы пришёл куда надо!\\pСмотри, смотри! Видишь?\\nЭто мои STICKERS!\\lВидишь, сколько их у меня?\\pНаверняка тоже хочешь.\\nЕщё бы!\\pЯ дам тебе STICKER, если расскажешь\\nмне что-нибудь крутое\\lо себе.\\pЧем будешь хвастаться?$"
TOKEN_RE = re.compile(r"\\[npl]|\$")
STRING_RE = re.compile(r'^\s*\.string\s+"((?:\\.|[^"\\])*)"\s*$', re.M)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_trainer_card_sticker_residual_v3_161.py <upstream-root>")
    if TOKEN_RE.findall(OLD) != TOKEN_RE.findall(NEW):
        raise RuntimeError("FireRed control-token mismatch")

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    block_re = re.compile(rf"(?ms)^(?P<label>{re.escape(LABEL)}::\n)(?P<body>(?:\s*\.string\s+.*\n)+)")
    matches = list(block_re.finditer(text))
    exact = []
    for m in matches:
        joined = "".join(STRING_RE.findall(m.group("body")))
        if joined == OLD:
            exact.append(m)
    if len(exact) != 1:
        observed = ["".join(STRING_RE.findall(m.group("body"))) for m in matches]
        raise RuntimeError(f"expected one exact pinned block for {LABEL}; found {len(exact)}; observed={observed!r}")

    m = exact[0]
    body = '\t.string "' + NEW.replace('"', '\\"') + '"\n'
    replacement = m.group("label") + body
    path.write_text(text[:m.start()] + replacement + text[m.end():], encoding="utf-8")

    out = root / "build" / "qarro_ru_trainer_card_sticker_residual_v3_161_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "label": LABEL,
        "translatedCount": 1,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names English",
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {LABEL}; gameplay/logic/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
