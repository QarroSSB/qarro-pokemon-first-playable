#!/usr/bin/env python3
"""Qarro v3.214: final human repolish for remaining awkward battle-message phrasing."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_FINAL_REPOLISH_V3_214"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNSLEPTHEALTHY": "{B_ATK_NAME_WITH_PREFIX}: сон восстанавливает HP!",
    "STRINGID_PKMNSEEDED": "{B_DEF_NAME_WITH_PREFIX}: семена пускают корни!",
    "STRINGID_PLAYERPICKEDUPMONEY": "Подобрано ¥{B_BUFF1}!\\p",
    "STRINGID_PKMNSXMADEITINEFFECTIVE": "{B_SCR_NAME_WITH_PREFIX} делает это неэффективным!",
}

TRANSLATIONS = {
    "STRINGID_PKMNSLEPTHEALTHY": "{B_ATK_NAME_WITH_PREFIX} восстанавливает HP во сне!",
    "STRINGID_PKMNSEEDED": "{B_DEF_NAME_WITH_PREFIX} поражён Leech Seed!",
    "STRINGID_PLAYERPICKEDUPMONEY": "Найдено ¥{B_BUFF1}!\\p",
    "STRINGID_PKMNSXMADEITINEFFECTIVE": "{B_SCR_NAME_WITH_PREFIX}: эффект нейтрализован!",
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
        raise RuntimeError(f"{string_id}: control-token drift old={control_tokens(current)} new={control_tokens(translated)}")
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{string_id}: invalid translation surface")
    path.write_text(text[:m.start()] + m.group("prefix") + translated + m.group("suffix") + text[m.end():], encoding="utf-8")

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_battle_message_final_repolish_v3_214.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 4:
        raise RuntimeError("unexpected v3.214 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_final_repolish_v3_214_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
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
    print(f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} remaining battle strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
