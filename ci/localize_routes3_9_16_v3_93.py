#!/usr/bin/env python3
"""Qarro v3.93 bulk Russian localization: Route 3 + Route 9 + Route 16.

Translates all English-only FireRed runtime _Text_ blocks reported by the
current v3.21 surface audit for these three Kanto routes: 26 + 28 + 29 = 83.
Pokemon species, Move and Ability proper names remain English by project canon.
Ash Bond / Ash Cap and gameplay logic are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTES3_9_16_V3_93"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    Path("data/maps/Route3_Frlg/scripts.inc"): {
        "Route3_Text_TunnelFromCeruleanTiring": "Фух... Надо отдохнуть...\\nУф...\\pЭтот тоннель из ЦЕРУЛИНА\\nвымотал меня!$",
        "Route3_Text_ColtonIntro": "Эй!\\nЯ видел тебя в ВИРИДИАНСКОМ ЛЕСУ!$",
        "Route3_Text_ColtonDefeat": "Ты снова меня победил!$",
        "Route3_Text_ColtonPostBattle": "Кроме лесных ПОКЕМОНОВ\\nесть и много других видов.$",
        "Route3_Text_BenIntro": "Привет!\\nЯ люблю шорты!\\pОни такие удобные,\\nи носить их легко!$",
        "Route3_Text_BenDefeat": "Не верю!$",
        "Route3_Text_BenPostBattle": "Ты пользуешься ПК в ЦЕНТРЕ ПОКЕМОНОВ\\nдля хранения ПОКЕМОНОВ?\\pВ каждом БОКСЕ помещается\\nдо 30 ПОКЕМОНОВ.$",
        "Route3_Text_JaniceIntro": "Извини!\\nТы ведь на меня посмотрел, да?$",
        "Route3_Text_JaniceDefeat": "Какой ты злой!$",
        "Route3_Text_JanicePostBattle": "Не глазей на ТРЕНЕРОВ,\\nесли не хочешь сражаться!$",
        "Route3_Text_GregIntro": "Ты ТРЕНЕР?\\nТогда начинаем прямо сейчас!$",
        "Route3_Text_GregDefeat": "Будь у меня новые ПОКЕМОНЫ,\\nя бы победил!$",
        "Route3_Text_GregPostBattle": "Если БОКС на ПК заполнится,\\nпросто переключись на другой.$",
        "Route3_Text_SallyIntro": "Этот твой взгляд...\\nТак интригует!$",
        "Route3_Text_SallyDefeat": "Будь добрее!$",
        "Route3_Text_SallyPostBattle": "Боя можно избежать,\\nесли ТРЕНЕР тебя не заметит.$",
        "Route3_Text_CalvinIntro": "Эй! Ты не в шортах!\\nЧто с тобой не так?$",
        "Route3_Text_CalvinDefeat": "Проиграл!\\nПроиграл! Проиграл!$",
        "Route3_Text_CalvinPostBattle": "Я всегда хожу в шортах, даже зимой.\\nЭто мой принцип.$",
        "Route3_Text_JamesIntro": "Я сражусь с тобой ПОКЕМОНОМ,\\nкоторого только что поймал.$",
        "Route3_Text_JamesDefeat": "Вот и всё!$",
        "Route3_Text_JamesPostBattle": "Тренированные ПОКЕМОНЫ сильнее,\\nчем дикие.$",
        "Route3_Text_RobinIntro": "Ай!\\nТы меня тронул?$",
        "Route3_Text_RobinDefeat": "И это всё?$",
        "Route3_Text_RobinPostBattle": "МАРШРУТ 4 находится у подножия\\nЛУННОЙ ГОРЫ.$",
        "Route3_Text_RouteSign": "МАРШРУТ 3\\nВПЕРЕДИ ЛУННАЯ ГОРА$",
    },
    Path("data/maps/Route9_Frlg/scripts.inc"): {
        "Route9_Text_AliciaIntro": "У тебя есть ПОКЕМОНЫ!\\nТы мой!$",
        "Route9_Text_AliciaDefeat": "Ты меня обманул...$",
        "Route9_Text_AliciaPostBattle": "Впереди кромешно тёмный тоннель.\\pЧтобы пройти его,\\nтебе понадобится FLASH.$",
        "Route9_Text_ChrisIntro": "Кто это идёт там\\nс такими классными ПОКЕМОНАМИ?$",
        "Route9_Text_ChrisDefeat": "Вырубил с одного удара!$",
        "Route9_Text_ChrisPostBattle": "Иди дальше!$",
        "Route9_Text_DrewIntro": "Я иду через СКАЛЬНЫЙ ТОННЕЛЬ,\\nчтобы попасть в ЛАВАНДЕР...$",
        "Route9_Text_DrewDefeat": "Не дотянул...$",
        "Route9_Text_DrewPostBattle": "Ты тоже идёшь в СКАЛЬНЫЙ ТОННЕЛЬ?$",
        "Route9_Text_CaitlinIntro": "Не смей смотреть на меня свысока!$",
        "Route9_Text_CaitlinDefeat": "Нет!\\nТы слишком силён.$",
        "Route9_Text_CaitlinPostBattle": "У тебя явно есть талант.\\nУдачи!$",
        "Route9_Text_JeremyIntro": "Бу-га-га!\\nОтлично! Я как раз скучал!$",
        "Route9_Text_JeremyDefeat": "Давай ещё!\\pА, погоди.\\nУ меня кончились ПОКЕМОНЫ!$",
        "Route9_Text_JeremyPostBattle": "Хватило же тебе смелости\\nвыступить против меня!$",
        "Route9_Text_BriceIntro": "Ха-ха-ха!\\nА ты крепкий малыш!$",
        "Route9_Text_BriceDefeat": "Это ещё что?$",
        "Route9_Text_BricePostBattle": "Ха-ха-ха!\\nДети должны быть крепкими!$",
        "Route9_Text_BrentIntro": "Я каждый день вставал рано,\\nчтобы растить ПОКЕМОНОВ из коконов!$",
        "Route9_Text_BrentDefeat": "ЧТО?\\pСтолько времени впустую!$",
        "Route9_Text_BrentPostBattle": "Чтобы стать сильнее, мне нужно\\nловить не только жуков...$",
        "Route9_Text_AlanIntro": "Ха-ха-ха!\\nДавай, нападай!$",
        "Route9_Text_AlanDefeat": "Ха-ха-ха!\\nТы победил по-честному!$",
        "Route9_Text_AlanPostBattle": "Ха-ха-ха!\\nМы, крепкие парни, всегда смеёмся!$",
        "Route9_Text_ConnerIntro": "Вперёд, мои супер-ПОКЕМОНЫ-ЖУКИ!$",
        "Route9_Text_ConnerDefeat": "Мои жуки...$",
        "Route9_Text_ConnerPostBattle": "Если тебе не нравятся ПОКЕМОНЫ-ЖУКИ,\\nты меня бесишь!$",
        "Route9_Text_RouteSign": "МАРШРУТ 9\\nЦЕРУЛИН - СКАЛЬНЫЙ ТОННЕЛЬ$",
    },
    Path("data/maps/Route16_Frlg/scripts.inc"): {
        "Route16_Text_LaoIntro": "Чего тебе надо?$",
        "Route16_Text_LaoDefeat": "Только попробуй засмеяться!$",
        "Route16_Text_LaoPostBattle": "Нам нравится просто торчать здесь.\\nТебе-то что?$",
        "Route16_Text_KojiIntro": "Крутой ВЕЛОСИПЕД!\\nА ну отдавай!$",
        "Route16_Text_KojiDefeat": "Нокаут!$",
        "Route16_Text_KojiPostBattle": "Да ну его, кому нужен твой ВЕЛОСИПЕД!$",
        "Route16_Text_LukeIntro": "Выходи поиграть, мышонок!$",
        "Route16_Text_LukeDefeat": "Ах ты крысёныш!$",
        "Route16_Text_LukePostBattle": "Ненавижу проигрывать!\\nИсчезни с глаз!$",
        "Route16_Text_HideoIntro": "Эй, ты меня только что толкнул!$",
        "Route16_Text_HideoDefeat": "Бабах!$",
        "Route16_Text_HideoPostBattle": "Мы всё равно будем торчать здесь,\\nнравится тебе это или нет.\\pИз ФУКСИИ можно объехать к ВЕРМИЛИОНУ\\nпо побережью.$",
        "Route16_Text_CamronIntro": "Я голодный и злой!\\nМне нужна груша для битья!$",
        "Route16_Text_CamronDefeat": "Плохо, плохо, плохо!$",
        "Route16_Text_CamronPostBattle": "Раз уж у меня есть ПОКЕМОНЫ,\\nпусть будут свирепыми.\\pЯ натравлю их на врагов,\\nчтобы от тех клочья остались.$",
        "Route16_Text_RubenIntro": "Эй, ты!\\nДавай повеселимся!$",
        "Route16_Text_RubenDefeat": "Не зли меня!$",
        "Route16_Text_RubenPostBattle": "Я развлекаюсь, пугая людей\\nсвоими вонючими ПОКЕМОНАМИ.\\pОни отлично умеют всех пугать.\\nИ ещё кусаются.$",
        "Route16_Text_MonSprawledOutInSlumber": "ПОКЕМОН растянулся на дороге\\nи крепко, безмятежно спит.$",
        "Route16_Text_CyclingRoadSign": "Наслаждайся спуском!\\nВЕЛОДОРОГА$",
        "Route16_Text_RouteSign": "МАРШРУТ 16\\nСЕЛАДОН - ФУКСИЯ$",
        "Route16_Text_JedIntro": "JED: Наша любовь не знает границ.\\nМы любим друг друга и не скрываем этого!$",
        "Route16_Text_JedDefeat": "JED: О нет!\\nМоя любовь увидела, как я проиграл!$",
        "Route16_Text_JedPostBattle": "JED: Слушай, LEA.\\nТебе стоит поменьше думать обо мне.$",
        "Route16_Text_JedNotEnoughMons": "JED: У тебя всего один ПОКЕМОН?\\nНеужели в твоём сердце нет любви?$",
        "Route16_Text_LeaIntro": "LEA: Иногда сила нашей любви\\nдаже пугает меня.$",
        "Route16_Text_LeaDefeat": "LEA: Ох! Но JED выглядит круто\\nдаже после поражения!$",
        "Route16_Text_LeaPostBattle": "LEA: Хи-хи, прости.\\nJED такой классный.$",
        "Route16_Text_LeaNotEnoughMons": "LEA: Ой, у тебя нет двух\\nПОКЕМОНОВ?\\pТебе и твоему ПОКЕМОНУ\\nне одиноко?$",
    },
}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def asm_quote(text: str) -> str:
    # The FireRed string parser expects control codes like \n/\p/\l with one
    # literal backslash. Escape only quote characters for the assembly string.
    return text.replace('"', '\\"')


def replace_block(text: str, label: str, translated: str) -> str:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, got {len(matches)}")
    match = matches[0]
    next_label = LABEL_RE.search(text, match.end())
    end = next_label.start() if next_label else len(text)
    old = text[match.start():end]
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: block already contains Cyrillic; refusing to overwrite")
    block = f'{label}::\n\t.string "{asm_quote(translated)}"\n\n'
    return text[:match.start()] + block + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    changed = []
    total = 0
    for rel, translations in FILES.items():
        path = root / rel
        if not path.is_file():
            die(f"missing FireRed map script {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in translations.items():
            text = replace_block(text, label, translated)
            total += 1
        path.write_text(text, encoding="utf-8")
        changed.append(str(rel))

    if total != 83:
        die(f"expected 83 translated blocks, got {total}")

    out = root / "build/qarro_ru_routes3_9_16_v3_93_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "translatedRuntimeBlocks": total,
        "changedFiles": changed,
        "pokemonMoveAbilityProperNamesStayEnglish": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[{MARKER}] PASS: translated {total} runtime blocks across Route 3 + Route 9 + Route 16")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
