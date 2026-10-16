#!/usr/bin/env python3
"""Qarro v3.247: human-quality Fame Checker flavor text for Brock and Misty.

Polishes twelve main Fame Checker entries (six per person). EXPECTED bodies
are exact installed v3.8 handoff surfaces. FireRed colors, fonts and all
line/page controls are preserved exactly; any source drift fails closed.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_FLAVOR_BROCK_MISTY_QUALITY_V3_247"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorText_Brock0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Город Питер POKeMON ГИМ\nЛидер: Брок\lСкалистый POKeMON Тренер!$",
    "gFameCheckerFlavorText_Brock1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Моя твердая воля очевидна\nДаже в моей POKeMON.\pМой POKeMON Все они являются твердыми и\nИмейте истинное мужество.\pПравильно - мой POKeMON Все они\nТип РОК!$",
    "gFameCheckerFlavorText_Brock2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Не так много серьезных POKeMON\nТренеры здесь.\pОни все как буги-катеры,\nНу, знаете, просто любители.\pНо Питер Гим не такой, как он.\nЭто, не один раз.$",
    "gFameCheckerFlavorText_Brock3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Брок классный, он не просто жесткий.\nЛюди любят и уважают его.\pЯ хочу стать лидером GYM\nКак он.$",
    "gFameCheckerFlavorText_Brock4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Привет, я здесь раскапываю окаменелости.\nПод МТ.Луной.\pИногда, в рот Питера Гима\nДай мне руку.$",
    "gFameCheckerFlavorText_Brock5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Брок редко смеется, но, как говорят,\nНевозможно остановиться, если он начнет.$",
    "gFameCheckerFlavorText_Misty0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}КРУЛЕВСКИЙ ГОРОД POKeMON ГИМ\nРуководитель: MISTУра.\lТомбойская Русалка!$",
    "gFameCheckerFlavorText_Misty1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Моя политика - это тотальное наступление.\nс типом воды POKeMON!$",
    "gFameCheckerFlavorText_Misty2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}MISTЯ - тренер, который собирается\nПродолжайте совершенствоваться.\pОна не проиграет кому-то вроде тебя!$",
    "gFameCheckerFlavorText_Misty3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Сильные тренеры и вода POKeMON\nЭто обычные достопримечательности в этих местах.\pГоворят, что MISTО, да.\nЗдесь ездят поезда 'Керулиан Гим'.$",
    "gFameCheckerFlavorText_Misty4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Этот мыс - знаменитое место для свиданий.\pMISTY, GYM LEADER, имеет высокий уровень\nнадежд на это место.$",
    "gFameCheckerFlavorText_Misty5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}MISTГоворят, что ты поклоняешься Лорели.\nИз элитной четверки.$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorText_Brock0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ГИМ ПЬЮТЕРА\nЛИДЕР: БРОК\lНЕПОКОЛЕБИМЫЙ ТРЕНЕР!$",
    "gFameCheckerFlavorText_Brock1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Моя каменная воля видна\nдаже в моих ПОКЕМОНАХ.\pВсе мои ПОКЕМОНЫ крепки\nи полны решимости.\pВерно - все мои ПОКЕМОНЫ\nКАМЕННОГО типа!$",
    "gFameCheckerFlavorText_Brock2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Здесь мало серьёзных ТРЕНЕРОВ\nПОКЕМОНОВ.\pБольшинство - вроде ЛОВЦОВ ЖУКОВ,\nпросто любители.\pНо БРОК из ГИМА ПЬЮТЕРА\nсовсем не такой.$",
    "gFameCheckerFlavorText_Brock3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}БРОК крут не только силой.\nЕго любят и уважают.\pЯ хочу стать ЛИДЕРОМ ГИМА,\nкак он.$",
    "gFameCheckerFlavorText_Brock4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я ищу ископаемые здесь,\nпод ЛУННОЙ ГОРОЙ.\pИногда БРОК из ГИМА ПЬЮТЕРА\nпомогает мне.$",
    "gFameCheckerFlavorText_Brock5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}БРОК редко смеётся, но говорят,\nесли начнёт - уже не остановить.$",
    "gFameCheckerFlavorText_Misty0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ГИМ СЕРУЛИНА\nЛИДЕР: МИСТИ\lОЗОРНАЯ РУСАЛКА!$",
    "gFameCheckerFlavorText_Misty1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Моя тактика - полное наступление\nВОДНЫМИ ПОКЕМОНАМИ!$",
    "gFameCheckerFlavorText_Misty2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}МИСТИ - ТРЕНЕР, который будет\nстановиться всё сильнее.\pТебе её так просто не победить!$",
    "gFameCheckerFlavorText_Misty3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Сильные ТРЕНЕРЫ и ВОДНЫЕ\nПОКЕМОНЫ здесь обычны.\pГоворят, МИСТИ из ГИМА\nСЕРУЛИНА тренируется здесь.$",
    "gFameCheckerFlavorText_Misty4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Этот мыс славится свиданиями.\pМИСТИ, ЛИДЕР ГИМА, очень\nлюбит это место.$",
    "gFameCheckerFlavorText_Misty5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, МИСТИ восхищается ЛОРЕЛЕЙ\nиз ЭЛИТНОЙ ЧЕТВЁРКИ.$",
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
            "usage: localize_fame_checker_flavor_brock_misty_quality_v3_247.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.247 Fame Checker flavor set")

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

    out = root / "build" / "qarro_ru_fame_checker_flavor_brock_misty_quality_v3_247_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "sourceAnchorsExactFromHandoffV38": True,
        "controlTokensPreserved": True,
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Brock/Misty Fame Checker flavor entries"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_flavor_surge_erika_quality_v3_248.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
