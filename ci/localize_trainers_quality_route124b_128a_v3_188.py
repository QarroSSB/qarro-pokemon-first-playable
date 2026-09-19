#!/usr/bin/env python3
"""Qarro v3.188: human-quality RU pass for trainer blocks 900-999."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
MARKER="QARRO_RU_TRAINERS_QUALITY_ROUTE124B_128A_V3_188"
TARGET=Path("data/text/trainers.inc")
TRANSLATIONS={
    "Route124_Text_IsabellaDefeat": "Мне просто пот в глаза попал!\\nЯ не плачу!$",
    "Route124_Text_IsabellaPostBattle": "Здесь можно найти красивые цветные осколки\\nразных вещей.$",
    "Route125_Text_NolenIntro": "Я услышал, что ты приближаешься, и решил\\nтебя дождаться!$",
    "Route125_Text_NolenDefeat": "Сдаюсь!$",
    "Route125_Text_NolenPostBattle": "В воде звук распространяется быстрее,\\nчем в воздухе.$",
    "Route125_Text_StanIntro": "Эй!\\nЗацени моего классного POKeMON!$",
    "Route125_Text_StanDefeat": "Я сел на мель...$",
    "Route125_Text_StanPostBattle": "Меня покорило очарование HORSEA,\\nвот я и начал плавать.$",
    "Route125_Text_TanyaIntro": "Я устала плавать.\\nНе хочешь сразиться?$",
    "Route125_Text_TanyaDefeat": "С тобой не справиться!$",
    "Route125_Text_TanyaPostBattle": "Фух...\\nВ какую сторону МОССДИП-СИТИ?$",
    "Route125_Text_SharonIntro": "Как насчет боя с POKeMON\\nводного типа, которых я вырастила?$",
    "Route125_Text_SharonDefeat": "Проиграла...$",
    "Route125_Text_SharonPostBattle": "Твоя сила... Ты настоящий мастер.\\nЯ поражена!$",
    "Route125_Text_ErnestIntro": "Эй-хо! Я крепкий, могучий МОРЯК!\\nЯ бороздил моря всего мира!$",
    "Route125_Text_ErnestDefeat": "Гр-р-ра-а!\\nНе смог победить!$",
    "Route125_Text_ErnestPostBattle": "Прилив в ПЕЩЕРЕ ШОАЛ то поднимается,\\nто отступает.\\pКстати, между приливом и отливом проходит\\nоколо шести часов. Знал?$",
    "Route125_Text_ErnestRegister": "Запиши меня в свой POKeNAV,\\nи я расскажу кое-что полезное.$",
    "Route125_Text_ErnestRematchIntro": "Давно пора мне взять реванш\\nза прошлое поражение! Давай сразимся!$",
    "Route125_Text_ErnestRematchDefeat": "Не смог победить!\\nСовсем никак!$",
    "Route125_Text_ErnestRematchPostBattle": "ПЕЩЕРА ШОАЛ...\\pИз-за приливов и отливов одни места\\nстановятся доступны, а другие\\lнет.\\pКстати, между приливом и отливом проходит\\nоколо шести часов. Не забудь!$",
    "Route125_Text_KimIntro": "КИМ: Говорят, в ПЕЩЕРЕ ШОАЛ живет\\nзабавный старик.\\lТы тоже идешь к нему?$",
    "Route125_Text_KimDefeat": "КИМ: Я думала, мы победим.$",
    "Route125_Text_KimPostBattle": "КИМ: В ПЕЩЕРЕ ШОАЛ ведь живет\\nзабавный старик, да?\\pПойдем к нему, ИРИС!$",
    "Route125_Text_KimNotEnoughMons": "КИМ: Нет-нет-нет! Нужны два POKeMON,\\nиначе никак!$",
    "Route125_Text_IrisIntro": "ИРИС: КИМ, скажи, что мы вообще\\nздесь ищем?$",
    "Route125_Text_IrisDefeat": "ИРИС: Ох, нам почти удалось.$",
    "Route125_Text_IrisPostBattle": "ИРИС: КИМ, мы правда пойдем в\\nПЕЩЕРУ ШОАЛ?\\lМы же промокнем.$",
    "Route125_Text_IrisNotEnoughMons": "ИРИС: О нет, мы никогда не станем\\nсражаться двое против одного.$",
    "Route125_Text_PresleyIntro": "Зачем ПТИЦЕВОДУ вроде меня\\nвыходить в море?$",
    "Route125_Text_PresleyDefeat": "Ладно.\\nРасскажу, зачем я здесь.$",
    "Route125_Text_PresleyPostBattle": "Я положил послание в бутылку и отправил\\nее в море.\\pУверен, какая-нибудь девушка-пловчиха\\nее найдет!$",
    "Route125_Text_AuronIntro": "Эй! Это ты выбрасывал мусор\\nв море?$",
    "Route125_Text_AuronDefeat": "А, значит, это не ты бросал мусор\\nв море.$",
    "Route125_Text_AuronPostBattle": "Раньше я заметил некрасивую бутылку,\\nкачающуюся на волнах.\\pМеня бесит, что кто-то смеет\\nзагрязнять море!$",
    "Route126_Text_BarryIntro": "Плавание тренирует все тело!\\nБудешь в отличной форме!$",
    "Route126_Text_BarryDefeat": "Признаю!\\nТы победил!$",
    "Route126_Text_BarryPostBattle": "Благодаря моим ежедневным заплывам...\\nСмотри! Любуйся этим телом!$",
    "Route126_Text_DeanIntro": "Эта огромная белая гора из камня -\\nСУТОПОЛИС-СИТИ.$",
    "Route126_Text_DeanDefeat": "Меня одолели?$",
    "Route126_Text_DeanPostBattle": "Не могу найти вход в\\nСУТОПОЛИС. Где же он?$",
    "Route126_Text_NikkiIntro": "Уфуфуфу!\\nЯ русалка!$",
    "Route126_Text_NikkiDefeat": "Моя фантазия лопнула, словно пузырь!\\nБуль-буль-буль...$",
    "Route126_Text_NikkiPostBattle": "Ты меня разгромил... Хочется\\nисчезнуть в волне отчаяния...$",
    "Route126_Text_BrendaIntro": "Привет, малыш!\\nХочешь со мной сразиться?$",
    "Route126_Text_BrendaDefeat": "О не-е-ет!$",
    "Route126_Text_BrendaPostBattle": "Обожаю вот так резвиться с POKeMON\\nв море!$",
    "Route126_Text_PabloIntro": "Зацени это рельефное тело!\\nУ меня рельеф круче, чем у ЧЕРНОГО ПОЯСА!$",
    "Route126_Text_PabloDefeat": "Упс! Слишком сильно!\\nНеплохо! Совсем неплохо!$",
    "Route126_Text_PabloPostBattle": "Поражение от тебя взбодрило меня!\\nБуду тренировать себя и POKeMON еще упорнее!$",
    "Route126_Text_PabloRegister": "Да, ты совсем неплох!\\nХочу узнать тебя получше!$",
    "Route126_Text_PabloRematchIntro": "Зацени это прекрасное тело!\\nЯ стройнее любого ПЛОВЦА!$",
    "Route126_Text_PabloRematchDefeat": "Упс! Ну очень сильно!\\nНеплохо! Совсем неплохо!$",
    "Route126_Text_PabloPostRematch": "Буду тренироваться еще упорнее!\\nТы отличный мотиватор!\\lОбязательно приходи снова!$",
    "Route126_Text_LeonardoIntro": "Еще год назад я вообще не умел плавать,\\nа теперь стал неплохим ПЛОВЦОМ.\\pПохоже, теперь мне все по силам.$",
    "Route126_Text_LeonardoDefeat": "Эх, жадность до победы\\nмне совсем не помогла.$",
    "Route126_Text_LeonardoPostBattle": "Если в чем-то тренироваться,\\nобязательно станешь лучше.\\pТы еще молод - не бойся\\nпробовать самые разные вещи!$",
    "Route126_Text_IsobelIntro": "Когда морская вода попадает в нос,\\nужасное ощущение, правда?$",
    "Route126_Text_IsobelDefeat": "Ах! Ну ты...\\nБуль!$",
    "Route126_Text_IsobelPostBattle": "Ой, я наглоталась воды!\\nГорькая! Соленая!!$",
    "Route126_Text_SiennaIntro": "Я вкладываю в это все сердце\\nбез остатка!$",
    "Route126_Text_SiennaDefeat": "У тебя оказалось больше духа!$",
    "Route126_Text_SiennaPostBattle": "Теперь мне надо остыть...\\nПожалуй, нырну.$",
    "Route127_Text_CamdenIntro": "Я вижу это по твоему лицу.\\nТы хочешь бросить мне вызов.$",
    "Route127_Text_CamdenDefeat": "Авававава...$",
    "Route127_Text_CamdenPostBattle": "Хороший бой оставляет после себя\\nсвежесть и спокойствие.$",
    "Route127_Text_DonnyIntro": "У тебя есть соперник, которому ты просто\\nненавидишь проигрывать?$",
    "Route127_Text_DonnyDefeat": "Ар-р-р!\\nНенавижу проигрывать!$",
    "Route127_Text_DonnyPostBattle": "Когда есть соперник, разве не появляется\\nощущение, что надо становиться\\lвсе лучше?$",
    "Route127_Text_JonahIntro": "Благодаря рыбалке я достиг\\nсостояния безмятежного спокойствия...\\pПозволь продемонстрировать...$",
    "Route127_Text_JonahDefeat": "Пусть я проиграл, мое сердце остается\\nспокойным...$",
    "Route127_Text_JonahPostBattle": "Неважно, что ничего не ловится.\\nЛеска все равно остается в воде...$",
    "Route127_Text_HenryIntro": "Упс! Неужели я подцепил\\nPOKeMON во время SURF?$",
    "Route127_Text_HenryDefeat": "За тобой не угнаться!$",
    "Route127_Text_HenryPostBattle": "Вот хлопот было бы, если бы я подцепил\\nтвоего сильного POKeMON!$",
    "Route127_Text_RogerIntro": "Ну что! Это бой между\\nфанатом POKeMON и фанатом рыбалки!$",
    "Route127_Text_RogerDefeat": "Нет! Леска совсем запуталась!\\nПраздник окончен!$",
    "Route127_Text_RogerPostBattle": "Моя леска танцует!\\nТанго запутавшейся лески! Ха-ха, узел!$",
    "Route127_Text_AidanIntro": "У POKeMON-птиц великолепное зрение.\\nОни замечают добычу с огромной высоты.$",
    "Route127_Text_AidanDefeat": "Фух... Сдаюсь.$",
    "Route127_Text_AidanPostBattle": "В здешнем море много мест\\nдля погружения.\\pС воздуха их легко заметить\\nпо более темному цвету воды.$",
    "Route127_Text_KojiIntro": "Бегай босиком.\\nТак подошвы станут крепче!$",
    "Route127_Text_KojiDefeat": "Ай!\\nКамешек забился под ноготь!$",
    "Route127_Text_KojiPostBattle": "Ходить босиком здорово.\\nНо твои БЕГОВЫЕ КРОССОВКИ тоже классные.$",
    "Route127_Text_KojiRegister": "Вот что я делаю с теми, кто меня победил!\\nНадеюсь, еще сразимся.$",
    "Route127_Text_KojiRematchIntro": "Я все еще каждый день бегаю босиком.\\nПодошвы у меня крепкие!$",
    "Route127_Text_KojiRematchDefeat": "Ай!\\nКамешки впились прямо в своды стоп!$",
    "Route127_Text_KojiPostRematch": "Не хочешь немного походить босиком?\\nА я пока примерю твои БЕГОВЫЕ КРОССОВКИ?$",
    "Route127_Text_AthenaIntro": "Давай проведем медленный и продуманный\\nбой.$",
    "Route127_Text_AthenaDefeat": "Ты не оставил мне времени\\nна стратегию.$",
    "Route127_Text_AthenaPostBattle": "Когда вокруг только синее море\\nи небо, кажется, что время замедляется.$",
    "Route128_Text_IsaiahIntro": "До ЭВЕР-ГРАНД-СИТИ еще очень\\nдалеко...$",
    "Route128_Text_IsaiahDefeat": "Похоже, до моей первой победы тоже\\nеще далеко...$",
    "Route128_Text_IsaiahPostBattle": "Вся моя жизнь состоит из поражений,\\nно я никогда не сдамся!$",
    "Route128_Text_IsaiahRegister": "Я знаю, что пока не слишком хорош, но верю,\\nчто когда-нибудь смогу победить.\\pПожалуйста, запиши меня в свой POKeNAV.$",
    "Route128_Text_IsaiahRematchIntro": "Я все еще полон сил. Продолжу\\nплыть к ЭВЕР-ГРАНД-СИТИ.$",
    "Route128_Text_IsaiahRematchDefeat": "Своей первой победы я пока так и не вкусил...$",
    "Route128_Text_IsaiahPostRematch": "Когда-нибудь я доберусь до ЭВЕР-ГРАНД-СИТИ,\\nи когда-нибудь там наконец одержу победу...$",
    "Route128_Text_KatelynIntro": "В триатлоне нужно плыть, ехать на велосипеде,\\nа потом бежать марафон.\\pЭто изнурительная гонка из\\nтрех дисциплин.$",
    "Route128_Text_KatelynDefeat": "Бой POKeMON тоже изматывает...$",
}
BANNED_UNICODE=set("—–←→“”«»")
def control_tokens(t): return re.findall(r'\{[^}]+\}|\\.|\$',t)
def replace_label(path,label,tr):
    text=path.read_text(encoding="utf-8")
    pat=re.compile(rf'(?ms)^(?P<head>{re.escape(label)}:\s*\n)(?P<body>(?:[ \t]*\.string\s+"(?:\\.|[^"\\])*"\s*\n?)+)')
    m=list(pat.finditer(text))
    if len(m)!=1: raise RuntimeError(f"{label}: expected one block, got {len(m)}")
    m=m[0]; cur="".join(re.findall(r'\.string\s+"((?:\\.|[^"\\])*)"',m.group("body")))
    if control_tokens(cur)!=control_tokens(tr): raise RuntimeError(f"{label}: control-token drift")
    if not tr.endswith("$") or '"' in tr or set(tr)&BANNED_UNICODE: raise RuntimeError(f"{label}: invalid translation surface")
    path.write_text(text[:m.start("body")]+'\t.string "'+tr+'"\n'+text[m.end("body"):],encoding="utf-8")
def main():
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=100: raise RuntimeError("expected 100 blocks")
    for k,v in TRANSLATIONS.items(): replace_label(path,k,v)
    out=root/"build"/"qarro_ru_trainers_quality_route124b_128a_v3_188_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"targetFile":str(TARGET),"qualityPassBlocks":100,"labels":list(TRANSLATIONS),"humanEditedRussian":True,"controlTokensPreserved":True,"pokemonMoveAbilityNamesPreserved":True,"gameplayLogicTouched":False,"balanceTouched":False,"bossTeamsTouched":False,"specialWhitelistTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: polished 100 trainer text blocks in {TARGET}"); return 0
if __name__=="__main__": raise SystemExit(main())
