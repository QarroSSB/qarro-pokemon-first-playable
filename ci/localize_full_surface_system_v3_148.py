#!/usr/bin/env python3
"""Qarro v3.148: contract-safe Bag/Shop/Egg/Decoration system UI localization.

Translates 81 confirmed English-only src/strings.c system/UI strings from the
post-v3.147 audit. Exact pinned source anchors and brace-token contracts are
required. Pokemon/Move/Ability proper names, gameplay, trainer logic, rewards,
flags, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations
import ast, re, sys
from pathlib import Path

TARGETS = {
    "src/strings.c": {
        'gText_CantWriteMail': ("You can't write\nMAIL here.", 'Здесь нельзя писать\nПИСЬМО.'),
        'gText_MoveVar1Where': ('Move the\n{STR_VAR_1}\nwhere?', 'Куда переместить\n{STR_VAR_1}?'),
        'gText_Var1CantBeHeld': ("The {STR_VAR_1} can't be held.", '{STR_VAR_1} нельзя держать.'),
        'gText_TossHowManyVar1s': ('Toss out how many\n{STR_VAR_1}?', 'Сколько {STR_VAR_1}\nвыбросить?'),
        'gText_ThrewAwayVar2Var1s': ('Threw away {STR_VAR_2}\n{STR_VAR_1}.', 'Выброшено: {STR_VAR_2}\n{STR_VAR_1}.'),
        'gText_ConfirmTossItems': ('Is it okay to\nthrow away {STR_VAR_2}\n{STR_VAR_1}?', 'Выбросить {STR_VAR_2}\n{STR_VAR_1}?'),
        'gText_ReturnToVar1': ('Return to\n{STR_VAR_1}.', 'Вернуться к\n{STR_VAR_1}.'),
        'gText_Var1CertainlyHowMany2': ('{STR_VAR_1}? Certainly.\nHow many would you like?', '{STR_VAR_1}? Конечно.\nСколько нужно?'),
        'gText_Var1IsItThatllBeVar2': ("{STR_VAR_1}, is it?\nThat'll be ¥{STR_VAR_2}. Do you want it?", '{STR_VAR_1}, верно?\nЦена ¥{STR_VAR_2}. Купить?'),
        'gText_YouWantedVar1ThatllBeVar2': ("You wanted {STR_VAR_1}?\nThat'll be ¥{STR_VAR_2}. Will that be okay?", 'Нужен {STR_VAR_1}?\nЦена ¥{STR_VAR_2}. Купить?'),
        'gText_ThankYouIllSendItHome': ("Thank you!\nI'll send it to your home PC.", 'Спасибо!\nОтправлю на домашний ПК.'),
        'gText_ThanksIllSendItHome': ("Thanks!\nI'll send it to your PC at home.", 'Спасибо!\nОтправлю на ПК дома.'),
        'gText_SpaceForVar1Full': ('The space for {STR_VAR_1} is full.{PAUSE_UNTIL_PRESS}', 'Нет места для {STR_VAR_1}.{PAUSE_UNTIL_PRESS}'),
        'gText_CanIHelpWithAnythingElse': ('Can I help you with anything else?', 'Что-нибудь еще?'),
        'gText_ThrowInPremierBall': ("I'll throw in a PREMIER BALL, too.{PAUSE_UNTIL_PRESS}", 'Бонус - ПРЕМЬЕР-БОЛЛ.{PAUSE_UNTIL_PRESS}'),
        'gText_ThrowInPremierBalls': ("I'll throw in {STR_VAR_1} PREMIER BALLS, too.{PAUSE_UNTIL_PRESS}", 'Бонус - ПРЕМЬЕР-БОЛЛ x{STR_VAR_1}.{PAUSE_UNTIL_PRESS}'),
        'gText_CantBuyKeyItem': ("{STR_VAR_2}? Oh, no.\nI can't buy that.{PAUSE_UNTIL_PRESS}", '{STR_VAR_2}? Нет.\nЭто я не куплю.{PAUSE_UNTIL_PRESS}'),
        'gText_HowManyToSell': ('{STR_VAR_2}?\nHow many would you like to sell?', '{STR_VAR_2}?\nСколько продать?'),
        'gText_ICanPayVar1': ('I can pay ¥{STR_VAR_1}.\nWould that be okay?', 'Могу заплатить ¥{STR_VAR_1}.\nСогласен?'),
        'gText_TurnedOverVar1ForVar2': ('Turned over the {STR_VAR_2}\nand received ¥{STR_VAR_1}.', 'Отдан {STR_VAR_2}.\nПолучено ¥{STR_VAR_1}.'),
        'gText_NoMoreThanVar1Pkmn': ('No more than {STR_VAR_1} POKéMON\nmay enter.{PAUSE_UNTIL_PRESS}', 'Можно взять не больше {STR_VAR_1}\nПОКЕМОНОВ.{PAUSE_UNTIL_PRESS}'),
        'gText_PkmnLearnedMove4': ('{STR_VAR_1} learned\n{STR_VAR_2}!{PAUSE_UNTIL_PRESS}', '{STR_VAR_1} выучил\n{STR_VAR_2}!{PAUSE_UNTIL_PRESS}'),
        'gText_PkmnFrostbiteHealed': ("{STR_VAR_1}'s frostbite was healed.{PAUSE_UNTIL_PRESS}", 'Обморожение {STR_VAR_1}\nвылечено.{PAUSE_UNTIL_PRESS}'),
        'gText_PkmnRegainhedHealth': ('{STR_VAR_1} regained health.{PAUSE_UNTIL_PRESS}', '{STR_VAR_1} восстановил здоровье.{PAUSE_UNTIL_PRESS}'),
        'gText_PkmnGainedExp': ('{STR_VAR_1} gained {STR_VAR_2} Exp. Points!{PAUSE_UNTIL_PRESS}', '{STR_VAR_1} получает {STR_VAR_2} очк. опыта!{PAUSE_UNTIL_PRESS}'),
        'gText_PkmnGainedExpAndElevatedToLvVar3': ('{STR_VAR_1} gained {STR_VAR_2} Exp. Points\nand was elevated to Lv. {STR_VAR_3}!', '{STR_VAR_1} получает {STR_VAR_2} очк. опыта\nи достигает ур. {STR_VAR_3}!'),
        'gText_PkmnFriendlyBaseVar2Fell': ('{STR_VAR_1} turned friendly.\nThe base {STR_VAR_2} fell!{PAUSE_UNTIL_PRESS}', '{STR_VAR_1} стал дружелюбнее.\nБазовый {STR_VAR_2} снизился!{PAUSE_UNTIL_PRESS}'),
        'gText_PkmnAdoresBaseVar2Fell': ('{STR_VAR_1} adores you!\nThe base {STR_VAR_2} fell!{PAUSE_UNTIL_PRESS}', '{STR_VAR_1} обожает тебя!\nБазовый {STR_VAR_2} снизился!{PAUSE_UNTIL_PRESS}'),
        'gText_PkmnFriendlyBaseVar2CantFall': ("{STR_VAR_1} turned friendly.\nThe base {STR_VAR_2} can't fall!{PAUSE_UNTIL_PRESS}", '{STR_VAR_1} стал дружелюбнее.\nБазовый {STR_VAR_2} ниже не станет!{PAUSE_UNTIL_PRESS}'),
        'gText_PkmnTransformed': ('{STR_VAR_1} transformed!{PAUSE_UNTIL_PRESS}', '{STR_VAR_1} превратился!{PAUSE_UNTIL_PRESS}'),
        'gText_ThrowAwayItem': ('Throw away this\n{STR_VAR_1}?', 'Выбросить\n{STR_VAR_1}?'),
        'gText_ItemThrownAway': ('The {STR_VAR_1}\nwas thrown away.{PAUSE_UNTIL_PRESS}', '{STR_VAR_1}\nвыброшен.{PAUSE_UNTIL_PRESS}'),
        'gText_TeachWhichPokemon2': ('Teach which POKéMON?', 'Какого ПОКЕМОНА обучить?'),
        'gText_BoostPP': ('Boost PP of which move?', 'Для какого приема повысить PP?'),
        'gText_PokemonAreNeeded': ('{STR_VAR_1} POKéMON are needed.', 'Нужно ПОКЕМОНОВ: {STR_VAR_1}.'),
        'gText_SendWhichMonToPC': ('Send which POKéMON to the PC?', 'Какого ПОКЕМОНА отправить на ПК?'),
        'gText_MoveItemWhere': ('Move item to where?', 'Куда переместить вещь?'),
        'gText_XsYAnd': ("{STR_VAR_1}'s {STR_VAR_2} and\n", '{STR_VAR_1}: {STR_VAR_2} и\n'),
        'gText_XsYWereSwapped': ("{STR_VAR_1}'s {STR_VAR_2} were swapped!{PAUSE_UNTIL_PRESS}", '{STR_VAR_1}: {STR_VAR_2} обменены!{PAUSE_UNTIL_PRESS}'),
        'gText_AlreadyHoldingOne': ('{STR_VAR_1} is already holding\none {STR_VAR_2}.', '{STR_VAR_1} уже держит\n{STR_VAR_2}.'),
        'gText_WhichAppliance': ('Order which\nappliance?', 'Какой прибор\nзаказать?'),
        'gText_EggWillHatchSoon': ('It moves occasionally.\nIt should hatch soon.', 'Иногда оно шевелится.\nСкоро должно вылупиться.'),
        'gText_EggAboutToHatch': ("It's making sounds.\nIt's about to hatch!", 'Из него доносятся звуки.\nВот-вот вылупится!'),
        'gText_HMMovesCantBeForgotten2': ("HM moves can't be\nforgotten now.", 'Приемы HM сейчас\nнельзя забыть.'),
        'gText_PeculiarEggTrade': ('A peculiar POKéMON EGG\nobtained in a trade.', 'Необычное ЯЙЦО ПОКЕМОНА,\nполученное при обмене.'),
        'gText_EggFromHotSprings': ('A POKéMON EGG obtained\nat the hot springs.', 'ЯЙЦО ПОКЕМОНА, полученное\nу горячих источников.'),
        'gText_EggFromTraveler': ('An odd POKéMON EGG\nobtained from a traveler.', 'Необычное ЯЙЦО ПОКЕМОНА,\nполученное от путешественника.'),
        'gText_OkayToDeleteFromRegistry': ('Is it okay to delete {STR_VAR_1}\nfrom the REGISTRY?', 'Удалить {STR_VAR_1}\nиз РЕЕСТРА?'),
        'gText_RegisteredDataDeleted': ('The registered data was deleted.{PAUSE_UNTIL_PRESS}', 'Данные реестра удалены.{PAUSE_UNTIL_PRESS}'),
        'gText_NoRegistry': ('There is no REGISTRY.{PAUSE_UNTIL_PRESS}', 'РЕЕСТР пуст.{PAUSE_UNTIL_PRESS}'),
        'gText_DelRegist': ('DEL REGIST.', 'УДАЛ. ЗАП.'),
        'gText_Decorate': ('DECORATE', 'УКРАСИТЬ'),
        'gText_PutAway': ('PUT AWAY', 'УБРАТЬ'),
        'gText_Toss2': ('TOSS', 'ВЫБРОСИТЬ'),
        'gText_PutOutSelectedDecorItem': ('Put out the selected decoration item.', 'Разместить выбранное украшение.'),
        'gText_StoreChosenDecorInPC': ('Store the chosen decoration in the PC.', 'Убрать выбранное украшение на ПК.'),
        'gText_ThrowAwayUnwantedDecors': ('Throw away unwanted decorations.', 'Выбросить ненужные украшения.'),
        'gText_NoDecorations': ('There are no decorations.{PAUSE_UNTIL_PRESS}', 'Украшений нет.{PAUSE_UNTIL_PRESS}'),
        'gText_Desk': ('DESK', 'СТОЛ'),
        'gText_Chair': ('CHAIR', 'СТУЛ'),
        'gText_Plant': ('PLANT', 'РАСТЕНИЕ'),
        'gText_Ornament': ('ORNAMENT', 'ДЕКОР'),
        'gText_Mat': ('MAT', 'КОВРИК'),
        'gText_Poster': ('POSTER', 'ПОСТЕР'),
        'gText_Doll': ('DOLL', 'КУКЛА'),
        'gText_Cushion': ('CUSHION', 'ПОДУШКА'),
        'gText_Gold': ('GOLD', 'ЗОЛОТО'),
        'gText_Silver': ('SILVER', 'СЕРЕБРО'),
        'gText_PlaceItHere': ('Place it here?', 'Поставить здесь?'),
        'gText_CantBePlacedHere': ("It can't be placed here.", 'Здесь это не поставить.'),
        'gText_CancelDecorating': ('Cancel decorating?', 'Прекратить украшение?'),
        'gText_InUseAlready': ('This is in use already.', 'Это уже используется.'),
        'gText_DecorationWillBeDiscarded': ('This {STR_VAR_1} will be discarded.\nIs that okay?', 'Выбросить {STR_VAR_1}?\nПродолжить?'),
        'gText_DecorationThrownAway': ('The decoration item was thrown away.', 'Украшение выброшено.'),
        'gText_StopPuttingAwayDecorations': ('Stop putting away decorations?', 'Перестать убирать украшения?'),
        'gText_NoDecorationHere': ('There is no decoration item here.', 'Здесь нет украшения.'),
        'gText_ReturnDecorationToPC': ('Return this decoration to the PC?', 'Вернуть украшение на ПК?'),
        'gText_DecorationReturnedToPC': ('The decoration was returned to the PC.', 'Украшение возвращено на ПК.'),
        'gText_NoDecorationsInUse': ('There are no decorations in use.{PAUSE_UNTIL_PRESS}', 'Используемых украшений нет.{PAUSE_UNTIL_PRESS}'),
        'gText_NoMailHere': ("There's no MAIL here.{PAUSE_UNTIL_PRESS}", 'Здесь нет ПИСЕМ.{PAUSE_UNTIL_PRESS}'),
        'gText_WhatToDoWithVar1sMail': ("What would you like to do with\n{STR_VAR_1}'s MAIL?", 'Что сделать с ПИСЬМОМ\nот {STR_VAR_1}?'),
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
    # Preserve FireRed text escapes (e.g. \p / \l); only encode real newlines and C quotes.
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
        print(f'[QARRO_RU_FULL_SURFACE_V3_148] {rel}: translated {len(targets)} symbols')
    if total!=81: raise RuntimeError(f'expected 81 translations, got {total}')
    print('[QARRO_RU_FULL_SURFACE_V3_148] PASS: translated 81 audited Bag/Shop/Egg/Decoration system/UI strings; exact placeholders/controls preserved; gameplay/Ash untouched')
    return 0

if __name__=='__main__': raise SystemExit(main())
