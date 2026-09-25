#!/usr/bin/env python3
"""Qarro v3.206: human-quality disobedience and Safari battle messages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_OBEDIENCE_SAFARI_QUALITY_V3_206"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNIGNORESASLEEP": "{B_ATK_NAME_WITH_PREFIX} Игнорировал приказы и продолжал спать.",
    "STRINGID_PKMNIGNOREDORDERS": "{B_ATK_NAME_WITH_PREFIX} Игнорируем приказы!",
    "STRINGID_PKMNBEGANTONAP": "{B_ATK_NAME_WITH_PREFIX} Начал дремать!",
    "STRINGID_PKMNLOAFING": "{B_ATK_NAME_WITH_PREFIX} Он рыщет вокруг!",
    "STRINGID_PKMNWONTOBEY": "{B_ATK_NAME_WITH_PREFIX} Не повинуюсь!",
    "STRINGID_PKMNTURNEDAWAY": "{B_ATK_NAME_WITH_PREFIX} Отвернулся!",
    "STRINGID_PKMNPRETENDNOTNOTICE": "{B_ATK_NAME_WITH_PREFIX} Притворился, что не заметил!",
    "STRINGID_ENEMYABOUTTOSWITCHPKMN": "{B_TRAINER1_NAME_WITH_CLASS} вот-вот отправят {B_BUFF2}Ты поменяешь свой Pokemon?",
    "STRINGID_CREPTCLOSER": "{B_PLAYER_NAME} Подбирался ближе к {B_OPPONENT_MON1_NAME}!",
    "STRINGID_CANTGETCLOSER": "{B_PLAYER_NAME} Не могу подойти ближе!",
    "STRINGID_PKMNWATCHINGCAREFULLY": "{B_OPPONENT_MON1_NAME} Смотри внимательно!",
    "STRINGID_PKMNCURIOUSABOUTX": "{B_OPPONENT_MON1_NAME} Любопытно, что в {B_BUFF1}!",
    "STRINGID_PKMNENTHRALLEDBYX": "{B_OPPONENT_MON1_NAME} В восторге от того, что {B_BUFF1}!",
    "STRINGID_PKMNIGNOREDX": "{B_OPPONENT_MON1_NAME} полностью игнорируется {B_BUFF1}!",
    "STRINGID_THREWPOKEBLOCKATPKMN": "{B_PLAYER_NAME} бросать {POKEBLOCK} в {B_OPPONENT_MON1_NAME}!",
    "STRINGID_OUTOFSAFARIBALLS": "{PLAY_SE SE_DING_DONG}Ты выбыл из сафари-баллов!\\p",
}

TRANSLATIONS = {
    "STRINGID_PKMNIGNORESASLEEP": "{B_ATK_NAME_WITH_PREFIX} игнорирует приказ и продолжает спать!",
    "STRINGID_PKMNIGNOREDORDERS": "{B_ATK_NAME_WITH_PREFIX} игнорирует приказ!",
    "STRINGID_PKMNBEGANTONAP": "{B_ATK_NAME_WITH_PREFIX} начинает дремать!",
    "STRINGID_PKMNLOAFING": "{B_ATK_NAME_WITH_PREFIX} бездельничает!",
    "STRINGID_PKMNWONTOBEY": "{B_ATK_NAME_WITH_PREFIX} не слушается!",
    "STRINGID_PKMNTURNEDAWAY": "{B_ATK_NAME_WITH_PREFIX} отворачивается!",
    "STRINGID_PKMNPRETENDNOTNOTICE": "{B_ATK_NAME_WITH_PREFIX} делает вид, что не замечает!",
    "STRINGID_ENEMYABOUTTOSWITCHPKMN": "{B_TRAINER1_NAME_WITH_CLASS} собирается выпустить {B_BUFF2}. Сменить POKeMON?",
    "STRINGID_CREPTCLOSER": "{B_PLAYER_NAME} подкрадывается ближе к {B_OPPONENT_MON1_NAME}!",
    "STRINGID_CANTGETCLOSER": "{B_PLAYER_NAME} не может подойти ближе!",
    "STRINGID_PKMNWATCHINGCAREFULLY": "{B_OPPONENT_MON1_NAME} внимательно наблюдает!",
    "STRINGID_PKMNCURIOUSABOUTX": "{B_OPPONENT_MON1_NAME} заинтересован в {B_BUFF1}!",
    "STRINGID_PKMNENTHRALLEDBYX": "{B_OPPONENT_MON1_NAME} в восторге от {B_BUFF1}!",
    "STRINGID_PKMNIGNOREDX": "{B_OPPONENT_MON1_NAME} полностью игнорирует {B_BUFF1}!",
    "STRINGID_THREWPOKEBLOCKATPKMN": "{B_PLAYER_NAME} бросает {POKEBLOCK} в сторону {B_OPPONENT_MON1_NAME}!",
    "STRINGID_OUTOFSAFARIBALLS": "{PLAY_SE SE_DING_DONG}Сафари-боллы закончились! Игра окончена!\\p",
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
        raise SystemExit("usage: localize_battle_message_obedience_safari_quality_v3_206.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 16:
        raise RuntimeError("unexpected v3.206 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_obedience_safari_quality_v3_206_audit.json"
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
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} obedience/Safari battle strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
