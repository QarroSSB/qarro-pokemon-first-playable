#!/usr/bin/env python3
"""Qarro v3.58 mandatory Mt. Ember Rocket battle localization.

Translates only the verified progression battle text for the two Rocket grunts
blocking the Ruby cave after the first Rocket Warehouse password scene. The
pre-quest idle dialogue, Ruby pickup/handoff, Rainbow Pass, optional NPC text,
Ash Bond, and Ash Cap remain untouched. Pokemon species / move / ability proper
names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_MT_EMBER_ROCKET_BATTLES_V3_58"
REL = Path("data/maps/MtEmber_Exterior_Frlg/scripts.inc")

PATCHES = {
    "MtEmber_Exterior_Text_Grunt1Intro": {
        "needles": ("eavesdropping on us", "haven't you"),
        "ru": '''MtEmber_Exterior_Text_Grunt1Intro::
\t.string "Вы ведь нас подслушивали,\\n"
\t.string "не так ли?$"
''',
    },
    "MtEmber_Exterior_Text_Grunt1Defeat": {
        "needles": ("Huh, what?",),
        "ru": '''MtEmber_Exterior_Text_Grunt1Defeat::
\t.string "Что? Как так?$"
''',
    },
    "MtEmber_Exterior_Text_Grunt1PostBattle": {
        "needles": ("Why'd you have to win?",),
        "ru": '''MtEmber_Exterior_Text_Grunt1PostBattle::
\t.string "И зачем тебе было побеждать?$"
''',
    },
    "MtEmber_Exterior_Text_Grunt2Intro": {
        "needles": ("horn in on our treasure", "Don't bet on it"),
        "ru": '''MtEmber_Exterior_Text_Grunt2Intro::
\t.string "Хочешь добраться до нашего\\n"
\t.string "сокровища? Даже не надейся!$"
''',
    },
    "MtEmber_Exterior_Text_Grunt2Defeat": {
        "needles": ("Wait!", "But how?"),
        "ru": '''MtEmber_Exterior_Text_Grunt2Defeat::
\t.string "Стой!\\n"
\t.string "Но как?$"
''',
    },
    "MtEmber_Exterior_Text_Grunt2PostBattle": {
        "needles": ("Develop amnesia conveniently", "forget everything you heard"),
        "ru": '''MtEmber_Exterior_Text_Grunt2PostBattle::
\t.string "Удобно потеряй память и забудь\\n"
\t.string "всё, что здесь слышал!$"
''',
    },
    "MtEmber_Exterior_Text_WellRegroupDontStepInsideThere": {
        "needles": ("What a setback", "We'll have to regroup", "Don't even think about taking", "If you know what's good for you"),
        "ru": '''MtEmber_Exterior_Text_WellRegroupDontStepInsideThere::
\t.string "Вот неудача...\\n"
\t.string "Придётся перегруппироваться.\\p"
\t.string "Тебе туда нельзя!\\n"
\t.string "Даже шага внутрь не делай!\\p"
\t.string "Если тебе дорога жизнь,\\n"
\t.string "забудь об этом месте!$"
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
        raise SystemExit("usage: localize_mt_ember_rocket_battles_v3_58.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_mt_ember_rocket_battles_v3_58_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Mt. Ember Rocket battles that unblock the Ruby cave",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Mt. Ember Rocket battle blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
