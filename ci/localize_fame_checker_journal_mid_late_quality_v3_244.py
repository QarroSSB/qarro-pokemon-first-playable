#!/usr/bin/env python3
"""Qarro v3.244: human-quality Fame Checker journal entries, Sabrina through Agatha.

Polishes five special POKéMON JOURNAL articles. EXPECTED bodies are exact
installed v3.8 machine-localized handoff surfaces. FireRed control tokens are
preserved exactly; any source drift aborts.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_JOURNAL_MID_LATE_QUALITY_V3_244"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "PokemonJournal_Text_SpecialFeatureSabrina":
        r"POKeMON ЙОРНАЛ\pСпециальная статья: SAFFRON GYM\nЛидер Сабрина!\pГоворят, что Сабрина может\nобщаться с ней POKeMON\lВо время боя без слов.$",
    "PokemonJournal_Text_SpecialFeatureBlaine":
        r"POKeMON ЙОРНАЛ\pОригинальное название: CINNABAR GYM\nЛидер Блейн!\pГоворят, что Блэйн убирает свою темноту.\nИ только тогда, когда он думает\lНовые вопросы викторины.$",
    "PokemonJournal_Text_SpecialFeatureLorelei":
        r"POKeMON ЙОРНАЛ\pОсобенность:\nЛОРЛЕЙ Элитной Четверки!\pИзвестен своей логикой, расчетливостью,\nХороший стиль боя, Лорелия\lУ него есть удивительный секрет!$",
    "PokemonJournal_Text_SpecialFeatureBruno":
        r"POKeMON ЙОРНАЛ\pОсобенность:\nБрюно Элитной Четверки!\pБруно, по-видимому, присоединился к элите.\nЧетыре из его жгучих амбиций\lСражайтесь с лучшими тренерами.$",
    "PokemonJournal_Text_SpecialFeatureAgatha":
        r"POKeMON ЙОРНАЛ\pОсобенность:\nАгата Элита Фоура!\pВ юности Агата и Проф.\nОАК были соперниками, которые боролись за\lПревосходство как тренеры.$",
}

TRANSLATIONS = {
    "PokemonJournal_Text_SpecialFeatureSabrina":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск: ГИМ САФФРОНА\nЛИДЕР САБРИНА!\pГоворят, САБРИНА может\nмысленно общаться с ПОКЕМОНАМИ\lпрямо во время боя.$",
    "PokemonJournal_Text_SpecialFeatureBlaine":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск: ГИМ КИННАБАРА\nЛИДЕР БЛЕЙН!\pБЛЕЙН снимает тёмные очки лишь\nкогда придумывает\lновые вопросы для викторины.$",
    "PokemonJournal_Text_SpecialFeatureLorelei":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск:\nЛОРЕЛЕЙ ИЗ ЭЛИТНОЙ ЧЕТВЁРКИ!\pЛОРЕЛЕЙ известна точным,\nхладнокровным стилем боя,\lно у неё есть неожиданный секрет!$",
    "PokemonJournal_Text_SpecialFeatureBruno":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск:\nБРУНО ИЗ ЭЛИТНОЙ ЧЕТВЁРКИ!\pГоворят, БРУНО вошёл в ЭЛИТНУЮ\nЧЕТВЁРКУ из горячего желания\lсражаться с лучшими ТРЕНЕРАМИ.$",
    "PokemonJournal_Text_SpecialFeatureAgatha":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск:\nАГАТА ИЗ ЭЛИТНОЙ ЧЕТВЁРКИ!\pВ молодости АГАТА и ПРОФ. ОУК\nбыли соперниками и боролись\lза первенство среди ТРЕНЕРОВ.$",
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
        raise RuntimeError(f"{label}: expected one journal entry, got {len(matches)}")
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
            "usage: localize_fame_checker_journal_mid_late_quality_v3_244.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 5:
        raise RuntimeError("unexpected v3.244 Fame Checker journal set")

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

    out = root / "build" / "qarro_ru_fame_checker_journal_mid_late_quality_v3_244_audit.json"
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Sabrina-Agatha Fame Checker journal entries"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_journal_final_quality_v3_245.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
