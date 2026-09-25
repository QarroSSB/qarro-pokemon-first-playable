#!/usr/bin/env python3
"""Qarro v3.43 Pokemon League rematch Russian runtime localization.

Translates only the verified pinned rematch intro blocks for Lorelei, Bruno,
Agatha, Lance, and Champion Rival after FLAG_IS_CHAMPION. First-clear text is
handled by v3.38-v3.42. Pokemon species / move / ability proper names remain
English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEMON_LEAGUE_REMATCHES_V3_43"

PATCHES = {
    Path("data/maps/PokemonLeague_LoreleisRoom_Frlg/scripts.inc"): {
        "PokemonLeague_LoreleisRoom_Text_RematchIntro": (
            "PokemonLeague_LoreleisRoom_Text_RematchIntro::\n"
            "\t.string \"Welcome to the POKéMON LEAGUE.\\p\"\n"
            "\t.string \"I, LORELEI of the ELITE FOUR,\\n\"\n"
            "\t.string \"have returned!\\p\"\n"
            "\t.string \"You know how it goes.\\n\"\n"
            "\t.string \"No one can best me when it comes\\l\"\n"
            "\t.string \"to icy POKéMON.\\p\"\n"
            "\t.string \"Freezing moves are powerful.\\p\"\n"
            "\t.string \"Your POKéMON will be at my mercy\\n\"\n"
            "\t.string \"when they are frozen solid.\\p\"\n"
            "\t.string \"Hahaha!\\n\"\n"
            "\t.string \"Are you ready?{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
            "PokemonLeague_LoreleisRoom_Text_RematchIntro::\n"
            "\t.string \"Снова добро пожаловать в ЛИГУ ПОКЕМОНОВ.\\p\"\n"
            "\t.string \"Я, LORELEI из ЭЛИТНОЙ ЧЕТВЁРКИ,\\n\"\n"
            "\t.string \"вернулась!\\p\"\n"
            "\t.string \"Ты знаешь, как всё будет.\\n\"\n"
            "\t.string \"Никто не сравнится со мной\\l\"\n"
            "\t.string \"в битвах ледяных ПОКЕМОНОВ.\\p\"\n"
            "\t.string \"Замораживающие приёмы очень сильны.\\p\"\n"
            "\t.string \"Твои ПОКЕМОНЫ будут беспомощны,\\n\"\n"
            "\t.string \"когда замёрзнут насквозь.\\p\"\n"
            "\t.string \"Ха-ха-ха!\\n\"\n"
            "\t.string \"Ты готов?{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        ),
    },
    Path("data/maps/PokemonLeague_BrunosRoom_Frlg/scripts.inc"): {
        "PokemonLeague_BrunosRoom_Text_RematchIntro": (
            "PokemonLeague_BrunosRoom_Text_RematchIntro::\n"
            "\t.string \"I am BRUNO of the ELITE FOUR!\\p\"\n"
            "\t.string \"Through rigorous training, people\\n\"\n"
            "\t.string \"and POKéMON can become stronger\\l\"\n"
            "\t.string \"without limit.\\p\"\n"
            "\t.string \"I've lived and trained with my\\n\"\n"
            "\t.string \"fighting POKéMON!\\l\"\n"
            "\t.string \"And that will never change!\\p\"\n"
            "\t.string \"{PLAYER}!\\p\"\n"
            "\t.string \"We will grind you down with our\\n\"\n"
            "\t.string \"superior power!\\p\"\n"
            "\t.string \"Hoo hah!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
            "PokemonLeague_BrunosRoom_Text_RematchIntro::\n"
            "\t.string \"Я BRUNO из ЭЛИТНОЙ ЧЕТВЁРКИ!\\p\"\n"
            "\t.string \"Упорные тренировки делают людей\\n\"\n"
            "\t.string \"и ПОКЕМОНОВ всё сильнее,\\l\"\n"
            "\t.string \"без предела.\\p\"\n"
            "\t.string \"Я жил и тренировался вместе\\n\"\n"
            "\t.string \"со своими боевыми ПОКЕМОНАМИ!\\l\"\n"
            "\t.string \"И это никогда не изменится!\\p\"\n"
            "\t.string \"{PLAYER}!\\p\"\n"
            "\t.string \"Мы сокрушим тебя нашей\\n\"\n"
            "\t.string \"непревзойдённой силой!\\p\"\n"
            "\t.string \"Ха!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        ),
    },
    Path("data/maps/PokemonLeague_AgathasRoom_Frlg/scripts.inc"): {
        "PokemonLeague_AgathasRoom_Text_RematchIntro": (
            "PokemonLeague_AgathasRoom_Text_RematchIntro::\n"
            "\t.string \"I am AGATHA of the ELITE FOUR.\\p\"\n"
            "\t.string \"You're the child that OAK's taken\\n\"\n"
            "\t.string \"under his wing, aren't you?\\p\"\n"
            "\t.string \"That old duff was once tough and\\n\"\n"
            "\t.string \"handsome.\\p\"\n"
            "\t.string \"But that was decades ago.\\n\"\n"
            "\t.string \"He's a shadow of his former self.\\p\"\n"
            "\t.string \"Now he just wants to fiddle with\\n\"\n"
            "\t.string \"his POKéDEX.\\p\"\n"
            "\t.string \"He's wrong.\\n\"\n"
            "\t.string \"POKéMON are for battling!\\p\"\n"
            "\t.string \"{PLAYER}! I'll show you how a real\\n\"\n"
            "\t.string \"TRAINER battles!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
            "PokemonLeague_AgathasRoom_Text_RematchIntro::\n"
            "\t.string \"Я AGATHA из ЭЛИТНОЙ ЧЕТВЁРКИ.\\p\"\n"
            "\t.string \"Ты тот ребёнок, которого OAK\\n\"\n"
            "\t.string \"взял под своё крыло, верно?\\p\"\n"
            "\t.string \"Когда-то этот старик был сильным\\n\"\n"
            "\t.string \"и красавцем.\\p\"\n"
            "\t.string \"Но это было десятки лет назад.\\n\"\n"
            "\t.string \"Теперь он лишь тень прежнего себя.\\p\"\n"
            "\t.string \"Сейчас ему нужен только\\n\"\n"
            "\t.string \"его ПОКЕДЕКС.\\p\"\n"
            "\t.string \"Он ошибается.\\n\"\n"
            "\t.string \"ПОКЕМОНЫ созданы для битв!\\p\"\n"
            "\t.string \"{PLAYER}! Я покажу, как сражается\\n\"\n"
            "\t.string \"настоящий ТРЕНЕР!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        ),
    },
    Path("data/maps/PokemonLeague_LancesRoom_Frlg/scripts.inc"): {
        "PokemonLeague_LancesRoom_Text_RematchIntro": (
            "PokemonLeague_LancesRoom_Text_RematchIntro::\n"
            "\t.string \"Ah!\\n\"\n"
            "\t.string \"So, you've returned, {PLAYER}!\\p\"\n"
            "\t.string \"I lead the ELITE FOUR.\\p\"\n"
            "\t.string \"You can call me LANCE the dragon\\n\"\n"
            "\t.string \"TRAINER.\\p\"\n"
            "\t.string \"You know that dragons are\\n\"\n"
            "\t.string \"mythical POKéMON.\\p\"\n"
            "\t.string \"They're hard to catch and raise,\\n\"\n"
            "\t.string \"but their powers are superior.\\p\"\n"
            "\t.string \"They're virtually indestructible.\\n\"\n"
            "\t.string \"There's no being clever with them.\\p\"\n"
            "\t.string \"Well, are you ready to lose?\\p\"\n"
            "\t.string \"Your LEAGUE challenge ends with\\n\"\n"
            "\t.string \"me, {PLAYER}!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
            "PokemonLeague_LancesRoom_Text_RematchIntro::\n"
            "\t.string \"А!\\n\"\n"
            "\t.string \"Ты вернулся, {PLAYER}!\\p\"\n"
            "\t.string \"Я возглавляю ЭЛИТНУЮ ЧЕТВЁРКУ.\\p\"\n"
            "\t.string \"Зови меня LANCE, ТРЕНЕРОМ\\n\"\n"
            "\t.string \"драконов.\\p\"\n"
            "\t.string \"Ты знаешь, что драконы -\\n\"\n"
            "\t.string \"мифические ПОКЕМОНЫ.\\p\"\n"
            "\t.string \"Их трудно ловить и растить,\\n\"\n"
            "\t.string \"но их сила огромна.\\p\"\n"
            "\t.string \"Они почти неуязвимы.\\n\"\n"
            "\t.string \"Хитростью их не одолеть.\\p\"\n"
            "\t.string \"Ну что, готов проиграть?\\p\"\n"
            "\t.string \"Твой вызов ЛИГЕ закончится здесь,\\n\"\n"
            "\t.string \"со мной, {PLAYER}!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$\"\n",
        ),
    },
    Path("data/maps/PokemonLeague_ChampionsRoom_Frlg/scripts.inc"): {
        "PokemonLeague_ChampionsRoom_Text_RematchIntro": (
            "PokemonLeague_ChampionsRoom_Text_RematchIntro::\n"
            "\t.string \"{RIVAL}: Hey, {PLAYER}!\\p\"\n"
            "\t.string \"You came back, {PLAYER}!\\n\"\n"
            "\t.string \"Hahah, that is so great!\\p\"\n"
            "\t.string \"My rival should be strong to keep\\n\"\n"
            "\t.string \"me sharp.\\p\"\n"
            "\t.string \"While working on my POKéDEX, I\\n\"\n"
            "\t.string \"looked all over for POKéMON.\\p\"\n"
            "\t.string \"Not only that, I assembled teams\\n\"\n"
            "\t.string \"that would beat any POKéMON type.\\p\"\n"
            "\t.string \"And now…\\p\"\n"
            "\t.string \"I'm the POKéMON LEAGUE CHAMPION!\\p\"\n"
            "\t.string \"{PLAYER}!\\n\"\n"
            "\t.string \"Do you know what that means?\\p\"\n"
            "\t.string \"I'll tell you.\\p\"\n"
            "\t.string \"I am the most powerful TRAINER in\\n\"\n"
            "\t.string \"the world!$\"\n",
            "PokemonLeague_ChampionsRoom_Text_RematchIntro::\n"
            "\t.string \"{RIVAL}: Эй, {PLAYER}!\\p\"\n"
            "\t.string \"Ты вернулся, {PLAYER}!\\n\"\n"
            "\t.string \"Ха-ха, отлично!\\p\"\n"
            "\t.string \"Мой соперник должен быть сильным,\\n\"\n"
            "\t.string \"чтобы я не терял форму.\\p\"\n"
            "\t.string \"Работая над ПОКЕДЕКСОМ, я\\n\"\n"
            "\t.string \"искал ПОКЕМОНОВ повсюду.\\p\"\n"
            "\t.string \"Я собрал команды, способные\\n\"\n"
            "\t.string \"победить любой тип ПОКЕМОНОВ.\\p\"\n"
            "\t.string \"И теперь...\\p\"\n"
            "\t.string \"Я снова ЧЕМПИОН ЛИГИ ПОКЕМОНОВ!\\p\"\n"
            "\t.string \"{PLAYER}!\\n\"\n"
            "\t.string \"Знаешь, что это значит?\\p\"\n"
            "\t.string \"Я скажу тебе.\\p\"\n"
            "\t.string \"Я самый сильный ТРЕНЕР\\n\"\n"
            "\t.string \"в мире!$\"\n",
        ),
    },
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_league_rematches_v3_43.py <upstream-root>")
    root = Path(sys.argv[1])
    applied = []

    for rel, file_patches in PATCHES.items():
        path = root / rel
        text = path.read_text(encoding="utf-8")
        for label, (pinned, ru) in file_patches.items():
            variants = [pinned]
            normalized = pinned.replace("é", "e").replace("É", "E").replace("…", "...")
            if normalized != pinned:
                variants.append(normalized)
            hits = [(variant, text.count(variant)) for variant in variants]
            total = sum(count for _, count in hits)
            if total != 1:
                raise SystemExit(f"{MARKER}: {label}: expected exactly one pinned/normalized anchor, found {total}")
            source = next(variant for variant, count in hits if count == 1)
            text = text.replace(source, ru, 1)
            applied.append({"file": str(rel), "label": label})
        path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_pokemon_league_rematches_v3_43_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "firstClearTouched": False,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} verified Pokemon League rematch intro blocks; first-clear and Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
