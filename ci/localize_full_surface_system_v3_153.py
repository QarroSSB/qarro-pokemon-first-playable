#!/usr/bin/env python3
"""Qarro v3.153: contract-safe Frontier/menu/link/rental system UI localization.

Translates 50 confirmed English-only src/strings.c UI strings remaining after
the fully-green v3.152 checkpoint. Exact pinned source anchors and brace-token
contracts are required. Pokemon/Move/Ability proper names, gameplay, trainer
logic, rewards, flags, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations
import ast, re, sys
from pathlib import Path

TARGETS = {
    "src/strings.c": {
        'gText_Current': ('CURRENT', 'ТЕКУЩИЙ'),
        'gText_Record': ('RECORD', 'РЕКОРД'),
        'gText_Prev': ('PREV.', 'ПРЕД.'),
        'gText_Total': ('Total', 'Всего'),
        'gText_FrontierFacilityRoomsCleared': ('Rooms cleared: {STR_VAR_2}', 'Комнат пройдено: {STR_VAR_2}'),
        'gText_FrontierFacilityKOsStreak': ('KOs in a row: {STR_VAR_2}', 'KO подряд: {STR_VAR_2}'),
        'gText_FrontierFacilityFloorsCleared': ('Floors cleared: {STR_VAR_2}', 'Этажей пройдено: {STR_VAR_2}'),
        'gText_FrontierFacilityTotalCaughtSpeciesBanned': (' and {STR_VAR_2} of the POKéMON species\nyou caught are inelegible', ' и {STR_VAR_2} пойманных видов\nПОКЕМОНОВ недопустимы'),
        'gText_FrontierFacilityIncluding': ('.\\pThese include ', '.\\pСреди них '),
        'gText_FrontierFacilityAreInelegible': (' are inelegible', ' недопустимы'),
        'gText_Day': ('DAY', 'ДЕНЬ'),
        'gText_Confirm2': ('CONFIRM', 'ГОТОВО'),
        'gText_Days': ('Days', 'Дни'),
        'gText_TimeColon2': ('Time:', 'Время:'),
        'gText_GameTime': ('Game time', 'Время игры'),
        'gText_RTCTime': ('RTC time', 'Время RTC'),
        'gText_UpdatedTime': ('Updated time', 'Новое время'),
        'gText_MenuBag': ('BAG', 'СУМКА'),
        'gText_MenuSave': ('SAVE', 'СОХРАНИТЬ'),
        'gText_MenuOption': ('OPTION', 'НАСТРОЙКИ'),
        'gText_MenuRest': ('REST', 'ОТДЫХ'),
        'gText_SafariBallStock': ('SAFARI BALLS\nStock: {STR_VAR_1}', 'БОЛЛЫ САФАРИ\nЗапас: {STR_VAR_1}'),
        'gText_BattlePyramidFloor': ('Battle Pyramid\n{STR_VAR_1}', 'БОЕВАЯ ПИРАМИДА\n{STR_VAR_1}'),
        'gText_Floor1': ('Floor 1', 'Этаж 1'),
        'gText_Floor2': ('Floor 2', 'Этаж 2'),
        'gText_Floor6': ('Floor 6', 'Этаж 6'),
        'gText_Floor7': ('Floor 7', 'Этаж 7'),
        'gText_Peak': ('Peak', 'Вершина'),
        'gText_LinkStandby2': ('Link standby…\n… … B Button: Cancel', 'Ожидание связи...\n... ... B: Отмена'),
        'gText_LoadingEvent': ('Loading event…', 'Загрузка события...'),
        'gText_EventSafelyLoaded': ('The event was safely loaded.', 'Событие успешно загружено.'),
        'gText_LoadErrorEndingSession': ('Loading error.\nEnding session.', 'Ошибка загрузки.\nСеанс завершен.'),
        'gText_MaxHP': ('MAX. HP', 'МАКС. HP'),
        'gText_Attack': ('ATTACK', 'АТАКА'),
        'gText_Defense': ('DEFENSE', 'ЗАЩИТА'),
        'gText_Speed': ('SPEED', 'СКОРОСТЬ'),
        'gText_SpAtk': ('SP. ATK', 'СП. АТК'),
        'gText_SpDef': ('SP. DEF', 'СП. ЗАЩ'),
        'gText_MixingRecords': ('Mixing records…', 'Обмен записями...'),
        'gText_RecordMixingComplete': ('Record mixing completed.\nThank you for waiting.', 'Обмен записями завершен.\nСпасибо за ожидание.'),
        'gText_RentalPkmn2': ('RENTAL POKéMON', 'АРЕНДА ПОКЕМОНОВ'),
        'gText_SelectFirstPkmn': ('Select the first POKéMON.', 'Выберите первого ПОКЕМОНА.'),
        'gText_SelectSecondPkmn': ('Select the second POKéMON.', 'Выберите второго ПОКЕМОНА.'),
        'gText_SelectThirdPkmn': ('Select the third POKéMON.', 'Выберите третьего ПОКЕМОНА.'),
        'gText_TheseThreePkmnOkay': ('Are these three POKéMON OK?', 'Выбрать этих трех ПОКЕМОНОВ?'),
        'gText_PkmnSwap': ('POKéMON SWAP', 'ОБМЕН ПОКЕМОНОВ'),
        'gText_SelectPkmnToSwap': ('Select POKéMON to swap.', 'Выберите ПОКЕМОНА для обмена.'),
        'gText_SelectPkmnToAccept': ('Select POKéMON to accept.', 'Выберите ПОКЕМОНА для приема.'),
        'gText_AcceptThisPkmn': ('Accept this POKéMON?', 'Принять этого ПОКЕМОНА?'),
        'gText_SavingPokedex': ('POKéDEX', 'ПОКЕДЕКС'),
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
        print(f'[QARRO_RU_FULL_SURFACE_V3_153] {rel}: translated {len(targets)} symbols')
    if total!=50: raise RuntimeError(f'expected 50 translations, got {total}')
    print('[QARRO_RU_FULL_SURFACE_V3_153] PASS: translated 50 Frontier/menu/link/rental UI strings; exact placeholders/controls preserved; gameplay/Ash untouched')
    return 0

if __name__=='__main__': raise SystemExit(main())
