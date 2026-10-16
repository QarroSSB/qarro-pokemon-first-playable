#!/usr/bin/env python3
"""Qarro v3.248: human-quality Fame Checker flavor text for Lt. Surge and Erika.

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

MARKER = "QARRO_RU_FAME_CHECKER_FLAVOR_SURGE_ERIKA_QUALITY_V3_248"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorText_LtSurge0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Город Вермилион POKeMON ГИМ\nЛидер: ЛТ. СЕРЖ.\lАмериканская молния!$",
    "gFameCheckerFlavorText_LtSurge1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я говорю тебе, парень, электрический POKeMON\nСпаси меня во время войны!$",
    "gFameCheckerFlavorText_LtSurge2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Когда я был в армии, Л. С.\nЭто был мой строгий командир.\pОн был трудным мастером.$",
    "gFameCheckerFlavorText_LtSurge3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Л.С.Сурж всегда славился\nЕго бережное отношение к армии.$",
    "gFameCheckerFlavorText_LtSurge4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Л.С.: Строители установили ловушки в\nСам Гим.\pОн везде установил двойные замки.$",
    "gFameCheckerFlavorText_LtSurge5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}По слухам, именно LT.SURGE\nПилот, находясь дома в США.\pОн использовал электричество, которое вырабатывалось\nчерез POKeMON Чтобы управлять своим самолетом.$",
    "gFameCheckerFlavorText_Erika0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Город Челадон POKeMON ГИМ\nЛидер: Эрика\lThe NatuВозлюбимая принцесса!$",
    "gFameCheckerFlavorText_Erika1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я студентка в области искусства\nЦветы раскрашивают.\pМой POKeMON являются исключительно\nТипа 'Грасс'.$",
    "gFameCheckerFlavorText_Erika2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Наш лидер Эрика может быть тихим,\nНо она знаменита здесь.$",
    "gFameCheckerFlavorText_Erika3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мы используем только GRASS-тип POKeMON в\nНаш Гим.\pМы также используем их для создания\nЦветочные композиции!$",
    "gFameCheckerFlavorText_Erika4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я никогда не собирал POKeMON если\nОни были непривлекательны.$",
    "gFameCheckerFlavorText_Erika5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Ходят слухи, что если вы заглянете в\nЧеладон Гим, вы можете часто\lСмотри, как Эрика спит.$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorText_LtSurge0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ГИМ ВЕРМИЛИОНА\nЛИДЕР: ЛТ. СЕРДЖ\lАМЕРИКАНСКАЯ МОЛНИЯ!$",
    "gFameCheckerFlavorText_LtSurge1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Знаешь, парень, ЭЛЕКТРИЧЕСКИЕ\nПОКЕМОНЫ спасли меня на войне!$",
    "gFameCheckerFlavorText_LtSurge2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Когда я служил в армии, ЛТ. СЕРДЖ\nбыл моим строгим командиром.\pОн был суровым начальником.$",
    "gFameCheckerFlavorText_LtSurge3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ЛТ. СЕРДЖ всегда славился\nосторожностью в армии.$",
    "gFameCheckerFlavorText_LtSurge4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ЛТ. СЕРДЖ сам установил ловушки\nв ГИМЕ.\pИ поставил повсюду двойные замки.$",
    "gFameCheckerFlavorText_LtSurge5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, ЛТ. СЕРДЖ был\nпилотом на родине, в Америке.\pОн питал самолёт электричеством\nсвоих ПОКЕМОНОВ.$",
    "gFameCheckerFlavorText_Erika0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ГИМ СЕЛАДОНА\nЛИДЕР: ЭРИКА\lПРИНЦЕССА ПРИРОДЫ!$",
    "gFameCheckerFlavorText_Erika1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я изучаю искусство\nсоставления букетов.\pВсе мои ПОКЕМОНЫ относятся\nк ТРАВЯНОМУ типу.$",
    "gFameCheckerFlavorText_Erika2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Наш ЛИДЕР ЭРИКА тиха,\nно здесь её знают все.$",
    "gFameCheckerFlavorText_Erika3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}В нашем ГИМЕ только ТРАВЯНЫЕ\nПОКЕМОНЫ.\pМы ведь ещё и создаём из них\nцветочные композиции!$",
    "gFameCheckerFlavorText_Erika4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я не стала бы ловить ПОКЕМОНОВ,\nесли бы они были некрасивыми.$",
    "gFameCheckerFlavorText_Erika5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, если заглянуть в\nГИМ СЕЛАДОНА, нередко можно\lувидеть, как ЭРИКА дремлет.$",
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
            "usage: localize_fame_checker_flavor_surge_erika_quality_v3_248.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.248 Fame Checker flavor set")

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

    out = root / "build" / "qarro_ru_fame_checker_flavor_surge_erika_quality_v3_248_audit.json"
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Lt. Surge/Erika Fame Checker flavor entries"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_flavor_koga_sabrina_quality_v3_249.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
