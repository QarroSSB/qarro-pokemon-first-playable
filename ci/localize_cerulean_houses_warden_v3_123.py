#!/usr/bin/env python3
"""Qarro v3.123: localize safe Cerulean houses and Fuchsia Warden text.

Translates exactly 34 English-only FireRed runtime blocks after v3.122:
  * CeruleanCity_House5_Frlg: 12 Berry Powder dialogue blocks
  * CeruleanCity_House1_Frlg: 11 badge-info dialogue blocks
  * FuchsiaCity_WardensHouse_Frlg: 11 Warden/sign dialogue blocks

Move proper names remain English. Berry Powder vendor/badge menu/HM04/Gold Teeth
logic, the unused Japanese Warden block, trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
MARKER="QARRO_RU_CERULEAN_HOUSES_WARDEN_V3_123"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES={
"data/maps/CeruleanCity_House5_Frlg/scripts.inc":{
"CeruleanCity_House1_Text_AnyInterestInBerries":"Я готовлю разные лекарства\\nиз ЯГОДНОГО ПОРОШКА.\\pИз хорошего ЯГОДНОГО ПОРОШКА\\nможно сделать любое лекарство.\\pСкажи, тебя интересуют ЯГОДЫ?$",
"CeruleanCity_House1_Text_HaveJustTheThing":"Отлично! Тогда у меня есть\\nдля тебя кое-что.$",
"CeruleanCity_House1_Text_GoCrushBerriesAtDirectCorner":"На втором этаже ПОКЕМОН-ЦЕНТРОВ\\nв DIRECT CORNER появилось новое.\\pТам установили устройство\\nдля измельчения ЯГОД.\\pИ тут мне нужна твоя помощь.\\pЯ могу доверить это только тебе.\\pСделаешь для меня ЯГОДНЫЙ ПОРОШОК\\nна этом устройстве?\\pНе забудь: оно находится\\nв DIRECT CORNER ПОКЕМОН-ЦЕНТРОВ.\\pПринесёшь ЯГОДНЫЙ ПОРОШОК -\\nя приготовлю тебе лекарство.\\pИзмельчай ЯГОДЫ в ПОРОШОК\\nи приноси его мне.$",
"CeruleanCity_House1_Text_WhyMustYouLieNoBerries":"Зачем же меня обманывать?\\pСколько у тебя ЯГОД?\\nНи одной!$",
"CeruleanCity_House1_Text_TakeInterestInAllSortsOfThings":"ЯГОДЫ тебя не интересуют?\\pЮный друг, важно интересоваться\\nсамыми разными вещами.$",
"CeruleanCity_House1_Text_HaveYouBroughtBerryPowder":"Кхм! Ты принёс мне\\nЯГОДНЫЙ ПОРОШОК?$",
"CeruleanCity_House5_Text_ExchangeWithWhat":"На что хочешь его обменять?$",
"CeruleanCity_House1_Text_YoullExchangeBerryPowderForItem":"Хорошо, обменяешь ЯГОДНЫЙ\\nПОРОШОК на {STR_VAR_1}?$",
"CeruleanCity_House1_Text_DontHaveEnoughBerryPowder":"Хм? У тебя недостаточно\\nЯГОДНОГО ПОРОШКА.$",
"CeruleanCity_House1_Text_TradeMoreBerryPowder":"Отличный ЯГОДНЫЙ ПОРОШОК.\\nИз него выйдет хорошее лекарство.\\pХочешь обменять ещё ПОРОШОК\\nна что-нибудь другое?$",
"CeruleanCity_House1_Text_HopeToSeeYouAgain":"Хорошо.\\nБуду ждать тебя снова.$",
"CeruleanCity_House1_Text_SeeMeIfYoudLikeToTradePowder":"Приходи, если захочешь обменять\\nЯГОДНЫЙ ПОРОШОК.$",
},
"data/maps/CeruleanCity_House1_Frlg/scripts.inc":{
"CeruleanCity_House1_Text_BadgesHaveAmazingSecrets":"Только умелые ТРЕНЕРЫ могут\\nсобирать ЗНАЧКИ ПОКЕМОНОВ.\\pВижу, у тебя уже есть хотя бы один.\\pЗнаешь, у этих ЗНАЧКОВ\\nесть удивительные секреты?$",
"CeruleanCity_House1_Text_DescribeWhichBadge":"Ну что же...\\pО каком из восьми ЗНАЧКОВ\\nтебе рассказать?$",
"CeruleanCity_House1_Text_ComeVisitAnytime":"Заходи ко мне в любое время.$",
"CeruleanCity_House1_Text_AttackStatFlash":"Показатель АТАКИ всех твоих\\nПОКЕМОНОВ немного повышается.\\pТакже можно использовать FLASH\\nвне боя.$",
"CeruleanCity_House1_Text_ObeyLv30Cut":"ПОКЕМОНЫ до ур. 30 будут\\nтебя слушаться.\\pДаже полученные по обмену.\\pПОКЕМОНЫ более высокого уровня\\nмогут не слушаться в бою.\\pТакже можно использовать CUT\\nвне боя.$",
"CeruleanCity_House1_Text_SpeedStatFly":"СКОРОСТЬ всех твоих ПОКЕМОНОВ\\nнемного повышается.\\pТакже можно использовать FLY\\nвне боя.$",
"CeruleanCity_House1_Text_ObeyLv50Strength":"ПОКЕМОНЫ до ур. 50 будут\\nтебя слушаться.\\pДаже полученные по обмену.\\pПОКЕМОНЫ более высокого уровня\\nмогут не слушаться в бою.\\pТакже можно использовать STRENGTH\\nвне боя.$",
"CeruleanCity_House1_Text_DefenseStatSurf":"ЗАЩИТА всех твоих ПОКЕМОНОВ\\nнемного повышается.\\pТакже можно использовать SURF\\nвне боя.$",
"CeruleanCity_House1_Text_ObeyLv70RockSmash":"ПОКЕМОНЫ до ур. 70 будут\\nтебя слушаться.\\pДаже полученные по обмену.\\pПОКЕМОНЫ более высокого уровня\\nмогут не слушаться в бою.\\pТакже можно использовать ROCK SMASH\\nвне боя.$",
"CeruleanCity_House1_Text_SpStatsWaterfall":"СП. АТК и СП. ЗАЩ всех твоих\\nПОКЕМОНОВ немного повышаются.\\pТакже можно использовать WATERFALL\\nвне боя.$",
"CeruleanCity_House1_Text_AllMonsWillObeyYou":"Все ПОКЕМОНЫ будут тебя слушаться!$",
},
"data/maps/FuchsiaCity_WardensHouse_Frlg/scripts.inc":{
"FuchsiaCity_WardensHouse_Text_HifFuffHefifoo":"СМОТРИТЕЛЬ: Хиф фуф хефифу!\\pХа лоф ха фиф и хафахи хо.\\nХеф хи фви!$",
"FuchsiaCity_WardensHouse_Text_AhHowheeHoHoo":"Ах хови хо ху!\\nИф и хафахи хо!$",
"FuchsiaCity_WardensHouse_Text_HeOhayHeHaHoo":"Ха?\\nХи охай хех ха ху и хахех!$",
"FuchsiaCity_WardensHouse_Text_GaveGoldTeethToWarden":"{PLAYER} отдал ЗОЛОТЫЕ ЗУБЫ\\nСМОТРИТЕЛЮ.$",
"FuchsiaCity_WardensHouse_Text_WardenPoppedInHisTeeth":"СМОТРИТЕЛЬ вставил свои зубы!$",
"FuchsiaCity_WardensHouse_Text_ThanksSonGiveYouSomething":"СМОТРИТЕЛЬ: Спасибо, сынок!\\nТы меня здорово выручил!\\pНикто не понимал ни слова\\nиз того, что я говорил!\\pМне было стыдно даже появляться\\nв ОФИСЕ.\\pПозволь отблагодарить тебя\\nза помощь.$",
"FuchsiaCity_WardensHouse_Text_ThanksLassieGiveYouSomething":"СМОТРИТЕЛЬ: Спасибо, девочка!\\nТы меня здорово выручила!\\pНикто не понимал ни слова\\nиз того, что я говорил!\\pМне было стыдно даже появляться\\nв ОФИСЕ.\\pПозволь отблагодарить тебя\\nза помощь.$",
"FuchsiaCity_WardensHouse_Text_ReceivedHM04FromWarden":"{PLAYER} получил HM04\\nот СМОТРИТЕЛЯ.$",
"FuchsiaCity_WardensHouse_Text_ExplainStrength":"СМОТРИТЕЛЬ: В HM04 находится\\nSTRENGTH.\\pЭтот приём позволяет ПОКЕМОНАМ\\nдвигать валуны вне боя.\\pКстати, ты нашёл СЕКРЕТНЫЙ ДОМ\\nв ЗОНЕ САФАРИ?$",
"FuchsiaCity_WardensHouse_Text_MonPhotosFossilsOnDisplay":"Здесь выставлены фотографии\\nПОКЕМОНОВ и окаменелости.$",
"FuchsiaCity_WardensHouse_Text_OldMonMerchandiseOnDisplay":"Здесь выставлены старые товары\\nс ПОКЕМОНАМИ.$",
},
}
EXPECTED_TOTAL=34

def die(msg): raise SystemExit(f"[{MARKER}] ERROR: {msg}")
def validate_translation(label,tr):
    if not tr.endswith('$'): die(f"{label}: must end with $")
    if '\n' in tr or '\r' in tr: die(f"{label}: physical newline")
    if any(ch in tr for ch in ('—','–','“','”','’','…','«','»')): die(f"{label}: unsupported punctuation")
    if '\\\\' in tr: die(f"{label}: doubled runtime backslash")
    if not re.search(r'[А-Яа-яЁё]',tr): die(f"{label}: expected Cyrillic")
def block_bounds(text,label):
    ms=list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$",text))
    if len(ms)!=1: die(f"{label}: expected one label, got {len(ms)}")
    s=ms[0].start(); nxt=LABEL_RE.search(text,ms[0].end()); e=nxt.start() if nxt else len(text); return s,e,text[s:e]
def replace_block(text,label,tr):
    s,e,old=block_bounds(text,label)
    if re.search(r'[А-Яа-яЁё]',old): die(f"{label}: already Cyrillic")
    if '.string ' not in old: die(f"{label}: not text block")
    safe=tr.replace('"','\\"'); return text[:s]+f'{label}::\n\t.string "{safe}"\n\n'+text[e:]
def validate_written(rel,text):
    for n,line in enumerate(text.splitlines(),1):
        if '.string "' in line and line.count('"')<2: die(f"{rel}:{n}: broken string")
    if re.search(r'\\\\[npl]',text): die(f"{rel}: doubled runtime escape")
def main():
    if len(sys.argv)!=2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>",file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve(); total=0; by={}
    for rel_s,patches in FILES.items():
        path=root/rel_s
        if not path.is_file(): die(f"missing target: {rel_s}")
        text=path.read_text(encoding='utf-8')
        for label,tr in patches.items(): validate_translation(label,tr); text=replace_block(text,label,tr)
        validate_written(Path(rel_s),text); path.write_text(text,encoding='utf-8'); by[rel_s]=len(patches); total+=len(patches)
    if total!=EXPECTED_TOTAL: die(f"expected {EXPECTED_TOTAL}, got {total}")
    audit=root/'build'/'qarro_ru_cerulean_houses_warden_v3_123_audit.json'; audit.parent.mkdir(parents=True,exist_ok=True)
    audit.write_text(json.dumps({"marker":MARKER,"translatedBlockCount":EXPECTED_TOTAL,"translatedByFile":by,"moveProperNamesPolicy":"English","berryPowderVendorLogicTouched":False,"badgeMenuLogicTouched":False,"hm04GoldTeethLogicTouched":False,"unusedJapaneseTextTouched":False,"trainerDataTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; vendor/badge/HM04/Gold Teeth/unused-Japanese/trainer/Ash logic untouched")
    return 0
if __name__=='__main__': raise SystemExit(main())
