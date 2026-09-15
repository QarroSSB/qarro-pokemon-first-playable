#!/usr/bin/env python3
"""Qarro v3.124: localize Route 18 and Lavender Name Rater runtime text.

Translates exactly 20 English-only FireRed runtime blocks after v3.123:
  * Route18_Frlg: 11
  * LavenderTown_House2_Frlg: 9

Cycling Road state/warp logic, Name Rater nickname logic, trainer data,
Pokemon/Move/Ability proper-name policy, and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
MARKER="QARRO_RU_ROUTE18_NAME_RATER_V3_124"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES={
"data/maps/Route18_Frlg/scripts.inc":{
"Route18_Text_WiltonIntro":"Я всегда проверяю каждую травяную\\nполяну в поисках новых ПОКЕМОНОВ.$",
"Route18_Text_WiltonDefeat":"Тц!$",
"Route18_Text_WiltonPostBattle":"Вот бы у меня был ВЕЛОСИПЕД!$",
"Route18_Text_RamiroIntro":"Курукку!\\nНу как тебе мой птичий крик?$",
"Route18_Text_RamiroDefeat":"Надо же было к тебе пристать!$",
"Route18_Text_RamiroPostBattle":"По выходным я ловлю морских\\nПОКЕМОНОВ - море совсем рядом.$",
"Route18_Text_JacobIntro":"Это моя территория!\\nУбирайся отсюда!$",
"Route18_Text_JacobDefeat":"Чёрт!$",
"Route18_Text_JacobPostBattle":"Это моё любимое место\\nдля ловли ПОКЕМОНОВ.$",
"Route18_Text_RouteSign":"МАРШРУТ 18\\nСЕЛАДОН-СИТИ - ФУКСИЯ-СИТИ$",
"Route18_Text_CyclingRoadSign":"ВЕЛОДОРОГА\\nПешеходам вход запрещён!$",
},
"data/maps/LavenderTown_House2_Frlg/scripts.inc":{
"LavenderTown_House2_Text_WantMeToRateNicknames":"Привет, привет!\\nЯ официальный ОЦЕНЩИК ИМЁН!\\pХочешь, я оценю клички\\nтвоих ПОКЕМОНОВ?$",
"LavenderTown_House2_Text_CritiqueWhichMonsNickname":"Кличку какого ПОКЕМОНА\\nмне оценить?$",
"LavenderTown_House2_Text_GiveItANicerName":"{STR_VAR_1}, значит?\\nНеплохая кличка!\\pНо хочешь, я дам ему\\nимя получше?\\pКак тебе идея?$",
"LavenderTown_House2_Text_WhatShallNewNicknameBe":"Отлично. Какой будет\\nновая кличка?$",
"LavenderTown_House2_Text_FromNowOnShallBeKnownAsName":"Готово! Теперь этого ПОКЕМОНА\\nбудут звать {STR_VAR_1}!\\pИмя стало лучше прежнего!\\nТебе повезло!$",
"LavenderTown_House2_Text_ISeeComeVisitAgain":"Понятно.\\nЗаходи ещё.$",
"LavenderTown_House2_Text_FromNowOnShallBeKnownAsSameName":"Готово! Теперь этого ПОКЕМОНА\\nбудут звать {STR_VAR_1}!\\pНа вид ничего не изменилось,\\nно теперь имя намного лучше!\\pТебе повезло!$",
"LavenderTown_House2_Text_TrulyImpeccableName":"{STR_VAR_1}, значит?\\nБезупречное имя!\\pБереги {STR_VAR_1}!$",
"LavenderTown_House2_Text_ThatIsMerelyAnEgg":"Ну-ну.\\nЭто всего лишь ЯЙЦО!$",
},
}
EXPECTED_TOTAL=20

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
    audit=root/'build'/'qarro_ru_route18_name_rater_v3_124_audit.json'; audit.parent.mkdir(parents=True,exist_ok=True)
    audit.write_text(json.dumps({"marker":MARKER,"translatedBlockCount":EXPECTED_TOTAL,"translatedByFile":by,"cyclingRoadLogicTouched":False,"nameRaterLogicTouched":False,"trainerDataTouched":False,"pokemonMoveAbilityProperNamesPolicy":"English","ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; Cycling Road/Name Rater/trainer/Ash logic untouched")
    return 0
if __name__=='__main__': raise SystemExit(main())
