#!/usr/bin/env python3
"""Qarro v3.233: polish Fame Checker origin object names for Koga.

Targets exactly Koga's six origin-object labels from pinned FireRed
Expansion 1.17.0. Exact machine-localized source surfaces from the installed
v3.8 chain are required; any drift fails closed.

FireRed's English Fame Checker calls Koga's daughter "CHARINE" here. That is a
known FRLG naming error for Janine, so the Russian quality surface uses
ДЖАНИН rather than preserving the English typo.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_OBJECTS_KOGA_QUALITY_V3_233"
TARGET = Path("data/text/fame_checker_frlg.inc")

PINNED_UPSTREAM_OBJECTS = {
    "gFameCheckerFlavorTextOriginObjectName_Koga0": "SIGN",
    "gFameCheckerFlavorTextOriginObjectName_Koga1": "KOGA",
    "gFameCheckerFlavorTextOriginObjectName_Koga2": "KIRK",
    "gFameCheckerFlavorTextOriginObjectName_Koga3": "CHARINE",
    "gFameCheckerFlavorTextOriginObjectName_Koga4": "POKéMON JOURNAL",
    "gFameCheckerFlavorTextOriginObjectName_Koga5": "MAN",
}

EXPECTED = {
    "gFameCheckerFlavorTextOriginObjectName_Koga0": "ЗВОН$",
    "gFameCheckerFlavorTextOriginObjectName_Koga1": "Кога$",
    "gFameCheckerFlavorTextOriginObjectName_Koga2": "Кёрк$",
    "gFameCheckerFlavorTextOriginObjectName_Koga3": "Харин$",
    "gFameCheckerFlavorTextOriginObjectName_Koga4": "POKeMON ЙОРНАЛ$",
    "gFameCheckerFlavorTextOriginObjectName_Koga5": "Человек$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginObjectName_Koga0": "ВЫВЕСКА$",
    "gFameCheckerFlavorTextOriginObjectName_Koga1": "КОГА$",
    "gFameCheckerFlavorTextOriginObjectName_Koga2": "КИРК$",
    "gFameCheckerFlavorTextOriginObjectName_Koga3": "ДЖАНИН$",
    "gFameCheckerFlavorTextOriginObjectName_Koga4": "ЖУРНАЛ ПОКЕМОНОВ$",
    "gFameCheckerFlavorTextOriginObjectName_Koga5": "МУЖЧИНА$",
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
            "usage: localize_fame_checker_objects_koga_quality_v3_233.py <upstream-root>"
        )

    if (
        set(PINNED_UPSTREAM_OBJECTS) != set(EXPECTED)
        or set(EXPECTED) != set(TRANSLATIONS)
        or len(TRANSLATIONS) != 6
    ):
        raise RuntimeError("unexpected v3.233 Fame Checker object-name set")

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

    out = root / "build" / "qarro_ru_fame_checker_objects_koga_quality_v3_233_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "pinnedExpansion": "expansion/1.17.0",
        "pinnedUpstreamObjects": PINNED_UPSTREAM_OBJECTS,
        "knownFrlgCharineJanineCorrection": True,
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Koga Fame Checker object labels"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_objects_sabrina_quality_v3_234.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
