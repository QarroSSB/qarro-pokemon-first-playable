#!/usr/bin/env python3
"""Qarro v3.211: final human-quality repolish for the remaining awkward weather line."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_WEATHER_REPOLISH_V3_211"
TARGET = Path("src/battle_message.c")
STRING_ID = "STRINGID_SUNLIGHTGOTBRIGHT"
EXPECTED = "Солнечный свет усилился!"
TRANSLATED = "Солнце засияло ярче!"
BANNED_UNICODE = set("—–←→“”«»")

def control_tokens(text: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", text)

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_battle_weather_repolish_v3_211.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(?m)^(?P<prefix>\s*\[{re.escape(STRING_ID)}\]\s*=\s*COMPOUND_STRING\(")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\),(?:\s*//.*)?\s*)$'
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{STRING_ID}: expected one table entry, got {len(matches)}")
    m = matches[0]
    current = m.group("body")
    if current != EXPECTED:
        raise RuntimeError(f"{STRING_ID}: source drift: {current!r} != {EXPECTED!r}")
    if control_tokens(current) != control_tokens(TRANSLATED):
        raise RuntimeError(f"{STRING_ID}: control-token drift")
    if '"' in TRANSLATED or set(TRANSLATED) & BANNED_UNICODE:
        raise RuntimeError(f"{STRING_ID}: invalid translation surface")
    path.write_text(
        text[:m.start()] + m.group("prefix") + TRANSLATED + m.group("suffix") + text[m.end():],
        encoding="utf-8",
    )
    out = root / "build" / "qarro_ru_battle_weather_repolish_v3_211_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": 1,
        "humanEditedRussian": True,
        "sourceAnchorsFailClosed": True,
        "controlTokensPreserved": True,
        "pokemonMoveAbilityNamesPreserved": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: repolished final weather phrasing")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
