#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_FINISH_TAIL_CLEANUP_V3_178"

def replace_once(path: Path, old: str, new: str, label: str):
    text = path.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{path}:{label}: expected one anchor, got {n}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

def replace_symbol(path: Path, symbol: str, new: str):
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(?m)^(?P<prefix>\s*(?:ALIGNED\(4\)\s+)?(?:static\s+)?const u8\s+'
        rf'{re.escape(symbol)}\[\]\s*=\s*_\(")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\);(?:\s*//.*)?\s*)$'
    )
    ms = list(pat.finditer(text))
    if len(ms) != 1:
        raise RuntimeError(f"{path}:{symbol}: expected one string symbol, got {len(ms)}")
    m = ms[0]
    text = text[:m.start()] + m.group("prefix") + new + m.group("suffix") + text[m.end():]
    path.write_text(text, encoding="utf-8")

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_finish_tail_cleanup_v3_178.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    translated = []
    cleaned = []

    trainers = root / "data/text/trainers.inc"
    replace_once(trainers,
                 '\t.string "← Мы всегда сражаемся POKeMON,\\nЯ и моя сестра.\\pЯ всегда проигрываю, но мы можем победить тебя.\\n2 на 2!$"',
                 '\t.string "РЭЙ: Мы всегда сражаемся POKeMON,\\nЯ и моя сестра.\\pЯ всегда проигрываю, но мы можем победить тебя.\\n2 на 2!$"',
                 "Ray trainer name mistranslated as arrow")
    cleaned.append("Route107_Text_RayIntro")

    battle = root / "src/battle_message.c"
    replace_once(battle, '[DOME_ROUND1]    = COMPOUND_STRING("Round 1"),',
                         '[DOME_ROUND1]    = COMPOUND_STRING("Раунд 1"),', "DOME round 1")
    replace_once(battle, '[DOME_ROUND2]    = COMPOUND_STRING("Round 2"),',
                         '[DOME_ROUND2]    = COMPOUND_STRING("Раунд 2"),', "DOME round 2")
    translated += ["DOME_ROUND1", "DOME_ROUND2"]

    dex = root / "src/pokedex.c"
    replace_once(dex, 'COMPOUND_STRING("HOENN DEX")',
                      'COMPOUND_STRING("ПОКЕДЕКС HOENN")', "HOENN short dex")
    replace_once(dex, 'COMPOUND_STRING("NATIONAL DEX")',
                      'COMPOUND_STRING("НАЦ. ПОКЕДЕКС")', "National short dex")
    translated += ["DEX_MODE_HOENN short", "DEX_MODE_NATIONAL short"]

    moves = root / "src/data/moves_info.h"
    old = '        .description = COMPOUND_STRING(\n            "Super effective on Water-\\n"\n            "types."),'
    new = '        .description = COMPOUND_STRING(\n            "Суперэффективен против\\n"\n            "водного типа."),'
    replace_once(moves, old, new, "Freeze-Dry champions description")
    translated.append("Freeze-Dry champions description")

    strings = root / "src/strings.c"
    clean_strings = {
        "gText_PickOk": "{DPAD_UPDOWN}ВЫБОР {A_BUTTON}ОК.",
        "gText_PickNextCancel": "{DPAD_UPDOWN}ВЫБОР {A_BUTTON}ДАЛЕЕ {B_BUTTON}ОТМЕНА",
        "gText_PickCancel": "{DPAD_UPDOWN}ВЫБОР {A_BUTTON}{B_BUTTON}ОТМЕНА",
        "gText_UnusedCancel": "ОТМЕНА",
        "gText_Cancel4": "ОТМЕНА",
        "gText_Cancel5": "ОТМЕНА",
        "gText_PokemonNature": "ХАРАКТЕР POKeMON",
        "gText_PokemonMoves": "ПРИЕМЫ POKeMON",
        "gText_BattlePokemon": "БОЙ POKeMON",
        "gText_PokemonLeague": "ЛИГА POKeMON",
        "gText_Seafloor": "МОРСКОЕ ДНО",
        "gText_Cloudy": "ОБЛАЧНО",
        "gText_Sunny2": "СОЛНЕЧНО2",
        "gText_Sunny3": "СОЛНЕЧНО3",
        "gText_HeavyRain": "СИЛЬНЫЙ ДОЖДЬ",
        "gText_Quiz": "ВИКТОРИНА",
        "gText_Answer": "ОТВЕТ",
    }
    for sym, val in clean_strings.items():
        replace_symbol(strings, sym, val)
        cleaned.append(sym)

    replace_symbol(battle, "gText_BattleMenu",
                   "БОЙ{CLEAR_TO 56}СУМКА\\nPOKeMON{CLEAR_TO 56}БЕГ")
    replace_symbol(battle, "gText_SafariZoneMenu",
                   "МЯЧ{CLEAR_TO 56}{POKEBLOCK}\\nПОДОЙТИ{CLEAR_TO 56}БЕГ")
    replace_symbol(battle, "gText_WhichMoveToForget4",
                   "{PALETTE 5}{BACKGROUND DYNAMIC_COLOR5}{TEXT_COLORS DYNAMIC_COLOR4 DYNAMIC_COLOR6 DYNAMIC_COLOR5}Какой прием\\nзабыть?")
    cleaned += ["gText_BattleMenu", "gText_SafariZoneMenu", "gText_WhichMoveToForget4"]

    out = root / "build" / "qarro_ru_finish_tail_cleanup_v3_178_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "translatedRealTailCount": len(translated),
        "translatedRealTail": translated,
        "bulkUiCleanupCount": len(cleaned),
        "bulkUiCleanupSymbols": cleaned,
        "technicalEnglishPreserved": True,
        "creditsProperNamesPreserved": True,
        "pokemonMoveAbilityNamesPreserved": True,
        "gameplayLogicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(translated)} real tail candidates; cleaned {len(cleaned)} bulk UI strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
