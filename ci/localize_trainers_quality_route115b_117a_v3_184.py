#!/usr/bin/env python3
"""Qarro v3.184: human-quality RU pass for trainer chunk 6.

Covers the next contiguous 100 machine-translated blocks in trainers.inc:
the rest of Route 115, Route 116 and the opening of Route 117.
Localization-only; exact runtime control-token sequences are preserved and
source drift fails closed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINERS_QUALITY_ROUTE115B_117A_V3_184"
TARGET = Path("data/text/trainers.inc")

TRANSLATIONS = {
    "Route115_Text_CyndyPostRematch": "Даже проиграв, я все равно получаю\\nудовольствие от боя.\\lНаверное, я просто люблю POKeMON.$",
    "Route115_Text_HectorIntro": "У меня есть редкий POKeMON!\\nХочешь, покажу?$",
    "Route115_Text_HectorDefeat": "Т-ты...\\nТы хочешь забрать моего POKeMON, да?$",
    "Route115_Text_HectorPostBattle": "У меня есть этот редкий POKeMON.\\nМне этого вполне достаточно.$",
    "Route115_Text_KyraIntro": "Буду сражаться прямо на бегу!\\nПопробуй за мной угнаться!$",
    "Route115_Text_KyraDefeat": "Фух, фух...$",
    "Route115_Text_KyraPostBattle": "Зря я решила сражаться\\nпрямо во время бега!\\pНадо пробежаться, чтобы успокоиться...$",
    "Route115_Text_JaidenIntro": "Получи!\\nУльтра-ниндзя-атака POKeMON!$",
    "Route115_Text_JaidenDefeat": "А-а-а!\\nНаша стратегия провалилась!$",
    "Route115_Text_JaidenPostBattle": "Но мои POKeMON были просто ультра,\\nправда?$",
    "Route115_Text_HeleneIntro": "Сила моих POKeMON достойна\\nчерного пояса!$",
    "Route115_Text_HeleneDefeat": "Какой позор!$",
    "Route115_Text_HelenePostBattle": "Я редко встречаю кого-то лучше\\nсебя...\\pТеперь понятно!\\nТы ЛИДЕР ЗАЛА, да?$",
    "Route115_Text_AlixIntro": "Мы встретились взглядами!\\nТеперь уже не уйти!$",
    "Route115_Text_AlixDefeat": "Гах!\\nНеплохо!$",
    "Route115_Text_AlixPostBattle": "Ну и ладно.\\nДумаю, использую TELEPORT и вернусь домой.$",
    "Route115_Text_MarleneIntro": "Ты нарушил мою медитацию...\\nЗа это придется ответить.$",
    "Route115_Text_MarleneDefeat": "Ты разрушил мою концентрацию!$",
    "Route115_Text_MarlenePostBattle": "Я медитировала вместе с POKeMON.\\nНо здесь не слишком спокойно...$",
    "Route116_Text_ClarkIntro": "Если туннель не проходит насквозь,\\nя просто перевалю через гору.$",
    "Route116_Text_ClarkDefeat": "Фух... Фух...\\nОт поражения я совсем выдохся...$",
    "Route116_Text_ClarkPostBattle": "Ничего страшного, если туннеля нет.\\nДля туриста горы и есть дороги!$",
    "Route116_Text_JoeyIntro": "Мои POKeMON рулят!\\nСмотри сам!$",
    "Route116_Text_JoeyDefeat": "Ай! Ссадина!\\nНужно заклеить пластырем!$",
    "Route116_Text_JoeyPostBattle": "Пластыри - признак крутости!\\nВот еще один!$",
    "Route116_Text_JoseIntro": "Мои POKeMON-жуки сильные!\\nДавай сразимся!$",
    "Route116_Text_JoseDefeat": "Я проиграл!\\nА думал, что победа уже моя!$",
    "Route116_Text_JosePostBattle": "POKeMON-жуки быстро эволюционируют.\\nПоэтому и сильнее становятся быстро.$",
    "Route116_Text_JaniceIntro": "Сейчас покажу, насколько силен мой\\nочаровательный POKeMON!$",
    "Route116_Text_JaniceDefeat": "Ты на ступень выше меня...$",
    "Route116_Text_JanicePostBattle": "POKeMON, сочетающий миловидность и\\nсилу, - вот мой идеал.$",
    "Route116_Text_JerryIntro": "В ШКОЛЕ ТРЕНЕРОВ мы изучаем\\nсамые разные вещи.\\pХочу проверить знания на практике!$",
    "Route116_Text_JerryDefeat": "Я ленился в школе...\\nВот почему проиграл.$",
    "Route116_Text_JerryPostBattle": "Придется повторить несколько уроков в\\nШКОЛЕ ТРЕНЕРОВ.\\lИначе РОКСАННА будет в ярости.$",
    "Route116_Text_JerryRegister1": "В ШКОЛЕ ТРЕНЕРОВ я узнал,\\nчто POKeNAV может записывать тренеров.\\pНе совсем понимаю, как это работает,\\nтак что можно попробовать?$",
    "Route116_Text_JerryRegister2": "В ШКОЛЕ ТРЕНЕРОВ я узнал,\\nчто POKeNAV может записывать тренеров.\\pНе совсем понимаю, как это работает,\\nтак что можно попробовать?$",
    "Route116_Text_JerryRematchIntro": "Я серьезно занимался в\\nШКОЛЕ ТРЕНЕРОВ.\\lНа этот раз не проиграю.$",
    "Route116_Text_JerryRematchDefeat": "Что?\\nЯ ведь так усердно учился.$",
    "Route116_Text_JerryPostRematch": "Придется повторить несколько уроков в\\nШКОЛЕ ТРЕНЕРОВ.\\lИначе РОКСАННА будет в ярости.$",
    "Route116_Text_KarenIntro": "Я учусь и в школе, и\\nпо дороге домой!$",
    "Route116_Text_KarenDefeat": "Я в шоке - я проиграла?$",
    "Route116_Text_KarenPostBattle": "Ох, так я никогда не стану элегантным\\nтренером, как РОКСАННА!$",
    "Route116_Text_KarenRegister1": "Ого! Это же POKeNAV?\\nУ меня тоже есть! Запиши меня!$",
    "Route116_Text_KarenRegister2": "Ого! Это же POKeNAV?\\nУ меня тоже есть! Запиши меня!$",
    "Route116_Text_KarenRematchIntro": "После нашей встречи я очень много училась.\\nСмотри, чего я добилась!$",
    "Route116_Text_KarenRematchDefeat": "Я в шоке.\\nОпять проиграла?$",
    "Route116_Text_KarenPostRematch": "Ты победил РОКСАННУ?\\nТогда мне тебя пока не одолеть.$",
    "Route116_Text_SarahIntro": "Чтобы ты знал: меня еще ни разу\\nникто ни в чем не превзошел.$",
    "Route116_Text_SarahDefeat": "О боже.\\nДля меня это совершенно новый опыт.$",
    "Route116_Text_SarahPostBattle": "Роскошная жизнь дает мне все,\\nчего только можно пожелать.\\pНо когда дело касается POKeMON,\\nбогатство ничего не значит.$",
    "Route116_Text_DawsonIntro": "Стоит увидеть великолепную шерсть моих POKeMON,\\nи их красота мгновенно сделает\\lтебя беспомощным!$",
    "Route116_Text_DawsonDefeat": "О нет, только не это!$",
    "Route116_Text_DawsonPostBattle": "Нет, нет, нет!\\nТы растрепал шерсть моих POKeMON!\\lИ мою прическу тоже испортил!\\lПридется срочно звонить стилисту!$",
    "Route116_Text_DevanIntro": "Мы тебя как следует встряхнем!$",
    "Route116_Text_DevanDefeat": "Ай-яй-яй!\\nБез шансов!$",
    "Route116_Text_DevanPostBattle": "Пожалуй, стоит попробовать POKeMON\\nдругих типов.$",
    "Route116_Text_JohnsonIntro": "Дальше тупик.\\nМне скучно, может, сразимся?$",
    "Route116_Text_JohnsonDefeat": "Даже проигрывать было весело.$",
    "Route116_Text_JohnsonPostBattle": "Может, останешься здесь и\\nсоставишь мне компанию?$",
    "Route117_Text_IsaacIntro": "Слушай, не мог бы ты сразиться\\nс POKeMON, которых я выращиваю?$",
    "Route117_Text_IsaacDefeat": "Твои выращены великолепно...$",
    "Route117_Text_IsaacPostBattle": "В POKeMON важна не только сила.\\pРазвивать уникальные черты\\nкаждого - еще один способ наслаждаться\\lPOKeMON.$",
    "Route117_Text_IsaacRegister": "Я удвою усилия в тренировках.\\nЗаглянешь потом посмотреть на нас?$",
    "Route117_Text_IsaacRematchIntro": "POKeMON, которых я выращивал,\\nпо-прежнему выглядят отлично.$",
    "Route117_Text_IsaacRematchDefeat": "Ты умеешь правильно их растить.\\nУ тебя талант воспитателя...$",
    "Route117_Text_IsaacPostRematch": "Твои POKeMON отлично растут!\\nТебе стоит выставить их на КОНКУРСЫ.$",
    "Route117_Text_LydiaIntro": "Позволь мне оценить, правильно ли\\nты выращиваешь своих POKeMON.$",
    "Route117_Text_LydiaDefeat": "Да, они развиваются как надо.$",
    "Route117_Text_LydiaPostBattle": "Попробуй растить POKeMON, уделяя больше\\nвнимания особенностям их характера.$",
    "Route117_Text_LydiaRegister": "Рада встретить такого отличного тренера.\\nНадеюсь, увидимся снова.$",
    "Route117_Text_LydiaRematchIntro": "Позволь еще раз оценить, правильно ли\\nты выращиваешь своих POKeMON.$",
    "Route117_Text_LydiaRematchDefeat": "Они развиваются превосходно.$",
    "Route117_Text_LydiaPostRematch": "POKeMON предпочитают разные виды\\n{POKEBLOCK} в зависимости от характера.$",
    "Route117_Text_DylanIntro": "Я посреди триатлона, но какая разница -\\nдавай сразимся!$",
    "Route117_Text_DylanDefeat": "У меня кончились силы!$",
    "Route117_Text_DylanPostBattle": "Кажется, я все испортил...\\pЗа время этого боя я мог скатиться\\nна последнее место...$",
    "Route117_Text_DylanRegister": "POKeMON тоже должны быть сильными?\\nНаучи меня тренироваться!$",
    "Route117_Text_DylanRematchIntro": "Я прямо посреди триатлона,\\nно уверенно лидирую.\\lДавай быстро сразимся!$",
    "Route117_Text_DylanRematchDefeat": "Опять закончились силы!$",
    "Route117_Text_DylanPostRematch": "В плавании и велогонке я лучший,\\nно с POKeMON пока чувствую себя\\lне так уверенно.$",
    "Route117_Text_MariaIntro": "Я тренируюсь к триатлону вместе с POKeMON,\\nтак что в своей скорости уверена.$",
    "Route117_Text_MariaDefeat": "Похоже, мне нужно больше\\nтренироваться.$",
    "Route117_Text_MariaPostBattle": "Тренировки приносят пользу, только если\\nзаниматься регулярно.\\pЛадно! Возобновлю тренировки!\\nЗавтра!$",
    "Route117_Text_MariaRegister": "Похоже, ты тренируешься как следует...\\nЕсли хочешь, потом сразимся!$",
    "Route117_Text_MariaRematchIntro": "Не забрасываешь тренировки?\\nЯ точно нет!\\lСейчас покажу результат!$",
    "Route117_Text_MariaRematchDefeat": "Похоже, мне нужно больше\\nтренироваться.$",
    "Route117_Text_MariaPostRematch": "Завтра снова начну тренироваться.\\nДавай как-нибудь еще сразимся!$",
    "Route117_Text_DerekIntro": "Когда-то я был ЛОВЦОМ ЖУКОВ!\\nА теперь я МАНЬЯК ЖУКОВ!\\pНо моя любовь к POKeMON остается\\nнеизменной!$",
    "Route117_Text_DerekDefeat": "И моя неумелость тоже остается\\nнеизменной...$",
    "Route117_Text_DerekPostBattle": "Я просто следовал зову сердца, и теперь\\nменя зовут МАНЬЯКОМ ЖУКОВ...\\pНо я эксперт по POKeMON-жукам,\\nтак что вполне естественно, что меня называют\\lМАНЬЯКОМ ЖУКОВ.$",
    "Route117_Text_AnnaIntro": "АННА: Я вместе со своей милой младшей\\nнапарницей. Нужно показать класс!$",
    "Route117_Text_AnnaDefeat": "АННА: Я же со своей младшей\\nнапарницей! Дай мне победить!$",
    "Route117_Text_AnnaPostBattle": "АННА: У твоих POKeMON отличные\\nсочетания.\\pПожалуй, вы уступаете только нам!$",
    "Route117_Text_AnnaAndMegRegister": "АННА: Мы не можем так это оставить!\\nТы ведь вернешься, правда?$",
    "Route117_Text_AnnaNotEnoughMons": "АННА: Хочешь сразиться с нами -\\nвозьми с собой двух POKeMON.$",
    "Route117_Text_MegIntro": "МЭГ: Я объединюсь со своей супер\\nстаршей напарницей и одолею тебя!$",
    "Route117_Text_MegDefeat": "МЭГ: О нет!\\nПрости, АННА! Я тебя подвела...$",
    "Route117_Text_MegPostBattle": "МЭГ: Я подвела АННУ...\\nБез меня она бы победила!$",
    "Route117_Text_MegNotEnoughMons": "МЭГ: У тебя только один POKeMON?\\nТогда мы не можем сражаться.\\pМы хотим бой два на два.$",
    "Route117_Text_AnnaRematchIntro": "АННА: Я ведь не могу постоянно проигрывать перед\\nсвоей младшей напарницей, правда?$",
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
        raise SystemExit("usage: localize_trainers_quality_route115b_117a_v3_184.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 100:
        raise RuntimeError(f"expected exactly 100 quality-pass blocks, got {len(TRANSLATIONS)}")
    for label, translated in TRANSLATIONS.items():
        replace_label(path, label, translated)

    out = root / "build" / "qarro_ru_trainers_quality_route115b_117a_v3_184_audit.json"
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
