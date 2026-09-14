#!/usr/bin/env python3
"""Qarro v3.73 mandatory Route 24 Nugget Bridge localization.

Translates only the verified forced Nugget Bridge contest battles and the Team
Rocket recruitment/battle sequence needed to pass Route 24 toward Bill. Optional
post-battle trainer chatter, Shane, Ash Bond, and Ash Cap remain untouched.
Pokemon species / move / ability proper names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTE24_NUGGET_BRIDGE_V3_73"
REL = Path("data/maps/Route24_Frlg/scripts.inc")

PATCHES = {
    "Route24_Text_CaleIntro": {
        "needles": ("People call this the NUGGET", "Beat us five TRAINERS", "Think you got what it takes?"),
        "ru": '''Route24_Text_CaleIntro::
\t.string "Это МОСТ НАГГЕТ!\\p"
\t.string "Победи пятерых ТРЕНЕРОВ\\n"
\t.string "и получи отличный приз!\\p"
\t.string "Думаешь, справишься?$"
''',
    },
    "Route24_Text_CaleDefeat": {
        "needles": ("Whoo!", "Good stuff!"),
        "ru": '''Route24_Text_CaleDefeat::
\t.string "Ух!\\n"
\t.string "Неплохо!$"
''',
    },
    "Route24_Text_AliIntro": {
        "needles": ("I'm second!", "Now it's serious!"),
        "ru": '''Route24_Text_AliIntro::
\t.string "Я второй!\\n"
\t.string "Теперь всё серьёзно!$"
''',
    },
    "Route24_Text_AliDefeat": {
        "needles": ("How could I lose?",),
        "ru": '''Route24_Text_AliDefeat::
\t.string "Как я мог проиграть?$"
''',
    },
    "Route24_Text_TimmyIntro": {
        "needles": ("Here's No. 3!", "I won't be easy!"),
        "ru": '''Route24_Text_TimmyIntro::
\t.string "А вот и номер три!\\n"
\t.string "Со мной будет непросто!$"
''',
    },
    "Route24_Text_TimmyDefeat": {
        "needles": ("Ow!", "Stomped flat!"),
        "ru": '''Route24_Text_TimmyDefeat::
\t.string "Ой!\\n"
\t.string "Меня разгромили!$"
''',
    },
    "Route24_Text_ReliIntro": {
        "needles": ("I'm No. 4!", "Getting tired?"),
        "ru": '''Route24_Text_ReliIntro::
\t.string "Я номер четыре!\\n"
\t.string "Уже устал?$"
''',
    },
    "Route24_Text_ReliDefeat": {
        "needles": ("I lost, too!",),
        "ru": '''Route24_Text_ReliDefeat::
\t.string "И я проиграла!$"
''',
    },
    "Route24_Text_EthanIntro": {
        "needles": ("Okay! I'm No. 5!", "I'll stomp you!"),
        "ru": '''Route24_Text_EthanIntro::
\t.string "Ладно! Я номер пять!\\n"
\t.string "Сейчас я тебя разгромлю!$"
''',
    },
    "Route24_Text_EthanDefeat": {
        "needles": ("Whoa!", "Too much!"),
        "ru": '''Route24_Text_EthanDefeat::
\t.string "Ого!\\n"
\t.string "Это слишком!$"
''',
    },
    "Route24_Text_JustEarnedFabulousPrize": {
        "needles": ("Congratulations! You beat our", "five contest TRAINERS!", "fabulous prize!"),
        "ru": '''Route24_Text_JustEarnedFabulousPrize::
\t.string "Поздравляю! Ты победил всех\\n"
\t.string "пятерых ТРЕНЕРОВ!\\p"
\t.string "Ты заслужил отличный приз!$"
''',
    },
    "Route24_Text_ReceivedNuggetFromMysteryTrainer": {
        "needles": ("received a NUGGET", "mystery TRAINER"),
        "ru": '''Route24_Text_ReceivedNuggetFromMysteryTrainer::
\t.string "{PLAYER} получил НАГГЕТ\\n"
\t.string "от загадочного ТРЕНЕРА!$"
''',
    },
    "Route24_Text_YouDontHaveAnyRoom": {
        "needles": ("You don't have any room!",),
        "ru": '''Route24_Text_YouDontHaveAnyRoom::
\t.string "В СУМКЕ нет места!$"
''',
    },
    "Route24_Text_JoinTeamRocket": {
        "needles": ("how would you like to", "join TEAM ROCKET?", "I'll make you an offer"),
        "ru": '''Route24_Text_JoinTeamRocket::
\t.string "Кстати, не хочешь вступить\\n"
\t.string "в TEAM ROCKET?\\p"
\t.string "Мы профессиональные преступники,\\n"
\t.string "специалисты по ПОКЕМОНАМ!\\p"
\t.string "Хочешь к нам?\\p"
\t.string "Точно нет?\\p"
\t.string "Да брось, вступай!\\p"
\t.string "Я говорю: вступай!\\p"
\t.string "Ладно, тебя надо убедить!\\p"
\t.string "Сделаю предложение, от которого\\n"
\t.string "ты не сможешь отказаться!$"
''',
    },
    "Route24_Text_RocketDefeat": {
        "needles": ("Arrgh!", "You are good!"),
        "ru": '''Route24_Text_RocketDefeat::
\t.string "Аргх!\\n"
\t.string "Ты силён!$"
''',
    },
    "Route24_Text_YoudBecomeTopRocketLeader": {
        "needles": ("you'd become", "a top leader in TEAM ROCKET", "Don't let this chance go to waste"),
        "ru": '''Route24_Text_YoudBecomeTopRocketLeader::
\t.string "С твоими способностями ты мог бы\\n"
\t.string "стать лидером TEAM ROCKET.\\p"
\t.string "Подумай, какая возможность!\\n"
\t.string "Не упускай такой шанс.$"
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
        raise SystemExit("usage: localize_route24_nugget_bridge_v3_73.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_route24_nugget_bridge_v3_73_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Route 24 Nugget Bridge contest and Team Rocket sequence",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Route 24 blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
