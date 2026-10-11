#!/usr/bin/env python3
"""Qarro v3.229: polish Fame Checker origin object names for Brock.

Targets only Brock's six single-string origin-object labels. Exact source
surfaces from the current pinned localization chain are required, and every
replacement is verified again before the file is written. Text only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_OBJECTS_BROCK_QUALITY_V3_229"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorTextOriginObjectName_Brock0": "Музей науки в Пьютере$",
    "gFameCheckerFlavorTextOriginObjectName_Brock1": "Питер Гим$",
    "gFameCheckerFlavorTextOriginObjectName_Brock2": "Питер Гим$",
    "gFameCheckerFlavorTextOriginObjectName_Brock3": "МТ. Луна$",
    "gFameCheckerFlavorTextOriginObjectName_Brock4": "МТ. Луна$",
    "gFameCheckerFlavorTextOriginObjectName_Brock5": "Музей науки в Пьютере$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginObjectName_Brock0": "МУЗЕЙ НАУКИ ПЬЮТЕРА$",
    "gFameCheckerFlavorTextOriginObjectName_Brock1": "ГИМ ПЬЮТЕРА$",
    "gFameCheckerFlavorTextOriginObjectName_Brock2": "ГИМ ПЬЮТЕРА$",
    "gFameCheckerFlavorTextOriginObjectName_Brock3": "ЛУННАЯ ГОРА$",
    "gFameCheckerFlavorTextOriginObjectName_Brock4": "ЛУННАЯ ГОРА$",
    "gFameCheckerFlavorTextOriginObjectName_Brock5": "МУЗЕЙ НАУКИ ПЬЮТЕРА$",
}

BANNED_UNICODE = set("—–←→“”«»…")


def replace_entry(text: str, label: str, expected: str, translated: str) -> tuple[str, str]:
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
    if current not in (expected, translated):
        raise RuntimeError(f"{label}: source drift: {current!r} not in {(expected, translated)!r}")
    if not translated.endswith("$") or "$" in translated[:-1]:
        raise RuntimeError(f"{label}: invalid translated terminator")
    if "\\" in translated or '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: invalid translated surface")
    if "\n" in translated or "\r" in translated:
        raise RuntimeError(f"{label}: physical newline in translated surface")
    if not re.search(r"[А-Яа-яЁё]", translated):
        raise RuntimeError(f"{label}: expected Cyrillic translation")

    if current == translated:
        return text, current

    replacement = (
        match.group("label")
        + match.group("prefix")
        + translated
        + match.group("suffix")
    )
    return text[:match.start()] + replacement + text[match.end():], current


def read_entry(text: str, label: str) -> str:
    pattern = re.compile(
        rf'(?m)^{re.escape(label)}::[^\n]*\n'
        rf'\s*\.string "(?P<body>(?:\\.|[^"\\])*)"\s*$'
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{label}: verification expected one entry, got {len(matches)}")
    return matches[0].group("body")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: localize_fame_checker_objects_brock_quality_v3_229.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 6:
        raise RuntimeError("unexpected v3.229 Fame Checker object-name set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    before = {}
    for label, translated in TRANSLATIONS.items():
        text, old = replace_entry(text, label, EXPECTED[label], translated)
        before[label] = old

    for label, translated in TRANSLATIONS.items():
        verified = read_entry(text, label)
        if verified != translated:
            raise RuntimeError(
                f"{label}: post-translation verification failed: {verified!r} != {translated!r}"
            )

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_fame_checker_objects_brock_quality_v3_229_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "humanEditedRussian": True,
        "sourceAnchorsFailClosed": True,
        "postTranslationSurfacesVerified": True,
        "singleStringLabelsOnly": True,
        "previousSurfaces": before,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Brock Fame Checker object labels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
