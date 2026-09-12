#!/usr/bin/env python3
"""Qarro v3.27 system localization: Generation II Move descriptions.

Only user-facing Move descriptions from MOVE_SKETCH through MOVE_BEAT_UP are
translated. Move names remain English by project policy. The pass is bounded
before MOVE_FAKE_OUT (first Gen III move), fails closed on source drift, and
does not touch move mechanics, trainer data, species names, Ability names,
Ash Bond, or Ash Cap.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_MOVES_GEN2_V3_27"

DATA = r"""SKETCH|Навсегда копирует|последнюю атаку врага.
TRIPLE_KICK|Бьет ногой трижды.|Каждый удар сильнее.
THIEF|Атакует и крадет|предмет противника.
SPIDER_WEB|Опутывает врага сетью|и не дает смениться.
MIND_READER|Читает движения врага:|следующий удар точно попадет.
NIGHTMARE|Спящий враг теряет HP|каждый ход.
FLAME_WHEEL|Атакует огненным колесом.|Может обжечь.
SNORE|Работает только во сне.|Может заставить дрогнуть.
CURSE|Эффект зависит от того,|является ли тип Ghost.
FLAIL|Чем меньше осталось HP,|тем сильнее атака.
CONVERSION_2|Меняет свой тип, чтобы|сопротивляться прошлой атаке.
AEROBLAST|Воздушный удар с высоким|шансом критического удара.
COTTON_SPORE|Споры хлопка резко|снижают Скорость врага.
REVERSAL|Чем меньше осталось HP,|тем сильнее атака.
SPITE|Снижает PP последней|атаки противника.
POWDER_SNOW|Атакует снежной пылью.|Может заморозить.
PROTECT|Защищает от атак.|Повторять подряд сложнее.
MACH_PUNCH|Очень быстрый удар,|обычно бьет первым.
SCARY_FACE|Страшный взгляд резко|снижает Скорость врага.
FEINT_ATTACK|Подкрадывается к врагу.|Атака не промахивается.
SWEET_KISS|Милый поцелуй|запутывает врага.
BELLY_DRUM|Тратит половину HP,|резко повышая Атаку.
SLUDGE_BOMB|Бросает токсичную грязь.|Может отравить.
MUD_SLAP|Бросает грязь во врага.|Снижает Точность.
OCTAZOOKA|Стреляет чернилами.|Может снизить Точность.
SPIKES|Рассыпает шипы у врага,|раня входящих покемонов.
ZAP_CANNON|Мощный электрический удар.|При попадании парализует.
FORESIGHT|Позволяет бить Ghost|Normal и Fighting-атаками.
DESTINY_BOND|Если пользователь падет,|враг падет вместе с ним.
PERISH_SONG|Через 3 хода все, кто слышал,|теряют сознание.
ICY_WIND|Атакует ледяным ветром.|Снижает Скорость врага.
DETECT|Защищает от атак.|Повторять подряд сложнее.
BONE_RUSH|Бьет костью подряд|от 2 до 5 раз.
LOCK_ON|Берет врага на прицел:|следующий удар точно попадет.
OUTRAGE|Атакует 2-3 хода подряд,|затем путается.
SANDSTORM|Вызывает песчаную бурю|на несколько ходов.
GIGA_DRAIN|Поглощает HP врага.|Лечит пользователя.
ENDURE|Выдерживает смертельный удар|с минимум 1 HP.
CHARM|Очаровывает врага и резко|снижает его Атаку.
ROLLOUT|Катится и атакует 5 ходов.|С каждым ходом сильнее.
FALSE_SWIPE|Всегда оставляет врагу|как минимум 1 HP.
SWAGGER|Резко повышает Атаку врага,|но запутывает его.
MILK_DRINK|Восстанавливает|до половины максимального HP.
SPARK|Электрическая атака телом.|Может парализовать.
FURY_CUTTER|Атакует подряд, становясь|сильнее при каждом попадании.
STEEL_WING|Бьет стальными крыльями.|Может повысить Защиту.
MEAN_LOOK|Страшный взгляд не дает|противнику смениться.
ATTRACT|Влюбляет подходящего врага,|мешая ему атаковать.
SLEEP_TALK|Во сне случайно использует|одну из известных атак.
HEAL_BELL|Лечит статусные проблемы|всей команды.
RETURN|Сильнее при высокой|дружбе с тренером.
PRESENT|Дарит случайный эффект:|урон или лечение врага.
FRUSTRATION|Сильнее при низкой|дружбе с тренером.
SAFEGUARD|На 5 ходов защищает команду|от статусных проблем.
PAIN_SPLIT|Делит общий HP обоих|поровну между ними.
SACRED_FIRE|Атакует священным огнем.|Часто вызывает ожог.
MAGNITUDE|Сила землетрясения|случайно меняется.
DYNAMIC_PUNCH|Очень мощный удар.|При попадании путает.
MEGAHORN|Атакует врага|мощным рогом.
DRAGON_BREATH|Дышит на врага энергией.|Может парализовать.
BATON_PASS|Меняется с союзником,|передавая изменения статов.
ENCORE|Заставляет несколько ходов|повторять прошлую атаку.
PURSUIT|Атакует уходящего врага|до его смены.
RAPID_SPIN|Атакует вращением и убирает|ловушки и связывание.
SWEET_SCENT|Сладкий запах резко|снижает Уклонение врага.
IRON_TAIL|Бьет стальным хвостом.|Может снизить Защиту.
METAL_CLAW|Бьет стальными когтями.|Может повысить Атаку.
VITAL_THROW|Атакует после врага,|но не промахивается.
MORNING_SUN|Восстанавливает HP.|Лечение зависит от погоды.
SYNTHESIS|Восстанавливает HP.|Лечение зависит от погоды.
MOONLIGHT|Восстанавливает HP.|Лечение зависит от погоды.
HIDDEN_POWER|Тип атаки зависит|от данных покемона.
CROSS_CHOP|Крестовый удар с высоким|шансом критического удара.
TWISTER|Атакует вихрем.|Может заставить дрогнуть.
RAIN_DANCE|Вызывает дождь|на несколько ходов.
SUNNY_DAY|Вызывает солнце|на несколько ходов.
CRUNCH|Кусает острыми клыками.|Может снизить Защиту.
MIRROR_COAT|Возвращает вдвое больше|специального урона.
PSYCH_UP|Копирует изменения|статов противника.
EXTREME_SPEED|Очень быстрая мощная атака,|обычно бьет первой.
ANCIENT_POWER|Атакует древней силой.|Может повысить все статы.
SHADOW_BALL|Бросает теневой сгусток.|Может снизить Сп. Защиту.
FUTURE_SIGHT|Психический удар попадает|через несколько ходов.
ROCK_SMASH|Разбивает врага ударом.|Может снизить Защиту.
WHIRLPOOL|Запирает врага в водовороте|на несколько ходов.
BEAT_UP|Все здоровые союзники|по очереди атакуют врага."""

RU = {}
for raw in DATA.splitlines():
    parts = raw.split("|")
    if len(parts) != 3:
        raise SystemExit(f"[{MARKER}] ERROR: malformed translation row: {raw!r}")
    move, line1, line2 = parts
    if move in RU:
        raise SystemExit(f"[{MARKER}] ERROR: duplicate move: {move}")
    if len(line1) > 30 or len(line2) > 30:
        raise SystemExit(f"[{MARKER}] ERROR: overlong UI line for {move}: {len(line1)}/{len(line2)}")
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

    if len(RU) != 86 or ORDER[0] != "SKETCH" or ORDER[-1] != "BEAT_UP":
        die(f"translation table boundary/count drift: count={len(RU)}")
    if "[MOVE_FAKE_OUT] =" not in text:
        die("missing MOVE_FAKE_OUT Gen III boundary")

    changed = 0
    already = 0
    english_names = {}

    for idx, move in enumerate(ORDER):
        next_move = ORDER[idx + 1] if idx + 1 < len(ORDER) else "FAKE_OUT"
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
        next_move = ORDER[idx + 1] if idx + 1 < len(ORDER) else "FAKE_OUT"
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
        "generation": "II",
        "firstMove": "MOVE_SKETCH",
        "lastMove": "MOVE_BEAT_UP",
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
    out = root / "build/qarro_ru_moves_gen2_v3_27_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: {len(RU)} Gen II Move descriptions localized; "
        "Move names remain English; mechanics and Ash protections unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
