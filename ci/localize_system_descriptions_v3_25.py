#!/usr/bin/env python3
"""Qarro v3.25 system localization: Gen I-V Ability descriptions.

Only user-facing Ability descriptions are translated. Ability names remain
English by project policy. The pass is bounded at TERAVOLT (last Gen V
Ability), fails closed on source drift, and does not touch battle mechanics,
trainer data, species names, Move names, Ash Bond, or Ash Cap.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_SYSTEM_V3_25"

# Compact Russian wording is intentional: these strings are rendered in the
# GBA summary UI. Names remain English in the source blocks.
RU = {
    "NONE": "Нет способности.",
    "STENCH": "Атаки могут заставить дрогнуть.",
    "DRIZZLE": "Вызывает дождь в бою.",
    "SPEED_BOOST": "Скорость растет каждый ход.",
    "BATTLE_ARMOR": "Защищает от критических ударов.",
    "STURDY": "Защищает от нокаута с одного удара.",
    "DAMP": "Не дает покемонам взрываться.",
    "LIMBER": "Защищает от паралича.",
    "SAND_VEIL": "Повышает уклонение в песчаной буре.",
    "STATIC": "Контакт может парализовать врага.",
    "VOLT_ABSORB": "Электроатаки восстанавливают HP.",
    "WATER_ABSORB": "Водные атаки восстанавливают HP.",
    "OBLIVIOUS": "Защищает от влюбления и Taunt.",
    "CLOUD_NINE": "Отменяет эффекты погоды.",
    "COMPOUND_EYES": "Повышает точность атак.",
    "INSOMNIA": "Не дает уснуть.",
    "COLOR_CHANGE": "Меняет тип под атаку противника.",
    "IMMUNITY": "Защищает от отравления.",
    "FLASH_FIRE": "Усиливает Fire после Fire-атаки.",
    "SHIELD_DUST": "Блокирует доп. эффекты атак.",
    "OWN_TEMPO": "Защищает от замешательства.",
    "SUCTION_CUPS": "Не дает насильно сменить покемона.",
    "INTIMIDATE": "При выходе снижает Attack врагов.",
    "SHADOW_TAG": "Не дает противнику смениться.",
    "ROUGH_SKIN": "Ранит врага при контакте.",
    "WONDER_GUARD": "Пропускает лишь суперэффективные атаки.",
    "LEVITATE": "Дает иммунитет к Ground-атакам.",
    "EFFECT_SPORE": "Контакт может дать яд, сон или паралич.",
    "SYNCHRONIZE": "Передает ожог, паралич или яд врагу.",
    "CLEAR_BODY": "Не дает противнику снижать статы.",
    "NATURAL_CURE": "Лечит статус при смене.",
    "LIGHTNING_ROD": "Тянет Electric-атаки и повышает Sp. Atk.",
    "SERENE_GRACE": "Повышает шанс доп. эффектов.",
    "SWIFT_SWIM": "Повышает Speed под дождем.",
    "CHLOROPHYLL": "Повышает Speed на солнце.",
    "ILLUMINATE": "Не дает снизить точность.",
    "TRACE": "Копирует Ability противника.",
    "HUGE_POWER": "Удваивает Attack.",
    "POISON_POINT": "Контакт может отравить врага.",
    "INNER_FOCUS": "Защищает от вздрагивания.",
    "MAGMA_ARMOR": "Защищает от заморозки.",
    "WATER_VEIL": "Защищает от ожога.",
    "MAGNET_PULL": "Не дает Steel-покемонам уйти.",
    "SOUNDPROOF": "Дает иммунитет к звуковым атакам.",
    "RAIN_DISH": "Понемногу лечит HP под дождем.",
    "SAND_STREAM": "Вызывает песчаную бурю.",
    "PRESSURE": "Заставляет врага тратить больше PP.",
    "THICK_FAT": "Вдвое снижает урон Fire и Ice.",
    "EARLY_BIRD": "Просыпается вдвое быстрее.",
    "FLAME_BODY": "Контакт может обжечь врага.",
    "RUN_AWAY": "Гарантирует побег от дикого покемона.",
    "KEEN_EYE": "Не дает снизить точность.",
    "HYPER_CUTTER": "Не дает снизить Attack.",
    "PICKUP": "Может подбирать предметы.",
    "TRUANT": "Действует только через ход.",
    "HUSTLE": "Сила выше, но точность ниже.",
    "CUTE_CHARM": "Контакт может влюбить врага.",
    "PLUS": "С Minus повышает Sp. Atk.",
    "MINUS": "С Plus повышает Sp. Atk.",
    "FORECAST": "Меняет форму и тип по погоде.",
    "STICKY_HOLD": "Не дает отнять удерживаемый предмет.",
    "SHED_SKIN": "Может вылечить статус каждый ход.",
    "GUTS": "Статус повышает Attack.",
    "MARVEL_SCALE": "Статус повышает Defense.",
    "LIQUID_OOZE": "Поглощение HP ранит поглотителя.",
    "OVERGROW": "Усиливает Grass-атаки при низком HP.",
    "BLAZE": "Усиливает Fire-атаки при низком HP.",
    "TORRENT": "Усиливает Water-атаки при низком HP.",
    "SWARM": "Усиливает Bug-атаки при низком HP.",
    "ROCK_HEAD": "Убирает урон от отдачи.",
    "DROUGHT": "Вызывает солнечную погоду.",
    "ARENA_TRAP": "Не дает наземным врагам уйти.",
    "VITAL_SPIRIT": "Не дает уснуть.",
    "WHITE_SMOKE": "Не дает противнику снижать статы.",
    "PURE_POWER": "Удваивает Attack.",
    "SHELL_ARMOR": "Защищает от критических ударов.",
    "AIR_LOCK": "Отменяет эффекты погоды.",
    "TANGLED_FEET": "Повышает уклонение при замешательстве.",
    "MOTOR_DRIVE": "Electric-атаки повышают Speed.",
    "RIVALRY": "Пол влияет на силу атак.",
    "STEADFAST": "После вздрагивания повышает Speed.",
    "SNOW_CLOAK": "Повышает уклонение в снежную погоду.",
    "GLUTTONY": "Съедает ягоды раньше обычного.",
    "ANGER_POINT": "Критический удар резко повышает Attack.",
    "UNBURDEN": "После потери предмета удваивает Speed.",
    "HEATPROOF": "Вдвое снижает урон Fire.",
    "SIMPLE": "Удваивает изменения статов.",
    "DRY_SKIN": "Water лечит, Fire наносит больше урона.",
    "DOWNLOAD": "При выходе повышает подходящую атаку.",
    "IRON_FIST": "Усиливает ударные атаки кулаками.",
    "POISON_HEAL": "Яд восстанавливает HP.",
    "ADAPTABILITY": "Усиливает бонус атак своего типа.",
    "SKILL_LINK": "Многоударные атаки бьют максимум раз.",
    "HYDRATION": "Дождь лечит статус.",
    "SOLAR_POWER": "Солнце усиливает Sp. Atk, но тратит HP.",
    "QUICK_FEET": "Статус повышает Speed.",
    "NORMALIZE": "Все атаки становятся Normal-типа.",
    "SNIPER": "Усиливает критические удары.",
    "MAGIC_GUARD": "Получает урон только от атак.",
    "NO_GUARD": "Все атаки обеих сторон всегда попадают.",
    "STALL": "Всегда действует последним.",
    "TECHNICIAN": "Усиливает слабые атаки.",
    "LEAF_GUARD": "Солнце защищает от статуса.",
    "KLUTZ": "Не использует эффект удерживаемого предмета.",
    "MOLD_BREAKER": "Атаки игнорируют Ability врага.",
    "SUPER_LUCK": "Повышает шанс критического удара.",
    "AFTERMATH": "При нокауте ранит контактного врага.",
    "ANTICIPATION": "Чувствует опасные атаки врага.",
    "FOREWARN": "Показывает одну опасную атаку врага.",
    "UNAWARE": "Игнорирует изменения статов врага.",
    "TINTED_LENS": "Усиливает малоэффективные атаки.",
    "FILTER": "Ослабляет суперэффективный урон.",
    "SLOW_START": "В начале боя снижает Attack и Speed.",
    "SCRAPPY": "Normal и Fighting бьют Ghost.",
    "STORM_DRAIN": "Тянет Water-атаки и повышает Sp. Atk.",
    "ICE_BODY": "Понемногу лечит HP в снежную погоду.",
    "SOLID_ROCK": "Ослабляет суперэффективный урон.",
    "SNOW_WARNING": "Вызывает снежную погоду.",
    "HONEY_GATHER": "Может находить Honey.",
    "FRISK": "Показывает предмет противника.",
    "RECKLESS": "Усиливает атаки с отдачей.",
    "MULTITYPE": "Меняет тип Arceus по Plate.",
    "FLOWER_GIFT": "Солнце повышает Attack и Sp. Def союзников.",
    "BAD_DREAMS": "Ранит спящих противников.",
    "PICKPOCKET": "Крадет предмет атакующего при контакте.",
    "SHEER_FORCE": "Убирает доп. эффекты ради силы.",
    "CONTRARY": "Обращает изменения статов.",
    "UNNERVE": "Не дает врагам есть ягоды.",
    "DEFIANT": "Снижение статов резко повышает Attack.",
    "DEFEATIST": "При половине HP снижает Attack и Sp. Atk.",
    "CURSED_BODY": "Попадание может запретить атаку врага.",
    "HEALER": "Может вылечить статус союзника.",
    "FRIEND_GUARD": "Снижает урон по союзникам.",
    "WEAK_ARMOR": "Удар снижает Defense и повышает Speed.",
    "HEAVY_METAL": "Удваивает вес.",
    "LIGHT_METAL": "Вдвое снижает вес.",
    "MULTISCALE": "При полном HP снижает получаемый урон.",
    "TOXIC_BOOST": "Яд усиливает физические атаки.",
    "FLARE_BOOST": "Ожог усиливает специальные атаки.",
    "HARVEST": "Может восстановить использованную ягоду.",
    "TELEPATHY": "Уклоняется от атак союзников.",
    "MOODY": "Каждый ход случайно меняет статы.",
    "OVERCOAT": "Защищает от погоды и порошков.",
    "POISON_TOUCH": "Контактные атаки могут отравить.",
    "REGENERATOR": "Восстанавливает HP при смене.",
    "BIG_PECKS": "Не дает снизить Defense.",
    "SAND_RUSH": "Повышает Speed в песчаной буре.",
    "WONDER_SKIN": "Снижает точность статусных атак врага.",
    "ANALYTIC": "Усиливает атаку, если ходит последним.",
    "ILLUSION": "Маскируется под последнего союзника.",
    "IMPOSTER": "При выходе превращается во врага.",
    "INFILTRATOR": "Игнорирует защитные барьеры врага.",
    "MUMMY": "Передает Mummy при контакте.",
    "MOXIE": "Нокаут врага повышает Attack.",
    "JUSTIFIED": "Dark-атака повышает Attack.",
    "RATTLED": "Некоторые угрозы повышают Speed.",
    "MAGIC_BOUNCE": "Отражает статусные атаки.",
    "SAP_SIPPER": "Grass-атаки повышают Attack.",
    "PRANKSTER": "Дает приоритет статусным атакам.",
    "SAND_FORCE": "В песке усиливает Rock, Ground и Steel.",
    "IRON_BARBS": "Ранит врага при контакте.",
    "ZEN_MODE": "При низком HP меняет форму.",
    "VICTORY_STAR": "Повышает точность союзников.",
    "TURBOBLAZE": "Атаки игнорируют Ability врага.",
    "TERAVOLT": "Атаки игнорируют Ability врага.",
}

ORDER = list(RU)


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    path = root / "src/data/abilities.h"
    if not path.is_file():
        die(f"missing {path}")
    text = path.read_text(encoding="utf-8")

    if len(RU) != 165 or ORDER[0] != "NONE" or ORDER[-1] != "TERAVOLT":
        die(f"translation table boundary/count drift: count={len(RU)}")

    changed = 0
    already = 0
    for idx, ability in enumerate(ORDER):
        start_token = f"[ABILITY_{ability}] ="
        start = text.find(start_token)
        if start < 0:
            die(f"missing ability block {ability}")

        if idx + 1 < len(ORDER):
            next_token = f"[ABILITY_{ORDER[idx + 1]}] ="
            end = text.find(next_token, start + len(start_token))
        else:
            # Bound TERAVOLT at the first Gen VI ability. Do not translate later gens.
            end = text.find("[ABILITY_AROMA_VEIL] =", start + len(start_token))
        if end < 0:
            die(f"could not bound ability block {ability}")

        block = text[start:end]
        name_match = re.search(r'\.name\s*=\s*_\("([^\"]+)"\)', block)
        if not name_match:
            die(f"English name missing in {ability}")
        english_name = name_match.group(1)

        desc = RU[ability]
        wanted = f'.description = COMPOUND_STRING("{desc}"),'
        if wanted in block:
            already += 1
            continue

        # Replace only the description expression (including any #if branches)
        # up to aiRating. This preserves .name and all behavior flags verbatim.
        pat = re.compile(r'(\n\s*\.description\s*=\s*)(.*?)(\n\s*\.aiRating\s*=)', re.S)
        matches = list(pat.finditer(block))
        if len(matches) != 1:
            die(f"{ability}: expected one description before aiRating, got {len(matches)}")
        block2 = pat.sub(lambda m: f'\n        {wanted}{m.group(3)}', block, count=1)

        # Explicitly prove the English Ability name survived this edit.
        if f'.name = _("{english_name}")' not in block2:
            die(f"{ability}: name changed unexpectedly")
        text = text[:start] + block2 + text[end:]
        changed += 1

    # Negative boundary audit: all Gen I-V descriptions must now be Russian,
    # while Gen VI starts immediately after untouched TERAVOLT.
    for idx, ability in enumerate(ORDER):
        start = text.find(f"[ABILITY_{ability}] =")
        end_token = f"[ABILITY_{ORDER[idx + 1]}] =" if idx + 1 < len(ORDER) else "[ABILITY_AROMA_VEIL] ="
        end = text.find(end_token, start + 1)
        block = text[start:end]
        if RU[ability] not in block:
            die(f"{ability}: Russian description missing after patch")
        if not re.search(r'\.name\s*=\s*_\("[^\"]+"\)', block):
            die(f"{ability}: English name field missing after patch")

    path.write_text(text, encoding="utf-8")
    report = {
        "marker": MARKER,
        "category": "Ability descriptions",
        "generations": "I-V",
        "abilitiesLocalized": len(RU),
        "blocksChanged": changed,
        "blocksAlreadyLocalized": already,
        "abilityNamesEnglish": True,
        "moveNamesTouched": False,
        "speciesNamesTouched": False,
        "battleLogicTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_system_v3_25_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: {len(RU)} Gen I-V Ability descriptions localized; "
        "Ability names remain English; battle logic and Ash protections unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
