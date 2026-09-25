#!/usr/bin/env python3
"""Qarro v3.171: localize all 49 remaining Pokédex rating text blocks.

Covers both Birch/Hoenn compatibility text and FRLG/Oak text because the broad
surface audit counts both. Replacements are label-scoped and fail closed.
Pokemon / Move / Ability proper names remain English by project canon.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEDEX_RATING_ALL_V3_171"
REL = Path("data/text/pokedex_rating.inc")
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
TOKEN_RE = re.compile(r"\\[npl]|\$|\{[^{}]+\}")

PATCHES = {
"gBirchDexRatingText_AreYouCurious": r'''gBirchDexRatingText_AreYouCurious::
	.string "PROF. BIRCH: А, {PLAYER}{KUN}!\p"
	.string "Хочешь узнать, как продвигается\n"
	.string "твой POKeDEX?$"
''',
"gBirchDexRatingText_Cancel": r'''gBirchDexRatingText_Cancel::
	.string "Хм? Ты поймал еще слишком мало\n"
	.string "POKeMON, чтобы оценивать результат.$"
''',
"gBirchDexRatingText_SoYouveSeenAndCaught": r'''gBirchDexRatingText_SoYouveSeenAndCaught::
	.string "Хм-хм…\p"
	.string "Ты видел {STR_VAR_1} POKeMON,\n"
	.string "а поймал {STR_VAR_2} POKeMON…$"
''',
"gBirchDexRatingText_LessThan10": r'''gBirchDexRatingText_LessThan10::
	.string "Чаще заходи в высокую траву и\n"
	.string "внимательнее ищи POKeMON.$"
''',
"gBirchDexRatingText_LessThan20": r'''gBirchDexRatingText_LessThan20::
	.string "Похоже, ты начинаешь разбираться.\n"
	.string "Но дальше станет сложнее.$"
''',
"gBirchDexRatingText_LessThan30": r'''gBirchDexRatingText_LessThan30::
	.string "Некоторые POKeMON встречаются\n"
	.string "только в определенных местах.\l"
	.string "Будь настойчив.$"
''',
"gBirchDexRatingText_LessThan40": r'''gBirchDexRatingText_LessThan40::
	.string "Количество еще можно увеличить,\n"
	.string "но это уже больше похоже\l"
	.string "на настоящий POKeDEX.$"
''',
"gBirchDexRatingText_LessThan50": r'''gBirchDexRatingText_LessThan50::
	.string "Все идет довольно хорошо.\n"
	.string "Продолжай стараться.$"
''',
"gBirchDexRatingText_LessThan60": r'''gBirchDexRatingText_LessThan60::
	.string "Ты пользуешься RODS?\n"
	.string "В море обитает много POKeMON.$"
''',
"gBirchDexRatingText_LessThan70": r'''gBirchDexRatingText_LessThan70::
	.string "Не только лови POKeMON,\n"
	.string "но и развивай их.$"
''',
"gBirchDexRatingText_LessThan80": r'''gBirchDexRatingText_LessThan80::
	.string "Из этого получится отличный\n"
	.string "POKeDEX.\l"
	.string "У меня такое чувство.$"
''',
"gBirchDexRatingText_LessThan90": r'''gBirchDexRatingText_LessThan90::
	.string "Ты собрал уже столько…\n"
	.string "У тебя замечательный талант!$"
''',
"gBirchDexRatingText_LessThan100": r'''gBirchDexRatingText_LessThan100::
	.string "Ты посещал SAFARI ZONE?\p"
	.string "Говорят, некоторых POKeMON\n"
	.string "можно поймать только там.$"
''',
"gBirchDexRatingText_LessThan110": r'''gBirchDexRatingText_LessThan110::
	.string "Наконец-то ты достиг\n"
	.string "отметки в 100 видов.\p"
	.string "Впечатляющий POKeDEX!$"
''',
"gBirchDexRatingText_LessThan120": r'''gBirchDexRatingText_LessThan120::
	.string "Некоторых POKeMON можно найти,\n"
	.string "используя ROCK SMASH.$"
''',
"gBirchDexRatingText_LessThan130": r'''gBirchDexRatingText_LessThan130::
	.string "Получи еще POKeMON,\n"
	.string "обмениваясь с другими.$"
''',
"gBirchDexRatingText_LessThan140": r'''gBirchDexRatingText_LessThan140::
	.string "Я слышал о POKeMON, которые\n"
	.string "эволюционируют, когда очень\l"
	.string "привязываются к TRAINERS.$"
''',
"gBirchDexRatingText_LessThan150": r'''gBirchDexRatingText_LessThan150::
	.string "Не думал, что в регионе HOENN\n"
	.string "существует так много видов\l"
	.string "POKeMON.$"
''',
"gBirchDexRatingText_LessThan160": r'''gBirchDexRatingText_LessThan160::
	.string "Иногда некоторые POKeMON\n"
	.string "появляются целыми стаями.\p"
	.string "Не упускай такие\n"
	.string "возможности.$"
''',
"gBirchDexRatingText_LessThan170": r'''gBirchDexRatingText_LessThan170::
	.string "По твоему POKeDEX уже можно\n"
	.string "многое узнать о POKeMON\l"
	.string "региона HOENN.$"
''',
"gBirchDexRatingText_LessThan180": r'''gBirchDexRatingText_LessThan180::
	.string "Ты уже вполне достоин звания\n"
	.string "POKeMON PROFESSOR, причем\l"
	.string "очень хорошего!$"
''',
"gBirchDexRatingText_LessThan190": r'''gBirchDexRatingText_LessThan190::
	.string "С таким полным POKeDEX\n"
	.string "ты уже настоящий профессионал!$"
''',
"gBirchDexRatingText_LessThan200": r'''gBirchDexRatingText_LessThan200::
	.string "Ты совсем близок к завершению\n"
	.string "этого POKeDEX.\l"
	.string "Я чувствую это всем нутром!$"
''',
"gBirchDexRatingText_DexCompleted": r'''gBirchDexRatingText_DexCompleted::
	.string "Поздравляю!\n"
	.string "Твой POKeDEX полностью заполнен!$"
''',
"gBirchDexRatingText_OnANationwideBasis": r'''gBirchDexRatingText_OnANationwideBasis::
	.string "Хм-хм…\n"
	.string "Если брать всю страну…\p"
	.string "Ты видел {STR_VAR_1} POKeMON,\n"
	.string "а поймал {STR_VAR_2} POKeMON…$"
''',
"PokedexRating_Text_HowIsPokedexComingAlong": r'''PokedexRating_Text_HowIsPokedexComingAlong::
	.string "OAK: Рад тебя видеть!\n"
	.string "Как продвигается твой POKeDEX?\p"
	.string "Дай-ка взглянуть.$"
''',
"PokedexRating_Text_SeenXOwnedY": r'''PokedexRating_Text_SeenXOwnedY::
	.string "Твой прогресс по POKeDEX:\p"
	.string "увидено {STR_VAR_1} POKeMON,\n"
	.string "поймано {STR_VAR_2} POKeMON.\p"
	.string "{FONT_NORMAL}Оценка PROF. OAK:$"
''',
"PokedexRating_Text_LessThan10": r'''PokedexRating_Text_LessThan10::
	.string "Тебе еще многое предстоит.\p"
	.string "Заглядывай в каждый участок травы\n"
	.string "и ищи POKeMON!$"
''',
"PokedexRating_Text_LessThan20": r'''PokedexRating_Text_LessThan20::
	.string "Похоже, ты движешься\n"
	.string "в правильном направлении!\p"
	.string "Я отдал одному из AIDES HM FLASH.\n"
	.string "Обязательно забери его!$"
''',
"PokedexRating_Text_LessThan30": r'''PokedexRating_Text_LessThan30::
	.string "Твоему POKeDEX все еще\n"
	.string "не хватает объема!\p"
	.string "Попробуй поймать другие виды\n"
	.string "POKeMON!$"
''',
"PokedexRating_Text_LessThan40": r'''PokedexRating_Text_LessThan40::
	.string "Хорошо, видно, что ты\n"
	.string "стараешься!\p"
	.string "Я отдал одному из AIDES\n"
	.string "ITEMFINDER. Обязательно забери!$"
''',
"PokedexRating_Text_LessThan50": r'''PokedexRating_Text_LessThan50::
	.string "Твой POKeDEX заполняется\n"
	.string "очень хорошо!\p"
	.string "Я отдал одному из AIDES\n"
	.string "AMULET COIN. Обязательно забери!$"
''',
"PokedexRating_Text_LessThan60": r'''PokedexRating_Text_LessThan60::
	.string "А, наконец-то больше 50\n"
	.string "видов!\p"
	.string "Я отдал одному из AIDES EXP.\n"
	.string "SHARE. Обязательно забери!$"
''',
"PokedexRating_Text_LessThan70": r'''PokedexRating_Text_LessThan70::
	.string "Хо-хо! Получается уже весьма\n"
	.string "солидный POKeDEX!$"
''',
"PokedexRating_Text_LessThan80": r'''PokedexRating_Text_LessThan80::
	.string "Очень хорошо!\p"
	.string "Думаю, рыбалка поможет тебе\n"
	.string "собрать еще больше POKeMON!$"
''',
"PokedexRating_Text_LessThan90": r'''PokedexRating_Text_LessThan90::
	.string "Прекрасно! Дай угадаю… Ты\n"
	.string "любишь что-нибудь собирать, да?$"
''',
"PokedexRating_Text_LessThan100": r'''PokedexRating_Text_LessThan100::
	.string "Я впечатлен!\n"
	.string "Наверняка это было нелегко!$"
''',
"PokedexRating_Text_LessThan110": r'''PokedexRating_Text_LessThan110::
	.string "Наконец-то 100 видов!\n"
	.string "Не могу поверить, как ты хорош!$"
''',
"PokedexRating_Text_LessThan120": r'''PokedexRating_Text_LessThan120::
	.string "У тебя есть даже развитые формы\n"
	.string "POKeMON! Отлично!$"
''',
"PokedexRating_Text_LessThan130": r'''PokedexRating_Text_LessThan130::
	.string "Превосходно! Обменивайся\n"
	.string "с друзьями и получай еще!$"
''',
"PokedexRating_Text_LessThan140": r'''PokedexRating_Text_LessThan140::
	.string "Выдающийся результат!\n"
	.string "Ты стал настоящим профессионалом!$"
''',
"PokedexRating_Text_LessThan150": r'''PokedexRating_Text_LessThan150::
	.string "Мне больше нечего сказать!\n"
	.string "Теперь ты сам POKeMON PROFESSOR!$"
''',
"PokedexRating_Text_Complete": r'''PokedexRating_Text_Complete::
	.string "Твой POKeDEX заполнен полностью!\n"
	.string "Поздравляю!!$"
''',
"PokedexRating_Text_NationalDexSeenXOwnedY": r'''PokedexRating_Text_NationalDexSeenXOwnedY::
	.string "А твой NATIONAL POKeDEX:\p"
	.string "увидено {STR_VAR_1} POKeMON,\n"
	.string "поймано {STR_VAR_2} POKeMON.$"
''',
"PokedexRating_Text_LookForwardToFilledNationalDex": r'''PokedexRating_Text_LookForwardToFilledNationalDex::
	.string "Буду ждать, когда ты полностью\n"
	.string "заполнишь NATIONAL POKeDEX!$"
''',
"PokedexRating_Text_YouveCompletedDex": r'''PokedexRating_Text_YouveCompletedDex::
	.string "Наконец-то…\p"
	.string "Ты полностью завершил\n"
	.string "POKeDEX!\p"
	.string "Великолепно!\n"
	.string "Это поистине выдающееся достижение!$"
''',
"PokedexRating_Text_Wroooaaarrr": r'''PokedexRating_Text_Wroooaaarrr::
	.string "Ура-а-а-а-а-а-а-а-а!$"
''',
"PokedexRating_Text_ThankYouMadeDreamReality": r'''PokedexRating_Text_ThankYouMadeDreamReality::
	.string "Спасибо, {PLAYER}!\n"
	.string "Искренне благодарю тебя!\l"
	.string "Ты воплотил мою мечту в реальность!$"
''',
"PokedexRating_Text_LoveSeeingYourPokedex": r'''PokedexRating_Text_LoveSeeingYourPokedex::
	.string "OAK: А, добро пожаловать!\p"
	.string "Ну что, как продвигается\n"
	.string "твой POKeDEX?\p"
	.string "Ха-ха-ха!\p"
	.string "Вообще-то я и так знаю, но мне\n"
	.string "все равно нравится смотреть!\p"
	.string "Посмотрим…$"
''',
}

def block_for(text: str, label: str) -> tuple[int,int,str]:
    ms=list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(ms)!=1:
        raise RuntimeError(f"{label}: expected one label, got {len(ms)}")
    start=ms[0].start()
    nxt=LABEL_RE.search(text, ms[0].end())
    end=nxt.start() if nxt else len(text)
    return start,end,text[start:end]

def main() -> int:
    if len(sys.argv)!=2:
        raise SystemExit("usage: localize_pokedex_rating_all_v3_171.py <upstream-root>")
    root=Path(sys.argv[1]).resolve()
    path=root/REL
    text=path.read_text(encoding="utf-8")
    if len(PATCHES)!=49:
        raise RuntimeError(f"scope drift: expected 49 patches, got {len(PATCHES)}")
    applied=[]
    for label,repl in PATCHES.items():
        start,end,old=block_for(text,label)
        if re.search(r"[А-Яа-яЁё]", old):
            raise RuntimeError(f"{label}: source block already contains Cyrillic")
        old_tokens=TOKEN_RE.findall(old)
        new_tokens=TOKEN_RE.findall(repl)
        # Preserve semantic control tokens; line-wrap tokens may legitimately differ in count.
        old_sem=[t for t in old_tokens if not re.fullmatch(r"\\[nlp]", t)]
        new_sem=[t for t in new_tokens if not re.fullmatch(r"\\[nlp]", t)]
        if old_sem!=new_sem:
            raise RuntimeError(f"{label}: semantic token mismatch {old_sem!r} != {new_sem!r}")
        text=text[:start]+repl+"\n"+text[end:]
        applied.append(label)
    path.write_text(text,encoding="utf-8")
    out=root/"build"/"qarro_ru_pokedex_rating_all_v3_171_audit.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        "marker":MARKER,
        "file":str(REL),
        "translatedBlockCount":len(applied),
        "translatedBlocks":applied,
        "expectedRemainingCandidatesInFile":0,
        "logicTouched":False,
        "ashBondTouched":False,
        "ashCapTouched":False,
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Pokédex-rating blocks; expected 49->0")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
