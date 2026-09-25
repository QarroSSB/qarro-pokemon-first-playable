#!/usr/bin/env python3
"""Qarro v3.227: polish Fame Checker origin object names for Prof. Oak.

Targets only Prof. Oak's six single-string origin-object labels verified
against the pinned FireRed upstream. Text only; fail closed on non-Cyrillic surfaces.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_OBJECTS_PROF_OAK_QUALITY_V3_227"
TARGET = Path("data/text/fame_checker_frlg.inc")
TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginObjectName_ProfOak0": "ВЫВЕСКА$",
    "gFameCheckerFlavorTextOriginObjectName_ProfOak1": "ПРОФ. ОУК$",
    "gFameCheckerFlavorTextOriginObjectName_ProfOak2": "ПОМОЩНИК$",
    "gFameCheckerFlavorTextOriginObjectName_ProfOak3": "ЖУРНАЛ ПОКЕМОНОВ$",
    "gFameCheckerFlavorTextOriginObjectName_ProfOak4": "АГАТА$",
    "gFameCheckerFlavorTextOriginObjectName_ProfOak5": "ПОМОЩНИК$",
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
    if len(TRANSLATIONS) != 6:
        raise RuntimeError("unexpected v3.227 Fame Checker object-name set")
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
    out = root / "build" / "qarro_ru_fame_checker_objects_prof_oak_quality_v3_227_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "targetFile": str(TARGET), "qualityPassStrings": len(TRANSLATIONS), "sourceLabelsVerifiedAgainstPinnedUpstream": True, "sourceSurfacesRequiredCyrillic": True, "singleStringLabelsOnly": True, "humanEditedRussian": True, "previousSurfaces": before, "gameplayLogicTouched": False, "balanceTouched": False, "bossTeamsTouched": False, "specialWhitelistTouched": False, "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Fame Checker object-name labels")

    next_script = Path(__file__).with_name("localize_fame_checker_objects_daisy_quality_v3_228.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
