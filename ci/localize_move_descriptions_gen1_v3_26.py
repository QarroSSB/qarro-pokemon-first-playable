#!/usr/bin/env python3
"""Qarro v3.26 system localization: Generation I Move descriptions.

Only user-facing Move descriptions from MOVE_POUND through MOVE_STRUGGLE are
translated. Move names remain English by project policy. The pass is bounded
before MOVE_SKETCH (first Gen II move), fails closed on source drift, and does
not touch move mechanics, trainer data, species names, Ability names, Ash Bond,
or Ash Cap.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_MOVES_GEN1_V3_26"

DATA = r"""POUND|Бьет врага лапами|или хвостом.
KARATE_CHOP|Рубящий удар с высоким|шансом критического удара.
DOUBLE_SLAP|Бьет врага подряд|от 2 до 5 раз.
COMET_PUNCH|Бьет врага кулаками|от 2 до 5 раз.
MEGA_PUNCH|Очень мощный удар|кулаком.
PAY_DAY|Бросает монеты во врага.|После боя дает деньги.
FIRE_PUNCH|Огненный удар кулаком.|Может обжечь врага.
ICE_PUNCH|Ледяной удар кулаком.|Может заморозить врага.
THUNDER_PUNCH|Электрический удар.|Может парализовать.
SCRATCH|Царапает врага|острыми когтями.
VISE_GRIP|Сжимает врага|мощными клешнями.
GUILLOTINE|Может нокаутировать|врага одним ударом.
RAZOR_WIND|Копит силу, затем бьет.|Высокий шанс крита.
SWORDS_DANCE|Резко повышает|Атаку пользователя.
CUT|Режет врага|когтями или лезвием.
GUST|Атакует врага|сильным порывом ветра.
WING_ATTACK|Наносит удар|расправленными крыльями.
WHIRLWIND|Сдувает врага и меняет|его на другого покемона.
FLY|Взлетает в первый ход,|атакует во второй.
BIND|Связывает и ранит врага|несколько ходов.
SLAM|Бьет врага длинным|хвостом или телом.
VINE_WHIP|Хлещет врага|тонкими лозами.
STOMP|Топчет врага.|Может заставить дрогнуть.
DOUBLE_KICK|Дважды подряд|пинает врага.
MEGA_KICK|Очень мощный удар|ногой.
JUMP_KICK|Прыжковый удар ногой.|Промах ранит пользователя.
ROLLING_KICK|Быстрый вращающийся удар.|Может заставить дрогнуть.
SAND_ATTACK|Бросает песок и снижает|Точность врага.
HEADBUTT|Бьет врага головой.|Может заставить дрогнуть.
HORN_ATTACK|Пронзает врага|острым рогом.
FURY_ATTACK|Бьет рогом подряд|от 2 до 5 раз.
HORN_DRILL|Может нокаутировать|врага одним ударом.
TACKLE|Атакует врага|всем телом.
BODY_SLAM|Наваливается всем телом.|Может парализовать.
WRAP|Обвивает и ранит врага|несколько ходов.
TAKE_DOWN|Мощная атака всем телом.|Часть урона идет обратно.
THRASH|Атакует 2-3 хода подряд,|затем путается.
DOUBLE_EDGE|Очень мощный таран.|Часть урона идет обратно.
TAIL_WHIP|Снижает Защиту врага|движениями хвоста.
POISON_STING|Жалит врага.|Может отравить.
TWINEEDLE|Дважды колет врага.|Может отравить.
PIN_MISSILE|Стреляет иглами|от 2 до 5 раз.
LEER|Пугает взглядом и снижает|Защиту врага.
BITE|Кусает врага.|Может заставить дрогнуть.
GROWL|Рычит и снижает|Атаку врага.
ROAR|Прогоняет врага и меняет|его на другого покемона.
SING|Поет колыбельную,|усыпляя врага.
SUPERSONIC|Странные звуки вызывают|замешательство.
SONIC_BOOM|Всегда наносит|ровно 20 урона.
DISABLE|Временно запрещает|последнюю атаку врага.
ACID|Обливает врага кислотой.|Может снизить Сп. Защиту.
EMBER|Атакует маленьким пламенем.|Может обжечь.
FLAMETHROWER|Атакует сильным пламенем.|Может обжечь.
MIST|Защищает команду|от снижения статов.
WATER_GUN|Стреляет во врага|сильной струей воды.
HYDRO_PUMP|Бьет врага мощной|струей воды.
SURF|Обрушивает на врагов|огромную волну.
ICE_BEAM|Атакует ледяным лучом.|Может заморозить.
BLIZZARD|Обрушивает сильную метель.|Может заморозить.
PSYBEAM|Атакует странным лучом.|Может запутать врага.
BUBBLE_BEAM|Бьет струей пузырей.|Может снизить Скорость.
AURORA_BEAM|Атакует радужным лучом.|Может снизить Атаку.
HYPER_BEAM|Очень мощный луч.|После него нужна перезарядка.
PECK|Клюет врага|острым клювом.
DRILL_PECK|Атакует вращающимся|острым клювом.
SUBMISSION|Жесткий бросок врага.|Часть урона идет обратно.
LOW_KICK|Чем тяжелее враг,|тем сильнее удар.
COUNTER|Возвращает вдвое больше|физического урона.
SEISMIC_TOSS|Наносит урон, равный|уровню пользователя.
STRENGTH|Мощно атакует врага|всем телом.
ABSORB|Поглощает HP врага.|Лечит пользователя.
MEGA_DRAIN|Сильно поглощает HP врага.|Лечит пользователя.
LEECH_SEED|Семена каждый ход крадут|HP врага.
GROWTH|Повышает Атаку|и Сп. Атаку.
RAZOR_LEAF|Режет врага листьями.|Высокий шанс крита.
SOLAR_BEAM|Копит свет в первый ход,|атакует во второй.
POISON_POWDER|Ядовитая пыль|отравляет врага.
STUN_SPORE|Пыль со спорами|парализует врага.
SLEEP_POWDER|Сонная пыль|усыпляет врага.
PETAL_DANCE|Атакует 2-3 хода подряд,|затем путается.
STRING_SHOT|Опутывает нитями|и снижает Скорость.
DRAGON_RAGE|Всегда наносит|ровно 40 урона.
FIRE_SPIN|Окружает врага огнем|на несколько ходов.
THUNDER_SHOCK|Слабый электрический удар.|Может парализовать.
THUNDERBOLT|Сильный электрический удар.|Может парализовать.
THUNDER_WAVE|Слабый электрический заряд|парализует врага.
THUNDER|Мощная атака молнией.|Может парализовать.
ROCK_THROW|Бросает во врага|небольшой камень.
EARTHQUAKE|Мощное землетрясение|бьет всех вокруг.
FISSURE|Может нокаутировать|врага одним ударом.
DIG|Зарывается в первый ход,|атакует во второй.
TOXIC|Сильно отравляет врага.|Урон яда растет.
CONFUSION|Слабая психическая атака.|Может запутать врага.
PSYCHIC|Сильная психическая атака.|Может снизить Сп. Защиту.
HYPNOSIS|Гипнотизирует врага|и усыпляет его.
MEDITATE|Спокойно медитирует|и повышает Атаку.
AGILITY|Расслабляет тело|и резко повышает Скорость.
QUICK_ATTACK|Очень быстрая атака,|обычно бьет первой.
RAGE|Сила Атаки растет,|когда пользователя бьют.
TELEPORT|Позволяет сбежать|из боя с диким покемоном.
NIGHT_SHADE|Наносит урон, равный|уровню пользователя.
MIMIC|Копирует последнюю|атаку противника.
SCREECH|Резкий визг сильно снижает|Защиту врага.
DOUBLE_TEAM|Создает копии и повышает|Уклонение пользователя.
RECOVER|Восстанавливает|до половины максимального HP.
HARDEN|Укрепляет тело|и повышает Защиту.
MINIMIZE|Сильно уменьшает тело|и резко повышает Уклонение.
SMOKESCREEN|Дым снижает|Точность врага.
CONFUSE_RAY|Странный луч|запутывает врага.
WITHDRAW|Прячется в панцирь|и повышает Защиту.
DEFENSE_CURL|Сворачивается и повышает|Защиту пользователя.
BARRIER|Создает барьер и резко|повышает Защиту.
LIGHT_SCREEN|На 5 ходов снижает|урон специальных атак.
HAZE|Убирает все изменения|статов на поле.
REFLECT|На 5 ходов снижает|урон физических атак.
FOCUS_ENERGY|Сосредотачивается и повышает|шанс критического удара.
BIDE|Копит полученный урон,|затем возвращает его вдвое.
METRONOME|Случайно использует|почти любую атаку.
MIRROR_MOVE|Повторяет последнюю атаку,|направленную в пользователя.
SELF_DESTRUCT|Мощный взрыв.|Пользователь теряет сознание.
EGG_BOMB|Бросает во врага|большое яйцо.
LICK|Лижет врага.|Может парализовать.
SMOG|Грязный газ бьет врага.|Может отравить.
SLUDGE|Бросает грязь во врага.|Может отравить.
BONE_CLUB|Бьет врага костью.|Может заставить дрогнуть.
FIRE_BLAST|Атакует мощным пламенем.|Может обжечь.
WATERFALL|Несется на врага с водой.|Может заставить дрогнуть.
CLAMP|Зажимает врага|на несколько ходов.
SWIFT|Стреляет звездными лучами.|Атака не промахивается.
SKULL_BASH|Сначала повышает Защиту,|затем атакует головой.
SPIKE_CANNON|Стреляет шипами|от 2 до 5 раз.
CONSTRICT|Сжимает врага.|Может снизить Скорость.
AMNESIA|Забывает заботы и резко|повышает Сп. Защиту.
KINESIS|Сгибает ложку и снижает|Точность врага.
SOFT_BOILED|Восстанавливает|до половины максимального HP.
HIGH_JUMP_KICK|Мощный прыжковый удар.|Промах ранит пользователя.
GLARE|Страшный взгляд|парализует врага.
DREAM_EATER|Бьет только спящего врага|и восстанавливает HP.
POISON_GAS|Ядовитый газ|отравляет врага.
BARRAGE|Бросает снаряды|от 2 до 5 раз.
LEECH_LIFE|Поглощает HP врага.|Лечит пользователя.
LOVELY_KISS|Страшный поцелуй|усыпляет врага.
SKY_ATTACK|Копит силу, затем бьет.|Может заставить дрогнуть.
TRANSFORM|Превращается во врага,|копируя его данные.
BUBBLE|Атакует пузырями.|Может снизить Скорость.
DIZZY_PUNCH|Ритмичный удар кулаком.|Может запутать врага.
SPORE|Рассыпает споры|и усыпляет врага.
FLASH|Яркая вспышка снижает|Точность врага.
PSYWAVE|Наносит случайный урон,|зависящий от уровня.
SPLASH|Просто плещется.|Ничего не происходит.
ACID_ARMOR|Меняет структуру тела|и резко повышает Защиту.
CRABHAMMER|Бьет большой клешней.|Высокий шанс крита.
EXPLOSION|Чудовищный взрыв.|Пользователь теряет сознание.
FURY_SWIPES|Царапает врага|от 2 до 5 раз.
BONEMERANG|Бросает кость,|которая бьет дважды.
REST|Полностью лечит HP и статус,|но усыпляет на 2 хода.
ROCK_SLIDE|Обрушивает большие камни.|Может заставить дрогнуть.
HYPER_FANG|Кусает острыми клыками.|Может заставить дрогнуть.
SHARPEN|Заостряет тело|и повышает Атаку.
CONVERSION|Меняет свой тип на тип|первой известной атаки.
TRI_ATTACK|Тройная атака может обжечь,|заморозить или парализовать.
SUPER_FANG|Снижает текущий HP врага|ровно наполовину.
SLASH|Режет острыми когтями.|Высокий шанс крита.
SUBSTITUTE|Тратит часть HP и создает|замену, принимающую урон.
STRUGGLE|Атакует без PP и ранит|самого пользователя."""

RU = {}
for raw in DATA.splitlines():
    parts = raw.split("|")
    if len(parts) != 3:
        raise SystemExit(f"[{MARKER}] ERROR: malformed translation row: {raw!r}")
    move, line1, line2 = parts
    if move in RU:
        raise SystemExit(f"[{MARKER}] ERROR: duplicate move: {move}")
    RU[move] = (line1, line2)
ORDER = list(RU)


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def render_description(lines: tuple[str, str]) -> str:
    return (
        '.description = COMPOUND_STRING(\n'
        f'            "{lines[0]}\\n"\n'
        f'            "{lines[1]}"),' 
    )


def get_block(text: str, move: str, next_move: str) -> tuple[int, int, str]:
    start_token = f"[MOVE_{move}] ="
    end_token = f"[MOVE_{next_move}] ="
    start = text.find(start_token)
    if start < 0:
        die(f"missing move block {move}")
    end = text.find(end_token, start + len(start_token))
    if end < 0:
        die(f"could not bound move block {move} before {next_move}")
    return start, end, text[start:end]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    path = root / "src/data/moves_info.h"
    if not path.is_file():
        die(f"missing {path}")
    text = path.read_text(encoding="utf-8")

    if len(RU) != 165 or ORDER[0] != "POUND" or ORDER[-1] != "STRUGGLE":
        die(f"translation table boundary/count drift: count={len(RU)}")
    if "[MOVE_SKETCH] =" not in text:
        die("missing MOVE_SKETCH Gen II boundary")

    changed = 0
    already = 0
    english_names = {}

    for idx, move in enumerate(ORDER):
        next_move = ORDER[idx + 1] if idx + 1 < len(ORDER) else "SKETCH"
        start, end, block = get_block(text, move, next_move)
        name_match = re.search(r'\.name\s*=\s*COMPOUND_STRING\("([^\"]+)"\)', block)
        if not name_match:
            die(f"English Move name missing in {move}")
        english_name = name_match.group(1)
        english_names[move] = english_name

        wanted = render_description(RU[move])
        if wanted in block:
            already += 1
            continue

        pat = re.compile(r'(\n\s*\.description\s*=\s*)(.*?)(\n\s*\.effect\s*=)', re.S)
        matches = list(pat.finditer(block))
        if len(matches) != 1:
            die(f"{move}: expected one description before effect, got {len(matches)}")
        block2 = pat.sub(lambda m: "\n        " + wanted + m.group(3), block, count=1)
        if f'.name = COMPOUND_STRING("{english_name}")' not in block2:
            die(f"{move}: English name changed unexpectedly")
        text = text[:start] + block2 + text[end:]
        changed += 1

    for idx, move in enumerate(ORDER):
        next_move = ORDER[idx + 1] if idx + 1 < len(ORDER) else "SKETCH"
        _, _, block = get_block(text, move, next_move)
        wanted = render_description(RU[move])
        if wanted not in block:
            die(f"{move}: Russian description missing after patch")
        if f'.name = COMPOUND_STRING("{english_names[move]}")' not in block:
            die(f"{move}: English name missing after patch")
        desc_match = re.search(r'\.description\s*=\s*(.*?)(?=\n\s*\.effect\s*=)', block, re.S)
        if not desc_match or not re.search(r'[А-Яа-я]', desc_match.group(1)):
            die(f"{move}: no Cyrillic found in localized description")

    path.write_text(text, encoding="utf-8")
    report = {
        "marker": MARKER,
        "category": "Move descriptions",
        "generation": "I",
        "firstMove": "MOVE_POUND",
        "lastMove": "MOVE_STRUGGLE",
        "movesLocalized": len(RU),
        "blocksChanged": changed,
        "blocksAlreadyLocalized": already,
        "moveNamesEnglish": True,
        "abilityNamesTouched": False,
        "speciesNamesTouched": False,
        "moveMechanicsTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_moves_gen1_v3_26_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: {len(RU)} Gen I Move descriptions localized; "
        "Move names remain English; mechanics and Ash protections unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
