#!/usr/bin/env python3
"""Qarro v3.125: localize Lavender Town and two Fishing Guru houses.

Translates exactly 23 English-only FireRed runtime blocks after v3.124:
  * LavenderTown_Frlg: 9
  * FuchsiaCity_House2_Frlg: 7
  * VermilionCity_House1_Frlg: 7

Fishing-rod reward/flag logic, map-transition logic, trainer data,
Pokemon/Move/Ability proper-name policy, and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
MARKER="QARRO_RU_LAVENDER_FISHING_V3_125"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES={
"data/maps/LavenderTown_Frlg/scripts.inc":{
"LavenderTown_Text_DoYouBelieveInGhosts":"Ты веришь в призраков?$",
"LavenderTown_Text_SoThereAreBelievers":"Правда?\\nЗначит, верующие всё-таки есть...$",
"LavenderTown_Text_JustImaginingWhiteHand":"Ха-ха, наверное, нет.\\pТа белая рука у тебя на плече...\\nМне просто показалось.$",
"LavenderTown_Text_TownKnownAsMonGraveSite":"Этот город известен как место\\nзахоронения ПОКЕМОНОВ.\\pВ БАШНЕ ПОКЕМОНОВ проводят\\nпоминальные службы.$",
"LavenderTown_Text_GhostsAppearedInTower":"В БАШНЕ ПОКЕМОНОВ\\nпоявились призраки.\\pДумаю, это духи ПОКЕМОНОВ,\\nкоторых убила КОМАНДА R.$",
"LavenderTown_Text_TownSign":"ЛАВАНДЕР-ТАУН\\nБлагородный фиолетовый город$",
"LavenderTown_Text_SilphScopeNotice":"Новый СИЛФ-СКОУП!\\nСделай невидимое видимым!\\pСИЛФ КО.$",
"LavenderTown_Text_VolunteerPokemonHouse":"ДОМ ДОБРОВОЛЬЦЕВ\\nЛАВАНДЕРА$",
"LavenderTown_Text_PokemonTowerSign":"БАШНЯ ПОКЕМОНОВ\\nУпокой души ПОКЕМОНОВ$",
},
"data/maps/FuchsiaCity_House2_Frlg/scripts.inc":{
"FuchsiaCity_House2_Text_DoYouLikeToFish":"Я старший брат РЫБОЛОВНОГО ГУРУ.\\pЯ просто обожаю рыбалку!\\nНе могу без неё.\\pСкажи, ты любишь рыбачить?$",
"FuchsiaCity_House2_Text_LikeYourStyleTakeThis":"Отлично! Мне нравится твой стиль.\\nДумаю, мы подружимся.\\pБери это и рыбачь, юный друг!$",
"FuchsiaCity_House2_Text_ReceivedGoodRod":"{PLAYER} получил ХОРОШУЮ УДОЧКУ\\nот брата РЫБОЛОВНОГО ГУРУ.$",
"FuchsiaCity_House2_Text_GoodRodCanCatchBetterMons":"Рыбалка - это образ жизни!\\nОна как лучшая поэзия.\\pСТАРАЯ УДОЧКА ловит только\\nMAGIKARP, верно?\\pА ХОРОШЕЙ УДОЧКОЙ можно\\nпоймать куда лучших ПОКЕМОНОВ.$",
"FuchsiaCity_House2_Text_OhThatsDisappointing":"Ох...\\nКак жаль...$",
"FuchsiaCity_House2_Text_HowAreTheFishBiting":"Привет, {PLAYER}!\\pНу как, рыба клюёт?$",
"FuchsiaCity_House2_Text_YouHaveNoRoomForGift":"О нет!\\pУ меня был для тебя подарок,\\nно в СУМКЕ нет места!$",
},
"data/maps/VermilionCity_House1_Frlg/scripts.inc":{
"VermilionCity_House1_Text_ImFishingGuruDoYouLikeToFish":"Я РЫБОЛОВНЫЙ ГУРУ!\\pЯ просто обожаю рыбалку!\\nНе могу без неё.\\pСкажи, ты любишь рыбачить?$",
"VermilionCity_House1_Text_TakeThisAndFish":"Отлично! Мне нравится твой стиль.\\nДумаю, мы подружимся.\\pБери это и рыбачь, юный друг!$",
"VermilionCity_House1_Text_ReceivedOldRodFromFishingGuru":"{PLAYER} получил СТАРУЮ УДОЧКУ\\nот РЫБОЛОВНОГО ГУРУ.$",
"VermilionCity_House1_Text_FishingIsAWayOfLife":"Рыбалка - это образ жизни!\\nОна как лучшая поэзия.\\pМоре или река - иди и поймай\\nнастоящего гиганта, мой друг!$",
"VermilionCity_House1_Text_OhThatsSoDisappointing":"Ох...\\nКак жаль...$",
"VermilionCity_House1_Text_HowAreTheFishBiting":"Привет, {PLAYER}!\\pНу как, рыба клюёт?$",
"VermilionCity_House1_Text_NoRoomForNiceGift":"О нет!\\pУ меня был для тебя подарок,\\nно в СУМКЕ нет места!$",
},
}
EXPECTED_TOTAL=23

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
    audit=root/'build'/'qarro_ru_lavender_fishing_v3_125_audit.json'; audit.parent.mkdir(parents=True,exist_ok=True)
    audit.write_text(json.dumps({"marker":MARKER,"translatedBlockCount":EXPECTED_TOTAL,"translatedByFile":by,"fishingRodRewardFlagLogicTouched":False,"mapTransitionLogicTouched":False,"trainerDataTouched":False,"pokemonMoveAbilityProperNamesPolicy":"English","ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; rod/map/trainer/Ash logic untouched")
    return 0
if __name__=='__main__': raise SystemExit(main())
