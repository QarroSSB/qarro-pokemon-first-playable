#!/usr/bin/env python3
"""Qarro v3.105: localize Memorial Pillar, Silph Co. 6F and Outcast Island runtime text.

Translates exactly 61 English-only FireRed runtime blocks from the v3.104
surface audit:
  * FiveIsland_MemorialPillar_Frlg: 21
  * SilphCo_6F_Frlg: 20
  * SixIsland_OutcastIsland_Frlg: 20

Pokemon species, Move and Ability proper names remain English by project canon.
The writer rejects physical newlines inside translation values so the v3.103
assembler-string regression cannot recur. Gameplay/trainer data and Ash code
are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_MEMORIAL_SILPH6_OUTCAST_V3_105"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/FiveIsland_MemorialPillar_Frlg/scripts.inc": {
        "FiveIsland_MemorialPillar_Text_MiloIntro": "Я старший из БРАТЬЕВ-ПТИЦЕЛОВ.\\pЛучшее в птицах...\\nКонечно же, клюв.$",
        "FiveIsland_MemorialPillar_Text_MiloDefeat": "Ох, как остро!$",
        "FiveIsland_MemorialPillar_Text_MiloPostBattle": "Отсюда можно долететь\\nдо ЧЕТВЁРТОГО ОСТРОВА.$",
        "FiveIsland_MemorialPillar_Text_ChazIntro": "Я средний из БРАТЬЕВ-ПТИЦЕЛОВ.\\pЛучшее в птицах...\\nКонечно же, крылья.$",
        "FiveIsland_MemorialPillar_Text_ChazDefeat": "Хлоп-хлоп!$",
        "FiveIsland_MemorialPillar_Text_ChazPostBattle": "Там неподалёку был\\nочень мрачный парень.$",
        "FiveIsland_MemorialPillar_Text_HaroldIntro": "Я младший из БРАТЬЕВ-ПТИЦЕЛОВ.\\pЛучшее в птицах...\\nКонечно же, пух.$",
        "FiveIsland_MemorialPillar_Text_HaroldDefeat": "Пух такой мягкий...\\nОт него клонит в сон...$",
        "FiveIsland_MemorialPillar_Text_HaroldPostBattle": "Я счастлив, когда птицы-ПОКЕМОНЫ\\nигриво просят внимания...$",
        "FiveIsland_MemorialPillar_Text_ScrubScrub": "Тру, тру...$",
        "FiveIsland_MemorialPillar_Text_YourMonsLookHealthy": "Привет...\\nТвои ПОКЕМОНЫ выглядят здоровыми...$",
        "FiveIsland_MemorialPillar_Text_ThisIsWhereIBuriedMyOnix": "Здесь я похоронил своего ONIX...\\nЕго звали TECTONIX...$",
        "FiveIsland_MemorialPillar_Text_HereLiesTectonixLemonadeOffering": "На валуне высечено:\\nЗДЕСЬ ПОКОИТСЯ TECTONIX.\\pПеред могилой оставлена\\nбанка ЛИМОНАДА.$",
        "FiveIsland_MemorialPillar_Text_LeaveAnotherLemonadeOffering": "Хочешь оставить ещё\\nЛИМОНАД в память о нём?$",
        "FiveIsland_MemorialPillar_Text_PlacedCanOfLemonade": "{PLAYER} поставил банку ЛИМОНАДА\\nперед могилой.$",
        "FiveIsland_MemorialPillar_Text_ThankYouPleaseTakeThis": "С-спасибо...\\pTECTONIX очень любил\\nэтот напиток...\\pЯ тебя даже не знаю,\\nно твоя доброта...\\pМне стало немного легче.\\pПожалуйста, возьми это\\nв знак благодарности.$",
        "FiveIsland_MemorialPillar_Text_BeGoodToYourMonsToo": "Пожалуйста, береги\\nи своих ПОКЕМОНОВ.$",
        "FiveIsland_MemorialPillar_Text_DontHaveRoomForIt": "Если места нет,\\nя сохраню это до встречи.$",
        "FiveIsland_MemorialPillar_Text_StillHaveThingAsMyThanks": "О, это снова ты...\\pУ меня всё ещё есть подарок,\\nкоторый я хотел тебе отдать.$",
        "FiveIsland_MemorialPillar_Text_ScrubScrubTectonix": "Тру, тру...\\p... ... ...\\nTECTONIX...$",
        "FiveIsland_MemorialPillar_Text_HereLiesTectonix": "Камни аккуратно сложены\\nв памятную насыпь.\\pНа валуне высечено:\\nЗДЕСЬ ПОКОИТСЯ TECTONIX.$",
    },
    "data/maps/SilphCo_6F_Frlg/scripts.inc": {
        "SilphCo_6F_Text_RocketsTookOverBuilding": "КОМАНДА R ворвалась\\nи захватила здание!$",
        "SilphCo_6F_Text_BetterGetBackToWork": "Ну, пора возвращаться к работе.$",
        "SilphCo_6F_Text_HelpMePlease": "Ох, беда, беда...\\nПомоги мне, пожалуйста!$",
        "SilphCo_6F_Text_WeGotEngaged": "Мы обручились.\\nХе-хе!$",
        "SilphCo_6F_Text_ThatManIsSuchACoward": "Тот мужчина рядом со мной...\\nОн такой трус!$",
        "SilphCo_6F_Text_NeedsMeToLookAfterHim": "Он такой беспомощный, что ему\\nнужна такая опека, как моя.$",
        "SilphCo_6F_Text_RocketsTryingToConquerWorld": "КОМАНДА R хочет захватить мир\\nс помощью ПОКЕМОНОВ.$",
        "SilphCo_6F_Text_RocketsRanAwayBecauseOfYou": "КОМАНДА R сбежала,\\nи всё благодаря тебе!$",
        "SilphCo_6F_Text_TargetedSilphForOurMonProducts": "Они нацелились на СИЛФ\\nиз-за наших товаров для ПОКЕМОНОВ.$",
        "SilphCo_6F_Text_ComeWorkForSilphWhenYoureOlder": "Когда подрастёшь,\\nприходи работать в СИЛФ.$",
        "SilphCo_6F_Text_Grunt1Intro": "Я один из четырёх\\nБРАТЬЕВ КОМАНДЫ R!$",
        "SilphCo_6F_Text_Grunt1Defeat": "Я прогорел!$",
        "SilphCo_6F_Text_Grunt1PostBattle": "Неважно!\\nБратья за меня отомстят!$",
        "SilphCo_6F_Text_TaylorIntro": "Этот мерзкий ПРЕЗИДЕНТ!\\pТак ему и надо за то, что\\nсослал меня в ФИЛИАЛ ТИКСИ!\\pУверен, поэтому КОМАНДА R\\nи пришла за нами!$",
        "SilphCo_6F_Text_TaylorDefeat": "Чёрт!$",
        "SilphCo_6F_Text_TaylorPostBattle": "ФИЛИАЛ ТИКСИ?\\nЭто в русской глуши!$",
        "SilphCo_6F_Text_Grunt2Intro": "Смеешь предавать КОМАНДУ R?$",
        "SilphCo_6F_Text_Grunt2Defeat": "Предатель!$",
        "SilphCo_6F_Text_Grunt2PostBattle": "Если ты за справедливость,\\nзначит, предаёшь нас, злодеев!$",
        "SilphCo_6F_Text_FloorSign": "ГЛАВНЫЙ ОФИС СИЛФ\\n6-Й ЭТАЖ$",
    },
    "data/maps/SixIsland_OutcastIsland_Frlg/scripts.inc": {
        "SixIsland_OutcastIsland_Text_RocketIntro": "Здесь нет ни одного\\nредкого ПОКЕМОНА!\\pМеня это бесит.\\nСорву злость на тебе!$",
        "SixIsland_OutcastIsland_Text_RocketDefeat": "...Что?$",
        "SixIsland_OutcastIsland_Text_RocketPostBattle": "Слушай, ты ведь не видел\\nредких ПОКЕМОНОВ, а?$",
        "SixIsland_OutcastIsland_Text_TylorIntro": "Мне совсем не везёт.\\nБой хоть немного развлечёт!$",
        "SixIsland_OutcastIsland_Text_TylorDefeat": "Нет, удачи так и нет...$",
        "SixIsland_OutcastIsland_Text_TylorPostBattle": "Не могу же я вернуться домой,\\nничего не поймав.$",
        "SixIsland_OutcastIsland_Text_MymoIntro": "Фух... Фух...\\pЯ доплыл сюда от ПОРТА\\nШЕСТОГО ОСТРОВА без остановки.$",
        "SixIsland_OutcastIsland_Text_MymoDefeat": "Фух...\\nФух...$",
        "SixIsland_OutcastIsland_Text_MymoPostBattle": "Я только на полпути...\\nСовсем выбился из сил...$",
        "SixIsland_OutcastIsland_Text_NicoleIntro": "Знаешь, выпускать ПОКЕМОНОВ\\nво время плавания непросто.$",
        "SixIsland_OutcastIsland_Text_NicoleDefeat": "В плавании я тебе не проиграла.\\nТак что меня это не задевает.$",
        "SixIsland_OutcastIsland_Text_NicolePostBattle": "Идёшь на остров дальше отсюда?\\pЯ не увидела там\\nничего интересного.$",
        "SixIsland_OutcastIsland_Text_AvaIntro": "АВА: Давай устроим морской\\nбой два на два!$",
        "SixIsland_OutcastIsland_Text_AvaDefeat": "АВА: Ого, ты великолепен!\\nИ даже сражаешься один!$",
        "SixIsland_OutcastIsland_Text_AvaPostBattle": "АВА: Знаешь, море мне\\nнравится больше любого бассейна.$",
        "SixIsland_OutcastIsland_Text_AvaNotEnoughMons": "АВА: Хочешь сразиться с нами?\\pТогда тебе нужны хотя бы\\nдва ПОКЕМОНА.$",
        "SixIsland_OutcastIsland_Text_GebIntro": "ГЕБ: Старшая сестра, помоги!\\nПожалуйста, сразись со мной!$",
        "SixIsland_OutcastIsland_Text_GebDefeat": "ГЕБ: Ух ты, сестра,\\nэтот человек правда силён!$",
        "SixIsland_OutcastIsland_Text_GebPostBattle": "ГЕБ: Я держусь за сестру,\\nпотому что не достаю до дна.$",
        "SixIsland_OutcastIsland_Text_GebNotEnoughMons": "ГЕБ: Сразись со мной\\nи моей сестрой!\\p...Ой, у тебя нет\\nдвух ПОКЕМОНОВ?$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/FiveIsland_MemorialPillar_Frlg/scripts.inc": 21,
    "data/maps/SilphCo_6F_Frlg/scripts.inc": 20,
    "data/maps/SixIsland_OutcastIsland_Frlg/scripts.inc": 20,
}
EXPECTED_TOTAL = 61


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
            die(f"{rel}:{lineno}: unterminated assembler string")
    if re.search(r"\\\\[npl]", text):
        die(f"{rel}: doubled FireRed runtime escape found")
    if "Ash Bond" in text or "Ash Cap" in text:
        die(f"{rel}: forbidden Ash token found")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    total = 0
    by_file: dict[str, int] = {}

    for rel_str, patches in FILES.items():
        rel = Path(rel_str)
        expected = EXPECTED_COUNTS[rel_str]
        if len(patches) != expected:
            die(f"{rel}: expected {expected} patches, got {len(patches)}")
        path = root / rel
        if not path.is_file():
            die(f"missing source file: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in patches.items():
            validate_translation(label, translated)
            text = replace_block(text, label, translated)
        validate_written_file(rel, text)
        path.write_text(text, encoding="utf-8")
        by_file[rel_str] = len(patches)
        total += len(patches)

    if total != EXPECTED_TOTAL:
        die(f"expected exactly {EXPECTED_TOTAL} translated blocks, got {total}")

    out = root / "build" / "qarro_ru_memorial_silph6_outcast_v3_105_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "marker": MARKER,
                "translatedBlockCount": total,
                "translatedByFile": by_file,
                "physicalNewlineGuard": True,
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
    print(f"[{MARKER}] PASS: translated {total} runtime blocks across {len(FILES)} files; Ash code untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
