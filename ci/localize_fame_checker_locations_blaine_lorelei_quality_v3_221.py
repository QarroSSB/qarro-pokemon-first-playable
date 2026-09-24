#!/usr/bin/env python3
"""Qarro v3.221: polish Fame Checker origin locations for Blaine and Lorelei.

Targets only the 12 single-string origin-location labels verified against the
pinned FireRed upstream. The current body must already be a simple Cyrillic
location surface; labels are unique and replacements are text-only.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_LOCATIONS_BLAINE_LORELEI_QUALITY_V3_221"
TARGET = Path("data/text/fame_checker_frlg.inc")
TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginLocation_Blaine0": "ОСТРОВ СИННАБАР$",
    "gFameCheckerFlavorTextOriginLocation_Blaine1": "ГИМ СИННАБАРА$",
    "gFameCheckerFlavorTextOriginLocation_Blaine2": "ГИМ СИННАБАРА$",
    "gFameCheckerFlavorTextOriginLocation_Blaine3": "ОСТРОВ СИННАБАР$",
    "gFameCheckerFlavorTextOriginLocation_Blaine4": "ГИМ СИННАБАРА$",
    "gFameCheckerFlavorTextOriginLocation_Blaine5": "КУРОРТ ГОРДЖЕС$",
    "gFameCheckerFlavorTextOriginLocation_Lorelei0": "ЛИГА ПОКЕМОНОВ$",
    "gFameCheckerFlavorTextOriginLocation_Lorelei1": "ЛИГА ПОКЕМОНОВ$",
    "gFameCheckerFlavorTextOriginLocation_Lorelei2": "ОСТРОВ 4$",
    "gFameCheckerFlavorTextOriginLocation_Lorelei3": "ОСТРОВ 5$",
    "gFameCheckerFlavorTextOriginLocation_Lorelei4": "ОСТРОВ 4$",
    "gFameCheckerFlavorTextOriginLocation_Lorelei5": "ОСТРОВ 4$",
}
BANNED_UNICODE = set("—–←→“”«»…")


def replace_entry(text: str, label: str, translated: str) -> tuple[str, str]:
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
    if not current.endswith("$") or "$" in current[:-1]:
        raise RuntimeError(f"{label}: current location has invalid terminator: {current!r}")
    if "\\" in current or '"' in current or set(current) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: current location is not a simple surface: {current!r}")
    if not re.search(r"[А-Яа-яЁё]", current):
        raise RuntimeError(f"{label}: expected already-localized Cyrillic source, got {current!r}")
    if not translated.endswith("$") or "$" in translated[:-1]:
        raise RuntimeError(f"{label}: invalid translated terminator")
    if "\\" in translated or '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: invalid translated location")
    if current == translated:
        return text, current
    return (
        text[:match.start()] + match.group("label") + match.group("prefix")
        + translated + match.group("suffix") + text[match.end():], current
    )


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <upstream-root>")
    if len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.221 Fame Checker location set")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")
    text = path.read_text(encoding="utf-8")
    before = {}
    for label, translated in TRANSLATIONS.items():
        text, old = replace_entry(text, label, translated)
        before[label] = old
    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_fame_checker_locations_blaine_lorelei_quality_v3_221_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "sourceLabelsVerifiedAgainstPinnedUpstream": True,
        "sourceSurfacesRequiredCyrillic": True,
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
    print(f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Fame Checker location labels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
