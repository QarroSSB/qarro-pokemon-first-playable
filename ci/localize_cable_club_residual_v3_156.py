#!/usr/bin/env python3
"""Qarro v3.156: next confirmed FireRed Cable Club residual runtime text.

Targets only two large English-only FRLG blocks confirmed by RU runtime audit #281
and pinned upstream e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7. Text-only pass:
no gameplay, trainer, reward, Gym, EXP Share, Ash Bond or Ash Cap logic is touched.
Pokemon/Move/Ability proper-name policy remains unchanged.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_CABLE_CLUB_RESIDUAL_V3_156"
REL = Path("data/scripts/cable_club_frlg.inc")

REPLACEMENTS = {
    "CableClub_Text_UnionRoomInfo_Frlg": [
        "В КОМНАТЕ СОЮЗА будут ТРЕНЕРЫ,\\n",
        "которые находятся рядом с вами\\l",
        "и тоже вошли в эту КОМНАТУ.\\p",
        "Здесь можно делать многое,\\n",
        "например обмениваться приветствиями.\\p",
        "Для боя один на один можно взять\\n",
        "двух ПОКЕМОНОВ до 30-го уровня.\\p",
        "Можно участвовать в чате\\n",
        "для двух-пяти человек.\\p",
        "Также можно выставить ПОКЕМОНА\\n",
        "для обмена.\\p",
        "Хотите войти в КОМНАТУ?$",
    ],
    "Text_PokemonJumpInfo_Frlg": [
        "“ПРЫЖКИ ПОКЕМОНОВ”\\p",
        "Нажимайте A, чтобы ПОКЕМОН прыгал\\n",
        "через веревку из VINE WHIP.\\p",
        "Участвовать могут только небольшие\\n",
        "ПОКЕМОНЫ ростом около 28 дюймов или ниже.\\p",
        "ПОКЕМОНЫ, которые только плавают,\\n",
        "роют землю или летают, плохо прыгают.\\p",
        "Поэтому такие ПОКЕМОНЫ\\n",
        "не могут участвовать.\\p",
        "Если все прыгают в такт,\\n",
        "происходит что-то хорошее.$",
    ],
}

LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\n")

def escape_asm(s: str) -> str:
    return s.replace('"', '\\"')

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_cable_club_residual_v3_156.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied = []
    for label, lines in REPLACEMENTS.items():
        matches = list(LABEL_RE.finditer(text))
        match = next((m for m in matches if m.group(1) == label), None)
        if match is None:
            raise RuntimeError(f"missing label: {label}")
        next_match = next((m for m in matches if m.start() > match.start()), None)
        end = next_match.start() if next_match else len(text)
        old = text[match.end():end]
        if not re.search(r'(?m)^\s*\.string\s+"', old):
            raise RuntimeError(f"no string body: {label}")
        body = ''.join(f'\t.string "{escape_asm(line)}"\n' for line in lines) + '\n'
        text = text[:match.end()] + body + text[end:]
        applied.append(label)
    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_cable_club_residual_v3_156_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "file": str(REL), "translated": applied,
                               "ashBondAshCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} confirmed FRLG Cable Club blocks; Ash Bond/Ash Cap untouched")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
