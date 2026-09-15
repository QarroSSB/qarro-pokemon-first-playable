#!/usr/bin/env python3
"""Qarro v3.110: localize Rocket Hideout B1F runtime text.

Translates exactly 15 English-only FireRed runtime blocks from the v3.109
surface audit. Pokemon species, Move and Ability proper names remain English by
project canon. Gameplay/trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROCKET_HIDEOUT_B1F_V3_110"
TARGET = Path("data/maps/RocketHideout_B1F_Frlg/scripts.inc")
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

PATCHES = {
    "RocketHideout_B1F_Text_Grunt1Intro": "Ты кто такой?\\nКак сюда пробрался?$",
    "RocketHideout_B1F_Text_Grunt1Defeat": "Ай!\\nПобит!$",
    "RocketHideout_B1F_Text_Grunt1PostBattle": "Чёрт... Ты ведь нарываешься\\nна КОМАНДУ R, да?$",
    "RocketHideout_B1F_Text_Grunt2Intro": "Ты вломился в логово КОМАНДЫ R?\\nКакая наглость!$",
    "RocketHideout_B1F_Text_Grunt2Defeat": "Бум!$",
    "RocketHideout_B1F_Text_Grunt2PostBattle": "Тебе это с рук не сойдёт,\\nмалец!$",
    "RocketHideout_B1F_Text_Grunt3Intro": "Тревога! Нарушитель!$",
    "RocketHideout_B1F_Text_Grunt3Defeat": "Не могу!$",
    "RocketHideout_B1F_Text_Grunt3PostBattle": "SILPH SCOPE? Ха!\\nНе знаю, где он.$",
    "RocketHideout_B1F_Text_Grunt4Intro": "Зачем ты сюда пришёл?$",
    "RocketHideout_B1F_Text_Grunt4Defeat": "Так не пойдёт!$",
    "RocketHideout_B1F_Text_Grunt4PostBattle": "Ладно, скажу...\\nПоднимись на лифте к моему БОССУ.$",
    "RocketHideout_B1F_Text_Grunt5Intro": "Заблудился, мышонок?$",
    "RocketHideout_B1F_Text_Grunt5Defeat": "Почему...?$",
    "RocketHideout_B1F_Text_Grunt5PostBattle": "Ой... Этот шум почему-то\\nоткрыл дверь!$",
}
EXPECTED_TOTAL = 15


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def validate_translation(label: str, translated: str) -> None:
    if not translated.endswith("$"):
        die(f"{label}: translated text must end with $")
    if "\n" in translated or "\r" in translated:
        die(f"{label}: physical newline/carriage return in translation value")
    if any(ch in translated for ch in ("—", "–", "“", "”", "’", "…", "«", "»")):
        die(f"{label}: unsupported Unicode punctuation")
    if "\\\\" in translated:
        die(f"{label}: doubled runtime backslash in translation value")
    if not re.search(r"[А-Яа-яЁё]", translated):
        die(f"{label}: expected Cyrillic translation")


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def replace_block(text: str, label: str, translated: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: target already contains Cyrillic; refusing overwrite")
    if ".string " not in old:
        die(f"{label}: target does not look like a text block")
    safe = translated.replace('"', '\\"')
    block = f'{label}::\n\t.string "{safe}"\n\n'
    return text[:start] + block + text[end:]


def validate_written(text: str) -> None:
    for lineno, line in enumerate(text.splitlines(), start=1):
        if '.string "' in line and line.count('"') < 2:
            die(f"{TARGET}:{lineno}: physical newline inside assembler string")
    if re.search(r"\\\\[npl]", text):
        die(f"{TARGET}: doubled FireRed runtime escape found")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    if len(PATCHES) != EXPECTED_TOTAL:
        die(f"expected {EXPECTED_TOTAL} translation entries, got {len(PATCHES)}")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        die(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    for label, translated in PATCHES.items():
        validate_translation(label, translated)
        text = replace_block(text, label, translated)
    validate_written(text)
    path.write_text(text, encoding="utf-8")

    audit = root / "build" / "qarro_ru_rocket_hideout_b1f_v3_110_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(
        json.dumps(
            {
                "marker": MARKER,
                "translatedBlockCount": EXPECTED_TOTAL,
                "translatedByFile": {str(TARGET): EXPECTED_TOTAL},
                "physicalNewlinesInsideAsmStrings": False,
                "doubledRuntimeEscapes": False,
                "gameplayLogicTouched": False,
                "trainerDataTouched": False,
                "ashBondTouched": False,
                "ashCapTouched": False,
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(
        f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} Rocket Hideout B1F runtime blocks; "
        "trainer/gameplay/Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
