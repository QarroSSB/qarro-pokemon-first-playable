#!/usr/bin/env python3
"""Qarro v3.112: localize Route 5 Day Care, Victory Road 2F and Viridian School runtime text.

Translates exactly 45 English-only FireRed runtime blocks after v3.111:
  * Route5_PokemonDayCare_Frlg: 15
  * VictoryRoad_2F_Frlg: 15
  * ViridianCity_School_Frlg: 15

The two unused Japanese Day Care blocks and unused Japanese Moltres cry are intentionally untouched.
Pokemon species, Move and Ability proper names remain English by project canon.
Gameplay/trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_DAYCARE_VICTORY2_SCHOOL_V3_112"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/Route5_PokemonDayCare_Frlg/scripts.inc": {
        "Route5_PokemonDayCare_Text_WantMeToRaiseMon": "Я управляю ПИТОМНИКОМ.\\pХочешь, чтобы я вырастил одного\\nиз твоих ПОКЕМОНОВ?$",
        "Route5_PokemonDayCare_Text_ComeAgain": "Заходи ещё.$",
        "Route5_PokemonDayCare_Text_WhichMonShouldIRaise": "Какого ПОКЕМОНА мне растить?$",
        "Route5_PokemonDayCare_Text_ComeAnytimeYouLike": "Хорошо.\\nПриходи, когда захочешь.$",
        "Route5_PokemonDayCare_Text_LookAfterMonForAWhile": "Хорошо, я присмотрю за твоим\\n{STR_VAR_1} некоторое время.$",
        "Route5_PokemonDayCare_Text_ComeSeeMeInAWhile": "Загляни ко мне через некоторое время.$",
        "Route5_PokemonDayCare_Text_MonNeedsToSpendMoreTime": "Уже вернулся?\\pТвоему {STR_VAR_1} нужно побыть\\nсо мной ещё немного.$",
        "Route5_PokemonDayCare_Text_OweMeXForMonsReturn": "С тебя ¥{STR_VAR_2} за возвращение\\nэтого ПОКЕМОНА.$",
        "Route5_PokemonDayCare_Text_ThankYouHeresMon": "Спасибо!\\nВот твой ПОКЕМОН.$",
        "Route5_PokemonDayCare_Text_PlayerGotMonBack": "{PLAYER} забрал {STR_VAR_1}\\nу СМОТРИТЕЛЯ ПИТОМНИКА.$",
        "Route5_PokemonDayCare_Text_OnlyHaveOneMonWithYou": "О? У тебя с собой только один\\nПОКЕМОН.$",
        "Route5_PokemonDayCare_Text_WhatWillYouBattleWith": "Если оставишь мне этого ПОКЕМОНА,\\nкем будешь сражаться?$",
        "Route5_PokemonDayCare_Text_MonHasGrownByXLevels": "Твой {STR_VAR_1} сильно вырос.\\nДа, очень сильно.\\pПосмотрим...\\nОн вырос на {STR_VAR_2} ур.\\pНеплохо я справился, правда?$",
        "Route5_PokemonDayCare_Text_YouveGotNoRoomForIt": "Ты не сможешь забрать этого ПОКЕМОНА,\\nесли в команде нет места.$",
        "Route5_PokemonDayCare_Text_DontHaveEnoughMoney": "У тебя недостаточно денег.$",
    },
    "data/maps/VictoryRoad_2F_Frlg/scripts.inc": {
        "VictoryRoad_2F_Text_DawsonIntro": "Если пройдёшь отсюда,\\nсможешь встретиться с ЭЛИТНОЙ ЧЕТВЁРКОЙ.$",
        "VictoryRoad_2F_Text_DawsonDefeat": "Нет!\\nНевероятно!$",
        "VictoryRoad_2F_Text_DawsonPostBattle": "Но в знаниях о ПОКЕМОНАХ\\nя всё равно тебя обойду!$",
        "VictoryRoad_2F_Text_DaisukeIntro": "Это ДОРОГА ПОБЕДЫ.\\nПоследнее испытание для ТРЕНЕРОВ!$",
        "VictoryRoad_2F_Text_DaisukeDefeat": "Апчхи!$",
        "VictoryRoad_2F_Text_DaisukePostBattle": "Если застрянешь, попробуй\\nподвигать валуны.$",
        "VictoryRoad_2F_Text_NelsonIntro": "Так ты хочешь бросить вызов\\nЭЛИТНОЙ ЧЕТВЁРКЕ?$",
        "VictoryRoad_2F_Text_NelsonDefeat": "Ты меня одолел!$",
        "VictoryRoad_2F_Text_NelsonPostBattle": "{RIVAL} тоже проходил здесь.$",
        "VictoryRoad_2F_Text_VincentIntro": "Давай!\\nЯ тебя разгромлю!$",
        "VictoryRoad_2F_Text_VincentDefeat": "Разгромили меня!$",
        "VictoryRoad_2F_Text_VincentPostBattle": "Ты заслужил право находиться\\nна ДОРОГЕ ПОБЕДЫ.$",
        "VictoryRoad_2F_Text_GregoryIntro": "ДОРОГА ПОБЕДЫ слишком трудна?$",
        "VictoryRoad_2F_Text_GregoryDefeat": "Отлично сработано!$",
        "VictoryRoad_2F_Text_GregoryPostBattle": "Многие ТРЕНЕРЫ сдаются здесь\\nи возвращаются домой.$",
    },
    "data/maps/ViridianCity_School_Frlg/scripts.inc": {
        "ViridianCity_School_Text_TryingToMemorizeNotes": "Фух! Пытаюсь запомнить\\nвсе свои записи.$",
        "ViridianCity_School_Text_ReadBlackboardCarefully": "Хорошо!\\pОбязательно внимательно прочитай,\\nчто написано на доске!$",
        "ViridianCity_School_Text_NotebookFirstPage": "Посмотрим тетрадь.\\pПервая страница...\\pPOKé BALLS нужны, чтобы ловить\\nПОКЕМОНОВ.\\pВ команде можно носить\\nдо шести ПОКЕМОНОВ.\\pЛюдей, которые растят ПОКЕМОНОВ\\nи сражаются ими, зовут ТРЕНЕРАМИ.$",
        "ViridianCity_School_Text_NotebookSecondPage": "Вторая страница...\\pЗдорового ПОКЕМОНА трудно поймать,\\nсначала ослабь его.\\pОтравление, ожог или другой статус\\nтоже помогут ослабить его.$",
        "ViridianCity_School_Text_NotebookThirdPage": "Третья страница...\\pТРЕНЕРЫ ПОКЕМОНОВ ищут других,\\nчтобы сразиться.\\pДля ТРЕНЕРА вкус победы\\nособенно сладок.\\pБои постоянно проходят\\nв ПОКЕМОН-ГИМАХ по всему миру.$",
        "ViridianCity_School_Text_NotebookFourthPage": "Четвёртая страница...\\pГлавная цель каждого\\nТРЕНЕРА ПОКЕМОНОВ проста.\\pПобедить восемь ЛИДЕРОВ\\nПОКЕМОН-ГИМОВ.\\pТак ты получишь право сразиться...\\pС ЭЛИТНОЙ ЧЕТВЁРКОЙ\\nЛИГИ ПОКЕМОНОВ!$",
        "ViridianCity_School_Text_TurnThePage": "Перевернуть страницу?$",
        "ViridianCity_School_Text_HeyDontLookAtMyNotes": "ДЕВОЧКА: Эй!\\nНе смотри мои записи!$",
        "ViridianCity_School_Text_BlackboardListsStatusProblems": "На доске перечислены СТАТУСЫ,\\nвозникающие у ПОКЕМОНОВ в бою.$",
        "ViridianCity_School_Text_ReadWhichTopic": "Какую тему хочешь прочитать?$",
        "ViridianCity_School_Text_ExplainSleep": "Спящий ПОКЕМОН не может атаковать.\\pСон сохраняется даже\\nпосле окончания боя.\\pИспользуй AWAKENING,\\nчтобы разбудить ПОКЕМОНА.$",
        "ViridianCity_School_Text_ExplainBurn": "Ожог снижает АТАКУ.\\nТакже он постепенно отнимает HP.\\pОжог остаётся после боя.\\nИспользуй BURN HEAL для лечения.$",
        "ViridianCity_School_Text_ExplainPoison": "При отравлении здоровье ПОКЕМОНА\\nпостепенно уменьшается.\\pЯд остаётся после боя.\\nИспользуй ANTIDOTE для лечения!$",
        "ViridianCity_School_Text_ExplainFreeze": "Замороженный ПОКЕМОН\\nне может двигаться.\\pОн остаётся замороженным\\nдаже после боя.\\pИспользуй ICE HEAL,\\nчтобы отогреть ПОКЕМОНА.$",
        "ViridianCity_School_Text_ExplainParalysis": "Паралич снижает СКОРОСТЬ и может\\nпомешать ПОКЕМОНУ двигаться.\\pПаралич остаётся после боя.\\nИспользуй PARLYZ HEAL для лечения.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/Route5_PokemonDayCare_Frlg/scripts.inc": 15,
    "data/maps/VictoryRoad_2F_Frlg/scripts.inc": 15,
    "data/maps/ViridianCity_School_Frlg/scripts.inc": 15,
}
EXPECTED_TOTAL = 45


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

    audit = root / "build" / "qarro_ru_daycare_victory2_school_v3_112_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlockCount": EXPECTED_TOTAL,
        "translatedByFile": translated_by_file,
        "unusedJapaneseBlocksTouched": False,
        "physicalNewlinesInsideAsmStrings": False,
        "doubledRuntimeEscapes": False,
        "gameplayLogicTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; unused Japanese/gameplay/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
