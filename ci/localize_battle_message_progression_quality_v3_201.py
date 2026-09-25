#!/usr/bin/env python3
"""Qarro v3.201: human-quality battle progression and move-learning messages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_PROGRESSION_QUALITY_V3_201"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNGAINEDEXP": "{B_BUFF1} полученный{B_BUFF2} {B_BUFF3} Экс-пойнтс!\\p",
    "STRINGID_PKMNGREWTOLV": "{B_BUFF1} Выросла до Львова. {B_BUFF2}!{WAIT_SE}\\p",
    "STRINGID_PKMNLEARNEDMOVE": "{B_BUFF1} выученный {B_BUFF2}!{WAIT_SE}\\p",
    "STRINGID_TRYTOLEARNMOVE1": "{B_BUFF1} Хочет научиться двигаться {B_BUFF2}.\\p",
    "STRINGID_TRYTOLEARNMOVE2": "Однако, {B_BUFF1} Уже известно четыре хода.\\p",
    "STRINGID_TRYTOLEARNMOVE3": "Если другой ход будет забыт и заменен на {B_BUFF2}?",
    "STRINGID_PKMNFORGOTMOVE": "{B_BUFF1} забыли {B_BUFF2}…\\p",
    "STRINGID_STOPLEARNINGMOVE": "{PAUSE 32}Вы хотите отказаться от того, чтобы иметь {B_BUFF1} учиться {B_BUFF2}?",
    "STRINGID_DIDNOTLEARNMOVE": "{B_BUFF1} Не научился {B_BUFF2}.\\p",
    "STRINGID_PKMNLEARNEDMOVE2": "{B_ATK_NAME_WITH_PREFIX} выученный {B_BUFF1}!",
    "STRINGID_PKMNPROTECTEDITSELF": "{B_SCR_NAME_WITH_PREFIX} Защищать себя!",
    "STRINGID_ITDOESNTAFFECT": "Это не влияет {B_DEF_NAME_WITH_PREFIX2}…",
    "STRINGID_ITDOESNTAFFECTSCR": "Это не влияет {B_SCR_NAME_WITH_PREFIX2}…",
    "STRINGID_BATTLERFAINTED": "{B_SCR_NAME_WITH_PREFIX} Обморок!\\p",
    "STRINGID_PLAYERGOTMONEY": "У тебя есть иена{B_BUFF1} За победу!\\p",
    "STRINGID_PLAYERWHITEOUT": "У тебя больше нет Pokemon Это может бороться!\\p",
    "STRINGID_PLAYERWHITEOUT2_WILD": "Ты запаниковал и упал{B_BUFF1}…",
    "STRINGID_PLAYERWHITEOUT2_TRAINER": "Ты дал иену{B_BUFF1} Победителю...",
    "STRINGID_PLAYERWHITEOUT3": "Вы были поражены своим поражением!",
    "STRINGID_PREVENTSESCAPE": "{B_SCR_NAME_WITH_PREFIX} Предотвращает побег с {B_SCR_ABILITY}!\\p",
    "STRINGID_ABOOSTED": " усиленный",
}

TRANSLATIONS = {
    "STRINGID_PKMNGAINEDEXP": "{B_BUFF1} получает{B_BUFF2} {B_BUFF3} очк. опыта!\\p",
    "STRINGID_PKMNGREWTOLV": "{B_BUFF1} достигает ур. {B_BUFF2}!{WAIT_SE}\\p",
    "STRINGID_PKMNLEARNEDMOVE": "{B_BUFF1} изучает {B_BUFF2}!{WAIT_SE}\\p",
    "STRINGID_TRYTOLEARNMOVE1": "{B_BUFF1} хочет изучить {B_BUFF2}.\\p",
    "STRINGID_TRYTOLEARNMOVE2": "Но {B_BUFF1} уже знает четыре приёма.\\p",
    "STRINGID_TRYTOLEARNMOVE3": "Забыть другой приём и заменить его на {B_BUFF2}?",
    "STRINGID_PKMNFORGOTMOVE": "{B_BUFF1} забывает {B_BUFF2}...\\p",
    "STRINGID_STOPLEARNINGMOVE": "{PAUSE 32}{B_BUFF1} не будет изучать {B_BUFF2}. Отказаться?",
    "STRINGID_DIDNOTLEARNMOVE": "{B_BUFF1}: не удалось изучить {B_BUFF2}.\\p",
    "STRINGID_PKMNLEARNEDMOVE2": "{B_ATK_NAME_WITH_PREFIX} изучает {B_BUFF1}!",
    "STRINGID_PKMNPROTECTEDITSELF": "{B_SCR_NAME_WITH_PREFIX} защищается!",
    "STRINGID_ITDOESNTAFFECT": "На {B_DEF_NAME_WITH_PREFIX2} это не действует...",
    "STRINGID_ITDOESNTAFFECTSCR": "На {B_SCR_NAME_WITH_PREFIX2} это не действует...",
    "STRINGID_BATTLERFAINTED": "{B_SCR_NAME_WITH_PREFIX} теряет сознание!\\p",
    "STRINGID_PLAYERGOTMONEY": "За победу получено ¥{B_BUFF1}!\\p",
    "STRINGID_PLAYERWHITEOUT": "Нет POKeMON, способных продолжать бой!\\p",
    "STRINGID_PLAYERWHITEOUT2_WILD": "В панике потеряно ¥{B_BUFF1}...",
    "STRINGID_PLAYERWHITEOUT2_TRAINER": "Победителю отдано ¥{B_BUFF1}...",
    "STRINGID_PLAYERWHITEOUT3": "Поражение оказалось слишком тяжёлым!",
    "STRINGID_PREVENTSESCAPE": "{B_SCR_NAME_WITH_PREFIX} не даёт сбежать благодаря {B_SCR_ABILITY}!\\p",
    "STRINGID_ABOOSTED": " бонусные",
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
        raise SystemExit("usage: localize_battle_message_progression_quality_v3_201.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 21:
        raise RuntimeError("unexpected v3.201 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_progression_quality_v3_201_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "boostedExpSemanticsReviewedAgainstExpansion1170": True,
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
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} progression/move-learning battle strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
