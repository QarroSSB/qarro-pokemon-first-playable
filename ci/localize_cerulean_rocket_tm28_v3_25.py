#!/usr/bin/env python3
"""Qarro v3.25 mandatory Cerulean Rocket / TM28 Russian runtime localization.

Translates only the verified pinned Rocket grunt progression chain after Bill:
intro, defeat, stolen-TM return, TM28 recovery, exit, and no-room response.
Pokemon species / move / ability proper names remain English. Ash Bond / Ash
Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_CERULEAN_ROCKET_TM28_V3_25"
REL = Path("data/maps/CeruleanCity_Frlg/scripts.inc")

PATCHES = {
    "CeruleanCity_Text_GruntIntro": (
        "CeruleanCity_Text_GruntIntro::\n"
        "\t.string \"Hey! Stay out!\\n\"\n"
        "\t.string \"It's not your yard!\\p\"\n"
        "\t.string \"…Huh?\\n\"\n"
        "\t.string \"Me?\\p\"\n"
        "\t.string \"I'm an innocent bystander!\\n\"\n"
        "\t.string \"Don't you believe me?{PLAY_BGM}{MUS_RG_ENCOUNTER_ROCKET}$\"\n",
        "CeruleanCity_Text_GruntIntro::\n"
        "\t.string \"Эй! Не лезь сюда!\\n\"\n"
        "\t.string \"Это не твой двор!\\p\"\n"
        "\t.string \"…А?\\n\"\n"
        "\t.string \"Я?\\p\"\n"
        "\t.string \"Я просто невинный прохожий!\\n\"\n"
        "\t.string \"Не веришь мне?{PLAY_BGM}{MUS_RG_ENCOUNTER_ROCKET}$\"\n",
    ),
    "CeruleanCity_Text_GruntDefeat": (
        "CeruleanCity_Text_GruntDefeat::\n"
        "\t.string \"GRUNT: Stop! I give up!\\n\"\n"
        "\t.string \"I'll leave quietly!$\"\n",
        "CeruleanCity_Text_GruntDefeat::\n"
        "\t.string \"ГРАНТ: Стой! Я сдаюсь!\\n\"\n"
        "\t.string \"Я тихо уйду!$\"\n",
    ),
    "CeruleanCity_Text_OkayIllReturnStolenTM": (
        "CeruleanCity_Text_OkayIllReturnStolenTM::\n"
        "\t.string \"…Okay.\\n\"\n"
        "\t.string \"I'll return the TM I stole.$\"\n",
        "CeruleanCity_Text_OkayIllReturnStolenTM::\n"
        "\t.string \"…Ладно.\\n\"\n"
        "\t.string \"Я верну украденный TM.$\"\n",
    ),
    "CeruleanCity_Text_RecoveredTM28FromGrunt": (
        "CeruleanCity_Text_RecoveredTM28FromGrunt::\n"
        "\t.string \"{PLAYER} recovered TM28 from\\n\"\n"
        "\t.string \"the TEAM ROCKET GRUNT.$\"\n",
        "CeruleanCity_Text_RecoveredTM28FromGrunt::\n"
        "\t.string \"{PLAYER} вернул TM28 у\\n\"\n"
        "\t.string \"бойца TEAM ROCKET.$\"\n",
    ),
    "CeruleanCity_Text_BetterGetMovingBye": (
        "CeruleanCity_Text_BetterGetMovingBye::\n"
        "\t.string \"I better get moving!\\n\"\n"
        "\t.string \"Bye!$\"\n",
        "CeruleanCity_Text_BetterGetMovingBye::\n"
        "\t.string \"Мне пора убираться!\\n\"\n"
        "\t.string \"Пока!$\"\n",
    ),
    "CeruleanCity_Text_MakeRoomForThisCantRun": (
        "CeruleanCity_Text_MakeRoomForThisCantRun::\n"
        "\t.string \"Make room for this!\\n\"\n"
        "\t.string \"I can't run until I give it to you!$\"\n",
        "CeruleanCity_Text_MakeRoomForThisCantRun::\n"
        "\t.string \"Освободи место!\\n\"\n"
        "\t.string \"Я не уйду, пока не отдам это!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_cerulean_rocket_tm28_v3_25.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied = []

    for label, (pinned, ru) in PATCHES.items():
        variants = [pinned]
        normalized = pinned.replace("é", "e").replace("É", "E")
        if normalized != pinned:
            variants.append(normalized)
        hits = [(variant, text.count(variant)) for variant in variants]
        total = sum(count for _, count in hits)
        if total != 1:
            raise SystemExit(f"{MARKER}: {label}: expected exactly one pinned/normalized anchor, found {total}")
        source = next(variant for variant, count in hits if count == 1)
        text = text.replace(source, ru, 1)
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_cerulean_rocket_tm28_v3_25_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names may remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Cerulean Rocket/TM28 runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
