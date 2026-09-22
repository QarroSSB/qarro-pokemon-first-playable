#!/usr/bin/env python3
"""Qarro v3.196: human-quality cleanup for broken core src/strings.c UI text.

Replaces 42 badly machine-translated single-string symbols by symbol name.
Runtime control-token sequences are compared against the currently reconstructed
source before every replacement, so any source drift fails closed.
Pokemon, Move and Ability proper names stay English. Gameplay logic is untouched.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_STRINGS_CORE_QUALITY_V3_196"
TARGET = Path("src/strings.c")
TRANSLATIONS = {
    "gText_ExpandedPlaceholder_Sapphire": "САПФИР",
    "gText_ExpandedPlaceholder_Ruby": "РУБИН",
    "gText_ExpandedPlaceholder_Emerald": "ИЗУМРУД",
    "gText_ExpandedPlaceholder_Aqua": "АКВА",
    "gText_ExpandedPlaceholder_Magma": "МАГМА",
    "gText_ExpandedPlaceholder_Archie": "АРЧИ",
    "gText_ExpandedPlaceholder_Maxie": "МАКСИ",
    "gText_ExpandedPlaceholder_Brendan": "БРЕНДАН",
    "gText_ExpandedPlaceholder_May": "МЭЙ",
    "gText_ExpandedPlaceholder_Red": "РЭД",
    "gText_ExpandedPlaceholder_Green": "ГРИН",
    "gText_AButton": "КНОПКА A",
    "gText_BButton": "КНОПКА B",
    "gText_RButton": "КНОПКА R",
    "gText_LButton": "КНОПКА L",
    "gText_Start": "START",
    "gText_Select": "ВЫБОР",
    "gText_ControlPad": "+ КРЕСТОВИНА",
    "gText_ThisIsAPokemon": "Вот кого мы называем POKeMON.{PAUSE 96}\\p",
    "gText_CryOf": "КРИК",
    "gText_SizeComparedTo": "РАЗМЕР ОТНОСИТЕЛЬНО ",
    "gText_HOFDexSaving": "СОХРАНЕНИЕ...\\nНЕ ВЫКЛЮЧАЙ ПИТАНИЕ.",
    "gText_Number": "No. ",
    "gText_IDNumber": "ID НОМЕР",
    "gText_ConfirmStarterChoice": "Выбираешь этого POKeMON?",
    "gText_Berry2": " ЯГОДА",
    "gText_SpAtk3": "СП. АТК",
    "gText_SpDef3": "СП. ЗАЩ",
    "gText_NextFusionMon": "Выбери {PKMN} для слияния.",
    "gText_Have": "ЕСТЬ",
    "gText_DontHave": "НЕТ",
    "gText_Fourth": "ЧЕТВЕРТЫЙ",
    "gText_ReturnToWaitingRoom": "Вернуться в ЗАЛ ОЖИДАНИЯ?",
    "gText_CancelChallenge": "Отменить испытание?",
    "gText_PkmnCantBeTraded": "Этого POKeMON нельзя обменять.",
    "gText_OTSlash": "OT/",
    "gText_RentalPkmn": "АРЕНДНЫЙ POKeMON",
    "gText_Appeal": "ПРИВЛЕЧ.",
    "gText_Jam": "ПОМЕХА",
    "gText_RibbonsVar1": "ЛЕНТЫ: {STR_VAR_1}",
    "gText_Events": "СОБЫТИЯ",
    "gText_ContestMoves": "КОНКУРСНЫЕ ПРИЕМЫ",
}
BANNED_UNICODE = set("—–←→“”«»")

def control_tokens(text: str) -> list[str]:
    return re.findall(r'\{[^}]+\}|\\.|\$', text)

def replace_symbol(path: Path, symbol: str, translated: str) -> None:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(?m)^(?P<prefix>\s*(?:ALIGNED\(4\)\s+)?(?:static\s+)?const u8\s+'
        rf'{re.escape(symbol)}\[\]\s*=\s*_\(")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\);(?:\s*//.*)?\s*)$'
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{path}:{symbol}: expected one string symbol, got {len(matches)}")
    m = matches[0]
    current = m.group("body")
    if control_tokens(current) != control_tokens(translated):
        raise RuntimeError(
            f"{path}:{symbol}: control-token drift "
            f"old={control_tokens(current)} new={control_tokens(translated)}"
        )
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{path}:{symbol}: invalid translation surface")
    updated = text[:m.start()] + m.group("prefix") + translated + m.group("suffix") + text[m.end():]
    path.write_text(updated, encoding="utf-8")

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_strings_core_quality_v3_196.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 42:
        raise RuntimeError(f"expected 42 symbols, got {len(TRANSLATIONS)}")
    for symbol, translated in TRANSLATIONS.items():
        replace_symbol(path, symbol, translated)
    out = root / "build" / "qarro_ru_strings_core_quality_v3_196_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassSymbols": len(TRANSLATIONS),
        "symbols": list(TRANSLATIONS),
        "humanEditedRussian": True,
        "controlTokensPreserved": True,
        "pokemonMoveAbilityNamesPreserved": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} core UI symbols in {TARGET}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
