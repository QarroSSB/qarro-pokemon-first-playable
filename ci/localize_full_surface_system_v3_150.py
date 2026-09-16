#!/usr/bin/env python3
"""Qarro v3.150: contract-safe RTC/Trainer Card/chat/Berry Crush/Frontier UI localization.

Translates 72 confirmed English-only src/strings.c system/UI strings remaining
in the post-v3.148 audit. Exact pinned source anchors and brace-token contracts
are required. Pokemon/Move/Ability proper names, gameplay, trainer logic,
rewards, flags, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations
import ast, re, sys
from pathlib import Path

TARGETS = {
    "src/strings.c": {
        'gText_ResetRTCConfirmCancel': ('Reset RTC?\nA: Confirm, B: Cancel', 'Сбросить RTC?\nA: Да, B: Отмена'),
        'gText_PresentTime': ('Present time in game', 'Текущее время в игре'),
        'gText_PreviousTime': ('Previous time in game', 'Предыдущее время в игре'),
        'gText_PleaseResetTime': ('Please reset the time.', 'Установи время заново.'),
        'gText_TrainerCardIDNo': ('IDNo.', 'ИД№'),
        'gText_WinsLosses': ('W:{COLOR RED}{SHADOW LIGHT_RED}{STR_VAR_1}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}  L:{COLOR RED}{SHADOW LIGHT_RED}{STR_VAR_2}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}', 'В:{COLOR RED}{SHADOW LIGHT_RED}{STR_VAR_1}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}  П:{COLOR RED}{SHADOW LIGHT_RED}{STR_VAR_2}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}'),
        'gText_UnionTradesAndBattles': ('UNION TRADES & BATTLES', 'UNION: ОБМЕНЫ И БОИ'),
        'gText_WonContestsWFriends': ('WON CONTESTS W/FRIENDS', 'ПОБЕДЫ В КОНКУРСАХ С ДРУЗ.'),
        'gText_BattlePtsWon': ('BATTLE POINTS WON', 'ВЫИГРАНО БОЕВЫХ ОЧКОВ'),
        'gText_BattleTower': ('BATTLE TOWER', 'БАШНЯ БИТВ'),
        'gText_WinsStraight': ('W/{COLOR RED}{SHADOW LIGHT_RED}{STR_VAR_1}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}  STRAIGHT/{COLOR RED}{SHADOW LIGHT_RED}{STR_VAR_2}', 'В/{COLOR RED}{SHADOW LIGHT_RED}{STR_VAR_1}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}  СЕРИЯ/{COLOR RED}{SHADOW LIGHT_RED}{STR_VAR_2}'),
        'gText_BattleTower2': ('BATTLE TOWER', 'БАШНЯ БИТВ'),
        'gText_BattleDome': ('BATTLE DOME', 'БОЕВОЙ КУПОЛ'),
        'gText_BattlePalace': ('BATTLE PALACE', 'БОЕВОЙ ДВОРЕЦ'),
        'gText_BattleFactory': ('BATTLE FACTORY', 'БОЕВАЯ ФАБРИКА'),
        'gText_BattleArena': ('BATTLE ARENA', 'БОЕВАЯ АРЕНА'),
        'gText_BattlePike': ('BATTLE PIKE', 'БОЕВАЯ ПИКА'),
        'gText_BattlePyramid': ('BATTLE PYRAMID', 'БОЕВАЯ ПИРАМИДА'),
        'gText_FacilitySingle': ('{STR_VAR_1} SINGLE', '{STR_VAR_1} ОДИНОЧ.'),
        'gText_FacilityDouble': ('{STR_VAR_1} DOUBLE', '{STR_VAR_1} ДВОЙНОЙ'),
        'gText_FacilityMulti': ('{STR_VAR_1} MULTI', '{STR_VAR_1} МУЛЬТИ'),
        'gText_FacilityLink': ('{STR_VAR_1} LINK', '{STR_VAR_1} СВЯЗЬ'),
        'gText_Give': ('Give', 'Дать'),
        'gText_NoNeed': ('No need', 'Не нужно'),
        'gText_AnnouncingResults': ('Announcing the results!', 'Объявляем результаты!'),
        'gText_PreliminaryResults': ('The preliminary results!', 'Предварительные результаты!'),
        'gText_Round2Results': ('Round 2 results!', 'Результаты 2-го раунда!'),
        'gText_ContestantsMonWon': ("{STR_VAR_1}'s {STR_VAR_2} won!", '{STR_VAR_1}: {STR_VAR_2} победил!'),
        'gText_CommunicationStandby': ('Communication standby…', 'Ожидание связи…'),
        'gText_Others': ('OTHERS', 'ДРУГОЕ'),
        'gText_Exit2': ('EXIT', 'ВЫХОД'),
        'gText_F700JoinedChat': ('{DYNAMIC 0} joined the chat!', '{DYNAMIC 0} вошел в чат!'),
        'gText_F700LeftChat': ('{DYNAMIC 0} left the chat.', '{DYNAMIC 0} вышел из чата.'),
        'gText_ExitingChat': ('Exiting the chat…', 'Выход из чата…'),
        'gText_LeaderLeftEndingChat': ('The LEADER, {DYNAMIC 0}, has\nleft, ending the chat.', 'ЛИДЕР, {DYNAMIC 0}, вышел.\nЧат завершен.'),
        'gText_SavingDontTurnOff_Chat': ("SAVING…\nDON'T TURN OFF THE POWER.", 'СОХРАНЕНИЕ…\nНЕ ВЫКЛЮЧАЙ ПИТАНИЕ.'),
        'gText_PlayerSavedGame_Chat': ('{DYNAMIC 0} saved the game.', '{DYNAMIC 0} сохранил игру.'),
        'gText_Ok': ('OK!', 'ОК!'),
        'gText_YaySmileEmoji': ('YAY{EMOJI_BIGSMILE}', 'УРА{EMOJI_BIGSMILE}'),
        'gText_NicknameHatchPrompt': ('Would you like to nickname the newly\nhatched {STR_VAR_1}?', 'Дать имя только что\nвылупившемуся {STR_VAR_1}?'),
        'gText_WaitForAllChooseBerry': ('Please wait while each member\nchooses a BERRY.', 'Подожди, пока все участники\nвыберут ЯГОДУ.'),
        'gText_PlayBerryCrushAgain': ('Want to play BERRY CRUSH again?', 'Сыграть в ДРОБИЛКУ ЯГОД снова?'),
        'gText_YouHaveNoBerries': ('You have no BERRIES.\nThe game will be canceled.', 'У тебя нет ЯГОД.\nИгра будет отменена.'),
        'gText_TimesUpNoGoodPowder': ("Time's up.\\pGood BERRY POWDER could not be\nmade…\\p", 'Время вышло.\\pХороший ЯГОДНЫЙ ПОРОШОК\nне получился…\\p'),
        'gText_CommunicationStandby2': ('Communication standby…', 'Ожидание связи…'),
        'gText_Var1Berry': ('{STR_VAR_1} BERRY', '{STR_VAR_1} ЯГОДА'),
        'gText_CoopRankings': ('Cooperative Rankings', 'Командный рейтинг'),
        'gText_SymbolsEarned': ('Symbols Earned', 'Полученные символы'),
        'gText_BattleRecord': ('Battle Record', 'Боевой рекорд'),
        'gText_BattlePoints': ('Battle Points', 'Боевые очки'),
        'gText_CheckFrontierMap': ('Check BATTLE FRONTIER MAP.', 'Смотреть КАРТУ РУБЕЖА.'),
        'gText_CheckTrainerCard': ('Check TRAINER CARD.', 'Смотреть КАРТУ ТРЕНЕРА.'),
        'gText_ViewRecordedBattle': ('View recorded battle.', 'Смотреть запись боя.'),
        'gText_PutAwayFrontierPass': ('Put away the FRONTIER PASS.', 'Убрать ПРОПУСК РУБЕЖА.'),
        'gText_CurrentBattlePoints': ('Your current Battle Points.', 'Текущие Боевые очки.'),
        'gText_CollectedSymbols': ('Your collected Symbols.', 'Собранные Символы.'),
        'gText_BattleTowerAbilitySymbol': ('Battle Tower - Ability Symbol', 'Башня - Символ Способности'),
        'gText_BattleDomeTacticsSymbol': ('Battle Dome - Tactics Symbol', 'Купол - Символ Тактики'),
        'gText_BattlePalaceSpiritsSymbol': ('Battle Palace - Spirits Symbol', 'Дворец - Символ Духа'),
        'gText_BattleArenaGutsSymbol': ('Battle Arena - Guts Symbol', 'Арена - Символ Смелости'),
        'gText_BattleFactoryKnowledgeSymbol': ('Battle Factory - Knowledge Symbol', 'Фабрика - Символ Знаний'),
        'gText_BattlePikeLuckSymbol': ('Battle Pike - Luck Symbol', 'Пика - Символ Удачи'),
        'gText_BattlePyramidBraveSymbol': ('Battle Pyramid - Brave Symbol', 'Пирамида - Символ Храбрости'),
        'gText_ThereIsNoBattleRecord': ('There is no Battle Record.', 'Записи боя нет.'),
        'gText_BattleTower3': ('BATTLE TOWER', 'БАШНЯ БИТВ'),
        'gText_BattleDome2': ('BATTLE DOME', 'БОЕВОЙ КУПОЛ'),
        'gText_BattlePalace2': ('BATTLE PALACE', 'БОЕВОЙ ДВОРЕЦ'),
        'gText_BattleArena2': ('BATTLE ARENA', 'БОЕВАЯ АРЕНА'),
        'gText_BattleFactory2': ('BATTLE FACTORY', 'БОЕВАЯ ФАБРИКА'),
        'gText_BattlePike2': ('BATTLE PIKE', 'БОЕВАЯ ПИКА'),
        'gText_BattlePyramid2': ('BATTLE PYRAMID', 'БОЕВАЯ ПИРАМИДА'),
        'gText_Powder': ('POWDER', 'ПОРОШОК'),
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
        if text==before: raise RuntimeError(f'{rel}: no changes made')
        path.write_text(text,encoding='utf-8')
        print(f'[QARRO_RU_FULL_SURFACE_V3_150] {rel}: translated {len(targets)} symbols')
    if total!=72: raise RuntimeError(f'expected 72 translations, got {total}')
    print('[QARRO_RU_FULL_SURFACE_V3_150] PASS: translated 72 audited RTC/Trainer Card/chat/Berry Crush/Frontier system/UI strings; exact placeholders/controls preserved; gameplay/Ash untouched')
    return 0

if __name__=='__main__': raise SystemExit(main())
