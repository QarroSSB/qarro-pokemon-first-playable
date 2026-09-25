#!/usr/bin/env python3
"""Qarro v3.122: localize Tanoby Ruins and Five Island Meadow runtime text.

Translates exactly 24 English-only FireRed runtime blocks after v3.121:
  * SevenIsland_TanobyRuins_Frlg: 12
  * FiveIsland_Meadow_Frlg: 12

The gameplay password phrases remain exactly English. The unused Japanese
Meadow block is untouched. Trainer IDs/parties, Warehouse door/password logic
and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
MARKER="QARRO_RU_TANOBY_MEADOW_V3_122"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES={
"data/maps/SevenIsland_TanobyRuins_Frlg/scripts.inc":{
"SevenIsland_TanobyRuins_Text_BrandonIntro":"Ты что-нибудь знаешь\\nоб этой каменной комнате?$",
"SevenIsland_TanobyRuins_Text_BrandonDefeat":"Это было лишнее.\\nНе обязательно было так жестоко.$",
"SevenIsland_TanobyRuins_Text_BrandonPostBattle":"РУИНАМ ТАНОБИ не меньше\\n1500 лет.\\pНо зачем их вообще построили -\\nдо сих пор загадка.$",
"SevenIsland_TanobyRuins_Text_BenjaminIntro":"Говорят, внутри спит\\nтаинственный ПОКЕМОН.$",
"SevenIsland_TanobyRuins_Text_BenjaminDefeat":"В бою я не очень хорош.$",
"SevenIsland_TanobyRuins_Text_BenjaminPostBattle":"Говорят, есть и другие\\nподобные руины.\\pМожет, там тоже покоятся\\nтаинственные ПОКЕМОНЫ?$",
"SevenIsland_TanobyRuins_Text_EdnaIntro":"CLIFFORD учит меня рисовать.$",
"SevenIsland_TanobyRuins_Text_EdnaDefeat":"Нас могут отругать за шум.$",
"SevenIsland_TanobyRuins_Text_EdnaPostBattle":"Я сказала, что хочу нарисовать\\nстаринное здание.\\pПоэтому CLIFFORD привёл меня сюда.$",
"SevenIsland_TanobyRuins_Text_CliffordIntro":"Сегодня кроме урока мы пришли\\nпосмотреть на эту комнату.$",
"SevenIsland_TanobyRuins_Text_CliffordDefeat":"Вот это необычно.$",
"SevenIsland_TanobyRuins_Text_CliffordPostBattle":"А, так ты самостоятельно\\nизучаешь ПОКЕМОНОВ...\\pДа, ты и правда очень\\nнеобычный человек.$",
},
"data/maps/FiveIsland_Meadow_Frlg/scripts.inc":{
"FiveIsland_Meadow_Text_EnteredPasswordAnotherNeeded":"{PLAYER} ввёл пароль.\\pGOLDEEN need log.\\p... ... ...\\pЧтобы открыть дверь, нужен\\nещё один пароль...$",
"FiveIsland_Meadow_Text_EnteredPasswordDoorOpened":"{PLAYER} ввёл два пароля.\\pGOLDEEN need log.\\nYes, nah, CHANSEY.\\p... ... ...\\pДверь СКЛАДА открылась!$",
"FiveIsland_Meadow_Text_WarehouseDoorAlreadyOpen":"Дверь СКЛАДА уже открыта.$",
"FiveIsland_Meadow_Text_Rocket1Intro":"Сюда посторонним строго нельзя!\\nПроваливай!$",
"FiveIsland_Meadow_Text_Rocket1Defeat":"Это серьёзно?$",
"FiveIsland_Meadow_Text_Rocket1PostBattle":"Тебе здесь нечего делать!\\nИди домой!$",
"FiveIsland_Meadow_Text_Rocket2Intro":"Дальше нет ничего, кроме\\nнашего СКЛАДА.\\pТак зачем ты сюда пришёл?$",
"FiveIsland_Meadow_Text_Rocket2Defeat":"Такого не должно было случиться...$",
"FiveIsland_Meadow_Text_Rocket2PostBattle":"Хочешь узнать, что внутри СКЛАДА?\\pЛучше тебе этого не знать.\\nДля твоего же блага.$",
"FiveIsland_Meadow_Text_Rocket3Intro":"Даже если пройдёшь мимо меня,\\nтолько зря потратишь время.$",
"FiveIsland_Meadow_Text_Rocket3Defeat":"Ох, как же я злюсь!$",
"FiveIsland_Meadow_Text_Rocket3PostBattle":"Всё равно без паролей\\nтебе внутрь не попасть.$",
},
}
EXPECTED_TOTAL=24

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
    audit=root/'build'/'qarro_ru_tanoby_meadow_v3_122_audit.json'; audit.parent.mkdir(parents=True,exist_ok=True)
    audit.write_text(json.dumps({"marker":MARKER,"translatedBlockCount":EXPECTED_TOTAL,"translatedByFile":by,"passwordPhrasesPreservedEnglish":True,"unusedJapaneseTextTouched":False,"trainerDataTouched":False,"warehouseDoorPasswordLogicTouched":False,"pokemonMoveAbilityNamesPolicy":"English","ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks; password phrases preserved; trainer/door/unused-Japanese/Ash logic untouched")
    return 0
if __name__=='__main__': raise SystemExit(main())
