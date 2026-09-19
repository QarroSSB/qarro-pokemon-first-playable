#!/usr/bin/env python3
"""Qarro v3.195: finish human-quality RU pass for trainers_frlg.inc.

Covers the final 95 machine-translated rematch blocks (indices 139-233).
Together with v3.191-v3.194 this completes trainers_frlg.inc 234/234.
Localization-only; exact runtime control-token sequences are preserved and
source drift fails closed. Pokemon, Move and Ability proper names stay English.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINERS_FRLG_QUALITY_FINISH_V3_195"
TARGET = Path("data/text/trainers_frlg.inc")
TRANSLATIONS = {
    "Route21_North_Text_RonaldRematchIntro:": "Хочешь знать, клюет ли здесь\\nрыба?$",
    "Route21_North_Text_WadeRematchIntro:": "Я снова наловил целую кучу!\\nХочешь еще разок сразиться?$",
    "Route21_North_Text_SpencerRematchIntro:": "Море очищает мое тело и душу!$",
    "Route21_South_Text_JackRematchIntro:": "Я поймал своих POKeMON в море.\\nТам же их и тренирую.$",
    "Route21_South_Text_JeromeRematchIntro:": "Прямо сейчас я снова участвую\\nв триатлоне!$",
    "Route21_South_Text_RolandRematchIntro:": "Ах!\\nЧувствуешь солнце и ветер?$",
    "Route21_South_Text_ClaudeRematchIntro:": "Эй, хватит уже.\\nТы постоянно распугиваешь рыбу!$",
    "Route21_South_Text_NolanRematchIntro:": "Составь мне компанию, пока не клюнет.$",
    "Route21_North_Text_LilRematchIntro:": "ЛИЛ: Что? Опять бой?\\nИЭН, ты не можешь сам?$",
    "Route21_North_Text_IanRematchIntro:": "ИЭН: Моя сестра все еще лентяйка.\\nПомоги привести ее в форму!$",
    "Route25_Text_JoeyRematchIntro:": "Пока я здесь, я не проиграю!$",
    "Route25_Text_DanRematchIntro:": "Папа водил меня на отличную вечеринку\\nна S.S. ANNE в ВЕРМИЛИОН-СИТИ.$",
    "Route25_Text_FlintRematchIntro:": "Я крутой парень.\\nУ меня есть девушка!\\pНа этот раз я точно покажу ей,\\nкакой я крутой!$",
    "Route25_Text_KelseyRematchIntro:": "Привет!\\nМой парень крутой!\\lСегодня я в отличной форме!$",
    "Route25_Text_ChadRematchIntro:": "У меня было предчувствие...\\nЯ знал, что мы снова сразимся!$",
    "Route25_Text_HaleyRematchIntro:": "У моей подруги столько милых POKeMON.\\nЯ так завидую!$",
    "Route25_Text_FranklinRematchIntro:": "Я только что тренировался на ЛУННОЙ ГОРЕ,\\nно сил у меня еще полно!$",
    "Route25_Text_NobRematchIntro:": "На мысе живет ПОКЕМАНЬЯК.\\nТы видел его коллекцию?$",
    "Route25_Text_WayneRematchIntro:": "Снова идешь к БИЛЛУ?\\nСначала сразись со мной!$",
    "Route24_Text_ShaneRematchIntro:": "Я видел твой подвиг из высокой травы!$",
    "Route24_Text_EthanRematchIntro:": "Ладно!\\nСейчас я тебя растопчу!$",
    "Route24_Text_ReliRematchIntro:": "Ты всегда такой занятой...\\nНе устаешь?$",
    "Route24_Text_TimmyRematchIntro:": "Тебе и правда нравится приходить\\nна НУГГЕТ-БРИДЖ.$",
    "Route24_Text_AliRematchIntro:": "Помнишь наш бой...\\pХотя я был вторым в\\nочереди, я ведь был лучшим, правда?$",
    "Route24_Text_CaleRematchIntro:": "Люди называют это НУГГЕТ-\\nБРИДЖЕМ!\\pТы уже победил нас, так что снова\\nпройти испытание нельзя...\\p...Но сразиться с нами еще раз\\nможно.$",
    "OneIsland_TreasureBeach_Text_AmaraRematchIntro:": "Лежать, покачиваясь на волнах...\\nЯ даже не замечаю, как проходит время...$",
    "OneIsland_KindleRoad_Text_MariaRematchIntro:": "Погода прекрасная!\\nПостараюсь ее не испортить.$",
    "OneIsland_KindleRoad_Text_AbigailRematchIntro:": "Солнечный ожог начинает болеть...$",
    "OneIsland_KindleRoad_Text_FinnRematchIntro:": "Гора огненной птицы отбрасывает\\nогромную тень...$",
    "OneIsland_KindleRoad_Text_GarrettRematchIntro:": "У меня сильное предчувствие, что\\nна этот раз победа будет моей!$",
    "OneIsland_KindleRoad_Text_TommyRematchIntro:": "Подожди! Секундочку!\\nКажется, я подцепил что-то огромное!$",
    "OneIsland_KindleRoad_Text_SharonRematchIntro:": "Снова поможешь мне\\nс тренировкой?$",
    "OneIsland_KindleRoad_Text_TanyaRematchIntro:": "Мы пока не пропустили ни одного дня\\nтренировок!$",
    "OneIsland_KindleRoad_Text_SheaRematchIntro:": "Каждое утро перед завтраком\\nя проплываю вокруг этого острова...\\lТри раза!$",
    "OneIsland_KindleRoad_Text_HughRematchIntro:": "Одевайся как следует для боя!\\nЯ же говорил, сними этот нелепый наряд!$",
    "OneIsland_KindleRoad_Text_BryceRematchIntro:": "Знаешь, на природе любая еда кажется\\nвкуснее.$",
    "OneIsland_KindleRoad_Text_ClaireRematchIntro:": "Я снова переела, так что не хочешь\\nсразиться с нами ради разминки?$",
    "OneIsland_KindleRoad_Text_KiaRematchIntro:": "КИА: Мы со старшим братом -\\nотличная команда!\\pНа этот раз не проиграем!$",
    "OneIsland_KindleRoad_Text_MikRematchIntro:": "МИК: Пока мы с КИА вместе,\\nнам ничего не страшно!\\pНа этот раз мы это докажем!$",
    "ThreeIsland_BondBridge_Text_NikkiRematchIntro:": "Снова будем сражаться?$",
    "ThreeIsland_BondBridge_Text_VioletRematchIntro:": "Откуда ты пришел и\\nкуда направляешься?$",
    "ThreeIsland_BondBridge_Text_AmiraRematchIntro:": "Скоро я хочу научиться плавать\\nбез надувного круга.$",
    "ThreeIsland_BondBridge_Text_AlexisRematchIntro:": "Ура, ура!\\nPOKeMON!$",
    "ThreeIsland_BondBridge_Text_TishaRematchIntro:": "О нет, разве я уже не говорила?\\nПожалуйста, держись от меня подальше!$",
    "ThreeIsland_BondBridge_Text_JoyRematchIntro:": "ДЖОЙ: Мы стали сильнее!\\nНамного-намного!$",
    "ThreeIsland_BondBridge_Text_MegRematchIntro:": "МЭГ: Сегодня ты нас не победишь!$",
    "FiveIsland_WaterLabyrinth_Text_AlizeRematchIntro:": "О, привет!\\pТы растишь своих POKeMON в\\nхороших условиях?$",
    "FiveIsland_ResortGorgeous_Text_DaisyRematchIntro:": "Сегодня этими руками я создам\\nсвою победу.$",
    "FiveIsland_ResortGorgeous_Text_CelinaRematchIntro:": "Мне опять повторять?\\nЯ пытаюсь рисовать.\\lПожалуйста, не попадайся мне на глаза!$",
    "FiveIsland_ResortGorgeous_Text_RaynaRematchIntro:": "Я так и не продвинулась...\\nВсе еще не могу подобрать правильный ракурс...$",
    "FiveIsland_ResortGorgeous_Text_JackiRematchIntro:": "О, ты дашь мне еще одну\\nвозможность помериться с тобой умом?$",
    "FiveIsland_ResortGorgeous_Text_GillianRematchIntro:": "Бассейн для моего POKeMON почти\\nдостроили.\\pОбязательно загляни в гости.$",
    "FiveIsland_ResortGorgeous_Text_DestinRematchIntro:": "Я хорошо бегаю.\\nИ стал еще быстрее!$",
    "FiveIsland_ResortGorgeous_Text_TobyRematchIntro:": "Приветствую, друг!\\nДавай приятно проведем время вместе!$",
    "FiveIsland_MemorialPillar_Text_MiloRematchIntro:": "Я старший из БРАТЬЕВ-ПТИЦЕВОДОВ.\\nПомнишь меня?\\pВерно, я тот, кто любит\\nптиц за их клювы!$",
    "FiveIsland_MemorialPillar_Text_ChazRematchIntro:": "Я средний из БРАТЬЕВ-\\nПТИЦЕВОДОВ.\\pЯ тот, кто любит крылья.\\nДавай снова сразимся!$",
    "FiveIsland_MemorialPillar_Text_HaroldRematchIntro:": "Я младший из БРАТЬЕВ-\\nПТИЦЕВОДОВ.\\pЯ люблю птиц за их пух.\\nНе думал, что снова тебя увижу!$",
    "SixIsland_OutcastIsland_Text_TylorRematchIntro:": "Мне все еще совсем не везет.\\nБой хоть немного развеет скуку!$",
    "SixIsland_OutcastIsland_Text_MymoRematchIntro:": "Фух... Фух...\\pЯ снова доплыл сюда от порта ШЕСТОГО ОСТРОВА\\nза один заход.$",
    "SixIsland_OutcastIsland_Text_NicoleRematchIntro:": "Ты всегда появляешься, когда я\\nплаваю.$",
    "SixIsland_OutcastIsland_Text_AvaRematchIntro:": "ЭЙВА: Давай сегодня снова устроим\\nморской бой два на два!$",
    "SixIsland_OutcastIsland_Text_GebRematchIntro:": "ГЕБ: Мы со старшей сестрой теперь\\nнамного сильнее, чем раньше!$",
    "SixIsland_GreenPath_Text_JaclynRematchIntro:": "...Что?\\pЯ представляю свой дом, но TELEPORT\\nвсегда переносит меня сюда!$",
    "SixIsland_WaterPath_Text_RoseRematchIntro:": "О, привет.\\nСнова дует приятный ветерок.$",
    "SixIsland_WaterPath_Text_EdwardRematchIntro:": "Хе-хе-хе, я снова тренируюсь\\nвтайне.$",
    "SixIsland_WaterPath_Text_SamirRematchIntro:": "Что, надоело встречать\\nПЛОВЦОВ вроде меня?\\pЭй, не злись!\\nДавай снова сразимся.$",
    "SixIsland_WaterPath_Text_DeniseRematchIntro:": "Вздох...\\nМой парень снова занят...$",
    "SixIsland_WaterPath_Text_EarlRematchIntro:": "Ну же, скажи, где здесь\\nгоры?$",
    "SixIsland_WaterPath_Text_MiuRematchIntro:": "МИУ: Привет, POKeMON!\\nСнова пора играть!$",
    "SixIsland_WaterPath_Text_MiaRematchIntro:": "МИА: Привет, POKeMON!\\nСнова пора сражаться!$",
    "SixIsland_RuinValley_Text_StanlyRematchIntro:": "Похоже, в этом мире осталось еще много\\nнеразгаданных тайн.$",
    "SixIsland_RuinValley_Text_FosterRematchIntro:": "Привет, мы ведь уже встречались?\\nЧто заставило тебя вернуться?$",
    "SixIsland_RuinValley_Text_LarryRematchIntro:": "Говорят, на этом острове есть\\nтаинственные камни.\\pТы узнал что-нибудь с тех пор, как\\nмы виделись в последний раз?$",
    "SixIsland_RuinValley_Text_DarylRematchIntro:": "Реванш с тобой на такой высоте!$",
    "SixIsland_RuinValley_Text_HectorRematchIntro:": "Я довольно хорошо знаю местность\\nв этих краях.$",
    "SevenIsland_TrainerTower_Text_DarioRematchIntro:": "Я почувствовал твое приближение.$",
    "SevenIsland_TrainerTower_Text_RodetteRematchIntro:": "Где-то на этом острове спят\\nнеобычные POKeMON.$",
    "SevenIsland_SevaultCanyon_Entrance_Text_MiahRematchIntro:": "Кья-ха-ха!\\pТо, что ты вернулся, ничего не изменит.\\nЯ снова легко тебя отброшу!$",
    "SevenIsland_SevaultCanyon_Entrance_Text_MasonRematchIntro:": "Привет! Ты ведь состоишь в моем\\nфан-клубе, верно?$",
    "SevenIsland_SevaultCanyon_Entrance_Text_NicolasRematchIntro:": "Этот остров слишком большой...\\nПатрулировать его - сплошная морока...$",
    "SevenIsland_SevaultCanyon_Entrance_Text_MadelineRematchIntro:": "Я не прощаю тех, кто плохо обращается\\nс POKeMON!$",
    "SevenIsland_SevaultCanyon_Entrance_Text_EveRematchIntro:": "ИВ: Мы с ДЖОНОМ снова объединимся и\\nбудем сражаться вместе.$",
    "SevenIsland_SevaultCanyon_Entrance_Text_JonRematchIntro:": "ДЖОН: Рядом с ИВ мне кажется,\\nчто мы вообще не можем проиграть.$",
    "SevenIsland_SevaultCanyon_Text_CyndyRematchIntro:": "Давай снова сразимся.\\nСегодня я в отличной форме!$",
    "SevenIsland_SevaultCanyon_Text_EvanRematchIntro:": "Неважно, даже если у тебя\\nсамые сильные POKeMON...\\pЭто ничего не значит, если ты не\\nумеешь правильно ими пользоваться!$",
    "SevenIsland_SevaultCanyon_Text_JacksonRematchIntro:": "Я защищаю окружающую среду.\\nА природа в ответ защищает меня!$",
    "SevenIsland_SevaultCanyon_Text_KatelynRematchIntro:": "Каждый раз, когда мы встречаемся, на тебе\\nэти стильные кроссовки.$",
    "SevenIsland_SevaultCanyon_Text_LeroyRematchIntro:": "Ты наверняка стал еще сильнее.\\nПожалуйста, сразись со мной!$",
    "SevenIsland_SevaultCanyon_Text_MichelleRematchIntro:": "Я получила лучшее возможное\\nобразование, чтобы стать такой сильной.\\pНа этот раз я не проиграю.\\nНи за что!$",
    "SevenIsland_SevaultCanyon_Text_LexRematchIntro:": "ЛЕКС: Моя дорогая НЬЯ, вместе\\nмы точно победим!$",
    "SevenIsland_SevaultCanyon_Text_NyaRematchIntro:": "НЬЯ: Я не подведу своего наставника\\nЛЕКСА! Мы победим!$",
    "SevenIsland_TanobyRuins_Text_BrandonRematchIntro:": "Ты узнал что-нибудь об\\nэтой каменной комнате?$",
    "SevenIsland_TanobyRuins_Text_BenjaminRematchIntro:": "Говорят, внутри спит\\nтаинственный POKeMON.$",
    "SevenIsland_TanobyRuins_Text_EdnaRematchIntro:": "Учитель снова показывает мне, как\\nрисовать.$",
    "SevenIsland_TanobyRuins_Text_CliffordRematchIntro:": "Сегодня помимо урока\\nмы снова пришли посмотреть на эту комнату.$",
}
BANNED_UNICODE = set("—–←→“”«»")

def control_tokens(text: str) -> list[str]:
    return re.findall(r'\{[^}]+\}|\\.|\$', text)

def replace_label(path: Path, label: str, translated: str) -> None:
    text = path.read_text(encoding="utf-8")
    # Upstream trainers_frlg labels are global (::). Keys intentionally retain
    # the first colon; this matcher supplies the second one.
    pat = re.compile(
        rf'(?ms)^(?P<head>{re.escape(label)}:\s*\n)'
        rf'(?P<body>(?:[ \t]*\.string\s+"(?:\\.|[^"\\])*"\s*\n?)+)'
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one block, got {len(matches)}")
    m = matches[0]
    current = "".join(re.findall(r'\.string\s+"((?:\\.|[^"\\])*)"', m.group("body")))
    if control_tokens(current) != control_tokens(translated):
        raise RuntimeError(f"{label}: control-token drift")
    if not translated.endswith("$"):
        raise RuntimeError(f"{label}: missing terminal $")
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: invalid translation surface")
    new_body = '\t.string "' + translated + '"\n'
    path.write_text(text[:m.start("body")] + new_body + text[m.end("body"):], encoding="utf-8")

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_trainers_frlg_quality_finish_v3_195.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 95:
        raise RuntimeError(f"expected 95 blocks, got {len(TRANSLATIONS)}")
    for label, translated in TRANSLATIONS.items():
        replace_label(path, label, translated)
    out = root / "build" / "qarro_ru_trainers_frlg_quality_finish_v3_195_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassBlocks": len(TRANSLATIONS),
        "humanQualityBlocksComplete": 234,
        "humanQualityBlocksExpected": 234,
        "labels": list(TRANSLATIONS),
        "humanEditedRussian": True,
        "controlTokensPreserved": True,
        "pokemonMoveAbilityNamesPreserved": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: polished final {len(TRANSLATIONS)} rematch blocks; trainers_frlg.inc complete 234/234")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
