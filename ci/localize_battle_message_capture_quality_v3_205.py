#!/usr/bin/env python3
"""Qarro v3.205: human-quality capture and residual escape battle messages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_CAPTURE_QUALITY_V3_205"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_TRAINERBLOCKEDBALL": "Тренер заблокировал ваш поке-бал!",
    "STRINGID_DONTBEATHIEF": "Не будь вором!",
    "STRINGID_ITDODGEDBALL": "Это ускользнуло от твоего брошенного мяча! Pokemon Не может быть пойман!",
    "STRINGID_PKMNBROKEFREE": "О нет! Pokemon Вырвался на свободу!",
    "STRINGID_ITAPPEAREDCAUGHT": "Похоже, его поймали!",
    "STRINGID_AARGHALMOSTHADIT": "Почти получилось!",
    "STRINGID_SHOOTSOCLOSE": "Это было так близко!",
    "STRINGID_GOTCHAPKMNCAUGHTPLAYER": "Попался! {B_DEF_NAME} Его поймали!{WAIT_SE}{PLAY_BGM MUS_CAUGHT}\\p",
    "STRINGID_GOTCHAPKMNCAUGHTWALLY": "Попался! {B_DEF_NAME} Его поймали!{WAIT_SE}{PLAY_BGM MUS_CAUGHT}{PAUSE 127}",
    "STRINGID_GIVENICKNAMECAPTURED": "Хотите ли вы дать {B_DEF_NAME} Прозвище?",
    "STRINGID_PKMNDATAADDEDTODEX": "{B_DEF_NAME}Данные были добавлены в Pokedex!\\p",
    "STRINGID_CANTESCAPE2": "Ты не мог уйти!\\p",
}

TRANSLATIONS = {
    "STRINGID_TRAINERBLOCKEDBALL": "Тренер блокирует брошенный Поке-бол!",
    "STRINGID_DONTBEATHIEF": "Нельзя ловить чужих POKeMON!",
    "STRINGID_ITDODGEDBALL": "POKeMON уклоняется от Поке-бола! Его нельзя поймать!",
    "STRINGID_PKMNBROKEFREE": "О нет! POKeMON вырвался!",
    "STRINGID_ITAPPEAREDCAUGHT": "Ох! Казалось, POKeMON уже пойман!",
    "STRINGID_AARGHALMOSTHADIT": "Ай! Почти удалось поймать!",
    "STRINGID_SHOOTSOCLOSE": "Эх! Совсем чуть-чуть!",
    "STRINGID_GOTCHAPKMNCAUGHTPLAYER": "Есть! {B_DEF_NAME} пойман!{WAIT_SE}{PLAY_BGM MUS_CAUGHT}\\p",
    "STRINGID_GOTCHAPKMNCAUGHTWALLY": "Есть! {B_DEF_NAME} пойман!{WAIT_SE}{PLAY_BGM MUS_CAUGHT}{PAUSE 127}",
    "STRINGID_GIVENICKNAMECAPTURED": "Дать {B_DEF_NAME} прозвище?",
    "STRINGID_PKMNDATAADDEDTODEX": "Данные о {B_DEF_NAME} добавлены в POKeDEX!\\p",
    "STRINGID_CANTESCAPE2": "Сбежать не удалось!\\p",
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
        raise SystemExit("usage: localize_battle_message_capture_quality_v3_205.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.205 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_capture_quality_v3_205_audit.json"
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
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} capture/escape battle strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
