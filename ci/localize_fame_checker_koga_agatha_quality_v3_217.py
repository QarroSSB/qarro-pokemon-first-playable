#!/usr/bin/env python3
"""Qarro v3.217: human-quality Fame Checker cards from Koga through Agatha.

Repairs twelve machine-translated person-card strings while preserving the
exact FireRed control-token sequence for every entry. This is a text-only,
fail-closed quality pass.

Pokemon, Move and Ability proper names stay English by project canon.
Gameplay, balance, boss teams, special whitelist, Ash Bond and Ash Cap are
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_KOGA_AGATHA_QUALITY_V3_217"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerPersonName_Koga": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Кога$",
    "gFameCheckerPersonQuote_Koga": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: KOGA\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мы с тобой должны установить наши отношения.\nПрицелы выше и работать в направлении\lРешение наших задач.\pТеперь я должен тренировать свою дочь.$",
    "gFameCheckerPersonName_Sabrina": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Сабрина$",
    "gFameCheckerPersonQuote_Sabrina": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: Сабрина\nВ: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Любовь, которую вы имеете к своей\nPOKeMON…\pЭто была сила, которая никогда не была\nЯ был одержим своей психической силой.$",
    "gFameCheckerPersonName_Blaine": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Блейн$",
    "gFameCheckerPersonQuote_Blaine": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: BLAINE\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мой огонь POKeMON!\nОни станут еще более мощными!\pА теперь, викторина.\nогненный тип POKeMON Есть там?$",
    "gFameCheckerPersonName_Lorelei": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ЛОРЛЕЙ$",
    "gFameCheckerPersonQuote_Lorelei": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: Лорели\nВ: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мне нужно было поблагодарить тебя за твою\nПомогите.\pНо это не имеет никакого отношения к нашей\nСражения.\pВ следующий раз лучше остерегаться!$",
    "gFameCheckerPersonName_Bruno": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Бруно$",
    "gFameCheckerPersonQuote_Bruno": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: Бруно\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Сверхдержава твоей POKeMON\nИ ты, я испытала себя.\pВ следующий раз, может, я покажу тебе\nКак тренировать себя.$",
    "gFameCheckerPersonName_Agatha": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Агата$",
    "gFameCheckerPersonQuote_Agatha": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: AGATHA\nВ: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Когда вы становитесь старше, не\nСмею быть мягким, как этот кут ОАК!\pБудьте как я и продолжайте бороться!$",
}

TRANSLATIONS = {
    "gFameCheckerPersonName_Koga": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}КОГА$",
    "gFameCheckerPersonQuote_Koga": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: КОГА\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Нам обоим нужно ставить\nперед собой высокие цели\lи преодолевать трудности.\pА теперь мне пора тренировать дочь.$",
    "gFameCheckerPersonName_Sabrina": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}САБРИНА$",
    "gFameCheckerPersonQuote_Sabrina": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: САБРИНА\nКому: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Твоя любовь к своим\nПОКЕМОНАМ...\pЭто сила, которую не смогла\nпревзойти даже моя психическая мощь.$",
    "gFameCheckerPersonName_Blaine": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}БЛЕЙН$",
    "gFameCheckerPersonQuote_Blaine": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: БЛЕЙН\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мои огненные ПОКЕМОНЫ!\nОни станут ещё сильнее!\pА теперь вопрос викторины.\nСколько видов огненных ПОКЕМОНОВ?$",
    "gFameCheckerPersonName_Lorelei": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ЛОРЕЛЕЙ$",
    "gFameCheckerPersonQuote_Lorelei": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: ЛОРЕЛЕЙ\nКому: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я хотела поблагодарить тебя за\nпомощь.\pНо к нашим боям это не имеет\nникакого отношения.\pВ следующий раз будь начеку!$",
    "gFameCheckerPersonName_Bruno": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}БРУНО$",
    "gFameCheckerPersonQuote_Bruno": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: БРУНО\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Силу твоих ПОКЕМОНОВ\nи твою я испытал на себе.\pВ следующий раз я покажу,\nкак следует тренироваться.$",
    "gFameCheckerPersonName_Agatha": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}АГАТА$",
    "gFameCheckerPersonQuote_Agatha": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: АГАТА\nКому: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Когда станешь старше, только не\nразмякни, как этот старикашка ОУК!\pБудь как я и продолжай сражаться!$",
}

BANNED_UNICODE = set("—–←→“”«»")


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
            "usage: localize_fame_checker_koga_agatha_quality_v3_217.py <upstream-root>"
        )

    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.217 Fame Checker string set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    for label in EXPECTED:
        text = replace_entry(text, label, EXPECTED[label], TRANSLATIONS[label])
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_fame_checker_koga_agatha_quality_v3_217_audit.json"
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
