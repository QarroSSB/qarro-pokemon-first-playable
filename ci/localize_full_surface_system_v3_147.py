#!/usr/bin/env python3
"""Qarro v3.147: contract-safe full-surface system/UI localization batch.

Translates 41 confirmed English-only src/strings.c system/UI strings from the
post-v3.146 full-surface audit. Exact pinned source anchors and brace-token
contracts are required. Pokemon/Move/Ability proper names, gameplay, trainer
logic, rewards, flags, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations
import ast, re, sys
from pathlib import Path

TARGETS = {
    "src/strings.c": {
        "gText_HOFDexRating": (
            "Spotted POKéMON: {STR_VAR_1}!\nOwned POKéMON: {STR_VAR_2}!\\pPROF. BIRCH's POKéDEX rating!\\pPROF. BIRCH: Let's see…\\p",
            "Замечено ПОКЕМОНОВ: {STR_VAR_1}!\nПоймано ПОКЕМОНОВ: {STR_VAR_2}!\\pОценка ПОКЕДЕКСА ПРОФ. БЕРЧА!\\pПРОФ. БЕРЧ: Посмотрим...\\p",
        ),
        "gText_BirchInTrouble": (
            "PROF. BIRCH is in trouble!\nRelease a POKéMON and rescue him!",
            "ПРОФ. БЕРЧ в беде!\nВыпусти ПОКЕМОНА и спаси его!",
        ),
        "gText_DadsAdvice": (
            "DAD's advice…\n{PLAYER}, there's a time and place for\\leverything!{PAUSE_UNTIL_PRESS}",
            "Совет ПАПЫ...\n{PLAYER}, всему свое время и\\lместо!{PAUSE_UNTIL_PRESS}",
        ),
        "gText_LureEffectsLingered": (
            "But the effects of a Lure\nlingered from earlier.{PAUSE_UNTIL_PRESS}",
            "Но эффект ПРИМАНКИ\nеще действует.{PAUSE_UNTIL_PRESS}",
        ),
        "gText_EggWillTakeALongTime": (
            "It looks like this EGG will\ntake a long time to hatch.",
            "Похоже, это ЯЙЦО\nвылупится еще нескоро.",
        ),
        "gText_EggWillTakeSomeTime": (
            "What will hatch from this?\nIt will take some time.",
            "Кто из него вылупится?\nНужно еще немного времени.",
        ),
        "gText_OddEggFoundByCouple": (
            "An odd POKéMON EGG found\nby the DAY CARE couple.",
            "Необычное ЯЙЦО ПОКЕМОНА,\nнайденное парой из САДИКА.",
        ),
        "gText_PeculiarEggNicePlace": (
            "A peculiar POKéMON EGG\nobtained at the nice place.",
            "Необычное ЯЙЦО ПОКЕМОНА,\nполученное в хорошем месте.",
        ),
        "gText_NoMoreDecorations": (
            "No more decorations can be placed.\nThe most that can be placed are {STR_VAR_1}.",
            "Больше украшений не поставить.\nМаксимум: {STR_VAR_1}.",
        ),
        "gText_NoMoreDecorations2": (
            "No more decorations can be placed.\nThe most that can be placed are {STR_VAR_1}.",
            "Больше украшений не поставить.\nМаксимум: {STR_VAR_1}.",
        ),
        "gText_MustBePlacedOnDesk": (
            "This can't be placed here.\nIt must be on a DESK, etc.",
            "Здесь это не поставить.\nНужен СТОЛ или похожее место.",
        ),
        "gText_CantPlaceInRoom": (
            "This decoration can't be placed in\nyour own room.",
            "Это украшение нельзя поставить\nв своей комнате.",
        ),
        "gText_CantThrowAwayInUse": (
            "This decoration is in use.\nIt can't be thrown away.",
            "Это украшение используется.\nЕго нельзя выбросить.",
        ),
        "gText_MailToBagMessageErased": (
            "The MAIL was returned to the BAG\nwith its message erased.{PAUSE_UNTIL_PRESS}",
            "ПИСЬМО возвращено в СУМКУ,\nа текст стерт.{PAUSE_UNTIL_PRESS}",
        ),
        "gText_GamePlayCannotBeContinued": (
            "{COLOR RED}“Game play cannot be continued.\nReturning to the title screen…”",
            "{COLOR RED}Игра не может быть продолжена.\nВозврат к главному экрану...",
        ),
        "gText_CheckCompleted": (
            "Check completed.\nAttempting to save again.\nPlease wait.",
            "Проверка завершена.\nПовторное сохранение.\nПодождите.",
        ),
        "gText_SaveCompleteGameCannotContinue": (
            "Save completed.\n{COLOR RED}“Game play cannot be continued.\nReturning to the title screen.”",
            "Сохранение завершено.\n{COLOR RED}Игра не может быть продолжена.\nВозврат к главному экрану.",
        ),
        "gText_ClockHasBeenReset": (
            "The clock has been reset.\nData will be saved. Please wait.",
            "Часы сброшены.\nДанные будут сохранены. Подождите.",
        ),
        "gText_NoSaveFileCantSetTime": (
            "There is no save file, so the time\ncan't be set.",
            "Нет файла сохранения, поэтому\nвремя нельзя изменить.",
        ),
        "gText_InGameClockUsable": (
            "The in-game clock adjustment system\nis now useable.",
            "Настройка игровых часов\nтеперь доступна.",
        ),
        "gText_RegisteredTextChangedOKToSave": (
            "The registered text has been changed.\nIs it okay to save the game?",
            "Зарегистрированный текст изменен.\nСохранить игру?",
        ),
        "gText_AlreadySavedFile_Chat": (
            "There is already a saved file.\nIs it okay to overwrite it?",
            "Файл сохранения уже существует.\nПерезаписать его?",
        ),
        "gText_IfLeaderLeavesChatEnds": (
            "If the LEADER leaves, the chat\nwill end. Is that okay?",
            "Если ЛИДЕР уйдет, чат завершится.\nПродолжить?",
        ),
        "gText_ReadyPickBerry": (
            "Are you ready to BERRY-CRUSH?\nPlease pick a BERRY for use.\\p",
            "Готовы к ДРОБЛЕНИЮ ЯГОД?\nВыберите ЯГОДУ.\\p",
        ),
        "gText_EndedWithXUnitsPowder": (
            "{PAUSE_MUSIC}{PLAY_BGM MUS_LEVEL_UP}You ended up with {STR_VAR_1} units of\nsilky-smooth BERRY POWDER.{RESUME_MUSIC}\\pYour total amount of BERRY POWDER\nis {STR_VAR_2}.\\p",
            "{PAUSE_MUSIC}{PLAY_BGM MUS_LEVEL_UP}Получено {STR_VAR_1} ед.\nЯГОДНОЙ ПУДРЫ.{RESUME_MUSIC}\\pВсего ЯГОДНОЙ ПУДРЫ:\n{STR_VAR_2}.\\p",
        ),
        "gText_RecordingGameResults": (
            "Recording your game results in the\nsave file.\\lPlease wait.",
            "Сохраняем результаты игры\nв файл.\\lПодождите.",
        ),
        "gText_MemberDroppedOut": (
            "A member dropped out.\nThe game will be canceled.",
            "Участник вышел.\nИгра отменена.",
        ),
        "gText_BattleTowerDesc": (
            "KO opponents and aim for the top!\nYour ability will be tested.",
            "Побеждай и иди к вершине!\nПроверка твоих навыков.",
        ),
        "gText_BattleDomeDesc": (
            "Keep winning at the tournament!\nYour tactics will be tested.",
            "Побеждай в турнире снова и снова!\nПроверка твоей тактики.",
        ),
        "gText_BattlePalaceDesc": (
            "Watch your POKéMON battle!\nYour spirit will be tested.",
            "Наблюдай за боем ПОКЕМОНОВ!\nПроверка твоего духа.",
        ),
        "gText_BattleArenaDesc": (
            "Win battles with teamed-up POKéMON!\nYour guts will be tested.",
            "Побеждай командой ПОКЕМОНОВ!\nПроверка твоей стойкости.",
        ),
        "gText_BattleFactoryDesc": (
            "Aim for victory using rental POKéMON!\nYour knowledge will be tested.",
            "Побеждай арендными ПОКЕМОНАМИ!\nПроверка твоих знаний.",
        ),
        "gText_BattlePikeDesc": (
            "Select one of three paths to battle!\nYour luck will be tested.",
            "Выбери один из трех путей!\nПроверка твоей удачи.",
        ),
        "gText_BattlePyramidDesc": (
            "Aim for the top with exploration!\nYour bravery will be tested.",
            "Исследуй путь к вершине!\nПроверка твоей храбрости.",
        ),
        "gText_PressAToLoadEvent": (
            "Press the A Button to load event.\n… … B Button: Cancel",
            "Нажмите A для загрузки события.\n... ... B: Отмена",
        ),
        "gText_DontRemoveCableTurnOff": (
            "Don't remove the Game Link cable.\nDon't turn off the power.",
            "Не отключайте кабель Game Link.\nНе выключайте питание.",
        ),
        "gText_PokedexDiploma": (
            "PLAYER: {CLEAR 16}{COLOR RED}{SHADOW LIGHT_RED}{PLAYER}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}\n\nThis document certifies\nthat you have successfully\ncompleted your\n{STR_VAR_1} POKéDEX.\n\n{CLEAR_TO 66}{COLOR RED}{SHADOW LIGHT_RED}GAME FREAK",
            "ИГРОК: {CLEAR 16}{COLOR RED}{SHADOW LIGHT_RED}{PLAYER}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}\n\nДокумент подтверждает,\nчто вы успешно\nзавершили\n{STR_VAR_1} ПОКЕДЕКС.\n\n{CLEAR_TO 66}{COLOR RED}{SHADOW LIGHT_RED}GAME FREAK",
        ),
        "gText_DontHaveCardNewOneInput": (
            "You don't have a WONDER CARD,\nso a new CARD will be input.",
            "У вас нет ЧУДО-КАРТЫ,\nбудет добавлена новая.",
        ),
        "gText_DontHaveNewsNewOneInput": (
            "You don't have any WONDER NEWS,\nso new NEWS will be input.",
            "У вас нет ВЕСТОЧКИ,\nбудет добавлена новая.",
        ),
        "gDaycareText_PlayOther": (
            "The two prefer to play with other\nPOKéMON than each other.",
            "Они предпочитают играть с другими\nПОКЕМОНАМИ, а не друг с другом.",
        ),
        "gText_MoveRelearnerPkmnTryingToLearnMove": (
            "{STR_VAR_1} is trying to learn\n{STR_VAR_2}.\\pBut {STR_VAR_1} can't learn more\nthan four moves.\\pDelete an older move to make\nroom for {STR_VAR_2}?",
            "{STR_VAR_1} пытается выучить\n{STR_VAR_2}.\\pНо {STR_VAR_1} знает уже\nчетыре приема.\\pЗабыть старый прием ради\n{STR_VAR_2}?",
        ),
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
        print(f'usage: {Path(sys.argv[0]).name} <upstream-root>',file=sys.stderr);return 2
    root=Path(sys.argv[1]).resolve(); total=0
    for rel,targets in TARGETS.items():
        path=root/rel
        if not path.is_file(): raise RuntimeError(f'missing target file: {path}')
        text=path.read_text(encoding='utf-8'); before=text
        for symbol,(expected,replacement) in targets.items():
            text,n=patch_symbol(text,symbol,expected,replacement); total+=n
        if text==before: raise RuntimeError(f'{rel}: no changes made')
        path.write_text(text,encoding='utf-8')
        print(f'[QARRO_RU_FULL_SURFACE_V3_147] {rel}: translated {len(targets)} symbols')
    if total!=41: raise RuntimeError(f'expected 41 translations, got {total}')
    print('[QARRO_RU_FULL_SURFACE_V3_147] PASS: translated 41 audited system/UI strings; exact placeholders/controls preserved; gameplay/Ash untouched')
    return 0

if __name__=='__main__': raise SystemExit(main())
