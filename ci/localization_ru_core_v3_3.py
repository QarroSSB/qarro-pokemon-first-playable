#!/usr/bin/env python3
"""Qarro Russian localization bootstrap + phase-1 descriptions.

Keep the exact green v3.4 core localization from commit f7f5d677, then add
concise Russian descriptions for the historically prepared Brock/Misty move
and ability set. Pokemon, Move and Ability proper names stay English.

No Ash Bond / Ash Cap changes.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "f7f5d67773203ef16e32e827167fa10f2886a215"
BASE_PATH = "ci/localization_ru_core_v3_3.py"
MARKER = "QARRO_RU_DESC_V3_5"

MOVE_DESCRIPTIONS = {
    "MOVE_EARTHQUAKE": ("Мощное землетрясение.", "Бьёт всех вокруг."),
    "MOVE_ROCK_POLISH": ("Резко повышает", "Скорость пользователя."),
    "MOVE_ROCK_SLIDE": ("Обрушивает камни.", "Может вызвать испуг."),
    "MOVE_EXPLOSION": ("Наносит огромный урон.", "Пользователь падает."),
    "MOVE_ICE_FANG": ("Ледяной укус. Может", "заморозить или испугать."),
    "MOVE_THUNDER_FANG": ("Электрический укус.", "Паралич или испуг."),
    "MOVE_CRUNCH": ("Сильный укус. Может", "снизить Защиту цели."),
    "MOVE_DRAGON_DANCE": ("Повышает Атаку", "и Скорость пользователя."),
    "MOVE_SURF": ("Мощная волна бьёт", "всех вокруг пользователя."),
    "MOVE_ICE_BEAM": ("Ледяной луч. Может", "заморозить цель."),
    "MOVE_EARTH_POWER": ("Сила земли. Может", "снизить Сп. защиту."),
    "MOVE_SHELL_SMASH": ("Резко усиливает атаку", "и Скорость, снижая защиту."),
    "MOVE_TOXIC": ("Сильно отравляет цель.", "Урон растёт каждый ход."),
    "MOVE_RECOVER": ("Восстанавливает", "половину максимальных HP."),
    "MOVE_GIGA_DRAIN": ("Высасывает HP цели", "и лечит пользователя."),
    "MOVE_ANCIENT_POWER": ("Древняя сила. Может", "повысить все параметры."),
    "MOVE_DRAIN_PUNCH": ("Удар лечит пользователя", "частью нанесённого урона."),
    "MOVE_THUNDER_WAVE": ("Электрическая волна", "парализует цель."),
    "MOVE_CURSE": ("Повышает Атаку и Защиту,", "но снижает Скорость."),
    "MOVE_STEALTH_ROCK": ("Камни ранят врагов", "при выходе на поле."),
    "MOVE_GYRO_BALL": ("Чем медленнее покемон,", "тем сильнее атака."),
    "MOVE_DRAGON_TAIL": ("Удар хвостом вынуждает", "цель покинуть поле."),
    "MOVE_ENCORE": ("Цель повторяет", "последнюю атаку."),
    "MOVE_ROCK_TOMB": ("Обрушивает камни", "и снижает Скорость цели."),
    "MOVE_PROTECT": ("Защищает от большинства", "атак в этот ход."),
    "MOVE_REST": ("Полностью лечит HP и статус,", "но усыпляет пользователя."),
    "MOVE_STONE_EDGE": ("Острые камни. Высокий", "шанс критического удара."),
    "MOVE_HYDRO_PUMP": ("Мощнейшая струя воды", "обрушивается на цель."),
    "MOVE_SCALD": ("Обдаёт цель кипятком.", "Может вызвать ожог."),
    "MOVE_HYPNOSIS": ("Гипноз погружает", "цель в сон."),
    "MOVE_PERISH_SONG": ("Услышавшие песню падут", "через 3 хода без смены."),
    "MOVE_DRAGON_PULSE": ("Ударная волна", "драконьей энергии."),
    "MOVE_RAIN_DANCE": ("Вызывает дождь", "на несколько ходов."),
    "MOVE_PSYCHIC": ("Психическая атака. Может", "снизить Сп. защиту."),
    "MOVE_TELEKINESIS": ("Поднимает цель и делает", "атаки по ней точнее."),
    "MOVE_WATERFALL": ("Водный таран. Может", "заставить цель дрогнуть."),
    "MOVE_BOUNCE": ("Взлетает и бьёт позже.", "Может парализовать."),
    "MOVE_CALM_MIND": ("Повышает Сп. атаку", "и Сп. защиту."),
    "MOVE_THUNDERBOLT": ("Сильный разряд. Может", "парализовать цель."),
    "MOVE_THUNDER": ("Мощнейшая молния. Может", "парализовать цель."),
    "MOVE_RAPID_SPIN": ("Атакует вращением", "и убирает ловушки."),
    "MOVE_SLACK_OFF": ("Восстанавливает", "половину максимальных HP."),
    "MOVE_ICICLE_SPEAR": ("Ледяные копья бьют", "от 2 до 5 раз."),
    "MOVE_ROCK_BLAST": ("Камни поражают цель", "от 2 до 5 раз."),
    "MOVE_RAZOR_SHELL": ("Режет острым панцирем.", "Может снизить Защиту."),
    "MOVE_OUTRAGE": ("Бьёт несколько ходов,", "затем вызывает смятение."),
    "MOVE_IRON_HEAD": ("Удар стальной головой.", "Может вызвать испуг."),
    "MOVE_EXTRASENSORY": ("Невидимая сила. Может", "заставить цель дрогнуть."),
}

ABILITY_DESCRIPTIONS = {
    "ABILITY_STURDY": ("При полном HP переживает", "удар, оставляя 1 HP."),
    "ABILITY_PRESSURE": ("Враг тратит больше PP", "на направленные атаки."),
    "ABILITY_SAND_STREAM": ("При выходе вызывает", "песчаную бурю."),
    "ABILITY_SHELL_ARMOR": ("Защищает покемона", "от критических ударов."),
    "ABILITY_STORM_DRAIN": ("Поглощает Водные атаки", "и повышает Сп. атаку."),
    "ABILITY_CLEAR_BODY": ("Не даёт противнику", "снижать параметры."),
    "ABILITY_LIGHTNING_ROD": ("Поглощает Электро-атаки", "и повышает Сп. атаку."),
    "ABILITY_DRIZZLE": ("При выходе вызывает", "дождь."),
    "ABILITY_SWIFT_SWIM": ("Во время дождя", "Скорость удваивается."),
    "ABILITY_NATURAL_CURE": ("Лечит статус покемона", "при уходе с поля."),
    "ABILITY_INTIMIDATE": ("При выходе снижает", "Атаку противников."),
    "ABILITY_VOLT_ABSORB": ("Электро-атаки лечат", "вместо нанесения урона."),
    "ABILITY_UNAWARE": ("Игнорирует изменения", "параметров противника."),
    "ABILITY_SKILL_LINK": ("Многоударные атаки", "всегда бьют максимум раз."),
    "ABILITY_REGENERATOR": ("При уходе восстанавливает", "треть максимальных HP."),
    "ABILITY_WATER_ABSORB": ("Водные атаки лечат", "вместо нанесения урона."),
}


def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    return subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )


def encode_description(lines: tuple[str, str]) -> str:
    if len(lines) != 2 or any(not line for line in lines):
        raise RuntimeError(f"invalid two-line description: {lines!r}")
    if any("—" in line or "…" in line for line in lines):
        raise RuntimeError(f"unsupported typography in description: {lines!r}")
    return lines[0].replace('"', '\\"') + "\\n" + lines[1].replace('"', '\\"')


def patch_table(path: Path, entries: dict[str, tuple[str, str]], prefix: str) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    for key, lines in entries.items():
        token = f"[{key}] ="
        start = text.find(token)
        if start < 0:
            raise RuntimeError(f"{path}: missing entry {key}")
        next_start = text.find(f"\n    [{prefix}", start + len(token))
        end = len(text) if next_start < 0 else next_start
        block = text[start:end]
        rx = re.compile(r"(?s)(\.description\s*=\s*COMPOUND_STRING\()(.*?)(\),)")
        matches = list(rx.finditer(block))
        if len(matches) != 1:
            raise RuntimeError(f"{path}: {key} expected one description, got {len(matches)}")
        encoded = encode_description(lines)
        replacement = f'.description = COMPOUND_STRING("{encoded}"),'
        current = matches[0].group(0)
        if current == replacement:
            continue
        block = block[:matches[0].start()] + replacement + block[matches[0].end():]
        text = text[:start] + block + text[end:]
        changed += 1
        print(f"[ru-desc] {key}: description localized")
    path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    code = load_base()
    ns = {
        "__name__": "qarro_ru_core_v34_base",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc:
        return rc

    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    moves = patch_table(root / "src/data/moves_info.h", MOVE_DESCRIPTIONS, "MOVE_")
    abilities = patch_table(root / "src/data/abilities.h", ABILITY_DESCRIPTIONS, "ABILITY_")

    audit = {
        "marker": MARKER,
        "moveDescriptionsLocalized": moves,
        "abilityDescriptionsLocalized": abilities,
        "pokemonNamesEnglish": True,
        "moveNamesEnglish": True,
        "abilityNamesEnglish": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_descriptions_v3_5_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: {moves} move + {abilities} ability descriptions localized; names/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
