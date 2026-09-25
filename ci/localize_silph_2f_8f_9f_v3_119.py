#!/usr/bin/env python3
"""Qarro v3.119: localize residual Silph Co. 2F/8F/9F runtime text.

Translates 43 FireRed runtime blocks after v3.118:
  * SilphCo_2F_Frlg: 13 audit-visible + 4 THUNDER WAVE tutor blind-spot strings
  * SilphCo_8F_Frlg: 13 audit-visible
  * SilphCo_9F_Frlg: 13 audit-visible

Pokemon species, Move and Ability proper names remain English by project canon.
Trainer IDs/parties, Silph door flags, healing logic, Move Tutor logic and
Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_SILPH_2F_8F_9F_V3_119"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
"data/maps/SilphCo_2F_Frlg/scripts.inc": {
"SilphCo_2F_Text_ConnorIntro": "Помогите!\\nЯ сотрудник SILPH.$",
"SilphCo_2F_Text_ConnorDefeat": "Как ты понял, что я\\nиз КОМАНДЫ R?$",
"SilphCo_2F_Text_ConnorPostBattle": "Я работаю и на SILPH,\\nи на КОМАНДУ R.$",
"SilphCo_2F_Text_JerryIntro": "Сюда нельзя!\\nИди домой!$",
"SilphCo_2F_Text_JerryDefeat": "Ты силён.$",
"SilphCo_2F_Text_JerryPostBattle": "Сможешь пройти здешний лабиринт?\\nЭто не так просто!$",
"SilphCo_2F_Text_Grunt1Intro": "Детям сюда нельзя!$",
"SilphCo_2F_Text_Grunt1Defeat": "Крепкий!$",
"SilphCo_2F_Text_Grunt1PostBattle": "Ромбовидные плитки - это\\nтелепорты.\\pОни перемещают людей по этому\\nвысокотехнологичному зданию.$",
"SilphCo_2F_Text_Grunt2Intro": "Эй, малыш!\\nЧего ты здесь бродишь?$",
"SilphCo_2F_Text_Grunt2Defeat": "Я оплошал!$",
"SilphCo_2F_Text_Grunt2PostBattle": "SILPH CO. будет работать\\nвместе с КОМАНДОЙ R!$",
"SilphCo_2F_Text_FloorSign": "ГЛАВНЫЙ ОФИС SILPH CO.\\n2F$",
"Text_ThunderWaveTeach": "А-а!\\nНет! Стой! Помогите!\\pОй, ты не из КОМАНДЫ R.\\nПрости, я ошиблась...\\pПростишь меня, если я научу тебя\\nприёму THUNDER WAVE?$",
"Text_ThunderWaveDeclined": "Ох...\\nНо THUNDER WAVE так полезен...$",
"Text_ThunderWaveWhichMon": "Какого ПОКЕМОНА научить\\nTHUNDER WAVE?$",
"Text_ThunderWaveTaught": "THUNDER WAVE парализует\\nПОКЕМОНА-цель.\\pПарализованный ПОКЕМОН иногда\\nне может двигаться в бою.\\pЭто приём типа ELECTRIC, поэтому\\nна некоторых ПОКЕМОНОВ он не действует.$",
},
"data/maps/SilphCo_8F_Frlg/scripts.inc": {
"SilphCo_8F_Text_WonderIfSilphIsFinished": "Неужели SILPH конец...$",
"SilphCo_8F_Text_ThanksForSavingUs": "Спасибо, что спас нас!$",
"SilphCo_8F_Text_Grunt1Intro": "Дальше ты не пройдёшь!$",
"SilphCo_8F_Text_Grunt1Defeat": "Не хватило упорства!$",
"SilphCo_8F_Text_Grunt1PostBattle": "Если не повернёшь назад...\\nЯ вызову подкрепление!$",
"SilphCo_8F_Text_ParkerIntro": "Из-за тебя у нас одни проблемы!$",
"SilphCo_8F_Text_ParkerDefeat": "Что?\\nЯ проиграл?$",
"SilphCo_8F_Text_ParkerPostBattle": "Ну как тебе лабиринт\\nв здании SILPH?$",
"SilphCo_8F_Text_Grunt2Intro": "Я один из четырёх\\nБРАТЬЕВ КОМАНДЫ R!$",
"SilphCo_8F_Text_Grunt2Defeat": "Ух!\\nО, братья!$",
"SilphCo_8F_Text_Grunt2PostBattle": "Дальше тобой займутся мои братья.$",
"SilphCo_8F_Text_FloorSign": "ГЛАВНЫЙ ОФИС SILPH CO.\\n8F$",
"SilphCo_8F_Text_ToRocketBossMonsAreTools": "ГЛАВА КОМАНДЫ R ужасно жесток!\\pДля него ПОКЕМОНЫ - лишь\\nинструменты.\\pЧто будет, если этот тиран\\nзахватит нашу компанию...$",
},
"data/maps/SilphCo_9F_Frlg/scripts.inc": {
"SilphCo_9F_Text_YouShouldTakeQuickNap": "Ты выглядишь уставшим.\\nТебе стоит немного поспать.$",
"SilphCo_9F_Text_DontGiveUp": "Не сдавайся!$",
"SilphCo_9F_Text_ThankYouSoMuch": "Огромное спасибо.$",
"SilphCo_9F_Text_Grunt1Intro": "Похоже, твои ПОКЕМОНЫ\\nобожают тебя, малыш!$",
"SilphCo_9F_Text_Grunt1Defeat": "Гха-а-а!$",
"SilphCo_9F_Text_Grunt1PostBattle": "Если бы я начал тренироваться\\nв твоём возрасте...$",
"SilphCo_9F_Text_EdIntro": "У твоих ПОКЕМОНОВ есть слабости!\\nЯ ими воспользуюсь!$",
"SilphCo_9F_Text_EdDefeat": "Ты меня разгромил!$",
"SilphCo_9F_Text_EdPostBattle": "Бить по слабым местам полезно.\\nПомни о преимуществах типов.$",
"SilphCo_9F_Text_Grunt2Intro": "Я один из четырёх\\nБРАТЬЕВ КОМАНДЫ R!$",
"SilphCo_9F_Text_Grunt2Defeat": "Аргх!\\nБратья, я проиграл!$",
"SilphCo_9F_Text_Grunt2PostBattle": "Мои братья отомстят за меня!$",
"SilphCo_9F_Text_FloorSign": "ГЛАВНЫЙ ОФИС SILPH CO.\\n9F$",
},
}
EXPECTED_COUNTS = {k: len(v) for k,v in FILES.items()}
EXPECTED_TOTAL = 43
AUDIT_VISIBLE_TOTAL = 39

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
    audit=root/'build'/'qarro_ru_silph_2f_8f_9f_v3_119_audit.json'; audit.parent.mkdir(parents=True,exist_ok=True)
    audit.write_text(json.dumps({"marker":MARKER,"translatedBlockCount":EXPECTED_TOTAL,"auditVisibleBlockCount":AUDIT_VISIBLE_TOTAL,"translatedByFile":by,"trainerDataTouched":False,"doorLogicTouched":False,"healLogicTouched":False,"moveTutorLogicTouched":False,"pokemonMoveAbilityNamesPolicy":"English","ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} runtime blocks ({AUDIT_VISIBLE_TOTAL} audit-visible + 4 THUNDER WAVE tutor blind-spot); trainer/door/heal/tutor/Ash logic untouched")
    return 0
if __name__=='__main__': raise SystemExit(main())
