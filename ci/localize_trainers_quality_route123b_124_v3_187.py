#!/usr/bin/env python3
"""Qarro v3.187: human-quality RU pass for trainer chunk 9 (blocks 800-899)."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
MARKER = "QARRO_RU_TRAINERS_QUALITY_ROUTE123B_124_V3_187"
TARGET = Path("data/text/trainers.inc")
TRANSLATIONS = {
    "Route123_Text_WendyPostBattle": "Даже меня удалось превзойти...\\nТвоя сила великолепна!$",
    "Route123_Text_BraxtonIntro": "Похоже, у тебя большая коллекция\\nЗНАЧКОВ ЗАЛОВ.\\pПроверим, действительно ли ты достоин\\nэтих ЗНАЧКОВ!$",
    "Route123_Text_BraxtonDefeat": "Да, ты их достоин!$",
    "Route123_Text_BraxtonPostBattle": "В этом бою ты доказал,\\nчто достоин своих ЗНАЧКОВ!$",
    "Route123_Text_VioletIntro": "Говорят, счастливые времена наполнены\\nприятными ароматами.$",
    "Route123_Text_VioletDefeat": "Ох...\\nЧувствую горький запах несчастья...$",
    "Route123_Text_VioletPostBattle": "Сад МАСТЕРА ЯГОД наполнен\\nбодрящими ароматами.$",
    "Route123_Text_CameronIntro": "Сила экстрасенса - это сила воли.\\pЯ заставил себя не проигрывать\\nникому. Вот что делает меня сильным!$",
    "Route123_Text_CameronDefeat": "Мне грустно...$",
    "Route123_Text_CameronPostBattle": "Сила экстрасенса - это сила воли.\\nЯ думал, тебе не проиграю...$",
    "Route123_Text_CameronRegister": "Я чувствую это!\\nМы еще обязательно сразимся!\\lПравда, не знаю, смогу ли победить...\\pПокажи свой POKeNAV.$",
    "Route123_Text_CameronRematchIntro": "Я убедил себя, что больше\\nне проиграю. Это делает меня сильнее!$",
    "Route123_Text_CameronRematchDefeat": "Мне грустно...$",
    "Route123_Text_CameronPostRematch": "Мне стоит потренироваться на ГОРЕ ПАЙР...\\nИначе мне тебя никогда не победить...$",
    "Route123_Text_JackiIntro": "Не спеши радоваться, если твои POKeMON\\nобрели психические силы.\\pЧтобы они действительно пригодились,\\nих нужно как следует развивать.$",
    "Route123_Text_JackiDefeat": "Меня сокрушили!$",
    "Route123_Text_JackiPostBattle": "Психические силы есть у всех.\\nМы просто забыли, как ими пользоваться.$",
    "Route123_Text_JackiRegister": "Я хотела бы снова сразиться с тобой.\\nТы не против?$",
    "Route123_Text_JackiRematchIntro": "Ты уже пробудил психические силы\\nвнутри себя?$",
    "Route123_Text_JackiRematchDefeat": "Поразительно!$",
    "Route123_Text_JackiPostRematch": "Твоя связь с POKeMON...\\nМожет, это тоже психическая сила.$",
    "Route123_Text_MiuIntro": "МИУ: Привет, тренер. Надеюсь, твои\\nPOKeMON не заплачут после поражения.$",
    "Route123_Text_MiuDefeat": "МИУ: Ой-ой, мы проиграли.$",
    "Route123_Text_MiuPostBattle": "МИУ: Тренер, твои POKeMON\\nсильны, потому что вы друзья.$",
    "Route123_Text_MiuNotEnoughMons": "МИУ: Сражаться неинтересно, если у тебя\\nнет двух POKeMON.$",
    "Route123_Text_YukiIntro": "ЮКИ: Ладно!\\nСейчас победим POKeMON тренера!$",
    "Route123_Text_YukiDefeat": "ЮКИ: Ой-ой, мы проиграли.$",
    "Route123_Text_YukiPostBattle": "ЮКИ: Почему ты такой сильный?\\nМы раньше никогда не проигрывали.$",
    "Route123_Text_YukiNotEnoughMons": "ЮКИ: Сражаться неинтересно, если у тебя\\nнет двух POKeMON.$",
    "Route123_Text_KindraIntro": "ГОРА ПАЙР...\\nМесто, где покоятся духи POKeMON...\\lУснут ли и твои POKeMON?$",
    "Route123_Text_KindraDefeat": "Столько жизненной силы...$",
    "Route123_Text_KindraPostBattle": "ГОРА ПАЙР...\\nМесто, где покоятся духи POKeMON...\\pНаверное, оно переполнено силой,\\nуспокаивающей духов...$",
    "Route123_Text_FernandoIntro": "Сейчас вырублю тебя,\\nпока отрываюсь под эту мелодию!$",
    "Route123_Text_FernandoDefeat": "Эй, погоди!\\nЯ еще только вступление играл!$",
    "Route123_Text_FernandoPostBattle": "Тебя ничем не проймешь.\\nХочу написать о тебе песню.$",
    "Route123_Text_FernandoRegister": "В следующий раз дослушай\\nмою песню до конца, ладно?$",
    "Route123_Text_FernandoRematchIntro": "Сегодня я точно сделаю это!\\nВырублю тебя прежде,\\lчем закончу свою песню!$",
    "Route123_Text_FernandoRematchDefeat": "Эй, погоди!\\nЯ еще даже до припева не дошел!$",
    "Route123_Text_FernandoPostRematch": "Я думал, ты так заслушаешься\\nмоей песней, что проиграешь.$",
    "Route123_Text_DavisIntro": "Вот мой крутой POKeMON-жук!\\nЕго подарил мне старший брат.$",
    "Route123_Text_DavisDefeat": "Уа-а-а!\\nНу ты и вредина!$",
    "Route123_Text_DavisPostBattle": "Только брату не говори, что я проиграл.\\nЭто должно остаться между нами!$",
    "Route123_Text_JazmynIntro": "Если я одолею кого-то явно сильного,\\nмоя уверенность вырастет!$",
    "Route123_Text_JazmynDefeat": "Вот и вся моя уверенность...$",
    "Route123_Text_JazmynPostBattle": "Говорят, нельзя судить человека\\nпо внешности.\\pНо иногда внешность все же не обманывает...$",
    "Route123_Text_FrederickIntro": "Привет, дитя!\\nУделишь мне немного времени?$",
    "Route123_Text_FrederickDefeat": "Ах, какой способный юный тренер!\\nПозволь немного пополнить твои карманные деньги.$",
    "Route123_Text_FrederickPostBattle": "Пополнить карманные деньги?\\nРазве призовых было мало?$",
    "Route123_Text_AlbertoIntro": "Скажу тебе честно: POKeMON-птицы\\nмоя настоящая страсть!\\pПтицы - это круто!\\nОни лучшие!$",
    "Route123_Text_AlbertoDefeat": "Даже проигрывая, POKeMON-птицы круты!$",
    "Route123_Text_AlbertoPostBattle": "Я собираю перья POKeMON-птиц,\\nкоторые разлетаются во время боя.\\pСделаю себе шляпу из\\nэтих перьев.$",
    "Route123_Text_EdIntro": "Когда тренеров поблизости нет,\\nя позволяю своим POKeMON сражаться друг с другом.\\lА сам наблюдаю.$",
    "Route123_Text_EdDefeat": "Мне вроде нравятся твои POKeMON.$",
    "Route123_Text_EdPostBattle": "Хе-хе, я позаимствую твои боевые идеи!\\nДумаю, они помогут мне стать лучше.$",
    "Route123_Text_JonasIntro": "Я сидел в засаде, и тренер\\nугодил прямо в мою ловушку!$",
    "Route123_Text_JonasDefeat": "Если ты не проигрываешь, как мне тогда\\nвеселиться, играя в ниндзя?$",
    "Route123_Text_JonasPostBattle": "В следующий раз устрою засаду тренеру,\\nкоторый выглядит послабее.$",
    "Route123_Text_KayleyIntro": "Я только что купила этот зонтик.\\nТеперь моя миловидность выросла на треть!$",
    "Route123_Text_KayleyDefeat": "Ты лучше меня примерно\\nраз в пять!$",
    "Route123_Text_KayleyPostBattle": "Умело подбирать аксессуары -\\nвот секрет стильного образа.$",
    "Route124_Text_SpencerIntro": "Эй, ты заблудился в море?\\pЕсли победишь моих POKeMON,\\nя стану твоим проводником.$",
    "Route124_Text_SpencerDefeat": "В бою я совсем потерял ориентиры!$",
    "Route124_Text_SpencerPostBattle": "В море многие теряют направление.\\pЕсли это про тебя, смотри\\nКАРТУ в POKeNAV.$",
    "Route124_Text_RolandIntro": "Хм! Ты едешь на POKeMON вместо\\nтого, чтобы плыть самому...\\pЗавидую!$",
    "Route124_Text_RolandDefeat": "Ох!\\nНе могу...$",
    "Route124_Text_RolandPostBattle": "Я совсем замерз...\\nСлишком долго пробыл в воде...\\pВот бы и мне кататься на POKeMON, как ты...$",
    "Route124_Text_JennyIntro": "Если просто дрейфовать по морю,\\nPOKeMON сами приплывают поиграть.$",
    "Route124_Text_JennyDefeat": "Вот досада.\\nЯ все-таки проиграла.$",
    "Route124_Text_JennyPostBattle": "Пока плавала, заметила: некоторые\\nPOKeMON нападают, а другие лишь смотрят.\\pПохоже, у каждого POKeMON свой\\nхарактер.$",
    "Route124_Text_JennyRegister": "Просто прихоть, но, может,\\nзапишешь меня в свой POKeNAV?$",
    "Route124_Text_JennyRematchIntro": "Если просто плавать в море вот так,\\nтренеры сами бросают вызов!$",
    "Route124_Text_JennyRematchDefeat": "Странно...\\nЯ снова проиграла...$",
    "Route124_Text_JennyPostRematch": "К делу это отношения не имеет,\\nно, может, схожу в ДОМ ХИТРОСТЕЙ.$",
    "Route124_Text_GraceIntro": "Мне уже надоело плавать...\\nКак насчет боя?$",
    "Route124_Text_GraceDefeat": "Понятия не имела, что ты\\nнастолько силен!$",
    "Route124_Text_GracePostBattle": "Наверняка именно все твои старания\\nсделали тебя таким сильным.$",
    "Route124_Text_ChadIntro": "Фуфуфу... Я ныряю глубоко под воду,\\nчтобы скрыться еще глубже.\\lИсследовать глубины - вот мой конек!$",
    "Route124_Text_ChadDefeat": "Буль-буль-буль...\\nЯ тону...$",
    "Route124_Text_ChadPostBattle": "Из надежного источника знаю,\\nчто где-то рядом есть место для DIVE.\\pТак и тянет снова уйти\\nна глубину...$",
    "Route124_Text_LilaIntro": "ЛИЛА: Вздох...\\pВот я в море, и кто рядом со мной?\\nМой младший брат!\\pДавай сразимся, чтобы я хотя бы\\nне думала об этом!$",
    "Route124_Text_LilaDefeat": "ЛИЛА: РОЙ! Мы проиграли из-за тебя!\\nПозже я с тобой разберусь!$",
    "Route124_Text_LilaPostBattle": "ЛИЛА: Вздох...\\pВот бы рядом со мной был не младший брат,\\nа хороший парень...$",
    "Route124_Text_LilaNotEnoughMons": "ЛИЛА: Хочешь сразиться с нами?\\nТогда у тебя должно быть два POKeMON.$",
    "Route124_Text_RoyIntro": "РОЙ: Моя старшая сестра отлично сражается с POKeMON!\\pНе плачь, когда проиграешь!$",
    "Route124_Text_RoyDefeat": "РОЙ: Ой-ой...\\nСестра меня отругает...$",
    "Route124_Text_RoyPostBattle": "РОЙ: Моя старшая сестра очень страшная,\\nкогда злится.\\pВот поэтому у нее и нет\\nпарня.$",
    "Route124_Text_LilaRoyRegister": "РОЙ: Еще раз с нами сразишься?\\nТолько в следующий раз полегче, ладно?$",
    "Route124_Text_RoyNotEnoughMons": "РОЙ: Хочешь с нами сразиться?\\nТогда приводи двух POKeMON.$",
    "Route124_Text_LilaRematchIntro": "ЛИЛА: Вздох...\\pВот я в море, и кто рядом со мной?\\nМой младший брат!\\pО, привет, давно не виделись. Давай сразимся,\\nчтобы я не думала о всяком!$",
    "Route124_Text_LilaRematchDefeat": "ЛИЛА: РОЙ!\\nМы снова проиграли из-за тебя!\\pПозже будет тренировка!$",
    "Route124_Text_LilaPostRematch": "ЛИЛА: Вздох...\\pБудь у меня хороший парень, мы бы вместе\\nпобеждали всех красивыми комбинациями...$",
    "Route124_Text_LilaRematchNotEnoughMons": "ЛИЛА: Хочешь сразиться с нами?\\nТогда у тебя должно быть два POKeMON.$",
    "Route124_Text_RoyRematchIntro": "РОЙ: Если проиграем, мне попадет.\\nТак что я выложусь на полную!$",
    "Route124_Text_RoyRematchDefeat": "РОЙ: Ой-ой...\\nСестра снова меня отругает.$",
    "Route124_Text_RoyPostRematch": "РОЙ: Моя старшая сестра очень страшная,\\nкогда злится.\\pПозже она заставит меня очень\\nусердно тренироваться с POKeMON...$",
    "Route124_Text_RoyRematchNotEnoughMons": "РОЙ: Хочешь с нами сразиться?\\nТогда приводи двух POKeMON.$",
    "Route124_Text_DeclanIntro": "Вот я плыву совсем один\\nпо этому огромному прекрасному морю.\\pДругого слова нет.\\nЭто жалко!$",
    "Route124_Text_DeclanDefeat": "Мне совсем тоскливо.\\nНа душе сине, как небо...$",
    "Route124_Text_DeclanPostBattle": "Надо бы разговорить девушек-пловчих\\nи позвать их на долгий заплыв.$",
    "Route124_Text_IsabellaIntro": "Я не проиграю какому-то\\nтренеру-серферу.$",
}
BANNED_UNICODE = set("—–←→“”«»")
def control_tokens(text: str) -> list[str]:
    return re.findall(r'\{[^}]+\}|\\.|\$', text)
def replace_label(path: Path, label: str, translated: str) -> None:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(rf'(?ms)^(?P<head>{re.escape(label)}:\s*\n)(?P<body>(?:[ \t]*\.string\s+"(?:\\.|[^"\\])*"\s*\n?)+)')
    matches=list(pat.finditer(text))
    if len(matches)!=1: raise RuntimeError(f"{path}:{label}: expected one text block, got {len(matches)}")
    m=matches[0]
    current="".join(re.findall(r'\.string\s+"((?:\\.|[^"\\])*)"',m.group("body")))
    if control_tokens(current)!=control_tokens(translated): raise RuntimeError(f"{path}:{label}: control-token drift")
    if not translated.endswith("$"): raise RuntimeError(f"{path}:{label}: missing terminal $")
    if set(translated)&BANNED_UNICODE: raise RuntimeError(f"{path}:{label}: unsupported punctuation")
    if '"' in translated: raise RuntimeError(f"{path}:{label}: raw quote")
    path.write_text(text[:m.start("body")]+'\t.string "'+translated+'"\n'+text[m.end("body"):],encoding="utf-8")
def main()->int:
    if len(sys.argv)!=2: raise SystemExit("usage: localize_trainers_quality_route123b_124_v3_187.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=100: raise RuntimeError(f"expected 100 blocks, got {len(TRANSLATIONS)}")
    for label,translated in TRANSLATIONS.items(): replace_label(path,label,translated)
    out=root/"build"/"qarro_ru_trainers_quality_route123b_124_v3_187_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"targetFile":str(TARGET),"qualityPassBlocks":len(TRANSLATIONS),"labels":list(TRANSLATIONS),"humanEditedRussian":True,"controlTokensPreserved":True,"pokemonMoveAbilityNamesPreserved":True,"gameplayLogicTouched":False,"balanceTouched":False,"bossTeamsTouched":False,"specialWhitelistTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} trainer text blocks in {TARGET}"); return 0
if __name__=="__main__": raise SystemExit(main())
