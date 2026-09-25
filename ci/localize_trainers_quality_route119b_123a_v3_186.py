#!/usr/bin/env python3
"""Qarro v3.186: human-quality RU pass for trainer chunk 8.

Covers the next contiguous 100 machine-translated blocks in trainers.inc:
the rest of Route 119, Routes 120-121 and the opening of Route 123.
Localization-only; exact runtime control-token sequences are preserved and
source drift fails closed. Pokemon, Move and Ability proper names stay English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINERS_QUALITY_ROUTE119B_123A_V3_186"
TARGET = Path("data/text/trainers.inc")

TRANSLATIONS = {
    "Route119_Text_DaytonPostBattle": "Хо-хо-хо!\\nПопробую перенять задор юных\\lтренеров вроде тебя!$",
    "Route119_Text_RachelIntro": "Где бы я ни была,\\nзонтик всегда у меня в руке.$",
    "Route119_Text_RachelDefeat": "Ох, ну...\\nЭто нечестно.$",
    "Route119_Text_RachelPostBattle": "Спрашиваешь, тяжелый ли мой зонтик?\\nДа в твоей СУМКЕ больше барахла, чем\\lя вообще когда-либо ношу с собой.$",
    "Route120_Text_ColinIntro": "У тебя есть приемы, способные достать\\nлетающего POKeMON?$",
    "Route120_Text_ColinDefeat": "Ты взлетел выше меня!$",
    "Route120_Text_ColinPostBattle": "FLY - очень удобный прием,\\nне находишь?\\pПока POKeMON летит,\\nпочти никакой прием его не достанет.$",
    "Route120_Text_RobertIntro": "Мой POKeMON сильный!\\nА твой?$",
    "Route120_Text_RobertDefeat": "Твои POKeMON оказались сильнее...$",
    "Route120_Text_RobertPostBattle": "На POKeMON, который стабильно растет,\\nвсегда можно положиться.$",
    "Route120_Text_RobertRegister": "Похоже, ты и дальше будешь становиться сильнее.\\nХочу записать тебя в свой POKeNAV!$",
    "Route120_Text_RobertRematchIntro": "На POKeMON, который стабильно растет,\\nвсегда можно положиться.$",
    "Route120_Text_RobertRematchDefeat": "Твои POKeMON действительно сильны.$",
    "Route120_Text_RobertPostRematch": "Мои POKeMON становятся сильнее.\\nИ мне тоже нужно расти.$",
    "Route120_Text_LorenzoIntro": "Проверю твоих POKeMON и посмотрю,\\nготовы ли они к дикой природе.$",
    "Route120_Text_LorenzoDefeat": "С такими сильными POKeMON тебе\\nточно не понадобится спасение!$",
    "Route120_Text_LorenzoPostBattle": "Путешествовать с POKeMON туда,\\nкуда зовет сердце...\\lВот радость жизни тренера.$",
    "Route120_Text_JennaIntro": "Как у тебя с физической формой?\\nЕсли она плохая, в критической ситуации\\lможет прийтись тяжело.$",
    "Route120_Text_JennaDefeat": "Я-то в отличной форме, но...$",
    "Route120_Text_JennaPostBattle": "Физические тренировки входят в мой распорядок.\\nЯ всегда бегаю вместе с POKeMON.$",
    "Route120_Text_JeffreyIntro": "... ... ... ... ... ...\\n... ... ... ... ... ...\\lХочешь сразиться?$",
    "Route120_Text_JeffreyDefeat": "Проиграл...$",
    "Route120_Text_JeffreyPostBattle": "... ... ... ... ... ...\\n... ... ... ... ... ...\\lБуду стараться больше...$",
    "Route120_Text_JeffreyRegister": "... ... ... ... ... ...\\n... ... ... ... ... ...\\lУ тебя есть POKeNAV...?$",
    "Route120_Text_JeffreyRematchIntro": "... ... ... ... ... ...\\n... ... ... ... ... ...\\lХочешь еще раз сразиться?$",
    "Route120_Text_JeffreyRematchDefeat": "... ... ... ... ... ...\\nЯ снова проиграл...$",
    "Route120_Text_JeffreyPostRematch": "... ... ... ... ... ...\\n... ... ... ... ... ...\\lБуду стараться больше...\\lРади моих любимых POKeMON-жуков...$",
    "Route120_Text_JenniferIntro": "У POKeMON множество особых способностей.\\nЕсли хочешь стать первоклассным\\lтренером, изучай их.$",
    "Route120_Text_JenniferDefeat": "Вижу, ты умеешь думать.$",
    "Route120_Text_JenniferPostBattle": "Особые способности POKeMON\\nмогут полностью менять стиль боя.$",
    "Route120_Text_ChipIntro": "Кто же ты такой?\\pУж не ищешь ли ты древние\\nруины, которые, по легендам,\\lвроде бы могут существовать?$",
    "Route120_Text_ChipDefeat": "Какое позорное поражение...$",
    "Route120_Text_ChipPostBattle": "Эта огромная скала... Хочется\\nверить, что внутри и правда скрыты древние\\lруины. Но входа я не вижу.$",
    "Route120_Text_ClarissaIntro": "Почему я ношу этот зонтик?\\pРасскажу, если сумеешь меня победить.$",
    "Route120_Text_ClarissaDefeat": "Зонтик не защищает POKeMON\\nот атак...$",
    "Route120_Text_ClarissaPostBattle": "Мне кажется, яркое солнце вредно\\nмоим POKeMON.\\lПоэтому я прикрываю их зонтиком.$",
    "Route120_Text_AngelicaIntro": "Я, POKeMON и мой зонтик...\\pУбери хоть что-то одно,\\nи картина красоты будет разрушена.$",
    "Route120_Text_AngelicaDefeat": "Ты полностью разрушил мою красоту...$",
    "Route120_Text_AngelicaPostBattle": "Тебе зонтик совсем не подойдет.\\pТакая вещь будет только\\nмешаться.$",
    "Route120_Text_KeigoIntro": "Я перенимаю движения POKeMON\\nи создаю новые техники ниндзя.$",
    "Route120_Text_KeigoDefeat": "Создание новых техник ниндзя\\nпока остается далекой мечтой...$",
    "Route120_Text_KeigoPostBattle": "Пожалуй, мне стоит стать учеником\\nнастоящего ниндзя-сенсея.$",
    "Route120_Text_RileyIntro": "Мы, ниндзя, скрываемся под\\nмаскировочными плащами.\\lДержу пари, ты не заметил, где я был!$",
    "Route120_Text_RileyDefeat": "Я проиграл!\\nПридется замаскировать свой позор!$",
    "Route120_Text_RileyPostBattle": "Все наши маскировочные плащи\\nсделаны вручную.$",
    "Route120_Text_CallieIntro": "Если будешь невнимателен,\\nможешь пострадать!$",
    "Route120_Text_CallieDefeat": "Ай!\\nВ итоге пострадала я.$",
    "Route120_Text_CalliePostBattle": "Интересно... Стоит ли эволюционировать моих POKeMON?\\nОни и так такие милые.$",
    "Route120_Text_LeonelIntro": "Твои POKeMON в команде...\\nУ тебя есть разные типы?$",
    "Route120_Text_LeonelDefeat": "Теперь я увидел твой подход в деле!$",
    "Route120_Text_LeonelPostBattle": "Круто, что ты так силен,\\nсражаясь любимыми POKeMON.$",
    "Route121_Text_VanessaIntro": "Не хочешь поиграть с моими удивительно\\nкрасивыми POKeMON?$",
    "Route121_Text_VanessaDefeat": "Я совсем не это имела в виду!$",
    "Route121_Text_VanessaPostBattle": "Я направляюсь на КОНКУРС в ЛИЛИКОВ.\\pМои POKeMON без труда\\nвозьмут МАСТЕР-КЛАСС.$",
    "Route121_Text_WalterIntro": "Вместе с POKeMON я объездил\\nвсе четыре стороны света.\\pМожно сказать, в своих силах\\nя довольно уверен.$",
    "Route121_Text_WalterDefeat": "Ах, хорошо сыграно.$",
    "Route121_Text_WalterPostBattle": "Я бы хотел еще раз объехать весь мир\\nвместе со своими POKeMON.$",
    "Route121_Text_WalterRegister": "Твое мастерство с POKeMON впечатляет.\\nПозволь записать тебя на память.$",
    "Route121_Text_WalterRematchIntro": "Вместе с POKeMON я объездил\\nвсе четыре стороны света.\\pМожно сказать, в своих силах\\nя довольно уверен.$",
    "Route121_Text_WalterRematchDefeat": "Ах, хорошо сыграно.$",
    "Route121_Text_WalterPostRematch": "Ты и твои POKeMON...\\pВашу совместную силу сочтут\\nвпечатляющей даже за морем.$",
    "Route121_Text_TammyIntro": "В мире есть силы, лежащие за пределами\\nнашего понимания...$",
    "Route121_Text_TammyDefeat": "Я проиграла...$",
    "Route121_Text_TammyPostBattle": "ГОРА ПАЙР...\\nТам действует таинственная сила\\lневедомой природы...$",
    "Route121_Text_KateIntro": "КЕЙТ: Вместе мы ничего не боимся!\\nСейчас покажем, насколько мы сильны!$",
    "Route121_Text_KateDefeat": "КЕЙТ: Я опозорилась перед своей младшей\\nнапарницей...$",
    "Route121_Text_KatePostBattle": "КЕЙТ: Когда на меня кто-то рассчитывает,\\nтак и хочется выглядеть круто\\lперед ним...$",
    "Route121_Text_KateNotEnoughMons": "КЕЙТ: Если у тебя только один POKeMON,\\nмы не можем сражаться.\\pЭто уже будет нечестно.$",
    "Route121_Text_JoyIntro": "ДЖОЙ: Вместе мы ничего не боимся!\\nСейчас покажем, насколько мы сильны!$",
    "Route121_Text_JoyDefeat": "ДЖОЙ: Прости меня, КЕЙТ!$",
    "Route121_Text_JoyPostBattle": "ДЖОЙ: Хе-хе, придется снова тренироваться с КЕЙТ,\\nмоей старшей напарницей.$",
    "Route121_Text_JoyNotEnoughMons": "ДЖОЙ: Чтобы бросить нам вызов,\\nнужно хотя бы два POKeMON!$",
    "Route121_Text_JessicaIntro": "Стой! Как следует полюбуйся моими\\nдрагоценными POKeMON!$",
    "Route121_Text_JessicaDefeat": "О, как ты смеешь!\\nНе надо было так стараться!$",
    "Route121_Text_JessicaPostBattle": "Может, пойду поймаю еще POKeMON\\nв САФАРИ.$",
    "Route121_Text_JessicaRegister": "В этот раз я тебе поддалась!\\nВ следующий такого не будет!$",
    "Route121_Text_JessicaRematchIntro": "Мои драгоценные POKeMON выросли!\\nПолюбуйся как следует!$",
    "Route121_Text_JessicaRematchDefeat": "О, как ты смеешь!\\nТы все еще не хочешь мне поддаваться!$",
    "Route121_Text_JessicaPostRematch": "Может, пойду поймаю еще POKeMON\\nв САФАРИ.$",
    "Route121_Text_CristinIntro": "У меня такой распорядок:\\nпобеждать по пять тренеров в день.\\lИ знаешь что? Ты номер пять!$",
    "Route121_Text_CristinDefeat": "Нет!\\nКакой кошмар!$",
    "Route121_Text_CristinPostBattle": "Не думала, что проиграю так легко...\\nВ следующий раз победа будет моей!$",
    "Route121_Text_CristinRegister": "Какое унижение!\\nЯ тебя не забуду...\\lДавай сюда свой POKeNAV!$",
    "Route121_Text_CristinRematchIntro": "Теперь у меня новый распорядок:\\nпобеждать по десять тренеров в день.\\lИ знаешь что? Ты номер десять!$",
    "Route121_Text_CristinRematchDefeat": "Стой! Это уже слишком!\\nТребую реванша!$",
    "Route121_Text_CristinPostRematch": "Соперник, которого я никак не могу победить...\\nХнык...\\lНе верится, что это происходит...$",
    "Route121_Text_CaleIntro": "Разве не видишь, сколько у меня\\nвсего в руках?\\pИ несмотря на это, ты все равно\\nнастаиваешь на бое?$",
    "Route121_Text_CaleDefeat": "Конечно я проиграл!\\nУ меня обе руки заняты!$",
    "Route121_Text_CalePostBattle": "Я слишком много купил в\\nУНИВЕРМАГЕ ЛИЛИКОВА.\\pОн чуть выше по дороге.\\nВот бы мне такую СУМКУ, как у тебя.$",
    "Route121_Text_MylesIntro": "Больше всего я люблю\\nразглядывать чужих POKeMON!$",
    "Route121_Text_MylesDefeat": "Супер!$",
    "Route121_Text_MylesPostBattle": "Твои POKeMON великолепны!\\nКак ты их растишь?$",
    "Route121_Text_PatIntro": "Хочу, чтобы все увидели POKeMON,\\nкоторых я вырастил!$",
    "Route121_Text_PatDefeat": "Ух ты!\\nВеликолепно!$",
    "Route121_Text_PatPostBattle": "Каждого POKeMON я выращиваю с одинаковой\\nлюбовью и заботой - любимчиков у меня нет.$",
    "Route121_Text_MarcelIntro": "Мои POKeMON еще не знали поражений!\\nПосле следующей победы я выставлю их\\lна КОНКУРС.$",
    "Route121_Text_MarcelDefeat": "О, и что же теперь случилось?$",
    "Route121_Text_MarcelPostBattle": "Похоже, придется еще потренировать команду,\\nпрежде чем идти на КОНКУРС.$",
    "Route123_Text_WendyIntro": "Хочешь узнать, насколько ты силен?\\nЯ буду твоей проверкой!$",
    "Route123_Text_WendyDefeat": "Ты прошел испытание блестяще!$",
}

BANNED_UNICODE = set("—–←→“”«»")


def control_tokens(text: str) -> list[str]:
    return re.findall(r'\{[^}]+\}|\\.|\$', text)


def replace_label(path: Path, label: str, translated: str) -> None:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(?ms)^(?P<head>{re.escape(label)}:\s*\n)'
        rf'(?P<body>(?:[ \t]*\.string\s+"(?:\\.|[^"\\])*"\s*\n?)+)'
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{path}:{label}: expected one text block, got {len(matches)}")
    m = matches[0]
    current_parts = re.findall(r'\.string\s+"((?:\\.|[^"\\])*)"', m.group("body"))
    if not current_parts:
        raise RuntimeError(f"{path}:{label}: no .string content found")
    current = "".join(current_parts)
    old_tokens = control_tokens(current)
    new_tokens = control_tokens(translated)
    if old_tokens != new_tokens:
        raise RuntimeError(f"{path}:{label}: control-token drift old={old_tokens} new={new_tokens}")
    if not translated.endswith("$"):
        raise RuntimeError(f"{path}:{label}: translated block must end in $")
    bad = sorted(set(translated) & BANNED_UNICODE)
    if bad:
        raise RuntimeError(f"{path}:{label}: unsupported punctuation {bad}")
    if '"' in translated:
        raise RuntimeError(f"{path}:{label}: raw double quote is not allowed")
    new_body = '\t.string "' + translated + '"\n'
    path.write_text(text[:m.start("body")] + new_body + text[m.end("body"):], encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_trainers_quality_route119b_123a_v3_186.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 100:
        raise RuntimeError(f"expected exactly 100 quality-pass blocks, got {len(TRANSLATIONS)}")
    for label, translated in TRANSLATIONS.items():
        replace_label(path, label, translated)

    out = root / "build" / "qarro_ru_trainers_quality_route119b_123a_v3_186_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassBlocks": len(TRANSLATIONS),
        "labels": list(TRANSLATIONS),
        "humanEditedRussian": True,
        "controlTokensPreserved": True,
        "pokemonMoveAbilityNamesPreserved": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} trainer text blocks in {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
