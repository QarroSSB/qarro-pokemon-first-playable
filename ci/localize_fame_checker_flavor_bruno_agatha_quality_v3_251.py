#!/usr/bin/env python3
"""Qarro v3.251: human-quality Fame Checker flavor text for Bruno and Agatha.

Polishes twelve main Fame Checker entries (six per person). EXPECTED bodies
are exact installed v3.8 handoff surfaces. FireRed colors, fonts and every
line/page control are preserved exactly; any source drift fails closed.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_FLAVOR_BRUNO_AGATHA_QUALITY_V3_251"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorText_Bruno0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я - Бруно из элитной четверки!$",
    "gFameCheckerFlavorText_Bruno1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я жил и тренировался со своей\nборьба POKeMON!$",
    "gFameCheckerFlavorText_Bruno2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Бруно, по-видимому, присоединился к элите.\nЧетыре из его жгучих амбиций\lСражайтесь с лучшими тренерами.$",
    "gFameCheckerFlavorText_Bruno3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Бруно, который старше меня,\nПосещает СПА время от времени.\pОн приходит на реабилитацию, оба\nего собственных и его POKeMONs.$",
    "gFameCheckerFlavorText_Bruno4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Он один из элитных четверых.\nЕго зовут Бруно.\pОн ушел разочарованным, когда\nОказалось, что все они были проданы.\lиз Rage Конфеты.$",
    "gFameCheckerFlavorText_Bruno5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Даже Бруно...\nОн тренировался с товарищем по\lНазвание: БРАВЛЫЙ раньше.$",
    "gFameCheckerFlavorText_Agatha0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я Агата из элитной четверки.$",
    "gFameCheckerFlavorText_Agatha1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Тип призрака Агаты POKeMON есть\nУжасно страшно в жесткости.$",
    "gFameCheckerFlavorText_Agatha2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}У этой старушки тоже есть\nКороткий предохранитель тоже.\pНе нужно ничего, чтобы получить\nЭта страшная леди кричала.$",
    "gFameCheckerFlavorText_Agatha3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}В юности Агата и Проф.\nОАК были соперниками, которые боролись за\lПревосходство как тренеры.$",
    "gFameCheckerFlavorText_Agatha4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я слышал, ОАК много чего взяла.\nИнтерес к тебе, дитя.\pЭтот старый дафф когда-то был жестким и\nКрасивый.\pНо это было десятилетия назад.\nОн тень своего прежнего 'я'.$",
    "gFameCheckerFlavorText_Agatha5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Возьмем, к примеру, Агату.\pОна установила рекорд, став\nСтарейший в истории Элитный Четверо членов.$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorText_Bruno0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я БРУНО из ЭЛИТНОЙ ЧЕТВЁРКИ!$",
    "gFameCheckerFlavorText_Bruno1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я жил и тренировался вместе\nсо своими БОЕВЫМИ ПОКЕМОНАМИ!$",
    "gFameCheckerFlavorText_Bruno2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, БРУНО вступил в ЭЛИТНУЮ\nЧЕТВЁРКУ из жгучего желания\lсражаться с лучшими ТРЕНЕРАМИ.$",
    "gFameCheckerFlavorText_Bruno3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}БРУНО, старший товарищ,\nиногда приходит в СПА.\pОн лечит здесь травмы - свои\nи своих ПОКЕМОНОВ.$",
    "gFameCheckerFlavorText_Bruno4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Он из ЭЛИТНОЙ ЧЕТВЁРКИ.\nЕго зовут БРУНО.\pОн ушёл разочарованным, когда\nузнал, что все КОНФЕТЫ ЯРОСТИ\lраспроданы.$",
    "gFameCheckerFlavorText_Bruno5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Даже БРУНО...\nКогда-то он тренировался с бойцом\lпо имени БРОУЛИ.$",
    "gFameCheckerFlavorText_Agatha0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я АГАТА из ЭЛИТНОЙ ЧЕТВЁРКИ.$",
    "gFameCheckerFlavorText_Agatha1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ПРИЗРАЧНЫЕ ПОКЕМОНЫ АГАТЫ\nужасающе сильны.$",
    "gFameCheckerFlavorText_Agatha2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}У этой старушки ещё и\nочень вспыльчивый характер.\pПочти ничего не нужно, чтобы\nона начала кричать.$",
    "gFameCheckerFlavorText_Agatha3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}В молодости АГАТА и ПРОФ.\nОУК были соперниками и спорили,\lкто из них лучший ТРЕНЕР.$",
    "gFameCheckerFlavorText_Agatha4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Слышала, ОУК очень\nзаинтересовался тобой, дитя.\pКогда-то этот старикашка был\nсильным и красавцем.\pНо это было много лет назад.\nТеперь он лишь тень прошлого.$",
    "gFameCheckerFlavorText_Agatha5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Возьми хотя бы АГАТУ.\pОна поставила рекорд, став\nстарейшим членом ЭЛИТНОЙ ЧЕТВЁРКИ.$",
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
            "usage: localize_fame_checker_flavor_bruno_agatha_quality_v3_251.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.251 Fame Checker flavor set")

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

    out = root / "build" / "qarro_ru_fame_checker_flavor_bruno_agatha_quality_v3_251_audit.json"
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Bruno/Agatha Fame Checker flavor entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
