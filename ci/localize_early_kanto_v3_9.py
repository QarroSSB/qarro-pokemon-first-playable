#!/usr/bin/env python3
"""Qarro v3.19: complete Viridian City zone localization with Viridian Gym.

Runs CI-green v3.18 first, then localizes all 35 user-facing FireRed text
blocks in ViridianCity_Gym_Frlg/scripts.inc. Pokemon species, Move and Ability
proper names stay English. Gameplay, trainer data, Ash Bond and Ash Cap are not
modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "f235e5556e1b5a97b665e356c958e688db1c745c"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_18"
BASE_COUNT = 265
MARKER = "QARRO_RU_EARLY_KANTO_V3_19"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
REL = Path("data/maps/ViridianCity_Gym_Frlg/scripts.inc")
SOURCE_BLOB = "7cbe9a6800a46495d789b1b858696dfc61301177"

def B(*lines: str) -> tuple[str, ...]: return lines

BLOCKS = {
"ViridianCity_Gym_Text_GiovanniIntro": B(
    r"Ха-ха-ха!\n", r"Добро пожаловать в мое убежище!\p",
    r"Оно останется им, пока я не верну\n", r"КОМАНДЕ R былую славу.\p",
    r"Но ты снова меня нашел.\n", r"Что ж.\l", r"На этот раз я не сдерживаюсь!\p",
    r"Ты снова встретишься с\n", r"GIOVANNI, величайшим ТРЕНЕРОМ!{PLAY_BGM}{MUS_RG_ENCOUNTER_ROCKET}$"),
"ViridianCity_Gym_Text_GiovanniDefeat": B(
    r"Ха!\n", r"Это был по-настоящему жаркий бой.\l", r"Ты победил!\p",
    r"В доказательство - ЗНАЧОК ЗЕМЛИ!\n",
    r"{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}$"),
"ViridianCity_Gym_Text_GiovanniPostBattle": B(
    r"После такого поражения я не могу\n", r"смотреть своим людям в глаза.\l", r"Я предал их доверие.\p",
    r"С этого дня КОМАНДА R\n", r"распущена навсегда!\p", r"А я снова посвящу свою жизнь\n",
    r"тренировкам.\p", r"Когда-нибудь мы еще встретимся!\n", r"Прощай!$"),
"ViridianCity_Gym_Text_ExplainEarthBadgeTakeThis": B(
    r"ЗНАЧОК ЗЕМЛИ заставит ПОКЕМОНОВ\n", r"любого уровня слушаться тебя.\p",
    r"Он доказывает твое мастерство\n", r"ТРЕНЕРА ПОКЕМОНОВ.\p", r"Теперь ты можешь бросить вызов\n",
    r"ЛИГЕ ПОКЕМОНОВ.\p", r"И еще возьми эту TM.\p", r"Считай ее подарком перед твоим\n",
    r"испытанием в ЛИГЕ ПОКЕМОНОВ.$"),
"ViridianCity_Gym_Text_ReceivedTM26FromGiovanni": B(r"{PLAYER} получает TM26\n", r"от GIOVANNI.$"),
"ViridianCity_Gym_Text_ExplainTM26": B(
    r"TM26 содержит EARTHQUAKE.\p", r"Это мощная атака, вызывающая\n", r"сильнейшее землетрясение.\p",
    r"Я создал ее, когда руководил\n", r"этим ГИМОМ много лет назад...$"),
"ViridianCity_Gym_Text_YouDoNotHaveSpace": B(r"В СУМКЕ нет места для этого!$"),
"ViridianCity_Gym_Text_YujiIntro": B(r"Хех!\n", r"Наверняка ты уже выдохся!$"),
"ViridianCity_Gym_Text_YujiDefeat": B(r"У меня кончились силы!$"),
"ViridianCity_Gym_Text_YujiPostBattle": B(r"Тебе понадобится сила, чтобы\n", r"сравниться с нашим ЛИДЕРОМ ГИМА.$"),
"ViridianCity_Gym_Text_AtsushiIntro": B(r"Р-р-р-р!\n", r"Я довожу себя до ярости!$"),
"ViridianCity_Gym_Text_AtsushiDefeat": B(r"Уа-а-а!$"),
"ViridianCity_Gym_Text_AtsushiPostBattle": B(r"Я все еще недостаточно хорош!$"),
"ViridianCity_Gym_Text_JasonIntro": B(r"Мы с ПОКЕМОНОМ создаем\n", r"прекрасную музыку вместе!$"),
"ViridianCity_Gym_Text_JasonDefeat": B(r"У тебя идеальная гармония!$"),
"ViridianCity_Gym_Text_JasonPostBattle": B(r"Ты знаешь, кто наш\n", r"ЛИДЕР ГИМА?$"),
"ViridianCity_Gym_Text_KiyoIntro": B(r"Каратэ - высшая форма\n", r"боевых искусств!$"),
"ViridianCity_Gym_Text_KiyoDefeat": B(r"Ай-я!$"),
"ViridianCity_Gym_Text_KiyoPostBattle": B(r"Если бы мои ПОКЕМОНЫ владели\n", r"каратэ так же хорошо, как я...$"),
"ViridianCity_Gym_Text_WarrenIntro": B(r"Настоящий талант побеждает стильно.$"),
"ViridianCity_Gym_Text_WarrenDefeat": B(r"Я потерял хватку!$"),
"ViridianCity_Gym_Text_WarrenPostBattle": B(r"ЛИДЕР будет ругать меня за\n", r"такое поражение...$"),
"ViridianCity_Gym_Text_TakashiIntro": B(r"Я КОРОЛЬ КАРАТЭ!\n", r"Твоя судьба в моих руках!$"),
"ViridianCity_Gym_Text_TakashiDefeat": B(r"Ай-я!$"),
"ViridianCity_Gym_Text_TakashiPostBattle": B(r"ЛИГА ПОКЕМОНОВ?\n", r"Ты? Не зазнавайся!$"),
"ViridianCity_Gym_Text_ColeIntro": B(r"Мои удары кнута заставят\n", r"твоих ПОКЕМОНОВ дрожать!$"),
"ViridianCity_Gym_Text_ColeDefeat": B(r"Ай!\n", r"Вот это удар!$"),
"ViridianCity_Gym_Text_ColePostBattle": B(r"Постой!\n", r"Я просто был неосторожен!$"),
"ViridianCity_Gym_Text_SamuelIntro": B(r"ВИРИДИАН-ГИМ долго был закрыт.\p", r"Но теперь наш ЛИДЕР вернулся!$"),
"ViridianCity_Gym_Text_SamuelDefeat": B(r"Меня победили?$"),
"ViridianCity_Gym_Text_SamuelPostBattle": B(r"Попасть в ЛИГУ ПОКЕМОНОВ можно,\n", r"только победив нашего\l", r"ЛИДЕРА ГИМА!$"),
"ViridianCity_Gym_Text_GymGuyAdvice": B(
    r"Йо!\n", r"Будущий чемпион!\p", r"Даже я не знаю, кто является\n", r"ЛИДЕРОМ ВИРИДИАН-ГИМА.\p",
    r"Но одно ясно наверняка:\n", r"это будет самый трудный\l", r"из всех ЛИДЕРОВ ГИМОВ.\p",
    r"Я также слышал, что ТРЕНЕРЫ\n", r"здесь любят ПОКЕМОНОВ земляного типа.$"),
"ViridianCity_Gym_Text_GymGuyPostVictory": B(r"Вот это да! GIOVANNI был\n", r"ЛИДЕРОМ ВИРИДИАН-ГИМА?$"),
"ViridianCity_Gym_Text_GymStatue": B(r"ПОКЕМОН-ГИМ ВИРИДИАН-СИТИ\n", r"ЛИДЕР: ?\p", r"ПОБЕДИВШИЕ ТРЕНЕРЫ:\n", r"{RIVAL}$"),
"ViridianCity_Gym_Text_GymStatuePlayerWon": B(r"ПОКЕМОН-ГИМ ВИРИДИАН-СИТИ\n", r"ЛИДЕР: GIOVANNI\p", r"ПОБЕДИВШИЕ ТРЕНЕРЫ:\n", r"{RIVAL}, {PLAYER}$"),
}

def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT], check=True)
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"], text=True)

def render(label: str, lines: tuple[str, ...]) -> str:
    return label + "::\n" + "".join(f'\t.string "{line}"\n' for line in lines)

def patch_label(text: str, label: str, lines: tuple[str, ...]) -> str:
    pat = re.compile(rf"(?m)^{re.escape(label)}::\n(?:\t\.string .*\n)+")
    hits = list(pat.finditer(text))
    if len(hits) != 1:
        raise RuntimeError(f"{label}: expected exactly one string block, got {len(hits)}")
    old = hits[0].group(0)
    if any("\u0400" <= ch <= "\u04ff" for ch in old):
        raise RuntimeError(f"{label}: source block unexpectedly already contains Cyrillic")
    return text[:hits[0].start()] + render(label, lines) + text[hits[0].end():]

def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <pokeemerald-expansion-root>", file=sys.stderr)
        return 2
    code = load_base()
    ns = {"__name__": "qarro_ru_early_kanto_v318_base", "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc:
        return rc

    root = Path(sys.argv[1]).resolve()
    audit_path = root / AUDIT_REL
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != BASE_MARKER or int(audit.get("selectedBlocksLocalized", -1)) != BASE_COUNT:
        raise RuntimeError(f"base localization audit drift: {audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}")

    path = root / REL
    actual = subprocess.check_output(["git", "-C", str(root), "hash-object", str(path)], text=True).strip()
    if actual != SOURCE_BLOB:
        raise RuntimeError(f"{REL}: pinned source blob drift: {actual} != {SOURCE_BLOB}")
    text = path.read_text(encoding="utf-8")
    for label, lines in BLOCKS.items():
        text = patch_label(text, label, lines)
    path.write_text(text, encoding="utf-8")

    changed = len(BLOCKS)
    if changed != 35:
        raise RuntimeError(f"Viridian Gym scope drift: expected 35 blocks, got {changed}")
    audit.setdefault("files", {})[str(REL)] = {"selectedBlocks": changed, "changedThisRun": changed, "sourceBlob": SOURCE_BLOB}
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + changed,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun", 0)) + changed,
        "viridianGymLocalized": True,
        "viridianCityZoneComplete": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {changed} Viridian Gym blocks = {BASE_COUNT + changed}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
