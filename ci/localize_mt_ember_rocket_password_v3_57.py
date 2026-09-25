#!/usr/bin/env python3
"""Qarro v3.57 mandatory Mt. Ember Rocket-password scene localization.

Translates only the verified forced coordinate-trigger scene that starts after
Celio enables the Ruby quest: the two Rocket grunts break through, mention the
Warehouse, reveal the first password, and notice the player listening in.
The following Rocket battles, Ruby pickup/handoff, Rainbow Pass, optional NPC
dialogue, Ash Bond, and Ash Cap remain untouched. Pokemon species / move /
ability proper names remain English.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_MT_EMBER_ROCKET_PASSWORD_V3_57"
REL = Path("data/maps/MtEmber_Exterior_Frlg/scripts.inc")

PATCHES = {
    "MtEmber_Exterior_Text_PunchedThroughAtLast": {
        "needles": ("punched through at last", "treasure hunting"),
        "ru": '''MtEmber_Exterior_Text_PunchedThroughAtLast::
\t.string "Фух, наконец-то пробились.\\n"
\t.string "Пора искать сокровища!$"
''',
    },
    "MtEmber_Exterior_Text_WhatsPasswordAgain": {
        "needles": ("treasure we find", "WAREHOUSE", "what're the passwords"),
        "ru": '''MtEmber_Exterior_Text_WhatsPasswordAgain::
\t.string "Все сокровища, которые найдём,\\n"
\t.string "тащим обратно на ROCKET WAREHOUSE,\\l"
\t.string "понял?\\p"
\t.string "…А какие там пароли?\\n"
\t.string "Ну, на ROCKET WAREHOUSE.$"
''',
    },
    "MtEmber_Exterior_Text_FirstPasswordGoldeen": {
        "needles": ("forgot the password", "actually two", "GOLDEEN need", "second one"),
        "ru": '''MtEmber_Exterior_Text_FirstPasswordGoldeen::
\t.string "Что, забыл пароль?\\n"
\t.string "Вообще-то их два.\\p"
\t.string "Первый - “GOLDEEN need log.”\\p"
\t.string "А второй - это…$"
''',
    },
    "MtEmber_Exterior_Text_SnoopsBeenListeningIn": {
        "needles": ("This snoop's been listening in",),
        "ru": '''MtEmber_Exterior_Text_SnoopsBeenListeningIn::
\t.string "Эй!\\n"
\t.string "Этот шпион нас подслушивал!$"
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
        raise SystemExit("usage: localize_mt_ember_rocket_password_v3_57.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_mt_ember_rocket_password_v3_57_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Mt. Ember Rocket password scene triggered by the Celio Ruby quest",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Mt. Ember Rocket-password blocks; Ash Bond/Ash Cap untouched")

    next_script = Path(__file__).with_name("localize_mt_ember_rocket_battles_v3_58.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
