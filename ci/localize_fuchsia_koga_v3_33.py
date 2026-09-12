#!/usr/bin/env python3
"""Qarro v3.33 mandatory Fuchsia Gym / Koga Russian runtime localization.

Translates only the verified pinned Koga progression chain: intro, defeat,
Soul Badge explanation, TM06 receipt/explanation, no-bag-space line, and
post-battle TOXIC explanation. Pokemon species / move / ability proper names
remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_FUCHSIA_KOGA_V3_33"
REL = Path("data/maps/FuchsiaCity_Gym_Frlg/scripts.inc")

PATCHES = {
    "FuchsiaCity_Gym_Text_KogaIntro": (
        "FuchsiaCity_Gym_Text_KogaIntro::\n"
        "\t.string \"KOGA: Fwahahaha!\\p\"\n"
        "\t.string \"A mere child like you dares to\\n\"\n"
        "\t.string \"challenge me?\\p\"\n"
        "\t.string \"The very idea makes me shiver\\n\"\n"
        "\t.string \"with mirth!\\p\"\n"
        "\t.string \"Very well, I shall show you true\\n\"\n"
        "\t.string \"terror as a ninja master.\\p\"\n"
        "\t.string \"Poison brings steady doom.\\n\"\n"
        "\t.string \"Sleep renders foes helpless.\\p\"\n"
        "\t.string \"Despair to the creeping horror of\\n\"\n"
        "\t.string \"POISON-type POKéMON!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        "FuchsiaCity_Gym_Text_KogaIntro::\n"
        "\t.string \"КОГА: Фвахахаха!\\p\"\n"
        "\t.string \"Простой ребёнок вроде тебя смеет\\n\"\n"
        "\t.string \"бросать мне вызов?\\p\"\n"
        "\t.string \"Одна эта мысль заставляет меня\\n\"\n"
        "\t.string \"дрожать от смеха!\\p\"\n"
        "\t.string \"Хорошо. Я покажу тебе настоящий\\n\"\n"
        "\t.string \"ужас мастера-ниндзя.\\p\"\n"
        "\t.string \"Яд медленно несёт гибель.\\n\"\n"
        "\t.string \"Сон делает врага беспомощным.\\p\"\n"
        "\t.string \"Познай ужас ЯДОВИТЫХ\\n\"\n"
        "\t.string \"ПОКЕМОНОВ!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
    ),
    "FuchsiaCity_Gym_Text_KogaDefeat": (
        "FuchsiaCity_Gym_Text_KogaDefeat::\n"
        "\t.string \"Humph!\\n\"\n"
        "\t.string \"You have proven your worth!\\p\"\n"
        "\t.string \"Here!\\n\"\n"
        "\t.string \"Take the SOULBADGE!$\"\n",
        "FuchsiaCity_Gym_Text_KogaDefeat::\n"
        "\t.string \"Хмф!\\n\"\n"
        "\t.string \"Ты доказал свою силу!\\p\"\n"
        "\t.string \"Вот!\\n\"\n"
        "\t.string \"Бери ЗНАЧОК ДУШИ!$\"\n",
    ),
    "FuchsiaCity_Gym_Text_KogaPostBattle": (
        "FuchsiaCity_Gym_Text_KogaPostBattle::\n"
        "\t.string \"When afflicted by TOXIC, a POKéMON\\n\"\n"
        "\t.string \"suffers more and more.\\p\"\n"
        "\t.string \"It suffers worsening damage as the\\n\"\n"
        "\t.string \"battle wears on!\\p\"\n"
        "\t.string \"It will surely terrorize foes!$\"\n",
        "FuchsiaCity_Gym_Text_KogaPostBattle::\n"
        "\t.string \"Под действием TOXIC ПОКЕМОН\\n\"\n"
        "\t.string \"страдает всё сильнее.\\p\"\n"
        "\t.string \"С каждым ходом урон только\\n\"\n"
        "\t.string \"возрастает!\\p\"\n"
        "\t.string \"Враги точно будут в ужасе!$\"\n",
    ),
    "FuchsiaCity_Gym_Text_KogaExplainSoulBadge": (
        "FuchsiaCity_Gym_Text_KogaExplainSoulBadge::\n"
        "\t.string \"Now that you have the SOULBADGE,\\n\"\n"
        "\t.string \"the DEFENSE of your POKéMON rises.\\p\"\n"
        "\t.string \"It also lets you SURF outside of\\n\"\n"
        "\t.string \"battle.\\p\"\n"
        "\t.string \"Ah!\\n\"\n"
        "\t.string \"Take this, too!$\"\n",
        "FuchsiaCity_Gym_Text_KogaExplainSoulBadge::\n"
        "\t.string \"Теперь у тебя есть ЗНАЧОК ДУШИ,\\n\"\n"
        "\t.string \"и ЗАЩИТА ПОКЕМОНОВ возрастёт.\\p\"\n"
        "\t.string \"Он также позволяет использовать\\n\"\n"
        "\t.string \"SURF вне боя.\\p\"\n"
        "\t.string \"Ах да!\\n\"\n"
        "\t.string \"Возьми ещё и это!$\"\n",
    ),
    "FuchsiaCity_Gym_Text_ReceivedTM06FromKoga": (
        "FuchsiaCity_Gym_Text_ReceivedTM06FromKoga::\n"
        "\t.string \"{PLAYER} received TM06\\n\"\n"
        "\t.string \"from KOGA.$\"\n",
        "FuchsiaCity_Gym_Text_ReceivedTM06FromKoga::\n"
        "\t.string \"{PLAYER} получил TM06\\n\"\n"
        "\t.string \"от КОГИ.$\"\n",
    ),
    "FuchsiaCity_Gym_Text_KogaExplainTM06": (
        "FuchsiaCity_Gym_Text_KogaExplainTM06::\n"
        "\t.string \"Sealed within that TM06 lies\\n\"\n"
        "\t.string \"TOXIC!\\p\"\n"
        "\t.string \"It is a secret technique dating\\n\"\n"
        "\t.string \"back some four hundred years.$\"\n",
        "FuchsiaCity_Gym_Text_KogaExplainTM06::\n"
        "\t.string \"В этой TM06 скрывается\\n\"\n"
        "\t.string \"TOXIC!\\p\"\n"
        "\t.string \"Это секретная техника возрастом\\n\"\n"
        "\t.string \"около четырёхсот лет.$\"\n",
    ),
    "FuchsiaCity_Gym_Text_MakeSpaceForThis": (
        "FuchsiaCity_Gym_Text_MakeSpaceForThis::\n"
        "\t.string \"Make space for this, child!$\"\n",
        "FuchsiaCity_Gym_Text_MakeSpaceForThis::\n"
        "\t.string \"Освободи для этого место!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_fuchsia_koga_v3_33.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_fuchsia_koga_v3_33_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Koga runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
