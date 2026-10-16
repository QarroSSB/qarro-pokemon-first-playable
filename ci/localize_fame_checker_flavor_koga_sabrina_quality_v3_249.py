#!/usr/bin/env python3
"""Qarro v3.249: human-quality Fame Checker flavor text for Koga and Sabrina.

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

MARKER = "QARRO_RU_FAME_CHECKER_FLAVOR_KOGA_SABRINA_QUALITY_V3_249"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorText_Koga0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Город Фуксии POKeMON ГИМ\nРуководитель: Кога\lЯдовитый мастер ниндзя$",
    "gFameCheckerFlavorText_Koga1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Отчаяние перед ползучим ужасом\nПойсонный тип POKeMON!$",
    "gFameCheckerFlavorText_Koga2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Даже если я проиграл, я буду продолжать\nОбучение в соответствии с учением\lКога, мой мастер ниндзя.$",
    "gFameCheckerFlavorText_Koga3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мой отец - лидер гинекологии\nэтого города.\pЯ тренируюсь использовать ПОИСОН POKeMON\nКак и мой отец.$",
    "gFameCheckerFlavorText_Koga4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, что у Коги есть основательный\nЗнание медицины.\pОн даже придумывает лекарство для медсестры.\nего POKeMON За здоровье.$",
    "gFameCheckerFlavorText_Koga5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Зона Сафари огромна, не\nТы говоришь?\pГим-лидер Фуксии, Кога, \nОни часто патрулируют территорию.\pБлагодаря ему мы можем играть здесь.\nЗная, что мы в безопасности.$",
    "gFameCheckerFlavorText_Sabrina0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Город САФФРОНА POKeMON ГИМ\nЛидер: Сабрина\lМастера в этом PSYCHIC POKeMON!$",
    "gFameCheckerFlavorText_Sabrina1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Ты знаешь о девушке, которая водит машину\nВ городе Саффрон?\pОна использует PSYCHICтип POKeMON,\nПравда?$",
    "gFameCheckerFlavorText_Sabrina2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}У меня были психические способности с тех пор, как я\nЯ был ребенком.\pВсе началось, когда я\nНебрежно подброшенный, согнутый.$",
    "gFameCheckerFlavorText_Sabrina3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я не люблю драться, но если хочешь,\nЯ покажу тебе свои силы!$",
    "gFameCheckerFlavorText_Sabrina4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, что Сабрина может\nобщаться с ней POKeMON\lВо время боя без слов.$",
    "gFameCheckerFlavorText_Sabrina5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Сабрина только что уничтожила каратэ\nУбийца по соседству.$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorText_Koga0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ГИМ ФУКСИИ\nЛИДЕР: КОГА\lЯДОВИТЫЙ МАСТЕР-НИНДЗЯ$",
    "gFameCheckerFlavorText_Koga1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Познай ползучий ужас\nЯДОВИТЫХ ПОКЕМОНОВ!$",
    "gFameCheckerFlavorText_Koga2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Даже проиграв, я продолжу\nследовать наставлениям\lКОГИ, моего мастера-ниндзя.$",
    "gFameCheckerFlavorText_Koga3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Мой отец - ЛИДЕР ГИМА\nэтого города.\pЯ тоже учусь владеть ЯДОВИТЫМИ\nПОКЕМОНАМИ, как мой отец.$",
    "gFameCheckerFlavorText_Koga4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, КОГА отлично\nразбирается в медицине.\pОн даже сам готовит лекарства,\nчтобы лечить своих ПОКЕМОНОВ.$",
    "gFameCheckerFlavorText_Koga5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}САФАРИ-ЗОНА огромна,\nправда?\pЛИДЕР ГИМА ФУКСИИ, КОГА,\nвремя от времени патрулирует её.\pБлагодаря ему мы играем здесь,\nзная, что мы в безопасности.$",
    "gFameCheckerFlavorText_Sabrina0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}ГИМ САФФРОНА\nЛИДЕР: САБРИНА\lМАСТЕР ПСИХИЧЕСКИХ ПОКЕМОНОВ!$",
    "gFameCheckerFlavorText_Sabrina1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Знаешь девушку-ЛИДЕРА ГИМА\nиз САФФРОНА?\pОна использует ПСИХИЧЕСКИХ ПОКЕМОНОВ,\nверно?$",
    "gFameCheckerFlavorText_Sabrina2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}У меня с детства были\nпсихические способности.\pВсё началось, когда ложка,\nкоторую я бросила, согнулась.$",
    "gFameCheckerFlavorText_Sabrina3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я не люблю сражаться, но если хочешь,\nпокажу тебе свою силу!$",
    "gFameCheckerFlavorText_Sabrina4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, САБРИНА может\nобщаться со своими ПОКЕМОНАМИ\lв бою, не произнося ни слова.$",
    "gFameCheckerFlavorText_Sabrina5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}САБРИНА только что разгромила\nМАСТЕРА КАРАТЭ по соседству.$",
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
            "usage: localize_fame_checker_flavor_koga_sabrina_quality_v3_249.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.249 Fame Checker flavor set")

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

    out = root / "build" / "qarro_ru_fame_checker_flavor_koga_sabrina_quality_v3_249_audit.json"
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Koga/Sabrina Fame Checker flavor entries"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_flavor_blaine_lorelei_quality_v3_250.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
