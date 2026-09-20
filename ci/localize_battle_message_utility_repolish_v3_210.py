#!/usr/bin/env python3
"""Qarro v3.210: second human-polish pass for awkward battle utility phrasing."""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_UTILITY_REPOLISH_V3_210"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNCHOSEXASDESTINY": "{B_ATK_NAME_WITH_PREFIX} выбирает Doom Desire своей судьбой!",
    "STRINGID_PKMNSXWOREOFF": "{B_ATK_TEAM1} сторона: действие {B_BUFF1} заканчивается!",
    "STRINGID_PKMNSXCUREDITSYPROBLEM": "{B_SCR_NAME_WITH_PREFIX}: {B_SCR_ABILITY} устраняет состояние {B_BUFF1}!",
}

TRANSLATIONS = {
    "STRINGID_PKMNCHOSEXASDESTINY": "{B_ATK_NAME_WITH_PREFIX} вверяет судьбу Doom Desire!",
    "STRINGID_PKMNSXWOREOFF": "На стороне {B_ATK_TEAM1} заканчивается действие {B_BUFF1}!",
    "STRINGID_PKMNSXCUREDITSYPROBLEM": "{B_SCR_NAME_WITH_PREFIX}: {B_SCR_ABILITY} избавляет от {B_BUFF1}!",
}

BANNED_UNICODE = set("—–←→“”«»")

def control_tokens(text: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", text)

def replace_entry(path: Path, string_id: str, expected: str, translated: str) -> None:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(?m)^(?P<prefix>\s*\[{re.escape(string_id)}\]\s*=\s*COMPOUND_STRING\(")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\),(?:\s*//.*)?\s*)$'
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{string_id}: expected one table entry, got {len(matches)}")
    m = matches[0]
    current = m.group("body")
    if current != expected:
        raise RuntimeError(f"{string_id}: source drift: {current!r} != {expected!r}")
    if control_tokens(current) != control_tokens(translated):
        raise RuntimeError(f"{string_id}: control-token drift")
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{string_id}: invalid translation surface")
    path.write_text(text[:m.start()] + m.group("prefix") + translated + m.group("suffix") + text[m.end():], encoding="utf-8")

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_battle_message_utility_repolish_v3_210.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 3:
        raise RuntimeError("unexpected v3.210 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_utility_repolish_v3_210_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "humanEditedRussian": True,
        "sourceAnchorsFailClosed": True,
        "controlTokensPreserved": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    next_script = Path(__file__).with_name("localize_battle_weather_repolish_v3_211.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    print(f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} battle utility strings; chained v3.211")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
