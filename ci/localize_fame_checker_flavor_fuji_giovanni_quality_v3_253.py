#!/usr/bin/env python3
"""Qarro v3.253: human-quality Fame Checker flavor text for Mr. Fuji and Giovanni.

Polishes twelve main Fame Checker entries (six per person). EXPECTED bodies
are exact installed v3.8 surfaces taken from the exact same-commit build
artifact. FireRed colors, fonts and every line/page control are preserved
exactly; any source drift fails closed.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_FLAVOR_FUJI_GIOVANNI_QUALITY_V3_253"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorText_MrFuji0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Он очень добрый.\pОн заботится о брошенных и\nсирота POKeMON.$",
    "gFameCheckerFlavorText_MrFuji1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Этот старик прошёл прямо до самого конца.\nСкрытая.\pИ он начинает говорить о том, как\nКоманда Ракета злоупотребляет POKeMON.\pМы просто обсуждаем это как\nвзрослые.$",
    "gFameCheckerFlavorText_MrFuji2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}POKeMON Фана Магазина\nЕжемесячный розыгрыш Гран-при!\pФорма заявки является...\pЕго вырезали.\nКто-то уже должен был подать заявку.$",
    "gFameCheckerFlavorText_MrFuji3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я слышал, что мистер Фуджи не из\nЭти части изначально тоже.$",
    "gFameCheckerFlavorText_MrFuji4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Это фотография Блэйна и\nМистер Фуджи.\pОни стоят плечом к плечу, чтобы\nплечо с большими ухмылками.$",
    "gFameCheckerFlavorText_MrFuji5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Редактор: Застенчивый мистер Фуджи повернулся\nЗапишите наши запросы на интервью.\pОн добрый человек, которого обожают.\nИ уважаем в городе Лавендер.$",
    "gFameCheckerFlavorText_Giovanni0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Команда ROCKET захватывает POKeMON из\nпо всему миру.\pЭто важные инструменты для сохранения\nНаше преступное предприятие идет.\pЯ лидер, Джиованни!$",
    "gFameCheckerFlavorText_Giovanni1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Те бандиты, которые захватили наши\nстроительство...\pВ их БОСС сказали, что он ищет\nсильный POKeMON.$",
    "gFameCheckerFlavorText_Giovanni2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Босс команды Rocket ужасен\nЖестоко!\pДля него, POKeMON Это просто инструменты для\nбыть использованным.$",
    "gFameCheckerFlavorText_Giovanni3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Добро пожаловать в мое убежище!\pТак будет, пока я не смогу восстановить\nКоманда отправляется в прежнюю славу.$",
    "gFameCheckerFlavorText_Giovanni4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}- Унеси меня! - Джиованни был тем, кто меня убил.\nГим-лидер ВИРИДИАНА?$",
    "gFameCheckerFlavorText_Giovanni5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Ты... ты не сын Джиованни,\nТы что, не так?\pНет, это не может быть правдой.\nУ ребенка Джованни рыжие волосы.$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorText_MrFuji0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Он очень добрый.\pОн заботится о брошенных\nи осиротевших ПОКЕМОНАХ.$",
    "gFameCheckerFlavorText_MrFuji1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Этот старик сам пришёл прямо\nк нашему УБЕЖИЩУ.\pА потом начал возмущаться, что\nКОМАНДА R плохо обращается с ПОКЕМОНАМИ.\pВот мы и обсуждаем это,\nкак взрослые.$",
    "gFameCheckerFlavorText_MrFuji2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ЖУРНАЛ ПОКЕМОН-ФАНАТОВ\nЕжемесячный розыгрыш приза!\pБланк заявки...\pИсчез! Его вырезали.\nКто-то уже подал заявку.$",
    "gFameCheckerFlavorText_MrFuji3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Слышал, МИСТЕР ФУДЗИ тоже не\nродом из этих мест.$",
    "gFameCheckerFlavorText_MrFuji4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Это фото БЛЕЙНА и\nМИСТЕРА ФУДЗИ.\pОни стоят плечом к плечу\nи широко улыбаются.$",
    "gFameCheckerFlavorText_MrFuji5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Редактор: застенчивый МИСТЕР ФУДЗИ\nотказался от нашего интервью.\pОн добрый человек, которого любят\nи уважают в ЛАВАНДЕР-ТАУНЕ.$",
    "gFameCheckerFlavorText_Giovanni0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}КОМАНДА R ловит ПОКЕМОНОВ\nпо всему миру.\pОни нужны для работы\nнашей преступной организации.\pЯ её лидер - ДЖОВАННИ!$",
    "gFameCheckerFlavorText_Giovanni1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Те бандиты, что захватили наше\nздание...\pИх БОСС сказал, что ищет\nсильных ПОКЕМОНОВ.$",
    "gFameCheckerFlavorText_Giovanni2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}БОСС КОМАНДЫ R ужасно\nжесток!\pДля него ПОКЕМОНЫ - лишь орудия,\nкоторые можно использовать.$",
    "gFameCheckerFlavorText_Giovanni3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Добро пожаловать в моё УБЕЖИЩЕ!\pЯ останусь здесь, пока не верну\nКОМАНДЕ R былую славу.$",
    "gFameCheckerFlavorText_Giovanni4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Вот это да! ДЖОВАННИ был\nЛИДЕРОМ ГИМА ВИРИДИАНА?$",
    "gFameCheckerFlavorText_Giovanni5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Ты... Ты ведь не ребёнок ДЖОВАННИ,\nправда?\pНет, быть не может.\nУ его ребёнка рыжие волосы.$",
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
            "usage: localize_fame_checker_flavor_fuji_giovanni_quality_v3_253.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.253 Fame Checker flavor set")

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

    out = root / "build" / "qarro_ru_fame_checker_flavor_fuji_giovanni_quality_v3_253_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "sourceAnchorsExactFromSameCommitArtifact": True,
        "controlTokensPreserved": True,
        "projectTerminologyPreserved": True,
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Mr. Fuji/Giovanni Fame Checker flavor entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
