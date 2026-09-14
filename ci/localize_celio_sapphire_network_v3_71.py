#!/usr/bin/env python3
"""Qarro v3.71 mandatory Celio Sapphire return / Network Machine localization.

Translates only the verified forced dialogue when the recovered Sapphire is
returned to Celio and the Network Machine is brought online. Optional repeat
Celio dialogue, signs, items, Ash Bond, and Ash Cap remain untouched. Pokemon
species / move / ability proper names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_CELIO_SAPPHIRE_NETWORK_V3_71"
REL = Path("data/maps/OneIsland_PokemonCenter_1F_Frlg/scripts.inc")

PATCHES = {
    "OneIsland_PokemonCenter_1F_Text_HandedSapphireToCelio": {
        "needles": ("handed the SAPPHIRE", "to CELIO"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_HandedSapphireToCelio::
\t.string "{PLAYER} передаёт САПФИР\\n"
\t.string "CELIO.$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_ThankYouGiveMeTime": {
        "needles": ("forms a pair with the RUBY", "Thank you so much!", "Please give me a little time"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_ThankYouGiveMeTime::
\t.string "CELIO: Так это тот камень,\\n"
\t.string "что образует пару с РУБИНОМ...\\p"
\t.string "{PLAYER}, тебе пришлось через\\n"
\t.string "многое пройти ради него.\\p"
\t.string "Можешь ничего не говорить.\\n"
\t.string "Я знаю, что было нелегко.\\p"
\t.string "Большое тебе спасибо!\\p"
\t.string "Теперь моя очередь поработать\\n"
\t.string "для тебя! Дай мне немного времени.$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_OkayThisIsGood": {
        "needles": ("Okay, this is good",),
        "ru": '''OneIsland_PokemonCenter_1F_Text_OkayThisIsGood::
\t.string "Так, отлично...$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_LinkedUpWithLanette": {
        "needles": ("I did it!", "linked up with LANETTE"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_LinkedUpWithLanette::
\t.string "Получилось!\\n"
\t.string "Связь с LANETTE установлена!$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_ManagedToLinkWithHoennThankYou": {
        "needles": ("managed to link up", "HOENN region", "Network Machine is", "dream came"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_ManagedToLinkWithHoennThankYou::
\t.string "{PLAYER}...\\n"
\t.string "{PLAYER}, получилось!\\p"
\t.string "Теперь есть связь с TRAINERS\\n"
\t.string "из региона HOENN!\\p"
\t.string "Наконец Network Machine\\n"
\t.string "полностью работает!\\p"
\t.string "{PLAYER}, всё это благодаря тебе!\\p"
\t.string "Спасибо! Моя мечта\\n"
\t.string "сбылась...$"
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
        raise SystemExit("usage: localize_celio_sapphire_network_v3_71.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_celio_sapphire_network_v3_71_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Celio Sapphire return and Network Machine completion dialogue",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Celio/Sapphire blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
