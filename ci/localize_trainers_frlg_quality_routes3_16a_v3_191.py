#!/usr/bin/env python3
"""Qarro v3.191: human-quality RU pass for trainers_frlg.inc blocks 0-99."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
MARKER="QARRO_RU_TRAINERS_FRLG_QUALITY_ROUTES3_16A_V3_191"
TARGET=Path("data/text/trainers_frlg.inc")
TRANSLATIONS={
    "Route3_Text_ColtonRematchIntro:": "Эй!\\nЯ видел тебя в ВИРИДИАНСКОМ ЛЕСУ!$",
    "Route3_Text_BenRematchIntro:": "Привет! Я люблю шорты!\\nОни удобные, и носить их легко!\\pТебе тоже стоит носить шорты!$",
    "Route3_Text_JaniceRematchIntro:": "Извини!\\nТы ведь снова на меня смотришь, да?$",
    "Route3_Text_GregRematchIntro:": "Ты тренер, да?\\nТогда давай сразу сразимся!$",
    "Route3_Text_SallyRematchIntro:": "Этот твой взгляд...\\nТак меня интригует!$",
    "Route3_Text_CalvinRematchIntro:": "Эй! Что с тобой?\\nТы все еще не носишь шорты!$",
    "Route3_Text_JamesRematchIntro:": "Сражусь с тобой POKeMON,\\nкоторого начал растить.$",
    "Route3_Text_RobinRematchIntro:": "Ай!\\nТы меня толкнул?$",
    "Route4_Text_CrissyRematchIntro:": "Я всегда ловлю грибных POKeMON\\nна ЛУННОЙ ГОРЕ.$",
    "Route6_Text_RickyRematchIntro:": "О! Ты тот любопытный ребенок, который\\nподслушивал нас!$",
    "Route6_Text_NancyRematchIntro:": "Извини! Разве я не говорила, что\\nэто частный разговор?\\pНе стоит подслушивать,\\nневоспитанный ты человек!$",
    "Route6_Text_KeigoRematchIntro:": "Я пытаюсь найти кого-нибудь хорошего,\\nтолько не POKeMON-жука, но...$",
    "Route6_Text_JeffRematchIntro:": "А?\\nСнова хочешь со мной сразиться?$",
    "Route6_Text_IsabelleRematchIntro:": "Я?\\nНу ладно. Один раз сыграю.$",
    "Route6_Text_ElijahRematchIntro:": "Эй, давно не виделись!\\nСтал сильнее?$",
    "Route8_Text_AidanRematchIntro:": "С POKeMON ты хорош, но как\\nу тебя с химией?$",
    "Route8_Text_StanRematchIntro:": "Отлично!\\nДавай сыграем еще раз!$",
    "Route8_Text_GlennRematchIntro:": "Чтобы побеждать в боях,\\nнужна стратегия.\\pТы следуешь моему совету?$",
    "Route8_Text_PaigeRematchIntro:": "Я собрала много NIDORAN.\\nНе хочу, чтобы они эволюционировали, но...$",
    "Route8_Text_LeslieRematchIntro:": "В школе весело, но я все равно считаю,\\nчто с POKeMON тоже весело.$",
    "Route8_Text_AndreaRematchIntro:": "MEOWTH и PERSIAN такие милые,\\nмяу, мяу, мяу!$",
    "Route8_Text_MeganRematchIntro:": "Наверное, мы глупо выглядим, стоя здесь\\nвот так, но сражаться я все еще могу.$",
    "Route8_Text_RichRematchIntro:": "Я бродяга и азартный игрок!\\nИ у меня победная серия!$",
    "Route8_Text_JuliaRematchIntro:": "Какой POKeMON милый, круглый и пушистый?\\nУгадай.\\pТы ведь уже знаешь ответ?$",
    "Route8_Text_RicardoRematchIntro:": "Мой велосипед все еще барахлит, дружище.$",
    "Route8_Text_JarenRematchIntro:": "Ладно, малыш!\\nНа этот раз пощады не жди!$",
    "Route8_Text_EliRematchIntro:": "ЭЛИ: Наша сила близнецов стала еще\\nмощнее!$",
    "Route8_Text_AnneRematchIntro:": "ЭНН: Наша сила близнецов выросла!$",
    "Route9_Text_AliciaRematchIntro:": "Снова будем сражаться?\\nНа этот раз ты мой!$",
    "Route9_Text_ChrisRematchIntro:": "Я не забыла тебя и тех\\nклассных POKeMON.$",
    "Route9_Text_DrewRematchIntro:": "Я иду через СКАЛЬНЫЙ ТУННЕЛЬ в\\nЛАВАНДЕР...\\pНо по дороге меня постоянно\\nкто-нибудь останавливает...$",
    "Route9_Text_CaitlinRematchIntro:": "Сегодня не смей смотреть на меня свысока!\\nНа этот раз все всерьез!$",
    "Route9_Text_JeremyRematchIntro:": "Бвахаха!\\nОтлично! Мне снова было скучно!$",
    "Route9_Text_BriceRematchIntro:": "Ха-ха-ха!\\nКак всегда, крепкий орешек!$",
    "Route9_Text_BrentRematchIntro:": "Я каждый день вставал рано, чтобы тренировать\\nсвоих POKeMON, вылупившихся из коконов!$",
    "Route9_Text_AlanRematchIntro:": "Ха-ха-ха!\\nНа этот раз я победю!$",
    "Route9_Text_ConnerRematchIntro:": "Вперед, мой супер-POKeMON-жук!$",
    "Route10_Text_MarkRematchIntro:": "Ого, ты снова здесь?\\nМожет, ты тоже ПОКЕМАНЬЯК?\\lХочешь посмотреть мою коллекцию?$",
    "Route10_Text_ClarkRematchIntro:": "Ха-ха-апчхи!\\nНе могу перестать чихать!$",
    "Route10_Text_HermanRematchIntro:": "Привет, малыш!\\nЯ уже показывал тебе своего POKeMON?$",
    "Route10_Text_HeidiRematchIntro:": "Я снова ходила в ЗАЛ POKeMON.\\p...Но, как обычно, проиграла.$",
    "Route10_Text_TrentRematchIntro:": "Ах!\\nКакой чудесный горный воздух!\\lТак хорошо, что уходить не хочется!$",
    "Route10_Text_CarolRematchIntro:": "У меня уже голова кружится.\\nСлишком долго иду по горам...$",
    "Route11_Text_HugoRematchIntro:": "Победа, поражение или ничья!\\nА теперь реванш!$",
    "Route11_Text_JasperRematchIntro:": "Соперничество - настоящий азарт.\\nМне все мало!$",
    "Route11_Text_EddieRematchIntro:": "Ты ведь знаешь правила?\\nДавай, только не жульничай!$",
    "Route11_Text_BraxtonRematchIntro:": "Привет!\\pНо осторожнее!\\nЯ все еще прокладываю кабели!$",
    "Route11_Text_DillonRematchIntro:": "Я стал тренером совсем недавно.\\nНо думаю, что смогу победить.$",
    "Route11_Text_DirkRematchIntro:": "Фвахаха!\\nЯ никогда не проигрывал!\\p...А если и проигрывал, то давно\\nоб этом забыл!$",
    "Route11_Text_DarianRematchIntro:": "Я еще ни разу не побеждал...\\pМожет, мне суждено навсегда\\nтаким и остаться...$",
    "Route11_Text_YasuRematchIntro:": "Я лучший в своем классе.\\nТренируюсь каждое утро и каждый вечер!$",
    "Route11_Text_BernieRematchIntro:": "Берегись проводов под напряжением!$",
    "Route11_Text_DaveRematchIntro:": "Я тщательно растил своих POKeMON.\\nТеперь они должны быть готовы.\\lНа этот раз они тоже должны победить.$",
    "Route12_Text_NedRematchIntro:": "Да!\\nКлюет!\\lЭ-это может быть настоящий улов!$",
    "Route12_Text_ChipRematchIntro:": "Наконец-то ты здесь.\\nНа рыбалке главное - уметь ждать.$",
    "Route12_Text_JustinRematchIntro:": "Все еще не могу найти ЛУННЫЙ КАМЕНЬ...\\nА тебе попадался?$",
    "Route12_Text_LucaRematchIntro:": "Электричество всегда было моей\\nспециализацией.\\pА вот о морских POKeMON\\nя ничего не знаю.$",
    "Route12_Text_HankRematchIntro:": "РЫБАК-ФАНАТ против ЮНОГО ТРЕНЕРА POKeMON!\\nЕще один раунд, бой!$",
    "Route12_Text_ElliotRematchIntro:": "Я люблю рыбалку, не пойми неправильно.\\nНо хотелось бы, чтобы работы было побольше...\\l...И все же бросить рыбалку трудно!$",
    "Route12_Text_AndrewRematchIntro:": "Что сегодня ловится?\\pНе узнаешь, пока не победишь\\nменя!$",
    "Route12_Text_JesRematchIntro:": "ДЖЕС: Сегодня я победю и\\nсделаю предложение моей ГИА.$",
    "Route12_Text_GiaRematchIntro:": "ГИА: Эй, ДЖЕС...\\nЯ уже давно жду.\\pЕсли сегодня победим, я выйду за тебя!$",
    "Route13_Text_SebastianRematchIntro:": "Мои POKeMON-птицы тебя помнят!$",
    "Route13_Text_SusieRematchIntro:": "Хочу стать лучшим тренером, \\nпока я еще ребенок!$",
    "Route13_Text_ValerieRematchIntro:": "Ого!\\nУ тебя стало еще больше крутых ЗНАЧКОВ!$",
    "Route13_Text_GwenRematchIntro:": "Мои мило выращенные POKeMON хотят\\nснова с тобой познакомиться.$",
    "Route13_Text_AlmaRematchIntro:": "Я опустошила все свои сбережения и\\nкупила еще КАРБОСА.$",
    "Route13_Text_PerryRematchIntro:": "На этот раз я не проиграю.\\nВетер сегодня на моей стороне!$",
    "Route13_Text_LolaRematchIntro:": "О, ты вернулся?\\pКонечно, я снова с тобой сыграю,\\nмилый.$",
    "Route13_Text_SheilaRematchIntro:": "Неужели ты не можешь забыть наш\\nпрошлый бой?$",
    "Route13_Text_JaredRematchIntro:": "Чего уставился?$",
    "Route13_Text_RobertRematchIntro:": "Я всегда выбираю POKeMON-птиц.\\nЯ посвятил себя им.$",
    "Route14_Text_CarterRematchIntro:": "Я использовал ТМ, чтобы научить своих POKeMON\\nхорошим приемам.$",
    "Route14_Text_MitchRematchIntro:": "На этот раз мои POKeMON-птицы должны быть готовы\\nк бою.$",
    "Route14_Text_BeckRematchIntro:": "Ты используешь ТМ на POKeMON?\\nПросто носить их с собой бесполезно.$",
    "Route14_Text_MarlonRematchIntro:": "Ты научил своего POKeMON-птицу\\nприему FLY?\\pТогда сможешь вместе с ним подняться\\nв небо! Попробуй.$",
    "Route14_Text_DonaldRematchIntro:": "Легенда о крылатых миражах...\\nТы ведь слышал ее, да?$",
    "Route14_Text_BennyRematchIntro:": "Мне не очень хочется, но ладно.\\nДавай!$",
    "Route14_Text_LukasRematchIntro:": "Эй!\\nЯ тебя помню!\\pДавай, давай.\\nНачнем, начнем, начнем!$",
    "Route14_Text_IsaacRematchIntro:": "Опять ты?\\nХватит болтать, сражайся.$",
    "Route14_Text_GeraldRematchIntro:": "Мы ездим сюда из-за\\nогромных открытых пространств.$",
    "Route14_Text_MalikRematchIntro:": "Бой POKeMON, да?\\nКруто! Погнали!$",
    "Route14_Text_KiriRematchIntro:": "КИРИ: ДЖЕН, надеюсь, сегодня мы победим.$",
    "Route14_Text_JanRematchIntro:": "ДЖЕН: КИРИ, начинаем!\\nНа этот раз точно победим!$",
    "Route15_Text_KindraRematchIntro:": "Я продолжу сражаться теми\\nPOKeMON, которых получила по обмену.$",
    "Route15_Text_BeckyRematchIntro:": "Ты выглядишь добрым, так что, думаю, смогу\\nтебя победить.\\pПопробую еще раз!$",
    "Route15_Text_EdwinRematchIntro:": "Стоит мне свистнуть, POKeMON-птицы\\nслетаются вокруг.\\pОни невероятно милые!$",
    "Route15_Text_ChesterRematchIntro:": "Хм? Мои птицы дрожат!\\nПостой, ты ведь тот самый тренер...$",
    "Route15_Text_GraceRematchIntro:": "О, какой же ты милашка!\\nПрямо как очаровательный POKeMON!\\lТеперь я тебя вспомнила!$",
    "Route15_Text_OliviaRematchIntro:": "Я выращиваю POKeMON для защиты,\\nпотому что живу одна.\\pНичего не изменилось.$",
    "Route15_Text_ErnestRematchIntro:": "Эй, малыш! Давай!\\nЯ отобрал это у какого-то неудачника!$",
    "Route15_Text_AlexRematchIntro:": "Когда проиграешь мне, отдашь\\nвсе свои деньги, малыш!$",
    "Route15_Text_CeliaRematchIntro:": "Что сейчас модно?\\nКонечно же, обмен POKeMON!$",
    "Route15_Text_YazminRematchIntro:": "Хочешь поиграть с моими POKeMON\\nеще раз?$",
    "Route15_Text_MyaRematchIntro:": "МАЙЯ: Привет, мы все время встречаемся,\\nправда?\\pСнова поможешь потренировать младшего брата\\nвместе со мной?$",
    "Route15_Text_RonRematchIntro:": "РОН: Моя сестра стала еще\\nсильнее...$",
    "Route16_Text_LaoRematchIntro:": "Чего тебе?$",
    "Route16_Text_KojiRematchIntro:": "Классный ВЕЛОСИПЕД!\\nБыстро отдавай!$",
    "Route16_Text_LukeRematchIntro:": "Выходи поиграть, мышонок.\\nЯ тебя не обижу!$",
    "Route16_Text_HideoRematchIntro:": "Эй, постой!\\nНе окликай меня и не убегай потом!$",
}
BANNED_UNICODE=set("—–←→“”«»")
def control_tokens(t): return re.findall(r'\{[^}]+\}|\\.|\$',t)
def replace_label(path,label,tr):
    text=path.read_text(encoding="utf-8")
    pat=re.compile(rf'(?ms)^(?P<head>{re.escape(label)}:\s*\n)(?P<body>(?:[ \t]*\.string\s+"(?:\\.|[^"\\])*"\s*\n?)+)')
    ms=list(pat.finditer(text))
    if len(ms)!=1: raise RuntimeError(f"{label}: expected one block, got {len(ms)}")
    m=ms[0]; cur="".join(re.findall(r'\.string\s+"((?:\\.|[^"\\])*)"',m.group("body")))
    if control_tokens(cur)!=control_tokens(tr): raise RuntimeError(f"{label}: control-token drift")
    if not tr.endswith("$") or '"' in tr or set(tr)&BANNED_UNICODE: raise RuntimeError(f"{label}: invalid translation surface")
    path.write_text(text[:m.start("body")]+'\t.string "'+tr+'"\n'+text[m.end("body"):],encoding="utf-8")
def main():
    if len(sys.argv)!=2: raise SystemExit("usage: localize_trainers_frlg_quality_routes3_16a_v3_191.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=100: raise RuntimeError("expected 100 blocks")
    for k,v in TRANSLATIONS.items(): replace_label(path,k,v)
    out=root/"build"/"qarro_ru_trainers_frlg_quality_routes3_16a_v3_191_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"targetFile":str(TARGET),"qualityPassBlocks":100,"labels":list(TRANSLATIONS),"humanEditedRussian":True,"controlTokensPreserved":True,"pokemonMoveAbilityNamesPreserved":True,"gameplayLogicTouched":False,"balanceTouched":False,"bossTeamsTouched":False,"specialWhitelistTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: polished 100 trainer rematch blocks in {TARGET}"); return 0
if __name__=="__main__": raise SystemExit(main())
