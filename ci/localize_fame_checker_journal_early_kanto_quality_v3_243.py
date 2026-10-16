#!/usr/bin/env python3
"""Qarro v3.243: human-quality early Kanto Fame Checker journal entries.

Polishes the five special POKéMON JOURNAL articles for Brock through Koga.
The EXPECTED bodies are the exact installed v3.8 machine-localized surfaces
captured from the handoff build. All FireRed control tokens are preserved
exactly and the pass fails closed on any source drift.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_JOURNAL_EARLY_KANTO_QUALITY_V3_243"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "PokemonJournal_Text_SpecialFeatureBrock":
        r"POKeMON ЙОРНАЛ\pСпециальная статья: PEWTER GYM\nЛидер Брок!\pБрок редко смеется, но, как говорят,\nНевозможно остановиться, если он начнет.$",
    "PokemonJournal_Text_SpecialFeatureMisty":
        r"POKeMON ЙОРНАЛ\pСпециальная функция: CERULEAN GYM\nЛидер MISTУ!\pMISTГоворят, что ты поклоняешься Лорели.\nИз элитной четверки.$",
    "PokemonJournal_Text_SpecialFeatureLtSurge":
        r"POKeMON ЙОРНАЛ\pСпециальная статья: VERMILION GYM\nЛидер ЛТ. БЕРЕЖЬ!\pПо слухам, именно LT.SURGE\nПилот, находясь дома в США.\pОн использовал электричество, которое вырабатывалось\nчерез POKeMON Чтобы управлять своим самолетом.$",
    "PokemonJournal_Text_SpecialFeatureErika":
        r"POKeMON ЙОРНАЛ\pСпециальная статья: CELADON GYM\nЛидер Эрика!\pХодят слухи, что если вы заглянете в\nЧеладон Гим, вы можете часто\lСмотри, как Эрика спит.$",
    "PokemonJournal_Text_SpecialFeatureKoga":
        r"POKeMON ЙОРНАЛ\pСпециальная статья: FUCHSIA GYM\nЛидер Кога!\pГоворят, что у Коги есть основательный\nЗнание медицины.\pОн даже придумывает лекарство для медсестры.\nего POKeMON За здоровье.$",
}

TRANSLATIONS = {
    "PokemonJournal_Text_SpecialFeatureBrock":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск: ГИМ ПЬЮТЕРА\nЛИДЕР БРОК!\pБРОК редко смеётся, но говорят,\nесли начнёт - уже не остановить.$",
    "PokemonJournal_Text_SpecialFeatureMisty":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск: ГИМ СЕРУЛИНА\nЛИДЕР МИСТИ!\pМИСТИ восхищается ЛОРЕЛЕЙ\nиз ЭЛИТНОЙ ЧЕТВЁРКИ.$",
    "PokemonJournal_Text_SpecialFeatureLtSurge":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск: ВЕРМИЛИОНСКИЙ ГИМ\nЛИДЕР ЛТ. СЕРДЖ!\pПо слухам, в Америке ЛТ. СЕРДЖ\nслужил пилотом.\pСамолёт он питал электричеством,\nкоторое вырабатывали ПОКЕМОНЫ.$",
    "PokemonJournal_Text_SpecialFeatureErika":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск: ГИМ СЕЛАДОНА\nЛИДЕР ЭРИКА!\pГоворят, если заглянуть в\nГИМ СЕЛАДОНА, часто можно\lувидеть спящую ЭРИКУ.$",
    "PokemonJournal_Text_SpecialFeatureKoga":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск: ГИМ ФУКСИИ\nЛИДЕР КОГА!\pГоворят, КОГА хорошо разбирается\nв медицине.\pОн даже готовит лекарства,\nчтобы лечить своих ПОКЕМОНОВ.$",
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
            "usage: localize_fame_checker_journal_early_kanto_quality_v3_243.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 5:
        raise RuntimeError("unexpected v3.243 Fame Checker journal set")

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

    out = root / "build" / "qarro_ru_fame_checker_journal_early_kanto_quality_v3_243_audit.json"
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} early Kanto Fame Checker journal entries"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_journal_mid_late_quality_v3_244.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
