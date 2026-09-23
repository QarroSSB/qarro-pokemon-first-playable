#!/usr/bin/env python3
"""Qarro v3.219: polish Fame Checker origin locations for Oak through Misty.

Repairs 24 short location labels that were mechanically mistranslated. Exact
single-string anchors are required. This pass changes text only.

Pokemon, Move and Ability proper names stay English by project canon.
Gameplay, balance, boss teams, special whitelist, Ash Bond and Ash Cap are
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_LOCATIONS_OAK_MISTY_QUALITY_V3_219"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorTextOriginLocation_ProfOak0": "Паллетный бутон$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak1": "Исследовательский центр$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak2": "Исследовательский центр$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak3": "ВИРИДИАНСКИЙ ГОРОД$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak4": "POKeMON ЛЕГИ$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak5": "Исследовательский центр$",
    "gFameCheckerFlavorTextOriginLocation_Daisy0": "Исследовательский центр$",
    "gFameCheckerFlavorTextOriginLocation_Daisy1": "Город Вермилион$",
    "gFameCheckerFlavorTextOriginLocation_Daisy2": "Водный лабиринт$",
    "gFameCheckerFlavorTextOriginLocation_Daisy3": "ВИРИДИАНСКИЙ ГОРОД$",
    "gFameCheckerFlavorTextOriginLocation_Daisy4": "Челадон Мансион$",
    "gFameCheckerFlavorTextOriginLocation_Daisy5": "Четыре острова$",
    "gFameCheckerFlavorTextOriginLocation_Brock0": "Город Питер$",
    "gFameCheckerFlavorTextOriginLocation_Brock1": "Питер Гим$",
    "gFameCheckerFlavorTextOriginLocation_Brock2": "Город Питер$",
    "gFameCheckerFlavorTextOriginLocation_Brock3": "Рута 4$",
    "gFameCheckerFlavorTextOriginLocation_Brock4": "МТ. Луна$",
    "gFameCheckerFlavorTextOriginLocation_Brock5": "Музей Питера$",
    "gFameCheckerFlavorTextOriginLocation_Misty0": "КРУЛЕВСКИЙ ГОРОД$",
    "gFameCheckerFlavorTextOriginLocation_Misty1": "КРУЛЕВСКИЙ ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_Misty2": "КРУЛЕВСКИЙ ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_Misty3": "СИФОАМ ИСЛАНДС$",
    "gFameCheckerFlavorTextOriginLocation_Misty4": "СЕРУЛЬСКАЯ КАРЬ$",
    "gFameCheckerFlavorTextOriginLocation_Misty5": "КРУЛЕВСКИЙ ГОРОД$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginLocation_ProfOak0": "ПАЛЛЕТ-ТАУН$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak1": "ЛАБОРАТОРИЯ$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak2": "ЛАБОРАТОРИЯ$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak3": "ВИРИДИАН-СИТИ$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak4": "ЛИГА ПОКЕМОНОВ$",
    "gFameCheckerFlavorTextOriginLocation_ProfOak5": "ЛАБОРАТОРИЯ$",
    "gFameCheckerFlavorTextOriginLocation_Daisy0": "ЛАБОРАТОРИЯ$",
    "gFameCheckerFlavorTextOriginLocation_Daisy1": "ВЕРМИЛИОН$",
    "gFameCheckerFlavorTextOriginLocation_Daisy2": "ВОДНЫЙ ЛАБИРИНТ$",
    "gFameCheckerFlavorTextOriginLocation_Daisy3": "ВИРИДИАН-СИТИ$",
    "gFameCheckerFlavorTextOriginLocation_Daisy4": "ОСОБНЯК СЕЛАДОНА$",
    "gFameCheckerFlavorTextOriginLocation_Daisy5": "ОСТРОВ 4$",
    "gFameCheckerFlavorTextOriginLocation_Brock0": "ПЬЮТЕР-СИТИ$",
    "gFameCheckerFlavorTextOriginLocation_Brock1": "ГИМ ПЬЮТЕРА$",
    "gFameCheckerFlavorTextOriginLocation_Brock2": "ПЬЮТЕР-СИТИ$",
    "gFameCheckerFlavorTextOriginLocation_Brock3": "МАРШРУТ 4$",
    "gFameCheckerFlavorTextOriginLocation_Brock4": "ЛУННАЯ ГОРА$",
    "gFameCheckerFlavorTextOriginLocation_Brock5": "МУЗЕЙ ПЬЮТЕРА$",
    "gFameCheckerFlavorTextOriginLocation_Misty0": "СЕРУЛИН$",
    "gFameCheckerFlavorTextOriginLocation_Misty1": "ГИМ СЕРУЛИНА$",
    "gFameCheckerFlavorTextOriginLocation_Misty2": "ГИМ СЕРУЛИНА$",
    "gFameCheckerFlavorTextOriginLocation_Misty3": "ОСТРОВА СИФОМ$",
    "gFameCheckerFlavorTextOriginLocation_Misty4": "МЫС СЕРУЛИНА$",
    "gFameCheckerFlavorTextOriginLocation_Misty5": "СЕРУЛИН$",
}

BANNED_UNICODE = set("—–←→“”«»…")


def replace_entry(text: str, label: str, expected: str, translated: str) -> str:
    pattern = re.compile(
        rf'(?m)^(?P<label>{re.escape(label)}::[^\n]*\n)'
        rf'(?P<prefix>\s*\.string ")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\s*)$'
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one text entry, got {len(matches)}")

    match = matches[0]
    current = match.group("body")
    if current != expected:
        raise RuntimeError(f"{label}: source drift: {current!r} != {expected!r}")
    if not translated.endswith("$") or "$" in translated[:-1]:
        raise RuntimeError(f"{label}: invalid terminator")
    if "\\" in translated or '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: invalid location surface")
    if "\n" in translated or "\r" in translated:
        raise RuntimeError(f"{label}: physical newline in location surface")
    if not re.search(r"[А-Яа-яЁё]", translated):
        raise RuntimeError(f"{label}: expected Cyrillic location")

    replacement = (
        match.group("label")
        + match.group("prefix")
        + translated
        + match.group("suffix")
    )
    return text[:match.start()] + replacement + text[match.end():]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: localize_fame_checker_locations_oak_misty_quality_v3_219.py <upstream-root>"
        )

    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 24:
        raise RuntimeError("unexpected v3.219 Fame Checker location set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    for label in EXPECTED:
        text = replace_entry(text, label, EXPECTED[label], TRANSLATIONS[label])
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_fame_checker_locations_oak_misty_quality_v3_219_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "humanEditedRussian": True,
        "sourceAnchorsFailClosed": True,
        "singleStringLabelsOnly": True,
        "projectLocationNamingReused": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Fame Checker location labels"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
