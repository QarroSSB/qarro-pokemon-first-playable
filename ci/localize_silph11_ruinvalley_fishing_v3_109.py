#!/usr/bin/env python3
"""Qarro v3.109: localize Silph 11F, Ruin Valley and Route 12 Fishing House.

Translates exactly 49 English-only FireRed runtime blocks from the v3.108
surface audit:
  * SilphCo_11F_Frlg: 17
  * SixIsland_RuinValley_Frlg: 17
  * Route12_FishingHouse_Frlg: 15

Pokemon species, Move and Ability proper names remain English by project canon.
Existing Ruin Valley door/CUT localization is left untouched. The writer rejects
physical newlines, doubled FireRed runtime escapes and unsupported punctuation.
Gameplay/trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_SILPH11_RUINVALLEY_FISHING_V3_109"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/SilphCo_11F_Frlg/scripts.inc": {
        "SilphCo_11F_Text_ThanksForSavingMeDearBoy": "ПРЕЗИДЕНТ: О, юный герой!\\nСпасибо, что спас СИЛФ.\\pЯ никогда не забуду, как ты\\nвыручил нас в минуту опасности.\\pЯ должен тебя отблагодарить.\\pЯ богат и могу позволить себе\\nподарить почти что угодно.\\pДумаю, это подойдёт.$",
        "SilphCo_11F_Text_ThanksForSavingMeDearGirl": "ПРЕЗИДЕНТ: О, юная героиня!\\nСпасибо, что спасла СИЛФ.\\pЯ никогда не забуду, как ты\\nвыручила нас в минуту опасности.\\pЯ должен тебя отблагодарить.\\pЯ богат и могу позволить себе\\nподарить почти что угодно.\\pДумаю, это подойдёт.$",
        "SilphCo_11F_Text_ObtainedMasterBallFromPresident": "{PLAYER} получил МАСТЕР-БОЛ\\nот ПРЕЗИДЕНТА!$",
        "SilphCo_11F_Text_ThatsOurSecretPrototype": "ПРЕЗИДЕНТ: Такое нигде не купить.\\pЭто наш секретный прототип -\\nМАСТЕР-БОЛ.\\pОн без промаха ловит\\nлюбого ПОКЕМОНА!\\pТолько не стоит всем рассказывать,\\nчто он у тебя есть.$",
        "SilphCo_11F_Text_YouHaveNoRoomForThis": "У тебя нет места для этого.$",
        "SilphCo_11F_Text_ThanksForRescuingUs": "СЕКРЕТАРЬ: Спасибо, что спас\\nвсех нас.\\pМы все, от ПРЕЗИДЕНТА до сотрудников,\\nтеперь у тебя в долгу.$",
        "SilphCo_11F_Text_GiovanniIntro": "А, {PLAYER}!\\nМы снова встретились!\\pМы с ПРЕЗИДЕНТОМ обсуждаем\\nважное деловое предложение.\\pНе суй нос во взрослые дела...\\pИли узнаешь, что такое боль!$",
        "SilphCo_11F_Text_GiovanniDefeat": "Аргх!!\\nЯ опять проиграл!?$",
        "SilphCo_11F_Text_GiovanniPostBattle": "Проклятье!\\nТы разрушил наши планы на СИЛФ!\\pНо КОМАНДА R никогда не падёт!\\p{PLAYER}! Не забывай: все ПОКЕМОНЫ\\nсуществуют ради КОМАНДЫ R!\\pМне пора, но я ещё вернусь!$",
        "SilphCo_11F_Text_Grunt2Intro": "Стоять!\\nНе двигайся!$",
        "SilphCo_11F_Text_Grunt2Defeat": "Не надо...\\nПрошу!$",
        "SilphCo_11F_Text_Grunt2PostBattle": "Так ты хочешь увидеть моего БОССА?$",
        "SilphCo_11F_Text_Grunt1Intro": "Стой! У тебя назначена встреча\\nс моим БОССОМ?$",
        "SilphCo_11F_Text_Grunt1Defeat": "А-а-а!\\nРазгромлен!$",
        "SilphCo_11F_Text_Grunt1PostBattle": "Смотри под ноги...\\nМой БОСС любит сильных ПОКЕМОНОВ!$",
        "SilphCo_11F_Text_MonitorHasMonsOnIt": "На мониторе изображены ПОКЕМОНЫ!$",
        "SilphCo_11F_Text_FloorSign": "ГЛАВНЫЙ ОФИС СИЛФ\\n11-Й ЭТАЖ$",
    },
    "data/maps/SixIsland_RuinValley_Frlg/scripts.inc": {
        "SixIsland_RuinValley_Text_CantFigureOutHowToGetInside": "Не могу понять, как мне\\nпопасть внутрь.$",
        "SixIsland_RuinValley_Text_IFoundThisPlace": "Между прочим, это место\\nнашёл именно я.\\pТолько не завидуй так сильно.$",
        "SixIsland_RuinValley_Text_StanlyIntro": "Похоже, в этом мире ещё немало\\nнеразгаданных тайн.$",
        "SixIsland_RuinValley_Text_StanlyDefeat": "Хм...$",
        "SixIsland_RuinValley_Text_StanlyPostBattle": "Советую и тебе хотя бы раз в день\\nзадумываться о тайнах\\lнашего мира.$",
        "SixIsland_RuinValley_Text_FosterIntro": "Любопытно, что заставило тебя\\nприйти сюда?$",
        "SixIsland_RuinValley_Text_FosterDefeat": "Я так давно не сражался, что\\nсовсем потерял форму.$",
        "SixIsland_RuinValley_Text_FosterPostBattle": "На ОСТРОВАХ СЕВИИ есть\\nнесколько древних руин.\\pБольшинству из них\\nочень много лет.$",
        "SixIsland_RuinValley_Text_LarryIntro": "Говорят, на этом острове есть\\nзагадочные камни.\\pДумаю, они как-то связаны\\nс здешними руинами.$",
        "SixIsland_RuinValley_Text_LarryDefeat": "О, любопытно.$",
        "SixIsland_RuinValley_Text_LarryPostBattle": "Вон те руины...\\pМне так и не удалось понять,\\nкак попасть внутрь.$",
        "SixIsland_RuinValley_Text_DarylIntro": "Сражение с тобой на такой высоте!$",
        "SixIsland_RuinValley_Text_DarylDefeat": "Как обидно проиграть тебе\\nтак легко!$",
        "SixIsland_RuinValley_Text_DarylPostBattle": "Почувствуй радость подъёма!$",
        "SixIsland_RuinValley_Text_HectorIntro": "Я неплохо знаю здешние места.$",
        "SixIsland_RuinValley_Text_HectorDefeat": "Не дави так.\\nЯ и сам всё расскажу.$",
        "SixIsland_RuinValley_Text_HectorPostBattle": "На двери руин...\\nСнаружи выгравированы\\lстранные узоры.\\pНо что они значат,\\nя понятия не имею.$",
    },
    "data/maps/Route12_FishingHouse_Frlg/scripts.inc": {
        "Route12_FishingHouse_Text_DoYouLikeToFish": "Я младший брат ГУРУ РЫБАЛКИ.\\pЯ просто обожаю рыбалку!\\nБез неё жить не могу.\\pСкажи, тебе нравится рыбачить?$",
        "Route12_FishingHouse_Text_TakeThisAndFish": "Отлично! Мне нравится твой настрой.\\nДумаю, мы поладим.\\pБери это и рыбачь, юный друг!$",
        "Route12_FishingHouse_Text_ReceivedSuperRod": "{PLAYER} получил СУПЕР-УДОЧКУ\\nот брата ГУРУ РЫБАЛКИ.$",
        "Route12_FishingHouse_Text_IfYouCatchBigMagikarpShowMe": "Рыбалка - это образ жизни!\\nЭто почти поэзия.\\pОт моря до реки - везде ищи\\nсвой самый большой улов.\\pИ у меня есть просьба.\\pЕсли поймаешь этой УДОЧКОЙ\\nкрупного MAGIKARP, покажи мне.\\pЯ люблю не только рыбачить,\\nно и смотреть на гигантских MAGIKARP.$",
        "Route12_FishingHouse_Text_OhThatsDisappointing": "Ох...\\nКак жаль...$",
        "Route12_FishingHouse_Text_TryFishingBringMeMagikarp": "Привет, {PLAYER}!\\nУже ходил на рыбалку?\\pПопробуй СУПЕР-УДОЧКУ\\nв любом водоёме.\\pВ разных местах водятся\\nразные ПОКЕМОНЫ.\\pИ не забудь принести мне\\nогромного MAGIKARP.$",
        "Route12_FishingHouse_Text_OhMagikarpAllowMeToSee": "О? {PLAYER}?\\nДа это же MAGIKARP!\\pДай скорее взглянуть!$",
        "Route12_FishingHouse_Text_WhoaXSizeTakeThis": "... ... ...Ух ты!\\n{STR_VAR_2}!\\pТы умеешь ценить настоящую\\nпоэзию рыбалки!\\pТы обязан взять это.\\nЯ настаиваю!$",
        "Route12_FishingHouse_Text_LookForwardToGreaterRecords": "Буду ждать от тебя\\nновых рекордов!$",
        "Route12_FishingHouse_Text_HuhXSizeSameSizeAsLast": "Хм?\\n{STR_VAR_2}?\\pТочно такой же размер,\\nкак у прошлого.$",
        "Route12_FishingHouse_Text_HmmXSizeDoesntMeasureUp": "Хм...\\nЭтот длиной {STR_VAR_2}.\\pОн не дотягивает до прежнего\\nрекорда - {STR_VAR_3}.$",
        "Route12_FishingHouse_Text_DoesntLookLikeMagikarp": "Эм... Это совсем не похоже\\nна MAGIKARP.$",
        "Route12_FishingHouse_Text_NoRoomForGift": "О нет!\\pУ меня был для тебя подарок,\\nно у тебя нет места.$",
        "Route12_FishingHouse_Text_MostGiganticMagikarpXSize": "Самый огромный MAGIKARP,\\nкоторого я когда-либо видел...\\p{STR_VAR_3}!$",
        "Route12_FishingHouse_Text_BlankChartOfSomeSort": "Это какая-то пустая таблица.\\pЗдесь есть место для записи\\nкаких-то рекордов.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/SilphCo_11F_Frlg/scripts.inc": 17,
    "data/maps/SixIsland_RuinValley_Frlg/scripts.inc": 17,
    "data/maps/Route12_FishingHouse_Frlg/scripts.inc": 15,
}
EXPECTED_TOTAL = 49


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
    translated_by_file: dict[str, int] = {}
    total = 0

    for rel_s, patches in FILES.items():
        rel = Path(rel_s)
        expected = EXPECTED_COUNTS[rel_s]
        if len(patches) != expected:
            die(f"{rel}: expected {expected} translation entries, got {len(patches)}")
        path = root / rel
        if not path.is_file():
            die(f"missing target: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in patches.items():
            validate_translation(label, translated)
            text = replace_block(text, label, translated)
        validate_written_file(rel, text)
        path.write_text(text, encoding="utf-8")
        translated_by_file[rel_s] = len(patches)
        total += len(patches)

    if total != EXPECTED_TOTAL:
        die(f"expected {EXPECTED_TOTAL} translated blocks, got {total}")

    audit = root / "build" / "qarro_ru_silph11_ruinvalley_fishing_v3_109_audit.json"
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
        f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; "
        "Ruin Valley door localization preserved; gameplay/Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
