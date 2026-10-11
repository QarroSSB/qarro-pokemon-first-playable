#!/usr/bin/env python3
"""Qarro v3.229: polish Fame Checker origin object names for Brock.

Targets exactly Brock's six origin-object labels from pinned FireRed
Expansion 1.17.0:
  SIGN, BROCK, YOUNG MAN, BOY, MAN, POKéMON JOURNAL.

The localization chain has already machine-translated these surfaces, so this
pass fail-closes on the exact label, one simple string, a valid terminator, and
an already-localized Cyrillic surface before replacing it. Every final surface
is verified before write. Text only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_OBJECTS_BROCK_QUALITY_V3_229"
TARGET = Path("data/text/fame_checker_frlg.inc")

PINNED_UPSTREAM_OBJECTS = {
    "gFameCheckerFlavorTextOriginObjectName_Brock0": "SIGN",
    "gFameCheckerFlavorTextOriginObjectName_Brock1": "BROCK",
    "gFameCheckerFlavorTextOriginObjectName_Brock2": "YOUNG MAN",
    "gFameCheckerFlavorTextOriginObjectName_Brock3": "BOY",
    "gFameCheckerFlavorTextOriginObjectName_Brock4": "MAN",
    "gFameCheckerFlavorTextOriginObjectName_Brock5": "POKéMON JOURNAL",
}

TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginObjectName_Brock0": "ВЫВЕСКА$",
    "gFameCheckerFlavorTextOriginObjectName_Brock1": "БРОК$",
    "gFameCheckerFlavorTextOriginObjectName_Brock2": "МОЛОДОЙ ЧЕЛОВЕК$",
    "gFameCheckerFlavorTextOriginObjectName_Brock3": "МАЛЬЧИК$",
    "gFameCheckerFlavorTextOriginObjectName_Brock4": "МУЖЧИНА$",
    "gFameCheckerFlavorTextOriginObjectName_Brock5": "ЖУРНАЛ ПОКЕМОНОВ$",
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


def validate_source(label: str, current: str, translated: str) -> None:
    if not current.endswith("$") or "$" in current[:-1]:
        raise RuntimeError(f"{label}: invalid source terminator: {current!r}")
    if "\\" in current or '"' in current or set(current) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: source is not a simple surface: {current!r}")
    if current == translated:
        return
    if not re.search(r"[А-Яа-яЁё]", current):
        raise RuntimeError(
            f"{label}: expected already-localized Cyrillic source, got {current!r}"
        )


def replace_entry(text: str, label: str, translated: str) -> tuple[str, str]:
    match = find_entry(text, label)
    current = match.group("body")
    validate_source(label, current, translated)

    if not translated.endswith("$") or "$" in translated[:-1]:
        raise RuntimeError(f"{label}: invalid translated terminator")
    if "\\" in translated or '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: invalid translated surface")
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
    return find_entry(text, label).group("body")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: localize_fame_checker_objects_brock_quality_v3_229.py <upstream-root>"
        )
    if set(PINNED_UPSTREAM_OBJECTS) != set(TRANSLATIONS) or len(TRANSLATIONS) != 6:
        raise RuntimeError("unexpected v3.229 Fame Checker object-name set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    before = {}
    for label, translated in TRANSLATIONS.items():
        text, old = replace_entry(text, label, translated)
        before[label] = old

    for label, translated in TRANSLATIONS.items():
        verified = read_entry(text, label)
        if verified != translated:
            raise RuntimeError(
                f"{label}: post-translation verification failed: "
                f"{verified!r} != {translated!r}"
            )

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_fame_checker_objects_brock_quality_v3_229_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "pinnedExpansion": "expansion/1.17.0",
        "pinnedUpstreamObjects": PINNED_UPSTREAM_OBJECTS,
        "exactLabelsRequired": True,
        "sourceSurfacesRequiredCyrillic": True,
        "postTranslationSurfacesVerified": True,
        "singleStringLabelsOnly": True,
        "humanEditedRussian": True,
        "previousSurfaces": before,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Brock Fame Checker object labels"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_objects_misty_quality_v3_230.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
