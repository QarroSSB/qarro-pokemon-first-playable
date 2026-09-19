#!/usr/bin/env python3
"""Qarro v3.185: human-quality RU pass for trainer chunk 7.

Covers the next contiguous 100 machine-translated blocks in trainers.inc:
the rest of Route 117, Route 118 and the opening of Route 119.
Localization-only; exact runtime control-token sequences are preserved and
source drift fails closed. Pokemon, Move and Ability proper names stay English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINERS_QUALITY_ROUTE117B_119A_V3_185"
TARGET = Path("data/text/trainers.inc")

TRANSLATIONS = {
    "Route117_Text_AnnaRematchDefeat": "АННА: Не смогла поймать ритм.$",
    "Route117_Text_AnnaPostRematch": "АННА: У твоих POKeMON отличные\\nсочетания.\\pПожалуй, вы уступаете только нам!$",
    "Route117_Text_AnnaRematchNotEnoughMons": "АННА: Хочешь сразиться с нами -\\nвозьми с собой двух POKeMON.$",
    "Route117_Text_MegRematchIntro": "МЭГ: Я объединюсь со своей\\nстаршей напарницей и на этот раз победю!$",
    "Route117_Text_MegRematchDefeat": "МЭГ: Слишком сильно!$",
    "Route117_Text_MegPostRematch": "МЭГ: Я сражалась вместе со своей\\nстаршей напарницей, но мы проиграли...\\pКак же обидно...$",
    "Route117_Text_MegRematchNotEnoughMons": "МЭГ: У тебя только один POKeMON?\\nТогда мы не можем сражаться.\\pМы хотим бой два на два.$",
    "Route117_Text_MelinaIntro": "Разве не приятно сражаться, любуясь\\nкрасивыми цветами?$",
    "Route117_Text_MelinaDefeat": "О, впечатляет!$",
    "Route117_Text_MelinaPostBattle": "Как же приятно бегать трусцой\\nи любоваться цветами.$",
    "Route117_Text_BrandiIntro": "Позволь показать силу,\\nскрытую в POKeMON психического типа!$",
    "Route117_Text_BrandiDefeat": "Поразительно!$",
    "Route117_Text_BrandiPostBattle": "POKeMON психического типа очень сложные.\\nПопробуй поймать такого.$",
    "Route117_Text_AishaIntro": "Сосредоточься только на победе.\\nВот как я сражаюсь!$",
    "Route117_Text_AishaDefeat": "Я не трачу время на злость\\nиз-за поражения - лучше тренироваться.$",
    "Route117_Text_AishaPostBattle": "Мне кажется, чем больше боишься проиграть,\\nтем вероятнее поражение.$",
    "Route118_Text_RoseIntro": "Аромат цветов обладает волшебной\\nсилой. Он очищает тело и душу.$",
    "Route118_Text_RoseDefeat": "Ох, надо же.\\nКажется, я проиграла.$",
    "Route118_Text_RosePostBattle": "Цветы, POKeMON...\\nЛюблю все, что приятно пахнет.\\pА вот вонючие вещи...\\nНет уж, спасибо.$",
    "Route118_Text_RoseRegister": "Хм... Этот запах - POKeNAV!\\nМы просто обязаны записать друг друга!$",
    "Route118_Text_RoseRematchIntro": "Тебя привел сюда сладкий\\nаромат?$",
    "Route118_Text_RoseRematchDefeat": "Сила аромата...\\nПохоже, в этот раз не помогла.$",
    "Route118_Text_RosePostRematch": "Если правильно использовать сладкий аромат,\\nон привлечет POKeMON.$",
    "Route118_Text_PerryIntro": "POKeMON-птицы, которые элегантно FLY в\\nнебе... Они лучшие!$",
    "Route118_Text_PerryDefeat": "Ургх...\\nЯ разбился...$",
    "Route118_Text_PerryPostBattle": "У тебя отличные POKeMON.\\nПридется тренировать своих усерднее.$",
    "Route118_Text_ChesterIntro": "Взлетайте!\\nМои POKeMON-птицы!$",
    "Route118_Text_ChesterDefeat": "Ну вот, они и правда улетели...$",
    "Route118_Text_ChesterPostBattle": "Если станут сильнее, смогут\\nлетать еще свободнее...$",
    "Route118_Text_BarnyIntro": "Я рыбак, но еще и тренер.\\nЯ выращиваю POKeMON, которых поймал.$",
    "Route118_Text_BarnyDefeat": "Я думал, мои тренировки идут\\nнеплохо...$",
    "Route118_Text_BarnyPostBattle": "Не получилось победить, тренируя POKeMON\\nмежду рыбалкой...\\pМожет, я все делал вполсилы?$",
    "Route118_Text_WadeIntro": "Для рыбака главное - снаряжение.\\pА для тренера главное, конечно,\\nPOKeMON и сердце!$",
    "Route118_Text_WadeDefeat": "Меня победили силой духа?$",
    "Route118_Text_WadePostBattle": "Если подумать, рыбалка - это бой\\nмежду рыбаком и POKeMON.$",
    "Route118_Text_DaltonIntro": "Пусть моя мелодия раскачает твою душу!$",
    "Route118_Text_DaltonDefeat": "Ла-лалала...$",
    "Route118_Text_DaltonPostBattle": "Электрогитара вовсе не обязана\\nвсегда быть громкой...\\pНа ней можно сыграть и\\nтакую трогательную мелодию...$",
    "Route118_Text_DaltonRegister": "Когда сочиню мелодию получше,\\nобязательно приходи послушать, ладно?$",
    "Route118_Text_DaltonRematchIntro": "Мелодия моих POKeMON и меня...\\nПусть она достигнет твоей души.$",
    "Route118_Text_DaltonRematchDefeat": "Ла-лалала...$",
    "Route118_Text_DaltonPostRematch": "Когда я играю, мои чувства должны доходить\\nдо тебя через электрогитару...$",
    "Route118_Text_DeandreIntro": "Вперед, вперед, вперед!\\nPOKeMON номер один, два и три!$",
    "Route118_Text_DeandreDefeat": "Эй, POKeMON! Вы в порядке?\\nНомер один, два и три?!$",
    "Route118_Text_DeandrePostBattle": "Круто, правда? У меня целая боевая\\nкоманда POKeMON!\\pМожешь скопировать - я не против!$",
    "Route119_Text_BrentIntro": "Мы КРУГ MIMIC!\\nМы MIMIC каждое твое движение!$",
    "Route119_Text_BrentDefeat": "Упс!\\nЯ проиграл!$",
    "Route119_Text_BrentPostBattle": "Что хорошего в подражании?\\pФуфуфу...\\nТебе этого никогда не понять...$",
    "Route119_Text_DonaldIntro": "Наконец-то мы встретились!\\nМои POKeMON-жуки составят тебе компанию!$",
    "Route119_Text_DonaldDefeat": "Лучше бы мы не встречались...$",
    "Route119_Text_DonaldPostBattle": "Хочу еще немного MIMIC тебя.\\nМожешь уже куда-нибудь пойти?$",
    "Route119_Text_TaylorIntro": "Шагнешь вперед - мы шагнем вперед.\\pПовернешь направо - мы тоже...$",
    "Route119_Text_TaylorDefeat": "Но если ты побеждаешь, я проигрываю...$",
    "Route119_Text_TaylorPostBattle": "Я не могу MIMIC твою победу.\\nЭто просто невозможно...\\lКак же меня это бесит...$",
    "Route119_Text_DougIntro": "Ага, наконец-то ты меня поймал!\\nИли пытался избежать?$",
    "Route119_Text_DougDefeat": "Ух, отличный был бой!$",
    "Route119_Text_DougPostBattle": "Мы КРУГ MIMIC!\\nНадеюсь, представление понравилось.$",
    "Route119_Text_GregIntro": "Ты не знаешь, кто я, верно?\\pНо и я тебя не знаю.\\nЗначит, сражаемся!$",
    "Route119_Text_GregDefeat": "Ты довольно силен!$",
    "Route119_Text_GregPostBattle": "Пока ты отсюда не уйдешь, мы будем\\nповторять каждое твое движение.$",
    "Route119_Text_KentIntro": "КРУГ MIMIC создали люди,\\nкоторые любят MIMIC.\\pСтоит нам встретиться - сразу начинается бой!$",
    "Route119_Text_KentDefeat": "Сдаюсь!$",
    "Route119_Text_KentPostBattle": "Не хочешь вступить в наш КРУГ MIMIC?$",
    "Route119_Text_JacksonIntro": "Кто знает все приемы\\nвыживания в дикой природе?\\pРЕЙНДЖЕРЫ POKeMON, вот кто!$",
    "Route119_Text_JacksonDefeat": "Мне не хватило знаний\\nо POKeMON...$",
    "Route119_Text_JacksonPostBattle": "Оставить цивилизацию позади и\\nпробудить свой дикий дух!\\pВот наша цель.$",
    "Route119_Text_JacksonRegister": "Надеюсь, дашь мне реванш, не\\nсмеясь над моими пробелами в знаниях.$",
    "Route119_Text_JacksonRematchIntro": "Я возвращаю свой дикий дух,\\nпроводя время вместе с POKeMON.$",
    "Route119_Text_JacksonRematchDefeat": "Ты все так же силен!$",
    "Route119_Text_JacksonPostRematch": "Верь своим POKeMON.\\nВерь в себя.\\pТогда путь откроется сам.$",
    "Route119_Text_CatherineIntro": "О? Посмотри на себя.\\pДля путешественника\\nу тебя удивительно мало вещей.$",
    "Route119_Text_CatherineDefeat": "Несчастья случаются, когда ты\\nне подготовлен!$",
    "Route119_Text_CatherinePostBattle": "Ты путешествуешь налегке, но у тебя есть\\nвсе необходимое.\\pИ морально, и физически\\nты отлично подготовлен.$",
    "Route119_Text_CatherineRegister": "У тебя есть POKeNAV?\\nДля тренера это незаменимая вещь.\\pО, он у тебя есть!\\nТогда давай запишем друг друга!$",
    "Route119_Text_CatherineRematchIntro": "Как проходит твое путешествие с POKeMON\\nвместе?$",
    "Route119_Text_CatherineRematchDefeat": "Мне все еще чего-то не хватает...$",
    "Route119_Text_CatherinePostRematch": "Так же как тренер полагается на\\nсвоих POKeMON, твои POKeMON\\lполагаются на тебя.$",
    "Route119_Text_HughIntro": "Бескрайнее небо таит безграничные возможности!\\pНичто не сравнится с чистым\\nвосторгом полета!$",
    "Route119_Text_HughDefeat": "Разбит наголову!$",
    "Route119_Text_HughPostBattle": "Мои POKeMON-птицы воплотили мечту\\nо полете в реальность!$",
    "Route119_Text_PhilIntro": "Я покажу истинный потенциал мой\\nи моих POKeMON-птиц!$",
    "Route119_Text_PhilDefeat": "Нам не хватило потенциала...$",
    "Route119_Text_PhilPostBattle": "С самого детства я всегда\\nвосхищался POKeMON-птицами...$",
    "Route119_Text_YasuIntro": "Прятаться в тенях и жить во\\nтьме... Такова моя судьба.\\pЯ выхожу, чтобы бросить тебе вызов!$",
    "Route119_Text_YasuDefeat": "Признаю поражение!$",
    "Route119_Text_YasuPostBattle": "Побежденный в бою должен тихо\\nвернуться обратно в тени.\\lТакова и эта судьба...$",
    "Route119_Text_TakashiIntro": "Если потеряешь бдительность,\\nбудет больно!$",
    "Route119_Text_TakashiDefeat": "Ты на удивление хорош!$",
    "Route119_Text_TakashiPostBattle": "Моя внезапная атака закончилась\\nпровалом...$",
    "Route119_Text_HideoIntro": "Хочешь спрятать дерево - используй лес!$",
    "Route119_Text_HideoDefeat": "Склоняюсь перед твоим превосходством.$",
    "Route119_Text_HideoPostBattle": "Хочешь спрятать дерево - используй лес!\\nХочешь спрятать POKeMON - используй POKeMON!\\pНикакого глубокого скрытого смысла\\nздесь нет.$",
    "Route119_Text_ChrisIntro": "Ты заговорил со мной...\\nЗначит, хочешь бросить вызов!\\pЛадно! Проверю POKeMON, которых поймал\\nво время SURF!$",
    "Route119_Text_ChrisDefeat": "Я понятия не имею, что\\nнужно для победы.$",
    "Route119_Text_ChrisPostBattle": "Отправиться на SURF на своем POKeMON...\\pА потом рыбачить прямо с его спины...\\pНепередаваемое удовольствие!$",
    "Route119_Text_FabianIntro": "Ударь мощным аккордом!\\nПобеда будет моей!\\lНаш час настал, уоу, да!$",
    "Route119_Text_FabianDefeat": "Ты показал, кто здесь главный!\\nПридется принять поражение, о нет!$",
    "Route119_Text_FabianPostBattle": "Ударь еще одним мощным аккордом!\\nОставь меня в покое!\\lЗа эту победу придется ответить!$",
    "Route119_Text_DaytonIntro": "Хо-хо-хо!\\nЛюблю юных тренеров!\\lДавай устроим отличный бой!$",
    "Route119_Text_DaytonDefeat": "Ты просто потрясающий!\\nХо-хо-хо!$",
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
        raise SystemExit("usage: localize_trainers_quality_route117b_119a_v3_185.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 100:
        raise RuntimeError(f"expected exactly 100 quality-pass blocks, got {len(TRANSLATIONS)}")
    for label, translated in TRANSLATIONS.items():
        replace_label(path, label, translated)

    out = root / "build" / "qarro_ru_trainers_quality_route117b_119a_v3_185_audit.json"
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
