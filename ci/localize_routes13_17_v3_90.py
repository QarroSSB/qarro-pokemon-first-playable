#!/usr/bin/env python3
"""Qarro v3.90 bulk Russian localization: Route 13 + Route 17.

Translates all 33 Route 13 and all 36 Route 17 FireRed runtime text blocks from
pinned Expansion 1.17.0. Pokemon species, Move and Ability proper names remain
English by project canon. Ash Bond / Ash Cap and gameplay logic are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTES13_17_V3_90"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    Path("data/maps/Route13_Frlg/scripts.inc"): {
        "Route13_Text_SebastianIntro": "Мои птичьи ПОКЕМОНЫ хотят\\nс тобой сразиться!$",
        "Route13_Text_SebastianDefeat": "Моя связка PIDGEY и PIDGEOTTO\\nпроиграла?$",
        "Route13_Text_SebastianPostBattle": "Мои ПОКЕМОНЫ выглядят счастливыми,\\nдаже несмотря на поражение.$",
        "Route13_Text_SusieIntro": "Говорят, для ребёнка я очень сильна.$",
        "Route13_Text_SusieDefeat": "Ох!\\nЯ проиграла!$",
        "Route13_Text_SusiePostBattle": "Я хочу стать хорошим ТРЕНЕРОМ.\\nБуду усердно тренироваться, вот увидишь.$",
        "Route13_Text_ValerieIntro": "Ух ты!\\nКакие у тебя крутые ЗНАЧКИ!$",
        "Route13_Text_ValerieDefeat": "Недостаточно!$",
        "Route13_Text_ValeriePostBattle": "Эти ЗНАЧКИ ты получил у\\nЛИДЕРОВ ЗАЛОВ. Я знаю!$",
        "Route13_Text_GwenIntro": "Мои милые ПОКЕМОНЫ хотят\\nс тобой познакомиться.$",
        "Route13_Text_GwenDefeat": "Здорово!\\nТы победил без вопросов!$",
        "Route13_Text_GwenPostBattle": "ПОКЕМОНАМ нужно сражаться,\\nчтобы становиться сильнее.$",
        "Route13_Text_AlmaIntro": "Однажды в пещере я нашла КАРБОС,\\nкогда занималась спелеологией.$",
        "Route13_Text_AlmaDefeat": "Ой, как жаль!\\nЯ всё испортила!$",
        "Route13_Text_AlmaPostBattle": "КАРБОС повысил СКОРОСТЬ\\nмоего ПОКЕМОНА.$",
        "Route13_Text_PerryIntro": "Я не проиграю.\\nТолько не с попутным ветром!$",
        "Route13_Text_PerryDefeat": "Ветер переменился!$",
        "Route13_Text_PerryPostBattle": "Я выдохся.\\nНаверное, полечу домой с FLY.$",
        "Route13_Text_LolaIntro": "Конечно, поиграю с тобой, лапочка.$",
        "Route13_Text_LolaDefeat": "Ой!\\nАх ты маленький зверёк!$",
        "Route13_Text_LolaPostBattle": "Интересно, кто сильнее - самцы\\nили самки ПОКЕМОНОВ?$",
        "Route13_Text_SheilaIntro": "Хочешь устроить со мной\\nбой ПОКЕМОНОВ?$",
        "Route13_Text_SheilaDefeat": "Уже всё?$",
        "Route13_Text_SheilaPostBattle": "Вообще-то я совсем не разбираюсь\\nв ПОКЕМОНАХ.\\pТех, кого использую, я выбрала\\nпросто за внешность!$",
        "Route13_Text_JaredIntro": "Чего уставился?$",
        "Route13_Text_JaredDefeat": "Чёрт!\\nШестерёнки сорвало!$",
        "Route13_Text_JaredPostBattle": "Проваливай!$",
        "Route13_Text_RobertIntro": "Я всегда выбираю птичьих ПОКЕМОНОВ.\\nЯ посвятил себя только им.$",
        "Route13_Text_RobertDefeat": "Энергия кончилась!$",
        "Route13_Text_RobertPostBattle": "Хотел бы я летать, как PIDGEY\\nи PIDGEOTTO...$",
        "Route13_Text_LookToLeftOfThatPost": "СОВЕТЫ ТРЕНЕРА\\pСмотри, смотри!\\nПосмотри слева от этого столба!$",
        "Route13_Text_SelectToSwitchItems": "СОВЕТЫ ТРЕНЕРА\\pНажми SELECT, чтобы менять местами\\nпредметы в окне ПРЕДМЕТОВ.$",
        "Route13_Text_RouteSign": "МАРШРУТ 13\\nНа север - МОСТ ТИШИНЫ$",
    },
    Path("data/maps/Route17_Frlg/scripts.inc"): {
        "Route17_Text_RaulIntro": "На боях с детьми быстро не разбогатеешь.$",
        "Route17_Text_RaulDefeat": "Перегорел!$",
        "Route17_Text_RaulPostBattle": "На ВЕЛОДОРОГЕ валяются полезные вещи.\\pИх можно подбирать и выгодно продавать.$",
        "Route17_Text_IsaiahIntro": "Я очень горжусь своей формой, малыш.\\nНу давай!$",
        "Route17_Text_IsaiahDefeat": "Ух!$",
        "Route17_Text_IsaiahPostBattle": "Да я тебя одним животом отсюда\\nвытолкну!$",
        "Route17_Text_VirgilIntro": "Едешь в ФУКСИЮ?$",
        "Route17_Text_VirgilDefeat": "Разбился и сгорел!$",
        "Route17_Text_VirgilPostBattle": "Обожаю мчаться с горы!$",
        "Route17_Text_BillyIntro": "Мы БАЙКЕРЫ!\\nМы здесь хозяева дорог!$",
        "Route17_Text_BillyDefeat": "Размазал!$",
        "Route17_Text_BillyPostBattle": "Ищешь приключений?$",
        "Route17_Text_NikolasIntro": "Пусть VOLTORB как следует тебя шарахнет!$",
        "Route17_Text_NikolasDefeat": "Заземлили!$",
        "Route17_Text_NikolasPostBattle": "Я поймал своего VOLTORB на заброшенной\\nЭЛЕКТРОСТАНЦИИ.$",
        "Route17_Text_ZeekIntro": "Я повышал уровень ПОКЕМОНА, но он\\nне эволюционирует. Почему?$",
        "Route17_Text_ZeekDefeat": "Ах ты!$",
        "Route17_Text_ZeekPostBattle": "Может, некоторым ПОКЕМОНАМ для эволюции\\nнужны особые КАМНИ.$",
        "Route17_Text_JamalIntro": "Мне надо немного размяться!$",
        "Route17_Text_JamalDefeat": "Фух!\\nОтличная тренировка!$",
        "Route17_Text_JamalPostBattle": "Наверняка я немного сбросил вес!$",
        "Route17_Text_CoreyIntro": "Будь бунтарём!$",
        "Route17_Text_CoreyDefeat": "А-а-а-а!$",
        "Route17_Text_CoreyPostBattle": "Будь готов драться за свои убеждения!$",
        "Route17_Text_JaxonIntro": "Классный ВЕЛОСИПЕД!\\nКак он в управлении?$",
        "Route17_Text_JaxonDefeat": "Чёрт!$",
        "Route17_Text_JaxonPostBattle": "На склоне очень трудно рулить.$",
        "Route17_Text_WilliamIntro": "Отвали, мелкий!\\nЯ вымотался!$",
        "Route17_Text_WilliamDefeat": "Теперь доволен?$",
        "Route17_Text_WilliamPostBattle": "Мне бы немного поспать!$",
        "Route17_Text_WatchOutForDiscardedItems": "Объявление.\\pОсторожно с выброшенными вещами.$",
        "Route17_Text_SameSpeciesGrowDifferentRates": "СОВЕТЫ ТРЕНЕРА\\pВсе ПОКЕМОНЫ уникальны.\\pДаже ПОКЕМОНЫ одного вида и уровня\\nразвиваются с разной скоростью.$",
        "Route17_Text_PressBToStayInPlace": "СОВЕТЫ ТРЕНЕРА\\pНа склоне удерживай кнопку B,\\nчтобы оставаться на месте.$",
        "Route17_Text_RouteSign": "МАРШРУТ 17\\nСЕЛАДОН - ФУКСИЯ$",
        "Route17_Text_DontThrowGameThrowBalls": "Объявление!\\pНе бросай игру - лучше бросай\\nПОКЕБОЛЫ!$",
        "Route17_Text_CyclingRoadSign": "ВЕЛОДОРОГА\\nЗдесь склон заканчивается!$",
    },
}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def replace_block(text: str, label: str, translated: str) -> str:
    match = re.search(rf"(?m)^{re.escape(label)}::\s*$", text)
    if not match:
        die(f"missing label {label}")
    next_label = LABEL_RE.search(text, match.end())
    end = next_label.start() if next_label else len(text)
    block = f"{label}::\n\t.string " + json.dumps(translated, ensure_ascii=False) + "\n\n"
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

    audit = {
        "marker": MARKER,
        "translatedRuntimeBlocks": total,
        "changedFiles": changed,
        "pokemonMoveAbilityProperNamesStayEnglish": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_routes13_17_v3_90_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if total != 69:
        die(f"expected 69 translated blocks, got {total}")
    print(f"[{MARKER}] PASS: translated {total} runtime blocks across Route 13 + Route 17")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
