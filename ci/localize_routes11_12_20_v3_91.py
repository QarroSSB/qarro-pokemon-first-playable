#!/usr/bin/env python3
"""Qarro v3.91 bulk Russian localization: Route 11 + Route 12 + Route 20.

Translates 99 real FireRed runtime text blocks from pinned Expansion 1.17.0:
31 on Route 11, 36 on Route 12 (including four shared Snorlax/Poke Flute Text_ labels
outside the audit's _Text_ naming filter), and 32 on Route 20.
Pokemon species, Move and Ability proper names remain English by project canon.
Ash Bond / Ash Cap and gameplay logic are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTES11_12_20_V3_91"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    Path("data/maps/Route11_Frlg/scripts.inc"): {
        "Route11_Text_HugoIntro": "Победа, поражение или ничья!$",
        "Route11_Text_HugoDefeat": "Эх!\\nНе повезло!$",
        "Route11_Text_HugoPostBattle": "ПОКЕМОНЫ - это жизнь!\\nА жить - значит играть!$",
        "Route11_Text_JasperIntro": "Соревнование!\\nМне всегда мало!$",
        "Route11_Text_JasperDefeat": "А ведь у меня был шанс!$",
        "Route11_Text_JasperPostBattle": "В мире ПОКЕМОНОВ нельзя быть трусом!$",
        "Route11_Text_EddieIntro": "Давай сразимся, только без жульничества!$",
        "Route11_Text_EddieDefeat": "Что?\\nТак не должно быть!$",
        "Route11_Text_EddiePostBattle": "Я сделал всё, что мог.\\nНи о чём не жалею.$",
        "Route11_Text_BraxtonIntro": "Осторожно!\\nЯ прокладываю кабели!$",
        "Route11_Text_BraxtonDefeat": "Вот это был разряд!$",
        "Route11_Text_BraxtonPostBattle": "Расскажи всем, что энергию надо беречь!$",
        "Route11_Text_DillonIntro": "Я только недавно стал ТРЕНЕРОМ.\\nНо думаю, что смогу победить.$",
        "Route11_Text_DillonDefeat": "Мои ПОКЕМОНЫ не смогли победить...\\nРазве они ещё недостаточно выросли?$",
        "Route11_Text_DillonPostBattle": "Ну и что теперь?\\nОставь меня в покое!$",
        "Route11_Text_DirkIntro": "Ха-ха-ха!\\nЯ ещё ни разу не проигрывал!$",
        "Route11_Text_DirkDefeat": "Моё первое поражение!$",
        "Route11_Text_DirkPostBattle": "Тебе просто повезло, вот и всё.$",
        "Route11_Text_DarianIntro": "Я ещё ни разу не побеждал...$",
        "Route11_Text_DarianDefeat": "Я так и знал...$",
        "Route11_Text_DarianPostBattle": "Мне опять не повезло. Как всегда.$",
        "Route11_Text_YasuIntro": "Я лучший в своём классе.\\nКаждое утро тренируюсь.$",
        "Route11_Text_YasuDefeat": "Чёрт!\\nМоим ПОКЕМОНАМ нужно стать сильнее!$",
        "Route11_Text_YasuPostBattle": "С гор иногда спускается толстый ПОКЕМОН.\\pЕсли его поймать, наверняка он окажется\\nочень сильным.$",
        "Route11_Text_BernieIntro": "Осторожно, провода под напряжением!$",
        "Route11_Text_BernieDefeat": "Ого!\\nВот это искра!$",
        "Route11_Text_BerniePostBattle": "Ладно, пора возвращаться к работе.$",
        "Route11_Text_DaveIntro": "Я тщательно растил своих ПОКЕМОНОВ.\\nТеперь они точно готовы!$",
        "Route11_Text_DaveDefeat": "Пока-пока!\\nСпасибо и до свидания!$",
        "Route11_Text_DavePostBattle": "Тц...\\nЛучше пойду искать тех, кто посильнее!$",
        "Route11_Text_DiglettsCave": "ПЕЩЕРА DIGLETT$",
    },
    Path("data/maps/Route12_Frlg/scripts.inc"): {
        "Route12_Text_MonSprawledOutInSlumber": "ПОКЕМОН растянулся на дороге\\nи крепко, безмятежно спит.$",
        "Text_SnorlaxWokeUp": "SNORLAX проснулся!\\pОн в ярости бросился в атаку!$",
        "Text_SnorlaxReturnedToMountains": "SNORLAX успокоился.\\nОн широко зевнул...\\lИ вернулся в горы.$",
        "Text_WantToUsePokeFlute": "Использовать ПОКЕ-ФЛЕЙТУ?$",
        "Text_PlayedPokeFlute": "{PLAYER} сыграл на ПОКЕ-ФЛЕЙТЕ.$",
        "Route12_Text_NedIntro": "Есть!\\nЗдесь клюёт!$",
        "Route12_Text_NedDefeat": "Тц!\\nВсего лишь мелкая рыбёшка...$",
        "Route12_Text_NedPostBattle": "Погоди!\\nЛеска зацепилась!$",
        "Route12_Text_ChipIntro": "Терпение.\\nНа рыбалке главное - уметь ждать.$",
        "Route12_Text_ChipDefeat": "Эта рыбка сорвалась!$",
        "Route12_Text_ChipPostBattle": "С хорошей УДОЧКОЙ я мог бы ловить\\nПОКЕМОНОВ получше...$",
        "Route12_Text_JustinIntro": "Я ищу ЛУННЫЙ КАМЕНЬ.\\nТебе такой не попадался?$",
        "Route12_Text_JustinDefeat": "Ай!$",
        "Route12_Text_JustinPostBattle": "С ЛУННЫМ КАМНЕМ мой ПОКЕМОН\\nмог бы эволюционировать.\\pТогда бы я точно победил.$",
        "Route12_Text_LucaIntro": "Электричество - моя специальность.\\pА вот о морских ПОКЕМОНАХ\\nя ничего не знаю.$",
        "Route12_Text_LucaDefeat": "Отключили!$",
        "Route12_Text_LucaPostBattle": "Вода проводит электричество, поэтому\\nморских ПОКЕМОНОВ стоит бить током.$",
        "Route12_Text_HankIntro": "РЫБОЛОВНЫЙ ФАНАТ против\\nЮНОГО ТРЕНЕРА!$",
        "Route12_Text_HankDefeat": "Перебор!$",
        "Route12_Text_HankPostBattle": "Наверное, каждый становится хорош\\nв том, что любит.\\pТы победил меня в ПОКЕМОНАХ,\\nно в рыбалке тебе меня не обойти.$",
        "Route12_Text_ElliotIntro": "Я люблю рыбалку, не подумай плохого.\\pНо было бы неплохо иметь\\nпобольше работы.$",
        "Route12_Text_ElliotDefeat": "Нелегко...$",
        "Route12_Text_ElliotPostBattle": "Всё нормально.\\nПоражения меня уже не раздражают.$",
        "Route12_Text_AndrewIntro": "Что ловится?\\pНикогда не знаешь, что именно\\nможет попасться!$",
        "Route12_Text_AndrewDefeat": "Упустил!$",
        "Route12_Text_AndrewPostBattle": "Что, MAGIKARP?\\pДа, я ловлю их постоянно.\\nНо они ужасно слабые.$",
        "Route12_Text_RouteSign": "МАРШРУТ 12\\nНа север - ЛАВАНДЕР$",
        "Route12_Text_SportfishingArea": "ЗОНА СПОРТИВНОЙ РЫБАЛКИ$",
        "Route12_Text_JesIntro": "JES: Если я выиграю,\\nто сделаю GIA предложение.$",
        "Route12_Text_JesDefeat": "JES: Ну почему ты не мог\\nдать нам победить?$",
        "Route12_Text_JesPostBattle": "JES: О, GIA, прости меня,\\nлюбовь моя!$",
        "Route12_Text_JesNotEnoughMons": "JES: Мы с GIA будем\\nвместе навсегда.\\pМы не станем сражаться, пока у тебя\\nне будет двух ПОКЕМОНОВ.$",
        "Route12_Text_GiaIntro": "GIA: Эй, JES...\\pЕсли мы победим, я выйду за тебя!$",
        "Route12_Text_GiaDefeat": "GIA: Ну почему?$",
        "Route12_Text_GiaPostBattle": "GIA: JES, глупенький!\\nТы всё испортил!$",
        "Route12_Text_GiaNotEnoughMons": "GIA: Я не могу сражаться\\nбез моего JES!\\pУ тебя правда нет ещё одного ПОКЕМОНА?$",
    },
    Path("data/maps/Route20_Frlg/scripts.inc"): {
        "Route20_Text_BarryIntro": "Здесь мелко.\\nПоэтому плавает столько людей.$",
        "Route20_Text_BarryDefeat": "Плюх!$",
        "Route20_Text_BarryPostBattle": "Хотел бы я кататься на своём ПОКЕМОНЕ.\\nДержу пари, ты совсем не устал.$",
        "Route20_Text_ShirleyIntro": "ОСТРОВА СИФОМ - тихое место для отдыха.\\nЯ провожу здесь отпуск.$",
        "Route20_Text_ShirleyDefeat": "Хватит!$",
        "Route20_Text_ShirleyPostBattle": "Под этим островом находится\\nогромная пещера.$",
        "Route20_Text_TiffanyIntro": "Обожаю качаться на волнах\\nрядом с рыбами.$",
        "Route20_Text_TiffanyDefeat": "Ай!$",
        "Route20_Text_TiffanyPostBattle": "Хочешь поплавать со мной?$",
        "Route20_Text_IreneIntro": "Ты тоже в отпуске?$",
        "Route20_Text_IreneDefeat": "Никакой пощады!$",
        "Route20_Text_IrenePostBattle": "Говорят, очень давно СИФОМ\\nбыл одним большим островом.$",
        "Route20_Text_DeanIntro": "Зацени мои мышцы!$",
        "Route20_Text_DeanDefeat": "Слабак!$",
        "Route20_Text_DeanPostBattle": "Надо было качать моих ПОКЕМОНОВ,\\nа не себя!$",
        "Route20_Text_DarrinIntro": "Почему ты едешь на ПОКЕМОНЕ?\\nПлавать не умеешь?$",
        "Route20_Text_DarrinDefeat": "Ай!\\nКак торпедой!$",
        "Route20_Text_DarrinPostBattle": "Кататься на ПОКЕМОНЕ выглядит весело!$",
        "Route20_Text_RogerIntro": "Я прилетел сюда на птичьем ПОКЕМОНЕ.$",
        "Route20_Text_RogerDefeat": "О нет!\\nИ что мне теперь делать?$",
        "Route20_Text_RogerPostBattle": "Мои птицы совсем выдохлись.\\nОни не смогут отвезти меня назад с FLY!$",
        "Route20_Text_NoraIntro": "Парень подарил мне большие жемчужины.$",
        "Route20_Text_NoraDefeat": "О нет!\\nТам же были мои жемчужины!$",
        "Route20_Text_NoraPostBattle": "Интересно, мои жемчужины станут больше\\nвнутри CLOYSTER?$",
        "Route20_Text_MissyIntro": "Я приплыла сюда с ОСТРОВА СИННАБАР.\\nПоверь, это было нелегко.$",
        "Route20_Text_MissyDefeat": "Какое разочарование!$",
        "Route20_Text_MissyPostBattle": "ПОКЕМОНЫ захватили заброшенный\\nособняк на СИННАБАРЕ.\\pТеперь его называют\\nОСОБНЯКОМ ПОКЕМОНОВ.$",
        "Route20_Text_MelissaIntro": "На западе, на СИННАБАРЕ, есть\\nЛАБОРАТОРИЯ ПОКЕМОНОВ.\\pТам работает мой папа.$",
        "Route20_Text_MelissaDefeat": "Стой!\\nТы должен был подождать!$",
        "Route20_Text_MelissaPostBattle": "СИННАБАР - вулканический остров.\\pГоворят, он поднялся из моря\\nпосле извержения вулкана.$",
        "Route20_Text_SeafoamIslands": "ОСТРОВА СИФОМ$",
        "Route20_Text_MistyTrainsHere": "Здесь часто встречаются сильные ТРЕНЕРЫ\\nи ВОДНЫЕ ПОКЕМОНЫ.\\pГоворят, здесь тренируется MISTY\\nиз ЦЕРУЛИНСКОГО ГИМА.$",
    },
}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def replace_block(text: str, label: str, translated: str) -> str:
    match = re.search(rf"(?m)^{re.escape(label)}::\s*$", text)
    if not match:
        die(f"missing label {label}")
    next_label = LABEL_RE.search(text, match.end())
    end = next_label.start() if next_label else len(text)
    block = f"{label}::\n\t.string " + json.dumps(translated, ensure_ascii=False) + "\n\n"
    return text[:match.start()] + block + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    changed = []
    total = 0
    for rel, translations in FILES.items():
        path = root / rel
        if not path.is_file():
            die(f"missing FireRed map script {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in translations.items():
            text = replace_block(text, label, translated)
            total += 1
        path.write_text(text, encoding="utf-8")
        changed.append(str(rel))

    audit = {
        "marker": MARKER,
        "translatedRuntimeBlocks": total,
        "auditScopedEnglishBlocksTargeted": 95,
        "extraRuntimeBlocksOutsideAuditNamingFilter": 4,
        "changedFiles": changed,
        "pokemonMoveAbilityProperNamesStayEnglish": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_routes11_12_20_v3_91_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if total != 99:
        die(f"expected 99 translated runtime blocks, got {total}")
    print(f"[{MARKER}] PASS: translated {total} runtime blocks across Route 11 + Route 12 + Route 20")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
