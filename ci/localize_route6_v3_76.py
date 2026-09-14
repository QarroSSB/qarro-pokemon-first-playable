#!/usr/bin/env python3
"""Qarro v3.76 Route 6 Russian runtime localization.

Translates the verified English-only Route 6 trainer dialogue and Underground
Path sign present in the current RU runtime inventory. No gameplay logic,
trainer data, Ash Bond, or Ash Cap paths are touched. Pokemon species / move /
ability proper names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTE6_V3_76"
REL = Path("data/maps/Route6_Frlg/scripts.inc")

PATCHES = {
    "Route6_Text_RickyIntro": {
        "needles": ("Who's there?", "Quit listening in on us!"),
        "ru": '''Route6_Text_RickyIntro::
\t.string "Кто там?\\n"
\t.string "Хватит нас подслушивать!$"
''',
    },
    "Route6_Text_RickyDefeat": {
        "needles": ("I just can't win!",),
        "ru": '''Route6_Text_RickyDefeat::
\t.string "Я просто не могу победить!$"
''',
    },
    "Route6_Text_RickyPostBattle": {
        "needles": ("Whisper…",),
        "ru": '''Route6_Text_RickyPostBattle::
\t.string "Шепот...\\n"
\t.string "Шепот...$"
''',
    },
    "Route6_Text_NancyIntro": {
        "needles": ("Excuse me!", "This is a private conversation!"),
        "ru": '''Route6_Text_NancyIntro::
\t.string "Извини!\\n"
\t.string "Это личный разговор!$"
''',
    },
    "Route6_Text_NancyDefeat": {
        "needles": ("Ugh!", "I hate losing."),
        "ru": '''Route6_Text_NancyDefeat::
\t.string "Уф!\\n"
\t.string "Ненавижу проигрывать.$"
''',
    },
    "Route6_Text_NancyPostBattle": {
        "needles": ("Whisper…",),
        "ru": '''Route6_Text_NancyPostBattle::
\t.string "Шепот...\\n"
\t.string "Шепот...$"
''',
    },
    "Route6_Text_KeigoIntro": {
        "needles": ("There aren't many bugs out here.",),
        "ru": '''Route6_Text_KeigoIntro::
\t.string "Здесь не так много жуков.$"
''',
    },
    "Route6_Text_KeigoDefeat": {
        "needles": ("No!", "You're kidding!"),
        "ru": '''Route6_Text_KeigoDefeat::
\t.string "Нет!\\n"
\t.string "Ты шутишь!$"
''',
    },
    "Route6_Text_KeigoPostBattle": {
        "needles": ("I like bugs, so I'm going back to", "VIRIDIAN FOREST."),
        "ru": '''Route6_Text_KeigoPostBattle::
\t.string "Я люблю жуков, так что вернусь\\n"
\t.string "в VIRIDIAN FOREST.$"
''',
    },
    "Route6_Text_JeffIntro": {
        "needles": ("Huh?", "You want to talk to me?"),
        "ru": '''Route6_Text_JeffIntro::
\t.string "А?\\n"
\t.string "Хочешь поговорить со мной?$"
''',
    },
    "Route6_Text_JeffDefeat": {
        "needles": ("This stinks…", "I couldn't beat your challenge…"),
        "ru": '''Route6_Text_JeffDefeat::
\t.string "Вот досада...\\n"
\t.string "Я не справился с твоим вызовом...$"
''',
    },
    "Route6_Text_JeffPostBattle": {
        "needles": ("I should bring more POKéMON with", "I'll feel safer that way."),
        "ru": '''Route6_Text_JeffPostBattle::
\t.string "Надо брать с собой больше POKéMON.\\n"
\t.string "Так мне будет спокойнее.$"
''',
    },
    "Route6_Text_IsabelleIntro": {
        "needles": ("Me?", "Well, okay. I'll play!"),
        "ru": '''Route6_Text_IsabelleIntro::
\t.string "Я?\\n"
\t.string "Ну ладно. Давай сыграем!$"
''',
    },
    "Route6_Text_IsabelleDefeat": {
        "needles": ("Things just didn't work…",),
        "ru": '''Route6_Text_IsabelleDefeat::
\t.string "Просто не получилось...$"
''',
    },
    "Route6_Text_IsabellePostBattle": {
        "needles": ("I want to get stronger.", "What's your secret?"),
        "ru": '''Route6_Text_IsabellePostBattle::
\t.string "Я хочу стать сильнее.\\n"
\t.string "В чем твой секрет?$"
''',
    },
    "Route6_Text_ElijahIntro": {
        "needles": ("I've never seen you around.", "Are you good?"),
        "ru": '''Route6_Text_ElijahIntro::
\t.string "Я тебя здесь раньше не видел.\\n"
\t.string "Ты силен?$"
''',
    },
    "Route6_Text_ElijahDefeat": {
        "needles": ("You're too good!",),
        "ru": '''Route6_Text_ElijahDefeat::
\t.string "Ты слишком хорош!$"
''',
    },
    "Route6_Text_ElijahPostBattle": {
        "needles": ("Are my POKéMON weak?", "Or, am I just bad?", "Which do you think?"),
        "ru": '''Route6_Text_ElijahPostBattle::
\t.string "Мои POKéMON слабые?\\n"
\t.string "Или я сам плох?\\l"
\t.string "Как думаешь?$"
''',
    },
    "Route6_Text_UndergroundPathSign": {
        "needles": ("UNDERGROUND PATH", "CERULEAN CITY - VERMILION CITY"),
        "ru": '''Route6_Text_UndergroundPathSign::
\t.string "ПОДЗЕМНЫЙ ПЕРЕХОД\\n"
\t.string "CERULEAN CITY - VERMILION CITY$"
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
        raise SystemExit("usage: localize_route6_v3_76.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_route6_v3_76_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "all 19 English-only Route 6 runtime blocks from current RU runtime inventory",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "route6EnglishRuntimeClosed": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Route 6 runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
