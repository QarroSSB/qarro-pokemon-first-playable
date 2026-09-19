#!/usr/bin/env python3
"""Qarro v3.172: sweep remaining small FRLG text surfaces.

Targets 87 user-facing English remnants across the new-game preset names,
trade text, Oak aides, Pokémon Center, Route 23 gates, area-screen labels,
party utility messages, move-tutor warning, mail/start-menu labels and a few
summary labels. Technical abbreviations such as IVs/EVs, grade letters and
button-mode literals are intentionally not changed here.
"""
from __future__ import annotations
from collections import Counter
import json,re,sys
from pathlib import Path

MARKER="QARRO_RU_SMALL_SURFACE_SWEEP_V3_172"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
TOKEN_RE=re.compile(r"\{[^{}]+\}|\$")

def sem_tokens(s): return Counter(TOKEN_RE.findall(s))

def replace_block(root, rel, label, repl):
    p=root/rel
    text=p.read_text(encoding="utf-8")
    ms=list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$",text))
    if len(ms)!=1: raise RuntimeError(f"{rel}:{label}: expected 1 label, got {len(ms)}")
    st=ms[0].start(); nxt=LABEL_RE.search(text,ms[0].end()); en=nxt.start() if nxt else len(text)
    old=text[st:en]
    if sem_tokens(old)!=sem_tokens(repl):
        raise RuntimeError(f"{rel}:{label}: semantic token mismatch {sem_tokens(old)} != {sem_tokens(repl)}")
    p.write_text(text[:st]+repl+"\n"+text[en:],encoding="utf-8")

def replace_exact(root, rel, old, new, label):
    p=root/rel; text=p.read_text(encoding="utf-8"); n=text.count(old)
    if n!=1: raise RuntimeError(f"{rel}:{label}: expected one exact anchor, got {n}")
    p.write_text(text.replace(old,new,1),encoding="utf-8")

NEW_NAMES={
'"NEW NAME$"':'"НОВОЕ ИМЯ$"','"GREEN$"':'"ГРИН$"','"RED$"':'"РЕД$"','"LEAF$"':'"ЛИФ$"',
'"FIRE$"':'"ФАЙР$"','"GARY$"':'"ГЭРИ$"','"KAZ$"':'"КАЗ$"','"TORU$"':'"ТОРУ$"',
'"ASH$"':'"ЭШ$"','"KENE$"':'"КЕНЕ$"','"GEKI$"':'"ГЕКИ$"','"JAK$"':'"ДЖАК$"',
'"JANNE$"':'"ЯННЕ$"','"JONN$"':'"ДЖОНН$"','"KAMON$"':'"КАМОН$"','"KARL$"':'"КАРЛ$"',
'"TAYLOR$"':'"ТЕЙЛОР$"','"OSCAR$"':'"ОСКАР$"','"HIRO$"':'"ХИРО$"','"MAX$"':'"МАКС$"',
'"JON$"':'"ДЖОН$"','"RALPH$"':'"РАЛЬФ$"','"KAY$"':'"КЕЙ$"','"TOSH$"':'"ТОШ$"',
'"ROAK$"':'"РОАК$"','"OMI$"':'"ОМИ$"','"JODI$"':'"ДЖОДИ$"','"AMANDA$"':'"АМАНДА$"',
'"HILLARY$"':'"ХИЛЛАРИ$"','"MAKEY$"':'"МЭЙКИ$"','"MICHI$"':'"МИЧИ$"','"PAULA$"':'"ПАУЛА$"',
'"JUNE$"':'"ДЖУН$"','"CASSIE$"':'"КЭССИ$"','"REY$"':'"РЕЙ$"','"SEDA$"':'"СЕДА$"',
'"KIKO$"':'"КИКО$"','"MINA$"':'"МИНА$"','"NORIE$"':'"НОРИ$"','"SAI$"':'"САЙ$"',
'"MOMO$"':'"МОМО$"','"SUZI$"':'"СЮЗИ$"',
}

