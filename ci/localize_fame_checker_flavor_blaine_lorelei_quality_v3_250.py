#!/usr/bin/env python3
"""Qarro v3.250: human-quality Fame Checker flavor text for Blaine and Lorelei.

Polishes twelve main Fame Checker entries (six per person). EXPECTED bodies
are exact installed v3.8 handoff surfaces. FireRed colors, fonts and every
line/page control are preserved exactly; any source drift fails closed.

Pokemon species names stay English by project canon (for example LAPRAS).
Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_FLAVOR_BLAINE_LORELEI_QUALITY_V3_250"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorText_Blaine0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}КИННАБАР ИСЛАНДИЯ POKeMON ГИМ\nЛидер: Блейн\lХотхедед Мастер Квиза!$",
    "gFameCheckerFlavorText_Blaine1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мой огненный POKeMON Все они грубые\nГотовы к интенсивному теплу!\pОни сжигают всех претендентов!$",
    "gFameCheckerFlavorText_Blaine2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Наш лидер, Блэйн, заблудился.\nВ горах, но хорошо.\pНочью пала, когда огненная птица\nPOKeMON Появился.\pСвет позволил Блэйну найти\nОн благополучно спустился вниз.$",
    "gFameCheckerFlavorText_Blaine3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Блейн Синнабара Гима - это вполне\nстранный парень.\pОн жил на острове с тех пор, как\nДо того, как был построен ЛАБ.$",
    "gFameCheckerFlavorText_Blaine4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Это фотография Блэйна и\nМистер Фуджи.\pОни стоят плечом к плечу, чтобы\nплечо с большими ухмылками.$",
    "gFameCheckerFlavorText_Blaine5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, что Блэйн убирает свою темноту.\nИ только тогда, когда он думает\lНовые вопросы викторины.$",
    "gFameCheckerFlavorText_Lorelei0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я Лорелия из элитной четверки.$",
    "gFameCheckerFlavorText_Lorelei1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Никто не может быть лучше меня, когда это происходит.\nледяной POKeMON.$",
    "gFameCheckerFlavorText_Lorelei2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Где родился этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}У нас был великий и могущественный\nТренеры растут на этом острове.\pУверен, что даже ты ее знаешь.\nЭто Лорели из элитной четверки!$",
    "gFameCheckerFlavorText_Lorelei3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Известен своей логикой, расчетливостью,\nХороший стиль боя, Лорелия\lУ него есть удивительный секрет!$",
    "gFameCheckerFlavorText_Lorelei4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}А вы знали, что у ЛОРЭЛИ много\nИ много фаршированных кукол?\pКаждый раз, когда она возвращается\nЧетыре острова, коллекция растет!$",
    "gFameCheckerFlavorText_Lorelei5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}The LAPRAS Она есть, я представляю это\nОна была той, с которой познакомилась в детстве.\pЯ думаю, что это было в ледяной пещере.\nчто она поймала его.\pВозможно, что POKeMON С ним был\nС тех пор.$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorText_Blaine0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ГИМ ОСТРОВА СИННАБАР\nЛИДЕР: БЛЕЙН\lВСПЫЛЬЧИВЫЙ МАСТЕР ВИКТОРИН!$",
    "gFameCheckerFlavorText_Blaine1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мои ОГНЕННЫЕ ПОКЕМОНЫ суровы\nи полны жара!\pОни испепеляют всех соперников!$",
    "gFameCheckerFlavorText_Blaine2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Наш ЛИДЕР БЛЕЙН однажды заблудился\nв горах.\pНочью появился огненный\nПОКЕМОН-птица.\pЕго свет помог БЛЕЙНУ\nбезопасно спуститься.$",
    "gFameCheckerFlavorText_Blaine3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}БЛЕЙН из ГИМА СИННАБАРА -\nдовольно странный человек.\pОн жил на острове задолго\nдо постройки ЛАБОРАТОРИИ.$",
    "gFameCheckerFlavorText_Blaine4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}На фото БЛЕЙН и\nМИСТЕР ФУДЗИ.\pОни стоят плечом к плечу\nи широко улыбаются.$",
    "gFameCheckerFlavorText_Blaine5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, БЛЕЙН снимает тёмные очки,\nтолько когда придумывает\lновые вопросы для викторины.$",
    "gFameCheckerFlavorText_Lorelei0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я ЛОРЕЛЕЙ из ЭЛИТНОЙ ЧЕТВЁРКИ.$",
    "gFameCheckerFlavorText_Lorelei1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}В ЛЕДЯНЫХ ПОКЕМОНАХ\nмне нет равных.$",
    "gFameCheckerFlavorText_Lorelei2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Где родился этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}На этом острове вырос один из\nвеличайших ТРЕНЕРОВ.\pДаже ты наверняка её знаешь.\nЭто ЛОРЕЛЕЙ из ЭЛИТНОЙ ЧЕТВЁРКИ!$",
    "gFameCheckerFlavorText_Lorelei3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ЛОРЕЛЕЙ известна своим холодным,\nрасчётливым стилем боя,\lно у неё есть неожиданный секрет!$",
    "gFameCheckerFlavorText_Lorelei4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Знаешь, у ЛОРЕЛЕЙ очень\nмного мягких игрушек?\pПосле каждого возвращения на\nОСТРОВ ЧЕТЫРЕ коллекция растёт!$",
    "gFameCheckerFlavorText_Lorelei5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Думаю, её LAPRAS - тот самый,\nкоторого она встретила в детстве.\pКажется, она поймала его\nв ЛЕДЯНОЙ ПЕЩЕРЕ.\pВозможно, этот ПОКЕМОН с ней\nс тех самых пор.$",
}

BANNED_UNICODE = set("—–←→“”«»…")


def control_tokens(text: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", text)


def find_entry(text: str, label: str) -> re.Match[str]:
    pattern = re.compile(
        rf'(?m)^(?P<label>{re.escape(label)}::[^\n]*\n)'
        rf'(?P<prefix>\s*\.string ")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\s*)$'
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one Fame Checker entry, got {len(matches)}")
    return matches[0]


def replace_entry(text: str, label: str, expected: str, translated: str) -> str:
    match = find_entry(text, label)
    current = match.group("body")
    if current not in (expected, translated):
        raise RuntimeError(
            f"{label}: source drift: {current!r} not in exact expected/final surfaces"
        )
    if control_tokens(expected) != control_tokens(translated):
        raise RuntimeError(
            f"{label}: control-token drift old={control_tokens(expected)} "
            f"new={control_tokens(translated)}"
        )
    if not translated.endswith("$") or "$" in translated[:-1]:
        raise RuntimeError(f"{label}: invalid translated terminator")
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: unsupported translated character")
    if "\n" in translated or "\r" in translated:
        raise RuntimeError(f"{label}: physical newline in translation")
    if not re.search(r"[А-Яа-яЁё]", translated):
        raise RuntimeError(f"{label}: expected Cyrillic translation")
    if current == translated:
        return text

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
            "usage: localize_fame_checker_flavor_blaine_lorelei_quality_v3_250.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.250 Fame Checker flavor set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    for label in EXPECTED:
        text = replace_entry(text, label, EXPECTED[label], TRANSLATIONS[label])

    for label, translated in TRANSLATIONS.items():
        verified = find_entry(text, label).group("body")
        if verified != translated:
            raise RuntimeError(
                f"{label}: post-translation verification failed: "
                f"{verified!r} != {translated!r}"
            )

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_fame_checker_flavor_blaine_lorelei_quality_v3_250_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "sourceAnchorsExactFromHandoffV38": True,
        "controlTokensPreserved": True,
        "pokemonSpeciesNamesPreservedEnglish": True,
        "postTranslationSurfacesVerified": True,
        "humanEditedRussian": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Blaine/Lorelei Fame Checker flavor entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
