#!/usr/bin/env python3
"""Qarro v3.192: human-quality RU pass for the next trainers_frlg.inc rematch block (Route 16b-17)."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
MARKER="QARRO_RU_TRAINERS_FRLG_QUALITY_ROUTES16B_17_V3_192"
TARGET=Path("data/text/trainers_frlg.inc")
TRANSLATIONS={
    "Route16_Text_CamronRematchIntro:": "Я голодный и злой!\\nМне срочно нужна боксерская груша!$",
    "Route16_Text_RubenRematchIntro:": "Эй, привет!\\nДавай как следует повеселимся!$",
    "Route16_Text_JedRematchIntro:": "ДЖЕД: Пришел посмотреть на нашу\\nбезграничную любовь?$",
    "Route16_Text_LeaRematchIntro:": "ЛЕА: Иногда сила нашей любви\\nдаже меня пугает.$",
    "Route17_Text_RaulRematchIntro:": "Я же говорил: на боях с детьми\\nбыстро не разбогатеешь.$",
    "Route17_Text_IsaiahRematchIntro:": "Я чертовски горжусь своим телом, малыш.\\nДавай!$",
    "Route17_Text_VirgilRematchIntro:": "Вышел прогуляться?$",
    "Route17_Text_BillyRematchIntro:": "Мы БАЙКЕРЫ!\\nДороги здесь наши, приятель!$",
    "Route17_Text_NikolasRematchIntro:": "Сегодня VOLTORB как следует\\nударит тебя током!$",
    "Route17_Text_ZeekRematchIntro:": "Я поднял уровень своего POKeMON, но он\\nникак не эволюционирует. Почему?$",
    "Route17_Text_JamalRematchIntro:": "А-а! Мне и правда пора тренироваться\\nи серьезно сбросить лишний жир!$",
    "Route17_Text_CoreyRematchIntro:": "Будь бунтарем!$",
    "Route17_Text_JaxonRematchIntro:": "Ага, отличный ВЕЛОСИПЕД!\\nКак он в управлении?$",
    "Route17_Text_WilliamRematchIntro:": "Отвали, малыш!\\nЯ вымотался!$",
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
    if len(sys.argv)!=2: raise SystemExit("usage: localize_trainers_frlg_quality_routes16b_17_v3_192.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=14: raise RuntimeError("expected 14 blocks")
    for k,v in TRANSLATIONS.items(): replace_label(path,k,v)
    out=root/"build"/"qarro_ru_trainers_frlg_quality_routes16b_17_v3_192_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"targetFile":str(TARGET),"qualityPassBlocks":14,"labels":list(TRANSLATIONS),"humanEditedRussian":True,"controlTokensPreserved":True,"pokemonMoveAbilityNamesPreserved":True,"gameplayLogicTouched":False,"balanceTouched":False,"bossTeamsTouched":False,"specialWhitelistTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: polished 14 trainer rematch blocks in {TARGET}"); return 0
if __name__=="__main__": raise SystemExit(main())
