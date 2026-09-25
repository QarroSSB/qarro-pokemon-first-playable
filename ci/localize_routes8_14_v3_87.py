#!/usr/bin/env python3
"""Qarro v3.87 bulk Russian localization: Route 8 + Route 14.

Translates all 42 Route 8 and all 39 Route 14 FireRed runtime text blocks from
pinned Expansion 1.17.0. Pokemon species, Move and Ability proper names remain
English by project canon. Ash Bond / Ash Cap and gameplay logic are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTES8_14_V3_87"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    Path("data/maps/Route8_Frlg/scripts.inc"): {
        "Route8_Text_AidanIntro": '''Route8_Text_AidanIntro::
\t.string "В ПОКЕМОНАХ ты, похоже, силён.\\n"
\t.string "А как у тебя с химией?$"
''',
        "Route8_Text_AidanDefeat": '''Route8_Text_AidanDefeat::
\t.string "Ай!\\n"
\t.string "Полный провал!$"
''',
        "Route8_Text_AidanPostBattle": '''Route8_Text_AidanPostBattle::
\t.string "В школе у меня получается лучше!$"
''',
        "Route8_Text_StanIntro": '''Route8_Text_StanIntro::
\t.string "Отлично!\\n"
\t.string "Давай сыграем!$"
''',
        "Route8_Text_StanDefeat": '''Route8_Text_StanDefeat::
\t.string "Чёрт!\\n"
\t.string "Чуть-чуть не хватило!$"
''',
        "Route8_Text_StanPostBattle": '''Route8_Text_StanPostBattle::
\t.string "Сегодня всё пошло не так.$"
''',
        "Route8_Text_GlennIntro": '''Route8_Text_GlennIntro::
\t.string "Тебе стоит это знать.\\n"
\t.string "Для победы нужна стратегия!$"
''',
        "Route8_Text_GlennDefeat": '''Route8_Text_GlennDefeat::
\t.string "Это нелогично!$"
''',
        "Route8_Text_GlennPostBattle": '''Route8_Text_GlennPostBattle::
\t.string "Сначала выпускаю GRIMER... потом...\\n"
\t.string "...потом... и затем...$"
''',
        "Route8_Text_PaigeIntro": '''Route8_Text_PaigeIntro::
\t.string "Я люблю NIDORAN и собираю их!$"
''',
        "Route8_Text_PaigeDefeat": '''Route8_Text_PaigeDefeat::
\t.string "Почему?\\n"
\t.string "Почему??$"
''',
        "Route8_Text_PaigePostBattle": '''Route8_Text_PaigePostBattle::
\t.string "Когда ПОКЕМОНЫ взрослеют, они\\n"
\t.string "становятся страшнее! Не эволюционируйте!$"
''',
        "Route8_Text_LeslieIntro": '''Route8_Text_LeslieIntro::
\t.string "В школе весело, но с ПОКЕМОНАМИ тоже!$"
''',
        "Route8_Text_LeslieDefeat": '''Route8_Text_LeslieDefeat::
\t.string "Ты ясно дал понять: мне лучше\\n"
\t.string "заниматься учёбой.$"
''',
        "Route8_Text_LesliePostBattle": '''Route8_Text_LesliePostBattle::
\t.string "Хотелось просто подышать\\n"
\t.string "свежим воздухом, но...\\p"
\t.string "Мы застряли здесь из-за ворот\\n"
\t.string "в САФФРОНЕ.$"
''',
        "Route8_Text_AndreaIntro": '''Route8_Text_AndreaIntro::
\t.string "MEOWTH такой милый: мяу, мяу,\\n"
\t.string "мяу!$"
''',
        "Route8_Text_AndreaDefeat": '''Route8_Text_AndreaDefeat::
\t.string "Мяяяяу!$"
''',
        "Route8_Text_AndreaPostBattle": '''Route8_Text_AndreaPostBattle::
\t.string "По-моему, PIDGEY и RATTATA\\n"
\t.string "тоже очень милые!$"
''',
        "Route8_Text_MeganIntro": '''Route8_Text_MeganIntro::
\t.string "Наверное, мы глупо выглядим,\\n"
\t.string "стоя здесь вот так.$"
''',
        "Route8_Text_MeganDefeat": '''Route8_Text_MeganDefeat::
\t.string "Посмотри, что ты сделал с моими\\n"
\t.string "бедными милыми ПОКЕМОНАМИ!$"
''',
        "Route8_Text_MeganPostBattle": '''Route8_Text_MeganPostBattle::
\t.string "Страж ворот САФФРОНА нас\\n"
\t.string "не пропускает.\\p"
\t.string "Понимаю, это его работа, но\\n"
\t.string "по-моему, он вредный.$"
''',
        "Route8_Text_RichIntro": '''Route8_Text_RichIntro::
\t.string "Я бродяга и фанат игр!$"
''',
        "Route8_Text_RichDefeat": '''Route8_Text_RichDefeat::
\t.string "Упустил отличный шанс!$"
''',
        "Route8_Text_RichPostBattle": '''Route8_Text_RichPostBattle::
\t.string "Игры и ПОКЕМОНЫ - как орешки!\\n"
\t.string "Начнёшь и уже не остановиться!$"
''',
        "Route8_Text_JuliaIntro": '''Route8_Text_JuliaIntro::
\t.string "Какой ПОКЕМОН милый, круглый\\n"
\t.string "и пушистый?$"
''',
        "Route8_Text_JuliaDefeat": '''Route8_Text_JuliaDefeat::
\t.string "Хватит!\\p"
\t.string "Не обижай моего CLEFAIRY!$"
''',
        "Route8_Text_JuliaPostBattle": '''Route8_Text_JuliaPostBattle::
\t.string "Я читала, что CLEFAIRY эволюционирует\\n"
\t.string "от MOON STONE.\\p"
\t.string "Это было в журнале о ПОКЕМОНАХ.\\n"
\t.string "Интересно, правда ли?$"
''',
        "Route8_Text_UndergroundPathSign": '''Route8_Text_UndergroundPathSign::
\t.string "ПОДЗЕМНЫЙ ПЕРЕХОД\\n"
\t.string "СЕЛАДОН - ЛАВАНДЕР$"
''',
        "Route8_Text_EliIntro": '''Route8_Text_EliIntro::
\t.string "ELI: Сила близнецов великолепна.\\n"
\t.string "Ты знал?$"
''',
        "Route8_Text_EliDefeat": '''Route8_Text_EliDefeat::
\t.string "ELI: Но...\\n"
\t.string "Мы же использовали силу близнецов...$"
''',
        "Route8_Text_EliPostBattle": '''Route8_Text_EliPostBattle::
\t.string "ELI: Я ловлю ПОКЕМОНОВ вместе\\n"
\t.string "с ANNE!$"
''',
        "Route8_Text_EliNotEnoughMons": '''Route8_Text_EliNotEnoughMons::
\t.string "ELI: Мы не можем сразиться, если\\n"
\t.string "у тебя нет двух ПОКЕМОНОВ.$"
''',
        "Route8_Text_AnneIntro": '''Route8_Text_AnneIntro::
\t.string "ANNE: Мы поразим тебя силой\\n"
\t.string "близнецов!$"
''',
        "Route8_Text_AnneDefeat": '''Route8_Text_AnneDefeat::
\t.string "ANNE: Наша сила близнецов...$"
''',
        "Route8_Text_AnnePostBattle": '''Route8_Text_AnnePostBattle::
\t.string "ANNE: Я выращиваю ПОКЕМОНОВ\\n"
\t.string "вместе с ELI.$"
''',
        "Route8_Text_AnneNotEnoughMons": '''Route8_Text_AnneNotEnoughMons::
\t.string "ANNE: Привет! Давай сразимся!\\n"
\t.string "Но приведи двух ПОКЕМОНОВ.$"
''',
        "Route8_Text_RicardoIntro": '''Route8_Text_RicardoIntro::
\t.string "Мой байк барахлит, дружище.$"
''',
        "Route8_Text_RicardoDefeat": '''Route8_Text_RicardoDefeat::
\t.string "Эх, дружище.\\n"
\t.string "Мне это совсем не нравится.$"
''',
        "Route8_Text_RicardoPostBattle": '''Route8_Text_RicardoPostBattle::
\t.string "Трава забилась в спицы\\n"
\t.string "моего байка.$"
''',
        "Route8_Text_JarenIntro": '''Route8_Text_JarenIntro::
\t.string "С дороги, иначе я тебя\\n"
\t.string "собью!$"
''',
        "Route8_Text_JarenDefeat": '''Route8_Text_JarenDefeat::
\t.string "Ты серьёзно, малыш?$"
''',
        "Route8_Text_JarenPostBattle": '''Route8_Text_JarenPostBattle::
\t.string "Не думай, что ты особенный\\n"
\t.string "только из-за этой победы.$"
''',
    },
    Path("data/maps/Route14_Frlg/scripts.inc"): {
        "Route14_Text_CarterIntro": '''Route14_Text_CarterIntro::
\t.string "Используй TM, чтобы учить ПОКЕМОНОВ\\n"
\t.string "хорошим приёмам.$"
''',
        "Route14_Text_CarterDefeat": '''Route14_Text_CarterDefeat::
\t.string "Пока ещё недостаточно хорош.$"
''',
        "Route14_Text_CarterPostBattle": '''Route14_Text_CarterPostBattle::
\t.string "У тебя есть HM, верно? ПОКЕМОНАМ\\n"
\t.string "непросто забыть такие приёмы.$"
''',
        "Route14_Text_MitchIntro": '''Route14_Text_MitchIntro::
\t.string "Мои летающие ПОКЕМОНЫ должны\\n"
\t.string "быть готовы к бою.$"
''',
        "Route14_Text_MitchDefeat": '''Route14_Text_MitchDefeat::
\t.string "Ещё не готовы!$"
''',
        "Route14_Text_MitchPostBattle": '''Route14_Text_MitchPostBattle::
\t.string "Моим летающим ПОКЕМОНАМ нужны\\n"
\t.string "приёмы получше.$"
''',
        "Route14_Text_BeckIntro": '''Route14_Text_BeckIntro::
\t.string "В универмаге СЕЛАДОНА продают TM.\\p"
\t.string "TM не так уж редки, а вот HM\\n"
\t.string "есть далеко не у всех.$"
''',
        "Route14_Text_BeckDefeat": '''Route14_Text_BeckDefeat::
\t.string "Эх, вот неудача!$"
''',
        "Route14_Text_BeckPostBattle": '''Route14_Text_BeckPostBattle::
\t.string "Попробуй дать ПОКЕМОНУ приём\\n"
\t.string "его собственного типа.\\p"
\t.string "Говорят, тогда приём становится\\n"
\t.string "сильнее.$"
''',
        "Route14_Text_MarlonIntro": '''Route14_Text_MarlonIntro::
\t.string "Ты научил летающего ПОКЕМОНА\\n"
\t.string "приёму FLY?\\p"
\t.string "Тогда сможешь взмыть с ним\\n"
\t.string "в небо!$"
''',
        "Route14_Text_MarlonDefeat": '''Route14_Text_MarlonDefeat::
\t.string "Меня сбили!$"
''',
        "Route14_Text_MarlonPostBattle": '''Route14_Text_MarlonPostBattle::
\t.string "Летающие ПОКЕМОНЫ - моя любовь.\\n"
\t.string "Других я растить не хочу.$"
''',
        "Route14_Text_DonaldIntro": '''Route14_Text_DonaldIntro::
\t.string "Ты слышал легенду о крылатых\\n"
\t.string "миражах?$"
''',
        "Route14_Text_DonaldDefeat": '''Route14_Text_DonaldDefeat::
\t.string "Почему?\\n"
\t.string "Почему я проиграл?$"
''',
        "Route14_Text_DonaldPostBattle": '''Route14_Text_DonaldPostBattle::
\t.string "Крылатые миражи - это легендарные\\n"
\t.string "птицы-ПОКЕМОНЫ.\\p"
\t.string "Их трое: ARTICUNO, ZAPDOS\\n"
\t.string "и MOLTRES.$"
''',
        "Route14_Text_BennyIntro": '''Route14_Text_BennyIntro::
\t.string "Не особо хочется, но ладно.\\n"
\t.string "Начнём!$"
''',
        "Route14_Text_BennyDefeat": '''Route14_Text_BennyDefeat::
\t.string "Я так и знал!$"
''',
        "Route14_Text_BennyPostBattle": '''Route14_Text_BennyPostBattle::
\t.string "Победа, поражение... всё это мелочи\\n"
\t.string "под таким огромным небом.$"
''',
        "Route14_Text_LukasIntro": '''Route14_Text_LukasIntro::
\t.string "Давай, давай!\\n"
\t.string "Вперёд, вперёд, вперёд!$"
''',
        "Route14_Text_LukasDefeat": '''Route14_Text_LukasDefeat::
\t.string "Ар-р!\\n"
\t.string "Проиграл! Проваливай!$"
''',
        "Route14_Text_LukasPostBattle": '''Route14_Text_LukasPostBattle::
\t.string "Что, что, что?\\n"
\t.string "Чего тебе ещё?$"
''',
        "Route14_Text_IsaacIntro": '''Route14_Text_IsaacIntro::
\t.string "Мне надо убить время.\\n"
\t.string "Хватит болтать, сражайся.$"
''',
        "Route14_Text_IsaacDefeat": '''Route14_Text_IsaacDefeat::
\t.string "Что?\\n"
\t.string "Ты!?$"
''',
        "Route14_Text_IsaacPostBattle": '''Route14_Text_IsaacPostBattle::
\t.string "Растить ПОКЕМОНОВ - та ещё морока.$"
''',
        "Route14_Text_GeraldIntro": '''Route14_Text_GeraldIntro::
\t.string "Мы ездим сюда из-за этих\\n"
\t.string "просторных мест.$"
''',
        "Route14_Text_GeraldDefeat": '''Route14_Text_GeraldDefeat::
\t.string "Разгром!$"
''',
        "Route14_Text_GeraldPostBattle": '''Route14_Text_GeraldPostBattle::
\t.string "Круто, что ты сделал своих\\n"
\t.string "ПОКЕМОНОВ такими сильными.\\p"
\t.string "Сила решает!\\n"
\t.string "И ты это знаешь!$"
''',
        "Route14_Text_MalikIntro": '''Route14_Text_MalikIntro::
\t.string "Бой ПОКЕМОНОВ?\\n"
\t.string "Круто! Погнали!$"
''',
        "Route14_Text_MalikDefeat": '''Route14_Text_MalikDefeat::
\t.string "Меня снесло!$"
''',
        "Route14_Text_MalikPostBattle": '''Route14_Text_MalikPostBattle::
\t.string "А один на один между нами\\n"
\t.string "кто бы победил?$"
''',
        "Route14_Text_RouteSign": '''Route14_Text_RouteSign::
\t.string "МАРШРУТ 14\\n"
\t.string "На запад - ФУКСИЯ$"
''',
        "Route14_Text_KiriIntro": '''Route14_Text_KiriIntro::
\t.string "KIRI: JAN, давай постараемся\\n"
\t.string "изо всех сил вместе.$"
''',
        "Route14_Text_KiriDefeat": '''Route14_Text_KiriDefeat::
\t.string "KIRI: Хнык...\\n"
\t.string "Мы проиграли, да?$"
''',
        "Route14_Text_KiriPostBattle": '''Route14_Text_KiriPostBattle::
\t.string "KIRI: Мы проиграли из-за меня?$"
''',
        "Route14_Text_KiriNotEnoughMons": '''Route14_Text_KiriNotEnoughMons::
\t.string "KIRI: Сразимся, если у тебя\\n"
\t.string "есть два ПОКЕМОНА.$"
''',
        "Route14_Text_JanIntro": '''Route14_Text_JanIntro::
\t.string "JAN: KIRI, начинаем!\\n"
\t.string "Надо очень постараться!$"
''',
        "Route14_Text_JanDefeat": '''Route14_Text_JanDefeat::
\t.string "JAN: Э-э-эй!\\n"
\t.string "Так нечестно!$"
''',
        "Route14_Text_JanPostBattle": '''Route14_Text_JanPostBattle::
\t.string "JAN: KIRI, не плачь!\\n"
\t.string "В следующий раз постараемся сильнее.$"
''',
        "Route14_Text_JanNotEnoughMons": '''Route14_Text_JanNotEnoughMons::
\t.string "JAN: Хочешь сразиться?\\n"
\t.string "У тебя недостаточно ПОКЕМОНОВ.$"
''',
    },
}


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_routes8_14_v3_87.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    total = 0
    report = []

    for rel, replacements in FILES.items():
        path = root / rel
        text = path.read_text(encoding="utf-8")
        applied = []
        for label, replacement in replacements.items():
            start, end, block = block_bounds(text, label)
            if re.search(r"[А-Яа-яЁё]", block):
                raise SystemExit(f"{MARKER}: {label}: already localized or unexpected Cyrillic")
            if ".string" not in block:
                raise SystemExit(f"{MARKER}: {label}: runtime text block has no string")
            text = text[:start] + replacement + "\n" + text[end:]
            applied.append(label)
        path.write_text(text, encoding="utf-8")
        total += len(applied)
        report.append({"file": str(rel), "translatedBlocks": applied, "translatedBlockCount": len(applied)})

    if total != 81:
        raise SystemExit(f"{MARKER}: expected 81 translated blocks, got {total}")

    out = root / "build" / "qarro_ru_routes8_14_v3_87_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "files": report,
        "translatedBlockCount": total,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} Route 8 + Route 14 runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
