#!/usr/bin/env python3
"""Qarro v3.89 bulk Russian localization: Route 15 + Route 19.

Translates all 39 Route 15 and all 39 Route 19 FireRed runtime text blocks from
pinned Expansion 1.17.0. Pokemon species, Move and Ability proper names remain
English by project canon. Ash Bond / Ash Cap and gameplay logic are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTES15_19_V3_89"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    Path("data/maps/Route15_Frlg/scripts.inc"): {
        "Route15_Text_KindraIntro": '''Route15_Text_KindraIntro::
\t.string "Я только что выменяла пару ПОКЕМОНОВ.\\n"
\t.string "Можно проверить их в бою с тобой?$"
''',
        "Route15_Text_KindraDefeat": '''Route15_Text_KindraDefeat::
\t.string "Недостаточно хорошо!$"
''',
        "Route15_Text_KindraPostBattle": '''Route15_Text_KindraPostBattle::
\t.string "Нельзя сменить кличку ПОКЕМОНУ,\\n"
\t.string "полученному в обмене.\\p"
\t.string "Сменить её может только его\\n"
\t.string "первоначальный ТРЕНЕР.$"
''',
        "Route15_Text_BeckyIntro": '''Route15_Text_BeckyIntro::
\t.string "Ты выглядишь добрым, так что, думаю,\\n"
\t.string "я смогу тебя победить.\\p"
\t.string "Попробую!$"
''',
        "Route15_Text_BeckyDefeat": '''Route15_Text_BeckyDefeat::
\t.string "Нет, не так!$"
''',
        "Route15_Text_BeckyPostBattle": '''Route15_Text_BeckyPostBattle::
\t.string "Я боюсь БАЙКЕРОВ. Они выглядят\\n"
\t.string "такими грубыми и злыми!$"
''',
        "Route15_Text_EdwinIntro": '''Route15_Text_EdwinIntro::
\t.string "Стоит мне свистнуть, и я могу призвать\\n"
\t.string "птичьих ПОКЕМОНОВ.$"
''',
        "Route15_Text_EdwinDefeat": '''Route15_Text_EdwinDefeat::
\t.string "Ай!\\n"
\t.string "Какая трагедия!$"
''',
        "Route15_Text_EdwinPostBattle": '''Route15_Text_EdwinPostBattle::
\t.string "Может, бои просто не для меня.\\n"
\t.string "Наверное, я не того типа.$"
''',
        "Route15_Text_ChesterIntro": '''Route15_Text_ChesterIntro::
\t.string "Хм? Мои птицы дрожат!\\n"
\t.string "Ты ведь силён, да?$"
''',
        "Route15_Text_ChesterDefeat": '''Route15_Text_ChesterDefeat::
\t.string "Как я и думал!$"
''',
        "Route15_Text_ChesterPostBattle": '''Route15_Text_ChesterPostBattle::
\t.string "Это очевидно, ты должен это знать,\\n"
\t.string "но всё же...\\p"
\t.string "Приёмы вроде EARTHQUAKE и FISSURE\\n"
\t.string "не действуют на птичьих ПОКЕМОНОВ.$"
''',
        "Route15_Text_GraceIntro": '''Route15_Text_GraceIntro::
\t.string "Ой, какой ты милашка!\\n"
\t.string "Прямо как очаровательный ПОКЕМОН!$"
''',
        "Route15_Text_GraceDefeat": '''Route15_Text_GraceDefeat::
\t.string "А выглядел таким милым!$"
''',
        "Route15_Text_GracePostBattle": '''Route15_Text_GracePostBattle::
\t.string "Я тебя прощаю.\\n"
\t.string "Я выдержу.\\l"
\t.string "Я уже взрослая девочка.$"
''',
        "Route15_Text_OliviaIntro": '''Route15_Text_OliviaIntro::
\t.string "Я ращу ПОКЕМОНОВ для защиты,\\n"
\t.string "потому что живу одна.$"
''',
        "Route15_Text_OliviaDefeat": '''Route15_Text_OliviaDefeat::
\t.string "Для меня ПОКЕМОНЫ - не вопрос\\n"
\t.string "победы или поражения.$"
''',
        "Route15_Text_OliviaPostBattle": '''Route15_Text_OliviaPostBattle::
\t.string "Люблю, когда мои ПОКЕМОНЫ встречают\\n"
\t.string "меня дома.\\p"
\t.string "С ними так спокойно.$"
''',
        "Route15_Text_ErnestIntro": '''Route15_Text_ErnestIntro::
\t.string "Эй, мелкий! Давай!\\n"
\t.string "Я только что забрал их у неудачника!$"
''',
        "Route15_Text_ErnestDefeat": '''Route15_Text_ErnestDefeat::
\t.string "Почему нет?$"
''',
        "Route15_Text_ErnestPostBattle": '''Route15_Text_ErnestPostBattle::
\t.string "Жизнь слишком коротка.\\n"
\t.string "Круто жить вне закона.\\l"
\t.string "КОМАНДА РОКЕТ РУЛИТ!$"
''',
        "Route15_Text_AlexIntro": '''Route15_Text_AlexIntro::
\t.string "Когда проиграешь, выкладывай\\n"
\t.string "все деньги, мелкий!$"
''',
        "Route15_Text_AlexDefeat": '''Route15_Text_AlexDefeat::
\t.string "Не может быть!$"
''',
        "Route15_Text_AlexPostBattle": '''Route15_Text_AlexPostBattle::
\t.string "Я просто пошутил насчёт денег.\\n"
\t.string "Не воспринимай всё так серьёзно.$"
''',
        "Route15_Text_CeliaIntro": '''Route15_Text_CeliaIntro::
\t.string "Что сейчас модно?\\n"
\t.string "Обмен ПОКЕМОНАМИ!$"
''',
        "Route15_Text_CeliaDefeat": '''Route15_Text_CeliaDefeat::
\t.string "Я сказала: обмен!$"
''',
        "Route15_Text_CeliaPostBattle": '''Route15_Text_CeliaPostBattle::
\t.string "Я постоянно меняюсь ПОКЕМОНАМИ\\n"
\t.string "с друзьями.$"
''',
        "Route15_Text_YazminIntro": '''Route15_Text_YazminIntro::
\t.string "Хочешь поиграть с моими ПОКЕМОНАМИ?$"
''',
        "Route15_Text_YazminDefeat": '''Route15_Text_YazminDefeat::
\t.string "Я слишком торопилась!$"
''',
        "Route15_Text_YazminPostBattle": '''Route15_Text_YazminPostBattle::
\t.string "Пойду тренироваться на тех, кто слабее.$"
''',
        "Route15_Text_RouteSign": '''Route15_Text_RouteSign::
\t.string "МАРШРУТ 15\\n"
\t.string "На запад - ФУКСИЯ$"
''',
        "Route15_Text_MyaIntro": '''Route15_Text_MyaIntro::
\t.string "MYA: Ты как раз подходишь.\\n"
\t.string "Поможешь тренировать братишку?$"
''',
        "Route15_Text_MyaDefeat": '''Route15_Text_MyaDefeat::
\t.string "MYA: RON, сосредоточься!\\n"
\t.string "Следи за тем, что делаешь!$"
''',
        "Route15_Text_MyaPostBattle": '''Route15_Text_MyaPostBattle::
\t.string "MYA: Ладно, повысим нагрузку.\\n"
\t.string "Добавлю кое-что в нашу тренировку!$"
''',
        "Route15_Text_MyaNotEnoughMons": '''Route15_Text_MyaNotEnoughMons::
\t.string "MYA: Хочешь бросить нам вызов?\\n"
\t.string "Тогда нужны два ПОКЕМОНА.$"
''',
        "Route15_Text_RonIntro": '''Route15_Text_RonIntro::
\t.string "RON: Моя сестра страшная, когда\\n"
\t.string "мы проигрываем.$"
''',
        "Route15_Text_RonDefeat": '''Route15_Text_RonDefeat::
\t.string "RON: Ой, нет, нет...\\n"
\t.string "Сестрёнка, прости!$"
''',
        "Route15_Text_RonPostBattle": '''Route15_Text_RonPostBattle::
\t.string "RON: Эх...\\n"
\t.string "Вот бы у меня была добрая сестра...$"
''',
        "Route15_Text_RonNotEnoughMons": '''Route15_Text_RonNotEnoughMons::
\t.string "RON: Хотел сразиться со мной\\n"
\t.string "и моей сестрой?\\p"
\t.string "Тогда нужны два ПОКЕМОНА.$"
''',
    },
    Path("data/maps/Route19_Frlg/scripts.inc"): {
        "Route19_Text_RichardIntro": '''Route19_Text_RichardIntro::
\t.string "Перед заплывом мне надо размяться\\n"
\t.string "и хорошенько разогреться.$"
''',
        "Route19_Text_RichardDefeat": '''Route19_Text_RichardDefeat::
\t.string "Вот теперь размялся!$"
''',
        "Route19_Text_RichardPostBattle": '''Route19_Text_RichardPostBattle::
\t.string "Спасибо, малыш!\\n"
\t.string "Теперь я готов плыть.$"
''',
        "Route19_Text_ReeceIntro": '''Route19_Text_ReeceIntro::
\t.string "Стой! Помедленнее!\\n"
\t.string "Так и до сердечного приступа недалеко!$"
''',
        "Route19_Text_ReeceDefeat": '''Route19_Text_ReeceDefeat::
\t.string "Ух!\\n"
\t.string "Холодновато!$"
''',
        "Route19_Text_ReecePostBattle": '''Route19_Text_ReecePostBattle::
\t.string "Берегись TENTACOOL.\\n"
\t.string "Они очень больно жалят.$"
''',
        "Route19_Text_MatthewIntro": '''Route19_Text_MatthewIntro::
\t.string "Обожаю плавать!\\n"
\t.string "А ты?$"
''',
        "Route19_Text_MatthewDefeat": '''Route19_Text_MatthewDefeat::
\t.string "Плюх животом!$"
''',
        "Route19_Text_MatthewPostBattle": '''Route19_Text_MatthewPostBattle::
\t.string "В плавании я обгоню даже\\n"
\t.string "морских ПОКЕМОНОВ.$"
''',
        "Route19_Text_DouglasIntro": '''Route19_Text_DouglasIntro::
\t.string "Что там, за горизонтом?$"
''',
        "Route19_Text_DouglasDefeat": '''Route19_Text_DouglasDefeat::
\t.string "Бульк!$"
''',
        "Route19_Text_DouglasPostBattle": '''Route19_Text_DouglasPostBattle::
\t.string "Вон там вдали я вижу\\n"
\t.string "пару островов!$"
''',
        "Route19_Text_DavidIntro": '''Route19_Text_DavidIntro::
\t.string "Пытался нырять за ПОКЕМОНАМИ,\\n"
\t.string "но ничего не вышло.$"
''',
        "Route19_Text_DavidDefeat": '''Route19_Text_DavidDefeat::
\t.string "Помогите!$"
''',
        "Route19_Text_DavidPostBattle": '''Route19_Text_DavidPostBattle::
\t.string "Похоже, морских ПОКЕМОНОВ\\n"
\t.string "надо ловить удочкой.$"
''',
        "Route19_Text_TonyIntro": '''Route19_Text_TonyIntro::
\t.string "Я смотрю на море, чтобы забыть\\n"
\t.string "всё плохое, что со мной случилось.$"
''',
        "Route19_Text_TonyDefeat": '''Route19_Text_TonyDefeat::
\t.string "Ух!\\n"
\t.string "Какая травма!$"
''',
        "Route19_Text_TonyPostBattle": '''Route19_Text_TonyPostBattle::
\t.string "Смотрю на море, чтобы забыть\\n"
\t.string "то плохое, что только что случилось!$"
''',
        "Route19_Text_AnyaIntro": '''Route19_Text_AnyaIntro::
\t.string "Ой, мне нравится твой транспорт!\\n"
\t.string "Отдашь его, если я выиграю?$"
''',
        "Route19_Text_AnyaDefeat": '''Route19_Text_AnyaDefeat::
\t.string "Ой! Я проиграла!$"
''',
        "Route19_Text_AnyaPostBattle": '''Route19_Text_AnyaPostBattle::
\t.string "До ОСТРОВОВ СИФОМ ещё очень далеко...\\p"
\t.string "Хочу обратно в ФУКСИЮ...$"
''',
        "Route19_Text_AliceIntro": '''Route19_Text_AliceIntro::
\t.string "Плавать здорово!\\n"
\t.string "А вот обгорать на солнце - нет!$"
''',
        "Route19_Text_AliceDefeat": '''Route19_Text_AliceDefeat::
\t.string "Вот это шок!$"
''',
        "Route19_Text_AlicePostBattle": '''Route19_Text_AlicePostBattle::
\t.string "Мой парень хотел доплыть\\n"
\t.string "до ОСТРОВОВ СИФОМ.$"
''',
        "Route19_Text_AxleIntro": '''Route19_Text_AxleIntro::
\t.string "Эй, на борту!\\n"
\t.string "Эти воды опасны!$"
''',
        "Route19_Text_AxleDefeat": '''Route19_Text_AxleDefeat::
\t.string "Ух!\\n"
\t.string "Опасно!$"
''',
        "Route19_Text_AxlePostBattle": '''Route19_Text_AxlePostBattle::
\t.string "М-мои ноги! Судорога!\\n"
\t.string "Бульк, бульк...$"
''',
        "Route19_Text_ConnieIntro": '''Route19_Text_ConnieIntro::
\t.string "Я приплыла сюда с друзьями...\\n"
\t.string "Я устала...$"
''',
        "Route19_Text_ConnieDefeat": '''Route19_Text_ConnieDefeat::
\t.string "Я совсем выдохлась...$"
''',
        "Route19_Text_ConniePostBattle": '''Route19_Text_ConniePostBattle::
\t.string "Если бы я плыла верхом на ПОКЕМОНЕ,\\n"
\t.string "то выбрала бы LAPRAS.\\p"
\t.string "LAPRAS такой большой, думаю,\\n"
\t.string "на нём я бы даже не промокла.$"
''',
        "Route19_Text_RouteSign": '''Route19_Text_RouteSign::
\t.string "МОРСКОЙ МАРШРУТ 19\\n"
\t.string "ФУКСИЯ - ОСТРОВА СИФОМ$"
''',
        "Route19_Text_LiaIntro": '''Route19_Text_LiaIntro::
\t.string "LIA: Я присматриваю за братом.\\n"
\t.string "Он только стал ТРЕНЕРОМ.$"
''',
        "Route19_Text_LiaDefeat": '''Route19_Text_LiaDefeat::
\t.string "LIA: Так с моим младшим братом\\n"
\t.string "обращаться нельзя!$"
''',
        "Route19_Text_LiaPostBattle": '''Route19_Text_LiaPostBattle::
\t.string "LIA: У тебя есть младший брат?\\p"
\t.string "Надеюсь, ты учишь его всяким\\n"
\t.string "полезным вещам.$"
''',
        "Route19_Text_LiaNotEnoughMons": '''Route19_Text_LiaNotEnoughMons::
\t.string "LIA: Я хочу сражаться вместе\\n"
\t.string "с младшим братом.\\p"
\t.string "Разве у тебя нет двух ПОКЕМОНОВ?$"
''',
        "Route19_Text_LucIntro": '''Route19_Text_LucIntro::
\t.string "LUC: Старшая сестра научила меня\\n"
\t.string "плавать и тренировать ПОКЕМОНОВ.$"
''',
        "Route19_Text_LucDefeat": '''Route19_Text_LucDefeat::
\t.string "LUC: Ого!\\n"
\t.string "Кто-то сильнее моей сестры!$"
''',
        "Route19_Text_LucPostBattle": '''Route19_Text_LucPostBattle::
\t.string "LUC: Моя сестра сильная и добрая.\\n"
\t.string "Она просто супер!$"
''',
        "Route19_Text_LucNotEnoughMons": '''Route19_Text_LucNotEnoughMons::
\t.string "LUC: Не хочу драться без\\n"
\t.string "моей старшей сестры.\\p"
\t.string "Разве у тебя нет двух ПОКЕМОНОВ?$"
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
        raise SystemExit("usage: localize_routes15_19_v3_89.py <upstream-root>")
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

    if total != 78:
        raise SystemExit(f"{MARKER}: expected 78 translated blocks, got {total}")

    out = root / "build" / "qarro_ru_routes15_19_v3_89_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "files": report,
        "translatedBlockCount": total,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} Route 15 + Route 19 runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
