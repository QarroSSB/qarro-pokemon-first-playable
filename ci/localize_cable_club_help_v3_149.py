#!/usr/bin/env python3
"""Qarro v3.149: first residual full-surface FireRed Cable Club help text.

Translates the three largest confirmed English-only FireRed Cable Club help
blocks reported by RU runtime audit #262. This pass is text-only: no gameplay,
trainer, reward, item, Gym, EXP Share, Ash Bond or Ash Cap logic is touched.
Pokemon/Move/Ability proper-name policy remains unchanged.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_CABLE_CLUB_INFO_V3_149"
REL = Path("data/scripts/cable_club_frlg.inc")

REPLACEMENTS = {
    "CableClub_Text_ExplainBattleModes_Frlg": [
        "Есть три режима боя.\\p",
        "ОДИНОЧНЫЙ БОЙ - для двух ТРЕНЕРОВ,\\n",
        "у каждого один или больше ПОКЕМОНОВ.\\p",
        "Каждый ТРЕНЕР выпускает в бой\\n",
        "по одному ПОКЕМОНУ.\\p",
        "ДВОЙНОЙ БОЙ - для двух ТРЕНЕРОВ,\\n",
        "у каждого два или больше ПОКЕМОНОВ.\\p",
        "Каждый ТРЕНЕР выпускает в бой\\n",
        "по два ПОКЕМОНА.\\p",
        "МУЛЬТИБОЙ - для четырех ТРЕНЕРОВ,\\n",
        "у каждого один или больше ПОКЕМОНОВ.\\p",
        "Каждый ТРЕНЕР выпускает в бой\\n",
        "по одному ПОКЕМОНУ.$",
    ],
    "CableClub_Text_ExplainWirelessClubFirstTime_Frlg": [
        "На верхнем этаже есть две комнаты.\\p",
        "Сначала комната слева.\\n",
        "Это КОМНАТА СОЮЗА.\\p",
        "Здесь можно связаться с ТРЕНЕРАМИ,\\n",
        "которые рядом и тоже вошли\\l",
        "в КОМНАТУ СОЮЗА.\\p",
        "С ними можно общаться,\\n",
        "сражаться и обмениваться.\\p",
        "Вторая комната справа -\\n",
        "ПРЯМОЙ УГОЛОК.\\p",
        "Здесь можно обмениваться ПОКЕМОНАМИ\\n",
        "или сражаться с друзьями.\\p",
        "Если беспроводной адаптер не подключен,\\n",
        "можно соединиться кабелем GBA Game Link.\\p",
        "В таком случае нужно идти\\n",
        "в ПРЯМОЙ УГОЛОК.\\p",
        "Приятного использования беспроводной\\n",
        "системы связи.$",
    ],
    "CableClub_Text_ExplainWirelessClub_Frlg": [
        "Объясню, как работает БЕСПРОВОДНОЙ\\n",
        "КЛУБ ПОКЕМОНОВ.\\p",
        "На верхнем этаже есть две комнаты.\\p",
        "Сначала комната слева.\\n",
        "Это КОМНАТА СОЮЗА.\\p",
        "Здесь можно связаться с ТРЕНЕРАМИ,\\n",
        "которые рядом и тоже вошли\\l",
        "в КОМНАТУ СОЮЗА.\\p",
        "С ними можно общаться,\\n",
        "сражаться и обмениваться.\\p",
        "Вторая комната справа -\\n",
        "ПРЯМОЙ УГОЛОК.\\p",
        "Здесь можно обмениваться ПОКЕМОНАМИ\\n",
        "или сражаться с друзьями.\\p",
        "Если друзья не находятся в КОМНАТЕ\\n",
        "СОЮЗА или ПРЯМОМ УГОЛКЕ,\\p",
        "подойдите к ним поближе.\\p",
        "Если беспроводной адаптер не подключен,\\n",
        "можно соединиться кабелем GBA Game Link.\\p",
        "В таком случае нужно идти\\n",
        "в ПРЯМОЙ УГОЛОК.\\p",
        "Приятного использования беспроводной\\n",
        "системы связи.$",
    ],
}

LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\n")

def escape_asm(s: str) -> str:
    # Preserve FireRed text escapes (\\n / \\p / \\l); only C/ASM-quote escaping is needed here.
    return s.replace('"', '\\"')

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_cable_club_help_v3_149.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_cable_club_info_v3_149_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "file": str(REL), "translated": applied,
                               "ashBondAshCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Cable Club help blocks; FireRed text escapes preserved; Ash Bond/Ash Cap untouched")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
