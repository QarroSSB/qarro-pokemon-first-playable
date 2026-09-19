#!/usr/bin/env python3
"""Qarro v3.183: human-quality RU pass for trainer chunk 5.

Covers the next contiguous 100 machine-translated blocks in trainers.inc:
the rest of Route 113, Route 114 and the opening of Route 115.
Localization-only; exact runtime control-token sequences are preserved and
source drift fails closed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINERS_QUALITY_ROUTE113B_115A_V3_183"
TARGET = Path("data/text/trainers.inc")

TRANSLATIONS = {
    "Route113_Text_LaoPostBattle": "Мне еще нужно отточить искусство скрытности.\\nПрощай.$",
    "Route113_Text_LaoRegister": "Йия! Узри древнюю технику ниндзя\\nрегистрации в POKeNAV!$",
    "Route113_Text_LaoRematchIntro": "Из пепла выскакиваю я! Хия!\\nБросаю тебе вызов!$",
    "Route113_Text_LaoRematchDefeat": "С честью признаю поражение!$",
    "Route113_Text_LaoPostRematch": "Моя безупречная маскировка подвела\\nиз-за слабых боевых навыков...\\pПрощай.$",
    "Route113_Text_LungIntro": "Спасибо, что нашел меня!\\nНо нам все равно придется сразиться!$",
    "Route113_Text_LungDefeat": "Сейчас применю ниндзюцу...\\nВУЛКАНИЧЕСКИЙ ПЕПЕЛ: ВИХРЕВОЙ ПЛАЩ!\\pЧто?\\nУже все закончилось?$",
    "Route113_Text_LungPostBattle": "Знаешь, что плохо в прятках?\\nСтановится одиноко, если никто не приходит.$",
    "Route113_Text_ToriIntro": "ТОРИ: Мы обе собираем пепел.\\nИ с POKeMON тоже сражаемся.$",
    "Route113_Text_ToriDefeat": "ТОРИ: Мы проиграли... Скучно, пойду\\nсобирать еще пепел.$",
    "Route113_Text_ToriPostBattle": "ТОРИ: Сколько у нас уже пепла?\\nНадеюсь, хватит на БЕЛУЮ ФЛЕЙТУ.$",
    "Route113_Text_ToriNotEnoughMons": "ТОРИ: Мы хотим бой два на два.\\nИначе мы точно проиграем!$",
    "Route113_Text_TiaIntro": "ТИА: Мы обе собираем пепел.\\nИ с POKeMON тоже сражаемся.$",
    "Route113_Text_TiaDefeat": "ТИА: Мы не смогли победить... Скучно,\\nпойду собирать еще пепел.$",
    "Route113_Text_TiaPostBattle": "ТИА: У нас уже много пепла!\\nДумаю, на БЕЛУЮ ФЛЕЙТУ хватит!$",
    "Route113_Text_TiaNotEnoughMons": "ТИА: Мы хотим бой два на два.\\nИначе победить не получится!$",
    "Route113_Text_CobyIntro": "Пф-ф! Этими крыльями я могу\\nсдуть тебя прочь!$",
    "Route113_Text_CobyDefeat": "А... Что?$",
    "Route113_Text_CobyPostBattle": "Даже не знаю, что сказать, когда меня\\nтак легко побеждают...$",
    "Route113_Text_SophieIntro": "От здешнего тепла меня клонит в сон.\\nСразись со мной, чтобы я не уснула.$",
    "Route113_Text_SophieDefeat": "Это сон.\\nТочно сон...$",
    "Route113_Text_SophiePostBattle": "От поражения прямо горю...\\nВсе, сплю прямо здесь!\\lХр-р-р!$",
    "Route113_Text_LawrenceIntro": "Ты случайно не собирал\\nвулканический пепел?$",
    "Route113_Text_LawrenceDefeat": "Хе-хе.\\nНас разгромили подчистую.$",
    "Route113_Text_LawrencePostBattle": "Мне тоже стоит спрятаться под пеплом.$",
    "Route113_Text_WyattIntro": "Т-ты хочешь сразиться со мной?\\nХотя я только что поймал POKeMON?$",
    "Route113_Text_WyattDefeat": "Т-ты так радуешься победе?\\nХотя соперник всего лишь я?$",
    "Route113_Text_WyattPostBattle": "А теперь решил что-то сказать\\nпроигравшему?\\pНу да, ты у нас самый крутой.\\nХмф!$",
    "Route114_Text_LennyIntro": "Йоделай-хи-хо!\\p... ...\\pВообще-то ты должен ответить\\nЙОДЕЛАЙ-ХИ-ХО, раз тут нет\\lэха!$",
    "Route114_Text_LennyDefeat": "Йоделай-хи-хо!$",
    "Route114_Text_LennyPostBattle": "В детстве я верил, что кто-то\\nповторяет за мной и кричит\\lв ответ: ЙОДЕЛАЙ-ХИ-ХО!$",
    "Route114_Text_LucasIntro": "Если не подготовился, не стоит\\nлезть в горы!$",
    "Route114_Text_LucasDefeat": "Горы ошибок не прощают...$",
    "Route114_Text_LucasPostBattle": "Зимой горы становятся смертельно опасными\\nиз-за метелей и лавин.$",
    "Route114_Text_ShaneIntro": "Кемпинг - это здорово! Можно рыбачить, жарить\\nмаршмеллоу и рассказывать страшилки!\\pНо лучше всего - бои POKeMON\\nна природе!$",
    "Route114_Text_ShaneDefeat": "Слишком силен!$",
    "Route114_Text_ShanePostBattle": "Здорово, что можно ходить\\nв походы вместе с POKeMON.$",
    "Route114_Text_NancyIntro": "После еды надо размяться.\\nДавай сразимся!$",
    "Route114_Text_NancyDefeat": "О нет!$",
    "Route114_Text_NancyPostBattle": "Я только что вкусно поела.\\nТеперь меня клонит в сон...$",
    "Route114_Text_SteveIntro": "Уфуфуфу...\\nХочешь сразиться с моим POKeMON?$",
    "Route114_Text_SteveDefeat": "М-мой POKeMON...$",
    "Route114_Text_StevePostBattle": "Огромное бугристое тело, твердое как камень,\\nгигантские рога и страшные клыки...\\pУфуфуфу...\\nВот бы мне такого POKeMON...$",
    "Route114_Text_SteveRegister": "Не забывай, что со мной сделал!\\nЯ позабочусь, чтобы ты не забыл!$",
    "Route114_Text_SteveRematchIntro": "Уфуфуфу...\\nДавай, сразись с моим POKeMON...$",
    "Route114_Text_SteveRematchDefeat": "Как же мне повезло увидеть твоего\\nPOKeMON...$",
    "Route114_Text_StevePostRematch": "Уфуфуфу...\\pКогда вижу сражающихся POKeMON, меня всего\\nначинает трясти...$",
    "Route114_Text_BernieIntro": "Если разводишь костер,\\nвсегда держи рядом воду.$",
    "Route114_Text_BernieDefeat": "Спасибо, что потушил мой огонь!$",
    "Route114_Text_BerniePostBattle": "С огнем в лесу всегда нужно быть\\nпредельно осторожным.\\pНикогда не недооценивай силу\\nогня.$",
    "Route114_Text_BernieRegister": "Ты разжег во мне боевой дух.\\nДавай запишем друг друга!$",
    "Route114_Text_BernieRematchIntro": "Научился держать воду под рукой\\nрядом с костром?$",
    "Route114_Text_BernieRematchDefeat": "Похоже, меня окатили водой раньше, чем я\\nуспел разгореться.$",
    "Route114_Text_BerniePostRematch": "С огнем в лесу всегда нужно быть\\nпредельно осторожным.\\pНикогда не недооценивай силу\\nогня.$",
    "Route114_Text_ClaudeIntro": "Будь это рыбалка, у тебя не было бы\\nни единого шанса против меня.\\lТак что выпускай своих POKeMON!$",
    "Route114_Text_ClaudeDefeat": "Будь это рыбалка, я бы победил...$",
    "Route114_Text_ClaudePostBattle": "Пожалуй, попробую поймать\\nчто-нибудь крупное у МЕТЕОР-ФОЛЛС.\\pТам точно что-то водится.\\nЯ это чувствую.$",
    "Route114_Text_NolanIntro": "Я люблю рыбачить. Но еще люблю\\nсражаться!\\pЕсли кто-то бросает вызов, я согласен,\\nдаже посреди рыбалки.$",
    "Route114_Text_NolanDefeat": "Я люблю сражаться, но это еще не значит,\\nчто я хорош в боях...$",
    "Route114_Text_NolanPostBattle": "В этот раз точно получится!\\pЯ всегда так думаю, поэтому и не могу\\nбросить ни рыбалку, ни POKeMON.$",
    "Route114_Text_TyraIntro": "ТАЙРА: Ну конечно.\\nЯ как раз в настроении.\\lПокажу тебе кое-что о POKeMON.$",
    "Route114_Text_TyraDefeat": "ТАЙРА: Какой потрясающий стиль боя!$",
    "Route114_Text_TyraPostBattle": "ТАЙРА: Я как раз учила младшую ученицу АЙВИ\\nобращаться с POKeMON.$",
    "Route114_Text_TyraNotEnoughMons": "ТАЙРА: Хи-хи...\\nХочешь сразиться с нами - одного\\lPOKeMON недостаточно!$",
    "Route114_Text_IvyIntro": "АЙВИ: Кто научил тебя обращаться с POKeMON?$",
    "Route114_Text_IvyDefeat": "АЙВИ: Какой потрясающий стиль боя!$",
    "Route114_Text_IvyPostBattle": "АЙВИ: Я начала тренировать POKeMON,\\nпотому что ТАЙРА, моя старшая наставница,\\lвсему меня научила!$",
    "Route114_Text_IvyNotEnoughMons": "АЙВИ: У тебя только один POKeMON?\\nНаверное, ему одиноко.$",
    "Route114_Text_KaiIntro": "Я поймал крупную рыбину!\\nОгромную, говорю тебе!$",
    "Route114_Text_KaiDefeat": "Что это было?\\nМоя оказалась меньше?$",
    "Route114_Text_KaiPostBattle": "Ладно!\\nПросто поймаю еще крупнее!$",
    "Route114_Text_CharlotteIntro": "Я!\\nЯ не только красивое личико!$",
    "Route114_Text_CharlotteDefeat": "Это было совсем не мило!$",
    "Route114_Text_CharlottePostBattle": "Мне не нужен POKeMON, который\\nпросто милый.\\pЯ обожаю милых, но с парой странностей\\nв характере!$",
    "Route114_Text_AngelinaIntro": "Твои POKeMON часто\\nэволюционировали?$",
    "Route114_Text_AngelinaDefeat": "Понятно.\\nПолезно знать.$",
    "Route114_Text_AngelinaPostBattle": "Некоторые POKeMON после эволюции меняются\\nтак сильно, что даже удивляешься!$",
    "Route115_Text_TimothyIntro": "Хм...\\nВыглядишь довольно умелым...\\lПозволь составить тебе компанию!$",
    "Route115_Text_TimothyDefeat": "Ты намного сильнее, чем\\nя представлял!$",
    "Route115_Text_TimothyPostBattle": "Прирожденных гениев не бывает.\\nВсе зависит от усилий!\\lЯ в это верю...$",
    "Route115_Text_TimothyRegister": "Хм... Я уже давно не терпел\\nнастолько полного поражения.\\pЕсли позволишь, я хотел бы получить\\nеще один шанс на бой.$",
    "Route115_Text_TimothyRematchIntro": "Хм... Как всегда, твоя ловкость говорит\\nсама за себя.\\lНу же, составь мне компанию!$",
    "Route115_Text_TimothyRematchDefeat": "Все так же силен!$",
    "Route115_Text_TimothyPostRematch": "Все решают усилия!\\pЯ проиграл, потому что приложил недостаточно\\nстараний!$",
    "Route115_Text_KoichiIntro": "Ты!\\pМой MACHOP!\\pТребуем боя!$",
    "Route115_Text_KoichiDefeat": "Ай, ай, ай!$",
    "Route115_Text_KoichiPostBattle": "Моя команда MACHOP!\\pПока они стремятся к силе, я тоже буду\\nстановиться сильнее вместе с ними!$",
    "Route115_Text_NobIntro": "Лучше всего у меня получается разбивать кирпичи\\nлбом!$",
    "Route115_Text_NobDefeat": "Угва-а-а!\\nГолова раскалывается!$",
    "Route115_Text_NobPostBattle": "Я учил своих POKeMON карате.\\pПохоже, скоро они станут намного лучше\\nменя. И это радует!$",
    "Route115_Text_NobRegister": "Ты меня впечатлил! Дай мне реванш\\nпосле новых тренировок!$",
    "Route115_Text_NobRematchIntro": "После поражения от тебя мы упорно тренировались,\\nчтобы улучшить навыки.\\lДавай, устрой нам реванш!$",
    "Route115_Text_NobRematchDefeat": "Угва-а-а!\\nМы снова проиграли!$",
    "Route115_Text_NobPostRematch": "Мои POKeMON станут сильнее!\\nЯ удвою тренировки!$",
    "Route115_Text_CyndyIntro": "Этот пляж - мое секретное место тренировок!\\nНе мешай мне!$",
    "Route115_Text_CyndyDefeat": "Я еще недостаточно тренировалась!$",
    "Route115_Text_CyndyPostBattle": "Песок смягчает удары, уменьшая\\nнагрузку и риск травм.\\lИдеальное место для тренировок.$",
    "Route115_Text_CyndyRegister": "Ладно, можешь приходить сюда.\\nНо взамен хочу еще раз сразиться.$",
    "Route115_Text_CyndyRematchIntro": "Ну что, начинаем бой!$",
    "Route115_Text_CyndyRematchDefeat": "Я еще могу сражаться, но мой POKeMON...$",
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
        raise SystemExit("usage: localize_trainers_quality_route113b_115a_v3_183.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 100:
        raise RuntimeError(f"expected exactly 100 quality-pass blocks, got {len(TRANSLATIONS)}")
    for label, translated in TRANSLATIONS.items():
        replace_label(path, label, translated)

    out = root / "build" / "qarro_ru_trainers_quality_route113b_115a_v3_183_audit.json"
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
