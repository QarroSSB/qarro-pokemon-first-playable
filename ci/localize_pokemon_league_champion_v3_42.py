#!/usr/bin/env python3
"""Qarro v3.42 mandatory Pokemon League / Champion Russian runtime localization.

Translates only the verified pinned first-clear Champion progression chain:
Champion intro, defeat/post-battle, and Professor Oak transition to Hall of Fame.
Rematch intro is intentionally left untouched. Pokemon species / move / ability
proper names remain English. Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEMON_LEAGUE_CHAMPION_V3_42"
REL = Path("data/maps/PokemonLeague_ChampionsRoom_Frlg/scripts.inc")

PATCHES = {
    "PokemonLeague_ChampionsRoom_Text_Intro": (
        "PokemonLeague_ChampionsRoom_Text_Intro::\n"
        "\t.string \"{RIVAL}: Hey, {PLAYER}!\\p\"\n"
        "\t.string \"I was looking forward to seeing\\n\"\n"
        "\t.string \"you, {PLAYER}.\\p\"\n"
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
        "PokemonLeague_ChampionsRoom_Text_Intro::\n"
        "\t.string \"{RIVAL}: Эй, {PLAYER}!\\p\"\n"
        "\t.string \"Я ждал встречи с тобой,\\n\"\n"
        "\t.string \"{PLAYER}.\\p\"\n"
        "\t.string \"Мой соперник должен быть сильным,\\n\"\n"
        "\t.string \"чтобы я не терял форму.\\p\"\n"
        "\t.string \"Работая над ПОКЕДЕКСОМ, я\\n\"\n"
        "\t.string \"искал ПОКЕМОНОВ повсюду.\\p\"\n"
        "\t.string \"Я собрал команды, способные\\n\"\n"
        "\t.string \"победить любой тип ПОКЕМОНОВ.\\p\"\n"
        "\t.string \"И теперь...\\p\"\n"
        "\t.string \"Я ЧЕМПИОН ЛИГИ ПОКЕМОНОВ!\\p\"\n"
        "\t.string \"{PLAYER}!\\n\"\n"
        "\t.string \"Знаешь, что это значит?\\p\"\n"
        "\t.string \"Я скажу тебе.\\p\"\n"
        "\t.string \"Я самый сильный ТРЕНЕР\\n\"\n"
        "\t.string \"в мире!$\"\n",
    ),
    "PokemonLeague_ChampionsRoom_Text_Defeat": (
        "PokemonLeague_ChampionsRoom_Text_Defeat::\n"
        "\t.string \"NO!\\n\"\n"
        "\t.string \"That can't be!\\l\"\n"
        "\t.string \"You beat me at my best!\\p\"\n"
        "\t.string \"After all that work to become\\n\"\n"
        "\t.string \"the LEAGUE CHAMP?\\p\"\n"
        "\t.string \"My reign is over already?\\n\"\n"
        "\t.string \"It's not fair!$\"\n",
        "PokemonLeague_ChampionsRoom_Text_Defeat::\n"
        "\t.string \"НЕТ!\\n\"\n"
        "\t.string \"Не может быть!\\l\"\n"
        "\t.string \"Ты победил меня в лучшей форме!\\p\"\n"
        "\t.string \"После всего, что я сделал, чтобы\\n\"\n"
        "\t.string \"стать ЧЕМПИОНОМ ЛИГИ?\\p\"\n"
        "\t.string \"Моё правление уже окончено?\\n\"\n"
        "\t.string \"Это нечестно!$\"\n",
    ),
    "PokemonLeague_ChampionsRoom_Text_PostBattle": (
        "PokemonLeague_ChampionsRoom_Text_PostBattle::\n"
        "\t.string \"Why?\\n\"\n"
        "\t.string \"Why did I lose?\\p\"\n"
        "\t.string \"I never made any mistakes raising\\n\"\n"
        "\t.string \"my POKéMON…\\p\"\n"
        "\t.string \"Darn it! You're the new POKéMON\\n\"\n"
        "\t.string \"LEAGUE CHAMPION!\\p\"\n"
        "\t.string \"Although I don't like to admit it…$\"\n",
        "PokemonLeague_ChampionsRoom_Text_PostBattle::\n"
        "\t.string \"Почему?\\n\"\n"
        "\t.string \"Почему я проиграл?\\p\"\n"
        "\t.string \"Я не допускал ошибок, выращивая\\n\"\n"
        "\t.string \"своих ПОКЕМОНОВ...\\p\"\n"
        "\t.string \"Чёрт! Теперь ты новый ЧЕМПИОН\\n\"\n"
        "\t.string \"ЛИГИ ПОКЕМОНОВ!\\p\"\n"
        "\t.string \"Хоть мне и не хочется это признавать...$\"\n",
    ),
    "PokemonLeague_ChampionsRoom_Text_OakPlayer": (
        "PokemonLeague_ChampionsRoom_Text_OakPlayer::\n"
        "\t.string \"OAK: {PLAYER}!$\"\n",
        "PokemonLeague_ChampionsRoom_Text_OakPlayer::\n"
        "\t.string \"OAK: {PLAYER}!$\"\n",
    ),
    "PokemonLeague_ChampionsRoom_Text_OakCongratulations": (
        "PokemonLeague_ChampionsRoom_Text_OakCongratulations::\n"
        "\t.string \"OAK: So, you've won!\\n\"\n"
        "\t.string \"Sincerely, congratulations!\\p\"\n"
        "\t.string \"You're the new POKéMON LEAGUE\\n\"\n"
        "\t.string \"CHAMPION!\\p\"\n"
        "\t.string \"You've grown up so much since you\\n\"\n"
        "\t.string \"first left with {STR_VAR_1} to work\\l\"\n"
        "\t.string \"on the POKéDEX.\\p\"\n"
        "\t.string \"{PLAYER}, you have come of age!$\"\n",
        "PokemonLeague_ChampionsRoom_Text_OakCongratulations::\n"
        "\t.string \"OAK: Итак, ты победил!\\n\"\n"
        "\t.string \"Искренне поздравляю!\\p\"\n"
        "\t.string \"Ты новый ЧЕМПИОН\\n\"\n"
        "\t.string \"ЛИГИ ПОКЕМОНОВ!\\p\"\n"
        "\t.string \"Ты так вырос с тех пор, как впервые\\n\"\n"
        "\t.string \"ушёл с {STR_VAR_1}, чтобы работать\\l\"\n"
        "\t.string \"над ПОКЕДЕКСОМ.\\p\"\n"
        "\t.string \"{PLAYER}, ты стал настоящим ТРЕНЕРОМ!$\"\n",
    ),
    "PokemonLeague_ChampionsRoom_Text_OakImDisappointedRival": (
        "PokemonLeague_ChampionsRoom_Text_OakImDisappointedRival::\n"
        "\t.string \"OAK: {RIVAL}…\\n\"\n"
        "\t.string \"I'm disappointed in you.\\p\"\n"
        "\t.string \"I came when I heard you'd beaten\\n\"\n"
        "\t.string \"the ELITE FOUR.\\p\"\n"
        "\t.string \"But, when I got here, you had\\n\"\n"
        "\t.string \"already lost!\\p\"\n"
        "\t.string \"{RIVAL}, do you understand why\\n\"\n"
        "\t.string \"you lost?\\p\"\n"
        "\t.string \"You have forgotten to treat your\\n\"\n"
        "\t.string \"POKéMON with love and trust.\\p\"\n"
        "\t.string \"Without them, you will never\\n\"\n"
        "\t.string \"become a CHAMP again!$\"\n",
        "PokemonLeague_ChampionsRoom_Text_OakImDisappointedRival::\n"
        "\t.string \"OAK: {RIVAL}...\\n\"\n"
        "\t.string \"Я разочарован в тебе.\\p\"\n"
        "\t.string \"Я пришёл, когда услышал, что ты\\n\"\n"
        "\t.string \"победил ЭЛИТНУЮ ЧЕТВЁРКУ.\\p\"\n"
        "\t.string \"Но когда я добрался сюда, ты\\n\"\n"
        "\t.string \"уже проиграл!\\p\"\n"
        "\t.string \"{RIVAL}, ты понимаешь, почему\\n\"\n"
        "\t.string \"проиграл?\\p\"\n"
        "\t.string \"Ты забыл относиться к своим\\n\"\n"
        "\t.string \"ПОКЕМОНАМ с любовью и доверием.\\p\"\n"
        "\t.string \"Без этого тебе больше не стать\\n\"\n"
        "\t.string \"ЧЕМПИОНОМ!$\"\n",
    ),
    "PokemonLeague_ChampionsRoom_Text_OakPlayerComeWithMe": (
        "PokemonLeague_ChampionsRoom_Text_OakPlayerComeWithMe::\n"
        "\t.string \"OAK: {PLAYER}.\\p\"\n"
        "\t.string \"You understand that your victory\\n\"\n"
        "\t.string \"was not just your own doing.\\p\"\n"
        "\t.string \"The bond you share with your\\n\"\n"
        "\t.string \"POKéMON is marvelous.\\p\"\n"
        "\t.string \"{PLAYER}!\\n\"\n"
        "\t.string \"Come with me!$\"\n",
        "PokemonLeague_ChampionsRoom_Text_OakPlayerComeWithMe::\n"
        "\t.string \"OAK: {PLAYER}.\\p\"\n"
        "\t.string \"Пойми: эта победа - не только\\n\"\n"
        "\t.string \"твоя заслуга.\\p\"\n"
        "\t.string \"Связь между тобой и твоими\\n\"\n"
        "\t.string \"ПОКЕМОНАМИ прекрасна.\\p\"\n"
        "\t.string \"{PLAYER}!\\n\"\n"
        "\t.string \"Идём со мной!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_league_champion_v3_42.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied = []

    for label, (pinned, ru) in PATCHES.items():
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
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_pokemon_league_champion_v3_42_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "rematchIntroTouched": False,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Champion/Hall-of-Fame transition runtime blocks; rematch intro and Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
