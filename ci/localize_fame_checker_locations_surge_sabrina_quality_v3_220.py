#!/usr/bin/env python3
"""Qarro v3.220: polish Fame Checker origin locations from Lt. Surge to Sabrina.

Repairs 24 short location labels that were mechanically mistranslated. Exact
single-string anchors are required. Text only; fail closed. Chains the verified
v3.221 Blaine/Lorelei location pass after this pass.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_LOCATIONS_SURGE_SABRINA_QUALITY_V3_220"
TARGET = Path("data/text/fame_checker_frlg.inc")
EXPECTED = {
    "gFameCheckerFlavorTextOriginLocation_LtSurge0": "Город Вермилион$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge1": "ВЕРМИЛИОН ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge2": "ВЕРМИЛИОН ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge3": "ВЕРМИЛИОН ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge4": "ВЕРМИЛИОН ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge5": "Город Вермилион$",
    "gFameCheckerFlavorTextOriginLocation_Erika0": "Город Челадон$",
    "gFameCheckerFlavorTextOriginLocation_Erika1": "Челадон Гим$",
    "gFameCheckerFlavorTextOriginLocation_Erika2": "Челадон Гим$",
    "gFameCheckerFlavorTextOriginLocation_Erika3": "Челадон Гим$",
    "gFameCheckerFlavorTextOriginLocation_Erika4": "Челадон Гим$",
    "gFameCheckerFlavorTextOriginLocation_Erika5": "Челадон Мансион$",
    "gFameCheckerFlavorTextOriginLocation_Koga0": "Город Фуксии$",
    "gFameCheckerFlavorTextOriginLocation_Koga1": "ДЖИМ КУЧШИ$",
    "gFameCheckerFlavorTextOriginLocation_Koga2": "ДЖИМ КУЧШИ$",
    "gFameCheckerFlavorTextOriginLocation_Koga3": "Город Фуксии$",
    "gFameCheckerFlavorTextOriginLocation_Koga4": "Город Фуксии$",
    "gFameCheckerFlavorTextOriginLocation_Koga5": "Зона Сафари$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina0": "Город САФФРОНА$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina1": "Три острова$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina2": "САФФРОН ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina3": "САФФРОН ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina4": "Город САФФРОНА$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina5": "САФФРОН ГИМ$",
}
TRANSLATIONS = {
    "gFameCheckerFlavorTextOriginLocation_LtSurge0": "ВЕРМИЛИОН$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge1": "ВЕРМИЛИОНСКИЙ ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge2": "ВЕРМИЛИОНСКИЙ ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge3": "ВЕРМИЛИОНСКИЙ ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge4": "ВЕРМИЛИОНСКИЙ ГИМ$",
    "gFameCheckerFlavorTextOriginLocation_LtSurge5": "ВЕРМИЛИОН$",
    "gFameCheckerFlavorTextOriginLocation_Erika0": "СЕЛАДОН$",
    "gFameCheckerFlavorTextOriginLocation_Erika1": "ГИМ СЕЛАДОНА$",
    "gFameCheckerFlavorTextOriginLocation_Erika2": "ГИМ СЕЛАДОНА$",
    "gFameCheckerFlavorTextOriginLocation_Erika3": "ГИМ СЕЛАДОНА$",
    "gFameCheckerFlavorTextOriginLocation_Erika4": "ГИМ СЕЛАДОНА$",
    "gFameCheckerFlavorTextOriginLocation_Erika5": "ОСОБНЯК СЕЛАДОНА$",
    "gFameCheckerFlavorTextOriginLocation_Koga0": "ФУКСИЯ$",
    "gFameCheckerFlavorTextOriginLocation_Koga1": "ГИМ ФУКСИИ$",
    "gFameCheckerFlavorTextOriginLocation_Koga2": "ГИМ ФУКСИИ$",
    "gFameCheckerFlavorTextOriginLocation_Koga3": "ФУКСИЯ$",
    "gFameCheckerFlavorTextOriginLocation_Koga4": "ФУКСИЯ$",
    "gFameCheckerFlavorTextOriginLocation_Koga5": "ЗОНА САФАРИ$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina0": "САФФРОН$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina1": "ОСТРОВ 3$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina2": "ГИМ САФФРОНА$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina3": "ГИМ САФФРОНА$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina4": "САФФРОН$",
    "gFameCheckerFlavorTextOriginLocation_Sabrina5": "ГИМ САФФРОНА$",
}
BANNED_UNICODE = set("—–←→“”«»…")

def replace_entry(text: str, label: str, expected: str, translated: str) -> str:
    pattern = re.compile(rf'(?m)^(?P<label>{re.escape(label)}::[^\n]*\n)(?P<prefix>\s*\.string ")(?P<body>(?:\\.|[^"\\])*)(?P<suffix>"\s*)$')
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
    return text[:match.start()] + match.group("label") + match.group("prefix") + translated + match.group("suffix") + text[match.end():]

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_fame_checker_locations_surge_sabrina_quality_v3_220.py <upstream-root>")
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 24:
        raise RuntimeError("unexpected v3.220 Fame Checker location set")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")
    text = path.read_text(encoding="utf-8")
    for label in EXPECTED:
        text = replace_entry(text, label, EXPECTED[label], TRANSLATIONS[label])
    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_fame_checker_locations_surge_sabrina_quality_v3_220_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "targetFile": str(TARGET), "qualityPassStrings": len(TRANSLATIONS), "humanEditedRussian": True, "sourceAnchorsFailClosed": True, "singleStringLabelsOnly": True, "projectLocationNamingReused": True, "gameplayLogicTouched": False, "balanceTouched": False, "bossTeamsTouched": False, "specialWhitelistTouched": False, "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    next_script = Path(__file__).with_name("localize_fame_checker_locations_blaine_lorelei_quality_v3_221.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    print(f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Fame Checker location labels; chained v3.221")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
