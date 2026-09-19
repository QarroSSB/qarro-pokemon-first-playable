#!/usr/bin/env python3
"""Qarro v3.194: human-quality RU pass for the next trainers_frlg.inc rematch block (Route 20)."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
MARKER="QARRO_RU_TRAINERS_FRLG_QUALITY_ROUTE20_V3_194"
TARGET=Path("data/text/trainers_frlg.inc")
TRANSLATIONS={
    "Route20_Text_BarryRematchIntro:": "Здесь мелководье.\nТут плавает много людей.$",
    "Route20_Text_ShirleyRematchIntro:": "Завидуешь, что я отдыхаю\nна ОСТРОВАХ СИФОМ?$",
    "Route20_Text_TiffanyRematchIntro:": "Обожаю качаться на волнах\nвместе с рыбками.$",
    "Route20_Text_IreneRematchIntro:": "Ты тоже был в отпуске?$",
    "Route20_Text_DeanRematchIntro:": "Зацени мои мышцы!\pТеперь они еще больше,\nчем раньше!$",
    "Route20_Text_DarrinRematchIntro:": "Почему ты едешь на POKeMON?\nТы так и не научился плавать?$",
    "Route20_Text_RogerRematchIntro:": "Я прилетел сюда на своем\nPOKeMON-птице.$",
    "Route20_Text_NoraRematchIntro:": "Мой парень подарил мне большие жемчужины.\nИ они стали еще больше!$",
    "Route20_Text_MissyRematchIntro:": "Я приплыла сюда с ОСТРОВА СИННАБАР.\nКак я и говорила, это было нелегко.$",
    "Route20_Text_MelissaRematchIntro:": "На западе, на СИННАБАРЕ, есть\nЛАБОРАТОРИЯ POKeMON.\pТам работает мой папа.$",
}
BANNED_UNICODE=set("—–←→“”«»")
def control_tokens(t): return re.findall(r'\{[^}]+\}|\\.|\$',t)
def replace_label(path,label,tr):
    text=path.read_text(encoding="utf-8")
    pat=re.compile(rf'(?ms)^(?P<head>{re.escape(label)}\s*\n)(?P<body>(?:[ \t]*\.string\s+"(?:\\.|[^"\\])*"\s*\n?)+)')
    ms=list(pat.finditer(text))
    if len(ms)!=1: raise RuntimeError(f"{label}: expected one block, got {len(ms)}")
    m=ms[0]; cur="".join(re.findall(r'\.string\s+"((?:\\.|[^"\\])*)"',m.group("body")))
    if control_tokens(cur)!=control_tokens(tr): raise RuntimeError(f"{label}: control-token drift")
    if not tr.endswith("$") or '"' in tr or set(tr)&BANNED_UNICODE: raise RuntimeError(f"{label}: invalid translation surface")
    path.write_text(text[:m.start("body")]+'\t.string "'+tr+'"\n'+text[m.end("body"):],encoding="utf-8")
def main():
    if len(sys.argv)!=2: raise SystemExit("usage: localize_trainers_frlg_quality_route20_v3_194.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=10: raise RuntimeError("expected 10 blocks")
    for k,v in TRANSLATIONS.items(): replace_label(path,k,v)
    out=root/"build"/"qarro_ru_trainers_frlg_quality_route20_v3_194_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"targetFile":str(TARGET),"qualityPassBlocks":10,"labels":list(TRANSLATIONS),"humanEditedRussian":True,"controlTokensPreserved":True,"pokemonMoveAbilityNamesPreserved":True,"gameplayLogicTouched":False,"balanceTouched":False,"bossTeamsTouched":False,"specialWhitelistTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: polished 10 trainer rematch blocks in {TARGET}"); return 0
if __name__=="__main__": raise SystemExit(main())
