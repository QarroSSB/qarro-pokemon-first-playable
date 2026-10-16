#!/usr/bin/env python3
"""Qarro v3.246: human-quality Fame Checker flavor text for Prof. Oak and Daisy.

Polishes twelve main Fame Checker entries (six per person). EXPECTED bodies
are exact installed v3.8 handoff surfaces. FireRed colors, fonts, line/page
controls and the {RIVAL} placeholder are preserved exactly; any source drift
fails closed.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_FLAVOR_OAK_DAISY_QUALITY_V3_246"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorText_ProfOak0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}О'Кей POKeMON Исследовательский центр$",
    "gFameCheckerFlavorText_ProfOak1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Составить полное руководство по всем\nтот POKeMON В мире...\pЭто была моя мечта!$",
    "gFameCheckerFlavorText_ProfOak2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}О.К. может не очень сильно выглядеть,\nНо он - авторитет в POKeMON.\pМногие POKeMON Тренеры задерживают его в\n- Большое уважение.$",
    "gFameCheckerFlavorText_ProfOak3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}По сообщениям, ОАК живет со своим\nВнуки, дети и {RIVAL}.$",
    "gFameCheckerFlavorText_ProfOak4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я слышал, ОАК много чего взяла.\nИнтерес к тебе, дитя.\pЭтот старый дафф когда-то был жестким и\nКрасивый.\pНо это было десятилетия назад.\nОн тень своего прежнего 'я'.$",
    "gFameCheckerFlavorText_ProfOak5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ОАК собирается иметь свою собственную\nСкоро радиошоу.\pПрограмма будет называться PROF.\nОАК POKeMON Семинар.$",
    "gFameCheckerFlavorText_Daisy0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Если вы покажете свой день POKeMON,\nОна может сказать, как сильно ты ей нравишься.\pИногда она даже будет ухаживать\nа POKeMON Для тебя.$",
    "gFameCheckerFlavorText_Daisy1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Человек, который больше всего нравится\nPOKeMON Это день, я думаю.$",
    "gFameCheckerFlavorText_Daisy2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Она нежно ухаживала за собой POKeMON…\nОна была маленьким ангелом.\pИмя этой маленькой девочки...\nЯ думаю, это был день рождения.$",
    "gFameCheckerFlavorText_Daisy3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}По сообщениям, ОАК живет со своим\nВнуки, дети и {RIVAL}.$",
    "gFameCheckerFlavorText_Daisy4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Девушка из Паллетта-Тауна, Дэйзи,\nОна наслаждается чай каждый день.\pОна навещает Челадонскую ДЕПТ.\nКупить чай.$",
    "gFameCheckerFlavorText_Daisy5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Весна POKeMON Конте\nЧемпион мира Дейзи Ок\lПаллетный бутон!$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorText_ProfOak0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ЛАБОРАТОРИЯ ПОКЕМОНОВ ОУКА$",
    "gFameCheckerFlavorText_ProfOak1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Полный справочник обо всех\nПОКЕМОНАХ мира...\pЭто была моя мечта!$",
    "gFameCheckerFlavorText_ProfOak2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ПРОФ. ОУК выглядит просто,\nно он знаток ПОКЕМОНОВ.\pМногие ТРЕНЕРЫ ПОКЕМОНОВ\nглубоко его уважают.$",
    "gFameCheckerFlavorText_ProfOak3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ПРОФ. ОУК живёт вместе с\nвнуками ДЭЙЗИ и {RIVAL}.$",
    "gFameCheckerFlavorText_ProfOak4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ОУК очень заинтересовался\nтобой, как я слышала.\pКогда-то этот старикашка был\nсильным и красавцем.\pНо это было много лет назад.\nТеперь он лишь тень прошлого.$",
    "gFameCheckerFlavorText_ProfOak5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Скоро у ПРОФ. ОУКА будет\nсвоя радиопередача.\pОна будет называться\nСЕМИНАР ПОКЕМОНОВ ПРОФ. ОУКА.$",
    "gFameCheckerFlavorText_Daisy0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Покажи ДЭЙЗИ своего ПОКЕМОНА,\nи она оценит вашу дружбу.\pИногда она даже ухаживает\nза твоим ПОКЕМОНОМ.$",
    "gFameCheckerFlavorText_Daisy1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Думаю, больше всех ПОКЕМОНЫ\nлюбят именно ДЭЙЗИ.$",
    "gFameCheckerFlavorText_Daisy2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Она так заботилась о ПОКЕМОНЕ...\nНастоящий ангел.\pКак же звали ту девочку...\nКажется, ДЭЙЗИ.$",
    "gFameCheckerFlavorText_Daisy3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ПРОФ. ОУК живёт вместе с\nвнуками ДЭЙЗИ и {RIVAL}.$",
    "gFameCheckerFlavorText_Daisy4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ДЭЙЗИ из ПАЛЛЕТ-ТАУНА\nкаждый день пьёт ЧАЙ.\pЗа ЧАЕМ она ходит в\nУНИВЕРМАГ СЕЛАДОНА.$",
    "gFameCheckerFlavorText_Daisy5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Весенний КОНКУРС ПОКЕМОНОВ\nвыиграла ДЭЙЗИ ОУК\lиз ПАЛЛЕТ-ТАУНА!$",
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
            "usage: localize_fame_checker_flavor_oak_daisy_quality_v3_246.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.246 Fame Checker flavor set")

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

    out = root / "build" / "qarro_ru_fame_checker_flavor_oak_daisy_quality_v3_246_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "sourceAnchorsExactFromHandoffV38": True,
        "controlTokensPreserved": True,
        "placeholdersPreserved": True,
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Oak/Daisy Fame Checker flavor entries"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_flavor_brock_misty_quality_v3_247.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
