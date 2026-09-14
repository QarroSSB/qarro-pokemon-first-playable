#!/usr/bin/env python3
"""Qarro v3.74 remaining Route 24 Russian runtime localization.

Translates only the verified English-only Route 24 blocks intentionally left by
v3.73: Shane's optional battle dialogue and post-battle chatter for the five
Nugget Bridge contest trainers. No gameplay logic, trainer data, Ash Bond, or
Ash Cap paths are touched. Pokemon species / move / ability proper names remain
English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTE24_REMAINING_V3_74"
REL = Path("data/maps/Route24_Frlg/scripts.inc")

PATCHES = {
    "Route24_Text_ShaneIntro": {
        "needles": ("I saw your feat from the grass!",),
        "ru": '''Route24_Text_ShaneIntro::
\t.string "Я видел твой подвиг из травы!$"
''',
    },
    "Route24_Text_ShaneDefeat": {
        "needles": ("I thought not!",),
        "ru": '''Route24_Text_ShaneDefeat::
\t.string "Я так и думал!$"
''',
    },
    "Route24_Text_ShanePostBattle": {
        "needles": ("I hid because the people on the", "bridge frightened me."),
        "ru": '''Route24_Text_ShanePostBattle::
\t.string "Я спрятался, потому что люди\\n"
\t.string "на мосту меня напугали.$"
''',
    },
    "Route24_Text_EthanPostBattle": {
        "needles": ("I did my best. I have no regrets!",),
        "ru": '''Route24_Text_EthanPostBattle::
\t.string "Я сделал всё, что мог.\\n"
\t.string "Мне не о чем жалеть!$"
''',
    },
    "Route24_Text_ReliPostBattle": {
        "needles": ("I did my best, so I've no regrets!",),
        "ru": '''Route24_Text_ReliPostBattle::
\t.string "Я сделала всё, что могла.\\n"
\t.string "Мне не о чем жалеть!$"
''',
    },
    "Route24_Text_TimmyPostBattle": {
        "needles": ("I did my best. I have no regrets!",),
        "ru": '''Route24_Text_TimmyPostBattle::
\t.string "Я сделал всё, что мог.\\n"
\t.string "Мне не о чем жалеть!$"
''',
    },
    "Route24_Text_AliPostBattle": {
        "needles": ("I did my best. I have no regrets!",),
        "ru": '''Route24_Text_AliPostBattle::
\t.string "Я сделал всё, что мог.\\n"
\t.string "Мне не о чем жалеть!$"
''',
    },
    "Route24_Text_CalePostBattle": {
        "needles": ("I did my best. I have no regrets!",),
        "ru": '''Route24_Text_CalePostBattle::
\t.string "Я сделал всё, что мог.\\n"
\t.string "Мне не о чем жалеть!$"
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
        raise SystemExit("usage: localize_route24_remaining_v3_74.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_route24_remaining_v3_74_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "remaining English-only Route 24 runtime dialogue after v3.73",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "route24EnglishRuntimeClosed": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} remaining Route 24 blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
