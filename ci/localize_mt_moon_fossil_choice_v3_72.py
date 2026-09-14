#!/usr/bin/env python3
"""Qarro v3.72 mandatory Mt. Moon fossil-choice localization.

Translates only the verified forced Super Nerd Miguel battle/fossil-choice
runtime text needed to finish the Mt. Moon story beat. Optional Rocket trainer
post-battle text, Cinnabar hint text, Ash Bond, and Ash Cap remain untouched.
Pokemon species / move / ability proper names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_MT_MOON_FOSSIL_CHOICE_V3_72"
REL = Path("data/maps/MtMoon_B2F_Frlg/scripts.inc")

PATCHES = {
    "MtMoon_B2F_Text_MiguelIntro": {
        "needles": ("Hey, stop!", "I found these fossils!", "They're both mine!"),
        "ru": '''MtMoon_B2F_Text_MiguelIntro::
\t.string "Эй, стой!\\p"
\t.string "Я нашёл эти ископаемые!\\n"
\t.string "Они оба мои!$"
''',
    },
    "MtMoon_B2F_Text_MiguelDefeat": {
        "needles": ("Okay!", "I'll share!"),
        "ru": '''MtMoon_B2F_Text_MiguelDefeat::
\t.string "Ладно!\\n"
\t.string "Поделюсь!$"
''',
    },
    "MtMoon_B2F_Text_WellEachTakeAFossil": {
        "needles": ("We'll each take a fossil!", "No being greedy!"),
        "ru": '''MtMoon_B2F_Text_WellEachTakeAFossil::
\t.string "Каждому по ископаемому!\\n"
\t.string "Не жадничай!$"
''',
    },
    "MtMoon_B2F_Text_ThenThisFossilIsMine": {
        "needles": ("Then this fossil is mine!",),
        "ru": '''MtMoon_B2F_Text_ThenThisFossilIsMine::
\t.string "Хорошо.\\n"
\t.string "Тогда этот мой!$"
''',
    },
    "MtMoon_B2F_Text_YouWantDomeFossil": {
        "needles": ("Do you want the DOME FOSSIL?",),
        "ru": '''MtMoon_B2F_Text_YouWantDomeFossil::
\t.string "Взять КУПОЛЬНУЮ\\n"
\t.string "ОКАМЕНЕЛОСТЬ?$"
''',
    },
    "MtMoon_B2F_Text_YouWantHelixFossil": {
        "needles": ("Do you want the HELIX FOSSIL?",),
        "ru": '''MtMoon_B2F_Text_YouWantHelixFossil::
\t.string "Взять СПИРАЛЬНУЮ\\n"
\t.string "ОКАМЕНЕЛОСТЬ?$"
''',
    },
    "MtMoon_B2F_Text_ObtainedHelixFossil": {
        "needles": ("Obtained the HELIX FOSSIL!",),
        "ru": '''MtMoon_B2F_Text_ObtainedHelixFossil::
\t.string "Получена СПИРАЛЬНАЯ\\n"
\t.string "ОКАМЕНЕЛОСТЬ!$"
''',
    },
    "MtMoon_B2F_Text_ObtainedDomeFossil": {
        "needles": ("Obtained the DOME FOSSIL!",),
        "ru": '''MtMoon_B2F_Text_ObtainedDomeFossil::
\t.string "Получена КУПОЛЬНАЯ\\n"
\t.string "ОКАМЕНЕЛОСТЬ!$"
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
        raise SystemExit("usage: localize_mt_moon_fossil_choice_v3_72.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_mt_moon_fossil_choice_v3_72_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Mt. Moon Miguel battle and fossil-choice dialogue",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Mt. Moon fossil blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
