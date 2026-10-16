#!/usr/bin/env python3
"""Qarro v3.245: finish human-quality Fame Checker journal localization.

Polishes the final four special POKéMON JOURNAL articles: Lance, Prof. Oak,
Daisy Oak and Mr. Fuji. EXPECTED bodies are exact installed v3.8 handoff
surfaces. All FireRed control tokens and placeholders are preserved exactly;
any source drift aborts.

Text only: gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay
untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_JOURNAL_FINAL_QUALITY_V3_245"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "PokemonJournal_Text_SpecialFeatureLance":
        r"POKeMON ЙОРНАЛ\pОсобенность:\nСпокойствие Элита Фоур!\pДедушка Ланса считается\nБудьте старшим из известного клана\lМастера драконов.$",
    "PokemonJournal_Text_SpecialFeatureProfOak":
        r"POKeMON ЙОРНАЛ\pСпециальная функция: PROF. OAK,\nтот POKeMON Исследователь!\pПо сообщениям, ОАК живет со своим\nВнуки Дейзи и {RIVAL}.$",
    "PokemonJournal_Text_SpecialFeatureDaisyOak":
        r"Это - а POKeMON ИОРНАЛЬНЫЙ\nНесколько лет назад...\pPOKeMON ЙОРНАЛ\nСпециальный конкурс!\pВесна POKeMON Конте\nЧемпион мира Дейзи Ок\lПаллетный бутон!$",
    "PokemonJournal_Text_SpecialFeatureMrFuji":
        r"POKeMON ЙОРНАЛ\pОсобенность:\nГ-н Фуджи из POKeMON Дом!\pРедактор: Застенчивый мистер Фуджи повернулся\nЗапишите наши запросы на интервью.\pОн добрый человек, которого обожают.\nИ уважаем в городе Лавендер.$",
}

TRANSLATIONS = {
    "PokemonJournal_Text_SpecialFeatureLance":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск:\nЛЭНС ИЗ ЭЛИТНОЙ ЧЕТВЁРКИ!\pДедушка ЛЭНСА - старейшина\nзнаменитого клана\lмастеров драконов.$",
    "PokemonJournal_Text_SpecialFeatureProfOak":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск: ПРОФ. ОУК,\nИССЛЕДОВАТЕЛЬ ПОКЕМОНОВ!\pГоворят, ПРОФ. ОУК живёт со своими\nвнуками ДЭЙЗИ и {RIVAL}.$",
    "PokemonJournal_Text_SpecialFeatureDaisyOak":
        r"Это ЖУРНАЛ ПОКЕМОНОВ\nмноголетней давности...\pЖУРНАЛ ПОКЕМОНОВ\nСПЕЦВЫПУСК О КОНКУРСЕ!\pПобедительница весеннего\nКОНКУРСА ПОКЕМОНОВ - ДЭЙЗИ ОУК\lиз ПАЛЛЕТ-ТАУНА!$",
    "PokemonJournal_Text_SpecialFeatureMrFuji":
        r"ЖУРНАЛ ПОКЕМОНОВ\pСпецвыпуск:\nМИСТЕР ФУДЗИ ИЗ ДОМА ПОКЕМОНОВ!\pРедактор: застенчивый МИСТЕР ФУДЗИ\nотказался от нашего интервью.\pЭто добрый человек, которого любят\nи уважают в ЛАВАНДЕР-ТАУНЕ.$",
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
            "usage: localize_fame_checker_journal_final_quality_v3_245.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 4:
        raise RuntimeError("unexpected v3.245 Fame Checker journal set")

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

    out = root / "build" / "qarro_ru_fame_checker_journal_final_quality_v3_245_audit.json"
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
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} final Fame Checker journal entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
