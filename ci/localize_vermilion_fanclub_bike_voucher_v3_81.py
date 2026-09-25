#!/usr/bin/env python3
"""Qarro v3.81 Vermilion Pokemon Fan Club Bike Voucher localization.

Translates the verified Chairman/Bike Voucher interaction as one coherent
runtime scene from the fresh RU audit. Gameplay logic, flags, item rewards,
trainer data, Ash Bond, and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_VERMILION_FANCLUB_BIKE_VOUCHER_V3_81"
REL = Path("data/maps/VermilionCity_PokemonFanClub_Frlg/scripts.inc")
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

REPLACEMENTS = {
    "VermilionCity_PokemonFanClub_Text_DidYouComeToHearAboutMyMons": (
        ("I chair the POKéMON Fan Club!", "I raise more than a hundred", "Did you come visit to hear about"),
        '''VermilionCity_PokemonFanClub_Text_DidYouComeToHearAboutMyMons::
\t.string "Я председатель Клуба ПОКЕМОНОВ!\\p"
\t.string "Я вырастил больше сотни\\n"
\t.string "ПОКЕМОНОВ!\\p"
\t.string "К ПОКЕМОНАМ я очень придирчив.\\n"
\t.string "Ещё бы!\\p"
\t.string "Ну так что...\\p"
\t.string "Ты пришёл послушать о моих\\n"
\t.string "ПОКЕМОНАХ?$"
'''),
    "VermilionCity_PokemonFanClub_Text_ChairmansStory": (
        ("Good!", "My favorite RAPIDASH", "Oops! Look at the time!", "I want you to have this!"),
        '''VermilionCity_PokemonFanClub_Text_ChairmansStory::
\t.string "Отлично!\\n"
\t.string "Тогда слушай!\\p"
\t.string "Мой любимый RAPIDASH...\\p"
\t.string "Он милый... красивый... умный...\\n"
\t.string "и просто потрясающий...\\l"
\t.string "добрый... я его обожаю!\\p"
\t.string "Обнять его во сне... тёплого\\n"
\t.string "и уютного... великолепно...\\l"
\t.string "просто чудесно...\\l"
\t.string "Ой! Уже столько времени!\\l"
\t.string "Я тебя задержал!\\p"
\t.string "Спасибо, что выслушал!\\n"
\t.string "Хочу подарить тебе вот это!$"
'''),
    "VermilionCity_PokemonFanClub_Text_ReceivedBikeVoucherFromChairman": (
        ("received a BIKE VOUCHER", "from the CHAIRMAN."),
        '''VermilionCity_PokemonFanClub_Text_ReceivedBikeVoucherFromChairman::
\t.string "{PLAYER} получил BIKE VOUCHER\\n"
\t.string "от ПРЕДСЕДАТЕЛЯ.$"
'''),
    "VermilionCity_PokemonFanClub_Text_ExplainBikeVoucher": (
        ("Take that BIKE VOUCHER", "BIKE SHOP in CERULEAN CITY", "free of charge!", "favorite FEAROW"),
        '''VermilionCity_PokemonFanClub_Text_ExplainBikeVoucher::
\t.string "Отнеси BIKE VOUCHER в\\n"
\t.string "BIKE SHOP в CERULEAN CITY.\\p"
\t.string "Там его бесплатно обменяют\\n"
\t.string "на BICYCLE!\\p"
\t.string "Не волнуйся, мой любимый FEAROW\\n"
\t.string "доставит меня куда угодно.\\p"
\t.string "Так что BICYCLE мне не нужен.\\p"
\t.string "Надеюсь, тебе понравится ездить!$"
'''),
    "VermilionCity_PokemonFanClub_Text_ComeBackToHearStory": (
        ("Come back when you want to", "hear my story!"),
        '''VermilionCity_PokemonFanClub_Text_ComeBackToHearStory::
\t.string "Ох. Возвращайся, когда захочешь\\n"
\t.string "послушать мою историю!$"
'''),
    "VermilionCity_PokemonFanClub_Text_DidntComeToSeeAboutMonsAgain": (
        ("Hello, {PLAYER}!", "Did you come see me about my", "Too bad!"),
        '''VermilionCity_PokemonFanClub_Text_DidntComeToSeeAboutMonsAgain::
\t.string "Привет, {PLAYER}!\\p"
\t.string "Снова пришёл послушать о моих\\n"
\t.string "ПОКЕМОНАХ?\\p"
\t.string "Нет?\\n"
\t.string "Очень жаль!$"
'''),
    "VermilionCity_PokemonFanClub_Text_MakeRoomForThis": (
        ("Make room for this!",),
        '''VermilionCity_PokemonFanClub_Text_MakeRoomForThis::
\t.string "Освободи для этого место!$"
'''),
}


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_vermilion_fanclub_bike_voucher_v3_81.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")

    for label, (needles, replacement) in REPLACEMENTS.items():
        start, end, block = block_bounds(text, label)
        missing = [needle for needle in needles if needle not in block]
        if missing:
            raise SystemExit(f"{MARKER}: {label}: pinned evidence mismatch; missing {missing}")
        if re.search(r"[А-Яа-яЁё]", block):
            raise SystemExit(f"{MARKER}: {label}: already localized or unexpectedly contains Cyrillic")
        text = text[:start] + replacement + "\n" + text[end:]

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_vermilion_fanclub_bike_voucher_v3_81_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": list(REPLACEMENTS),
        "translatedBlockCount": len(REPLACEMENTS),
        "scope": "fresh-audit Vermilion Pokemon Fan Club Chairman/Bike Voucher scene only",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(REPLACEMENTS)} Bike Voucher scene blocks; Ash Bond/Ash Cap untouched")
    next_script = Path(__file__).with_name("localize_vermilion_fanclub_remaining_v3_82.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
