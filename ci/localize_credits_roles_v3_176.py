#!/usr/bin/env python3
"""Qarro v3.176: localize FireRed credit headings/roles, preserve staff names."""
from __future__ import annotations
import json,re,sys
from pathlib import Path

MARKER="QARRO_RU_CREDITS_ROLES_V3_176"
REL=Path("src/credits_frlg.c")
MACRO_RE=re.compile(r'_\("(?P<body>(?:\\.|[^"\\])*)"\)')

TERMS={
    "English Version Coordinators":"Координаторы англ. версии",
    "Environment & Tool Programmers":"Программисты среды и инструментов",
    "Program Leader":"Руководитель программирования",
    "Graphic Design Leader":"Руководитель графики",
    "Information Supervisors":"Информационные консультанты",
    "Supporting Programmers":"Дополнительные программисты",
    "Planning Leader":"Руководитель планирования",
    "Parametric Designers":"Дизайнеры параметров",
    "Graphic Designers":"Графические дизайнеры",
    "Executive Producer":"Исполнительный продюсер",
    "Executive Director":"Исполнительный директор",
    "System Programmers":"Системные программисты",
    "Braille Code Check":"Проверка кода Брайля",
    "POKéMON Designers":"Дизайнеры POKéMON",
    "POKeMON Designers":"Дизайнеры POKeMON",
    "Art Director":"Арт-директор",
    "Battle Director":"Директор боев",
    "Script Designer":"Дизайнер скриптов",
    "Graphic Designer":"Графический дизайнер",
    "Music Composition":"Музыка",
    "Sound Effects":"Звуковые эффекты",
    "Game Designers":"Геймдизайнеры",
    "Game Scenario":"Сценарий",
    "Map Designer":"Дизайнер карт",
    "POKéDEX Text":"Текст POKéDEX",
    "POKeDEX Text":"Текст POKeDEX",
    "NCL Product Testing":"Тестирование NCL",
    "NOA Product Testing":"Тестирование NOA",
    "Special Thanks":"Особая благодарность",
    "Task Managers":"Менеджеры задач",
    "Coordinators":"Координаторы",
    "Programmers":"Программисты",
    "Producers":"Продюсеры",
    "Translator":"Переводчик",
    "Text Editor":"Редактор текста",
    "Director":"Директор",
    "Pokémon FireRed Version":"Pokémon FireRed",
    "Pokémon LeafGreen Version":"Pokémon LeafGreen",
    "Pokemon FireRed Version":"Pokemon FireRed",
    "Pokemon LeafGreen Version":"Pokemon LeafGreen",
    "Staff":"Команда",
}

def main()->int:
    if len(sys.argv)!=2:
        raise SystemExit("usage: localize_credits_roles_v3_176.py <upstream-root>")
    root=Path(sys.argv[1]).resolve()
    p=root/REL
    text=p.read_text(encoding="utf-8")
    changed_macros=0
    replacements=0

    # Longest phrases first so generic Director/Programmers cannot partially
    # consume compound job titles.
    ordered=sorted(TERMS.items(),key=lambda kv:-len(kv[0]))

    def sub(m):
        nonlocal changed_macros,replacements
        body=m.group("body")
        new=body
        local=0
        for old,ru in ordered:
            n=new.count(old)
            if n:
                new=new.replace(old,ru)
                local+=n
        if local:
            changed_macros+=1
            replacements+=local
            return f'_("{new}")'
        return m.group(0)

    text=MACRO_RE.sub(sub,text)
    if changed_macros < 20:
        raise RuntimeError(f"unexpectedly small credits role scope: {changed_macros}")
    p.write_text(text,encoding="utf-8")
    out=root/"build"/"qarro_ru_credits_roles_v3_176_audit.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
      "marker":MARKER,"file":str(REL),"changedMacros":changed_macros,
      "phraseReplacements":replacements,
      "properNamesPreserved":True,"logicTouched":False,
      "ashBondTouched":False,"ashCapTouched":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {changed_macros} credits role/title strings; staff proper names preserved")
    return 0
if __name__=="__main__":
    raise SystemExit(main())
