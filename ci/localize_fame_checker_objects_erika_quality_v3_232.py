#!/usr/bin/env python3
"""Qarro v3.232: polish Fame Checker origin object names for Erika.

Targets exactly Erika's six origin-object labels from pinned FireRed
Expansion 1.17.0. Exact machine-localized source surfaces from the installed
v3.8 chain are required; any drift fails closed.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_OBJECTS_ERIKA_QUALITY_V3_232"
TARGET = Path("data/text/fame_checker_frlg.inc")

PINNED_UPSTREAM_OBJECTS = {
    "gFameCheckerFlavorTextOriginObjectName_Erika0": "SIGN",
    "gFameCheckerFlavorTextOriginObjectName_Erika1": "ERIKA",
    "gFameCheckerFlavorTextOriginObjectName_Erika2": "LOLA",
    "gFameCheckerFlavorTextOriginObjectName_Erika3": "TAMIA",
    "gFameCheckerFlavorTextOriginObjectName_Erika4": "ERIKA",
    "gFameCheckerFlavorTextOriginObjectName_Erika5": "POKéMON JOURNAL",
}

EXPECTED = {
    "gFameCheckerFlavorTextOriginObjectName_Erika0": "ЗВОН$",
    "gFameCheckerFlavorTextOriginObjectName_Erika1": "Эрика$",
    "gFameCheckerFlavorTextOriginObjectName_Erika2": "Лола$",
    "gFameCheckerFlavorTextOriginObjectName_Erika3": "ТАМИЯ$",
    "gFameCheckerFlavorTextOriginObjectName_Erika4": "Эрика$",
    "gFameCheckerFlavorTextOriginObjectName_Erika5": "POKeMON ЙОРНАЛ$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginObjectName_Erika0": "ВЫВЕСКА$",
    "gFameCheckerFlavorTextOriginObjectName_Erika1": "ЭРИКА$",
    "gFameCheckerFlavorTextOriginObjectName_Erika2": "ЛОЛА$",
    "gFameCheckerFlavorTextOriginObjectName_Erika3": "ТАМИЯ$",
    "gFameCheckerFlavorTextOriginObjectName_Erika4": "ЭРИКА$",
    "gFameCheckerFlavorTextOriginObjectName_Erika5": "ЖУРНАЛ ПОКЕМОНОВ$",
}

BANNED_UNICODE = set("—–←→“”«»…")


def find_entry(text: str, label: str) -> re.Match[str]:
    pattern = re.compile(
        rf'(?m)^(?P<label>{re.escape(label)}::[^\n]*\n)'
        rf'(?P<prefix>\s*\.string ")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\s*)$'
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one text entry, got {len(matches)}")
    return matches[0]


def replace_entry(text: str, label: str, expected: str, translated: str) -> str:
    match = find_entry(text, label)
    current = match.group("body")
    if current not in (expected, translated):
        raise RuntimeError(
            f"{label}: source drift: {current!r} not in {(expected, translated)!r}"
        )
    if not translated.endswith("$") or "$" in translated[:-1]:
        raise RuntimeError(f"{label}: invalid translated terminator")
    if "\\" in translated or '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: invalid translated surface")
    if not re.search(r"[А-Яа-яЁё]", translated):
        raise RuntimeError(f"{label}: expected Cyrillic translation")
    if current == translated:
        return text

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
            "usage: localize_fame_checker_objects_erika_quality_v3_232.py <upstream-root>"
        )

    if (
        set(PINNED_UPSTREAM_OBJECTS) != set(EXPECTED)
        or set(EXPECTED) != set(TRANSLATIONS)
        or len(TRANSLATIONS) != 6
    ):
        raise RuntimeError("unexpected v3.232 Fame Checker object-name set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    for label in EXPECTED:
        text = replace_entry(text, label, EXPECTED[label], TRANSLATIONS[label])

    for label, translated in TRANSLATIONS.items():
        verified = find_entry(text, label).group("body")
        if verified != translated:
            raise RuntimeError(
                f"{label}: post-translation verification failed: "
                f"{verified!r} != {translated!r}"
            )

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_fame_checker_objects_erika_quality_v3_232_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "pinnedExpansion": "expansion/1.17.0",
        "pinnedUpstreamObjects": PINNED_UPSTREAM_OBJECTS,
        "sourceAnchorsFailClosed": True,
        "postTranslationSurfacesVerified": True,
        "singleStringLabelsOnly": True,
        "humanEditedRussian": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Erika Fame Checker object labels"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
