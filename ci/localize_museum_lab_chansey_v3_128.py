#!/usr/bin/env python3
"""Qarro v3.128: localize Pewter Museum 2F, Cinnabar Lab entrance and Chansey Dance house.

Translates 23 safe FireRed runtime text blocks after v3.127:
  * PewterCity_Museum_2F_Frlg: 11 (7 audit-visible + 4 SEISMIC TOSS tutor blind-spot)
  * CinnabarIsland_PokemonLab_Entrance_Frlg: 6
  * SevenIsland_SevaultCanyon_House_Frlg: 6

SEISMIC TOSS remains English by Move-name canon. Tutor, fossil-state, heal/dance,
trainer, Pokemon/Move/Ability proper-name policy, and Ash Bond/Ash Cap logic
are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_MUSEUM_LAB_CHANSEY_V3_128"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/PewterCity_Museum_2F_Frlg/scripts.inc": {
        "Text_SeismicTossTeach": "Секреты космоса...\\nТайны земли...\\pМы так мало знаем\\nобо всём этом.\\pНо это должно заставлять нас\\nучиться усерднее, а не сдаваться.\\pБросать стоит только одно...\\pКак насчёт SEISMIC TOSS?\\nОбучить этой атаке ПОКЕМОНА?$",
        "Text_SeismicTossDeclined": "Вот как?\\nУверен, ты ещё вернёшься.$",
        "Text_SeismicTossWhichMon": "Какой ПОКЕМОН хочет выучить\\nSEISMIC TOSS?$",
        "Text_SeismicTossTaught": "Надеюсь, ты не сдашься.\\nПродолжай в том же духе.$",
        "PewterCity_Museum_1F_Text_WhatsSpecialAboutMoonStone": "MOON STONE, значит?\\pЧто в нём особенного?\\nПо мне, обычный камень.$",
        "PewterCity_Museum_1F_Text_BoughtColorTVForMoonLanding": "20 июля 1969 года!\\pВ тот день человек впервые\\nступил на Луну.\\pЯ купил цветной телевизор\\nспециально ради этой новости.$",
        "PewterCity_Museum_1F_Text_RunningSpaceExhibitThisMonth": "В этом месяце у нас проходит\\nвыставка о космосе.$",
        "PewterCity_Museum_1F_Text_AskedDaddyToCatchPikachu": "Я хочу PIKACHU!\\nОн такой милый!\\pЯ попросила папу поймать мне одного!$",
        "PewterCity_Museum_1F_Text_PikachuSoonIPromise": "Да, скоро будет PIKACHU, обещаю!$",
        "PewterCity_Museum_1F_Text_SpaceShuttle": "Космический шаттл$",
        "PewterCity_Museum_1F_Text_MeteoriteThatFellOnMtMoon": "Метеорит, упавший на MT. MOON.\\nСчитается, что это MOON STONE.$",
    },
    "data/maps/CinnabarIsland_PokemonLab_Entrance_Frlg/scripts.inc": {
        "CinnabarIsland_Gym_Text_PhotoOfBlaineAndFuji": "Это фотография BLAINE и\\nMR. FUJI.\\pОни стоят плечом к плечу\\nи широко улыбаются.$",
        "CinnabarIsland_PokemonLab_Entrance_Text_StudyMonsExtensively": "Мы каждый день тщательно\\nизучаем ПОКЕМОНОВ.\\pЛюди часто приносят нам редких\\nПОКЕМОНОВ для исследования.$",
        "CinnabarIsland_PokemonLab_Entrance_Text_PhotoOfLabFounderDrFuji": "Фотография основателя ЛАБОРАТОРИИ...\\nDR. FUJI?!$",
        "CinnabarIsland_PokemonLab_Entrance_Text_MeetingRoomSign": "ЛАБОРАТОРИЯ ПОКЕМОНОВ\\nКомната совещаний$",
        "CinnabarIsland_PokemonLab_Entrance_Text_RAndDRoomSign": "ЛАБОРАТОРИЯ ПОКЕМОНОВ\\nОтдел исследований$",
        "CinnabarIsland_PokemonLab_Entrance_Text_TestingRoomSign": "ЛАБОРАТОРИЯ ПОКЕМОНОВ\\nИспытательная комната$",
    },
    "data/maps/SevenIsland_SevaultCanyon_House_Frlg/scripts.inc": {
        "SevenIsland_SevaultCanyon_House_Text_ChanseyDanceJoinIn": "Танцуй, танцуй!\\nТанец CHANSEY!\\pТы тоже присоединяйся!\\nТанцуй, танцуй!$",
        "SevenIsland_SevaultCanyon_House_Text_WouldYouLikeToDance": "Хочешь потанцевать?$",
        "SevenIsland_SevaultCanyon_House_Text_ComeOnDance": "Ну же, танцуй!$",
        "SevenIsland_SevaultCanyon_House_Text_DancedChanseyDance": "{PLAYER} исполнил танец CHANSEY!$",
        "SevenIsland_SevaultCanyon_House_Text_YoureAllChipperNow": "Ахахахаха!\\pВот теперь ты снова бодр!\\nПовезло!$",
        "SevenIsland_SevaultCanyon_House_Text_Chansey": "CHANSEY: Чанси! Чанси!$",
    },
}
EXPECTED_TOTAL = 23


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
        "auditVisibleBlocks": 19,
        "blindSpotBlocks": 4,
        "byFile": by_file,
        "protected": [
            "Pokemon species names remain English",
            "Move names remain English, including SEISMIC TOSS",
            "Ability names remain English",
            "SEISMIC TOSS tutor logic untouched",
            "Cinnabar fossil state logic untouched",
            "Chansey Dance healing and event logic untouched",
            "Trainer data untouched",
            "Ash Bond/Ash Cap untouched",
        ],
    }
    out = root / "build" / "qarro_ru_museum_lab_chansey_v3_128_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {total} runtime blocks (19 audit-visible + 4 tutor blind-spot); tutor/heal/event/trainer/Ash logic untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
