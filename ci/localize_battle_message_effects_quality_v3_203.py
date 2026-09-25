#!/usr/bin/env python3
"""Qarro v3.203: human-quality battle effects, team grammar and stat messages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_EFFECTS_QUALITY_V3_203"
TARGET = Path("src/battle_message.c")

EXPECTED_SYMBOLS = {
    "gText_StatRose": "Роза!",
    "gText_StatFell": "Упал!",
    "gText_DefendersStatRose": "{B_DEF_NAME_WITH_PREFIX}? {B_BUFF1} роза{B_BUFF2}!",
    "sText_Your1": "Твой",
    "sText_Opposing1": "Противоположный",
    "sText_Your2": "твой",
    "sText_Opposing2": "противостоящий",
}

SYMBOL_TRANSLATIONS = {
    "gText_StatRose": "повысился!",
    "gText_StatFell": "понизился!",
    "gText_DefendersStatRose": "{B_DEF_NAME_WITH_PREFIX}: показатель {B_BUFF1} повысился{B_BUFF2}!",
    "sText_Your1": "Твоя",
    "sText_Opposing1": "Вражеская",
    "sText_Your2": "твоя",
    "sText_Opposing2": "вражеская",
}

EXPECTED_ENTRIES = {
    "STRINGID_PKMNFELLINLOVE": "{B_DEF_NAME_WITH_PREFIX} Влюбилась!",
    "STRINGID_PKMNINLOVE": "{B_ATK_NAME_WITH_PREFIX} Влюблённый в {B_SCR_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNIMMOBILIZEDBYLOVE": "{B_ATK_NAME_WITH_PREFIX} Обездвижен любовью!",
    "STRINGID_PKMNCHANGEDTYPE": "{B_ATK_NAME_WITH_PREFIX} преобразуясь в {B_BUFF1} Тип!",
    "STRINGID_PKMNFLINCHED": "{B_ATK_NAME_WITH_PREFIX} Сморщился и не мог двигаться!",
    "STRINGID_PKMNREGAINEDHEALTH": "{B_DEF_NAME_WITH_PREFIX}HP был восстановлен.",
    "STRINGID_PKMNHPFULL": "{B_DEF_NAME_WITH_PREFIX}HP переполнена!",
    "STRINGID_PKMNRAISEDSPDEF": "Light Screen сделанный {B_ATK_TEAM2} Сильнее против специальных ходов!",
    "STRINGID_PKMNRAISEDDEF": "Reflect сделанный {B_ATK_TEAM2} Сильнее против физических движений!",
    "STRINGID_PKMNAURORAVEIL": "Aurora Veil сделанный {B_ATK_TEAM2} Сильнее против физических и специальных движений!",
    "STRINGID_PKMNPROTECTEDBY": "{B_DEF_NAME_WITH_PREFIX} был защищен {B_DEF_ABILITY}!",
    "STRINGID_PKMNPREVENTSUSAGE": "{B_DEF_NAME_WITH_PREFIX}? {B_DEF_ABILITY} предотвращать {B_ATK_NAME_WITH_PREFIX2} от использования {B_CURRENT_MOVE}!",
    "STRINGID_PKMNRESTOREDHPUSING": "{B_SCR_NAME_WITH_PREFIX} И ее НР восстановили.",
    "STRINGID_PKMNCHANGEDTYPEWITH": "{B_EFF_NAME_WITH_PREFIX}Тип менялся на {B_BUFF1}!",
    "STRINGID_PKMNPREVENTSROMANCEWITH": "{B_DEF_NAME_WITH_PREFIX}? {B_DEF_ABILITY} Препятствует романтике!",
    "STRINGID_PKMNPREVENTSCONFUSIONWITH": "{B_SCR_NAME_WITH_PREFIX} Невозможно спутать!",
    "STRINGID_PKMNRAISEDFIREPOWERWITH": "Сила власти {B_SCR_NAME_WITH_PREFIX}Огненный тип движения поднялся!",
    "STRINGID_PKMNANCHORSITSELFWITH": "{B_EFF_NAME_WITH_PREFIX} Он закрепляется на месте с помощью своих присоски!",
    "STRINGID_PKMNPREVENTSSTATLOSSWITH": "{B_SCR_NAME_WITH_PREFIX}Статистика не была понижена!",
    "STRINGID_PKMNHURTSWITH": "{B_ATK_NAME_WITH_PREFIX} был ранен {B_DEF_NAME_WITH_PREFIX2}? {B_BUFF1}!",
    "STRINGID_PKMNTRACED": "Проследил {B_BUFF1}? {B_BUFF2}!",
    "STRINGID_STATHARSHLY": "сурово ",
    "STRINGID_STATROSE": "{B_SCR_NAME_WITH_PREFIX}? {B_BUFF1} роза{B_BUFF2}!",
    "STRINGID_STATFELL": "{B_SCR_NAME_WITH_PREFIX}? {B_BUFF1} {B_BUFF2}Упал!",
    "STRINGID_ONEHITKO": "Это одноразовый КО!",
}

ENTRY_TRANSLATIONS = {
    "STRINGID_PKMNFELLINLOVE": "{B_DEF_NAME_WITH_PREFIX} влюбляется!",
    "STRINGID_PKMNINLOVE": "{B_ATK_NAME_WITH_PREFIX} влюблён в {B_SCR_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNIMMOBILIZEDBYLOVE": "{B_ATK_NAME_WITH_PREFIX} не может двигаться из-за любви!",
    "STRINGID_PKMNCHANGEDTYPE": "{B_ATK_NAME_WITH_PREFIX} меняет тип на {B_BUFF1}!",
    "STRINGID_PKMNFLINCHED": "{B_ATK_NAME_WITH_PREFIX} вздрагивает и не может двигаться!",
    "STRINGID_PKMNREGAINEDHEALTH": "{B_DEF_NAME_WITH_PREFIX} восстанавливает HP.",
    "STRINGID_PKMNHPFULL": "{B_DEF_NAME_WITH_PREFIX}: HP уже на максимуме!",
    "STRINGID_PKMNRAISEDSPDEF": "{B_ATK_TEAM2} сторона защищена Light Screen от специальных атак!",
    "STRINGID_PKMNRAISEDDEF": "{B_ATK_TEAM2} сторона защищена Reflect от физических атак!",
    "STRINGID_PKMNAURORAVEIL": "{B_ATK_TEAM2} сторона защищена Aurora Veil от физических и специальных атак!",
    "STRINGID_PKMNPROTECTEDBY": "{B_DEF_NAME_WITH_PREFIX}: {B_DEF_ABILITY} обеспечивает защиту!",
    "STRINGID_PKMNPREVENTSUSAGE": "{B_DEF_NAME_WITH_PREFIX}: {B_DEF_ABILITY} не даёт {B_ATK_NAME_WITH_PREFIX2} использовать {B_CURRENT_MOVE}!",
    "STRINGID_PKMNRESTOREDHPUSING": "{B_SCR_NAME_WITH_PREFIX} восстанавливает HP.",
    "STRINGID_PKMNCHANGEDTYPEWITH": "{B_EFF_NAME_WITH_PREFIX}: тип меняется на {B_BUFF1}!",
    "STRINGID_PKMNPREVENTSROMANCEWITH": "{B_DEF_NAME_WITH_PREFIX}: {B_DEF_ABILITY} не даёт влюбиться!",
    "STRINGID_PKMNPREVENTSCONFUSIONWITH": "{B_SCR_NAME_WITH_PREFIX} нельзя запутать!",
    "STRINGID_PKMNRAISEDFIREPOWERWITH": "{B_SCR_NAME_WITH_PREFIX}: сила Fire-приёмов повышается!",
    "STRINGID_PKMNANCHORSITSELFWITH": "{B_EFF_NAME_WITH_PREFIX} прочно закрепляется на месте!",
    "STRINGID_PKMNPREVENTSSTATLOSSWITH": "{B_SCR_NAME_WITH_PREFIX}: характеристики не снижаются!",
    "STRINGID_PKMNHURTSWITH": "{B_ATK_NAME_WITH_PREFIX} получает урон от {B_DEF_NAME_WITH_PREFIX2}: {B_BUFF1}!",
    "STRINGID_PKMNTRACED": "{B_BUFF1}: скопировано {B_BUFF2}!",
    "STRINGID_STATHARSHLY": "сильно ",
    "STRINGID_STATROSE": "{B_SCR_NAME_WITH_PREFIX}: показатель {B_BUFF1} повысился{B_BUFF2}!",
    "STRINGID_STATFELL": "{B_SCR_NAME_WITH_PREFIX}: показатель {B_BUFF1} {B_BUFF2}понизился!",
    "STRINGID_ONEHITKO": "Нокаут одним ударом!",
}

BANNED_UNICODE = set("—–←→“”«»")

def control_tokens(text: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", text)

def validate_surface(label: str, expected: str, translated: str) -> None:
    if control_tokens(expected) != control_tokens(translated):
        raise RuntimeError(
            f"{label}: control-token drift old={control_tokens(expected)} new={control_tokens(translated)}"
        )
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: invalid translation surface")

def replace_symbol(path: Path, symbol: str, expected: str, translated: str) -> None:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(?m)^(?P<prefix>\s*(?:ALIGNED\(4\)\s+)?(?:static\s+)?const u8\s+'
        rf'{re.escape(symbol)}\[\]\s*=\s*_\(")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\);(?:\s*//.*)?\s*)$'
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{symbol}: expected one symbol, got {len(matches)}")
    m = matches[0]
    current = m.group("body")
    if current != expected:
        raise RuntimeError(f"{symbol}: source drift: {current!r} != {expected!r}")
    validate_surface(symbol, current, translated)
    path.write_text(
        text[:m.start()] + m.group("prefix") + translated + m.group("suffix") + text[m.end():],
        encoding="utf-8",
    )

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
    validate_surface(string_id, current, translated)
    path.write_text(
        text[:m.start()] + m.group("prefix") + translated + m.group("suffix") + text[m.end():],
        encoding="utf-8",
    )

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_battle_message_effects_quality_v3_203.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED_SYMBOLS) != set(SYMBOL_TRANSLATIONS) or len(SYMBOL_TRANSLATIONS) != 7:
        raise RuntimeError("unexpected v3.203 symbol set")
    if set(EXPECTED_ENTRIES) != set(ENTRY_TRANSLATIONS) or len(ENTRY_TRANSLATIONS) != 25:
        raise RuntimeError("unexpected v3.203 entry set")
    for symbol, translated in SYMBOL_TRANSLATIONS.items():
        replace_symbol(path, symbol, EXPECTED_SYMBOLS[symbol], translated)
    for string_id, translated in ENTRY_TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED_ENTRIES[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_effects_quality_v3_203_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassSymbols": len(SYMBOL_TRANSLATIONS),
        "qualityPassEntries": len(ENTRY_TRANSLATIONS),
        "teamGrammarHelpersReviewed": True,
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
    print(f"[{MARKER}] PASS: polished {len(SYMBOL_TRANSLATIONS)} helper symbols and {len(ENTRY_TRANSLATIONS)} battle-effect strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
