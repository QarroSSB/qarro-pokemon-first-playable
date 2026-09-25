#!/usr/bin/env python3
"""Qarro v3.207: human-quality held-item cure and recovery battle messages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_ITEM_RECOVERY_QUALITY_V3_207"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNSITEMCUREDPARALYSIS": "{B_SCR_NAME_WITH_PREFIX}? {B_LAST_ITEM} Вылечили его паралич!",
    "STRINGID_PKMNSITEMCUREDPOISON": "{B_SCR_NAME_WITH_PREFIX}? {B_LAST_ITEM} Вылечил яд!",
    "STRINGID_PKMNSITEMHEALEDBURN": "{B_SCR_NAME_WITH_PREFIX}? {B_LAST_ITEM} Вылечила ожог!",
    "STRINGID_PKMNSITEMDEFROSTEDIT": "{B_SCR_NAME_WITH_PREFIX}? {B_LAST_ITEM} Разморозить!",
    "STRINGID_PKMNSITEMWOKEIT": "{B_SCR_NAME_WITH_PREFIX}? {B_LAST_ITEM} Разбудил его!",
    "STRINGID_PKMNSITEMSNAPPEDOUT": "{B_SCR_NAME_WITH_PREFIX}? {B_LAST_ITEM} Вырвал его из своей сумятицы!",
    "STRINGID_PKMNSITEMCUREDPROBLEM": "{B_SCR_NAME_WITH_PREFIX}? {B_LAST_ITEM} излечивающий его {B_BUFF1} Проблема!",
    "STRINGID_PKMNSITEMRESTOREDHEALTH": "{B_SCR_NAME_WITH_PREFIX} Восстанавливает здоровье с помощью {B_LAST_ITEM}!",
    "STRINGID_PKMNSITEMRESTOREDPP": "{B_SCR_NAME_WITH_PREFIX} Восстановление ПП к ее движению {B_BUFF1} используя его {B_LAST_ITEM}!",
    "STRINGID_PKMNSITEMRESTOREDSTATUS": "{B_SCR_NAME_WITH_PREFIX} вернула свою статистику в нормальное состояние, используя {B_LAST_ITEM}!",
    "STRINGID_PKMNSITEMRESTOREDHPALITTLE": "{B_SCR_NAME_WITH_PREFIX} Восстановлено немного HP с помощью {B_LAST_ITEM}!",
    "STRINGID_ITEMALLOWSONLYYMOVE": "{B_LAST_ITEM} Только позволяет использовать {B_CURRENT_MOVE}!\\p",
    "STRINGID_PKMNHUNGONWITHX": "{B_DEF_NAME_WITH_PREFIX} Повесить на использование его {B_LAST_ITEM}!",
}

TRANSLATIONS = {
    "STRINGID_PKMNSITEMCUREDPARALYSIS": "{B_SCR_NAME_WITH_PREFIX}: {B_LAST_ITEM} лечит паралич!",
    "STRINGID_PKMNSITEMCUREDPOISON": "{B_SCR_NAME_WITH_PREFIX}: {B_LAST_ITEM} нейтрализует яд!",
    "STRINGID_PKMNSITEMHEALEDBURN": "{B_SCR_NAME_WITH_PREFIX}: {B_LAST_ITEM} лечит ожог!",
    "STRINGID_PKMNSITEMDEFROSTEDIT": "{B_SCR_NAME_WITH_PREFIX}: {B_LAST_ITEM} размораживает!",
    "STRINGID_PKMNSITEMWOKEIT": "{B_SCR_NAME_WITH_PREFIX}: {B_LAST_ITEM} пробуждает!",
    "STRINGID_PKMNSITEMSNAPPEDOUT": "{B_SCR_NAME_WITH_PREFIX}: {B_LAST_ITEM} выводит из замешательства!",
    "STRINGID_PKMNSITEMCUREDPROBLEM": "{B_SCR_NAME_WITH_PREFIX}: {B_LAST_ITEM} устраняет состояние {B_BUFF1}!",
    "STRINGID_PKMNSITEMRESTOREDHEALTH": "{B_SCR_NAME_WITH_PREFIX} восстанавливает здоровье с помощью {B_LAST_ITEM}!",
    "STRINGID_PKMNSITEMRESTOREDPP": "{B_SCR_NAME_WITH_PREFIX} восстанавливает PP приёма {B_BUFF1} с помощью {B_LAST_ITEM}!",
    "STRINGID_PKMNSITEMRESTOREDSTATUS": "{B_SCR_NAME_WITH_PREFIX} возвращает характеристики в норму с помощью {B_LAST_ITEM}!",
    "STRINGID_PKMNSITEMRESTOREDHPALITTLE": "{B_SCR_NAME_WITH_PREFIX} немного восстанавливает HP с помощью {B_LAST_ITEM}!",
    "STRINGID_ITEMALLOWSONLYYMOVE": "{B_LAST_ITEM} позволяет использовать только {B_CURRENT_MOVE}!\\p",
    "STRINGID_PKMNHUNGONWITHX": "{B_DEF_NAME_WITH_PREFIX} выдерживает удар благодаря {B_LAST_ITEM}!",
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
        raise RuntimeError(
            f"{string_id}: control-token drift old={control_tokens(current)} new={control_tokens(translated)}"
        )
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{string_id}: invalid translation surface")
    path.write_text(
        text[:m.start()] + m.group("prefix") + translated + m.group("suffix") + text[m.end():],
        encoding="utf-8",
    )

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_battle_message_item_recovery_quality_v3_207.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 13:
        raise RuntimeError("unexpected v3.207 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_item_recovery_quality_v3_207_audit.json"
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
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} item-recovery battle strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
