#!/usr/bin/env python3
"""Qarro v3.99: Russian runtime localization for Water Path, Bond Bridge and Fighting Dojo.

74 runtime text blocks total:
- SixIsland_WaterPath_Frlg: 25
- ThreeIsland_BondBridge_Frlg: 25
- SaffronCity_Dojo_Frlg: 24 (includes the legacy Japanese gift text)
Pokemon species / Move / Ability proper names remain English by project canon.
Ash Bond / Ash Cap are untouched.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_SEVII_DOJO_V3_99"
FILES = {
Path("data/maps/SixIsland_WaterPath_Frlg/scripts.inc"): {
"SixIsland_WaterPath_Text_RoseIntro": ["Приятный ветерок привёл меня\\n", "прямо сюда.$"],
"SixIsland_WaterPath_Text_RoseDefeat": ["Хи-хи... Ты такой милый, когда\\n", "полон решимости.$"],
"SixIsland_WaterPath_Text_RosePostBattle": ["Я хочу сходить в тот лес, но...\\p", "Там полно ПОКЕМОНОВ типа BUG.\\n", "Они меня немного пугают.$"],
"SixIsland_WaterPath_Text_EdwardIntro": ["Я тайно тренируюсь, чтобы никто\\n", "меня не видел.$"],
"SixIsland_WaterPath_Text_EdwardDefeat": ["Никто ведь не видел, как я\\n", "проиграл?$"],
"SixIsland_WaterPath_Text_EdwardPostBattle": ["Как артист, я не хочу, чтобы люди\\n", "видели, сколько сил я трачу.$"],
"SixIsland_WaterPath_Text_SamirIntro": ["Что, тебе уже надоело видеть\\n", "ПЛОВЦОВ вроде меня?\\p", "Эй, не надо так!$"],
"SixIsland_WaterPath_Text_SamirDefeat": ["О нет, нет, нет.$"],
"SixIsland_WaterPath_Text_SamirPostBattle": ["Так и не смог избавиться от\\n", "клейма ПЛОВЦА...$"],
"SixIsland_WaterPath_Text_DeniseIntro": ["Мой парень всегда занят, поэтому\\n", "я плаваю одна.$"],
"SixIsland_WaterPath_Text_DeniseDefeat": ["Эх, я знала, что так будет!$"],
"SixIsland_WaterPath_Text_DenisePostBattle": ["Когда моего парня нет рядом,\\n", "я провожу время с ПОКЕМОНОМ,\\l", "которого он мне подарил.$"],
"SixIsland_WaterPath_Text_EarlIntro": ["Скажи, а где здесь поблизости\\n", "горы?$"],
"SixIsland_WaterPath_Text_EarlDefeat": ["Я так увлёкся боем, что совсем\\n", "сбился с пути!$"],
"SixIsland_WaterPath_Text_EarlPostBattle": ["Неужели здесь поблизости совсем\\n", "нет гор?$"],
"SixIsland_WaterPath_Text_MiuIntro": ["МИУ: Привет, ПОКЕМОНЫ!\\n", "Пора играть!$"],
"SixIsland_WaterPath_Text_MiuDefeat": ["МИУ: О нет!\\n", "Мамочка!$"],
"SixIsland_WaterPath_Text_MiuPostBattle": ["МИУ: Когда мы проигрываем, мне\\n", "становится так грустно...$"],
"SixIsland_WaterPath_Text_MiuNotEnoughMons": ["МИУ: Мы с МИА - БЛИЗНЯШКИ.\\n", "Мы хотим сражаться вместе.$"],
"SixIsland_WaterPath_Text_MiaIntro": ["МИА: Привет, ПОКЕМОНЫ!\\n", "Пора сражаться!$"],
"SixIsland_WaterPath_Text_MiaDefeat": ["МИА: Ты вредина!\\n", "Плохо, что ты победил!$"],
"SixIsland_WaterPath_Text_MiaPostBattle": ["МИА: Ох...\\n", "Прости, мой ПОКЕМОН...$"],
"SixIsland_WaterPath_Text_MiaNotEnoughMons": ["МИА: Ой, у тебя только один\\n", "ПОКЕМОН?\\p", "Тебе не одиноко?$"],
"SixIsland_WaterPath_Text_WantedUltimateHorn": ["Разыскивается!\\n", "Идеальный рог!$"],
"SixIsland_WaterPath_Text_RouteSign": ["ВОДНЫЙ ПУТЬ\\n", "Ведёт в ДОЛИНУ РУИН$"],
},
Path("data/maps/ThreeIsland_BondBridge_Frlg/scripts.inc"): {
"ThreeIsland_BondBridge_Text_NikkiIntro": ["Солёный запах моря...\\n", "Он волнует моё сердце.$"],
"ThreeIsland_BondBridge_Text_NikkiDefeat": ["...Фу-фу...\\n", "Что-то неприятно пахнет...$"],
"ThreeIsland_BondBridge_Text_NikkiPostBattle": ["Может, это запах пота от твоих\\n", "ПОКЕМОНОВ...$"],
"ThreeIsland_BondBridge_Text_VioletIntro": ["Куда ты так торопишься?$"],
"ThreeIsland_BondBridge_Text_VioletDefeat": ["Ты растишь замечательных\\n", "ПОКЕМОНОВ.$"],
"ThreeIsland_BondBridge_Text_VioletPostBattle": ["Если пойдёшь дальше, в конце концов\\n", "доберёшься до ЯГОДНОГО ЛЕСА.$"],
"ThreeIsland_BondBridge_Text_AmiraIntro": ["Мама сказала, что мне нельзя плавать\\n", "без надувного круга.$"],
"ThreeIsland_BondBridge_Text_AmiraDefeat": ["Уа-а-а!\\n", "Уа-а-а!$"],
"ThreeIsland_BondBridge_Text_AmiraPostBattle": ["В этом году я наконец-то\\n", "научусь плавать!$"],
"ThreeIsland_BondBridge_Text_AlexisIntro": ["Ура, ура!\\n", "ПОКЕМОНЫ!$"],
"ThreeIsland_BondBridge_Text_AlexisDefeat": ["И что теперь будет?$"],
"ThreeIsland_BondBridge_Text_AlexisPostBattle": ["Я только что победила?\\n", "Или проиграла?$"],
"ThreeIsland_BondBridge_Text_TishaIntro": ["О нет, не подходи!\\n", "Пожалуйста, держись подальше!$"],
"ThreeIsland_BondBridge_Text_TishaDefeat": ["Ладно, ты победил!\\n", "Теперь можешь уйти?$"],
"ThreeIsland_BondBridge_Text_TishaPostBattle": ["ПОКЕМОН прокусил мой купальник.\\p", "Я не могу выйти из воды!$"],
"ThreeIsland_BondBridge_Text_JoyIntro": ["ДЖОЙ: Мы покажем тебе наших\\n", "любимых ПОКЕМОНОВ!$"],
"ThreeIsland_BondBridge_Text_JoyDefeat": ["ДЖОЙ: Ох...\\n", "МЕГ!$"],
"ThreeIsland_BondBridge_Text_JoyPostBattle": ["ДЖОЙ: Правда было весело?\\n", "Надеюсь, ещё сразимся!$"],
"ThreeIsland_BondBridge_Text_JoyNotEnoughMons": ["ДЖОЙ: Я очень хочу сражаться\\n", "вместе с МЕГ.\\p", "Одного ПОКЕМОНА недостаточно.$"],
"ThreeIsland_BondBridge_Text_MegIntro": ["МЕГ: Мы покажем тебе наших\\n", "любимых ПОКЕМОНОВ.$"],
"ThreeIsland_BondBridge_Text_MegDefeat": ["МЕГ: Ох...\\n", "ДЖОЙ!$"],
"ThreeIsland_BondBridge_Text_MegPostBattle": ["МЕГ: ДЖОЙ, правда было весело?$"],
"ThreeIsland_BondBridge_Text_MegNotEnoughMons": ["МЕГ: Я хочу сражаться вместе\\n", "с ДЖОЙ.\\p", "Одного ПОКЕМОНА недостаточно.$"],
"ThreeIsland_BondBridge_Text_BerryForestAhead": ["ВПЕРЕДИ ЯГОДНЫЙ ЛЕС$"],
"ThreeIsland_BondBridge_Text_BondBridgeSign": ["МОСТ СВЯЗИ\\n", "Переходите тихо.\\p", "ВПЕРЕДИ ЯГОДНЫЙ ЛЕС$"],
},
Path("data/maps/SaffronCity_Dojo_Frlg/scripts.inc"): {
"SaffronCity_Dojo_Text_MasterKoichiIntro": ["Хр-р!\\p", "Я МАСТЕР КАРАТЕ!\\n", "Я здесь ГЛАВНЫЙ!\\p", "Хочешь бросить нам вызов?\\n", "Пощады не жди!\\p", "Хва-а-а!$"],
"SaffronCity_Dojo_Text_MasterKoichiDefeat": ["Хва!\\n", "Аргх! Побеждён!$"],
"SaffronCity_Dojo_Text_ChoosePrizedFightingMon": ["Да, я проиграл!\\p", "Но прошу, не забирай нашу эмблему\\n", "как трофей!\\p", "Взамен я отдам тебе ценного\\n", "ПОКЕМОНА типа FIGHTING!\\p", "Выбирай любого!$"],
"SaffronCity_Dojo_Text_StayAndTrainWithUs": ["Хр-р!\\n", "Оставайся и тренируй карате с нами!$"],
"SaffronCity_Dojo_Text_MikeIntro": ["Хо-о!\\n", "Сними обувь!$"],
"SaffronCity_Dojo_Text_MikeDefeat": ["Сдаюсь!$"],
"SaffronCity_Dojo_Text_MikePostBattle": ["Вот увидишь нашего МАСТЕРА!\\n", "По сравнению с ним я мелочь!$"],
"SaffronCity_Dojo_Text_HidekiIntro": ["Говорят, ты хорош!\\n", "Покажи мне!$"],
"SaffronCity_Dojo_Text_HidekiDefeat": ["Судья!\\n", "Одно очко!$"],
"SaffronCity_Dojo_Text_HidekiPostBattle": ["Наш МАСТЕР - профессиональный боец.\\n", "Готовься проиграть!$"],
"SaffronCity_Dojo_Text_AaronIntro": ["Хия!\\n", "Я ничего не боюсь!\\p", "Каждый день на тренировках\\n", "я разбиваю валуны!$"],
"SaffronCity_Dojo_Text_AaronDefeat": ["Ай!\\n", "Пальцы отбил!$"],
"SaffronCity_Dojo_Text_AaronPostBattle": ["Единственное, чего мы боимся, -\\n", "психическая сила!$"],
"SaffronCity_Dojo_Text_HitoshiIntro": ["Хва-а!\\p", "Ты вторгся в наше\\n", "БОЕВОЕ ДОДЗЁ!$"],
"SaffronCity_Dojo_Text_HitoshiDefeat": ["Уф!\\n", "Сдаюсь!$"],
"SaffronCity_Dojo_Text_HitoshiPostBattle": ["Лучшие бойцы со всей страны\\n", "тренируются здесь.$"],
"SaffronCity_Dojo_Text_YouWantHitmonlee": ["Хочешь мастера ударов ногами\\n", "HITMONLEE?$"],
"SaffronCity_Dojo_Text_ReceivedMonFromKarateMaster": ["{PLAYER} получил {STR_VAR_1}\\n", "от МАСТЕРА КАРАТЕ.$"],
"SaffronCity_Dojo_Text_YouWantHitmonchan": ["Хочешь мастера ударов руками\\n", "HITMONCHAN?$"],
"SaffronCity_Dojo_Text_ReceivedMonFromKarateMaster2": ["{PLAYER} получил {STR_VAR_1}\\n", "от МАСТЕРА КАРАТЕ!$"],
"SaffronCity_Dojo_Text_BetterNotGetGreedy": ["Лучше не жадничать...$"],
"SaffronCity_Dojo_Text_EnemiesOnEverySide": ["Враги со всех сторон!$"],
"SaffronCity_Dojo_Text_GoesAroundComesAround": ["Что посеешь, то и пожнёшь.$"],
"SaffronCity_Dojo_Text_FightingDojo": ["БОЕВОЕ ДОДЗЁ$"],
},
}


def render(label, lines):
    out=[f"{label}::"]
    for line in lines:
        out.append(f'\t.string "{line.replace(chr(34), chr(92)+chr(34))}"')
    return "\n".join(out)+"\n"


def replace_block(text,label,lines):
    pat=re.compile(rf"^{re.escape(label)}::\n(?:\t\.string [^\n]*(?:\n|$))+",re.M)
    ms=list(pat.finditer(text))
    if len(ms)!=1: raise SystemExit(f"[{MARKER}] {label}: expected 1 block, found {len(ms)}")
    old=ms[0].group(0)
    if re.search(r"[А-Яа-яЁё]",old): raise SystemExit(f"[{MARKER}] {label}: already Cyrillic")
    return text[:ms[0].start()]+render(label,lines)+text[ms[0].end():]


def main():
    if len(sys.argv)!=2: raise SystemExit(f"usage: {Path(sys.argv[0]).name} <upstream-root>")
    root=Path(sys.argv[1]).resolve(); by={}; total=0
    for rel,patches in FILES.items():
        p=root/rel; text=p.read_text(encoding='utf-8')
        for label,lines in patches.items(): text=replace_block(text,label,lines)
        p.write_text(text,encoding='utf-8'); by[str(rel)]=len(patches); total+=len(patches)
    if total!=74: raise SystemExit(f"[{MARKER}] expected 74 blocks, got {total}")
    out=root/'build/qarro_ru_sevii_dojo_v3_99_audit.json'; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'marker':MARKER,'translatedBlockCount':total,'byFile':by,'includesLegacyJapaneseDojoGiftText':True,'policy':'Pokemon+Move+Ability proper names remain English','ashBondTouched':False,'ashCapTouched':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"[{MARKER}] PASS: translated {total} runtime blocks; Ash Bond/Ash Cap untouched")
    return 0
if __name__=='__main__': raise SystemExit(main())
