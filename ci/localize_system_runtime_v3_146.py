#!/usr/bin/env python3
"""Qarro v3.146: manual contract-safe cleanup of donor-incompatible system/battle strings.

These entries were intentionally excluded from v3.145 because the legacy donor
changed placeholders or controls. This pass translates the current Expansion
strings directly and requires every brace token to remain byte-for-byte in the
same order. It runs before the final accented-e normalizer, so pinned source
anchors use FireRed's literal POKé spelling. Gameplay, trainer logic,
Pokemon/Move/Ability proper-name policy, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations
import ast, re, sys
from pathlib import Path

TARGETS = {
    "src/strings.c": {
        "gText_SaveFailedCheckingBackup": (
            'Save failed. Checking the backup\nmemory… Please wait.\n{COLOR RED}“Time required: about 1 minute”',
            'Сохранение не удалось. Проверка\nрезервной памяти… Подождите.\n{COLOR RED}Время: около 1 минуты',
        ),
        "gText_BagFullCouldNotRemoveItem": (
            "The BAG is full. The POKéMON's\nitem could not be removed.{PAUSE_UNTIL_PRESS}",
            'СУМКА заполнена. Вещь\nпокемона не забрать.{PAUSE_UNTIL_PRESS}',
        ),
        "gText_SaveCompletePressA": (
            'Save completed.\n{COLOR RED}“Please press the A Button.”',
            'Сохранение завершено.\n{COLOR RED}Нажмите кнопку A.',
        ),
        "gText_PkmnCantLearnMove": (
            "{STR_VAR_1} and {STR_VAR_2}\nare not compatible.\\p{STR_VAR_2} can't be\nlearned.{PAUSE_UNTIL_PRESS}",
            '{STR_VAR_1} и {STR_VAR_2}\nнесовместимы.\\p{STR_VAR_2} нельзя\nвыучить.{PAUSE_UNTIL_PRESS}',
        ),
        "gText_EscapeFromHere": (
            'Want to escape from here and return\nto {STR_VAR_1}?',
            'Выбраться отсюда и вернуться\nв {STR_VAR_1}?',
        ),
        "gText_WonderNewsSentTo": (
            'Your WONDER NEWS item has been\nsent to {STR_VAR_1}.',
            'ВЕСТОЧКА отправлена\nигроку {STR_VAR_1}.',
        ),
        "gText_Var1AndYouWantedVar2": (
            '{STR_VAR_1}? And you wanted {STR_VAR_2}?\nThat will be ¥{STR_VAR_3}.',
            '{STR_VAR_1}? И нужен {STR_VAR_2}?\nЦена: ¥{STR_VAR_3}.',
        ),
        "gText_WonderCardSentTo": (
            'Your WONDER CARD has been sent\nto {STR_VAR_1}.',
            'ЧУДО-КАРТА отправлена\nигроку {STR_VAR_1}.',
        ),
        "gText_StampSentTo": (
            'A STAMP has been sent to {STR_VAR_1}.',
            'ПЕЧАТЬ отправлена игроку {STR_VAR_1}.',
        ),
        "gText_GiftSentTo": (
            'A GIFT has been sent to {STR_VAR_1}.',
            'ПОДАРОК отправлен игроку {STR_VAR_1}.',
        ),
        "gText_ReceivedItemFromPkmn": (
            'Received the {STR_VAR_2}\nfrom {STR_VAR_1}.{PAUSE_UNTIL_PRESS}',
            'Получен {STR_VAR_2}\nот {STR_VAR_1}.{PAUSE_UNTIL_PRESS}',
        ),
        "gText_DoWhatWithPokemon": (
            'Do what with this {PKMN}?',
            'Что сделать с этим {PKMN}?',
        ),
        "gText_Var1sTrainerCard": (
            "{STR_VAR_1}'s TRAINER CARD",
            'КАРТОЧКА ТРЕНЕРА: {STR_VAR_1}',
        ),
    },
    "src/battle_message.c": {
        "gText_CongratsPkmnEvolved": (
            'Congratulations! Your {STR_VAR_1}\nevolved into {STR_VAR_2}!{WAIT_SE}\\p',
            'Поздравляем! {STR_VAR_1}\nэволюционирует в {STR_VAR_2}!{WAIT_SE}\\p',
        ),
        "sText_PlayerBattledToDrawVsTwo": (
            'You battled to a draw against {B_LINK_OPPONENT1_NAME} and {B_LINK_OPPONENT2_NAME}!',
            'Ничья с {B_LINK_OPPONENT1_NAME}\nи {B_LINK_OPPONENT2_NAME}!',
        ),
        "sText_PlayerBattledToDrawLinkTrainer": (
            'You battled to a draw against {B_LINK_OPPONENT1_NAME}!',
            'Ничья с {B_LINK_OPPONENT1_NAME}!',
        ),
        "sText_PlayerBattledToDrawTrainer1": (
            'You battled to a draw against {B_TRAINER1_NAME_WITH_CLASS}!',
            'Ничья с {B_TRAINER1_NAME_WITH_CLASS}!',
        ),
        "sText_Trainer1WantsToBattle": (
            'You are challenged by {B_TRAINER1_NAME_WITH_CLASS}!\\p',
            '{B_TRAINER1_NAME_WITH_CLASS}\nвызывает тебя на бой!\\p',
        ),
        "gText_PkmnStoppedEvolving": (
            'Huh? {STR_VAR_1}\nstopped evolving!\\p',
            'Что? {STR_VAR_1}\nпрекращает эволюцию!\\p',
        ),
        "gText_PkmnIsEvolving": (
            'What?\n{STR_VAR_1} is evolving!',
            'Что?\n{STR_VAR_1} эволюционирует!',
        ),
        "sText_Trainer1SentOutTwoPkmn": (
            '{B_TRAINER1_NAME_WITH_CLASS} sent out {B_OPPONENT_MON1_NAME} and {B_OPPONENT_MON2_NAME}!',
            '{B_TRAINER1_NAME_WITH_CLASS} выбирает\n{B_OPPONENT_MON1_NAME} и {B_OPPONENT_MON2_NAME}!',
        ),
        "sText_PlayerLostAgainstTrainer1": (
            'You lost to {B_TRAINER1_NAME_WITH_CLASS}!',
            '{B_TRAINER1_NAME_WITH_CLASS}\nпобеждает!',
        ),
        "gText_SafariBalls": (
            'Safari Balls',
            'САФАРИ-БОЛЛЫ',
        ),
        "sText_Trainer1SentOutPkmn": (
            '{B_TRAINER1_NAME_WITH_CLASS} sent out {B_OPPONENT_MON1_NAME}!',
            '{B_TRAINER1_NAME_WITH_CLASS} выбирает\n{B_OPPONENT_MON1_NAME}!',
        ),
        "sText_Trainer1SentOutPkmn2": (
            '{B_TRAINER1_NAME_WITH_CLASS} sent out {B_BUFF1}!',
            '{B_TRAINER1_NAME_WITH_CLASS} выбирает\n{B_BUFF1}!',
        ),
        "sText_LinkTrainerSentOutPkmn": (
            '{B_LINK_OPPONENT1_NAME} sent out {B_BUFF1}!',
            '{B_LINK_OPPONENT1_NAME} выбирает\n{B_BUFF1}!',
        ),
        "sText_LinkTrainerSentOutPkmn2": (
            '{B_LINK_OPPONENT1_NAME} sent out {B_LINK_OPPONENT_MON2_NAME}!',
            '{B_LINK_OPPONENT1_NAME} выбирает\n{B_LINK_OPPONENT_MON2_NAME}!',
        ),
        "sText_Trainer1WithdrewPkmn": (
            '{B_TRAINER1_NAME_WITH_CLASS} withdrew {B_BUFF1}!',
            '{B_TRAINER1_NAME_WITH_CLASS}\nотзывает {B_BUFF1}!',
        ),
        "sText_LinkTrainer2WithdrewPkmn": (
            '{B_LINK_OPPONENT2_NAME} withdrew {B_BUFF1}!',
            '{B_LINK_OPPONENT2_NAME} отзывает\n{B_BUFF1}!',
        ),
        "sText_AttackerUsedX": (
            '{B_ATK_NAME_WITH_PREFIX} used {B_BUFF3}!',
            '{B_ATK_NAME_WITH_PREFIX} использует\n{B_BUFF3}!',
        ),
        "sText_Trainer1Fled": (
            '{PLAY_SE SE_FLEE}{B_TRAINER1_NAME_WITH_CLASS} fled!',
            '{PLAY_SE SE_FLEE}{B_TRAINER1_NAME_WITH_CLASS}\nубегает!',
        ),
        "gText_Loss": (
            '{BACKGROUND TRANSPARENT}{ACCENT TRANSPARENT}Loss',
            '{BACKGROUND TRANSPARENT}{ACCENT TRANSPARENT}ПОР.',
        ),
        "gText_Draw": (
            '{BACKGROUND TRANSPARENT}{ACCENT TRANSPARENT}Draw',
            '{BACKGROUND TRANSPARENT}{ACCENT TRANSPARENT}НИЧ.',
        ),
        "gText_Win": (
            '{BACKGROUND TRANSPARENT}{ACCENT TRANSPARENT}Win',
            '{BACKGROUND TRANSPARENT}{ACCENT TRANSPARENT}ПОБ.',
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
    return '"' + text.replace('"','\\"') + '"'

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
        print(f'[QARRO_RU_SYSTEM_V3_146] {rel}: translated {len(targets)} symbols')
    if total!=34: raise RuntimeError(f'expected 34 translations, got {total}')
    print('[QARRO_RU_SYSTEM_V3_146] PASS: translated 34 donor-incompatible current strings; exact placeholders/controls preserved; Ash untouched')
    return 0

if __name__=='__main__': raise SystemExit(main())
