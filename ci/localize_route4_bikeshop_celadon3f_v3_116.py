#!/usr/bin/env python3
"""Qarro v3.116: localize Route 4 PC, Cerulean Bike Shop and Celadon Dept. Store 3F.

Translates exactly 37 FireRed runtime text blocks after v3.115:
  * Route4_PokemonCenter_1F_Frlg: 11 audit-visible blocks
  * CeruleanCity_BikeShop_Frlg: 11 audit-visible blocks
  * CeladonCity_DepartmentStore_3F_Frlg: 11 audit-visible blocks + 4 COUNTER tutor blocks

The four generic Text_Counter* labels are runtime-used but are outside the
current _Text_-label RU audit filter; they are deliberately included here.
The unused Japanese Bike Shop block is intentionally untouched.
Pokemon species, Move and Ability proper names remain English by project canon.
Purchase/voucher/tutor/gameplay/trainer logic and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTE4_BIKESHOP_CELADON3F_V3_116"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/Route4_PokemonCenter_1F_Frlg/scripts.inc": {
        "Route4_PokemonCenter_1F_Text_CanHaveSixMonsWithYou": "Так, шесть POKé BALLS на пояс...\\pДа, всё верно. С собой можно\\nносить лишь шесть ПОКЕМОНОВ.$",
        "Route4_PokemonCenter_1F_Text_TeamRocketAttacksCerulean": "КОМАНДА R нападает на жителей\\nСЕРУЛИНА...\\pКаждый день КОМАНДА R снова\\nпопадает в новости.$",
        "Route4_PokemonCenter_1F_Text_LaddieBuyMagikarpForJust500": "МУЖЧИНА: Привет, паренёк!\\nДля тебя есть отличная сделка!\\pПродам редкого ПОКЕМОНА -\\nMAGIKARP - всего за ¥500!\\pНу что, покупаешь?$",
        "Route4_PokemonCenter_1F_Text_SweetieBuyMagikarpForJust500": "МУЖЧИНА: Привет, милая!\\nДля тебя есть отличная сделка!\\pПродам редкого ПОКЕМОНА -\\nMAGIKARP - всего за ¥500!\\pНу что, покупаешь?$",
        "Route4_PokemonCenter_1F_Text_PaidOutrageouslyForMagikarp": "{PLAYER} заплатил безумные ¥500\\nи купил MAGIKARP...$",
        "Route4_PokemonCenter_1F_Text_OnlyDoingThisAsFavorToYou": "Нет? Отказываешься?\\nЯ ведь делаю тебе одолжение!$",
        "Route4_PokemonCenter_1F_Text_NoRoomForMorePokemon": "Похоже, у тебя больше нет места\\nдля ПОКЕМОНОВ.$",
        "Route4_PokemonCenter_1F_Text_YoullNeedMoreMoney": "Тебе понадобится больше денег!$",
        "Route4_PokemonCenter_1F_Text_IDontGiveRefunds": "МУЖЧИНА: Возврата денег нет.\\nТы знал, что покупаешь!$",
        "Route4_PokemonCenter_1F_Text_ShouldStoreMonsUsingPC": "Иногда команда уже заполнена,\\nи нового ПОКЕМОНА не взять.\\pТогда оставь кого-нибудь\\nв любом ПК.$",
        "Route4_PokemonCenter_1F_Text_ItsANewspaper": "Это газета.$",
    },
    "data/maps/CeruleanCity_BikeShop_Frlg/scripts.inc": {
        "CeruleanCity_BikeShop_Text_WelcomeToBikeShop": "Привет!\\nДобро пожаловать в BIKE SHOP.\\pУ нас точно найдётся BIKE\\nдля тебя!$",
        "CeruleanCity_BikeShop_Text_SorryYouCantAffordIt": "Извини!\\nТебе это не по карману!$",
        "CeruleanCity_BikeShop_Text_OhBikeVoucherHereYouGo": "О, это же...\\pBIKE VOUCHER!\\pХорошо!\\nВот, держи!$",
        "CeruleanCity_BikeShop_Text_ExchangedVoucherForBicycle": "{PLAYER} обменял BIKE VOUCHER\\nна BICYCLE.$",
        "CeruleanCity_BikeShop_Text_ThankYouComeAgain": "Спасибо!\\nЗаходи ещё!$",
        "CeruleanCity_BikeShop_Text_HowDoYouLikeNewBicycle": "Ну как тебе новый BICYCLE?\\nНравится ездить?\\pНа нём можно ездить по\\nCYCLING ROAD и даже\\lзаезжать в пещеры!$",
        "CeruleanCity_BikeShop_Text_MakeRoomForBicycle": "Освободи место для BICYCLE!$",
        "CeruleanCity_BikeShop_Text_CityBikeGoodEnoughForMe": "Мне вполне хватает обычного\\nгородского велосипеда.\\pВ конце концов, на горный\\nвелосипед корзину не поставишь.$",
        "CeruleanCity_BikeShop_Text_BikesCoolButExpensive": "Эти велосипеды классные,\\nно ужасно дорогие!$",
        "CeruleanCity_BikeShop_Text_WowYourBikeIsCool": "Ого.\\nУ тебя очень крутой BIKE!$",
        "CeruleanCity_BikeShop_Text_ShinyNewBicycle": "Блестящий новый BICYCLE!$",
    },
    "data/maps/CeladonCity_DepartmentStore_3F_Frlg/scripts.inc": {
        "CeladonCity_DepartmentStore_3F_Text_OTStandsForOriginalTrainer": "У пойманного ПОКЕМОНА есть\\nID No. и OT.\\pOT - первоначальный ТРЕНЕР,\\nкоторый поймал его первым.$",
        "CeladonCity_DepartmentStore_3F_Text_BuddyTradingKangaskhanForHaunter": "Отлично!\\pМой приятель обменяет своего\\nKANGASKHAN на моего HAUNTER!$",
        "CeladonCity_DepartmentStore_3F_Text_HaunterEvolvedOnTrade": "Давай, HAUNTER!\\pЯ обожаю HAUNTER!\\nЯ их коллекционирую!\\pА?\\pВо время обмена HAUNTER\\nпревратился в другого ПОКЕМОНА!$",
        "CeladonCity_DepartmentStore_3F_Text_CanIdentifyTradeMonsByID": "Обменных ПОКЕМОНОВ можно узнать\\nпо их ID No.$",
        "CeladonCity_DepartmentStore_3F_Text_ItsSuperNES": "Это Super NES.$",
        "CeladonCity_DepartmentStore_3F_Text_AnRPG": "RPG!\\nНа это сейчас нет времени!$",
        "CeladonCity_DepartmentStore_3F_Text_SportsGame": "Спортивная игра!\\nПапе такое понравится!$",
        "CeladonCity_DepartmentStore_3F_Text_PuzzleGame": "Головоломка!\\nПохоже, затягивает!$",
        "CeladonCity_DepartmentStore_3F_Text_FightingGame": "Файтинг!\\nВыглядит сложно!$",
        "CeladonCity_DepartmentStore_3F_Text_TVGameShop": "3F: МАГАЗИН ВИДЕОИГР$",
        "CeladonCity_DepartmentStore_3F_Text_RedGreenBothArePokemon": "Red и Green!\\nОбе игры - о ПОКЕМОНАХ!$",
        "Text_CounterTeach": "О, привет!\\nЯ наконец закончил POKéMON.\\pЕщё не закончил? Хочешь,\\nя научу тебя хорошему приёму?\\pЯ говорю о приёме COUNTER.\\pИ не тот COUNTER,\\nна который я опираюсь!$",
        "Text_CounterDeclined": "Не интересно? Приходи,\\nесли передумаешь.$",
        "Text_CounterWhichMon": "Какого ПОКЕМОНА научить\\nCOUNTER?$",
        "Text_CounterTaught": "Используешь COUNTER, которому\\nя научил твоего ПОКЕМОНА?$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/Route4_PokemonCenter_1F_Frlg/scripts.inc": 11,
    "data/maps/CeruleanCity_BikeShop_Frlg/scripts.inc": 11,
    "data/maps/CeladonCity_DepartmentStore_3F_Frlg/scripts.inc": 15,
}
EXPECTED_TOTAL = 37
AUDIT_VISIBLE_TOTAL = 33
COUNTER_TUTOR_BLIND_SPOT_TOTAL = 4


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def validate_translation(label: str, translated: str) -> None:
    if not translated.endswith("$"):
        die(f"{label}: translated text must end with $")
    if "\n" in translated or "\r" in translated:
        die(f"{label}: physical newline/carriage return in translation value")
    if any(ch in translated for ch in ("—", "–", "“", "”", "’", "…", "«", "»")):
        die(f"{label}: unsupported Unicode punctuation")
    if "\\\\" in translated:
        die(f"{label}: doubled runtime backslash in translation value")
    if not re.search(r"[А-Яа-яЁё]", translated):
        die(f"{label}: expected Cyrillic translation")


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def replace_block(text: str, label: str, translated: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: target already contains Cyrillic; refusing overwrite")
    if ".string " not in old:
        die(f"{label}: target does not look like a text block")
    safe = translated.replace('"', '\\"')
    block = f'{label}::\n\t.string "{safe}"\n\n'
    return text[:start] + block + text[end:]


def validate_written(rel: Path, text: str) -> None:
    for lineno, line in enumerate(text.splitlines(), start=1):
        if '.string "' in line and line.count('"') < 2:
            die(f"{rel}:{lineno}: physical newline inside assembler string")
    if re.search(r"\\\\[npl]", text):
        die(f"{rel}: doubled FireRed runtime escape found")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    total = 0
    translated_by_file = {}
    for rel_s, patches in FILES.items():
        expected = EXPECTED_COUNTS[rel_s]
        if len(patches) != expected:
            die(f"{rel_s}: expected {expected} entries, got {len(patches)}")
        rel = Path(rel_s)
        path = root / rel
        if not path.is_file():
            die(f"missing target: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in patches.items():
            validate_translation(label, translated)
            text = replace_block(text, label, translated)
        validate_written(rel, text)
        path.write_text(text, encoding="utf-8")
        translated_by_file[rel_s] = len(patches)
        total += len(patches)

    if total != EXPECTED_TOTAL:
        die(f"expected {EXPECTED_TOTAL} translated blocks, got {total}")

    audit = root / "build" / "qarro_ru_route4_bikeshop_celadon3f_v3_116_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlockCount": EXPECTED_TOTAL,
        "auditVisibleTextBlockCount": AUDIT_VISIBLE_TOTAL,
        "counterTutorBlindSpotBlockCount": COUNTER_TUTOR_BLIND_SPOT_TOTAL,
        "translatedByFile": translated_by_file,
        "magikarpPurchaseLogicTouched": False,
        "bikeVoucherLogicTouched": False,
        "counterTutorLogicTouched": False,
        "unusedJapaneseBlocksTouched": False,
        "physicalNewlinesInsideAsmStrings": False,
        "doubledRuntimeEscapes": False,
        "gameplayLogicTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks "
        f"({AUDIT_VISIBLE_TOTAL} audit-visible + {COUNTER_TUTOR_BLIND_SPOT_TOTAL} COUNTER tutor blind-spot); "
        "purchase/voucher/tutor/gameplay/trainer/Ash logic untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
