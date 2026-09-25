#!/usr/bin/env python3
"""Qarro v3.197: human-quality cleanup for obvious broken src/strings.c UI labels."""
from __future__ import annotations
import json,re,sys
from pathlib import Path

MARKER="QARRO_RU_STRINGS_UI_QUALITY_V3_197"
TARGET=Path("src/strings.c")
TRANSLATIONS={
    "gText_Dad": "ПАПА",
    "gText_Mom": "МАМА",
    "gText_CoolnessContest": "КОНКУРС КРУТОСТИ",
    "gText_BeautyContest": "КОНКУРС КРАСОТЫ",
    "gText_CutenessContest": "КОНКУРС МИЛОВИДНОСТИ",
    "gText_SmartnessContest": "КОНКУРС УМА",
    "gText_ToughnessContest": "КОНКУРС СТОЙКОСТИ",
    "gText_OpenLevel": "ОТКРЫТЫЙ УРОВЕНЬ",
    "gText_BattleFrontier": "БОЕВОЙ РУБЕЖ",
    "gText_Super": "СУПЕР",
    "gText_Hyper": "ГИПЕР",
    "gText_Master": "МАСТЕР",
    "gText_SomeonesPC": "ЧЕЙ-ТО ПК",
    "gText_LanettesPC": "ПК ЛАНЕТТ",
    "gText_BillsPc": "ПК БИЛЛА",
    "gText_PlayersPC": "ПК {PLAYER}",
    "gText_Single2": "ОДИНОЧНЫЙ",
    "gText_Double2": "ДВОЙНОЙ",
    "gText_Multi": "МУЛЬТИ",
    "gText_MultiLink": "МУЛЬТИ-СВЯЗЬ",
    "gText_SouthernIsland": "ЮЖНЫЙ ОСТРОВ",
    "gText_FarawayIsland": "ДАЛЕКИЙ ОСТРОВ",
    "gText_NormalTagMatch": "ОБЫЧНЫЙ ТАГ-БОЙ",
    "gText_VarietyTagMatch": "РАЗНЫЙ ТАГ-БОЙ",
    "gText_UniqueTagMatch": "ОСОБЫЙ ТАГ-БОЙ",
    "gText_ExpertTagMatch": "ЭКСПЕРТНЫЙ ТАГ-БОЙ",
    "gText_BattleBasics": "ОСНОВЫ БОЯ",
    "gText_Underpowered": "НЕХВАТКА СИЛЫ",
    "gText_WhenInDanger": "ПРИ ОПАСНОСТИ",
    "gText_BattleTrainers": "ТРЕНЕРЫ В БОЮ",
    "gText_ElevatorNowOn": "СЕЙЧАС:",
    "gText_BP": "BP",
    "gText_RankingHall": "ЗАЛ РЕЙТИНГА",
    "gText_ExchangeService": "ОБМЕН",
    "gText_SlateportCity": "СЛЕЙТПОРТ-СИТИ",
    "gText_Ferry": "ПАРОМ",
    "gText_SecretBase": "СЕКРЕТНАЯ БАЗА",
    "gText_Hideout": "УБЕЖИЩЕ",
    "gText_Spicy2": "ОСТРЫЙ",
    "gText_Dry2": "СУХОЙ",
    "gText_Sweet2": "СЛАДКИЙ",
    "gText_Bitter2": "ГОРЬКИЙ",
    "gText_Sour2": "КИСЛЫЙ",
    "gText_Single": "ОДИНОЧНЫЙ",
    "gText_Double": "ДВОЙНОЙ",
    "gText_Knockout": "НОКАУТ",
    "gText_Mixed": "СМЕШАННЫЙ",
    "gText_Points": " ОЧК.",
    "gText_NumBP": "{STR_VAR_1}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}BP",
    "gText_OpenLv": "ОТКР. УР.",
    "gText_RecordsOpenLevel": "ОТКРЫТЫЙ УРОВЕНЬ",
    "gText_Peekaboo": "КУ-КУ!",
    "gText_DexHoenn": "HOENN",
    "gText_DexNational": "НАЦИОНАЛЬНЫЙ",
    "gText_Hoenn": "HOENN",
    "gText_MoveRelearnerType": "ТИП/",
    "gText_IsThisTheCorrectTime": "Время указано верно?",
    "gText_Confirm3": "ПОДТВЕРДИТЬ",
    "gText_NoWeather": "БЕЗ ПОГОДЫ",
    "gText_Sunny": "СОЛНЕЧНО",
    "gText_Rain": "ДОЖДЬ",
    "gText_Snow": "СНЕГ",
    "gText_Lightning": "МОЛНИЯ",
    "gText_VolcanoAsh": "ВУЛКАНИЧЕСКИЙ ПЕПЕЛ",
    "gText_Seafloor2": "МОРСКОЕ ДНО 2",
    "gText_DelAll": "УДАЛ. ВСЕ",
    "gText_Ok2": "ОК",
}
EXACT_REPLACEMENTS=[
    ("[POCKET_ITEMS]      = COMPOUND_STRING(\"ИТЕМС\"),", "[POCKET_ITEMS]      = COMPOUND_STRING(\"ПРЕДМЕТЫ\"),"),
    ("[POCKET_POKE_BALLS] = COMPOUND_STRING(\"Козьи шары\"),", "[POCKET_POKE_BALLS] = COMPOUND_STRING(\"ПОКЕБОЛЫ\"),"),
    ("[POCKET_BERRIES]    = COMPOUND_STRING(\"БЕРРИЗ\"),", "[POCKET_BERRIES]    = COMPOUND_STRING(\"ЯГОДЫ\"),"),
    ("[POCKET_KEY_ITEMS]  = COMPOUND_STRING(\"Ключевые ИТЕМЫ\")", "[POCKET_KEY_ITEMS]  = COMPOUND_STRING(\"КЛЮЧ. ПРЕДМ.\")"),
]
BANNED_UNICODE=set("—–←→“”«»")

