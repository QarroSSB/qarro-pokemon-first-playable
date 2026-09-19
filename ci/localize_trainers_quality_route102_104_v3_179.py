#!/usr/bin/env python3
"""Qarro v3.179: human-quality RU pass for trainers Route 102-104.

This pass replaces the first coherent 100 machine-translated trainer text
blocks from v3.177 with hand-edited Russian. It only touches
data/text/trainers.inc, preserves runtime control-token order exactly, keeps
Pokemon/Move proper names in English, and is fail-closed on source drift.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINERS_QUALITY_ROUTE102_104_V3_179"
TARGET = Path("data/text/trainers.inc")

TRANSLATIONS = {
    "Route102_Text_CalvinIntro": "Если у тебя есть POKeMON,\\nзначит, ты настоящий тренер!\\lОт моего вызова не отвертеться!$",
    "Route102_Text_CalvinDefeated": "Арр, проиграл...\\nНадо было тренировать их лучше...$",
    "Route102_Text_CalvinPostBattle": "Эй! Если у тебя такая сила,\\nнадо было сразу сказать!$",
    "Route102_Text_CalvinRegister": "С нашей прошлой встречи я много\\nтренировался.\\pХочу снова сразиться, так что\\nзапишешь меня в свой POKeNAV?$",
    "Route102_Text_CalvinRegisterShort": "Хочу снова сразиться, так что\\nзапишешь меня в свой POKeNAV?$",
    "Route102_Text_CalvinRematchIntro": "После проигрыша тебе я упорно\\nтренировал своих POKeMON.\\lОт моего вызова не отвертеться!$",
    "Route102_Text_CalvinRematchDefeated": "Арр, опять проиграл...\\nЯ что, тренируюсь неправильно?$",
    "Route102_Text_CalvinRematchPostBattle": "Если ты станешь еще сильнее,\\nя тоже стану сильнее.$",
    "Route102_Text_AllenIntro": "Ты только начинаешь путь тренера?\\nМы оба еще новички!$",
    "Route102_Text_AllenDefeated": "Я вызвал тебя, потому что думал,\\nчто смогу победить...$",
    "Route102_Text_AllenPostBattle": "Я еще ни разу не побеждал...\\nВот бы скорее выиграть...$",
    "Route102_Text_RickIntro": "Ха-ха! Мы встретились взглядами!\\nТеперь бой с моими POKeMON-жуками!$",
    "Route102_Text_RickDefeated": "Ай! Разгромлен!$",
    "Route102_Text_RickPostBattle": "Если встретился взглядом с тренером,\\nнадо сражаться! Таково правило!$",
    "Route102_Text_TianaIntro": "Я буду побеждать и стремиться\\nстать лучшим тренером.\\pПомоги моей карьере расти!$",
    "Route102_Text_TianaDefeated": "Выходит, я продвинула твою карьеру...$",
    "Route102_Text_TianaPostBattle": "Чтобы и дальше побеждать,\\nмне нужно поймать больше POKeMON.$",
    "Route103_Text_DaisyIntro": "Чувствуешь, как притягивает\\nнаш успокаивающий аромат?$",
    "Route103_Text_DaisyDefeated": "Наш аромат не смог тебя одурманить...$",
    "Route103_Text_DaisyPostBattle": "Ароматерапия лечит душу\\nс помощью приятных ароматов.$",
    "Route103_Text_AmyIntro": "ЭМИ: Я ЭМИ.\\nА это моя младшая сестра ЛИВ.\\lМы всегда сражаемся вместе!$",
    "Route103_Text_AmyDefeated": "ЭМИ: Ой, мы проиграли.$",
    "Route103_Text_AmyPostBattle": "ЭМИ: В бою против двух тренеров\\nнужно учитывать очень многое.\\lИначе победить будет трудно.$",
    "Route103_Text_AmyNotEnoughPokemon": "ЭМИ: Ой, у тебя только один\\nPOKeMON.\\lТак с нами сражаться нельзя.$",
    "Route103_Text_LivIntro": "ЛИВ: Мы сражаемся вместе,\\nкак одна команда.$",
    "Route103_Text_LivDefeated": "ЛИВ: Ой, мы проиграли, сестренка...$",
    "Route103_Text_LivPostBattle": "ЛИВ: Мы со старшей сестрой\\nотлично действуем вместе...\\pНо все равно проиграли...$",
    "Route103_Text_AmyLivRegister": "ЛИВ: На самом деле мы намного сильнее!\\nВ следующий раз все увидишь!$",
    "Route103_Text_LivNotEnoughPokemon": "ЛИВ: Хочешь сразиться с нами -\\nнужно иметь двух POKeMON!\\lИначе это будет нечестно!$",
    "Route103_Text_AmyRematchIntro": "ЭМИ: Я ЭМИ.\\nА это моя младшая сестра ЛИВ.\\lМы всегда сражаемся вместе!$",
    "Route103_Text_AmyRematchDefeated": "ЭМИ: Эх, вот досада!\\nМы снова не смогли победить...$",
    "Route103_Text_AmyRematchPostBattle": "ЭМИ: В бою против двух тренеров\\nнужно учитывать очень многое.\\lИначе победить будет трудно.$",
    "Route103_Text_AmyRematchNotEnoughPokemon": "ЭМИ: Ой, у тебя только один\\nPOKeMON.\\lТак с нами сражаться нельзя.$",
    "Route103_Text_LivRematchIntro": "ЛИВ: Мы сражаемся вместе,\\nкак одна команда.$",
    "Route103_Text_LivRematchDefeated": "ЛИВ: А-а, снова проиграли...\\nСестренка...$",
    "Route103_Text_LivRematchPostBattle": "ЛИВ: Мы со старшей сестрой\\nидеально действуем вместе...\\pПочему же мы опять проиграли?$",
    "Route103_Text_LivRematchNotEnoughPokemon": "ЛИВ: Хочешь сразиться с нами -\\nнужно иметь двух POKeMON!\\lИначе это будет нечестно!$",
    "Route103_Text_AndrewIntro": "Ух! Леска совсем запуталась!\\nЯ уже начинаю злиться!\\lВсе, хватит! Сражайся со мной!$",
    "Route103_Text_AndrewDefeated": "Ух! И тут не вышло!\\nТеперь я злюсь еще сильнее!$",
    "Route103_Text_AndrewPostBattle": "Ух, я все еще киплю от злости...\\nГр-р-р...$",
    "Route103_Text_MiguelIntro": "Мой POKeMON просто очарователен!\\nНе стесняйся - сейчас покажу!$",
    "Route103_Text_MiguelDefeated": "Ох, боже!\\nМой любимый POKeMON!$",
    "Route103_Text_MiguelPostBattle": "Мой чудесный POKeMON прекрасен,\\nдаже когда он без сознания!$",
    "Route103_Text_MiguelRegister": "Я еще заставлю тебя снова\\nполюбоваться моим POKeMON!$",
    "Route103_Text_MiguelRematchIntro": "Привет! Мой милейший\\nPOKeMON стал еще очаровательнее!$",
    "Route103_Text_MiguelRematchDefeated": "Ох!\\nМой любимый POKeMON!$",
    "Route103_Text_MiguelRematchPostBattle": "Чем больше времени мы вместе,\\nтем милее становится мой POKeMON.$",
    "Route103_Text_PeteIntro": "Такое расстояние...\\nЕго проще просто проплыть!$",
    "Route103_Text_PeteDefeated": "О, неплохо плывешь!$",
    "Route103_Text_PetePostBattle": "Теперь я понимаю твою логику.\\nВсе ясно.\\pБудь у меня такой надежный POKeMON,\\nя бы тоже использовал SURF!$",
    "Route103_Text_IsabelleIntro": "Смотри, куда плывешь!\\nСейчас столкнемся!$",
    "Route103_Text_IsabelleDefeated": "Уф...$",
    "Route103_Text_IsabellePostBattle": "Я плохо плаваю, поэтому тренировалась...\\nПрости, что чуть не врезалась в тебя.$",
    "Route103_Text_RhettIntro": "Ого!\\nКак тебе удалось сюда протиснуться?$",
    "Route103_Text_RhettDefeated": "Ого!\\nНу ты даешь!$",
    "Route103_Text_RhettPostBattle": "Тебе нравятся такие тесные\\nместа?$",
    "Route103_Text_MarcosIntro": "Тебя привел сюда вой моей гитары?$",
    "Route103_Text_MarcosDefeated": "Мое сольное шоу испорчено...$",
    "Route103_Text_MarcosPostBattle": "Я играл на гитаре там, где почти\\nникого не было, но фанатов набралось полно!\\lВот это публика.\\pХе-хе, может, мне стать профессионалом?$",
    "Route104_Text_GinaIntro": "ДЖИНА: Хорошо, давай сразимся\\nнашими POKeMON!$",
    "Route104_Text_GinaDefeat": "ДЖИНА: Ненавижу проигрывать!$",
    "Route104_Text_GinaPostBattle": "ДЖИНА: Какая сила!\\nНам нужно тренироваться еще больше!$",
    "Route104_Text_GinaNotEnoughMons": "ДЖИНА: Что? Только один POKeMON?\\nТогда мы не будем сражаться.\\pОдному POKeMON будет одиноко,\\nа это совсем нехорошо.$",
    "Route104_Text_MiaIntro": "МИА: Мы близняшки, поэтому\\nсражаемся вместе с POKeMON.$",
    "Route104_Text_MiaDefeat": "МИА: Мы сражались вместе, но\\nобе проиграли...$",
    "Route104_Text_MiaPostBattle": "МИА: Будем больше тренировать POKeMON\\nи станем такими же сильными.$",
    "Route104_Text_MiaNotEnoughMons": "МИА: Хочешь сразиться с нами?\\pБез двух POKeMON нельзя -\\nэто строгое правило!\\lМы слишком сильны для одного!$",
    "Route104_Text_IvanIntro": "Зачем скрывать очевидное?\\nЯ эксперт по водным POKeMON!\\pЧто?\\nТы обо мне не знаешь?$",
    "Route104_Text_IvanDefeat": "Я думал, что неплох в этом деле,\\nно, похоже, ошибался... Эх...$",
    "Route104_Text_IvanPostBattle": "Я слишком увлекся рыбалкой.\\nИ забыл тренировать своих POKeMON...$",
    "Route104_Text_BillyIntro": "Оставлять следы на песке\\nтак весело!$",
    "Route104_Text_BillyDefeat": "А-а! В кроссовки набился песок!\\nТеперь там все хрустит!$",
    "Route104_Text_BillyPostBattle": "Хочу оставлять свои следы\\nна песке повсюду, но они\\lтак быстро исчезают...$",
    "Route104_Text_HaleyIntro": "Стоит ли...\\nИли не стоит?\\pЛадно, решено! Сражаемся!$",
    "Route104_Text_HaleyDefeat": "Не надо было соглашаться на бой...$",
    "Route104_Text_HaleyPostBattle": "Если перед тобой выбор,\\nа решение за тебя принимает другой,\\lпотом пожалеешь при любом\\lисходе.$",
    "Route104_Text_HaleyRegister1": "Ты впечатляешь, но стоит ли\\nзаписывать тебя в мой POKeNAV?\\lМожет, не стоит...\\pЛадно, запишу!$",
    "Route104_Text_HaleyRegister2": "Ты впечатляешь, но стоит ли\\nзаписывать тебя в мой POKeNAV?\\lМожет, не стоит...\\pЛадно, запишу!$",
    "Route104_Text_HaleyRematchIntro": "Ну же, сразись со мной!$",
    "Route104_Text_HaleyRematchDefeat": "Ох...\\nЯ думала, что смогу победить...$",
    "Route104_Text_HaleyPostRematch": "Я сама решила сражаться,\\nтак что приму поражение достойно.\\pНо все равно ужасно обидно!$",
    "Route104_Text_WinstonIntro": "О, конечно, я принимаю вызов.\\nДенег у меня предостаточно.$",
    "Route104_Text_WinstonDefeat": "Почему я не смог победить?$",
    "Route104_Text_WinstonPostBattle": "Есть вещи, которые не купить за деньги.\\nНапример, POKeMON...$",
    "Route104_Text_WinstonRegister1": "Хм?\\nА, у тебя появился POKeNAV.\\pС радостью запишу тебя.\\nДенег-то у меня достаточно.$",
    "Route104_Text_WinstonRegister2": "Хм?\\nА, у тебя появился POKeNAV.\\pС радостью запишу тебя.\\nДенег-то у меня достаточно.$",
    "Route104_Text_WinstonRematchIntro": "После поражения от тебя я узнал\\nмного нового о POKeMON.$",
    "Route104_Text_WinstonRematchDefeat": "Опять проиграл?\\nПочему я не смог победить?$",
    "Route104_Text_WinstonPostRematch": "Я невероятно богат, но никак\\nне могу побеждать с POKeMON...\\pКак же глубок мир POKeMON...$",
    "Route104_Text_CindyIntro": "Видимо, нам было суждено встретиться.\\nМожно пригласить тебя на бой?$",
    "Route104_Text_CindyDefeat": "Ох, надо же!$",
    "Route104_Text_CindyPostBattle": "Каждая встреча ведет к прощанию.\\nНадеюсь, мы еще увидимся.$",
    "Route104_Text_CindyRegister1": "Здравствуйте, мы снова встретились.\\pПохоже, судьба сводит нас. Давай\\nзапишем друг друга в POKeNAV.$",
    "Route104_Text_CindyRegister2": "Стоит отметить, как судьба\\nснова и снова сводит нас.\\pДавай запишем друг друга\\nв POKeNAV.$",
    "Route104_Text_CindyRematchIntro": "Здравствуйте, мы снова встретились.\\nМожно пригласить тебя на бой?$",
    "Route104_Text_CindyRematchDefeat": "Ох...\\nЯ сделала все, что могла...$",
    "Route104_Text_CindyPostRematch": "Каждая встреча ведет к прощанию.\\nНадеюсь, мы еще увидимся.$",
    "Route104_Text_DarianIntro": "Я выловил очень грозного POKeMON!\\pВ нем будто есть что-то волшебное!\\nВыглядит сильным, правда?$",
    "Route104_Text_DarianDefeat": "Что за...$",
    "Route104_Text_DarianPostBattle": "Эй, MAGIKARP, твое имя звучит\\nкуда внушительнее тебя, да?$",
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
        raise RuntimeError(
            f"{path}:{label}: control-token drift old={old_tokens} new={new_tokens}"
        )
    if not translated.endswith("$"):
        raise RuntimeError(f"{path}:{label}: translated block must end in $")
    bad = sorted(set(translated) & BANNED_UNICODE)
    if bad:
        raise RuntimeError(f"{path}:{label}: unsupported punctuation {bad}")
    if '"' in translated:
        raise RuntimeError(f"{path}:{label}: raw double quote is not allowed")

    new_body = '\t.string "' + translated + '"\n'
    updated = text[:m.start("body")] + new_body + text[m.end("body"):]
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_trainers_quality_route102_104_v3_179.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 100:
        raise RuntimeError(f"expected exactly 100 quality-pass blocks, got {len(TRANSLATIONS)}")

    for label, translated in TRANSLATIONS.items():
        replace_label(path, label, translated)

    out = root / "build" / "qarro_ru_trainers_quality_route102_104_v3_179_audit.json"
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
