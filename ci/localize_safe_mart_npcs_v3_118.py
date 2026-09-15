#!/usr/bin/env python3
"""Qarro v3.118: localize safe residual Mart NPC runtime text.

Translates exactly 19 English-only FireRed runtime blocks after v3.117:
  * CeruleanCity_Mart_Frlg: 2
  * PewterCity_Mart_Frlg: 2
  * SaffronCity_Mart_Frlg: 2
  * ThreeIsland_Mart_Frlg: 3
  * SevenIsland_Mart_Frlg: 3
  * CinnabarIsland_Mart_Frlg: 2
  * FuchsiaCity_Mart_Frlg: 2
  * LavenderTown_Mart_Frlg: 3

Pokemon species, Move and Ability proper names remain English by project canon.
Pokemart inventories/clerk logic, unused Japanese text, trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_SAFE_MART_NPCS_V3_118"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/CeruleanCity_Mart_Frlg/scripts.inc": {
        "CeruleanCity_Mart_Text_RepelWorksOnWeakMons": "REPEL отпугивает не только насекомых,\\nно и слабых ПОКЕМОНОВ.\\pПоставь самого сильного ПОКЕМОНА\\nпервым в списке.\\pЧем сильнее первый ПОКЕМОН,\\nтем полезнее будет REPEL.$",
        "CeruleanCity_Mart_Text_DoYouKnowAboutRareCandy": "Знаешь про RARE CANDY?\\nВ магазинах их не продают.\\pКажется, от них ПОКЕМОН\\nочень быстро растёт.$",
    },
    "data/maps/PewterCity_Mart_Frlg/scripts.inc": {
        "PewterCity_Mart_Text_BoughtWeirdFishFromShadyGuy": "Какой-то подозрительный старик\\nуговорил меня купить странного\\lрыбного ПОКЕМОНА!\\pОн совсем слабый, а стоил ¥500!$",
        "PewterCity_Mart_Text_GoodThingsIfRaiseMonsDiligently": "Если старательно растить ПОКЕМОНОВ,\\nслучаются хорошие вещи.\\pДаже слабые могут удивить,\\nесли не бросать их.$",
    },
    "data/maps/SaffronCity_Mart_Frlg/scripts.inc": {
        "SaffronCity_Mart_Text_MaxRepelMoreEffectiveThanSuper": "MAX REPEL не даёт слабым ПОКЕМОНАМ\\nпоявляться.\\pMAX REPEL действует дольше,\\nчем SUPER REPEL.$",
        "SaffronCity_Mart_Text_ReviveIsCostly": "REVIVE стоит дорого, но возвращает\\nв строй потерявшего сознание ПОКЕМОНА!$",
    },
    "data/maps/ThreeIsland_Mart_Frlg/scripts.inc": {
        "ThreeIsland_Mart_Text_TrueThatCeldadonDeptStoreBigger": "Правда?\\pУНИВЕРМАГ СЕЛАДОНА в несколько раз\\nбольше этого магазина?$",
        "ThreeIsland_Mart_Text_PeopleHealWithBerriesFromForest": "Иногда я покупаю здесь лекарства.\\pНо многие лечат ПОКЕМОНОВ ЯГОДАМИ\\nиз ЯГОДНОГО ЛЕСА.\\pВедь ЯГОДЫ бесплатны\\nи никогда не заканчиваются.$",
        "ThreeIsland_Mart_Text_BikersWereAboutToTrashMart": "Эти БАЙКЕРЫ чуть не разгромили\\nэтот МАГАЗИН ПОКЕМОНОВ.\\pХорошо, что они решили уйти!$",
    },
    "data/maps/SevenIsland_Mart_Frlg/scripts.inc": {
        "SevenIsland_Mart_Text_MonHavePersonalitiesOfTheirOwn": "У ПОКЕМОНОВ есть свой характер,\\nкак и у людей.\\pУ моего PIKACHU натура HASTY,\\nпоэтому он вырос очень быстрым.$",
        "SevenIsland_Mart_Text_PreparationsCompleteForRuins": "Так, приготовления закончены.\\nМожно отправляться исследовать РУИНЫ.$",
        "SevenIsland_Mart_Text_NeedToFishOnSevenIsland": "Мне осталось порыбачить на\\nСЕДЬМОМ ОСТРОВЕ.\\pТогда мой рыболовный тур по\\nОСТРОВАМ СЕВИИ будет завершён.\\pНо сначала надо запастись\\nPOKe BALLS.$",
    },
    "data/maps/CinnabarIsland_Mart_Frlg/scripts.inc": {
        "CinnabarIsland_Mart_Text_DontTheyHaveXAttack": "У них нет X ATTACK?\\pМне он нравится: в бою\\nон повышает параметр ATTACK.$",
        "CinnabarIsland_Mart_Text_ExtraItemsNeverHurt": "Лишние предметы не помешают.\\nНикогда не знаешь, что случится.$",
    },
    "data/maps/FuchsiaCity_Mart_Frlg/scripts.inc": {
        "FuchsiaCity_Mart_Text_DontTheyHaveSafariZonePennants": "У них нет вымпелов с рекламой\\nЗОНЫ САФАРИ?\\pА бумажных фонариков?\\nДаже календарей нет?$",
        "FuchsiaCity_Mart_Text_DidYouTryXSpeed": "Пробовал X SPEED?\\nВ бою он ускоряет ПОКЕМОНА.$",
    },
    "data/maps/LavenderTown_Mart_Frlg/scripts.inc": {
        "LavenderTown_Mart_Text_SearchingForStatRaiseItems": "Я ищу предметы, которые повышают\\nпараметры ПОКЕМОНОВ.\\pОни действуют в течение\\nодного боя.\\pМне нужны X ATTACK, X DEFEND,\\nX SPEED и X SPECIAL.\\pЗнаешь, где их достать?$",
        "LavenderTown_Mart_Text_DidYouBuyRevives": "Купил REVIVE?\\nОн возвращает в строй ПОКЕМОНА,\\lпотерявшего сознание!$",
        "LavenderTown_Mart_Text_TrainerDuosCanChallengeYou": "Иногда пара ТРЕНЕРОВ вызывает тебя\\nна бой сразу двумя ПОКЕМОНАМИ.\\pТогда и тебе нужно выпустить\\nсразу двух ПОКЕМОНОВ.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/CeruleanCity_Mart_Frlg/scripts.inc": 2,
    "data/maps/PewterCity_Mart_Frlg/scripts.inc": 2,
    "data/maps/SaffronCity_Mart_Frlg/scripts.inc": 2,
    "data/maps/ThreeIsland_Mart_Frlg/scripts.inc": 3,
    "data/maps/SevenIsland_Mart_Frlg/scripts.inc": 3,
    "data/maps/CinnabarIsland_Mart_Frlg/scripts.inc": 2,
    "data/maps/FuchsiaCity_Mart_Frlg/scripts.inc": 2,
    "data/maps/LavenderTown_Mart_Frlg/scripts.inc": 3,
}
EXPECTED_TOTAL = 19


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

    audit = root / "build" / "qarro_ru_safe_mart_npcs_v3_118_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlockCount": EXPECTED_TOTAL,
        "translatedByFile": translated_by_file,
        "pokemartInventoryTouched": False,
        "pokemartClerkLogicTouched": False,
        "unusedJapaneseTextTouched": False,
        "trainerDataTouched": False,
        "pokemonMoveAbilityNamesPolicy": "English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} Mart NPC runtime blocks; "
        "inventories/clerk/unused-Japanese/trainer/Ash logic untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
