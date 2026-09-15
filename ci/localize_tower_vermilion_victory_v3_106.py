#!/usr/bin/env python3
"""Qarro v3.106: localize Trainer Tower lobby, Vermilion City and Victory Road 3F runtime text.

Translates exactly 60 English-only FireRed runtime blocks from the v3.105 surface audit:
  * TrainerTower_Lobby_Frlg: 20
  * VermilionCity_Frlg: 20
  * VictoryRoad_3F_Frlg: 20

Pokemon species, Move and Ability proper names remain English by project canon.
The writer rejects physical newlines in translation values and doubled FireRed
runtime escapes. Gameplay/trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TOWER_VERMILION_VICTORY_V3_106"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/TrainerTower_Lobby_Frlg/scripts.inc": {
        "TrainerTower_Lobby_Text_WelcomeToTrainerTower": "Здравствуйте!\\pДобро пожаловать в БАШНЮ ТРЕНЕРОВ,\\nкуда съезжаются ТРЕНЕРЫ отовсюду!$",
        "TrainerTower_Lobby_Text_TrainersUpToFloorNum": "ТРЕНЕРЫ со всего мира\\nсобираются здесь для боёв.\\pПосмотрим...\\pСейчас ТРЕНЕРЫ ждут тебя\\nдо этажа {STR_VAR_1}.$",
        "TrainerTower_Lobby_Text_TrainersUpEighthFloor": "ТРЕНЕРЫ ждут твоего вызова\\nвплоть до восьмого этажа.$",
        "TrainerTower_Lobby_Text_LikeToChallengeTrainers": "Хочешь бросить вызов\\nожидающим ТРЕНЕРАМ?$",
        "TrainerTower_Lobby_Text_StartClockGetSetGo": "Хорошо, запускаю таймер.\\nПокажи всё, на что способен!\\pНа старт...\\pВнимание...\\pМарш!$",
        "TrainerTower_Lobby_Text_PleaseVisitUsAgain": "Приходи к нам ещё!$",
        "TrainerTower_Lobby_Text_TooBadComeBackTryAgain": "Очень жаль.\\pТы приложил огромные усилия\\nв этих боях.\\pВозвращайся и попробуй снова!$",
        "TrainerTower_Lobby_Text_GiveItYourBest": "Желаю показать всё, на что ты способен.$",
        "TrainerTower_Lobby_Text_MoveCounterHereWhenTrainersSwitch": "Когда ТРЕНЕРЫ меняются местами,\\nздесь становится очень шумно.\\pЧтобы не попасть в толпу, мы перенесли\\nстойку регистрации сюда.\\pИзвини за неудобства.$",
        "TrainerTower_Roof_Text_ImOwnerBattledPerfectly": "Здравствуйте...\\pЯ владелец этой БАШНИ...\\pКак высоко над крышей небо...\\pКак приятно здесь дует ветер...\\pВсё просто идеально...\\pИ твои бои...\\nОни тоже были безупречны...$",
        "TrainerTower_Roof_Text_ThisIsForYou": "Это тебе...$",
        "TrainerTower_Roof_Text_DoneItInRecordTime": "О!\\nПотрясающе!\\pНевероятно, как быстро\\nты сюда поднялся.\\pТы установил рекордное время...\\pЯ внесу твой результат\\nна доску у стойки регистрации.$",
        "TrainerTower_Roof_Text_TookSweetTimeGettingHere": "Похоже, ты совсем не спешил\\nподниматься сюда...$",
        "TrainerTower_Roof_Text_IdLikeToSeeBetterTime": "Я хотел бы увидеть\\nот тебя время получше...\\pЯ на тебя рассчитываю.\\pДо встречи...$",
        "TrainerTower_Text_XMinYZSec": "{STR_VAR_1} мин. {STR_VAR_2}.{STR_VAR_3} сек.$",
        "TrainerTower_Lobby_Text_NeedTwoMonsForDouble": "Это бой два на два.\\pТы не можешь участвовать,\\nесли у тебя меньше двух ПОКЕМОНОВ.$",
        "TrainerTower_Lobby_Text_ExplainTrainerTower": "В БАШНЕ ТРЕНЕРОВ проходит\\nиспытание на время - TIME ATTACK.\\pЗасекается, как быстро ты доберёшься\\nот стойки регистрации до ВЛАДЕЛЬЦА\\lна крыше.\\pЛучшие результаты записываются\\nна ДОСКУ ВРЕМЕНИ.\\pСоревнуйся с друзьями и узнай,\\nкто пройдёт башню быстрее.\\pЗа победы над ТРЕНЕРАМИ здесь\\nне дают EXP. и денег.$",
        "TrainerTower_Lobby_Text_ThanksForCompeting": "Спасибо за участие!$",
        "TrainerTower_Lobby_Text_WonderWhatKindsOfTrainers": "Я пришла проверить, насколько я сильна.\\pИнтересно, какие ТРЕНЕРЫ\\nменя здесь ждут?\\pДаже нервничаю!$",
        "TrainerTower_Lobby_Text_StairsTougherThanAnyBattle": "Фух, фух...\\nФух...\\pДа какие там бои! Эти лестницы...\\nОни тяжелее любой битвы...$",
    },
    "data/maps/VermilionCity_Frlg/scripts.inc": {
        "VermilionCity_Text_DidYouSeeSSAnneInHarbor": "Ты видел S.S. ANNE,\\nпришвартованный в гавани?$",
        "VermilionCity_Text_SSAnneHasDepartedForYear": "Значит, S.S. ANNE уже отплыл?\\pОн вернётся в ВЕРМИЛИОН\\nпримерно в это же время через год.$",
        "VermilionCity_Text_BuildingOnThisLand": "Я строю здание на этом участке.\\nВся земля здесь моя.\\pМой POKeMON утрамбовывает грунт\\nпод фундамент.$",
        "VermilionCity_Text_Machop": "MACHOP: Гуо! Гогого!$",
        "VermilionCity_Text_MachopStompingLandFlat": "MACHOP утрамбовывает землю.$",
        "VermilionCity_Text_SSAnneVisitsOnceAYear": "S.S. ANNE - знаменитый роскошный\\nкруизный лайнер.\\pОн заходит в ВЕРМИЛИОН\\nраз в год.$",
        "VermilionCity_Text_CitySign": "ВЕРМИЛИОН-СИТИ\\nПорт великолепных закатов$",
        "VermilionCity_Text_SnorlaxBlockingRoute12": "ВНИМАНИЕ!\\pМАРШРУТ 12 может быть перекрыт\\nспящим ПОКЕМОНОМ.\\pОбъезд - через КАМЕННЫЙ ТУННЕЛЬ\\nк ЛАВАНДЕР-ТАУНУ.\\pПОЛИЦИЯ ВЕРМИЛИОНА$",
        "VermilionCity_Text_PokemonFanClubSign": "КЛУБ ПОКЕМОНОВ\\nДобро пожаловать всем фанатам!$",
        "VermilionCity_Text_GymSign": "ЗАЛ ПОКЕМОНОВ ВЕРМИЛИОНА\\nЛИДЕР: LT. SURGE\\lМолниеносный американец!$",
        "VermilionCity_Text_VermilionHarbor": "ГАВАНЬ ВЕРМИЛИОНА$",
        "VermilionCity_Text_TheShipSetSail": "Корабль уже отплыл.$",
        "VermilionCity_Text_BoardSeagallopTriPass": "А, у тебя TRI-PASS.\\pХочешь сесть на паром\\nSEAGALLOP?$",
        "VermilionCity_Text_Seagallop7Departing": "Хорошо, всё в порядке.\\pSEAGALLOP HI-SPEED 7\\nотправляется немедленно.$",
        "VermilionCity_Text_BoardSeagallopRainbowPass": "А, у тебя RAINBOW PASS.\\pХочешь сесть на паром\\nSEAGALLOP?$",
        "VermilionCity_Text_OhMysticTicketTakeYouToNavelRock": "О! Это MYSTICTICKET!\\nВот это редкость.\\pМы с радостью отвезём тебя\\nна NAVEL ROCK в любое время.$",
        "VermilionCity_Text_OhAuroraTicketTakeYouToBirthIsland": "О! Это AURORATICKET!\\nВот это редкость.\\pМы с радостью отвезём тебя\\nна BIRTH ISLAND в любое время.$",
        "VermilionCity_Text_BoardSeagallopFerry": "Хочешь сесть на паром\\nSEAGALLOP?$",
        "VermilionCity_Text_Seagallop10Departing": "Хорошо, всё готово к посадке\\nна специальный паром.\\pSEAGALLOP HI-SPEED 10\\nотправляется немедленно.$",
        "VermilionCity_Text_Seagallop12Departing": "Хорошо, всё готово к посадке\\nна специальный паром.\\pSEAGALLOP HI-SPEED 12\\nотправляется немедленно.$",
    },
    "data/maps/VictoryRoad_3F_Frlg/scripts.inc": {
        "VictoryRoad_3F_Text_GeorgeIntro": "Я слышал слухи о юном гении.$",
        "VictoryRoad_3F_Text_GeorgeDefeat": "Слухи оказались правдой!$",
        "VictoryRoad_3F_Text_GeorgePostBattle": "Так это ты победил GIOVANNI\\nиз КОМАНДЫ R?$",
        "VictoryRoad_3F_Text_AlexaIntro": "ТРЕНЕРЫ живут ради встречи\\nс более сильными соперниками.$",
        "VictoryRoad_3F_Text_AlexaDefeat": "Ох!\\nКакая сила!$",
        "VictoryRoad_3F_Text_AlexaPostBattle": "В тяжёлых боях ты становишься\\nсильнее.$",
        "VictoryRoad_3F_Text_CarolineIntro": "Сейчас покажу, чего ты стоишь.\\nДа ничего!$",
        "VictoryRoad_3F_Text_CarolineDefeat": "Я в ярости!$",
        "VictoryRoad_3F_Text_CarolinePostBattle": "Ты показал мне,\\nчего я на самом деле стою...$",
        "VictoryRoad_3F_Text_ColbyIntro": "Только избранные могут пройти здесь!$",
        "VictoryRoad_3F_Text_ColbyDefeat": "Не могу поверить!$",
        "VictoryRoad_3F_Text_ColbyPostBattle": "Все ТРЕНЕРЫ здесь направляются\\nв ЛИГУ ПОКЕМОНОВ.\\pНе теряй бдительность.$",
        "VictoryRoad_3F_Text_RayIntro": "RAY: Вместе мы двое\\nпредназначены для величия!$",
        "VictoryRoad_3F_Text_RayDefeat": "RAY: Нелепость!\\nНе может быть!$",
        "VictoryRoad_3F_Text_RayPostBattle": "RAY: Ты победил нас.\\nВеличие снова ускользнуло...$",
        "VictoryRoad_3F_Text_RayNotEnoughMons": "RAY: Мы вдвоём стремимся\\nк самой вершине.\\pЧтобы сразиться с нами,\\nвозьми хотя бы двух ПОКЕМОНОВ.$",
        "VictoryRoad_3F_Text_TyraIntro": "TYRA: Мы вместе пытаемся\\nстать чемпионами.$",
        "VictoryRoad_3F_Text_TyraDefeat": "TYRA: Ох, но...$",
        "VictoryRoad_3F_Text_TyraPostBattle": "TYRA: Ты показал мне, что сила\\nможет принимать бесконечные формы.$",
        "VictoryRoad_3F_Text_TyraNotEnoughMons": "TYRA: Ты не сможешь сразиться с нами,\\nесли у тебя только один ПОКЕМОН.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/TrainerTower_Lobby_Frlg/scripts.inc": 20,
    "data/maps/VermilionCity_Frlg/scripts.inc": 20,
    "data/maps/VictoryRoad_3F_Frlg/scripts.inc": 20,
}
EXPECTED_TOTAL = 60


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def asm_quote(text: str) -> str:
    return text.replace('"', '\\"')


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def validate_translation(label: str, translated: str) -> None:
    if not translated.endswith("$"):
        die(f"{label}: translated text must end with $")
    if "\n" in translated or "\r" in translated:
        die(f"{label}: physical newline/carriage return in translation value")
    if any(ch in translated for ch in ("—", "–", "“", "”", "’", "…", "«", "»")):
        die(f"{label}: unsupported Unicode punctuation")
    if "\\\\" in translated:
        die(f"{label}: doubled runtime backslash in translation value")
    if not re.search(r"[А-Яа-яЁё]", translated):
        die(f"{label}: expected Cyrillic translation")


def replace_block(text: str, label: str, translated: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: target already contains Cyrillic; refusing overwrite")
    if ".string " not in old:
        die(f"{label}: target does not look like a text block")
    block = f'{label}::\n\t.string "{asm_quote(translated)}"\n\n'
    return text[:start] + block + text[end:]


def validate_written_file(rel: Path, text: str) -> None:
    for lineno, line in enumerate(text.splitlines(), start=1):
        if ".string \"" in line and line.count('"') < 2:
            die(f"{rel}:{lineno}: physical newline inside assembler string")
    if re.search(r"\\\\[npl]", text):
        die(f"{rel}: doubled FireRed runtime escape found")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    total = sum(len(v) for v in FILES.values())
    if total != EXPECTED_TOTAL:
        die(f"expected translation table total {EXPECTED_TOTAL}, got {total}")

    translated_by_file: dict[str, int] = {}
    for rel_str, patches in FILES.items():
        if len(patches) != EXPECTED_COUNTS[rel_str]:
            die(f"{rel_str}: expected {EXPECTED_COUNTS[rel_str]} entries, got {len(patches)}")
        rel = Path(rel_str)
        path = root / rel
        if not path.is_file():
            die(f"missing target file: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in patches.items():
            validate_translation(label, translated)
            text = replace_block(text, label, translated)
        validate_written_file(rel, text)
        path.write_text(text, encoding="utf-8")
        translated_by_file[rel_str] = len(patches)

    audit = root / "build" / "qarro_ru_tower_vermilion_victory_v3_106_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(
        json.dumps(
            {
                "marker": MARKER,
                "translatedBlockCount": EXPECTED_TOTAL,
                "translatedByFile": translated_by_file,
                "physicalNewlinesInsideAsmStrings": False,
                "doubledRuntimeEscapes": False,
                "gameplayLogicTouched": False,
                "trainerDataTouched": False,
                "ashBondTouched": False,
                "ashCapTouched": False,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"[{MARKER}] PASS: translated {EXPECTED_TOTAL} runtime blocks across 3 files; "
        "Ash Bond/Ash Cap untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
