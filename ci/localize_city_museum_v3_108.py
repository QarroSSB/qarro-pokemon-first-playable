#!/usr/bin/env python3
"""Qarro v3.108: localize Celadon City, Fuchsia City and Pewter Museum 1F runtime text.

Translates exactly 53 English-only FireRed runtime blocks from the v3.107 surface audit:
  * CeladonCity_Frlg: 18 blocks
  * FuchsiaCity_Frlg: 18 blocks
  * PewterCity_Museum_1F_Frlg: 17 blocks

Pokemon species, Move and Ability proper names remain English by project canon.
Gameplay/trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_CITY_MUSEUM_V3_108"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/CeladonCity_Frlg/scripts.inc": {
        "CeladonCity_Text_GotMyKoffingInCinnabar": "Я поймала своего KOFFING на СИННАБАРЕ.\\pОбычно он милый, но когда злится,\\nто выпускает ядовитый газ.$",
        "CeladonCity_Text_GymIsGreatFullOfWomen": "Хе-хе! Этот ЗАЛ просто отличный!\\nЗдесь полно женщин!$",
        "CeladonCity_Text_GameCornerIsBadForCitysImage": "СЕЛАДОН гордится тем, как жители\\nзаботятся о красоте города.\\pПоэтому новый ИГРОВОЙ УГОЛОК\\nпортит нашему городу репутацию.$",
        "CeladonCity_Text_BlewItAllAtSlots": "Эх...\\nЯ всё проиграл на автоматах!\\pНадо было вовремя обменять\\nМОНЕТЫ на призы!$",
        "CeladonCity_Text_MyTrustedPalPoliwrath": "Это мой верный друг POLIWRATH.\\pОн эволюционировал из POLIWHIRL,\\nкогда я использовал ВОДНЫЙ КАМЕНЬ.$",
        "CeladonCity_Text_Poliwrath": "POLIWRATH: Риби-рибит!$",
        "CeladonCity_Text_GetLostOrIllPunchYou": "Чего уставился?\\nПроваливай, а то получишь!$",
        "CeladonCity_Text_KeepOutOfTeamRocketsWay": "Не путайся под ногами у КОМАНДЫ R!$",
        "CeladonCity_Text_ExplainXAccuracyDireHit": "СОВЕТЫ ТРЕНЕРУ\\pX ACCURACY повышает точность\\nприёмов.\\pDIRE HIT увеличивает вероятность\\nкритического удара.\\pВсе эти предметы есть\\nв УНИВЕРМАГЕ СЕЛАДОНА!$",
        "CeladonCity_Text_CitySign": "СЕЛАДОН-СИТИ\\nГород радужных мечтаний$",
        "CeladonCity_Text_GymSign": "ЗАЛ ПОКЕМОНОВ СЕЛАДОНА\\nЛИДЕР: ЭРИКА\\lПринцесса, любящая природу!$",
        "CeladonCity_Text_MansionSign": "ОСОБНЯК СЕЛАДОНА$",
        "CeladonCity_Text_DeptStoreSign": "Всё необходимое найдётся\\nв УНИВЕРМАГЕ СЕЛАДОНА!$",
        "CeladonCity_Text_GuardSpecProtectsFromStatus": "СОВЕТЫ ТРЕНЕРУ\\pGUARD SPEC. защищает ПОКЕМОНОВ\\nот снижения характеристик в бою.\\pВсе эти предметы есть\\nв УНИВЕРМАГЕ СЕЛАДОНА!$",
        "CeladonCity_Text_PrizeExchangeSign": "Обмен МОНЕТ на призы!\\nПУНКТ ОБМЕНА ПРИЗОВ$",
        "CeladonCity_Text_GameCornerSign": "ИГРОВОЙ УГОЛОК КОМАНДЫ R\\nПлощадка для взрослых!$",
        "CeladonCity_Text_ScaldedTongueOnTea": "А-а-ай...\\nЯ обжёг язык!\\pМилая старушка из ОСОБНЯКА\\nдала мне ЧАЙ.\\pНо он был кипятком!\\nНадо остудить его перед питьём.$",
        "CeladonCity_Text_SomeoneStoleSilphScope": "Ох, что же делать...\\pКто-то украл наш SILPH SCOPE.\\pЯ точно видел, как вор\\nпобежал в эту сторону.\\pНо потом потерял его из виду!\\nКуда же он делся?$",
    },
    "data/maps/FuchsiaCity_Frlg/scripts.inc": {
        "FuchsiaCity_Text_DidYouTrySafariGame": "Ты уже пробовал САФАРИ-ИГРУ?\\pНекоторых редких ПОКЕМОНОВ\\nможно поймать только там.$",
        "FuchsiaCity_Text_SafariZoneZooInFront": "Перед входом в ЗОНУ САФАРИ\\nнаходится небольшой зоопарк.\\pА дальше начинается САФАРИ-ИГРА,\\nгде можно ловить ПОКЕМОНОВ.$",
        "FuchsiaCity_Text_WheresSara": "ЭРИК: Где же САРА?\\nЯ обещал встретиться с ней здесь.$",
        "FuchsiaCity_Text_ItemBallInThere": "Тот шар с предметом там...\\nТы тоже хотел его забрать?\\pЯ тоже!\\n...А? Это ПОКЕМОН?$",
        "FuchsiaCity_Text_CitySign": "ФУКСИЯ-СИТИ\\nВзгляни! Цвет страсти - розовый!$",
        "FuchsiaCity_Text_SafariZoneSign": "РАЙ ДЛЯ ПОКЕМОНОВ\\nЗОНА САФАРИ$",
        "FuchsiaCity_Text_SafariGameSign": "САФАРИ-ИГРА\\nПОЙМАЙ СВОЕГО ПОКЕМОНА!$",
        "FuchsiaCity_Text_WardensHomeSign": "ЗОНА САФАРИ\\nДОМ СМОТРИТЕЛЯ$",
        "FuchsiaCity_Text_SafariZoneOfficeSign": "РАЙ ДЛЯ ПОКЕМОНОВ!\\nДобро пожаловать в ЗОНУ САФАРИ!\\lОФИС ЗОНЫ САФАРИ$",
        "FuchsiaCity_Text_GymSign": "ЗАЛ ПОКЕМОНОВ ФУКСИИ\\nЛИДЕР: КОГА\\lМастер ядовитых ниндзя$",
        "FuchsiaCity_Text_ChanseySign": "Имя: CHANSEY\\nПоймать её - дело удачи.$",
        "FuchsiaCity_Text_VoltorbSign": "Имя: VOLTORB\\nВылитый ПОКЕБОЛ.$",
        "FuchsiaCity_Text_KangaskhanSign": "Имя: KANGASKHAN\\pЗаботливый ПОКЕМОН, который носит\\nдетёныша в сумке на животе.$",
        "FuchsiaCity_Text_SlowpokeSign": "Имя: SLOWPOKE\\nДружелюбный и очень медлительный.$",
        "FuchsiaCity_Text_LaprasSign": "Имя: LAPRAS\\nЕго ещё называют королём морей.$",
        "FuchsiaCity_Text_OmanyteSign": "Имя: OMANYTE\\nЧрезвычайно редкий ПОКЕМОН,\\lвосстановленный из окаменелости.$",
        "FuchsiaCity_Text_KabutoSign": "Имя: KABUTO\\nЧрезвычайно редкий ПОКЕМОН,\\lвосстановленный из окаменелости.$",
        "FuchsiaCity_Text_MyFatherIsGymLeader": "Мой отец - ЛИДЕР ЗАЛА\\nв этом городе.\\pЯ тоже учусь обращаться\\nс ядовитыми ПОКЕМОНАМИ, как он.$",
    },
    "data/maps/PewterCity_Museum_1F_Frlg/scripts.inc": {
        "PewterCity_Museum_1F_Text_Its50YForChildsTicket": "Да-да.\\nДетский билет стоит ¥50.\\pХочешь войти?$",
        "PewterCity_Museum_1F_Text_ComeAgain": "Приходи ещё!$",
        "PewterCity_Museum_1F_Text_Right50YThankYou": "Верно, ¥50!\\nСпасибо!$",
        "PewterCity_Museum_1F_Text_DontHaveEnoughMoney": "У тебя недостаточно денег.$",
        "PewterCity_Museum_1F_Text_PleaseEnjoyYourself": "Приятного посещения.$",
        "PewterCity_Museum_1F_Text_DoYouKnowWhatAmberIs": "С заднего входа не проскочишь!\\nНеплохая попытка, но нет.\\pЛадно уж!\\nТы знаешь, что такое ЯНТАРЬ?$",
        "PewterCity_Museum_1F_Text_AmberContainsGeneticMatter": "ЯНТАРЬ содержит генетический материал\\nдревних ПОКЕМОНОВ.\\pГде-то есть ЛАБОРАТОРИЯ, где пытаются\\nвосстановить ПОКЕМОНА из ЯНТАРЯ.$",
        "PewterCity_Museum_1F_Text_AmberIsFossilizedSap": "ЯНТАРЬ - это окаменевшая смола,\\nкоторая когда-то вытекала из деревьев.\\pСо временем древняя смола затвердела\\nи превратилась в прочный ЯНТАРЬ.$",
        "PewterCity_Museum_1F_Text_ShouldBeGratefulForLongLife": "Я должен быть благодарен\\nза свою долгую жизнь.\\pНикогда не думал, что увижу\\nкости дракона!$",
        "PewterCity_Museum_1F_Text_WantYouToGetAmberExamined": "Тсс! Послушай, мне нужно\\nподелиться с кем-то секретом.\\pДумаю, в этом куске ЯНТАРЯ\\nесть ДНК ПОКЕМОНА!\\pЕсли ПОКЕМОНОВ удастся воскресить,\\nэто станет научным прорывом.\\pНо коллеги просто не слушают меня.\\pПоэтому у меня к тебе просьба!\\pОтнеси это на исследование\\nв какую-нибудь ЛАБОРАТОРИЮ ПОКЕМОНОВ.$",
        "PewterCity_Museum_1F_Text_ReceivedOldAmberFromMan": "{PLAYER} получил СТАРЫЙ ЯНТАРЬ\\nот мужчины.$",
        "PewterCity_Museum_1F_Text_GetOldAmberChecked": "Тсс!\\nПроверь СТАРЫЙ ЯНТАРЬ!$",
        "PewterCity_Museum_1F_Text_DontHaveSpaceForThis": "Для этого нет места.$",
        "PewterCity_Museum_1F_Text_WeHaveTwoFossilsOnExhibit": "У нас выставлены две окаменелости\\nредких древних ПОКЕМОНОВ.$",
        "PewterCity_Museum_1F_Text_BeautifulPieceOfAmber": "Здесь лежит красивый кусок\\nпрозрачного золотистого ЯНТАРЯ.$",
        "PewterCity_Museum_1F_Text_AerodactylFossil": "Окаменелость AERODACTYL\\nДревний и редкий ПОКЕМОН.$",
        "PewterCity_Museum_1F_Text_KabutopsFossil": "Окаменелость KABUTOPS\\nДревний и редкий ПОКЕМОН.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/CeladonCity_Frlg/scripts.inc": 18,
    "data/maps/FuchsiaCity_Frlg/scripts.inc": 18,
    "data/maps/PewterCity_Museum_1F_Frlg/scripts.inc": 17,
}
EXPECTED_TOTAL = 53


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
        if '.string "' in line and line.count('"') < 2:
            die(f"{rel}:{lineno}: physical newline inside assembler string")
    if re.search(r"\\\\[npl]", text):
        die(f"{rel}: doubled FireRed runtime escape found")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    total = 0
    translated_by_file: dict[str, int] = {}

    for rel_str, patches in FILES.items():
        rel = Path(rel_str)
        expected = EXPECTED_COUNTS[rel_str]
        if len(patches) != expected:
            die(f"{rel}: expected {expected} mappings, got {len(patches)}")
        path = root / rel
        if not path.is_file():
            die(f"missing target: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in patches.items():
            validate_translation(label, translated)
            text = replace_block(text, label, translated)
        validate_written_file(rel, text)
        path.write_text(text, encoding="utf-8")
        translated_by_file[rel_str] = len(patches)
        total += len(patches)

    if total != EXPECTED_TOTAL:
        die(f"expected {EXPECTED_TOTAL} translated blocks, got {total}")

    audit = root / "build" / "qarro_ru_city_museum_v3_108_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(
        json.dumps(
            {
                "marker": MARKER,
                "translatedBlockCount": total,
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
        ) + "\n",
        encoding="utf-8",
    )
    print(
        f"[{MARKER}] PASS: translated {total} runtime blocks across 3 files; "
        "Ash Bond/Ash Cap untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
