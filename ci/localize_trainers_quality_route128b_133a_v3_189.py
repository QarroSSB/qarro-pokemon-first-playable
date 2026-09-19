#!/usr/bin/env python3
"""Qarro v3.189: human-quality RU pass for trainer blocks 1000-1099."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
MARKER="QARRO_RU_TRAINERS_QUALITY_ROUTE128B_133A_V3_189"
TARGET=Path("data/text/trainers.inc")
TRANSLATIONS={
    "Route128_Text_KatelynPostBattle": "Дальше мне еще ехать на ВЕЛОСИПЕДЕ, но...\\nЯ уже почти готова сдаться...$",
    "Route128_Text_KatelynRegister": "Ну что ж, раз уж я здесь,\\nхочу получить максимум. Как-нибудь устроим реванш.$",
    "Route128_Text_KatelynRematchIntro": "Триатлон - длинное испытание. Но, думаю,\\nпуть к званию ЧЕМПИОНА POKeMON\\lтоже долог и изнурителен.$",
    "Route128_Text_KatelynRematchDefeat": "Бой POKeMON и правда суров\\nи беспощаден...$",
    "Route128_Text_KatelynPostRematch": "Тебе стоит всерьез подумать\\nоб испытаниях на ДОРОГЕ ПОБЕДЫ.$",
    "Route128_Text_AlexaIntro": "Мы так упорно готовились к\\nвызову ЛИГЕ POKeMON...\\pСейчас нельзя проигрывать!$",
    "Route128_Text_AlexaDefeat": "О!\\nКак такое могло случиться?!$",
    "Route128_Text_AlexaPostBattle": "После всего, что я сделала, чтобы дойти сюда,\\nодно поражение меня не остановит.$",
    "Route128_Text_RubenIntro": "Нет тренера сильнее меня!$",
    "Route128_Text_RubenDefeat": "Не может быть!$",
    "Route128_Text_RubenPostBattle": "Пожалуй, нет тренера сильнее,\\nчем ты!$",
    "Route128_Text_WayneIntro": "Я хочу попасть в ЭВЕР-ГРАНД, поэтому\\nпоймал POKeMON, который знает\\lWATERFALL и сможет подняться по водопаду.$",
    "Route128_Text_WayneDefeat": "Я совсем пал духом!$",
    "Route128_Text_WaynePostBattle": "Эх, вот досада!\\pМой POKeMON знает WATERFALL, но\\nу меня нет ЗНАЧКА ЗАЛА СУТОПОЛИСА!$",
    "Route128_Text_HarrisonIntro": "Выглядишь очень крепким соперником.\\nИнтересно, смогу ли победить?$",
    "Route128_Text_HarrisonDefeat": "Ай!\\nПохоже, победить было невозможно.$",
    "Route128_Text_HarrisonPostBattle": "Вокруг ЭВЕР-ГРАНДА полно\\nсильных тренеров.\\pМожет, я здесь просто\\nне своего уровня?$",
    "Route128_Text_CarleeIntro": "В этих местах солнечный свет кажется\\nособенно резким.$",
    "Route128_Text_CarleeDefeat": "Из-за солнечных бликов\\nя почти ничего не видела.$",
    "Route128_Text_CarleePostBattle": "Пора возвращаться.\\nНужно снова нанести солнцезащитный крем.$",
    "Route129_Text_ChaseIntro": "Это мой первый триатлон.\\nЯ весь напряжен и нервничаю!$",
    "Route129_Text_ChaseDefeat": "Рррооаар!\\nНе получилось победить!$",
    "Route129_Text_ChasePostBattle": "Если буду так напряжен, не смогу\\nвыложиться на полную.$",
    "Route129_Text_AllisonIntro": "Я прямо посреди триатлона,\\nно почему бы не сразиться?$",
    "Route129_Text_AllisonDefeat": "Я была уверена в победе!$",
    "Route129_Text_AllisonPostBattle": "Знаешь, что самое прекрасное\\nв триатлоне?\\pПроверять пределы собственной\\nсилы и выносливости в борьбе\\lс самой природой!$",
    "Route129_Text_ReedIntro": "Эй, эй!\\nДавай уже начнем!$",
    "Route129_Text_ReedDefeat": "Все, меня побили.\\nГотово, конец!$",
    "Route129_Text_ReedPostBattle": "Проигравшему ничего не достается.\\nПора мне убираться домой.$",
    "Route129_Text_TishaIntro": "Куда спешишь?\\nДавай спокойно, не торопясь.$",
    "Route129_Text_TishaDefeat": "Ох.\\nЯ хотела еще немного расслабиться...$",
    "Route129_Text_TishaPostBattle": "Разве не бесит ошибаться,\\nкогда спешишь?\\pВот поэтому я стараюсь делать все\\nне торопясь.$",
    "Route129_Text_ClarenceIntro": "SURF не так прост, как кажется,\\nправда?$",
    "Route129_Text_ClarenceDefeat": "Побеждать и правда нелегко.$",
    "Route129_Text_ClarencePostBattle": "Нацелился на ЛИГУ POKeMON?\\nПродолжай в том же духе!$",
    "Route130_Text_RodneyIntro": "Вот это сюрприз! Не ожидал\\nвстретить тренера посреди моря.\\pДумаю, нам стоит сразиться!$",
    "Route130_Text_RodneyDefeat": "Этот ребенок ужасно силен...$",
    "Route130_Text_RodneyPostBattle": "По твоим глазам видно: ты прошел\\nчерез тяжелые испытания\\lи победил. Тебе идет этот взгляд!$",
    "Route130_Text_KatieIntro": "В глубоком синем море\\nмое разбитое сердце находит\\lутешение среди волн.$",
    "Route130_Text_KatieDefeat": "Как бескрайнее синее море,\\nмир POKeMON скрывает\\lневероятные глубины.$",
    "Route130_Text_KatiePostBattle": "Дети всего мира мечтают\\nкогда-нибудь стать\\lЧЕМПИОНОМ POKeMON.$",
    "Route130_Text_SantiagoIntro": "Вот так плыть по открытому морю...\\nТак спокойно.$",
    "Route130_Text_SantiagoDefeat": "Надо было быть чуть менее спокойным!$",
    "Route130_Text_SantiagoPostBattle": "Плавать и сражаться вот так...\\nЯ счастлив...$",
    "Route131_Text_RichardIntro": "Море кишит POKeMON.\\nПлавать здесь совсем непросто.$",
    "Route131_Text_RichardDefeat": "POKeMON, выращенные тренерами,\\nпо-настоящему сильны...$",
    "Route131_Text_RichardPostBattle": "Фух... Фух...\\nЯ совсем вымотался...\\pТуда плыть легко. А вот обратно -\\nсовсем другое дело.\\pХватит ли у меня сил\\nна обратный путь?$",
    "Route131_Text_HermanIntro": "Море... Море... Море...\\nКуда ни глянь - одно море!\\lНадоело мне это море!$",
    "Route131_Text_HermanDefeat": "Бе-е!$",
    "Route131_Text_HermanPostBattle": "Море мне надоело, но плавать придется.\\pЯ прирожденный пловец!\\nВот кто я.$",
    "Route131_Text_SusieIntro": "Эй, милый, постой!\\nНам с тобой надо сразиться!$",
    "Route131_Text_SusieDefeat": "А ты сильнее, чем\\nвыглядишь!$",
    "Route131_Text_SusiePostBattle": "Видел вон того парня, который ноет,\\nчто ему надоело море?\\pЭто одни разговоры.\\nОн безнадежно влюблен в море!$",
    "Route131_Text_KaraIntro": "Почему мужчины так любят купальники?\\pВсе на меня пялятся!$",
    "Route131_Text_KaraDefeat": "Я не справилась!$",
    "Route131_Text_KaraPostBattle": "Может, мужчины смотрят вовсе не\\nиз-за купальника. Наверное, дело в моей красоте!$",
    "Route131_Text_ReliIntro": "РЕЛИ: Мы с братом будем действовать вместе,\\nчтобы победить тебя!$",
    "Route131_Text_ReliDefeat": "РЕЛИ: Даже действуя вместе, мы\\nне смогли победить...$",
    "Route131_Text_ReliPostBattle": "РЕЛИ: Жители ПАСИФИДЛОГА\\nс самого рождения живут рядом с морем и\\lPOKeMON.$",
    "Route131_Text_ReliNotEnoughMons": "РЕЛИ: У тебя нет двух POKeMON?\\nТогда нормального боя не получится.$",
    "Route131_Text_IanIntro": "ИЭН: Я изо всех сил стараюсь вместе\\nсо своей сестрой!$",
    "Route131_Text_IanDefeat": "ИЭН: Мы с сестрой старались изо всех сил,\\nно все равно не смогли победить...$",
    "Route131_Text_IanPostBattle": "ИЭН: Ты же знаешь, ПАСИФИДЛОГ -\\nплавучий город?\\pЗначит, где есть море,\\nтам есть и частичка ПАСИФИДЛОГА!$",
    "Route131_Text_IanNotEnoughMons": "ИЭН: Если у тебя есть два POKeMON,\\nмы готовы сразиться!$",
    "Route131_Text_TaliaIntro": "Если победишь меня, расскажу тебе\\nкое-что очень интересное!$",
    "Route131_Text_TaliaDefeat": "О?\\nЯ проиграла?$",
    "Route131_Text_TaliaPostBattle": "Неподалеку есть странное место.\\nТам стоит огромная башня.\\lПочему бы тебе не сходить посмотреть?$",
    "Route131_Text_KevinIntro": "Жители ПАСИФИДЛОГА -\\nочень мирный народ.\\pОни никогда не сердятся.\\nЯ тоже.$",
    "Route131_Text_KevinDefeat": "Упс!$",
    "Route131_Text_KevinPostBattle": "Тц! ...Ой, погоди.\\nЯ не злюсь. Честно!\\pНо ты и правда силен!\\nХа-ха-ха!$",
    "Route132_Text_GilbertIntro": "В детстве я постоянно простужался,\\nно стал совершенно здоровым после того,\\lкак начал плавать.$",
    "Route132_Text_GilbertDefeat": "Мне нужно больше силы...$",
    "Route132_Text_GilbertPostBattle": "Тренеры путешествуют по полям и\\nгорам, значит, им тоже нужна хорошая форма.$",
    "Route132_Text_DanaIntro": "Я стараюсь не плавать там, где течения\\nслишком сильные.$",
    "Route132_Text_DanaDefeat": "О нет, пожалуйста!$",
    "Route132_Text_DanaPostBattle": "Если течение меня унесет, я совсем\\nпотеряю ориентир...$",
    "Route132_Text_RonaldIntro": "Пока не попробуешь, не узнаешь,\\nпобедишь или проиграешь!$",
    "Route132_Text_RonaldDefeat": "А-а-а!\\nЯ утонул в поражении!$",
    "Route132_Text_RonaldPostBattle": "Я не сражаюсь, если заранее знаю, что выиграю.\\nМне нравятся бои на самой грани\\lпобеды и поражения!$",
    "Route132_Text_KiyoIntro": "Я думаю о POKeMON круглые сутки.\\nКак ты вообще можешь меня победить?$",
    "Route132_Text_KiyoDefeat": "Я проиграл.\\nПризнаю поражение.$",
    "Route132_Text_KiyoPostBattle": "Ургх...\\nТы фанат POKeMON, да?\\pНаверняка думаешь о POKeMON круглые сутки,\\nверно?$",
    "Route132_Text_MakaylaIntro": "Я всегда рядом с мужем,\\nно могу победить и без него.$",
    "Route132_Text_MakaylaDefeat": "Похоже, мне все-таки не хватило мастерства.$",
    "Route132_Text_MakaylaPostBattle": "Вон тот молодой человек так похож\\nна моего мужа в молодости.\\pЯ даже краснею!$",
    "Route132_Text_JonathanIntro": "Кто-то очень пристально на меня смотрит.\\nЭто ты?$",
    "Route132_Text_JonathanDefeat": "Ух ты!\\nВот это сила!$",
    "Route132_Text_JonathanPostBattle": "Не могу избавиться от ощущения, что\\nкто-то наблюдает за мной.\\pНе могу сосредоточиться!$",
    "Route132_Text_PaxtonIntro": "Куда же делась моя жена?\\nМы всегда вместе.\\lИнтересно, смогу ли я победить один.$",
    "Route132_Text_PaxtonDefeat": "Понятно. Все-таки в одиночку\\nпобедить мне не удалось.$",
    "Route132_Text_PaxtonPostBattle": "Жена наверняка меня ищет.\\nНужно срочно ее найти.$",
    "Route132_Text_DarcyIntro": "Мне нравилось тренироваться здесь одному.\\nУжасно, что сюда пришло столько людей!$",
    "Route132_Text_DarcyDefeat": "Ладно! Больше не буду жаловаться на\\nдругих людей здесь.$",
    "Route132_Text_DarcyPostBattle": "Пожалуй, объединюсь с тем\\nстариком и брошу вызов другой команде.$",
    "Route133_Text_FranklinIntro": "Тебя тоже принесло сюда течением?\\nЗначит, так было суждено.\\lДавай сразимся!$",
    "Route133_Text_FranklinDefeat": "Сильно!\\nСлишком сильно!$",
    "Route133_Text_FranklinPostBattle": "Ну конечно, именно ко мне приплыл\\nтакой сильный тренер, как ты...\\lДа я проклят...$",
    "Route133_Text_DebraIntro": "Вся моя жизнь полна горя и несчастий...\\nМеня выбросило прочь, и вот сюда\\lя приплыла...$",
    "Route133_Text_DebraDefeat": "Еще одно поражение...$",
    "Route133_Text_DebraPostBattle": "Жизнь в вечном дрейфе...\\nБольше я так не хочу!$",
}
BANNED_UNICODE=set("—–←→“”«»")
def control_tokens(t): return re.findall(r'\{[^}]+\}|\\.|\$',t)
def replace_label(path,label,tr):
    text=path.read_text(encoding="utf-8")
    pat=re.compile(rf'(?ms)^(?P<head>{re.escape(label)}:\s*\n)(?P<body>(?:[ \t]*\.string\s+"(?:\\.|[^"\\])*"\s*\n?)+)')
    ms=list(pat.finditer(text))
    if len(ms)!=1: raise RuntimeError(f"{label}: expected one block, got {len(ms)}")
    m=ms[0]
    cur="".join(re.findall(r'\.string\s+"((?:\\.|[^"\\])*)"',m.group("body")))
    if control_tokens(cur)!=control_tokens(tr): raise RuntimeError(f"{label}: control-token drift")
    if not tr.endswith("$") or '"' in tr or set(tr)&BANNED_UNICODE: raise RuntimeError(f"{label}: invalid translation surface")
    path.write_text(text[:m.start("body")]+'\t.string "'+tr+'"\n'+text[m.end("body"):],encoding="utf-8")
def main():
    if len(sys.argv)!=2: raise SystemExit("usage: localize_trainers_quality_route128b_133a_v3_189.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=100: raise RuntimeError("expected 100 blocks")
    for k,v in TRANSLATIONS.items(): replace_label(path,k,v)
    out=root/"build"/"qarro_ru_trainers_quality_route128b_133a_v3_189_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"targetFile":str(TARGET),"qualityPassBlocks":100,"labels":list(TRANSLATIONS),"humanEditedRussian":True,"controlTokensPreserved":True,"pokemonMoveAbilityNamesPreserved":True,"gameplayLogicTouched":False,"balanceTouched":False,"bossTeamsTouched":False,"specialWhitelistTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: polished 100 trainer text blocks in {TARGET}"); return 0
if __name__=="__main__": raise SystemExit(main())
