#!/usr/bin/env python3
"""Qarro v3.107: localize One Island PC, Silph Co. 5F and Celadon Dept. roof runtime text.

Translates exactly 56 English-only FireRed runtime blocks from the v3.106 surface audit:
  * OneIsland_PokemonCenter_1F_Frlg: 19 remaining blocks
  * SilphCo_5F_Frlg: 19 blocks
  * CeladonCity_DepartmentStore_Roof_Frlg: 18 blocks

Pokemon species, Move and Ability proper names remain English by project canon.
Gameplay/trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ONEISLAND_SILPH5_CELADONROOF_V3_107"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/OneIsland_PokemonCenter_1F_Frlg/scripts.inc": {
        "OneIsland_PokemonCenter_1F_Text_HmmHowAboutLikeThis": "Хм...\\pА если попробовать вот так...$",
        "OneIsland_PokemonCenter_1F_Text_GotPCWorkingStrollAWhileMore": "О, привет, {PLAYER}!\\pВидел? PC снова работает!\\pМне нужно ещё кое-что показать CELIO.\\pМожешь пока немного прогуляться?$",
        "OneIsland_PokemonCenter_1F_Text_SorryForBeingPoorHost": "Прости, что я отнял у BILL столько времени.\\pИ прости, что оказался плохим хозяином во время твоего визита.$",
        "OneIsland_PokemonCenter_1F_Text_UsualPCServicesUnavailable": "Обычные функции PC сейчас недоступны...$",
        "OneIsland_PokemonCenter_1F_Text_CelioImModifyingMyNetworkMachine": "CELIO: Привет!\\nКак всегда, у тебя полно дел.\\pКак мои успехи?\\pЯ дорабатываю СЕТЕВУЮ МАШИНУ.\\pКогда закончу, надеюсь, ты первым её опробуешь, {PLAYER}.$",
        "OneIsland_PokemonCenter_1F_Text_TryingToFindGem": "Я искал этот камень даже во время учёбы.\\pВ итоге не продвинулся ни в поисках, ни в исследованиях...\\pС BILL работа наверняка пошла бы быстрее.\\pНо на этот раз я хочу справиться сам.$",
        "OneIsland_PokemonCenter_1F_Text_WishYouBestOfLuck": "Я...\\nЯ не плачу.\\pЛадно, хватит обо мне!\\p{PLAYER}, ты продолжишь искать редких ПОКЕМОНОВ, верно?\\pЖелаю тебе удачи!$",
        "OneIsland_PokemonCenter_1F_Text_CelioHearingRumorsAboutYou": "CELIO: Привет!\\p{PLAYER}, до меня доходят слухи о тебе.$",
        "OneIsland_PokemonCenter_1F_Text_BillsFirstMonWasAbra": "{PLAYER}, какой вид ПОКЕМОНОВ тебе нравится больше всего?\\pBILL любит всех ПОКЕМОНОВ без исключения.\\pГоворят, первым он поймал ABRA.$",
        "OneIsland_PokemonCenter_1F_Text_BillsHometownInGoldenrod": "Кстати, {PLAYER}, ты из ПАЛЛЕТ-ТАУНА, верно?\\pГоворят, там тихо и приятно.\\pРодной город BILL - ГОЛДЕНРОД-СИТИ, там до сих пор живёт его семья.\\pГоворят, это шумный и весёлый город.\\pКогда-нибудь я хотел бы там побывать.$",
        "OneIsland_PokemonCenter_1F_Text_BillCantStomachMilk": "{PLAYER}, есть что-нибудь, чего ты совсем не переносишь?\\pГоворят, BILL совершенно не выносит молоко.$",
        "OneIsland_PokemonCenter_1F_Text_CameFromPalletDontKnowIt": "О, ты здесь впервые!\\nПривет! Откуда ты?\\p...ПАЛЛЕТ-ТАУН?\\nНе знаю такого места!$",
        "OneIsland_PokemonCenter_1F_Text_EnormousVolcanoOnIsland": "На этом острове есть огромный вулкан.\\pДавно не извергался, так почему бы не прогуляться туда?$",
        "OneIsland_PokemonCenter_1F_Text_WishICouldTradeWithBoyfriend": "Хотела бы я обменяться ПОКЕМОНОМ со своим парнем, который живёт далеко отсюда...$",
        "OneIsland_PokemonCenter_1F_Text_TradedWithFarAwayBoyfriend": "Я обменялась ПОКЕМОНОМ со своим парнем далеко отсюда!\\pВсе говорят, что за это нужно благодарить тебя и CELIO.\\pТак что спасибо!$",
        "OneIsland_PokemonCenter_1F_Text_MachineUnderAdjustment": "СЕТЕВАЯ МАШИНА\\nУровень связи 0\\p...Система хранения ПОКЕМОНОВ настраивается...$",
        "OneIsland_PokemonCenter_1F_Text_MachineLinkedWithKanto": "СЕТЕВАЯ МАШИНА\\nУровень связи 1\\pСвязь с регионом KANTO установлена.$",
        "OneIsland_PokemonCenter_1F_Text_MachineLinkedWithKantoAndHoenn": "СЕТЕВАЯ МАШИНА\\nУровень связи 2\\pСвязь с регионами KANTO и HOENN установлена.$",
        "OneIsland_PokemonCenter_1F_Text_ObtainedTriPass": "Получен ТРИ-ПРОПУСК!$",
    },
    "data/maps/SilphCo_5F_Frlg/scripts.inc": {
        "SilphCo_5F_Text_RocketsInUproarAboutIntruder": "В КОМАНДЕ R переполох из-за какого-то незваного гостя.\\pЭто ведь ты, да?$",
        "SilphCo_5F_Text_YoureOurHeroThankYou": "КОМАНДА R ушла!\\nТы наш герой! Спасибо!$",
        "SilphCo_5F_Text_Grunt1Intro": "Я слышал, тут бродит какой-то ребёнок.$",
        "SilphCo_5F_Text_Grunt1Defeat": "Бум!$",
        "SilphCo_5F_Text_Grunt1PostBattle": "Не стоит затевать драку с КОМАНДОЙ R!$",
        "SilphCo_5F_Text_BeauIntro": "На этом этаже мы изучаем технологию ПОКЕБОЛЛОВ.$",
        "SilphCo_5F_Text_BeauDefeat": "Чёрт!\\nВот же!$",
        "SilphCo_5F_Text_BeauPostBattle": "Мы работали над идеальным ПОКЕБОЛЛОМ, который сможет поймать кого угодно.$",
        "SilphCo_5F_Text_DaltonIntro": "Что-о-о?\\pЗдесь не должно быть никаких детей!$",
        "SilphCo_5F_Text_DaltonDefeat": "Ох, надо же!$",
        "SilphCo_5F_Text_DaltonPostBattle": "Ты всего лишь на 5-м этаже.\\nДо моего БОССА ещё далеко!$",
        "SilphCo_5F_Text_Grunt2Intro": "Прояви хоть немного уважения к КОМАНДЕ R!$",
        "SilphCo_5F_Text_Grunt2Defeat": "Кхе...\\nКхе...$",
        "SilphCo_5F_Text_Grunt2PostBattle": "Кстати говоря.\\pKOFFING эволюционирует в WEEZING!$",
        "SilphCo_5F_Text_PorygonFirstVRMon": "Это ОТЧЁТ О ПОКЕМОНАХ!\\pЛАБОРАТОРИЯ ПОКЕМОНОВ создала PORYGON - первого виртуального ПОКЕМОНА.$",
        "SilphCo_5F_Text_Over350TechniquesConfirmed": "Это ОТЧЁТ О ПОКЕМОНАХ!\\pПодтверждено существование более 350 приёмов ПОКЕМОНОВ.$",
        "SilphCo_5F_Text_SomeMonsEvolveWhenTraded": "Это ОТЧЁТ О ПОКЕМОНАХ!\\pПодтверждено, что некоторые ПОКЕМОНЫ эволюционируют при обмене.$",
        "SilphCo_5F_Text_FloorSign": "ГЛАВНЫЙ ОФИС SILPH CO.\\n5-й ЭТАЖ$",
        "SilphCo_5F_Text_RocketBossLookingForStrongMons": "Эти бандиты, захватившие здание...\\pИх БОСС говорил, что ищет сильных ПОКЕМОНОВ.\\pНадеюсь, наш ПРЕЗИДЕНТ избежал неприятностей...$",
    },
    "data/maps/CeladonCity_DepartmentStore_Roof_Frlg/scripts.inc": {
        "CeladonCity_DepartmentStore_Roof_Text_ImThirstyGiveHerDrink": "Я хочу пить!\\nХочу чего-нибудь выпить!\\p{FONT_NORMAL}Дать ей напиток?$",
        "CeladonCity_DepartmentStore_Roof_Text_GiveWhichDrink": "Какой напиток ей дать?$",
        "CeladonCity_DepartmentStore_Roof_Text_YayFreshWaterHaveThis": "Ура!\\pСВЕЖАЯ ВОДА!\\pСпасибо!\\nВозьми это от меня!$",
        "CeladonCity_DepartmentStore_Roof_Text_ExplainTM16": "TM16 содержит LIGHT SCREEN.\\pЭтот приём ослабляет специальные атаки противника.$",
        "CeladonCity_DepartmentStore_Roof_Text_YaySodaPopHaveThis": "Ура!\\pГАЗИРОВКА!\\pСпасибо!\\nВозьми это от меня!$",
        "CeladonCity_DepartmentStore_Roof_Text_ExplainTM20": "TM20 содержит SAFEGUARD.\\pЭтот приём защищает твою команду от проблем со статусом.$",
        "CeladonCity_DepartmentStore_Roof_Text_YayLemonadeHaveThis": "Ура!\\pЛИМОНАД!\\pСпасибо!\\nВозьми это от меня!$",
        "CeladonCity_DepartmentStore_Roof_Text_ExplainTM33": "TM33 содержит REFLECT.\\pЭтот приём ослабляет физические атаки противника.$",
        "CeladonCity_DepartmentStore_Roof_Text_DontHaveSpaceForThis": "Для этого нет места!$",
        "CeladonCity_DepartmentStore_Roof_Text_ImNotThirstyAfterAll": "Нет, спасибо!\\nЯ уже не хочу пить!$",
        "CeladonCity_DepartmentStore_Roof_Text_MySisterIsImmature": "Не поверишь, моя сестра - ТРЕНЕР.\\pНо она такая несерьёзная, что сводит меня с ума!$",
        "CeladonCity_DepartmentStore_Roof_Text_ImThirstyIWantDrink": "Я хочу пить!\\nХочу чего-нибудь выпить!$",
        "CeladonCity_DepartmentStore_Roof_Text_FloorSign": "ПЛОЩАДКА НА КРЫШЕ:\\nТОРГОВЫЕ АВТОМАТЫ$",
        "CeladonCity_DepartmentStore_Roof_Text_VendingMachineWhatDoesItHave": "Торговый автомат!\\nЧто в нём есть?$",
        "CeladonCity_DepartmentStore_Roof_Text_NotEnoughMoney": "Ой, не хватает денег!$",
        "CeladonCity_DepartmentStore_Roof_Text_DrinkCanPoppedOut": "Из автомата выпал {STR_VAR_1}!$",
        "CeladonCity_DepartmentStore_Roof_Text_NoMoreRoomForStuff": "Больше ничего не помещается!$",
        "CeladonCity_DepartmentStore_Roof_Text_NotThirsty": "Не хочется пить!$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/OneIsland_PokemonCenter_1F_Frlg/scripts.inc": 19,
    "data/maps/SilphCo_5F_Frlg/scripts.inc": 19,
    "data/maps/CeladonCity_DepartmentStore_Roof_Frlg/scripts.inc": 18,
}
EXPECTED_TOTAL = 56


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def asm_quote(text: str) -> str:
    return text.replace('"', '\\"')


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


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


def replace_block(text: str, label: str, translated: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: target already contains Cyrillic; refusing overwrite")
    if ".string " not in old:
        die(f"{label}: target does not look like a text block")
    block = f'{label}::\n\t.string "{asm_quote(translated)}"\n\n'
    return text[:start] + block + text[end:]


def validate_written_file(rel: Path, text: str) -> None:
    for lineno, line in enumerate(text.splitlines(), start=1):
        if ".string \"" in line and line.count('"') < 2:
            die(f"{rel}:{lineno}: physical newline inside assembler string")
    if re.search(r"\\\\[npl]", text):
        die(f"{rel}: doubled FireRed runtime escape found")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    total = sum(len(v) for v in FILES.values())
    if total != EXPECTED_TOTAL:
        die(f"expected translation table total {EXPECTED_TOTAL}, got {total}")

    translated_by_file: dict[str, int] = {}
    for rel_str, patches in FILES.items():
        if len(patches) != EXPECTED_COUNTS[rel_str]:
            die(f"{rel_str}: expected {EXPECTED_COUNTS[rel_str]} entries, got {len(patches)}")
        rel = Path(rel_str)
        path = root / rel
        if not path.is_file():
            die(f"missing target file: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in patches.items():
            validate_translation(label, translated)
            text = replace_block(text, label, translated)
        validate_written_file(rel, text)
        path.write_text(text, encoding="utf-8")
        translated_by_file[rel_str] = len(patches)

    audit = root / "build" / "qarro_ru_oneisland_silph5_celadonroof_v3_107_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(
        json.dumps(
            {
                "marker": MARKER,
                "translatedBlockCount": EXPECTED_TOTAL,
                "translatedByFile": translated_by_file,
                "physicalNewlinesInsideAsmStrings": False,
                "doubledRuntimeEscapes": False,
                "gameplayLogicTouched": False,
                "trainerDataTouched": False,
                "ashBondTouched": False,
                "ashCapTouched": False,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"[{MARKER}] PASS: translated {EXPECTED_TOTAL} runtime blocks across 3 files; "
        "Ash Bond/Ash Cap untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