BLOCKS=[
("data/scripts/move_tutors_frlg.inc","Text_MoveCanOnlyBeLearnedOnce",r'''Text_MoveCanOnlyBeLearnedOnce::
	.string "Этот прием можно выучить только\n"
	.string "один раз. Все в порядке?$"
'''),
("data/scripts/aide.inc","Aide_Text_HaventCaughtEnoughMonsForItem",r'''Aide_Text_HaventCaughtEnoughMonsForItem::
	.string "Посмотрим…\n"
	.string "Ой! Ты поймал только\l"
	.string "{STR_VAR_3} видов POKeMON!\p"
	.string "Нужно {STR_VAR_1} видов,\n"
	.string "чтобы получить {STR_VAR_2}.$"
'''),
("data/scripts/aide.inc","Aide_Text_GetEnoughMonsComeBackForItem",r'''Aide_Text_GetEnoughMonsComeBackForItem::
	.string "…Понятно.\p"
	.string "Когда поймаешь {STR_VAR_1} видов POKeMON,\n"
	.string "вернись за {STR_VAR_2}.$"
'''),
("data/scripts/aide.inc","Aide_Text_DontHaveAnyRoomForItem",r'''Aide_Text_DontHaveAnyRoomForItem::
	.string "О! Похоже, у тебя нет\n"
	.string "места для {STR_VAR_2}.$"
'''),
("data/scripts/pkmn_center_nurse_frlg.inc","Text_WelcomeWantToHealPkmn_Frlg",r'''Text_WelcomeWantToHealPkmn_Frlg::
	.string "Добро пожаловать в наш POKeMON CENTER!\p"
	.string "Хочешь, я полностью вылечу\n"
	.string "твоих POKeMON?$"
'''),
("data/scripts/pkmn_center_nurse_frlg.inc","Text_TakeYourPkmnForFewSeconds_Frlg",r'''Text_TakeYourPkmnForFewSeconds_Frlg::
	.string "Хорошо, я заберу твоих POKeMON\n"
	.string "на несколько секунд.$"
'''),
("data/scripts/pkmn_center_nurse_frlg.inc","Text_WeHopeToSeeYouAgain_Frlg",r'''Text_WeHopeToSeeYouAgain_Frlg::
	.string "Будем рады видеть тебя снова!$"
'''),
("data/scripts/pkmn_center_nurse_frlg.inc","Text_RestoredPkmnToFullHealth_Frlg",r'''Text_RestoredPkmnToFullHealth_Frlg::
	.string "Спасибо за ожидание.\n"
	.string "Твои POKeMON полностью\l"
	.string "восстановлены.$"
'''),
("data/scripts/route23.inc","Text_OnlySkilledTrainersAllowedThrough",r'''Text_OnlySkilledTrainersAllowedThrough::
	.string "Только по-настоящему сильные TRAINERS\n"
	.string "могут пройти дальше.\p"
	.string "У тебя еще нет {STR_VAR_1}!$"
'''),
("data/scripts/route23.inc","Text_CantLetYouPass",r'''Text_CantLetYouPass::
	.string "Правила есть правила.\n"
	.string "Я не могу тебя пропустить.$"
'''),
("data/scripts/route23.inc","Text_OhThatsBadgeGoRightAhead",r'''Text_OhThatsBadgeGoRightAhead::
	.string "О! Это же {STR_VAR_1}!\n"
	.string "Проходи.$"
'''),
("data/scripts/route23.inc","Text_OnlyPassWithBadgeDontHaveYet",r'''Text_OnlyPassWithBadgeDontHaveYet::
	.string "Здесь можно пройти только с\n"
	.string "{STR_VAR_1}.\p"
	.string "У тебя пока нет {STR_VAR_1}.\p"
	.string "Он нужен, чтобы попасть в\n"
	.string "POKeMON LEAGUE.$"
'''),
("data/scripts/route23.inc","Text_OnlyPassWithBadgeOhGoAhead",r'''Text_OnlyPassWithBadgeOhGoAhead::
	.string "Здесь можно пройти только с\n"
	.string "{STR_VAR_1}.\p"
	.string "О! Это же {STR_VAR_1}!{PAUSE_MUSIC}{PLAY_BGM}{MUS_LEVEL_UP}{PAUSE 0x60}{RESUME_MUSIC}\p"
	.string "Все в порядке.\n"
	.string "Проходи.$"
'''),

("data/text/ingame_trade_frlg.inc","Trade_Text_LookingForMonWannaTradeForMon",r'''Trade_Text_LookingForMonWannaTradeForMon::
	.string "Я ищу POKeMON\n"
	.string "{STR_VAR_1}!\p"
	.string "Обменяешь его на моего\n"
	.string "{STR_VAR_2}?$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_AwwOhWell",r'''Trade_Text_AwwOhWell::
	.string "Ох!\n"
	.string "Ну ладно…$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_WhatThatsNoMon",r'''Trade_Text_WhatThatsNoMon::
	.string "Что?\n"
	.string "Это не {STR_VAR_1}!$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_HeyThanks",r'''Trade_Text_HeyThanks::
	.string "Эй, спасибо!$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_IsntMyOldMonGreat",r'''Trade_Text_IsntMyOldMonGreat::
	.string "Разве мой старый {STR_VAR_2} не прекрасен?$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_DoYouHaveMonWouldYouTradeForMon",r'''Trade_Text_DoYouHaveMonWouldYouTradeForMon::
	.string "Привет! У тебя случайно нет\n"
	.string "{STR_VAR_1}?\p"
	.string "Согласишься обменять его\n"
	.string "на моего {STR_VAR_2}?$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_WellIfYouDontWantTo",r'''Trade_Text_WellIfYouDontWantTo::
	.string "Ну, если не хочешь…$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_ThisIsntMon",r'''Trade_Text_ThisIsntMon::
	.string "Хм-м?\n"
	.string "Это не {STR_VAR_1}.\p"
	.string "Вспомни обо мне, если поймаешь.$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_Thanks",r'''Trade_Text_Thanks::
	.string "Спасибо!$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_HasTradedMonGrownStronger",r'''Trade_Text_HasTradedMonGrownStronger::
	.string "{STR_VAR_2}, которого я тебе обменял,\n"
	.string "стал сильнее?$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_DoYouHaveMonWantToTradeForMon",r'''Trade_Text_DoYouHaveMonWantToTradeForMon::
	.string "Привет!\n"
	.string "У тебя есть {STR_VAR_1}?\p"
	.string "Хочешь обменять его на моего\n"
	.string "{STR_VAR_2}?$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_ThatsTooBad",r'''Trade_Text_ThatsTooBad::
	.string "Очень жаль.$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_ThisIsNoMon",r'''Trade_Text_ThisIsNoMon::
	.string "…Это не {STR_VAR_1}.\p"
	.string "Если поймаешь, обменяй со мной.$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_ThanksYoureAPal",r'''Trade_Text_ThanksYoureAPal::
	.string "Спасибо, ты настоящий друг!$"
'''),
("data/text/ingame_trade_frlg.inc","Trade_Text_HowIsMyOldMon",r'''Trade_Text_HowIsMyOldMon::
	.string "Как там мой старый {STR_VAR_2}?\n"
	.string "Мой {STR_VAR_1} чувствует себя отлично!$"
'''),
]

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: localize_small_surface_sweep_v3_172.py <upstream-root>")
    root=Path(sys.argv[1]).resolve()
    applied=[]

    # 42 preset-name/name-label literals + one remaining START hint.
    rel="data/text/new_game_intro_frlg.inc"
    for old,new in NEW_NAMES.items():
        replace_exact(root,rel,old,new,old); applied.append((rel,old))
    start_old='''gControlsGuide_Text_StartButton::
\t.string "Press this button to open the\\n"
\t.string "MENU.$"'''
    start_new='''gControlsGuide_Text_StartButton::
\t.string "Нажми эту кнопку, чтобы открыть\\n"
\t.string "МЕНЮ.$"'''
    replace_exact(root,rel,start_old,start_new,"START hint"); applied.append((rel,"START hint"))

    for rel,label,repl in BLOCKS:
        replace_block(root,rel,label,repl); applied.append((rel,label))

    # Tiny C-runtime leftovers.
    replace_exact(root,"src/mail.c",'static const u8 sText_FromSpace[] = _("From ");',
                  'static const u8 sText_FromSpace[] = _("От ");',"mail From")
    applied.append(("src/mail.c","sText_FromSpace"))
    replace_exact(root,"src/start_menu.c",'static const u8 sText_MenuDebug[] = _("DEBUG");',
                  'static const u8 sText_MenuDebug[] = _("ОТЛАДКА");',"DEBUG")
    applied.append(("src/start_menu.c","sText_MenuDebug"))

    # Pokédex area screen labels.
    area={
      '    static const u8 gText_Morning[] = _("{DPAD_UPDOWN} MORNING");':'    static const u8 gText_Morning[] = _("{DPAD_UPDOWN} УТРО");',
      '    static const u8 gText_Day[] = _("{DPAD_UPDOWN} DAY");':'    static const u8 gText_Day[] = _("{DPAD_UPDOWN} ДЕНЬ");',
      '    static const u8 gText_Evening[] = _("{DPAD_UPDOWN} EVENING");':'    static const u8 gText_Evening[] = _("{DPAD_UPDOWN} ВЕЧЕР");',
      '    static const u8 gText_Night[] = _("{DPAD_UPDOWN} NIGHT");':'    static const u8 gText_Night[] = _("{DPAD_UPDOWN} НОЧЬ");',
      '    static const u8 gText_AreaUnknown[] = _("AREA UNKNOWN");':'    static const u8 gText_AreaUnknown[] = _("ОБЛАСТЬ НЕИЗВЕСТНА");',
    }
    for old,new in area.items():
        replace_exact(root,"src/pokedex_area_screen.c",old,new,old); applied.append(("src/pokedex_area_screen.c",old))

    # Remaining semantic party-menu messages (two box messages were localized earlier).
    party={
      'static const u8 sText_askText[] = _("Would you like to change {STR_VAR_1}\'s\\nability to {STR_VAR_2}?");':
      'static const u8 sText_askText[] = _("Сменить способность {STR_VAR_1}\\nна {STR_VAR_2}?");',
      'static const u8 sText_doneText[] = _("{STR_VAR_1}\'s ability became\\n{STR_VAR_2}!{PAUSE_UNTIL_PRESS}");':
      'static const u8 sText_doneText[] = _("Способность {STR_VAR_1} стала\\n{STR_VAR_2}!{PAUSE_UNTIL_PRESS}");',
      'static const u8 sText_BasePointsResetToZero[] = _("{STR_VAR_1}\'s base points\\nwere all reset to zero!{PAUSE_UNTIL_PRESS}");':
      'static const u8 sText_BasePointsResetToZero[] = _("Базовые очки {STR_VAR_1}\\nсброшены до нуля!{PAUSE_UNTIL_PRESS}");',
      '    static const u8 sText_doneText[] = _("{STR_VAR_1}\'s Dynamax Level\\nincreased by 1!{PAUSE_UNTIL_PRESS}");':
      '    static const u8 sText_doneText[] = _("Dynamax Level {STR_VAR_1}\\nповышен на 1!{PAUSE_UNTIL_PRESS}");',
    }
    for old,new in party.items():
        replace_exact(root,"src/party_menu.c",old,new,old); applied.append(("src/party_menu.c",old))

    # Semantic summary labels; grades and IV/EV remain technical tokens.
    summary={
      'static const u8 sText_Relearn[] = _("{START_BUTTON} RELEARN");':
      'static const u8 sText_Relearn[] = _("{START_BUTTON} ПЕРЕУЧ.");',
      '    const u8* gText_SkillPageStats = COMPOUND_STRING("STATS");':
      '    const u8* gText_SkillPageStats = COMPOUND_STRING("ПАРАМ.");',
      '    const u8* gText_Rename = COMPOUND_STRING("RENAME");':
      '    const u8* gText_Rename = COMPOUND_STRING("ИМЯ");',
    }
    for old,new in summary.items():
        # Relearn source line has a trailing comment, so use prefix literal.
        p=root/"src/pokemon_summary_screen.c"; text=p.read_text(encoding="utf-8"); n=text.count(old)
        if n!=1: raise RuntimeError(f"summary anchor expected 1, got {n}: {old}")
        p.write_text(text.replace(old,new,1),encoding="utf-8"); applied.append(("src/pokemon_summary_screen.c",old))

    out=root/"build"/"qarro_ru_small_surface_sweep_v3_172_audit.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
      "marker":MARKER,"translatedOperations":len(applied),
      "files":sorted(set(x[0] for x in applied)),
      "logicTouched":False,"ashBondTouched":False,"ashCapTouched":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: {len(applied)} exact/block localization operations across {len(set(x[0] for x in applied))} files")
    return 0
if __name__=="__main__": raise SystemExit(main())
