#!/usr/bin/env python3
"""Qarro v3.55 mandatory Professor Oak National Dex scene localization.

Translates only the verified forced Pallet Town Professor Oak's Lab scene that
runs after Oak's post-Elite Four rating reaches the National Dex threshold.
Optional lab NPC dialogue and later Sevii/Ruby/Sapphire progression remain
untouched. Pokemon species / move / ability proper names remain English.
Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_PALLET_OAK_NATIONAL_DEX_V3_55"
REL = Path("data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc")

PATCHES = {
    "PalletTown_ProfessorOaksLab_Text_OakSightingsOfRareMons": {
        "needles": ("sightings", "never been seen in KANTO", "go in my place"),
        "ru": '''PalletTown_ProfessorOaksLab_Text_OakSightingsOfRareMons::
\t.string "Недавно стали замечать много\\n"
\t.string "редких видов POKeMON.\\p"
\t.string "Таких POKeMON раньше никогда\\n"
\t.string "не видели в KANTO.\\p"
\t.string "Я бы сам отправился посмотреть,\\n"
\t.string "но для этого я уже слишком стар.\\p"
\t.string "Поэтому, {PLAYER}, прошу тебя\\n"
\t.string "отправиться вместо меня.$"
''',
    },
    "PalletTown_ProfessorOaksLab_Text_RivalJustLetMeHandleEverything": {
        "needles": ("Hey, I heard that!", "favoring", "let me handle"),
        "ru": '''PalletTown_ProfessorOaksLab_Text_RivalJustLetMeHandleEverything::
\t.string "{RIVAL}: Эй, я всё слышал!\\p"
\t.string "Дед, почему ты всё время\\n"
\t.string "предпочитаешь {PLAYER}?\\p"
\t.string "Я собрал больше POKeMON,\\n"
\t.string "да ещё и быстрее.\\p"
\t.string "Просто доверь всё мне.$"
''',
    },
    "PalletTown_ProfessorOaksLab_Text_OakNeedYourHelpTooNeedToSeePokedexes": {
        "needles": ("Of course I need your help", "both your", "POKéDEXES"),
        "ru": '''PalletTown_ProfessorOaksLab_Text_OakNeedYourHelpTooNeedToSeePokedexes::
\t.string "OAK: Знаю, знаю.\\n"
\t.string "Твоя помощь мне тоже нужна.\\p"
\t.string "А теперь мне нужны оба ваших\\n"
\t.string "POKeDEX.$"
''',
    },
    "PalletTown_ProfessorOaksLab_Text_OakTookBothPokedexUnits": {
        "needles": ("PROF. OAK took both", "POKéDEX", "units"),
        "ru": '''PalletTown_ProfessorOaksLab_Text_OakTookBothPokedexUnits::
\t.string "PROF. OAK взял оба\\n"
\t.string "POKeDEX.$"
''',
    },
    "PalletTown_ProfessorOaksLab_Text_OakNowTheseUnitsCanRecordMoreData": {
        "needles": ("And that's done!", "record data", "a lot more"),
        "ru": '''PalletTown_ProfessorOaksLab_Text_OakNowTheseUnitsCanRecordMoreData::
\t.string "… … …  … … …\\p"
\t.string "… … …  … … …\\p"
\t.string "…Готово!\\p"
\t.string "Теперь эти устройства могут\\n"
\t.string "записывать намного больше данных.$"
''',
    },
    "PalletTown_ProfessorOaksLab_Text_PlayersPokedexWasUpgraded": {
        "needles": ("{PLAYER}'s", "POKéDEX was upgraded"),
        "ru": '''PalletTown_ProfessorOaksLab_Text_PlayersPokedexWasUpgraded::
\t.string "POKeDEX {PLAYER} был улучшен!$"
''',
    },
    "PalletTown_ProfessorOaksLab_Text_OakMustReallyWorkToFillPokedex": {
        "needles": ("really must work", "filling your", "monumentally great"),
        "ru": '''PalletTown_ProfessorOaksLab_Text_OakMustReallyWorkToFillPokedex::
\t.string "Теперь, {PLAYER} и {RIVAL}!\\p"
\t.string "На этот раз вы должны всерьёз\\n"
\t.string "заняться заполнением POKeDEX.\\p"
\t.string "Сделайте их лучшими и самыми\\n"
\t.string "полными за всю историю!\\p"
\t.string "Это поистине великое дело\\n"
\t.string "в истории POKeMON!$"
''',
    },
    "PalletTown_ProfessorOaksLab_Text_RivalIllCompleteThePokedex": {
        "needles": ("Gramps, calm down", "POKéDEX completed", "ONE ISLAND"),
        "ru": '''PalletTown_ProfessorOaksLab_Text_RivalIllCompleteThePokedex::
\t.string "{RIVAL}: Дед, успокойся.\\n"
\t.string "Не волнуйся так.\\p"
\t.string "Я заполню POKeDEX,\\n"
\t.string "можешь не переживать.\\p"
\t.string "Для начала загляну\\n"
\t.string "на ONE ISLAND…\\p"
\t.string "Ладно, я пошёл!$"
''',
    },
}

LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")


def replace_label_block(text: str, label: str, needles: tuple[str, ...], replacement: str) -> str:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    block = text[start:end]
    missing = [needle for needle in needles if needle not in block]
    if missing:
        raise SystemExit(f"{MARKER}: {label}: pinned evidence mismatch; missing {missing}")
    if re.search(r"[А-Яа-яЁё]", block):
        raise SystemExit(f"{MARKER}: {label}: block is already localized or unexpectedly contains Cyrillic")
    return text[:start] + replacement + "\n" + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pallet_oak_national_dex_v3_55.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_pallet_oak_national_dex_v3_55_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Professor Oak National Dex upgrade scene after Pallet rating threshold",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} National Dex scene blocks; Ash Bond/Ash Cap untouched")

    next_script = Path(__file__).with_name("localize_one_island_celio_ruby_request_v3_56.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
