#!/usr/bin/env python3
"""Qarro v3.121: localize residual Pokemon Tower 3F/4F/6F/7F runtime text.

Translates exactly 39 English-only FireRed runtime blocks after v3.120:
  * PokemonTower_3F_Frlg: 9
  * PokemonTower_4F_Frlg: 9
  * PokemonTower_6F_Frlg: 12
  * PokemonTower_7F_Frlg: 9 Rocket battle blocks

The already-localized Mr. Fuji 7F scene is intentionally untouched.
Pokemon species, Move and Ability proper names remain English by project canon.
Trainer IDs/parties, Marowak scene logic, Mr. Fuji flags/warp and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
MARKER = "QARRO_RU_POKEMON_TOWER_3F_4F_6F_7F_V3_121"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES = {
"data/maps/PokemonTower_3F_Frlg/scripts.inc": {
"PokemonTower_3F_Text_HopeIntro": "Ур-р... А-а...\\nХу-ху... Гра-а...$",
"PokemonTower_3F_Text_HopeDefeat": "А-а!\\nЯ спасена!$",
"PokemonTower_3F_Text_HopePostBattle": "Призраков можно опознать\\nс помощью SILPH SCOPE.$",
"PokemonTower_3F_Text_CarlyIntro": "Ке-ке-ке...\\nКва-а-а!$",
"PokemonTower_3F_Text_CarlyDefeat": "Хм?\\nЧто я делаю?$",
"PokemonTower_3F_Text_CarlyPostBattle": "Прости!\\nЯ была одержима!$",
"PokemonTower_3F_Text_PatriciaIntro": "Прочь!\\nЗлобный дух!$",
"PokemonTower_3F_Text_PatriciaDefeat": "Фух!\\nДух ушёл!$",
"PokemonTower_3F_Text_PatriciaPostBattle": "Те, кто выше...\\nНаверное, они тоже одержимы.$",
},
"data/maps/PokemonTower_4F_Frlg/scripts.inc": {
"PokemonTower_4F_Text_PaulaIntro": "Призрак! Нет!\\nКва-а-а!$",
"PokemonTower_4F_Text_PaulaDefeat": "Где призрак?$",
"PokemonTower_4F_Text_PaulaPostBattle": "Наверное, мне всё это приснилось...$",
"PokemonTower_4F_Text_LaurelIntro": "Будь проклят вместе со мной!\\nКва-а-а!$",
"PokemonTower_4F_Text_LaurelDefeat": "Что?!$",
"PokemonTower_4F_Text_LaurelPostBattle": "Мы не можем определить,\\nкто эти призраки...$",
"PokemonTower_4F_Text_JodyIntro": "Ху-ху-ху...\\nНе побеждай меня!$",
"PokemonTower_4F_Text_JodyDefeat": "А?\\nКто? Что?$",
"PokemonTower_4F_Text_JodyPostBattle": "Пусть ушедшие ПОКЕМОНЫ\\nпокоятся с миром...$",
},
"data/maps/PokemonTower_6F_Frlg/scripts.inc": {
"PokemonTower_6F_Text_AngelicaIntro": "Дай... мне...\\nкровь...$",
"PokemonTower_6F_Text_AngelicaDefeat": "У-у-у!$",
"PokemonTower_6F_Text_AngelicaPostBattle": "Я чувствую слабость...\\nСловно у меня малокровие.$",
"PokemonTower_6F_Text_EmiliaIntro": "Урф...\\nКва-а!$",
"PokemonTower_6F_Text_EmiliaDefeat": "Что-то выпало!$",
"PokemonTower_6F_Text_EmiliaPostBattle": "Мои волосы не выпали!\\nЭто был злобный дух!$",
"PokemonTower_6F_Text_JenniferIntro": "Ке... ке... ке...\\nке... ке... ке!$",
"PokemonTower_6F_Text_JenniferDefeat": "Ки-и-и!$",
"PokemonTower_6F_Text_JenniferPostBattle": "Что здесь происходит?$",
"PokemonTower_6F_Text_BeGoneIntruders": "Прочь...\\nНезваные гости...$",
"PokemonTower_6F_Text_GhostWasCubonesMother": "Призрак оказался беспокойным духом\\nматери CUBONE!$",
"PokemonTower_6F_Text_MothersSpiritWasCalmed": "Дух матери успокоился.\\pОн отправился в иной мир...$",
},
"data/maps/PokemonTower_7F_Frlg/scripts.inc": {
"PokemonTower_7F_Text_Grunt1Intro": "Чего тебе надо?\\nЗачем ты здесь?$",
"PokemonTower_7F_Text_Grunt1Defeat": "Сдаюсь!$",
"PokemonTower_7F_Text_Grunt1PostBattle": "Я этого не забуду!$",
"PokemonTower_7F_Text_Grunt2Intro": "Этот старик сам пришёл прямо\\nк нашему УБЕЖИЩУ.\\pА потом начал возмущаться, что\\nКОМАНДА R плохо обращается с ПОКЕМОНАМИ.\\pВот мы и обсуждаем это,\\nкак взрослые.$",
"PokemonTower_7F_Text_Grunt2Defeat": "Прошу!\\nХватит!$",
"PokemonTower_7F_Text_Grunt2PostBattle": "ПОКЕМОНЫ нужны только для денег.\\nПочему бы их не использовать?\\pНе лезь в наши дела!$",
"PokemonTower_7F_Text_Grunt3Intro": "Ты никого не спасёшь, малыш!$",
"PokemonTower_7F_Text_Grunt3Defeat": "Не связывайся с КОМАНДОЙ R!$",
"PokemonTower_7F_Text_Grunt3PostBattle": "Тебе это с рук не сойдёт!$",
},
}
EXPECTED_TOTAL=39

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
    start=ms[0].start(); nxt=LABEL_RE.search(text,ms[0].end()); end=nxt.start() if nxt else len(text)
    return start,end,text[start:end]
def replace_block(text,label,tr):
    start,end,old=block_bounds(text,label)
    if re.search(r'[А-Яа-яЁё]',old): die(f"{label}: already Cyrillic")
    if '.string ' not in old: die(f"{label}: not text block")
    safe=tr.replace('"','\\"')
    return text[:start]+f'{label}::\n\t.string "{safe}"\n\n'+text[end:]
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
    audit=root/'build'/'qarro_ru_pokemon_tower_3f_4f_6f_7f_v3_121_audit.json'; audit.parent.mkdir(parents=True,exist_ok=True)
    audit.write_text(json.dumps({"marker":MARKER,"translatedBlockCount":EXPECTED_TOTAL,"translatedByFile":by,"trainerDataTouched":False,"marowakSceneLogicTouched":False,"mrFujiSceneTouched":False,"pokemonMoveAbilityNamesPolicy":"English","ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"[{MARKER}] PASS: localized {EXPECTED_TOTAL} Pokemon Tower runtime blocks; trainer/Marowak/MrFuji/Ash logic untouched")
    return 0
if __name__=='__main__': raise SystemExit(main())
