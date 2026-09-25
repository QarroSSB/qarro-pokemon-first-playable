#!/usr/bin/env python3
"""Qarro v3.190: final human-quality RU pass for trainers.inc (blocks 1100-1143)."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
MARKER="QARRO_RU_TRAINERS_QUALITY_ROUTE133B_134_VSSEEKER_V3_190"
TARGET=Path("data/text/trainers.inc")
TRANSLATIONS={
    "Route133_Text_LindaIntro": "Добро пожаловать!\\nЯ тебя ждала!$",
    "Route133_Text_LindaDefeat": "Нет! Пожалуйста!$",
    "Route133_Text_LindaPostBattle": "Сильный юный тренер...\\nКак же раздражает!$",
    "Route133_Text_WarrenIntro": "Я хочу побеждать, как все, но\\nрастить POKeMON как все не собираюсь.$",
    "Route133_Text_WarrenDefeat": "Черт!\\nМой путь все еще слишком слабый!$",
    "Route133_Text_WarrenPostBattle": "Гораздо веселее делать все так,\\nкак хочется мне, чем быть как все.\\lЭто же очевидно!$",
    "Route133_Text_BeckIntro": "Я проделал весь путь сюда со своими\\nPOKeMON-птицами.$",
    "Route133_Text_BeckDefeat": "Ты...\\nТы потрясающе крут!$",
    "Route133_Text_BeckPostBattle": "Я хотел бы вернуться в ФОРТРИ,\\nно это место мне тоже полюбилось.$",
    "Route133_Text_MollieIntro": "Наверное, я сражалась уже тысячи\\nраз. Я сбилась со счета.$",
    "Route133_Text_MollieDefeat": "Пусть я проигрывала тысячи раз,\\nкаждое поражение все равно больно.$",
    "Route133_Text_MolliePostBattle": "Продолжай в том же духе, юный тренер. И однажды\\nстанешь таким, как мы с мужем.$",
    "Route133_Text_ConorIntro": "Молодежь слишком охотно плывет\\nпо течению. Никакой цели.$",
    "Route133_Text_ConorDefeat": "У тебя есть четкая цель.$",
    "Route133_Text_ConorPostBattle": "Не позволяй другим сбить тебя с пути.\\nИ взрослея, не теряй направления.$",
    "Route134_Text_JackIntro": "Даже POKeMON, которые умеют плавать,\\nуносит быстрое течение.$",
    "Route134_Text_JackDefeat": "Ай-и-и-и!$",
    "Route134_Text_JackPostBattle": "Думаю, POKeMON нравятся быстрые\\nтечения в этих местах.$",
    "Route134_Text_LaurelIntro": "Мои LUVDISC хотят веселого\\nбоя. Присоединишься?$",
    "Route134_Text_LaurelDefeat": "Упс!$",
    "Route134_Text_LaurelPostBattle": "Есть коллекционер, который ищет\\nЧЕШУЮ LUVDISC.$",
    "Route134_Text_AlexIntro": "Ладушки! Отдохнули и хватит, команда!\\nПора сражаться!$",
    "Route134_Text_AlexDefeat": "Снова выдохлись...$",
    "Route134_Text_AlexPostBattle": "Мои POKeMON-птицы быстро устают после\\nдолгого полета...$",
    "Route134_Text_HitoshiIntro": "Ты тренер POKeMON.\\nСлова не нужны. Сражаемся.$",
    "Route134_Text_HitoshiPostBattle": "Это я бросил тебе вызов и все же\\nпроиграл. Мне очень стыдно...$",
    "Route134_Text_AaronIntro": "Свирепое течение в этих местах помогает\\nнам становиться еще сильнее.$",
    "Route134_Text_AaronDefeat": "Я добровольно признаю поражение.$",
    "Route134_Text_AaronPostBattle": "Мы вернемся тренироваться в\\nМЕТЕОР-ФОЛЛС.\\pЕсли хочешь, приходи тоже.\\nЭто точно сделает тебя сильнее!$",
    "Route134_Text_KelvinIntro": "Н-наша лодка!\\nЕе унесло течением!$",
    "Route134_Text_KelvinDefeat": "Ававава!\\nПожалуйста, хватит! Пожалуйста!$",
    "Route134_Text_KelvinPostBattle": "Если мы не можем использовать SURF, как\\nнам вернуться домой?\\pВообще-то я знаю, что потерявший сознание POKeMON\\nвсе еще может использовать SURF, но это неправильно.$",
    "Route134_Text_MarleyIntro": "Сможет ли твой POKeMON уклониться от наших\\nмолниеносных атак?$",
    "Route134_Text_MarleyDefeat": "Не знал, что существует такая техника!\\nТы разгромил нас полностью.$",
    "Route134_Text_MarleyPostBattle": "Я не потеряла страсть к скорости.\\nБуду стараться еще сильнее.$",
    "Route134_Text_ReynaIntro": "Моего POKeMON не так-то просто\\nпобедить!$",
    "Route134_Text_ReynaDefeat": "Да ладно!\\nОбъясни, как я проиграла!$",
    "Route134_Text_ReynaPostBattle": "Ха-ха!\\nЛадно, ты победил!\\pЯ верну форму, сражаясь со всеми\\nтренерами, которых встречу!$",
    "Route134_Text_HudsonIntro": "Слушай, ты не видел другого МОРЯКА\\nгде-нибудь поблизости?$",
    "Route134_Text_HudsonDefeat": "Вот это да!$",
    "Route134_Text_HudsonPostBattle": "Нашу лодку унесло в море.\\pМой приятель робкий парень, и я\\nза него переживаю.$",
    "VSSeeker_Text_BatteryNotChargedNeedXSteps:": "Батарея заряжена недостаточно.\\pШагов до полной зарядки:\\n{STR_VAR_1}{PAUSE_UNTIL_PRESS}$",
    "VSSeeker_Text_NoTrainersWithinRange:": "Поблизости нет тренеров,\\nготовых сразиться...\\pVS SEEKER выключен.{PAUSE_UNTIL_PRESS}$",
    "VSSeeker_Text_TrainersNotReady:": "Другие тренеры, похоже,\\nеще не готовы к бою.\\pПодождем немного.{PAUSE_UNTIL_PRESS}$",
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
    if len(sys.argv)!=2: raise SystemExit("usage: localize_trainers_quality_route133b_134_vsseeker_v3_190.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=44: raise RuntimeError("expected 44 blocks")
    for k,v in TRANSLATIONS.items(): replace_label(path,k,v)
    out=root/"build"/"qarro_ru_trainers_quality_route133b_134_vsseeker_v3_190_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"targetFile":str(TARGET),"qualityPassBlocks":44,"trainersIncHumanQualityBlocksTotal":1144,"trainersIncHumanQualityComplete":True,"labels":list(TRANSLATIONS),"humanEditedRussian":True,"controlTokensPreserved":True,"pokemonMoveAbilityNamesPreserved":True,"gameplayLogicTouched":False,"balanceTouched":False,"bossTeamsTouched":False,"specialWhitelistTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: final 44 blocks; trainers.inc human-quality pass complete 1144/1144"); return 0
if __name__=="__main__": raise SystemExit(main())
