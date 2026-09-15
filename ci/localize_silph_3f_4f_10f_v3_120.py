#!/usr/bin/env python3
"""Qarro v3.120: localize residual Silph Co. 3F/4F/10F runtime text.

Translates exactly 30 English-only FireRed runtime blocks after v3.119:
  * SilphCo_3F_Frlg: 9
  * SilphCo_4F_Frlg: 12
  * SilphCo_10F_Frlg: 9

Pokemon species, Move and Ability proper names remain English by project canon.
Trainer IDs/parties, Silph door flags and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_SILPH_3F_4F_10F_V3_120"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES = {
"data/maps/SilphCo_3F_Frlg/scripts.inc": {
"SilphCo_3F_Text_WhatAmIToDo": "Я работаю в SILPH CO.\\nЧто же мне делать?$",
"SilphCo_3F_Text_YouAndYourMonsSavedUs": "{PLAYER}!\\nТы и твои ПОКЕМОНЫ спасли нас!$",
"SilphCo_3F_Text_GruntIntro": "Хватит нам мешать, мелкий!$",
"SilphCo_3F_Text_GruntDefeat": "Сдаюсь!$",
"SilphCo_3F_Text_GruntPostBattle": "Подсказку хочешь? Двери открываются\\nс помощью CARD KEY!$",
"SilphCo_3F_Text_JoseIntro": "Я поддерживаю КОМАНДУ R сильнее,\\nчем SILPH CO.!$",
"SilphCo_3F_Text_JoseDefeat": "Ты меня достал!$",
"SilphCo_3F_Text_JosePostBattle": "Хм...\\pКОМАНДА R сказала, что если я им\\nпомогу, мне разрешат изучать ПОКЕМОНОВ.$",
"SilphCo_3F_Text_FloorSign": "ГЛАВНЫЙ ОФИС SILPH CO.\\n3F$",
},
"data/maps/SilphCo_4F_Frlg/scripts.inc": {
"SilphCo_4F_Text_CantYouSeeImHiding": "Тс-с!\\nНе видишь, я прячусь?$",
"SilphCo_4F_Text_TeamRocketIsGone": "Что?\\nКОМАНДА R ушла?$",
"SilphCo_4F_Text_Grunt1Intro": "КОМАНДА R захватила\\nSILPH CO.!$",
"SilphCo_4F_Text_Grunt1Defeat": "Ар-р-р!$",
"SilphCo_4F_Text_Grunt1PostBattle": "Фва-ха-ха!\\nНаш БОСС давно охотился за этим местом!$",
"SilphCo_4F_Text_RodneyIntro": "Мой ПОКЕМОН - мой верный слуга.$",
"SilphCo_4F_Text_RodneyDefeat": "Чёрт!\\nБесполезный ПОКЕМОН!$",
"SilphCo_4F_Text_RodneyPostBattle": "Двери заперты электронными\\nзамками.\\pЧтобы открыть их, нужен CARD KEY.$",
"SilphCo_4F_Text_Grunt2Intro": "Обнаружен нарушитель!$",
"SilphCo_4F_Text_Grunt2Defeat": "Ты кто такой?$",
"SilphCo_4F_Text_Grunt2PostBattle": "Лучше доложу БОССУ на 11F!$",
"SilphCo_4F_Text_FloorSign": "ГЛАВНЫЙ ОФИС SILPH CO.\\n4F$",
},
"data/maps/SilphCo_10F_Frlg/scripts.inc": {
"SilphCo_10F_Text_GruntIntro": "Добро пожаловать на 10F!\\nКак мило, что заглянул!$",
"SilphCo_10F_Text_GruntDefeat": "Я ошеломлён!$",
"SilphCo_10F_Text_GruntPostBattle": "Хорошая попытка, но зал заседаний\\nна этаж выше.$",
"SilphCo_10F_Text_TravisIntro": "Хватит этих глупых игр!$",
"SilphCo_10F_Text_TravisDefeat": "Попытки закончились!$",
"SilphCo_10F_Text_TravisPostBattle": "Доволен, что победил меня?\\nТогда иди домой!$",
"SilphCo_10F_Text_WaaaImScared": "А-а-а-а!\\nМне страшно!$",
"SilphCo_10F_Text_KeepMeCryingASecret": "Только никому не говори,\\nчто я плакала...$",
"SilphCo_10F_Text_FloorSign": "ГЛАВНЫЙ ОФИС SILPH CO.\\n10F$",
},
}
EXPECTED_TOTAL = 30

def die(msg): raise SystemExit(f"[{MARKER}] ERROR: {msg}")
def validate_translation(label, translated):
    if not translated.endswith('$'): die(f"{label}: must end with $")
    if '\n' in translated or '\r' in translated: die(f"{label}: physical newline")
    if any(ch in translated for ch in ('—','–','“','”','’','…','«','»')): die(f"{label}: unsupported punctuation")
    if '\\\\' in translated: die(f"{label}: doubled runtime backslash")
    if not re.search(r'[А-Яа-яЁё]', translated): die(f"{label}: expected Cyrillic")
def block_bounds(text,label):
    ms=list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(ms)!=1: die(f"{label}: expected one label, got {len(ms)}")
    start=ms[0].start(); nxt=LABEL_RE.search(text,ms[0].end()); end=nxt.start() if nxt else len(text)
    return start,end,text[start:end]
def replace_block(text,label,translated):
    start,end,old=block_bounds(text,label)
    if re.search(r'[А-Яа-яЁё]',old): die(f"{label}: already Cyrillic")
    if '.string ' not in old: die(f"{label}: not text block")
    safe=translated.replace('"','\\"')
    return text[:start]+f'{label}::\n\t.string "{safe}"\n\n'+text[end:]
def validate_written(rel,text):
    for n,line in enumerate(text.splitlines(),1):
        if '.string "' in line and line.count('"')<2: die(f"{rel}:{n}: broken string")
    if re.search(r'\\\\[npl]',text): die(f"{rel}: doubled runtime escape")
def main():
    if len(sys.argv)!=2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>",file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve(); total=0; by={}
    for rel_s, patches in FILES.items():
        path=root/rel_s
        if not path.is_file(): die(f"missing target: {rel_s}")
        text=path.read_text(encoding='utf-8')
        for label,tr in patches.items(): validate_translation(label,tr); text=replace_block(text,label,tr)
        validate_written(Path(rel_s),text); path.write_text(text,encoding='utf-8'); by[rel_s]=len(patches); total+=len(patches)
    if total!=EXPECTED_TOTAL: die(f"expected {EXPECTED_TOTAL}, got {total}")
    audit=root/'build'/'qarro_ru_silph_3f_4f_10f_v3_120_audit.json'; audit.parent.mkdir(parents=True,exist_ok=True)
    audit.write_text(json.dumps({"marker":MARKER,"translatedBlockCount":EXPECTED_TOTAL,"translatedByFile":by,"trainerDataTouched":False,"doorLogicTouched":False,"pokemonMoveAbilityNamesPolicy":"English","ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} Silph runtime blocks; trainer/door/Ash logic untouched")
    return 0
if __name__=='__main__': raise SystemExit(main())
