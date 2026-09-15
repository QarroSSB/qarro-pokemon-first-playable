#!/usr/bin/env python3
"""Qarro v3.115: localize residual Pokemon Center and Vermilion Mart runtime text.

Translates exactly 22 English-only FireRed runtime blocks after v3.114:
  * SixIsland_PokemonCenter_1F_Frlg: 3
  * IndigoPlateau_PokemonCenter_1F_Frlg: 5
  * CinnabarIsland_PokemonCenter_1F_Frlg: 6
  * VermilionCity_PokemonCenter_1F_Frlg: 6
  * VermilionCity_Mart_Frlg: 2

Pokemon species, Move and Ability proper names remain English by project canon.
Rival/Bill/VS Seeker/Pokemart/event logic, trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_PC_MART_RESIDUALS_V3_115"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/SixIsland_PokemonCenter_1F_Frlg/scripts.inc": {
        "SixIsland_PokemonCenter_1F_Text_SomethingHiddenOnThisIsland": "Уже десять лет я ищу РУИНЫ.\\pНет, пожалуй, двадцать лет.\\pУ меня такое чувство, что на этом\\nострове что-то скрыто.$",
        "SixIsland_PokemonCenter_1F_Text_SomeMonsEvolveByTradingWithHeldItem": "Ты знаешь, что некоторые ПОКЕМОНЫ\\nэволюционируют только при обмене?\\pНо есть и другие.\\pНекоторые ПОКЕМОНЫ эволюционируют\\nтолько при обмене, если держат\\lособый предмет.$",
        "SixIsland_PokemonCenter_1F_Text_RivalImpossibleToGetAllMonsAroundHere": "{RIVAL}: Эй, {PLAYER}!\\nКак продвигается твой ПОКЕДЕКС?\\pПохоже, всех ПОКЕМОНОВ здесь\\nсобрать невозможно.\\pНаверное, где-то далеко есть\\nнеизвестные нам ПОКЕМОНЫ...\\p... ... ...\\pДаже если у меня не выходит,\\nу тебя тем более не получится.\\pНо я не собираюсь из-за этого\\nсходить с ума.\\pБуду собирать ПОКЕМОНОВ в своём\\nтемпе и тренировать их.\\pТак и поступлю.\\nЗдесь мне больше делать нечего.\\lПора домой.\\pВот и всё!\\nУвидимся!$",
    },
    "data/maps/IndigoPlateau_PokemonCenter_1F_Frlg/scripts.inc": {
        "IndigoPlateau_PokemonCenter_1F_Text_GymGuyAdvice": "Йо!\\nБудущий чемпион!\\pВ ЛИГЕ ПОКЕМОНОВ тебе придётся\\nподряд сразиться со всей\\lЭЛИТНОЙ ЧЕТВЁРКОЙ.\\pПроиграешь - придётся начинать\\nсначала!\\pВот он, решающий момент!\\nВперёд!$",
        "IndigoPlateau_PokemonCenter_1F_Text_FaceEliteFourGoodLuck": "Отсюда ты будешь сражаться\\nс ЭЛИТНОЙ ЧЕТВЁРКОЙ по очереди.\\pПосле каждой победы откроется дверь\\nк следующему ТРЕНЕРУ. Удачи!$",
        "IndigoPlateau_PokemonCenter_1F_Text_LoreleiIsAbsentClosedForTimeBeing": "К сожалению, сейчас ЛИГА недоступна.\\pLORELEI из ЭЛИТНОЙ ЧЕТВЁРКИ\\nотсутствует.\\pПоэтому ЛИГА ПОКЕМОНОВ временно\\nзакрыта.$",
        "IndigoPlateau_PokemonCenter_1F_Text_AgathaWhuppedUs": "ПОКЕМОНЫ типа GHOST у AGATHA\\nужасающе сильны.\\pЯ довёл своих ПОКЕМОНОВ типа\\nFIGHTING до предела.\\pЯ бросил вызов AGATHA, уверенный\\nв победе, но она нас разгромила.\\pУ этой старушки ещё и очень\\nвспыльчивый характер.\\pПочти ничего не нужно, чтобы\\nона начала кричать.$",
        "IndigoPlateau_PokemonCenter_1F_Text_LancesCousinGymLeaderFarAway": "Может, членство в ЭЛИТНОЙ ЧЕТВЁРКЕ\\nу них в крови.\\pЯ слышал, кто-то из родни LANCE\\nтоже ЛИДЕР ГИМА где-то далеко.$",
    },
    "data/maps/CinnabarIsland_PokemonCenter_1F_Frlg/scripts.inc": {
        "CinnabarIsland_PokemonCenter_1F_Text_CinnabarGymLocked": "Дверь ГИМА ОСТРОВА СИННАБАР\\nнаглухо заперта.\\pГде-то должен быть ключ.\\pМожет, он в том сгоревшем\\nособняке?\\pГоворят, раньше там жил\\nдруг ЛИДЕРА ГИМА.$",
        "CinnabarIsland_PokemonCenter_1F_Text_VisitUnionRoom": "У тебя много друзей?\\pИграть со старыми друзьями весело.\\pНо почему бы иногда не заглянуть\\nв UNION ROOM?\\pКто знает, может, там появятся\\nновые друзья.\\pДумаю, стоит туда заглянуть.$",
        "CinnabarIsland_PokemonCenter_1F_Text_EvolutionCanWaitForNewMoves": "ПОКЕМОНЫ всё ещё могут учить\\nприёмы после отмены эволюции.\\pС эволюцией можно подождать,\\nпока не будут выучены новые приёмы.$",
        "CinnabarIsland_PokemonCenter_1F_Text_ReadyToSailToOneIsland": "BILL: Эй, я тебя заждался!\\nОтправляемся на ONE ISLAND?$",
        "CinnabarIsland_PokemonCenter_1F_Text_OhNotDoneYet": "О, у тебя ещё остались дела?$",
        "CinnabarIsland_PokemonCenter_1F_Text_LetsGo": "Ну, всё.\\nПойдём!$",
    },
    "data/maps/VermilionCity_PokemonCenter_1F_Frlg/scripts.inc": {
        "VermilionCity_PokemonCenter_1F_Text_TrainerMonsStrongerThanWild": "Даже на одном уровне у ПОКЕМОНОВ\\nмогут сильно различаться параметры\\lи способности.\\pПОКЕМОН, выращенный ТРЕНЕРОМ,\\nсильнее дикого.$",
        "VermilionCity_PokemonCenter_1F_Text_PoisonedMonFaintedWhileWalking": "Мой ПОКЕМОН был отравлен!\\nОн потерял сознание, пока мы шли!$",
        "VermilionCity_PokemonCenter_1F_Text_AllMonWeakToSpecificTypes": "ПОКЕМОН более высокого уровня\\nдействительно будет сильнее...\\pНо у каждого ПОКЕМОНА есть слабость\\nк определённым типам.\\pПохоже, совершенно непобедимых\\nПОКЕМОНОВ не бывает.$",
        "VermilionCity_PokemonCenter_1F_Text_UrgeToBattleSomeoneAgain": "Бывало желание снова сразиться\\nс уже знакомым ТРЕНЕРОМ?\\pНаверняка да.\\pМне тоже хотелось снова и снова\\nсражаться с некоторыми людьми.\\pПоэтому я раздаю эти устройства.\\nВозьми одно!$",
        "VermilionCity_PokemonCenter_1F_Text_UseDeviceForRematches": "Используй это устройство, и найдёшь\\nТРЕНЕРОВ, желающих реванша.\\pНо перед использованием нужно\\nзарядить его батарею.$",
        "VermilionCity_PokemonCenter_1F_Text_ExplainVSSeeker": "Как пользоваться VS SEEKER?\\nПроще простого.\\pВключи его - бип-бип-бип - и\\nТРЕНЕРЫ вокруг заметят сигнал.\\pЕсли кто-то хочет реванша,\\nустройство сразу сообщит об этом.\\pЗаряди батарею и используй его\\nна дороге.$",
    },
    "data/maps/VermilionCity_Mart_Frlg/scripts.inc": {
        "VermilionCity_Mart_Text_TeamRocketAreWickedPeople": "Есть мерзавцы, которые используют\\nПОКЕМОНОВ для преступлений.\\pНапример, КОМАНДА R торгует\\nредкими ПОКЕМОНАМИ.\\pА тех ПОКЕМОНОВ, которых считает\\nбесполезными, просто бросает.\\pВот какие ужасные люди\\nсостоят в КОМАНДЕ R.$",
        "VermilionCity_Mart_Text_MonsGoodOrBadDependingOnTrainer": "Думаю, ПОКЕМОН может стать\\nхорошим или плохим.\\pВсё зависит от ТРЕНЕРА.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/SixIsland_PokemonCenter_1F_Frlg/scripts.inc": 3,
    "data/maps/IndigoPlateau_PokemonCenter_1F_Frlg/scripts.inc": 5,
    "data/maps/CinnabarIsland_PokemonCenter_1F_Frlg/scripts.inc": 6,
    "data/maps/VermilionCity_PokemonCenter_1F_Frlg/scripts.inc": 6,
    "data/maps/VermilionCity_Mart_Frlg/scripts.inc": 2,
}
EXPECTED_TOTAL = 22


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

    audit = root / "build" / "qarro_ru_pc_mart_residuals_v3_115_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlockCount": EXPECTED_TOTAL,
        "translatedByFile": translated_by_file,
        "eventLogicTouched": False,
        "rivalLogicTouched": False,
        "billTravelLogicTouched": False,
        "vsSeekerRewardLogicTouched": False,
        "pokemartLogicTouched": False,
        "physicalNewlinesInsideAsmStrings": False,
        "doubledRuntimeEscapes": False,
        "gameplayLogicTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; event/trainer/Ash logic untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
