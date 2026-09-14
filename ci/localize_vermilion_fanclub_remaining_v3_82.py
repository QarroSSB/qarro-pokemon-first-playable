#!/usr/bin/env python3
"""Qarro v3.82 remaining Vermilion Pokemon Fan Club localization.

Translates the remaining verified English-only runtime text blocks in the
Vermilion Pokemon Fan Club from pinned upstream. Gameplay logic, flags,
trainer data, Ash Bond, and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_VERMILION_FANCLUB_REMAINING_V3_82"
REL = Path("data/maps/VermilionCity_PokemonFanClub_Frlg/scripts.inc")
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

REPLACEMENTS = {
    "VermilionCity_PokemonFanClub_Text_AdmirePikachusTail": (
        ("Won't you admire my PIKACHU's", "adorable tail?"),
        '''VermilionCity_PokemonFanClub_Text_AdmirePikachusTail::
\t.string "Полюбуйся очаровательным хвостом\\n"
\t.string "моего PIKACHU!$"
'''),
    "VermilionCity_PokemonFanClub_Text_PikachuTwiceAsCute": (
        ("Humph!", "My PIKACHU is twice as cute"),
        '''VermilionCity_PokemonFanClub_Text_PikachuTwiceAsCute::
\t.string "Хм!\\p"
\t.string "Мой PIKACHU вдвое милее\\n"
\t.string "того!$"
'''),
    "VermilionCity_PokemonFanClub_Text_AdoreMySeel": (
        ("I just adore my SEEL!", "It squeals, “Kyuuuh,”"),
        '''VermilionCity_PokemonFanClub_Text_AdoreMySeel::
\t.string "Я просто обожаю моего SEEL!\\n"
\t.string "Он такой милый!\\p"
\t.string "Когда я его обнимаю, он пищит:\\n"
\t.string "“Кьююю!”$"
'''),
    "VermilionCity_PokemonFanClub_Text_SeelFarMoreAttractive": (
        ("Oh, dear!", "My SEEL is far more attractive."),
        '''VermilionCity_PokemonFanClub_Text_SeelFarMoreAttractive::
\t.string "Ох, ну что ты!\\p"
\t.string "Мой SEEL куда привлекательнее.\\n"
\t.string "Я бы сказала, раза в два.$"
'''),
    "VermilionCity_PokemonFanClub_Text_Pikachu": (
        ("PIKACHU: Chu! Pikachu!",),
        '''VermilionCity_PokemonFanClub_Text_Pikachu::
\t.string "PIKACHU: Чу! Пикачу!$"
'''),
    "VermilionCity_PokemonFanClub_Text_Seel": (
        ("SEEL: Kyuoo!",),
        '''VermilionCity_PokemonFanClub_Text_Seel::
\t.string "SEEL: Кьюу!$"
'''),
    "VermilionCity_PokemonFanClub_Text_ChairmanVeryVocalAboutPokemon": (
        ("Our CHAIRMAN is very vocal about", "POKéMON."),
        '''VermilionCity_PokemonFanClub_Text_ChairmanVeryVocalAboutPokemon::
\t.string "Наш ПРЕДСЕДАТЕЛЬ обожает говорить\\n"
\t.string "о ПОКЕМОНАХ.$"
'''),
    "VermilionCity_PokemonFanClub_Text_ListenPolitelyToOtherTrainers": (
        ("Let's all listen politely to other", "TRAINERS!"),
        '''VermilionCity_PokemonFanClub_Text_ListenPolitelyToOtherTrainers::
\t.string "Давайте вежливо слушать других\\n"
\t.string "ТРЕНЕРОВ!$"
'''),
    "VermilionCity_PokemonFanClub_Text_SomeoneBragsBragBack": (
        ("If someone brags, brag right back!",),
        '''VermilionCity_PokemonFanClub_Text_SomeoneBragsBragBack::
\t.string "Если кто-то хвастается —\\n"
\t.string "похвастайся в ответ!$"
'''),
    "VermilionCity_PokemonFanClub_Text_ChairmanReallyAdoresHisMons": (
        ("Our CHAIRMAN really does adore his", "POKéMON is DAISY, I think."),
        '''VermilionCity_PokemonFanClub_Text_ChairmanReallyAdoresHisMons::
\t.string "Наш ПРЕДСЕДАТЕЛЬ и правда обожает\\n"
\t.string "своих ПОКЕМОНОВ.\\p"
\t.string "Но, думаю, больше всех ПОКЕМОНЫ\\n"
\t.string "любят DAISY.$"
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
        raise SystemExit("usage: localize_vermilion_fanclub_remaining_v3_82.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_vermilion_fanclub_remaining_v3_82_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": list(REPLACEMENTS),
        "translatedBlockCount": len(REPLACEMENTS),
        "scope": "remaining pinned-upstream Vermilion Pokemon Fan Club runtime text only",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(REPLACEMENTS)} remaining Fan Club blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
