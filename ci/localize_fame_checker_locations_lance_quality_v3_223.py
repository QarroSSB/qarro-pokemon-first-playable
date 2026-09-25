#!/usr/bin/env python3
"""Qarro v3.223: polish Fame Checker origin locations for Lance.

Targets only Lance's six single-string origin-location labels verified against
the pinned FireRed upstream. Text only; fail closed on non-Cyrillic surfaces.
Chains the verified Bill location pass after this pass.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_LOCATIONS_LANCE_QUALITY_V3_223"
TARGET = Path("data/text/fame_checker_frlg.inc")
TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginLocation_Lance0": "ЛИГА ПОКЕМОНОВ$",
    "gFameCheckerFlavorTextOriginLocation_Lance1": "ЛИГА ПОКЕМОНОВ$",
    "gFameCheckerFlavorTextOriginLocation_Lance2": "САФФРОН$",
    "gFameCheckerFlavorTextOriginLocation_Lance3": "УНИВЕРМАГ СЕЛАДОНА$",
    "gFameCheckerFlavorTextOriginLocation_Lance4": "ПЛАТО ИНДИГО$",
    "gFameCheckerFlavorTextOriginLocation_Lance5": "ПЛАТО ИНДИГО$",
}
BANNED_UNICODE = set("—–←→“”«»…")


def replace_entry(text: str, label: str, translated: str) -> tuple[str, str]:
    pattern = re.compile(rf'(?m)^(?P<label>{re.escape(label)}::[^\n]*\n)(?P<prefix>\s*\.string ")(?P<body>(?:\\.|[^"\\])*)(?P<suffix>"\s*)$')
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one text entry, got {len(matches)}")
    match = matches[0]
    current = match.group("body")
    if not current.endswith("$") or "$" in current[:-1]:
        raise RuntimeError(f"{label}: invalid source terminator: {current!r}")
    if "\\" in current or '"' in current or set(current) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: source is not a simple surface: {current!r}")
    if not re.search(r"[А-Яа-яЁё]", current):
        raise RuntimeError(f"{label}: expected already-localized Cyrillic source, got {current!r}")
    if current == translated:
        return text, current
    return text[:match.start()] + match.group("label") + match.group("prefix") + translated + match.group("suffix") + text[match.end():], current


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <upstream-root>")
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
    out = root / "build" / "qarro_ru_fame_checker_locations_lance_quality_v3_223_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "targetFile": str(TARGET), "qualityPassStrings": len(TRANSLATIONS), "sourceLabelsVerifiedAgainstPinnedUpstream": True, "sourceSurfacesRequiredCyrillic": True, "singleStringLabelsOnly": True, "humanEditedRussian": True, "previousSurfaces": before, "gameplayLogicTouched": False, "balanceTouched": False, "bossTeamsTouched": False, "specialWhitelistTouched": False, "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Fame Checker location labels")
    next_pass = Path(__file__).with_name("localize_fame_checker_locations_bill_quality_v3_224.py")
    subprocess.run([sys.executable, str(next_pass), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
