#!/usr/bin/env python3
"""Qarro v3.211: human-quality repolish for remaining battle weather phrasing."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_WEATHER_REPOLISH_V3_211"
TARGET = Path("src/battle_message.c")
REPLACEMENTS = [
    ("Песчаная буря стихла.", "Песчаная буря утихла."),
    ("Пошёл дождь!", "Начался дождь!"),
    ("Солнечный свет стал ярче!", "Солнце засияло ярче!"),
]

def control_tokens(text: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", text)

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_battle_weather_repolish_v3_211.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"v3.211 anchor drift: {old!r} count={count}")
        if control_tokens(old) != control_tokens(new):
            raise RuntimeError(f"v3.211 control-token drift: {old!r}")
        text = text.replace(old, new, 1)
    if text == original:
        raise RuntimeError("v3.211 made no changes")
    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_battle_weather_repolish_v3_211_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(REPLACEMENTS),
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
    print(f"[{MARKER}] PASS: repolished {len(REPLACEMENTS)} battle weather strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
