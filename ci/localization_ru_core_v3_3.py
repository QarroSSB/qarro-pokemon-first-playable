#!/usr/bin/env python3
"""Qarro v3.3/v3.4 safe Russian localization layer.

Translate high-visibility menus/system UI plus the custom early-route dialogue
introduced by the Qarro v3.1 content pass. English Pokemon, Move and Ability
proper names are deliberately preserved.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def patch_symbol(text: str, symbol: str, value: str, *, required: bool = True) -> tuple[str, bool]:
    rx = re.compile(rf'(?m)^([^\n]*\b{re.escape(symbol)}\b[^\n]*?\s*=\s*_\(")(.*?)("\);[^\n]*)$')
    matches = list(rx.finditer(text))
    if not matches:
        if required:
            raise RuntimeError(f"missing localization anchor: {symbol}")
        return text, False
    if len(matches) != 1:
        raise RuntimeError(f"{symbol}: expected one localization anchor, got {len(matches)}")
    current = matches[0].group(2)
    if current == value:
        return text, False
    text = rx.sub(lambda m: f"{m.group(1)}{value}{m.group(3)}", text, count=1)
    print(f"[ru-core] {symbol}: {current!r} -> {value!r}")
    return text, True


def patch_file(path: Path, mapping: dict[str, str]) -> int:
    if not path.exists():
        raise RuntimeError(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    changed = 0
    for symbol, value in mapping.items():
        text, did = patch_symbol(text, symbol, value)
        changed += int(did)
    path.write_text(text, encoding="utf-8")
    return changed


def patch_option_menu(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    mapping = {
        "gText_Option": "НАСТРОЙКИ",
        "gText_TextSpeedSlow": "{COLOR GREEN}{SHADOW LIGHT_GREEN}МЕДЛ.",
        "gText_TextSpeedMid": "{COLOR GREEN}{SHADOW LIGHT_GREEN}СРЕД.",
        "gText_TextSpeedFast": "{COLOR GREEN}{SHADOW LIGHT_GREEN}БЫСТР.",
        "gText_BattleSceneOn": "{COLOR GREEN}{SHADOW LIGHT_GREEN}ВКЛ",
        "gText_BattleSceneOff": "{COLOR GREEN}{SHADOW LIGHT_GREEN}ВЫКЛ",
        "gText_BattleStyleShift": "{COLOR GREEN}{SHADOW LIGHT_GREEN}СМЕНА",
        "gText_BattleStyleSet": "{COLOR GREEN}{SHADOW LIGHT_GREEN}ФИКС.",
        "gText_SoundMono": "{COLOR GREEN}{SHADOW LIGHT_GREEN}МОНО",
        "gText_SoundStereo": "{COLOR GREEN}{SHADOW LIGHT_GREEN}СТЕРЕО",
        "gText_FrameType": "{COLOR GREEN}{SHADOW LIGHT_GREEN}ТИП",
        "gText_ButtonTypeNormal": "{COLOR GREEN}{SHADOW LIGHT_GREEN}ОБЫЧН.",
    }
    changed = 0
    for symbol, value in mapping.items():
        text, did = patch_symbol(text, symbol, value)
        changed += int(did)

    exact = {
        'COMPOUND_STRING("TEXT SPEED")': 'COMPOUND_STRING("СКОР. ТЕКСТА")',
        'COMPOUND_STRING("BATTLE SCENE")': 'COMPOUND_STRING("АНИМ. БОЯ")',
        'COMPOUND_STRING("BATTLE STYLE")': 'COMPOUND_STRING("СТИЛЬ БОЯ")',
        'COMPOUND_STRING("SOUND")': 'COMPOUND_STRING("ЗВУК")',
        'COMPOUND_STRING("BUTTON MODE")': 'COMPOUND_STRING("КНОПКИ")',
        'COMPOUND_STRING("FRAME")': 'COMPOUND_STRING("РАМКА")',
        'COMPOUND_STRING("CANCEL")': 'COMPOUND_STRING("НАЗАД")',
    }
    for old, new in exact.items():
        if new in text:
            continue
        if text.count(old) != 1:
            raise RuntimeError(f"option anchor count for {old!r}: {text.count(old)}")
        text = text.replace(old, new, 1)
        changed += 1
        print(f"[ru-core] option: {old} -> {new}")
    path.write_text(text, encoding="utf-8")
    return changed


def patch_exact_strings(path: Path, mapping: dict[str, str]) -> int:
    if not path.exists():
        raise RuntimeError(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    changed = 0
    for old, new in mapping.items():
        if new in text:
            continue
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"{path}: expected one exact text anchor {old!r}, got {count}")
        text = text.replace(old, new, 1)
        changed += 1
        print(f"[ru-route] {path.name}: {old!r} -> {new!r}")
    path.write_text(text, encoding="utf-8")
    return changed


def patch_custom_route_dialogue(root: Path) -> int:
    changed = 0
    changed += patch_exact_strings(root / "data/maps/Route1_Frlg/scripts.inc", {
        '    .string "KANTO isn\'t the whole world!\\nLet\'s battle!$"': '    .string "КАНТО - не весь мир!\\nДавай сразимся!$"',
        '    .string "Okay, your team is stronger!$"': '    .string "Ладно, твоя команда сильнее!$"',
        '    .string "You\'ll meet POKéMON from many regions.$"': '    .string "Ты встретишь ПОКЕМОНОВ из разных регионов.$"',
        '    .string "My POKéMON came from far away.\\nReady?$"': '    .string "Мои ПОКЕМОНЫ прибыли издалека.\\nГотов?$"',
        '    .string "That was a good battle!$"': '    .string "Это был хороший бой!$"',
        '    .string "Different regions mean different tactics.$"': '    .string "Разные регионы - разные тактики.$"',
    })
    changed += patch_exact_strings(root / "data/maps/Route2_Frlg/scripts.inc", {
        '    .string "Electric POKéMON aren\'t just PIKACHU!$"': '    .string "Электрические ПОКЕМОНЫ - не только PIKACHU!$"',
        '    .string "You grounded my plan!$"': '    .string "Ты сорвал мой план!$"',
        '    .string "I\'ll train with POKéMON from every region.$"': '    .string "Я буду тренироваться с ПОКЕМОНАМИ всех регионов.$"',
        '    .string "Bugs evolved in every region.\\nTake a look!$"': '    .string "Насекомые есть в каждом регионе.\\nСмотри!$"',
        '    .string "My bugs need more training!$"': '    .string "Моим насекомым нужно больше тренировок!$"',
        '    .string "Forests hide many different species.$"': '    .string "В лесах скрывается множество разных видов.$"',
    })
    changed += patch_exact_strings(root / "data/maps/Route4_Frlg/scripts.inc", {
        '    .string "I trained by MT. MOON.\\nLet\'s see what you learned!$"': '    .string "Я тренировался у MT. MOON.\\nПокажи, чему научился!$"',
        '    .string "You made it through!$"': '    .string "Ты справился!$"',
        '    .string "Your PC will need room for many species.$"': '    .string "В твоём ПК понадобится место для многих видов.$"',
    })
    return changed


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    main_menu = {
        "gText_SaveFileCorrupted": "Файл сохранения повреждён.\\nБудет загружена предыдущая копия.",
        "gText_SaveFileErased": "Файл сохранения удалён\\nиз-за повреждения данных.",
        "gText_BatteryRunDry": "Внутренняя батарея разряжена.\\nИграть можно.\\pСобытия, зависящие от часов,\\nработать не будут.",
        "gText_MainMenuNewGame": "НОВАЯ ИГРА",
        "gText_MainMenuContinue": "ПРОДОЛЖИТЬ",
        "gText_MainMenuOption": "НАСТРОЙКИ",
        "gText_MainMenuMysteryGift": "ТАЙНЫЙ ПОДАРОК",
        "gText_MainMenuMysteryGift2": "ТАЙНЫЙ ПОДАРОК",
        "gText_MainMenuMysteryEvents": "ТАЙНЫЕ СОБЫТИЯ",
        "gText_WirelessNotConnected": "Беспроводной адаптер\\nне подключён.",
        "gText_ContinueMenuPlayer": "ИГРОК",
        "gText_ContinueMenuTime": "ВРЕМЯ",
        "gText_ContinueMenuPokedex": "ПОКЕДЕКС",
        "gText_ContinueMenuBadges": "ЗНАЧКИ",
    }

    core = {
        "gText_Pokemon": "ПОКЕМОН",
        "gText_Pokedex": "ПОКЕДЕКС",
        "gText_Time": "ВРЕМЯ",
        "gText_Badges": "ЗНАЧКИ",
        "gText_Next": "{A_BUTTON}ДАЛЕЕ",
        "gText_NextBack": "{A_BUTTON}ДАЛЕЕ {B_BUTTON}НАЗАД",
        "gText_AButtonExit": "{A_BUTTON}ВЫХОД",
        "gText_Boy": "МАЛЬЧИК",
        "gText_Girl": "ДЕВОЧКА",
        "gText_Name": "ИМЯ",
        "gText_FlyToWhere": "КУДА ЛЕТЕТЬ?",
        "gMenuText_Use": "ИСП.",
        "gMenuText_Toss": "ВЫБРОС.",
        "gMenuText_Register": "НАЗНАЧ.",
        "gMenuText_Give": "ДАТЬ",
        "gMenuText_Confirm": "ГОТОВО",
        "gText_Cancel": "НАЗАД",
        "gText_Cancel2": "НАЗАД",
        "gText_None": "НЕТ",
        "gText_GoBackPrevMenu": "Вернуться в\\nпредыдущее меню.",
        "gText_WhatWouldYouLike": "Что вы хотите сделать?",
        "gMenuText_Give2": "ДАТЬ",
        "gText_CloseBag": "ЗАКРЫТЬ СУМКУ",
        "gText_NoPokemon": "Здесь нет\\nПОКЕМОНОВ.",
        "gText_TheField": "поле",
        "gText_TheBattle": "бой",
        "gText_ThePokemonList": "список ПОКЕМОНОВ",
        "gText_TheShop": "магазин",
        "gText_ThePC": "ПК",
        "gText_ShopBuy": "КУПИТЬ",
        "gText_ShopSell": "ПРОДАТЬ",
        "gText_ShopQuit": "ВЫХОД",
        "gText_ThatItemIsSoldOut": "Извините, этот предмет закончился.{PAUSE_UNTIL_PRESS}",
        "gText_SoldOut": "НЕТ В НАЛИЧИИ",
        "gText_InBagVar1": "В СУМКЕ: {STR_VAR_1}",
        "gText_QuitShopping": "Закончить покупки.",
        "gText_HereYouGoThankYou": "Вот, пожалуйста!\\nБольшое спасибо.",
        "gText_YouDontHaveMoney": "У вас недостаточно денег.{PAUSE_UNTIL_PRESS}",
        "gText_NoMoreRoomForThis": "В сумке больше нет места\\nдля этого предмета.{PAUSE_UNTIL_PRESS}",
        "gText_AnythingElseICanHelp": "Могу помочь ещё чем-нибудь?",
        "gText_Register": "НАЗНАЧ.",
        "gText_Attack3": "АТАКА",
        "gText_Defense3": "ЗАЩИТА",
        "gText_SpAtk4": "СП. АТК",
        "gText_SpDef4": "СП. ЗАЩ",
        "gText_Speed2": "СКОРОСТЬ",
        "gText_TypeSlash": "ТИП/",
        "gText_Power": "СИЛА",
        "gText_Accuracy2": "ТОЧНОСТЬ",
        "gText_Status": "СТАТУС",
        "gText_ExpPoints": "ОПЫТ",
        "gText_NextLv": "ДО УР.",
        "gText_Switch": "СМЕНИТЬ",
        "gText_PkmnInfo": "ИНФО ПОКЕМОНА",
        "gText_PkmnSkills": "ПАРАМЕТРЫ",
        "gText_BattleMoves": "АТАКИ",
        "gText_Info": "ИНФО",
        "gText_NoItems": "Предметов нет.{PAUSE_UNTIL_PRESS}",
        "gText_BagIsFull": "СУМКА заполнена.{PAUSE_UNTIL_PRESS}",
        "gText_Information": "ИНФОРМАЦИЯ",
        "gText_Yes": "ДА",
        "gText_No": "НЕТ",
        "gText_HallOfFame": "ЗАЛ СЛАВЫ",
        "gText_LogOff": "ВЫЙТИ",
        "gText_MenuOptionPokedex": "ПОКЕДЕКС",
        "gText_MenuOptionPokemon": "ПОКЕМОНЫ",
        "gText_MenuOptionBag": "СУМКА",
        "gText_MenuOptionSave": "СОХРАНИТЬ",
        "gText_MenuOptionOption": "НАСТРОЙКИ",
        "gText_MenuOptionExit": "ВЫХОД",
        "gText_Exit": "ВЫХОД",
        "gText_YourPartysFull": "Ваша команда заполнена!{PAUSE_UNTIL_PRESS}",
        "gText_InParty": "В КОМАНДЕ",
        "gText_SaveCompleted": "Сохранение завершено.",
        "gText_SaveFailed": "Ошибка сохранения…",
    }

    changed = 0
    changed += patch_file(root / "src/main_menu.c", main_menu)
    changed += patch_option_menu(root / "src/option_menu.c")
    changed += patch_file(root / "src/strings.c", core)
    changed += patch_custom_route_dialogue(root)

    print(f"[QARRO_RU_CORE_V3_3] PASS: {changed} visible UI/system/route strings localized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
