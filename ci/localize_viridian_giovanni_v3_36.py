#!/usr/bin/env python3
"""Qarro v3.36 mandatory Viridian Gym / Giovanni Russian runtime localization.

Translates only the verified pinned Giovanni progression chain: intro, defeat,
Earth Badge explanation, TM26 receipt/explanation, no-bag-space line, and
post-battle dialogue. Pokemon species / move / ability proper names remain
English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_VIRIDIAN_GIOVANNI_V3_36"
REL = Path("data/maps/ViridianCity_Gym_Frlg/scripts.inc")

PATCHES = {
    "ViridianCity_Gym_Text_GiovanniIntro": (
        "ViridianCity_Gym_Text_GiovanniIntro::\n\t.string \"Fwahahaha!\\n\"\n\t.string \"Welcome to my hideout!\\p\"\n\t.string \"It shall be so until I can restore\\n\"\n\t.string \"TEAM ROCKET to its former glory.\\p\"\n\t.string \"But, you have found me again.\\n\"\n\t.string \"So be it.\\l\"\n\t.string \"This time, I'm not holding back!\\p\"\n\t.string \"Once more, you shall face\\n\"\n\t.string \"GIOVANNI, the greatest TRAINER!{PLAY_BGM}{MUS_RG_ENCOUNTER_ROCKET}$\"\n",
        "ViridianCity_Gym_Text_GiovanniIntro::\n\t.string \"Ха-ха-ха!\\n\"\n\t.string \"Добро пожаловать в моё убежище!\\p\"\n\t.string \"Оно останется им, пока я не верну\\n\"\n\t.string \"TEAM ROCKET былую славу.\\p\"\n\t.string \"Но ты снова нашёл меня.\\n\"\n\t.string \"Пусть так.\\l\"\n\t.string \"На этот раз я не сдерживаюсь!\\p\"\n\t.string \"Снова перед тобой\\n\"\n\t.string \"GIOVANNI, величайший ТРЕНЕР!{PLAY_BGM}{MUS_RG_ENCOUNTER_ROCKET}$\"\n",
    ),
    "ViridianCity_Gym_Text_GiovanniDefeat": (
        "ViridianCity_Gym_Text_GiovanniDefeat::\n\t.string \"Ha!\\n\"\n\t.string \"That was a truly intense fight.\\l\"\n\t.string \"You have won!\\p\"\n\t.string \"As proof, here is the EARTHBADGE!\\n\"\n\t.string \"{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}$\"\n",
        "ViridianCity_Gym_Text_GiovanniDefeat::\n\t.string \"Ха!\\n\"\n\t.string \"Это была по-настоящему жаркая битва.\\l\"\n\t.string \"Ты победил!\\p\"\n\t.string \"В доказательство возьми ЗНАЧОК ЗЕМЛИ!\\n\"\n\t.string \"{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}$\"\n",
    ),
    "ViridianCity_Gym_Text_GiovanniPostBattle": (
        "ViridianCity_Gym_Text_GiovanniPostBattle::\n\t.string \"Having lost in this fashion, \\n\"\n\t.string \"I can't face my followers.\\l\"\n\t.string \"I have betrayed their trust.\\p\"\n\t.string \"As of today, TEAM ROCKET is\\n\"\n\t.string \"finished forever!\\p\"\n\t.string \"As for myself, I shall dedicate\\n\"\n\t.string \"my life to training again.\\p\"\n\t.string \"Let us meet again someday!\\n\"\n\t.string \"Farewell!$\"\n",
        "ViridianCity_Gym_Text_GiovanniPostBattle::\n\t.string \"После такого поражения я не могу\\n\"\n\t.string \"смотреть в глаза своим людям.\\l\"\n\t.string \"Я предал их доверие.\\p\"\n\t.string \"С сегодняшнего дня TEAM ROCKET\\n\"\n\t.string \"распущена навсегда!\\p\"\n\t.string \"А я снова посвящу свою жизнь\\n\"\n\t.string \"тренировкам.\\p\"\n\t.string \"Когда-нибудь мы ещё встретимся!\\n\"\n\t.string \"Прощай!$\"\n",
    ),
    "ViridianCity_Gym_Text_ExplainEarthBadgeTakeThis": (
        "ViridianCity_Gym_Text_ExplainEarthBadgeTakeThis::\n\t.string \"The EARTHBADGE makes POKéMON of\\n\"\n\t.string \"any level obey without question.\\p\"\n\t.string \"It is evidence of your mastery as\\n\"\n\t.string \"a POKéMON TRAINER.\\p\"\n\t.string \"With it, you can challenge the\\n\"\n\t.string \"POKéMON LEAGUE.\\p\"\n\t.string \"Also, take this TM.\\p\"\n\t.string \"Consider it a gift for your POKéMON\\n\"\n\t.string \"LEAGUE challenge.$\"\n",
        "ViridianCity_Gym_Text_ExplainEarthBadgeTakeThis::\n\t.string \"Со ЗНАЧКОМ ЗЕМЛИ ПОКЕМОНЫ\\n\"\n\t.string \"любого уровня будут слушаться тебя.\\p\"\n\t.string \"Это доказательство мастерства\\n\"\n\t.string \"ТРЕНЕРА ПОКЕМОНОВ.\\p\"\n\t.string \"Теперь ты можешь бросить вызов\\n\"\n\t.string \"ЛИГЕ ПОКЕМОНОВ.\\p\"\n\t.string \"И ещё возьми эту TM.\\p\"\n\t.string \"Считай её подарком перед испытанием\\n\"\n\t.string \"ЛИГИ ПОКЕМОНОВ.$\"\n",
    ),
    "ViridianCity_Gym_Text_ReceivedTM26FromGiovanni": (
        "ViridianCity_Gym_Text_ReceivedTM26FromGiovanni::\n\t.string \"{PLAYER} received TM26\\n\"\n\t.string \"from GIOVANNI.$\"\n",
        "ViridianCity_Gym_Text_ReceivedTM26FromGiovanni::\n\t.string \"{PLAYER} получил TM26\\n\"\n\t.string \"от GIOVANNI.$\"\n",
    ),
    "ViridianCity_Gym_Text_ExplainTM26": (
        "ViridianCity_Gym_Text_ExplainTM26::\n\t.string \"TM26 contains EARTHQUAKE.\\p\"\n\t.string \"It is a powerful attack that causes\\n\"\n\t.string \"a massive tremor.\\p\"\n\t.string \"I made it when I ran the GYM here,\\n\"\n\t.string \"far too long ago… $\"\n",
        "ViridianCity_Gym_Text_ExplainTM26::\n\t.string \"TM26 содержит EARTHQUAKE.\\p\"\n\t.string \"Это мощная атака, вызывающая\\n\"\n\t.string \"сильнейшее землетрясение.\\p\"\n\t.string \"Я создал её, когда руководил этим ГИМОМ\\n\"\n\t.string \"много лет назад... $\"\n",
    ),
    "ViridianCity_Gym_Text_YouDoNotHaveSpace": (
        "ViridianCity_Gym_Text_YouDoNotHaveSpace::\n\t.string \"You do not have space for this!$\"\n",
        "ViridianCity_Gym_Text_YouDoNotHaveSpace::\n\t.string \"В СУМКЕ нет места для этого!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_viridian_giovanni_v3_36.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_viridian_giovanni_v3_36_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Viridian Giovanni runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
