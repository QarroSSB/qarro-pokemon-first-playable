#!/usr/bin/env python3
"""Qarro v3.117: localize Celadon Hotel/Restaurant and Ember Spa runtime text.

Translates exactly 20 English-only FireRed runtime blocks after v3.116:
  * CeladonCity_Hotel_Frlg: 4
  * CeladonCity_Restaurant_Frlg: 8
  * OneIsland_KindleRoad_EmberSpa_Frlg: 8

Pokemon species, Move and Ability proper names remain English by project canon.
Coin Case/HM06/healing/event logic, trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_CELADON_SERVICE_EMBER_SPA_V3_117"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/CeladonCity_Hotel_Frlg/scripts.inc": {
        "CeladonCity_Hotel_Text_ThisHotelIsForPeople": "ПОКЕМОНЫ?\\nНет, это отель для людей.\\pК сожалению, свободных мест нет.$",
        "CeladonCity_Hotel_Text_OnVacationWithBrotherAndBoyfriend": "Я отдыхаю с братом и парнем.\\pСЕЛАДОН - такой красивый город!$",
        "CeladonCity_Hotel_Text_WhyDidSheBringBrother": "Почему?\\nЗачем она взяла с собой брата?$",
        "CeladonCity_Hotel_Text_SisBroughtMeOnVacation": "Ура! Я на отдыхе!\\nСестра взяла меня с собой! Круто!$",
    },
    "data/maps/CeladonCity_Restaurant_Frlg/scripts.inc": {
        "CeladonCity_Restaurant_Text_TakingBreakRightNow": "Привет!\\pИзвини, сейчас у нас перерыв.$",
        "CeladonCity_Restaurant_Text_OftenGoToDrugstore": "Мои ПОКЕМОНЫ слабые, поэтому мне\\nчасто приходится ходить в АПТЕКУ.$",
        "CeladonCity_Restaurant_Text_PsstBasementUnderGameCorner": "Псс! Говорят, под ИГРОВЫМ УГОЛКОМ\\nесть подвал.$",
        "CeladonCity_Restaurant_Text_ManLostItAllAtSlots": "Ням...\\pТот мужчина за столом всё проиграл\\nв автоматах.$",
        "CeladonCity_Restaurant_Text_TakeThisImBusted": "Смейся, смейся!\\nЯ разорён!\\pБольше никаких автоматов!\\nЗавязал!\\pВот!\\nМне это больше не понадобится!$",
        "CeladonCity_Restaurant_Text_ReceivedCoinCaseFromMan": "{PLAYER} получил COIN CASE\\nот мужчины.$",
        "CeladonCity_Restaurant_Text_MakeRoomForThis": "Освободи для этого место!$",
        "CeladonCity_Restaurant_Text_ThoughtIdWinItBack": "Я всё думал, что сумею\\nотыграться...$",
    },
    "data/maps/OneIsland_KindleRoad_EmberSpa_Frlg/scripts.inc": {
        "OneIsland_KindleRoad_EmberSpa_Text_WaterWarmsMeToCore": "Хм!\\nА-а-а-а-а-а!\\pАх! Вот это рай!\\nВода прогревает до самых костей!\\pТебе тоже стоит окунуться.\\pИди в центр, расслабься\\nи как следует согрейся!$",
        "OneIsland_KindleRoad_EmberSpa_Text_EnjoyBowlOfChowder": "Лучшее после купания\\nначинается потом.\\pЛюблю съесть тарелку похлёбки,\\nчтобы согреться ещё и изнутри!$",
        "OneIsland_KindleRoad_EmberSpa_Text_WaterExquisiteFullyRefreshed": "Вода идеально тёплая.\\nКак же приятно...\\p{PLAYER} и ПОКЕМОНЫ\\nполностью восстановились!$",
        "OneIsland_KindleRoad_EmberSpa_Text_HotSpringIsTherapeutic": "Говорят, купание в горячем\\nисточнике полезно для здоровья.$",
        "OneIsland_KindleRoad_EmberSpa_Text_SeeHowSmoothMySkinIs": "Посмотри на моё лицо.\\nВидишь, какая гладкая кожа?\\pВода горячего источника\\nсохраняет её моложе моих лет.$",
        "OneIsland_KindleRoad_EmberSpa_Text_BrunoVisitsSpaOnOccasion": "После честной тренировки ничто не\\nсравнится с отдыхом в горячем\\lисточнике.\\pBRUNO, мой старший товарищ,\\nиногда бывает в СПА.\\pОн восстанавливается после травм -\\nи своих, и своих ПОКЕМОНОВ.$",
        "OneIsland_KindleRoad_EmberSpa_Text_UsedThisToMakeEmberSpa": "Горячие источники всегда рядом\\nс вулканами.\\pСПА ЭМБЕР здесь...\\nЯ построил его много лет назад.\\pЯ собственными руками вырубил\\nбассейн в огромной скале.\\pТогда я пользовался вот этим.\\nПожалуй, могу отдать тебе.$",
        "OneIsland_KindleRoad_EmberSpa_Text_ExplainHM06": "Этим можно разбивать валуны,\\nсловно они из сухарей.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/CeladonCity_Hotel_Frlg/scripts.inc": 4,
    "data/maps/CeladonCity_Restaurant_Frlg/scripts.inc": 8,
    "data/maps/OneIsland_KindleRoad_EmberSpa_Frlg/scripts.inc": 8,
}
EXPECTED_TOTAL = 20


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

    audit = root / "build" / "qarro_ru_celadon_service_ember_spa_v3_117_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlockCount": EXPECTED_TOTAL,
        "translatedByFile": translated_by_file,
        "coinCaseLogicTouched": False,
        "hm06LogicTouched": False,
        "healLogicTouched": False,
        "eventLogicTouched": False,
        "trainerDataTouched": False,
        "pokemonMoveAbilityNamesPolicy": "English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; "
        "Coin Case/HM06/heal/event/trainer/Ash logic untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
