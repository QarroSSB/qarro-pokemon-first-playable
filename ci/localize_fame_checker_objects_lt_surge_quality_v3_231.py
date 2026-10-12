#!/usr/bin/env python3
"""Qarro v3.231: polish Fame Checker origin object names for Lt. Surge.

Targets exactly Lt. Surge's six origin-object labels from pinned FireRed
Expansion 1.17.0. The source surfaces below are the exact machine-localized
surfaces from the installed v3.8 chain. Any drift fails closed.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_OBJECTS_LT_SURGE_QUALITY_V3_231"
TARGET = Path("data/text/fame_checker_frlg.inc")

PINNED_UPSTREAM_OBJECTS = {
    "gFameCheckerFlavorTextOriginObjectName_LtSurge0": "SIGN",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge1": "LT. SURGE",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge2": "TUCKER",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge3": "TUCKER",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge4": "DWAYNE",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge5": "POKéMON JOURNAL",
}

EXPECTED = {
    "gFameCheckerFlavorTextOriginObjectName_LtSurge0": "ЗВОН$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge1": "ЛТ. КУРС$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge2": "Дыщик$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge3": "Дыщик$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge4": "Дуэйн$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge5": "POKeMON ЙОРНАЛ$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginObjectName_LtSurge0": "ВЫВЕСКА$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge1": "ЛТ. СЕРДЖ$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge2": "ТАКЕР$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge3": "ТАКЕР$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge4": "ДУЭЙН$",
    "gFameCheckerFlavorTextOriginObjectName_LtSurge5": "ЖУРНАЛ ПОКЕМОНОВ$",
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
            "usage: localize_fame_checker_objects_lt_surge_quality_v3_231.py <upstream-root>"
        )

    if (
        set(PINNED_UPSTREAM_OBJECTS) != set(EXPECTED)
        or set(EXPECTED) != set(TRANSLATIONS)
        or len(TRANSLATIONS) != 6
    ):
        raise RuntimeError("unexpected v3.231 Fame Checker object-name set")

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

    out = root / "build" / "qarro_ru_fame_checker_objects_lt_surge_quality_v3_231_audit.json"
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Lt. Surge Fame Checker object labels"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_objects_erika_quality_v3_232.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
