#!/usr/bin/env python3
"""Qarro v3.113: localize Safari Entrance, Pokemon Tower 5F and Mt. Moon B2F residual runtime text.

Translates exactly 41 English-only FireRed runtime blocks after v3.112:
  * FuchsiaCity_SafariZone_Entrance_Frlg: 14
  * PokemonTower_5F_Frlg: 14
  * MtMoon_B2F_Frlg: 13 residual blocks

Already localized Mt. Moon fossil-choice/Miguel blocks are intentionally untouched.
Pokemon species, Move and Ability proper names remain English by project canon.
Gameplay/trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_SAFARI_TOWER_MTMOON_V3_113"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/FuchsiaCity_SafariZone_Entrance_Frlg/scripts.inc": {
        "FuchsiaCity_SafariZone_Entrance_Text_WelcomeToSafariZone": "Добро пожаловать в ЗОНУ САФАРИ!$",
        "FuchsiaCity_SafariZone_Entrance_Text_PlaySafariGameFor500": "Всего за ¥500 ты можешь сыграть\\nв САФАРИ-ИГРУ.\\pГуляй по огромной зоне сафари\\nи лови кого захочешь.\\pХочешь сыграть?$",
        "FuchsiaCity_SafariZone_Entrance_Text_ThatllBe500WeOnlyUseSpecialBalls": "С тебя ¥500!\\pЗдесь используются только\\nспециальные POKe BALLS.$",
        "FuchsiaCity_SafariZone_Entrance_Text_PlayerReceived30SafariBalls": "{PLAYER} получил 30 SAFARI BALLS\\nу служителя.$",
        "FuchsiaCity_SafariZone_Entrance_Text_CallYouOnPAWhenYouRunOut": "Мы вызовем тебя по громкой связи,\\nкогда кончится время или SAFARI BALLS.\\pЖелаю удачи!$",
        "FuchsiaCity_SafariZone_Entrance_Text_OkayPleaseComeAgain": "Хорошо.\\nПриходи ещё!$",
        "FuchsiaCity_SafariZone_Entrance_Text_OopsNotEnoughMoney": "Ой!\\nНедостаточно денег!$",
        "FuchsiaCity_SafariZone_Entrance_Text_GoingToLeaveSafariZoneEarly": "Ты хочешь покинуть\\nЗОНУ САФАРИ раньше времени?$",
        "FuchsiaCity_SafariZone_Entrance_Text_PleaseReturnSafariBalls": "Пожалуйста, верни оставшиеся\\nSAFARI BALLS.$",
        "FuchsiaCity_SafariZone_Entrance_Text_GoodLuck": "Удачи!$",
        "FuchsiaCity_SafariZone_Entrance_Text_CatchFairShareComeAgain": "Удалось как следует наловить?\\nПриходи ещё!$",
        "FuchsiaCity_SafariZone_Entrance_Text_FirstTimeAtSafariZone": "Привет! Ты впервые\\nв ЗОНЕ САФАРИ?$",
        "FuchsiaCity_SafariZone_Entrance_Text_ExplainSafariZone": "В ЗОНЕ САФАРИ есть четыре зоны.\\pВ каждой встречаются разные ПОКЕМОНЫ,\\nв том числе редкие.\\pЛови их выданными SAFARI BALLS.\\pКроме SAFARI BALLS можно бросать\\nПРИМАНКУ или КАМНИ.\\pПРИМАНКА уменьшает шанс побега,\\nно ПОКЕМОНА становится сложнее поймать.\\pКАМНИ увеличивают шанс побега,\\nно ПОКЕМОНА становится легче поймать.\\pКогда закончатся время или SAFARI BALLS,\\nигра завершится!$",
        "FuchsiaCity_SafariZone_Entrance_Text_SorryYoureARegularHere": "Извини, ты здесь уже завсегдатай!$",
    },
    "data/maps/PokemonTower_5F_Frlg/scripts.inc": {
        "PokemonTower_5F_Text_RestHereInPurifiedSpace": "Подойди, дитя!\\nЯ очистила это место.\\lЗдесь можно отдохнуть.$",
        "PokemonTower_5F_Text_TammyIntro": "Отдай... мне...\\nвсё...$",
        "PokemonTower_5F_Text_TammyDefeat": "Ах!$",
        "PokemonTower_5F_Text_TammyPostBattle": "Я была одержима.$",
        "PokemonTower_5F_Text_RuthIntro": "Ты... присоединишься...\\nк нам...$",
        "PokemonTower_5F_Text_RuthDefeat": "Какой кошмар!$",
        "PokemonTower_5F_Text_RuthPostBattle": "Я была одержима.$",
        "PokemonTower_5F_Text_KarinaIntro": "Зомби!$",
        "PokemonTower_5F_Text_KarinaDefeat": "А?$",
        "PokemonTower_5F_Text_KarinaPostBattle": "Я снова пришла в себя.$",
        "PokemonTower_5F_Text_JanaeIntro": "Ургх...\\nУрф...$",
        "PokemonTower_5F_Text_JanaeDefeat": "Уф!$",
        "PokemonTower_5F_Text_JanaePostBattle": "Злые духи одолели меня, несмотря\\nна мои тренировки в горах...$",
        "PokemonTower_5F_Text_PurifiedZoneMonsFullyHealed": "Ты вошёл в очищенную и защищённую\\nзону.\\pПОКЕМОНЫ {PLAYER} полностью\\nвосстановлены.$",
    },
    "data/maps/MtMoon_B2F_Frlg/scripts.inc": {
        "MtMoon_B2F_Text_LabOnCinnabarRegeneratesFossils": "Далеко отсюда, на ОСТРОВЕ СИННАБАР,\\nесть ЛАБОРАТОРИЯ ПОКЕМОНОВ.\\pТам изучают восстановление\\nПОКЕМОНОВ из ископаемых.$",
        "MtMoon_B2F_Text_Grunt1Intro": "Мы, КОМАНДА R, найдём\\nэти ископаемые!\\pВозрождённые из них ПОКЕМОНЫ\\nпринесут нам огромные деньги!$",
        "MtMoon_B2F_Text_Grunt1Defeat": "Ургх!\\nТеперь я зол!$",
        "MtMoon_B2F_Text_Grunt1PostBattle": "Ты меня разозлил!\\nКОМАНДА R занесёт тебя в чёрный список!$",
        "MtMoon_B2F_Text_Grunt2Intro": "Мы, КОМАНДА R, - бандиты\\nмира ПОКЕМОНОВ!\\lМы внушаем страх своей силой!$",
        "MtMoon_B2F_Text_Grunt2Defeat": "Я всё испортил!$",
        "MtMoon_B2F_Text_Grunt2PostBattle": "Чёрт!\\nМои товарищи этого не потерпят!$",
        "MtMoon_B2F_Text_Grunt3Intro": "У нас тут большое дело!\\nИсчезни, мелкий!$",
        "MtMoon_B2F_Text_Grunt3Defeat": "А ты хорош...$",
        "MtMoon_B2F_Text_Grunt3PostBattle": "Найдёшь ископаемое - отдай мне\\nи проваливай!$",
        "MtMoon_B2F_Text_Grunt4Intro": "Мелким детям не стоит мешаться\\nпод ногами у взрослых!\\pЭто плохо кончится!$",
        "MtMoon_B2F_Text_Grunt4Defeat": "Я в бешенстве!$",
        "MtMoon_B2F_Text_Grunt4PostBattle": "ПОКЕМОНЫ жили здесь задолго\\nдо появления людей.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/FuchsiaCity_SafariZone_Entrance_Frlg/scripts.inc": 14,
    "data/maps/PokemonTower_5F_Frlg/scripts.inc": 14,
    "data/maps/MtMoon_B2F_Frlg/scripts.inc": 13,
}
EXPECTED_TOTAL = 41


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


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


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def replace_block(text: str, label: str, translated: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: target already contains Cyrillic; refusing overwrite")
    if ".string " not in old:
        die(f"{label}: target does not look like a text block")
    safe = translated.replace('"', '\\"')
    block = f'{label}::\n\t.string "{safe}"\n\n'
    return text[:start] + block + text[end:]


def validate_written(rel: Path, text: str) -> None:
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
    translated_by_file = {}
    for rel_s, patches in FILES.items():
        expected = EXPECTED_COUNTS[rel_s]
        if len(patches) != expected:
            die(f"{rel_s}: expected {expected} entries, got {len(patches)}")
        rel = Path(rel_s)
        path = root / rel
        if not path.is_file():
            die(f"missing target: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in patches.items():
            validate_translation(label, translated)
            text = replace_block(text, label, translated)
        validate_written(rel, text)
        path.write_text(text, encoding="utf-8")
        translated_by_file[rel_s] = len(patches)
        total += len(patches)

    if total != EXPECTED_TOTAL:
        die(f"expected {EXPECTED_TOTAL} translated blocks, got {total}")

    audit = root / "build" / "qarro_ru_safari_tower_mtmoon_v3_113_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps({
        "marker": MARKER,
        "translatedBlockCount": EXPECTED_TOTAL,
        "translatedByFile": translated_by_file,
        "alreadyLocalizedMtMoonBlocksTouched": False,
        "physicalNewlinesInsideAsmStrings": False,
        "doubledRuntimeEscapes": False,
        "gameplayLogicTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; gameplay/trainer/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
