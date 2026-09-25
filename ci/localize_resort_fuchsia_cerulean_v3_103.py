#!/usr/bin/env python3
"""Qarro v3.103: localize remaining Resort Gorgeous, Fuchsia Gym and Cerulean City runtime text.

Translates exactly the English-only runtime blocks still reported by the v3.102
RU surface audit in:
  * FiveIsland_ResortGorgeous_Frlg: 23 blocks
  * FuchsiaCity_Gym_Frlg: 22 blocks (Koga story blocks stay untouched)
  * CeruleanCity_Frlg: 21 blocks (Rival/Rocket story blocks stay untouched)

Pokemon species, Move and Ability proper names remain English by project canon.
Gameplay logic, trainer data, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_RESORT_FUCHSIA_CERULEAN_V3_103"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES: dict[Path, dict[str, str]] = {
    Path("data/maps/FiveIsland_ResortGorgeous_Frlg/scripts.inc"): {
        "FiveIsland_ResortGorgeous_Text_DaisyIntro": "Этими руками я создам\nсвою победу!$",
        "FiveIsland_ResortGorgeous_Text_DaisyDefeat": "Какой позор...\nЯ вся покраснела...$",
        "FiveIsland_ResortGorgeous_Text_DaisyPostBattle": "Ой! Краски разбросаны\nповсюду!$",
        "FiveIsland_ResortGorgeous_Text_CelinaIntro": "Простите!\nЯ пытаюсь рисовать.\lПожалуйста, не мешайте мне!$",
        "FiveIsland_ResortGorgeous_Text_CelinaDefeat": "Это поражение...\nЯ словно побледнела...$",
        "FiveIsland_ResortGorgeous_Text_CelinaPostBattle": "ДЖИЛЛИАН?\nЧуть наклоните голову...\lДа! Вот так и стойте!$",
        "FiveIsland_ResortGorgeous_Text_RaynaIntro": "Хм...\nРакурс всё ещё не тот...$",
        "FiveIsland_ResortGorgeous_Text_RaynaDefeat": "Ох...\nНа душе совсем сине...$",
        "FiveIsland_ResortGorgeous_Text_RaynaPostBattle": "Небо и море...\nОни так переменчивы.\pИх настроение меняется,\nи его трудно поймать.$",
        "FiveIsland_ResortGorgeous_Text_JackiIntro": "Я гостю в доме друга,\nесли вам интересно.$",
        "FiveIsland_ResortGorgeous_Text_JackiDefeat": "Ох, какая сила.$",
        "FiveIsland_ResortGorgeous_Text_JackiPostBattle": "Как приятно спокойно\nсражаться под морским бризом.$",
        "FiveIsland_ResortGorgeous_Text_GillianIntro": "Я думаю устроить бассейн\nспециально для ПОКЕМОНОВ.$",
        "FiveIsland_ResortGorgeous_Text_GillianDefeat": "Боже мой!$",
        "FiveIsland_ResortGorgeous_Text_GillianPostBattle": "Бассейн хорош, но, пожалуй,\nсолнечная веранда лучше.$",
        "FiveIsland_ResortGorgeous_Text_DestinIntro": "Я отлично бегаю.\nЯ очень быстрый!$",
        "FiveIsland_ResortGorgeous_Text_DestinDefeat": "Упс!\nЯ слишком спешил!$",
        "FiveIsland_ResortGorgeous_Text_DestinPostBattle": "Когда бегу по ветру,\nкажется, будто я лечу!$",
        "FiveIsland_ResortGorgeous_Text_TobyIntro": "Морская жизнь на этом\nкурорте мне по душе.$",
        "FiveIsland_ResortGorgeous_Text_TobyDefeat": "Вот это сюрприз!\nВы шутите.$",
        "FiveIsland_ResortGorgeous_Text_TobyPostBattle": "Так серьёзно к этому\nотноситься... Нелепо.$",
        "FiveIsland_ResortGorgeous_Text_SelphyThanksYouMayGoNow": "СЕЛФИ: Спасибо.\pТеперь можете идти.$",
        "FiveIsland_ResortGorgeous_Text_SelphysHouse": "ДОМ СЕЛФИ$",
    },
    Path("data/maps/FuchsiaCity_Gym_Frlg/scripts.inc"): {
        "FuchsiaCity_Gym_Text_KaydenIntro": "Для ПОКЕМОНОВ сила - не всё.\nПонимаешь?\pГлавное - стратегия!\pЯ покажу, как тактика\nпобеждает грубую силу.$",
        "FuchsiaCity_Gym_Text_KaydenDefeat": "Что?\nНевероятно!$",
        "FuchsiaCity_Gym_Text_KaydenPostBattle": "Ты соединяешь силу и ум?\nХорошая стратегия!\pДля юного ТРЕНЕРА\nэто впечатляет.$",
        "FuchsiaCity_Gym_Text_KirkIntro": "Когда-то я был фокусником.\pНо мечтал стать ниндзя,\nпоэтому пришёл в этот ГИМ.$",
        "FuchsiaCity_Gym_Text_KirkDefeat": "Мне конец!$",
        "FuchsiaCity_Gym_Text_KirkPostBattle": "Даже проиграв, я продолжу\nучиться у КОГИ,\lмоего мастера-ниндзя.$",
        "FuchsiaCity_Gym_Text_NateIntro": "Попробуй одолеть мои\nособые приёмы!$",
        "FuchsiaCity_Gym_Text_NateDefeat": "Ты меня провёл!$",
        "FuchsiaCity_Gym_Text_NatePostBattle": "Я люблю яд и сон:\nих эффект остаётся после боя!$",
        "FuchsiaCity_Gym_Text_PhilIntro": "Стой!\pЗнаменитые невидимые стены\nГИМА ФУКСИИ уже раздражают?$",
        "FuchsiaCity_Gym_Text_PhilDefeat": "Ого!\nТы разобрался!$",
        "FuchsiaCity_Gym_Text_PhilPostBattle": "Ты меня впечатлил!\nВот подсказка.\pИщи просветы между\nневидимыми стенами!$",
        "FuchsiaCity_Gym_Text_EdgarIntro": "Я тоже изучаю путь ниндзя\nу мастера КОГИ!\pНиндзя издавна используют\nживотных!$",
        "FuchsiaCity_Gym_Text_EdgarDefeat": "Аууу!$",
        "FuchsiaCity_Gym_Text_EdgarPostBattle": "Мне ещё многому учиться.$",
        "FuchsiaCity_Gym_Text_ShawnIntro": "Мастер КОГА из древнего\nрода ниндзя.\pА кто были твои предки?$",
        "FuchsiaCity_Gym_Text_ShawnDefeat": "Ты искуснее, чем я думал!$",
        "FuchsiaCity_Gym_Text_ShawnPostBattle": "Где есть свет, есть и тень!\pСвет или тень -\nчто выберешь?$",
        "FuchsiaCity_Gym_Text_GymGuyAdvice": "Йо!\nБудущий чемпион!\pГИМ ФУКСИИ полон хитростей.\nЗдесь невидимые стены!\pКОГА кажется совсем рядом,\nно путь к нему закрыт.\pИщи проходы в стенах,\nчтобы добраться до него.$",
        "FuchsiaCity_Gym_Text_GymGuyPostVictory": "Удивительно, как ниндзя\nдо сих пор внушают страх!$",
        "FuchsiaCity_Gym_Text_GymStatue": "ГИМ ПОКЕМОНОВ ФУКСИИ\nЛИДЕР: КОГА\pПОБЕДИВШИЕ ТРЕНЕРЫ:\n{RIVAL}$",
        "FuchsiaCity_Gym_Text_GymStatuePlayerWon": "ГИМ ПОКЕМОНОВ ФУКСИИ\nЛИДЕР: КОГА\pПОБЕДИВШИЕ ТРЕНЕРЫ:\n{RIVAL}, {PLAYER}$",
    },
    Path("data/maps/CeruleanCity_Frlg/scripts.inc"): {
        "CeruleanCity_Text_TrainerLifeIsToughIsntIt": "Ты тоже ТРЕНЕР?\pЛовить, сражаться...\nНелёгкая жизнь, правда?$",
        "CeruleanCity_Text_YouCanCutDownSmallTrees": "Знаешь, маленькие деревья\nможно срубить приёмом CUT?\pДаже дерево у магазина\nможно срубить.\pХотя, кажется, его можно\nи обойти.$",
        "CeruleanCity_Text_IfSlowbroWasntThereCouldCutTree": "Если бы SLOWBRO не мешал,\nты мог бы срубить дерево.\pТак можно попасть\nна другую сторону.\pХотя, кажется, его можно\nи обойти.$",
        "CeruleanCity_Text_PokemonEncyclopediaAmusing": "Ты составляешь энциклопедию\nо ПОКЕМОНАХ? Забавно.$",
        "CeruleanCity_Text_PeopleHereWereRobbed": "Людей здесь ограбили.\pЯсно, что за этим стоит\nКОМАНДА R!\pДаже ПОЛИЦИИ трудно\nсправиться с ними!$",
        "CeruleanCity_Text_SlowbroUseSonicboom": "Так! SLOWBRO!\nИспользуй SONICBOOM!$",
        "CeruleanCity_Text_SlowbroPayAttention": "SLOWBRO, соберись!$",
        "CeruleanCity_Text_SlowbroPunch": "SLOWBRO, ударь!$",
        "CeruleanCity_Text_NoYouBlewItAgain": "Нет!\nОпять не получилось!$",
        "CeruleanCity_Text_SlowbroWithdraw": "SLOWBRO, используй WITHDRAW!$",
        "CeruleanCity_Text_HardToControlMonsObedience": "Нет! Не так!\nПОКЕМОНАМИ трудно управлять!\pИх послушание зависит\nот навыка ТРЕНЕРА.$",
        "CeruleanCity_Text_SlowbroTookSnooze": "SLOWBRO задремал...$",
        "CeruleanCity_Text_SlowbroLoafingAround": "SLOWBRO бездельничает...$",
        "CeruleanCity_Text_SlowbroTurnedAway": "SLOWBRO отвернулся...$",
        "CeruleanCity_Text_SlowbroIgnoredOrders": "SLOWBRO не слушается...$",
        "CeruleanCity_Text_WantBrightRedBicycle": "Я хочу ярко-красный велосипед.\pБуду держать его дома,\nчтобы не испачкался.$",
        "CeruleanCity_Text_ThisIsCeruleanCave": "Это ПЕЩЕРА СЕРУЛИНА.\pВнутри живут невероятно\nсильные ПОКЕМОНЫ.\pТуда пускают только\nособых ТРЕНЕРОВ.\pДля начала нужно стать\nЧЕМПИОНОМ ЛИГИ ПОКЕМОНОВ.\pИ ещё совершить\nвеликое достижение.$",
        "CeruleanCity_Text_CitySign": "СЕРУЛИН-СИТИ\nГород в загадочной\lголубой ауре$",
        "CeruleanCity_Text_TrainerTipsHeldItems": "СОВЕТЫ ТРЕНЕРУ\pПОКЕМОН может держать предмет.\pНекоторые предметы он может\nиспользовать прямо в бою.$",
        "CeruleanCity_Text_BikeShopSign": "Трава и пещеры - без проблем!\nМАГАЗИН ВЕЛОСИПЕДОВ$",
        "CeruleanCity_Text_GymSign": "ГИМ ПОКЕМОНОВ СЕРУЛИНА\nЛИДЕР: МИСТИ\lРусалка-сорванец!$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/FiveIsland_ResortGorgeous_Frlg/scripts.inc": 23,
    "data/maps/FuchsiaCity_Gym_Frlg/scripts.inc": 22,
    "data/maps/CeruleanCity_Frlg/scripts.inc": 21,
}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def asm_quote(text: str) -> str:
    return text.replace('"', '\\"')


def replace_block(text: str, label: str, translated: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: target already contains Cyrillic; refusing broad overwrite")
    if ".string " not in old:
        die(f"{label}: target does not look like a text block")
    block = f'{label}::\n\t.string "{asm_quote(translated)}"\n\n'
    return text[:start] + block + text[end:]


def validate_translation(label: str, translated: str) -> None:
    if not translated.endswith("$"):
        die(f"{label}: translated text must end with $")
    if any(ch in translated for ch in ("—", "–", "“", "”", "’", "…")):
        die(f"{label}: unsupported Unicode punctuation")
    if "\\\\" in translated:
        die(f"{label}: doubled runtime backslash in translation value")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    total = 0
    by_file: dict[str, int] = {}

    for rel, patches in FILES.items():
        expected = EXPECTED_COUNTS[str(rel)]
        if len(patches) != expected:
            die(f"{rel}: expected {expected} patches in script, got {len(patches)}")
        path = root / rel
        if not path.is_file():
            die(f"missing source file: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in patches.items():
            validate_translation(label, translated)
            text = replace_block(text, label, translated)
        path.write_text(text, encoding="utf-8")
        by_file[str(rel)] = len(patches)
        total += len(patches)

    if total != 66:
        die(f"expected exactly 66 translated blocks, got {total}")

    out = root / "build" / "qarro_ru_resort_fuchsia_cerulean_v3_103_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlockCount": total,
        "translatedByFile": by_file,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon species, Move and Ability proper names remain English",
        "gameplayLogicTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} runtime blocks across {len(FILES)} files; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
