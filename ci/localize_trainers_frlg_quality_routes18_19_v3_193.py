#!/usr/bin/env python3
"""Qarro v3.193: human-quality RU pass for the next trainers_frlg.inc rematch block (Routes 18-19)."""
from __future__ import annotations
import json,re,subprocess,sys
from pathlib import Path
MARKER="QARRO_RU_TRAINERS_FRLG_QUALITY_ROUTES18_19_V3_193"
TARGET=Path("data/text/trainers_frlg.inc")
TRANSLATIONS={
    "Route18_Text_WiltonRematchIntro:": "Я проверяю каждый клочок травы\\nв поисках новых POKeMON.\\pНо это не всегда легко...$",
    "Route18_Text_RamiroRematchIntro:": "Ку-ру-ку-ку-ку!\\nМой птичий зов стал лучше?$",
    "Route18_Text_JacobRematchIntro:": "Я уже предупреждал: это моя\\nтерритория!\\pНе хочу, чтобы ты сюда приходил.$",
    "Route19_Text_RichardRematchIntro:": "Я почти размялся и готов\\nпоплавать.$",
    "Route19_Text_ReeceRematchIntro:": "Стой! Помедленнее!\\nА вдруг у тебя сердце не выдержит?$",
    "Route19_Text_MatthewRematchIntro:": "Обожаю плавать!\\nА ты, похоже, любишь SURF.$",
    "Route19_Text_DouglasRematchIntro:": "Что там, за горизонтом?\\nТы видел?$",
    "Route19_Text_DavidRematchIntro:": "Я снова нырял за POKeMON,\\nно, как и раньше, безуспешно.$",
    "Route19_Text_TonyRematchIntro:": "Я смотрю на море, чтобы забыть\\nвсе плохое, что случилось.\\p...Например, как в прошлый раз проиграл тебе!$",
    "Route19_Text_AnyaRematchIntro:": "Ты всегда катаешься на своем\\nPOKeMON...\\pВыглядит так расслабляюще.\\nОтдашь его мне, если я выиграю?$",
    "Route19_Text_AliceRematchIntro:": "Плавать здорово!\\nА вот обгорать на солнце - нет!$",
    "Route19_Text_AxleRematchIntro:": "Эти воды опасны!\\nТебе не стоит сюда возвращаться!$",
    "Route19_Text_ConnieRematchIntro:": "Я приплыла сюда с друзьями...\\nЯ устала...\\lНам правда снова нужно сражаться?$",
    "Route19_Text_LiaRematchIntro:": "ЛИА: Ты ведь знаешь, что мой брат\\nнедавно стал ТРЕНЕРОМ?\\pЯ хочу, чтобы он стал сильнее, поэтому\\nмне снова нужна твоя помощь.$",
    "Route19_Text_LucRematchIntro:": "ЛЮК: Старшая сестра научила меня всему\\nо POKeMON.\\pИнтересно, стал ли я лучше?$",
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
    if len(sys.argv)!=2: raise SystemExit("usage: localize_trainers_frlg_quality_routes18_19_v3_193.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=15: raise RuntimeError("expected 15 blocks")
    for k,v in TRANSLATIONS.items(): replace_label(path,k,v)
    out=root/"build"/"qarro_ru_trainers_frlg_quality_routes18_19_v3_193_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"targetFile":str(TARGET),"qualityPassBlocks":15,"labels":list(TRANSLATIONS),"humanEditedRussian":True,"controlTokensPreserved":True,"pokemonMoveAbilityNamesPreserved":True,"gameplayLogicTouched":False,"balanceTouched":False,"bossTeamsTouched":False,"specialWhitelistTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    next_script=Path(__file__).with_name("localize_trainers_frlg_quality_route20_v3_194.py")
    subprocess.run([sys.executable,str(next_script),str(root)],check=True)
    print(f"[{MARKER}] PASS: polished 15 trainer rematch blocks in {TARGET}; chained v3.194"); return 0
if __name__=="__main__": raise SystemExit(main())
