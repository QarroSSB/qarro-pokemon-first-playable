#!/usr/bin/env python3
"""Qarro v3.151: contract-safe remaining Frontier/record UI localization.

Translates 33 confirmed English-only src/strings.c system/UI strings that remain
unchanged in the fully-green v3.150 build diff. Exact pinned source anchors and
brace-token contracts are required. Pokemon/Move/Ability proper names,
gameplay, trainer logic, rewards, flags, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations
import ast, re, sys
from pathlib import Path

TARGETS = {
    "src/strings.c": {
        'gText_SingleBattleRoomResults': ("{PLAYER}'s Single Battle Room Results", 'ОДИНОЧНАЯ КОМНАТА: {PLAYER}'),
        'gText_DoubleBattleRoomResults': ("{PLAYER}'s Double Battle Room Results", 'ДВОЙНАЯ КОМНАТА: {PLAYER}'),
        'gText_MultiBattleRoomResults': ("{PLAYER}'s Multi Battle Room Results", 'МУЛЬТИ-КОМНАТА: {PLAYER}'),
        'gText_LinkMultiBattleRoomResults': ("{PLAYER}'s Link Multi Battle Room Results", 'LINK-МУЛЬТИ: {PLAYER}'),
        'gText_SingleBattleTourneyResults': ("{PLAYER}'s Single Battle Tourney Results", 'ОДИНОЧНЫЙ ТУРНИР: {PLAYER}'),
        'gText_DoubleBattleTourneyResults': ("{PLAYER}'s Double Battle Tourney Results", 'ДВОЙНОЙ ТУРНИР: {PLAYER}'),
        'gText_SingleBattleHallResults': ("{PLAYER}'s Single Battle Hall Results", 'ОДИНОЧНЫЙ ЗАЛ: {PLAYER}'),
        'gText_DoubleBattleHallResults': ("{PLAYER}'s Double Battle Hall Results", 'ДВОЙНОЙ ЗАЛ: {PLAYER}'),
        'gText_BattleChoiceResults': ("{PLAYER}'s Battle Choice Results", 'ВЫБОР БИТВЫ: {PLAYER}'),
        'gText_SetKOTourneyResults': ("{PLAYER}'s Set KO Tourney Results", 'KO-ТУРНИР: {PLAYER}'),
        'gText_BattleSwapSingleResults': ("{PLAYER}'s Battle Swap Single Results", 'ОБМЕН 1 НА 1: {PLAYER}'),
        'gText_BattleSwapDoubleResults': ("{PLAYER}'s Battle Swap Double Results", 'ДВОЙНОЙ ОБМЕН: {PLAYER}'),
        'gText_BattleQuestResults': ("{PLAYER}'s Battle Quest Results", 'БОЕВОЙ КВЕСТ: {PLAYER}'),
        'gText_WinStreak': ('Win streak: {STR_VAR_1}', 'Серия побед: {STR_VAR_1}'),
        'gText_RentalSwap': ('Rental/Swap', 'Аренда/Обмен'),
        'gText_ClearStreak': ('Clear streak: {STR_VAR_1}', 'Серия зачисток: {STR_VAR_1}'),
        'gText_Championships': ('Championships: {STR_VAR_1}', 'Чемпионств: {STR_VAR_1}'),
        'gText_RoomsCleared': ('Rooms cleared: {STR_VAR_1}', 'Комнат пройдено: {STR_VAR_1}'),
        'gText_TimesCleared': ('Times cleared:{CLEAR 5}{STR_VAR_1}', 'Пройдено раз:{CLEAR 5}{STR_VAR_1}'),
        'gText_KOsInARow': ('KOs in a row: {STR_VAR_1}', 'KO подряд: {STR_VAR_1}'),
        'gText_TimesVar1': ('Times: {STR_VAR_1}', 'Раз: {STR_VAR_1}'),
        'gText_FloorsCleared': ('Floors cleared: {STR_VAR_1}', 'Этажей пройдено: {STR_VAR_1}'),
        'gText_FrontierFacilityWinStreak': ('Win streak: {STR_VAR_2}', 'Серия побед: {STR_VAR_2}'),
        'gText_FrontierFacilityClearStreak': ('Clear streak: {STR_VAR_2}', 'Серия зачисток: {STR_VAR_2}'),
        'gText_Floor3': ('Floor 3', 'Этаж 3'),
        'gText_Floor4': ('Floor 4', 'Этаж 4'),
        'gText_Floor5': ('Floor 5', 'Этаж 5'),
        'gText_QuitSwapping': ('Quit swapping?', 'Закончить обмен?'),
        'gText_Yes3': ('YES', 'ДА'),
        'gText_No3': ('NO', 'НЕТ'),
        'gText_TrainerHill2F': ('2F', '2Э'),
        'gText_TrainerHill3F': ('3F', '3Э'),
        'gText_TrainerHill4F': ('4F', '4Э'),
    },
}

C_QUOTED_RE = re.compile(r'"(?:\\.|[^"\\])*"')
TOKEN_RE = re.compile(r'\{[^{}]+\}')

def decode_body(body: str) -> str:
    vals=[]
    for q in C_QUOTED_RE.findall(body):
        try: vals.append(ast.literal_eval(q))
        except Exception: vals.append(q[1:-1])
    return ''.join(vals)

def encode_body(text: str) -> str:
    # Preserve FireRed text escapes (e.g. \\p / \\l); only encode real newlines and C quotes.
    return '"' + text.replace('"','\\"').replace('\n', '\\n') + '"'

def brace_tokens(s: str):
    return TOKEN_RE.findall(s)

def patch_symbol(text: str, symbol: str, expected: str, replacement: str) -> tuple[str,int]:
    if brace_tokens(expected) != brace_tokens(replacement):
        raise RuntimeError(f'{symbol}: brace-token contract changed: {brace_tokens(expected)} -> {brace_tokens(replacement)}')
    rx=re.compile(
        r'(?ms)(?P<head>^(?:ALIGNED\(4\)\s+)?(?:static\s+)?const\s+u8\s+'+re.escape(symbol)+
        r'\s*(?:\[[^\]]*\])?\s*=\s*(?:COMPOUND_STRING|_)\s*\(\s*)'+
        r'(?P<body>(?:"(?:\\.|[^"\\])*"\s*)+)'+
        r'(?P<tail>\)\s*;)'
    )
    matches=list(rx.finditer(text))
    if len(matches)!=1:
        raise RuntimeError(f'{symbol}: expected exactly one string definition, got {len(matches)}')
    m=matches[0]
    actual=decode_body(m.group('body'))
    if actual==replacement:
        return text,1
    if re.search(r"[А-Яа-яЁё]", actual):
        if brace_tokens(actual) != brace_tokens(expected):
            raise RuntimeError(
                f'{symbol}: already-Cyrillic placeholder drift\\n'
                f'EXPECTED_PLACEHOLDERS={brace_tokens(expected)!r}\\n'
                f'ACTUAL_PLACEHOLDERS={brace_tokens(actual)!r}'
            )
        return text,1
    if actual!=expected:
        raise RuntimeError(f'{symbol}: source drift\nEXPECTED={expected!r}\nACTUAL={actual!r}')
    new=m.group('head')+encode_body(replacement)+m.group('tail')
    return text[:m.start()]+new+text[m.end():],1

def main() -> int:
    if len(sys.argv)!=2:
        print(f'usage: {Path(sys.argv[0]).name} <upstream-root>',file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve(); total=0
    for rel,targets in TARGETS.items():
        path=root/rel
        if not path.is_file(): raise RuntimeError(f'missing target file: {path}')
        text=path.read_text(encoding='utf-8'); before=text
        for symbol,(expected,replacement) in targets.items():
            text,n=patch_symbol(text,symbol,expected,replacement); total+=n
        # Idempotent replay is valid when exact targets are already localized.
        path.write_text(text,encoding='utf-8')
        print(f'[QARRO_RU_FULL_SURFACE_V3_151] {rel}: translated {len(targets)} symbols')
    if total!=33: raise RuntimeError(f'expected 33 translations, got {total}')
    print('[QARRO_RU_FULL_SURFACE_V3_151] PASS: translated 33 remaining Frontier/record UI strings; exact placeholders/controls preserved; gameplay/Ash untouched')
    return 0

if __name__=='__main__': raise SystemExit(main())
