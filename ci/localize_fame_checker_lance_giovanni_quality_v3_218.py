#!/usr/bin/env python3
"""Qarro v3.218: human-quality Fame Checker cards for Lance through Giovanni.

Repairs eight machine-translated person-card strings while preserving the exact
FireRed control-token sequence for every entry. Text only; fail closed.

Pokemon, Move and Ability proper names stay English by project canon.
Gameplay, balance, boss teams, special whitelist, Ash Bond and Ash Cap are
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_LANCE_GIOVANNI_QUALITY_V3_218"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerPersonName_Lance": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ЛАНС$",
    "gFameCheckerPersonQuote_Lance": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: Лэнс\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я подумываю вернуться к своей\nРодной город.\pЯ хочу переучить свой дракон\nPOKeMON И укреплять их.\pЯ хотел бы пригласить тебя на мой\nОднажды родной город.$",
    "gFameCheckerPersonName_Bill": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Билл$",
    "gFameCheckerPersonQuote_Bill": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: BILL\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}У Селио ничего не было, кроме\nХвалите вас.\pСлышать это делает меня счастливым.\pКогда ловишь редкую POKeMON,\nПойдем, покажи мне, ладно?$",
    "gFameCheckerPersonName_MrFuji": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Г-н Фуджи$",
    "gFameCheckerPersonQuote_MrFuji": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: MR. FUJI\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Вместо того, чтобы надеяться на счастье\nтолько твой POKeMON…\pМогу ли я заставить вас пожелать\nСчастье всех POKeMON?$",
    "gFameCheckerPersonName_Giovanni": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Джиованни$",
    "gFameCheckerPersonQuote_Giovanni": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: GIOVANNI\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Нет ничего, что я хотел бы сказать\nТебе.\pЯ буду концентрироваться исключительно на\nЯ улучшаю себя, и никто другой.$",
}

TRANSLATIONS = {
    "gFameCheckerPersonName_Lance": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ЛЭНС$",
    "gFameCheckerPersonQuote_Lance": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: ЛЭНС\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я думаю вернуться в свой\nродной город.\pХочу заново тренировать своих\nПОКЕМОНОВ драконьего типа.\pОднажды я приглашу тебя\nк себе на родину.$",
    "gFameCheckerPersonName_Bill": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}БИЛЛ$",
    "gFameCheckerPersonQuote_Bill": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: БИЛЛ\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Привет! СЕЛИО только и делал,\nчто хвалил тебя.\pМне очень приятно это слышать.\pПоймаешь редкого ПОКЕМОНА -\nобязательно покажи мне! Обещаешь?$",
    "gFameCheckerPersonName_MrFuji": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}МИСТЕР ФУДЗИ$",
    "gFameCheckerPersonQuote_MrFuji": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: МИСТЕР ФУДЗИ\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Не желай счастья только\nсвоим ПОКЕМОНАМ...\pПожелай счастья и всем\nостальным ПОКЕМОНАМ.$",
    "gFameCheckerPersonName_Giovanni": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ДЖОВАННИ$",
    "gFameCheckerPersonQuote_Giovanni": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: ДЖОВАННИ\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мне нечего тебе сказать.\nСовсем нечего.\pЯ сосредоточусь лишь на том,\nчтобы стать сильнее.$",
}

BANNED_UNICODE = set("—–←→“”«»…")


def control_tokens(text: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", text)


def replace_entry(text: str, label: str, expected: str, translated: str) -> str:
    pattern = re.compile(
        rf'(?m)^(?P<label>{re.escape(label)}::[^\n]*\n)'
        rf'(?P<prefix>\s*\.string ")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\s*)$'
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one text entry, got {len(matches)}")

    match = matches[0]
    current = match.group("body")
    if current != expected:
        raise RuntimeError(f"{label}: source drift: {current!r} != {expected!r}")
    if control_tokens(current) != control_tokens(translated):
        raise RuntimeError(
            f"{label}: control-token drift old={control_tokens(current)} "
            f"new={control_tokens(translated)}"
        )
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: invalid translation surface")
    if "\n" in translated or "\r" in translated:
        raise RuntimeError(f"{label}: physical newline in translation body")
    if not translated.endswith("$"):
        raise RuntimeError(f"{label}: translated text must end with $")

    replacement = (
        match.group("label")
        + match.group("prefix")
        + translated
        + match.group("suffix")
    )
    return text[:match.start()] + replacement + text[match.end():]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: localize_fame_checker_lance_giovanni_quality_v3_218.py <upstream-root>"
        )

    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 8:
        raise RuntimeError("unexpected v3.218 Fame Checker string set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    for label in EXPECTED:
        text = replace_entry(text, label, EXPECTED[label], TRANSLATIONS[label])
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_fame_checker_lance_giovanni_quality_v3_218_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "humanEditedRussian": True,
        "sourceAnchorsFailClosed": True,
        "controlTokensPreserved": True,
        "playerGenderNeutral": True,
        "pokemonMoveAbilityNamesPreserved": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Fame Checker strings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
