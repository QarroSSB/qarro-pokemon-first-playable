#!/usr/bin/env python3
"""Qarro v3.22 mandatory Cerulean Gym Russian runtime localization.

Translates only the verified pinned Misty progression chain: intro, defeat,
Cascade Badge explanation, TM03 receipt/explanation, and the no-bag-space line.
Pokemon species and move proper names remain English. Ash Bond / Ash Cap are
not referenced or changed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_CERULEAN_MISTY_V3_22"
REL = Path("data/maps/CeruleanCity_Gym_Frlg/scripts.inc")

PATCHES = {
    "CeruleanCity_Gym_Text_MistyIntro": (
        "CeruleanCity_Gym_Text_MistyIntro::\n"
        "\t.string \"Hi, you're a new face!\\p\"\n"
        "\t.string \"Only those TRAINERS who have a\\n\"\n"
        "\t.string \"policy about POKéMON can turn pro.\\p\"\n"
        "\t.string \"What is your approach when you\\n\"\n"
        "\t.string \"catch and train POKéMON?\\p\"\n"
        "\t.string \"My policy is an all-out offensive\\n\"\n"
        "\t.string \"with WATER-type POKéMON!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "CeruleanCity_Gym_Text_MistyIntro::\n"
        "\t.string \"Привет! Новое лицо!\\p\"\n"
        "\t.string \"Настоящим ТРЕНЕРОМ становится\\n\"\n"
        "\t.string \"тот, у кого есть свой подход.\\p\"\n"
        "\t.string \"Как ты ловишь и тренируешь\\n\"\n"
        "\t.string \"ПОКЕМОНОВ?\\p\"\n"
        "\t.string \"Мой стиль - постоянная атака\\n\"\n"
        "\t.string \"ВОДНЫМИ ПОКЕМОНАМИ!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "CeruleanCity_Gym_Text_MistyDefeat": (
        "CeruleanCity_Gym_Text_MistyDefeat::\n"
        "\t.string \"Wow!\\n\"\n"
        "\t.string \"You're too much!\\p\"\n"
        "\t.string \"All right!\\p\"\n"
        "\t.string \"You can have the CASCADEBADGE to\\n\"\n"
        "\t.string \"show you beat me.$\"\n",
        "CeruleanCity_Gym_Text_MistyDefeat::\n"
        "\t.string \"Ого!\\n\"\n"
        "\t.string \"Ты слишком силён!\\p\"\n"
        "\t.string \"Ладно!\\p\"\n"
        "\t.string \"Получай КАСКАДНЫЙ ЗНАЧОК -\\n\"\n"
        "\t.string \"доказательство победы надо мной.$\"\n",
    ),
    "CeruleanCity_Gym_Text_ExplainCascadeBadge": (
        "CeruleanCity_Gym_Text_ExplainCascadeBadge::\n"
        "\t.string \"The CASCADEBADGE makes all\\n\"\n"
        "\t.string \"POKéMON up to Lv. 30 obey.\\p\"\n"
        "\t.string \"That includes even outsiders you\\n\"\n"
        "\t.string \"got in trades.\\p\"\n"
        "\t.string \"There's more. You can now use CUT\\n\"\n"
        "\t.string \"anytime, even out of battle.\\p\"\n"
        "\t.string \"You can CUT down small trees to\\n\"\n"
        "\t.string \"open new pathways.\\p\"\n"
        "\t.string \"You can also have my favorite TM.$\"\n",
        "CeruleanCity_Gym_Text_ExplainCascadeBadge::\n"
        "\t.string \"КАСКАДНЫЙ ЗНАЧОК заставит всех\\n\"\n"
        "\t.string \"ПОКЕМОНОВ до ур. 30 слушаться.\\p\"\n"
        "\t.string \"Даже полученных по обмену.\\p\"\n"
        "\t.string \"И это ещё не всё. Теперь CUT\\n\"\n"
        "\t.string \"работает даже вне боя.\\p\"\n"
        "\t.string \"CUT срубает маленькие деревья\\n\"\n"
        "\t.string \"и открывает новые пути.\\p\"\n"
        "\t.string \"А ещё возьми мою любимую TM.$\"\n",
    ),
    "CeruleanCity_Gym_Text_ReceivedTM03FromMisty": (
        "CeruleanCity_Gym_Text_ReceivedTM03FromMisty::\n"
        "\t.string \"{PLAYER} received TM03\\n\"\n"
        "\t.string \"from MISTY.$\"\n",
        "CeruleanCity_Gym_Text_ReceivedTM03FromMisty::\n"
        "\t.string \"{PLAYER} получил TM03\\n\"\n"
        "\t.string \"от МИСТИ.$\"\n",
    ),
    "CeruleanCity_Gym_Text_ExplainTM03": (
        "CeruleanCity_Gym_Text_ExplainTM03::\n"
        "\t.string \"TM03 teaches WATER PULSE.\\p\"\n"
        "\t.string \"Use it on an aquatic POKéMON!$\"\n",
        "CeruleanCity_Gym_Text_ExplainTM03::\n"
        "\t.string \"TM03 обучает WATER PULSE.\\p\"\n"
        "\t.string \"Используй её на ВОДНОМ ПОКЕМОНЕ!$\"\n",
    ),
    "CeruleanCity_Gym_Text_BetterMakeRoomForThis": (
        "CeruleanCity_Gym_Text_BetterMakeRoomForThis::\n"
        "\t.string \"You better make room for this!$\"\n",
        "CeruleanCity_Gym_Text_BetterMakeRoomForThis::\n"
        "\t.string \"Освободи для этого место в СУМКЕ!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_cerulean_misty_v3_22.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_cerulean_misty_v3_22_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Misty runtime blocks; Ash Bond/Ash Cap untouched")

    rival_script = Path(__file__).with_name("localize_cerulean_rival_v3_23.py")
    subprocess.run([sys.executable, str(rival_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
