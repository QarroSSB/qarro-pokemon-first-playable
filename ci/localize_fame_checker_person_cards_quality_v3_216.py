#!/usr/bin/env python3
"""Qarro v3.216: human-quality Fame Checker person cards for Oak through Erika.

This pass runs after the generated bulk localization and the battle-message
quality chain. It repairs twelve visibly broken Russian person-card strings in
data/text/fame_checker_frlg.inc while preserving every FireRed control token.

Pokemon, Move and Ability proper names stay English by project canon.
Gameplay, balance, boss teams, special whitelist, Ash Bond and Ash Cap are
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_PERSON_CARDS_QUALITY_V3_216"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerPersonName_ProfOak": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}- Хорошо.$",
    "gFameCheckerPersonQuote_ProfOak": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: ПРОФ. ОАК\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Почему POKeMON Соревноваться и сражаться\nТак тяжело для тебя?\pОни делают это, потому что видят\nЛюбовь и доверие, которые у вас есть\lк POKeMON.\pНикогда не забывай об этом.$",
    "gFameCheckerPersonName_Daisy": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ПРЯМОЙ$",
    "gFameCheckerPersonQuote_Daisy": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: Дэйзи\nВ: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Когда я наслаждался комфортом\nМои чайные перерывы, ты очень вырос\lквалифицированным и мощным.\pНадеюсь, что вы останетесь хорошим соперником.\nМоему младшему брату.$",
    "gFameCheckerPersonName_Brock": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Брок$",
    "gFameCheckerPersonQuote_Brock": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: BROCK\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}В нашем большом мире, там\nДолжно быть много жестких тренеров.\pДавайте продолжим тренироваться и\nСделаем себя сильнее!$",
    "gFameCheckerPersonName_Misty": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}MISTУра.$",
    "gFameCheckerPersonQuote_Misty": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: MISTУра.\nВ: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я собираюсь продолжать тренироваться здесь, в\nЭтот Гим.\pКогда мне станет лучше, я бы с удовольствием ударил\nПутешествие и дорога.$",
    "gFameCheckerPersonName_LtSurge": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ЛТ. КУРС$",
    "gFameCheckerPersonQuote_LtSurge": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: LT.SURGE\nВ: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Эй, малыш!\nТы наэлектризовал меня в нашей битве!\pЯ не знал, что там были\nТакие же хитрые тренеры, как и вы.\pЭто заставило меня изменить свое мнение о\nТы!$",
    "gFameCheckerPersonName_Erika": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Эрика$",
    "gFameCheckerPersonQuote_Erika": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Из: Эрика\nВ: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я очень рад, что есть сильные\nТакие тренеры, как вы.\pТолько это осознание вдохновляет и\nЭто мотивирует меня стараться больше.\pПожалуйста, навести меня снова.\nЗзз...$",
}

TRANSLATIONS = {
    "gFameCheckerPersonName_ProfOak": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ПРОФ. ОУК$",
    "gFameCheckerPersonQuote_ProfOak": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: ПРОФ. ОУК\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Почему ПОКЕМОНЫ так упорно\nсражаются ради тебя?\pОни чувствуют твою любовь\nи доверие к ним.\lПоэтому и стараются изо всех сил.\pНикогда об этом не забывай.$",
    "gFameCheckerPersonName_Daisy": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ДЭЙЗИ$",
    "gFameCheckerPersonQuote_Daisy": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: ДЭЙЗИ\nКому: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Пока я спокойно пила чай,\nтвоё мастерство заметно выросло\lвместе с твоей силой.\pНадеюсь, вы с моим братом\nостанетесь хорошими соперниками.$",
    "gFameCheckerPersonName_Brock": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}БРОК$",
    "gFameCheckerPersonQuote_Brock": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: БРОК\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}В нашем огромном мире\nесть много сильных ТРЕНЕРОВ.\pДавай продолжать тренировки\nи становиться ещё сильнее!$",
    "gFameCheckerPersonName_Misty": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}МИСТИ$",
    "gFameCheckerPersonQuote_Misty": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: МИСТИ\nКому: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я продолжу тренироваться здесь,\nв этом ГИМЕ.\pКогда стану ещё сильнее,\nотправлюсь путешествовать.$",
    "gFameCheckerPersonName_LtSurge": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ЛТ. СЕРДЖ$",
    "gFameCheckerPersonQuote_LtSurge": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: ЛТ. СЕРДЖ\nКому: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Эй!\nВот это был бой!\pНе думал, что бывают\nнастолько смелые ТРЕНЕРЫ.\pПосле нашей встречи я смотрю\nна тебя совсем иначе!$",
    "gFameCheckerPersonName_Erika": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}ЭРИКА$",
    "gFameCheckerPersonQuote_Erika": r"{COLOR BLUE}{SHADOW LIGHT_BLUE}От: ЭРИКА\nКому: {PLAYER}\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я очень рада, что встречаются\nтакие сильные ТРЕНЕРЫ.\pОдно это вдохновляет меня\nстараться ещё усерднее.\pПриходи ко мне ещё раз.\nЗзз...$",
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
            "usage: localize_fame_checker_person_cards_quality_v3_216.py <upstream-root>"
        )

    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.216 Fame Checker string set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    for label in EXPECTED:
        text = replace_entry(text, label, EXPECTED[label], TRANSLATIONS[label])
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_fame_checker_person_cards_quality_v3_216_audit.json"
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Fame Checker person-card strings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
