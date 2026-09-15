#!/usr/bin/env python3
"""Qarro v3.111: localize remaining Pewter City and Vermilion Gym runtime text.

Translates exactly 32 English-only FireRed runtime blocks after v3.110:
  * PewterCity_Frlg: 16
  * VermilionCity_Gym_Frlg: 16
Existing Running Shoes, LT. Surge and Gym advice Russian scenes are preserved.
Pokemon species, Move and Ability proper names remain English by project canon.
Gameplay/trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_PEWTER_VERMILION_GYM_V3_111"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES = {
    "data/maps/PewterCity_Frlg/scripts.inc": {
        "PewterCity_Text_ClefairyCameFromMoon": "Говорят, CLEFAIRY прилетели с Луны.\\pОни появились после того, как\\nна ГОРУ МУН упали ЛУННЫЕ КАМНИ.$",
        "PewterCity_Text_BrockOnlySeriousTrainerHere": "Здесь не так много серьёзных\\nТРЕНЕРОВ ПОКЕМОНОВ.\\pВ основном тут ЛОВЦЫ ЖУКОВ -\\nдля них это просто хобби.\\pНо БРОК из ПЬЮТЕР-ГИМА\\nсовсем другой.$",
        "PewterCity_Text_DidYouCheckOutMuseum": "Ты уже был в МУЗЕЕ?$",
        "PewterCity_Text_WerentThoseFossilsAmazing": "Правда, окаменелости с ГОРЫ МУН\\nпотрясающие?$",
        "PewterCity_Text_ReallyYouHaveToGo": "Правда?\\nТы обязательно должен сходить!$",
        "PewterCity_Text_ThisIsTheMuseum": "Вот он, МУЗЕЙ.\\pЗа вход нужно заплатить, но оно\\nтого стоит. Ещё увидимся!$",
        "PewterCity_Text_DoYouKnowWhatImDoing": "Пс-с-с!\\nЗнаешь, чем я занимаюсь?$",
        "PewterCity_Text_ThatsRightItsHardWork": "Точно!\\nРабота непростая!$",
        "PewterCity_Text_SprayingRepelToKeepWildMonsOut": "Я распыляю REPEL, чтобы дикие\\nПОКЕМОНЫ не лезли в мой сад!$",
        "PewterCity_Text_BrocksLookingForChallengersFollowMe": "Ты ТРЕНЕР, верно?\\pБРОК ищет новых соперников.\\nИди за мной!$",
        "PewterCity_Text_GoTakeOnBrock": "Если уверен в себе,\\nиди и сразись с БРОКОМ!$",
        "PewterCity_Text_TrainerTipsEarningEXP": "СОВЕТЫ ТРЕНЕРУ\\pВсе ПОКЕМОНЫ, участвовавшие в бою,\\nдаже недолго, получают EXP.$",
        "PewterCity_Text_CallPoliceIfInfoOnThieves": "ВНИМАНИЕ!\\pВоры крадут окаменелости ПОКЕМОНОВ\\nс ГОРЫ МУН.\\pЕсли что-нибудь знаете, сообщите\\nв ПОЛИЦИЮ ПЬЮТЕРА.$",
        "PewterCity_Text_MuseumOfScience": "НАУЧНЫЙ МУЗЕЙ ПЬЮТЕРА$",
        "PewterCity_Text_GymSign": "ПЬЮТЕР-СИТИ ПОКЕМОН-ГИМ\\nЛИДЕР: БРОК\\lКаменно-крепкий ТРЕНЕР ПОКЕМОНОВ!$",
        "PewterCity_Text_CitySign": "ПЬЮТЕР-СИТИ\\nКаменно-серый город$",
    },
    "data/maps/VermilionCity_Gym_Frlg/scripts.inc": {
        "VermilionCity_Gym_Text_TuckerIntro": "Когда я служил в армии, LT. SURGE\\nбыл моим строгим командиром.\\pСпуску он никому не давал.$",
        "VermilionCity_Gym_Text_TuckerDefeat": "Стой!\\nТы очень хорош!$",
        "VermilionCity_Gym_Text_TuckerPostBattle": "Открыть ту дверь непросто.\\pLT. SURGE ещё в армии славился\\nсвоей осторожностью.$",
        "VermilionCity_Gym_Text_BailyIntro": "Я не тяжеловес, зато отлично\\nразбираюсь в электричестве!\\pПоэтому я и вступил в этот ГИМ.$",
        "VermilionCity_Gym_Text_BailyDefeat": "Поджарен!$",
        "VermilionCity_Gym_Text_BailyPostBattle": "Ладно, расскажу!\\pLT. SURGE сказал, что спрятал\\nпереключатели двери внутри чего-то.$",
        "VermilionCity_Gym_Text_DwayneIntro": "Детям здесь не место!\\nДаже если ты силён!$",
        "VermilionCity_Gym_Text_DwayneDefeat": "Ого!\\nВот это сюрприз!$",
        "VermilionCity_Gym_Text_DwaynePostBattle": "LT. SURGE сам установил\\nловушки в ГИМЕ.\\pОн везде поставил двойные замки.\\nДам тебе подсказку.\\pКогда откроешь первый замок,\\nвторой будет прямо рядом.$",
        "VermilionCity_Gym_Text_GymGuyPostVictory": "Фух!\\nВот это был электрический бой!$",
        "VermilionCity_Gym_Text_GymStatue": "ВЕРМИЛИОНСКИЙ ПОКЕМОН-ГИМ\\nЛИДЕР: LT. SURGE\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}$",
        "VermilionCity_Gym_Text_GymStatuePlayerWon": "ВЕРМИЛИОНСКИЙ ПОКЕМОН-ГИМ\\nЛИДЕР: LT. SURGE\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}, {PLAYER}$",
        "VermilionCity_Gym_Text_NopeOnlyTrashHere": "Нет!\\nЗдесь только мусор.$",
        "VermilionCity_Gym_Text_SwitchUnderTrashFirstLockOpened": "Эй! Под мусором переключатель!\\nВключай!\\pПервый электрический замок открыт!$",
        "VermilionCity_Gym_Text_SecondLockOpened": "Второй электрический замок открыт!\\nАвтоматическая дверь открылась!$",
        "VermilionCity_Gym_Text_OnlyTrashLocksWereReset": "Нет!\\nЗдесь только мусор.\\pЭй!\\nЭлектрические замки сбросились!$",
    },
}
EXPECTED_COUNTS = {
    "data/maps/PewterCity_Frlg/scripts.inc": 16,
    "data/maps/VermilionCity_Gym_Frlg/scripts.inc": 16,
}
EXPECTED_TOTAL = 32


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

    audit = root / "build" / "qarro_ru_pewter_vermilion_gym_v3_111_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlockCount": EXPECTED_TOTAL,
        "translatedByFile": translated_by_file,
        "physicalNewlinesInsideAsmStrings": False,
        "doubledRuntimeEscapes": False,
        "gameplayLogicTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; existing leader/RUNNING SHOES scenes preserved; gameplay/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
