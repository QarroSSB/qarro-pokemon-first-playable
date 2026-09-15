#!/usr/bin/env python3
"""Qarro v3.114: localize Oak aide rewards and small gatehouse/center runtime text.

Translates exactly 33 English-only FireRed runtime blocks after v3.113:
  * Route2_EastBuilding_Frlg: 5
  * Route10_PokemonCenter_1F_Frlg: 7
  * Route11_EastEntrance_2F_Frlg: 7
  * Route15_WestEntrance_2F_Frlg: 6
  * Route16_NorthEntrance_2F_Frlg: 8

Pokemon species, Move and Ability proper names remain English by project canon.
Reward/event logic, trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_OAK_AIDES_GATEHOUSES_V3_114"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/Route2_EastBuilding_Frlg/scripts.inc": {
        "Route2_EastBuilding_Text_GiveHM05IfSeen10Mons": "Привет! Помнишь меня?\\nЯ один из ПОМОЩНИКОВ ПРОФ. ОУКА.\\pЕсли в твоём ПОКЕДЕКСЕ есть данные\\nо десяти видах, тебе полагается награда.\\pПРОФ. ОУК доверил мне HM05\\nдля тебя.\\pИтак, {PLAYER}, скажи:\\pТы собрал данные хотя бы\\nо десяти видах ПОКЕМОНОВ?$",
        "Route2_EastBuilding_Text_GreatHereYouGo": "Отлично! Ты поймал или получил\\n{STR_VAR_3} видов ПОКЕМОНОВ!\\pПоздравляю!\\nВот, держи!$",
        "Route2_EastBuilding_Text_ReceivedHM05FromAide": "{PLAYER} получает HM05\\nот ПОМОЩНИКА.$",
        "Route2_EastBuilding_Text_ExplainHM05": "В HM05 находится скрытый приём\\nFLASH.\\pFLASH освещает даже самые тёмные\\nпещеры и подземелья.$",
        "Route2_EastBuilding_Text_CanGetThroughRockTunnel": "Когда ПОКЕМОН выучит FLASH,\\nты сможешь пройти СКАЛЬНЫЙ ТУННЕЛЬ.$",
    },
    "data/maps/Route10_PokemonCenter_1F_Frlg/scripts.inc": {
        "Route10_PokemonCenter_1F_Text_EveryTypeStrongerThanOthers": "Типы ПОКЕМОНОВ по-разному\\nвзаимодействуют друг с другом.\\pКаждый тип сильнее одних типов\\nи слабее других.$",
        "Route10_PokemonCenter_1F_Text_NuggetUselessSoldFor5000": "NUGGET совершенно бесполезен.\\nПоэтому я продал его за ¥5000.$",
        "Route10_PokemonCenter_1F_Text_HeardGhostsHauntLavender": "Я слышал, что в ЛАВЕНДЕР-ТАУНЕ\\nводятся призраки.$",
        "Route10_PokemonCenter_1F_Text_GiveEverstoneIfCaught20Mons": "О... {PLAYER}!\\nЯ тебя искал!\\pЯ один из ПОМОЩНИКОВ\\nПРОФ. ОУКА.\\pЕсли в твоём ПОКЕДЕКСЕ есть данные\\nо двадцати видах, тебе полагается награда.\\pОн доверил мне для тебя\\nEVERSTONE.\\pИтак, {PLAYER}, скажи:\\pТы собрал данные хотя бы\\nо двадцати видах ПОКЕМОНОВ?$",
        "Route10_PokemonCenter_1F_Text_GreatHereYouGo": "Отлично! Ты поймал или получил\\n{STR_VAR_3} видов ПОКЕМОНОВ!\\pПоздравляю!\\nВот, держи!$",
        "Route10_PokemonCenter_1F_Text_ReceivedEverstoneFromAide": "{PLAYER} получает EVERSTONE\\nот ПОМОЩНИКА.$",
        "Route10_PokemonCenter_1F_Text_ExplainEverstone": "Эволюция ПОКЕМОНОВ помогает\\nзаполнять ПОКЕДЕКС.\\pНо иногда ты можешь не хотеть,\\nчтобы ПОКЕМОН эволюционировал.\\pТогда дай ему EVERSTONE.\\pПо словам ПРОФЕССОРА,\\nон предотвратит эволюцию.$",
    },
    "data/maps/Route11_EastEntrance_2F_Frlg/scripts.inc": {
        "Route11_EastEntrance_2F_Text_GiveItemfinderIfCaught30": "Привет! Помнишь меня?\\nЯ один из ПОМОЩНИКОВ ПРОФ. ОУКА.\\pЕсли в твоём ПОКЕДЕКСЕ есть данные\\nо {STR_VAR_1} видах, тебе полагается награда.\\pПРОФ. ОУК доверил мне для тебя\\n{STR_VAR_2}.\\pИтак, {PLAYER}, скажи:\\pТы собрал данные хотя бы\\nо {STR_VAR_1} видах ПОКЕМОНОВ?$",
        "Route11_EastEntrance_2F_Text_GreatHereYouGo": "Отлично! Ты поймал или получил\\n{STR_VAR_3} видов ПОКЕМОНОВ!\\pПоздравляю!\\nВот, держи!$",
        "Route11_EastEntrance_2F_Text_ReceivedItemfinderFromAide": "{PLAYER} получает {STR_VAR_2}\\nот ПОМОЩНИКА.$",
        "Route11_EastEntrance_2F_Text_ExplainItemfinder": "На земле бывают предметы,\\nкоторых не видно.\\pИспользуй ITEMFINDER, чтобы найти\\nскрытые предметы поблизости.\\pНо прибор не может указать\\nточное место предмета.\\pОн лишь показывает направление.\\pОпредели сторону, а затем\\nобыщи подозрительное место сам.$",
        "Route11_EastEntrance_2F_Text_BigMonAsleepOnRoad": "Посмотрим в бинокль...\\pНа дороге спит\\nогромный ПОКЕМОН!$",
        "Route11_EastEntrance_2F_Text_WhatABreathtakingView": "Посмотрим в бинокль...\\pКакой потрясающий вид!$",
        "Route11_EastEntrance_2F_Text_RockTunnelGoodRouteToLavender": "Посмотрим в бинокль...\\pЧтобы попасть из СЕРУЛИН-СИТИ\\nв ЛАВЕНДЕР-ТАУН,\\pлучше всего идти через\\nСКАЛЬНЫЙ ТУННЕЛЬ.$",
    },
    "data/maps/Route15_WestEntrance_2F_Frlg/scripts.inc": {
        "Route15_WestEntrance_2F_Text_GiveItemIfCaughtEnough": "Привет! Помнишь меня?\\nЯ один из ПОМОЩНИКОВ ПРОФ. ОУКА.\\pЕсли в твоём ПОКЕДЕКСЕ есть данные\\nо {STR_VAR_1} видах, тебе полагается награда.\\pПРОФ. ОУК доверил мне для тебя\\n{STR_VAR_2}.\\pИтак, {PLAYER}, скажи:\\pТы собрал данные хотя бы\\nо {STR_VAR_1} видах ПОКЕМОНОВ?$",
        "Route15_WestEntrance_2F_Text_GreatHereYouGo": "Отлично! Ты поймал или получил\\n{STR_VAR_3} видов ПОКЕМОНОВ!\\pПоздравляю!\\nВот, держи!$",
        "Route15_WestEntrance_2F_Text_ReceivedItemFromAide": "{PLAYER} получает {STR_VAR_2}\\nот ПОМОЩНИКА.$",
        "Route15_WestEntrance_2F_Text_ExplainExpShare": "EXP. SHARE - предмет, который\\nможет держать ПОКЕМОН.\\pТак ПОКЕМОН получает часть опыта,\\nдаже не участвуя в бою.$",
        "Route15_WestEntrance_2F_Text_LargeShiningBird": "Посмотрим в бинокль...\\pБольшая сияющая птица летит\\nв сторону моря.$",
        "Route15_WestEntrance_2F_Text_SmallIslandOnHorizon": "Посмотрим в бинокль...\\pНа горизонте виден\\nмаленький остров!$",
    },
    "data/maps/Route16_NorthEntrance_2F_Frlg/scripts.inc": {
        "Route16_NorthEntrance_2F_Text_OnBikeRideWithGirlfriend": "Мы с моей девушкой спокойно\\nкатаемся на новом велосипеде.$",
        "Route16_NorthEntrance_2F_Text_RidingTogetherOnNewBikes": "Мы вместе катаемся\\nна наших новых велосипедах.$",
        "Route16_NorthEntrance_2F_Text_ItsCeladonDeptStore": "Посмотрим в бинокль...\\pЭто УНИВЕРМАГ СЕЛАДОНА!$",
        "Route16_NorthEntrance_2F_Text_LongPathOverWater": "Посмотрим в бинокль...\\pВдалеке над водой тянется\\nдлинная дорога.$",
        "Route16_NorthEntrance_2F_Text_GiveAmuletCoinIfCaught40": "Привет! Помнишь меня?\\nЯ один из ПОМОЩНИКОВ ПРОФ. ОУКА.\\pЕсли в твоём ПОКЕДЕКСЕ есть данные\\nо 40 видах, тебе полагается награда.\\pПРОФ. ОУК доверил мне для тебя\\nAMULET COIN.\\pИтак, {PLAYER}, скажи:\\pТы собрал данные хотя бы\\nо 40 видах ПОКЕМОНОВ?$",
        "Route16_NorthEntrance_2F_Text_GreatHereYouGo": "Отлично! Ты поймал или получил\\n{STR_VAR_3} видов ПОКЕМОНОВ!\\pПоздравляю!\\nВот, держи!$",
        "Route16_NorthEntrance_2F_Text_ReceivedAmuletCoinFromAide": "{PLAYER} получает AMULET COIN\\nот ПОМОЩНИКА.$",
        "Route16_NorthEntrance_2F_Text_ExplainAmuletCoin": "AMULET COIN - предмет, который\\nможет держать ПОКЕМОН.\\pЕсли этот ПОКЕМОН участвовал\\nв победном бою, ты получишь больше денег.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/Route2_EastBuilding_Frlg/scripts.inc": 5,
    "data/maps/Route10_PokemonCenter_1F_Frlg/scripts.inc": 7,
    "data/maps/Route11_EastEntrance_2F_Frlg/scripts.inc": 7,
    "data/maps/Route15_WestEntrance_2F_Frlg/scripts.inc": 6,
    "data/maps/Route16_NorthEntrance_2F_Frlg/scripts.inc": 8,
}
EXPECTED_TOTAL = 33


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

    audit = root / "build" / "qarro_ru_oak_aides_gatehouses_v3_114_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlockCount": EXPECTED_TOTAL,
        "translatedByFile": translated_by_file,
        "rewardEventLogicTouched": False,
        "physicalNewlinesInsideAsmStrings": False,
        "doubledRuntimeEscapes": False,
        "gameplayLogicTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; reward/gameplay/trainer/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
