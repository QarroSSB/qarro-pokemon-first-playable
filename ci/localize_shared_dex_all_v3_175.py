#!/usr/bin/env python3
"""Qarro v3.175: all 46 remaining shared Pokédex descriptions."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
MARKER="QARRO_RU_SHARED_DEX_ALL_V3_175"
REL=Path("src/data/pokemon/species_info/shared_dex_text.h")

RU={
"gFallbackPokedexText":[
"Это недавно обнаруженный ПОКЕМОН.",
"Он все еще изучается.",
"Подробной информации",
"пока нет."],
"gRaticateAlolaPokedexText":[
"Он собирает группу Rattata",
"и командует ею. У каждой группы",
"своя территория, поэтому споры",
"из-за пищи случаются часто."],
"gPichuPokedexText":[
"Он еще плохо хранит электричество.",
"При испуге случайно разряжается.",
"С возрастом он учится",
"лучше удерживать энергию."],
"gPikachuPokedexText":[
"Он хранит электричество",
"в мешочках на щеках.",
"Выпущенный разом заряд",
"по силе сравним с молнией."],
"gMarowakAlolaPokedexText":[
"Проклятое пламя на кости",
"этого ПОКЕМОНА, говорят,",
"причиняет душевную и физическую",
"боль, которая не проходит."],
"gEeveePokedexText":[
"У Eevee нестабильный генокод,",
"меняющийся под влиянием среды.",
"Излучение разных Stones",
"заставляет его эволюционировать."],
"gUnownPokedexText":[
"Этот ПОКЕМОН похож на знаки",
"древней письменности. Неясно,",
"что появилось раньше:",
"письмена или разные Unown."],
"gMothimPokedexText":[
"Он не строит гнездо и любит",
"цветочный мед, но не собирает его.",
"Вместо этого он крадет",
"мед, собранный Combee."],
"gArceusPokedexText":[
"В мифах говорится, что этот",
"ПОКЕМОН появился из яйца",
"и создал все сущее",
"еще до появления вселенной."],
"gGenesectPokedexText":[
"300 млн лет назад его боялись",
"как сильнейшего охотника.",
"Team Plasma изменила его",
"и установила пушку на спине."],
"gGreninjaPokedexText":[
"Он появляется и исчезает",
"с грацией ниндзя. Быстрыми",
"движениями режет врагов звездами",
"из сжатой воды."],
"gScatterbugPokedexText":[
"При атаке птиц-ПОКЕМОНОВ",
"он распыляет черный яд,",
"вызывающий паралич. Scatterbug",
"живет в любом климате."],
"gSpewpaPokedexText":[
"Он прячется в тени зарослей.",
"При нападении хищников",
"мгновенно взъерошивает шерсть,",
"стараясь их запугать."],
"gFurfrouPokedexText":[
"Стрижка пушистой шерсти",
"делает его изящнее и быстрее.",
"Когда-то эти ПОКЕМОНЫ",
"служили стражами королей."],
"gXerneasPokedexText":[
"Легенды гласят: когда его рога",
"сияют семью цветами,",
"он делится вечной жизнью.",
"Тысячу лет он спал деревом."],
"gZygarde50PokedexText":[
"Говорят, из глубины пещер",
"он наблюдает за экосистемой.",
"Ходят слухи, что в его клетках",
"скрыта еще большая сила."],
"gZygarde10PokedexText":[
"Это Zygarde, собранный примерно",
"на 10%. Он прыгает врагу на грудь",
"и впивается в него",
"острыми клыками."],
"gGumshoosPokedexText":[
"Найдя след добычи, он терпеливо",
"устраивает засаду.",
"Но он активен днем,",
"поэтому к ночи всегда засыпает."],
"gVikavoltPokedexText":[
"Он собирает электричество",
"в огромных челюстях и бьет врагов.",
"Птиц-ПОКЕМОНОВ он подавляет",
"мощными электрическими лучами."],
"gRibombeePokedexText":[
"Ribombee скатывает пыльцу",
"в шарики разных видов.",
"Одни служат пищей, другие — бою.",
"Иногда их продают как добавки."],
"gRockruffPokedexText":[
"Этот ПОКЕМОН издавна живет",
"рядом с людьми. Он чувствует,",
"когда его Trainer грустит,",
"и старается быть рядом."],
"gAraquanidPokedexText":[
"Несмотря на внешний вид,",
"он заботится о других.",
"Слабых ПОКЕМОНОВ он защищает",
"внутри своего водяного пузыря."],
"gLurantisPokedexText":[
"Яркую окраску Lurantis",
"очень трудно поддерживать.",
"Некоторым коллекционерам",
"нравится такая забота о нем."],
"gSalazzlePokedexText":[
"Почему-то встречаются лишь самки.",
"Она окружает себя самцами Salandit.",
"Ее ядовитый газ",
"насыщен феромонами."],
"gSilvallyNormalPokedexText":[
"Доверие к партнеру пробуждает его.",
"С помощью особых дисков памяти",
"этот ПОКЕМОН меняет свой тип,",
"что особенно полезно в бою."],
"gSilvallyMemoryPokedexText":[
"После пробуждения включается",
"его RKS System. Особые диски памяти",
"позволяют менять тип",
"и сбивать врагов с толку."],
"gMiniorMeteorPokedexText":[
"Он живет в озоновом слое,",
"но падает, когда оболочка",
"становится слишком тяжелой.",
"Рожден из измененных наночастиц."],
"gMiniorCorePokedexText":[
"Если ядро долго открыто,",
"он вскоре погибнет.",
"Он может выжить, если быстро",
"поместить его в Poke Ball."],
"gTogedemaruPokedexText":[
"Обычно колючая шерсть на спине",
"лежит спокойно. При возбуждении",
"она встает дыбом",
"и впивается в нападающих."],
"gMimikyuDisguisedPokedexText":[
"Одинокий ПОКЕМОН скрывает",
"страшный облик под старой тряпкой,",
"чтобы сближаться с другими.",
"Его настоящий вид неизвестен."],
"gMimikyuBustedPokedexText":[
"После всех усилий маскировки",
"его шея сломалась.",
"То, что внутри, вероятно, цело,",
"но он все равно очень расстроен."],
"gKommoOPokedexText":[
"Твердая чешуя служит",
"и оружием, и защитой.",
"В прошлом из нее делали оружие",
"и другие ценные вещи."],
"gAlcremieVanillaCreamPokedexText":[
"Когда Alcremie довольна,",
"крем из ее рук становится слаще.",
"Доверяя Trainer, она угощает его",
"ягодами, украшенными кремом."],
"gAlcremieRubyCreamPokedexText":[
"После эволюции он получил",
"кисло-сладкий вкус.",
"Причина — внезапное изменение",
"клеток во время эволюции."],
"gAlcremieMatchaCreamPokedexText":[
"После эволюции он получил",
"ароматный вкус.",
"Причина — внезапное изменение",
"клеток во время эволюции."],
"gAlcremieMintCreamPokedexText":[
"После эволюции он получил",
"освежающий вкус.",
"Причина — внезапное изменение",
"клеток во время эволюции."],
"gAlcremieLemonCreamPokedexText":[
"После эволюции он получил",
"кислый вкус.",
"Причина — внезапное изменение",
"клеток во время эволюции."],
"gAlcremieSaltedCreamPokedexText":[
"После эволюции он получил",
"соленый вкус.",
"Причина — внезапное изменение",
"клеток во время эволюции."],
"gAlcremieRubySwirlPokedexText":[
"После эволюции он получил",
"смешанный вкус.",
"Причина — внезапное изменение",
"клеток во время эволюции."],
"gAlcremieCaramelSwirlPokedexText":[
"После эволюции он получил",
"горький вкус.",
"Причина — внезапное изменение",
"клеток во время эволюции."],
"gAlcremieRainbowSwirlPokedexText":[
"После эволюции он получил",
"сложный вкус.",
"Причина — внезапное изменение",
"клеток во время эволюции."],
"gToxtricityGigantamaxPokedexText":[
"Собственный яд проник в мозг,",
"и он потерял контроль.",
"В ярости он несется по земле,",
"заражая ее ядовитым потом."],
"gOgerponTealMaskPokedexText":[
"Тип этого ПОКЕМОНА зависит",
"от надетой маски.",
"Ловкими движениями и ударами ног",
"он сбивает врагов с толку."],
"gOgerponWellspringMaskPokedexText":[
"Эта форма сильна",
"и в атаке, и в защите.",
"Она непрерывно применяет приемы,",
"словно источник извергает воду."],
"gOgerponHearthflameMaskPokedexText":[
"Это самая агрессивная форма.",
"Она обрушивает на врагов",
"яростную силу пламени,",
"пылающего в очаге."],
"gOgerponCornerstoneMaskPokedexText":[
"В этой форме он использует",
"силу камня. Тело твердо как скала",
"и надежно защищает его",
"от самых разных атак."],
}

PAT=re.compile(r'const u8 (?P<name>\w+PokedexText)\[\]\s*=\s*_\(\n(?P<body>[\s\S]*?)\);')

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: localize_shared_dex_all_v3_175.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); p=root/REL
    text=p.read_text(encoding="utf-8")
    if len(RU)!=46: raise RuntimeError(f"expected 46 entries, got {len(RU)}")
    seen=set()
    def sub(m):
        name=m.group("name")
        if name not in RU: return m.group(0)
        if name in seen: raise RuntimeError(f"duplicate {name}")
        lines=RU[name]
        if len(lines)!=4: raise RuntimeError(f"{name}: expected 4 lines")
        seen.add(name)
        body="\n".join(f'    "{s}\\n"' for s in lines[:-1])
        body+="\n"+f'    "{lines[-1]}"'
        return f"const u8 {name}[] = _(\n{body});"
    text=PAT.sub(sub,text)
    missing=set(RU)-seen
    if missing: raise RuntimeError(f"missing shared dex labels: {sorted(missing)}")
    p.write_text(text,encoding="utf-8")
    out=root/"build"/"qarro_ru_shared_dex_all_v3_175_audit.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"translatedCount":46,
      "expectedRemainingCandidatesInFile":0,"logicTouched":False,
      "ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: translated all 46 shared Pokédex descriptions")
    return 0
if __name__=="__main__": raise SystemExit(main())
