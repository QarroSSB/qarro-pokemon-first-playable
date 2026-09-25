#!/usr/bin/env python3
"""Qarro v3.126: localize Lavender volunteer house, Move Deleter and Heracross size house.

Translates exactly 27 English-only FireRed runtime text blocks after v3.125:
  * LavenderTown_VolunteerPokemonHouse_Frlg: 9
  * FuchsiaCity_House3_Frlg: 8
  * SixIsland_WaterPath_House1_Frlg: 10

Poke Flute reward flow, move-deletion logic, Heracross size/reward logic,
trainer data, Pokemon/Move/Ability proper-name policy, and Ash Bond/Ash Cap
are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_LAVENDER_MOVE_DELETER_HERACROSS_V3_126"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/LavenderTown_VolunteerPokemonHouse_Frlg/scripts.inc": {
        "LavenderTown_PokemonCenter_1F_Text_HearMrFujiNotFromAroundHere": "Я недавно переехал в этот город.\\pГоворят, MR. FUJI тоже\\nне местный.$",
        "LavenderTown_VolunteerPokemonHouse_Text_WhereDidMrFujiGo": "Странно, MR. FUJI здесь нет.\\nКуда же он ушёл?$",
        "LavenderTown_VolunteerPokemonHouse_Text_MrFujiWasPrayingForCubonesMother": "MR. FUJI молился в одиночестве\\nза мать CUBONE.$",
        "LavenderTown_VolunteerPokemonHouse_Text_MrFujiLooksAfterOrphanedMons": "Вообще-то это дом MR. FUJI.\\pОн очень добрый.\\pОн заботится о брошенных\\nи осиротевших ПОКЕМОНАХ.$",
        "LavenderTown_VolunteerPokemonHouse_Text_MonsNiceToHug": "Как тепло!\\nПОКЕМОНОВ так приятно обнимать.$",
        "LavenderTown_VolunteerPokemonHouse_Text_Nidorino": "NIDORINO: Га-оо!$",
        "LavenderTown_VolunteerPokemonHouse_Text_Psyduck": "PSYDUCK: Кваппа!$",
        "LavenderTown_VolunteerPokemonHouse_Text_GrandPrizeDrawingClipped": "ЖУРНАЛ ФАНАТОВ ПОКЕМОНОВ\\nЕжемесячный розыгрыш приза!\\pБланк заявки...\\pИсчез! Его вырезали.\\nКто-то уже подал заявку.$",
        "LavenderTown_VolunteerPokemonHouse_Text_PokemonMagazinesLineShelf": "На полке журналы о ПОКЕМОНАХ.\\pPOKEMON INSIDER...\\pPOKEMON FAN...$",
    },
    "data/maps/FuchsiaCity_House3_Frlg/scripts.inc": {
        "FuchsiaCity_House3_Text_WouldYouLikeToForgetMove": "Эм...\\nДа, я УДАЛЯЮ АТАКИ.\\pЯ могу заставить ПОКЕМОНА\\nзабыть атаку.\\pХотите, чтобы я это сделал?$",
        "FuchsiaCity_House3_Text_WhichMonShouldForgetMove": "Какой ПОКЕМОН должен\\nзабыть атаку?$",
        "FuchsiaCity_House3_Text_WhichMoveShouldBeForgotten": "Какую атаку нужно забыть?$",
        "FuchsiaCity_House3_Text_MonOnlyKnowsOneMove": "{STR_VAR_1}, похоже, знает только\\nодну атаку...$",
        "FuchsiaCity_House3_Text_MonsMoveShouldBeForgotten": "Хм! У {STR_VAR_1} атака {STR_VAR_2}?\\nЕё нужно забыть?$",
        "FuchsiaCity_House3_Text_MonHasForgottenMoveCompletely": "Идеально!\\p{STR_VAR_1} полностью забыл\\n{STR_VAR_2}.$",
        "FuchsiaCity_House3_Text_ComeAgainToForgetOtherMoves": "Приходите снова, если нужно\\nзабыть другие атаки.$",
        "FuchsiaCity_House3_Text_NoEggShouldKnowMoves": "Что?\\nЯЙЦО не должно знать атак.$",
    },
    "data/maps/SixIsland_WaterPath_House1_Frlg/scripts.inc": {
        "SixIsland_WaterPath_House1_Text_LoveItNeedItHeracross": "Hera, hera, HERACROSS!\\nБольшой и блестящий - король жуков!\\lОбожаю HERACROSS!$",
        "SixIsland_WaterPath_House1_Text_MayIMeasureHeracross": "А-а-а!\\nЭто HERACROSS!\\pПожалуйста, можно измерить,\\nкакой он большой?$",
        "SixIsland_WaterPath_House1_Text_ItsXSizeDeserveReward": "Ого, его размер {STR_VAR_2}!\\nТакого я ещё не видела!\\lТы заслужил награду!$",
        "SixIsland_WaterPath_House1_Text_WantToSeeBiggerOne": "Хочу увидеть HERACROSS\\nещё гораздо крупнее этого.\\pАх, как же я обожаю\\nогромных HERACROSS!$",
        "SixIsland_WaterPath_House1_Text_ItsXSizeSameAsBefore": "А? Размер {STR_VAR_2}...\\nЭх! Такой же, как раньше.$",
        "SixIsland_WaterPath_House1_Text_ItsXSizeYSizeWasBiggest": "Всего {STR_VAR_2}.\\nПрошлый HERACROSS был крупнее.\\pОн был {STR_VAR_3} - самый большой\\nHERACROSS, которого ты приносил.$",
        "SixIsland_WaterPath_House1_Text_ThisWontDo": "О нет! Так не пойдёт!\\pHERACROSS выглядит куда мощнее,\\nи у него прекрасный рог!$",
        "SixIsland_WaterPath_House1_Text_YourBagIsFull": "СУМКА заполнена.\\nМоя награда не поместится.$",
        "SixIsland_WaterPath_House1_Text_BiggestHeracrossIsXSize": "Самый большой HERACROSS,\\nкоторого я видела, был размером:\\p{STR_VAR_3}!$",
        "SixIsland_WaterPath_House1_Text_BlankChartOfSomeSort": "Это какая-то пустая таблица.\\pЗдесь есть места для записи\\nкаких-то рекордов.$",
    },
}
EXPECTED_TOTAL = 27


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def validate_translation(label: str, tr: str) -> None:
    if not tr.endswith("$"):
        die(f"{label}: must end with $")
    if "\n" in tr or "\r" in tr:
        die(f"{label}: physical newline")
    if any(ch in tr for ch in ("—", "–", "“", "”", "’", "…", "«", "»")):
        die(f"{label}: unsupported punctuation")
    if "\\\\" in tr:
        die(f"{label}: doubled runtime backslash")
    if not re.search(r"[А-Яа-яЁё]", tr):
        die(f"{label}: expected Cyrillic")


def block_bounds(text: str, label: str):
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected one label, got {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def replace_block(text: str, label: str, tr: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: already Cyrillic")
    if ".string " not in old:
        die(f"{label}: not text block")
    safe = tr.replace('"', '\\"')
    return text[:start] + f'{label}::\n\t.string "{safe}"\n\n' + text[end:]


def validate_written(rel: Path, text: str) -> None:
    for n, line in enumerate(text.splitlines(), 1):
        if '.string "' in line and line.count('"') < 2:
            die(f"{rel}:{n}: broken string")
    if re.search(r"\\\\[npl]", text):
        die(f"{rel}: doubled runtime escape")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    total = 0
    by_file = {}
    for rel_s, patches in FILES.items():
        path = root / rel_s
        if not path.is_file():
            die(f"missing target: {rel_s}")
        text = path.read_text(encoding="utf-8")
        for label, tr in patches.items():
            validate_translation(label, tr)
            text = replace_block(text, label, tr)
        validate_written(Path(rel_s), text)
        path.write_text(text, encoding="utf-8")
        by_file[rel_s] = len(patches)
        total += len(patches)

    if total != EXPECTED_TOTAL:
        die(f"expected {EXPECTED_TOTAL} blocks, got {total}")

    audit = {
        "marker": MARKER,
        "localizedBlocks": total,
        "byFile": by_file,
        "protected": [
            "Pokemon species names remain English",
            "Move names remain English",
            "Ability names remain English",
            "Poke Flute reward logic untouched",
            "Move Deleter logic untouched",
            "Heracross size and Nest Ball reward logic untouched",
            "Trainer data untouched",
            "Ash Bond/Ash Cap untouched",
        ],
    }
    out = root / "build" / "qarro_ru_lavender_move_deleter_heracross_v3_126_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {total} runtime blocks; reward/move/size/trainer/Ash logic untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
