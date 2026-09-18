#!/usr/bin/env python3
"""Qarro v3.161: localize audited FireRed controls-guide residual text.

Targets six English-only controls-guide blocks confirmed by RU runtime surface
audit #310 on v3.160 GREEN and checked against pinned Expansion 1.17.0
(e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7). Text-only pass: no gameplay,
trainer, reward, inventory, flag, progression, Ash Bond or Ash Cap logic is
touched. Pokemon/Move/Ability proper names remain English by policy.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_CONTROLS_GUIDE_RESIDUAL_V3_161"
REL = Path("data/text/new_game_intro_frlg.inc")

REPLACEMENTS = {
    "gControlsGuide_Text_Intro": (
        "The various buttons will be explained in\nthe order of their importance.$",
        [
            "Разные кнопки будут объяснены\\n",
            "в порядке их важности.$",
        ],
    ),
    "gControlsGuide_Text_DPad": (
        "Moves the main character.\nAlso used to choose various data\nheadings.$",
        [
            "Перемещает главного героя.\\n",
            "Также используется для выбора\\n",
            "разных пунктов меню.$",
        ],
    ),
    "gControlsGuide_Text_AButton": (
        "Used to confirm a choice, check\nthings, chat, and scroll text.$",
        [
            "Подтверждает выбор, позволяет\\n",
            "осматривать, говорить и листать текст.$",
        ],
    ),
    "gControlsGuide_Text_BButton": (
        "Used to exit, cancel a choice,\nand cancel a mode.$",
        [
            "Выход, отмена выбора\\n",
            "и отмена режима.$",
        ],
    ),
    "gControlsGuide_Text_SelectButton": (
        "Used to shift items and to use\na registered item.$",
        [
            "Перемещает предметы и использует\\n",
            "зарегистрированный предмет.$",
        ],
    ),
    "gControlsGuide_Text_LRButtons": (
        "If you need help playing the\ngame, or on how to do things,\npress the L or R Button.$",
        [
            "Если нужна помощь по игре\\n",
            "или управлению,\\n",
            "нажми кнопку L или R.$",
        ],
    ),
}

LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\n")
STRING_RE = re.compile(r'^\s*\.string\s+"((?:\\.|[^"\\])*)"\s*$', re.M)


def decode_asm_literal(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        if s[i] != "\\" or i + 1 >= len(s):
            out.append(s[i])
            i += 1
            continue
        nxt = s[i + 1]
        if nxt == "n":
            out.append("\n")
        elif nxt == "r":
            out.append("\r")
        elif nxt == "t":
            out.append("\t")
        elif nxt == '"':
            out.append('"')
        elif nxt == "\\":
            out.append("\\")
        else:
            out.append("\\" + nxt)
        i += 2
    return "".join(out)


def decode_block(body: str) -> str:
    return "".join(decode_asm_literal(x) for x in STRING_RE.findall(body))


def escape_asm(s: str) -> str:
    return s.replace('"', '\\"')


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_controls_guide_residual_v3_161.py <upstream-root>")

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied = []

    for label, (old_raw, new_lines) in REPLACEMENTS.items():
        matches = list(LABEL_RE.finditer(text))
        label_matches = [m for m in matches if m.group(1) == label]
        if len(label_matches) != 1:
            raise RuntimeError(f"expected one label {label}; found {len(label_matches)}")
        match = label_matches[0]
        next_match = next((m for m in matches if m.start() > match.start()), None)
        end = next_match.start() if next_match else len(text)
        old_body = text[match.end():end]
        observed = decode_block(old_body)
        if observed != old_raw:
            raise RuntimeError(f"source drift for {label}: {observed!r}")
        new_raw = "".join(decode_asm_literal(x) for x in new_lines)
        if old_raw.count("$") != new_raw.count("$"):
            raise RuntimeError(f"terminator mismatch for {label}")
        body = "".join(f'\t.string "{escape_asm(line)}"\n' for line in new_lines) + "\n"
        text = text[:match.end()] + body + text[end:]
        applied.append({"label": label, "old": old_raw, "new": new_raw})

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_controls_guide_residual_v3_161_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translated": applied,
        "translatedCount": len(applied),
        "policy": "Pokemon/Move/Ability names English; descriptions/UI/dialogue/system text Russian",
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} controls-guide blocks; gameplay/logic/Ash untouched")

    sticker = Path(__file__).resolve().parent / "localize_trainer_card_sticker_residual_v3_161.py"
    if not sticker.is_file():
        raise FileNotFoundError(f"missing staged v3.161 sticker script: {sticker}")
    subprocess.run([sys.executable, str(sticker), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
