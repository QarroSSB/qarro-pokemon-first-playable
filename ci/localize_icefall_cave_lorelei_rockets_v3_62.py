#!/usr/bin/env python3
"""Qarro v3.62 mandatory Icefall Cave Lorelei / Team Rocket localization.

Translates only the verified forced Lorelei/Rocket progression scene in the back
room of Four Island's Icefall Cave. The scene includes the required Rocket Grunt
battle and the Rocket Warehouse/Five Island reveal. Optional NPC text, later
Rocket Warehouse/Sapphire progression, Ash Bond, and Ash Cap remain untouched.
Pokemon species / move / ability proper names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ICEFALL_LORELEI_ROCKETS_V3_62"
REL = Path("data/maps/FourIsland_IcefallCave_Back_Frlg/scripts.inc")

PATCHES = {
    "FourIsland_IcefallCave_Back_Text_LoreleiKeepHandsOffMons": {
        "needles": ("LORELEI: Keep your filthy hands", "off the POKéMON in the cave", "answer to"),
        "ru": '''FourIsland_IcefallCave_Back_Text_LoreleiKeepHandsOffMons::
\t.string "LORELEI: Уберите свои грязные\\n"
\t.string "руки от ПОКЕМОНОВ в пещере!\\p"
\t.string "Делайте, что я сказала, иначе\\n"
\t.string "будете иметь дело со мной!$"
''',
    },
    "FourIsland_IcefallCave_Back_Text_ShutItLadyLeaveUsBe": {
        "needles": ("shut it, lady", "leave", "us be", "glasses get all", "steamed up"),
        "ru": '''FourIsland_IcefallCave_Back_Text_ShutItLadyLeaveUsBe::
\t.string "Да заткнись ты, дамочка,\\n"
\t.string "и оставь нас в покое.\\p"
\t.string "Смотри, как бы очки от злости\\n"
\t.string "не запотели!$"
''',
    },
    "FourIsland_IcefallCave_Back_Text_LoreleiPlayerHelpMeKickPoachersOut": {
        "needles": ("LORELEI: {PLAYER}", "catch up later", "need your help", "poachers", "selling them off", "You take that one"),
        "ru": '''FourIsland_IcefallCave_Back_Text_LoreleiPlayerHelpMeKickPoachersOut::
\t.string "LORELEI: {PLAYER}?!\\n"
\t.string "Что ты здесь делаешь?\\p"
\t.string "Нет, поговорим потом.\\n"
\t.string "Сейчас мне нужна твоя помощь.\\p"
\t.string "Помоги выгнать этих браконьеров,\\n"
\t.string "пока они не натворили ещё бед.\\p"
\t.string "Они ловят здесь ПОКЕМОНОВ,\\n"
\t.string "а потом продают их!\\p"
\t.string "Готов?\\n"
\t.string "Возьми на себя вот этого!$"
''',
    },
    "FourIsland_IcefallCave_Back_Text_GruntIntro": {
        "needles": ("W-what", "Who says we can't", "POKéMON we catch"),
        "ru": '''FourIsland_IcefallCave_Back_Text_GruntIntro::
\t.string "Ч-что?!\\p"
\t.string "Кто сказал, что мы не можем\\n"
\t.string "делать с пойманными ПОКЕМОНАМИ\\n"
\t.string "всё, что захотим?$"
''',
    },
    "FourIsland_IcefallCave_Back_Text_GruntDefeat": {
        "needles": ("We didn't plan on this",),
        "ru": '''FourIsland_IcefallCave_Back_Text_GruntDefeat::
\t.string "Такого мы не планировали!$"
''',
    },
    "FourIsland_IcefallCave_Back_Text_LoreleiWhereHaveYouTakenMons": {
        "needles": ("So despicably weak", "Where have you taken", "captured", "smashing your ring"),
        "ru": '''FourIsland_IcefallCave_Back_Text_LoreleiWhereHaveYouTakenMons::
\t.string "LORELEI: Хм.\\n"
\t.string "До чего же вы жалкие слабаки.\\p"
\t.string "Ты!\\n"
\t.string "Отвечай!\\p"
\t.string "Куда вы увезли пойманных\\n"
\t.string "ПОКЕМОНОВ?\\p"
\t.string "Я разнесу вашу шайку\\n"
\t.string "раз и навсегда!$"
''',
    },
    "FourIsland_IcefallCave_Back_Text_NotTellingYouThat": {
        "needles": ("N-no way", "not telling you"),
        "ru": '''FourIsland_IcefallCave_Back_Text_NotTellingYouThat::
\t.string "Н-ни за что!\\n"
\t.string "Я тебе не скажу!$"
''',
    },
    "FourIsland_IcefallCave_Back_Text_LoreleiWellDeepFreezeYou": {
        "needles": ("If you won't confess", "deep-freeze you", "LAPRAS", "ICE BEAM"),
        "ru": '''FourIsland_IcefallCave_Back_Text_LoreleiWellDeepFreezeYou::
\t.string "LORELEI: Не хочешь говорить -\\n"
\t.string "мы тебя заморозим.\\p"
\t.string "Мой LAPRAS в ярости из-за того,\\n"
\t.string "что вы сделали с его друзьями.\\p"
\t.string "Вперёд, LAPRAS!\\n"
\t.string "ICE BEAM...$"
''',
    },
    "FourIsland_IcefallCave_Back_Text_OkayRocketWareHouseFiveIsland": {
        "needles": ("I'll talk", "ROCKET", "WAREHOUSE on FIVE ISLAND", "ever make it", "ROCKET WAREHOUSE"),
        "ru": '''FourIsland_IcefallCave_Back_Text_OkayRocketWareHouseFiveIsland::
\t.string "А-а-а! Ладно!\\n"
\t.string "Я всё скажу!\\p"
\t.string "ПОКЕМОНЫ на СКЛАДЕ ROCKET\\n"
\t.string "на ПЯТОМ ОСТРОВЕ.\\p"
\t.string "Вот! Я сказал!\\n"
\t.string "А теперь мы уходим!\\p"
\t.string "...Но вряд ли вы вообще сможете\\n"
\t.string "попасть на СКЛАД ROCKET!\\p"
\t.string "Хе-хе-хе!$"
''',
    },
    "FourIsland_IcefallCave_Back_Text_ThankYouThisIsAwful": {
        "needles": ("{PLAYER}, thank you", "born and raised here", "these islands", "horrible", "criminals"),
        "ru": '''FourIsland_IcefallCave_Back_Text_ThankYouThisIsAwful::
\t.string "{PLAYER}, спасибо.\\n"
\t.string "Но это ужасно...\\p"
\t.string "Я родилась и выросла здесь,\\n"
\t.string "на этих островах.\\p"
\t.string "Я и не знала, что здесь\\n"
\t.string "орудуют такие преступники...$"
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
        raise SystemExit("usage: localize_icefall_cave_lorelei_rockets_v3_62.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_icefall_lorelei_rockets_v3_62_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Icefall Cave Lorelei/Rocket battle and Five Island warehouse reveal",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} forced Icefall Lorelei/Rocket blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
