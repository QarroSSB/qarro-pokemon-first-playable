#!/usr/bin/env python3
"""Qarro v3.157: confirmed FireRed new-game intro residual runtime text.

Targets only the three English-only FRLG adventure-intro pages confirmed by RU
runtime audit #283 and pinned upstream e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7.
Text-only pass: no gameplay, trainer, reward, Gym, EXP Share, Ash Bond or Ash Cap
logic is touched. Pokemon/Move/Ability proper-name policy remains unchanged.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_NEW_GAME_INTRO_RESIDUAL_V3_157"
REL = Path("data/text/new_game_intro_frlg.inc")

REPLACEMENTS = {
    "gPikachuIntro_Text_Page1": [
        "В мире, в который ты сейчас войдешь,\\n",
        "тебя ждет большое приключение,\\n",
        "где главным героем будешь ты.\\n",
        "\\n",
        "Говори с людьми и осматривай все\\n",
        "в городах, на дорогах и в пещерах.\\n",
        "Собирай сведения и подсказки\\n",
        "из любых источников.$",
    ],
    "gPikachuIntro_Text_Page2": [
        "Новые пути откроются, если помогать\\n",
        "тем, кто в беде, преодолевать испытания\\n",
        "и разгадывать тайны.\\n",
        "\\n",
        "Порой другие будут бросать тебе вызов,\\n",
        "а дикие существа - нападать.\\n",
        "Будь смелее и продолжай идти вперед.$",
    ],
    "gPikachuIntro_Text_Page3": [
        "Мы надеемся, что в приключении\\n",
        "ты встретишь самых разных людей\\n",
        "и станешь сильнее как личность.\\n",
        "Это наша главная цель.\\n",
        "\\n",
        "Нажми кнопку A - и пусть\\n",
        "приключение начнется!$",
    ],
}

LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\n")

def escape_asm(s: str) -> str:
    return s.replace('"', '\\"')

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_new_game_intro_residual_v3_157.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_new_game_intro_residual_v3_157_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "file": str(REL), "translated": applied,
                               "ashBondAshCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} confirmed FRLG new-game intro blocks; Ash Bond/Ash Cap untouched")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