def control_tokens(text):
    return re.findall(r'\{[^}]+\}|\\[npl]|\$', text)

def replace_symbol(path,symbol,translated):
    text=path.read_text(encoding="utf-8")
    pat=re.compile(
        rf'(?m)^(?P<prefix>\s*(?:ALIGNED\(4\)\s+)?(?:static\s+)?const u8\s+'
        rf'{re.escape(symbol)}\[\]\s*=\s*_\(")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\);(?:\s*//.*)?\s*)$'
    )
    ms=list(pat.finditer(text))
    if len(ms)!=1: raise RuntimeError(f"{symbol}: expected one symbol, got {len(ms)}")
    m=ms[0]; current=m.group("body")
    if control_tokens(current)!=control_tokens(translated):
        raise RuntimeError(f"{symbol}: control-token drift old={control_tokens(current)} new={control_tokens(translated)}")
    if '"' in translated or set(translated)&BANNED_UNICODE:
        raise RuntimeError(f"{symbol}: invalid translation surface")
    path.write_text(text[:m.start()]+m.group("prefix")+translated+m.group("suffix")+text[m.end():],encoding="utf-8")

def replace_exact(path,old,new):
    text=path.read_text(encoding="utf-8")
    count=text.count(old)
    if count!=1: raise RuntimeError(f"exact UI anchor expected once, got {count}: {old}")
    path.write_text(text.replace(old,new,1),encoding="utf-8")

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: localize_strings_ui_quality_v3_197.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=67: raise RuntimeError(f"expected 67 symbols, got {len(TRANSLATIONS)}")
    for sym,tr in TRANSLATIONS.items(): replace_symbol(path,sym,tr)
    for old,new in EXACT_REPLACEMENTS: replace_exact(path,old,new)
    out=root/"build"/"qarro_ru_strings_ui_quality_v3_197_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        "marker":MARKER,"targetFile":str(TARGET),
        "qualityPassSymbols":len(TRANSLATIONS),
        "exactUiReplacements":len(EXACT_REPLACEMENTS),
        "symbols":list(TRANSLATIONS),
        "humanEditedRussian":True,"controlTokensPreserved":True,
        "pokemonMoveAbilityNamesPreserved":True,
        "gameplayLogicTouched":False,"balanceTouched":False,
        "bossTeamsTouched":False,"specialWhitelistTouched":False,
        "ashBondTouched":False,"ashCapTouched":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} symbols + {len(EXACT_REPLACEMENTS)} pocket labels")
    return 0

if __name__=="__main__": raise SystemExit(main())
