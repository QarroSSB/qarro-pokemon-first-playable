#!/usr/bin/env python3
"""Qarro v3.152: contract-safe rental/wireless/day-care/move-relearner UI localization.

Translates 62 confirmed English-only src/strings.c UI strings remaining after
the fully-green v3.151 checkpoint. Exact pinned source anchors and brace-token
contracts are required. Pokemon/Move/Ability proper names, gameplay, trainer
logic, rewards, flags, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations
import ast, re, sys
from pathlib import Path

TARGETS = {
    "src/strings.c": {
        'gText_Rent': ('RENT', 'АРЕНДА'),
        'gText_Summary': ('SUMMARY', 'СВОДКА'),
        'gText_Others2': ('OTHERS', 'ДРУГОЕ'),
        'gText_Deselect': ('DESELECT', 'СНЯТЬ'),
        'gText_Yes2': ('YES', 'ДА'),
        'gText_No2': ('NO', 'НЕТ'),
        'gText_CantSelectSamePkmn': ("Can't select same {PKMN}.", 'Нельзя выбрать того же {PKMN}.'),
        'gText_Swap': ('SWAP', 'ОБМЕН'),
        'gText_Summary2': ('SUMMARY', 'СВОДКА'),
        'gText_Rechoose': ('RECHOOSE', 'ВЫБРАТЬ СНОВА'),
        'gText_PkmnForSwap': ('{PKMN} FOR SWAP', '{PKMN} ДЛЯ ОБМЕНА'),
        'gText_Cancel3': ('CANCEL', 'ОТМЕНА'),
        'gText_Swap2': ('SWAP', 'ОБМЕН'),
        'gText_Accept': ('ACCEPT', 'ПРИНЯТЬ'),
        'gText_SamePkmnInPartyAlready': ('Same {PKMN} in party already.', 'Такой {PKMN} уже в команде.'),
        'gText_SavingPlayer': ('PLAYER', 'ИГРОК'),
        'gText_SavingBadges': ('BADGES', 'ЗНАЧКИ'),
        'gText_SavingTime': ('TIME', 'ВРЕМЯ'),
        'gText_WirelessCommStatus': ('Wireless Communication Status', 'Статус беспроводной связи'),
        'gText_F700Players': ('{DYNAMIC 0} players', '{DYNAMIC 0} игроков'),
        'gText_F701Players': ('{DYNAMIC 1} players', '{DYNAMIC 1} игроков'),
        'gText_F702Players': ('{DYNAMIC 2} players', '{DYNAMIC 2} игроков'),
        'gText_F703Players': ('{DYNAMIC 3} players', '{DYNAMIC 3} игроков'),
        'gText_Toss': ('TOSS', 'ВЫБРОСИТЬ'),
        'gText_CommunicationStandbyBButtonCancel': ('Communication standby…\nB Button: Cancel', 'Ожидание связи...\nB: Отмена'),
        'gText_PickOKExit': ('{DPAD_UPDOWN}PICK {A_BUTTON}OK {B_BUTTON}EXIT', '{DPAD_UPDOWN}ВЫБОР {A_BUTTON}ОК {B_BUTTON}ВЫХОД'),
        'gText_PickOKCancel': ('{DPAD_UPDOWN}PICK {A_BUTTON}OK {B_BUTTON}CANCEL', '{DPAD_UPDOWN}ВЫБОР {A_BUTTON}ОК {B_BUTTON}ОТМЕНА'),
        'gText_PlayersBattleResults': ("{PLAYER}'s BATTLE RESULTS", '{PLAYER}: РЕЗУЛЬТАТЫ БОЕВ'),
        'gText_TotalRecordWLD': ('TOTAL RECORD W:{STR_VAR_1} L:{STR_VAR_2} D:{STR_VAR_3}', 'ВСЕГО В:{STR_VAR_1} П:{STR_VAR_2} Н:{STR_VAR_3}'),
        'gText_WinLoseDraw': ('{CLEAR_TO 83}WIN{CLEAR_TO 128}LOSE{CLEAR_TO 176}DRAW', '{CLEAR_TO 83}ПОБЕД{CLEAR_TO 128}ПОРАЖ{CLEAR_TO 176}НИЧЬЯ'),
        'gDaycareText_GetAlongVeryWell': ('The two seem to get along\nvery well.', 'Эти двое отлично\nладят.'),
        'gDaycareText_GetAlong': ('The two seem to get along.', 'Эти двое ладят.'),
        'gDaycareText_DontLikeOther': ("The two don't seem to like\neach other much.", 'Похоже, эти двое\nне очень ладят.'),
        'gText_Exit4': ('EXIT', 'ВЫХОД'),
        'gText_TimeCleared': ('TIME CLEARED ', 'ВРЕМЯ ПРОХОЖДЕНИЯ '),
        'gText_XMinYDotZSec': ('{STR_VAR_1} min. {STR_VAR_2}.{STR_VAR_3} sec.', '{STR_VAR_1} мин. {STR_VAR_2}.{STR_VAR_3} сек.'),
        'gText_TrainerHill1F': ('1F', '1Э'),
        'gText_TeachWhichMoveToPkmn': ('Teach which {STR_VAR_3} to\n{STR_VAR_1}?', 'Какой {STR_VAR_3} обучить\n{STR_VAR_1}?'),
        'gText_MoveRelearnerTeachMoveConfirm': ('Teach {STR_VAR_2}?', 'Обучить {STR_VAR_2}?'),
        'gText_MoveRelearnerTeachMoveConfirmUseTm': ('Teach {STR_VAR_2}?\nThis will consume one {STR_VAR_3}.', 'Обучить {STR_VAR_2}?\nБудет потрачен {STR_VAR_3}.'),
        'gText_MoveRelearnerPkmnLearnedMove': ('{STR_VAR_1} learned\n{STR_VAR_2}!', '{STR_VAR_1} выучил\n{STR_VAR_2}!'),
        'gText_MoveRelearnerStopTryingToTeachMove': ('Stop trying to teach\n{STR_VAR_2}?', 'Не обучать\n{STR_VAR_2}?'),
        'gText_MoveRelearnerPkmnForgotMoveAndLearnedNew': ('{STR_VAR_1} forgot {STR_VAR_3}.\\pAnd…\\p{STR_VAR_1} learned {STR_VAR_2}.', '{STR_VAR_1} забыл {STR_VAR_3}.\\pИ...\\p{STR_VAR_1} выучил {STR_VAR_2}.'),
        'gText_MoveRelearnedPkmnDidNotLearnMove': ('{STR_VAR_1} did not learn the\nmove {STR_VAR_2}.', '{STR_VAR_1} не выучил\nприем {STR_VAR_2}.'),
        'gText_MoveRelearnerGiveUp': ('Give up trying to teach a new\nmove to {STR_VAR_1}?', 'Не учить {STR_VAR_1}\nновому приему?'),
        'gText_MoveRelearnerStop': ('Stop trying to learn new\nmoves for {STR_VAR_1}?', 'Больше не учить\n{STR_VAR_1} новым приемам?'),
        'gText_MoveRelearnerWhichMoveToForget': ('Which move should be\nforgotten?\\p', 'Какой прием\nзабыть?\\p'),
        'gText_MoveRelearnerBattleMoves': ('BATTLE MOVES', 'БОЕВЫЕ ПРИЕМЫ'),
        'gText_MoveRelearnerContestMovesTitle': ('CONTEST MOVES', 'КОНКУРСНЫЕ ПРИЕМЫ'),
        'gText_MoveRelearnerPP': ('PP/', 'ЗАПАС PP/'),
        'gText_MoveRelearnerPower': ('POWER/', 'СИЛА/'),
        'gText_MoveRelearnerAccuracy': ('ACCURACY/', 'ТОЧНОСТЬ/'),
        'gText_MoveRelearnerAppeal': ('APPEAL', 'ПРИВЛЕК.'),
        'gText_MoveRelearnerJam': ('JAM', 'ПОМЕХА'),
        'gText_FirstPlacePrize': ('The first-place winner gets\nthis {DYNAMIC 0}!', 'Победитель получает\n{DYNAMIC 0}!'),
        'gText_AwesomeWonF701F700': ("Awesome score! You've\nwon {DYNAMIC 1} {DYNAMIC 0}!", 'Отличный счет! Выиграно:\n{DYNAMIC 1} {DYNAMIC 0}!'),
        'gText_LinkContestResults': ("{PLAYER}'s Link Contest Results", 'LINK-КОНКУРС {PLAYER}: ИТОГИ'),
        'gText_1st': ('1st', '1-е'),
        'gText_2nd': ('2nd', '2-е'),
        'gText_3rd': ('3rd', '3-е'),
        'gText_4th': ('4th', '4-е'),
        'gText_Friend': ('Friend', 'ДРУГ'),
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
        print(f'[QARRO_RU_FULL_SURFACE_V3_152] {rel}: translated {len(targets)} symbols')
    if total!=62: raise RuntimeError(f'expected 62 translations, got {total}')
    print('[QARRO_RU_FULL_SURFACE_V3_152] PASS: translated 62 rental/wireless/day-care/move-relearner UI strings; exact placeholders/controls preserved; gameplay/Ash untouched')
    return 0

if __name__=='__main__': raise SystemExit(main())
