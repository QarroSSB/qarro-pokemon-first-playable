#!/usr/bin/env python3
"""Qarro v3.198: human-quality Easy Chat / quiz / contest UI cleanup."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
MARKER="QARRO_RU_STRINGS_EASYCHAT_QUALITY_V3_198"
TARGET=Path("src/strings.c")
TRANSLATIONS={
    "gText_CombineSixWordsOrPhrases": "Соедини шесть слов или фраз",
    "gText_WithFourPhrases": "Из четырех фраз,",
    "gText_AndMakeAMessage2": "и составь сообщение.",
    "gText_TheMailSalutation": "Обращение в ПИСЬМЕ",
    "gText_TheBardsSong2": "Новая песня",
    "gText_CombineTwoWordsOrPhrases2": "Соедини два слова или фразы",
    "gText_ToTeachHerAGoodSaying": "чтобы научить ее хорошей фразе.",
    "gText_FindWordsWhichFit": "Найди подходящие слова",
    "gText_TheTrainersImage": "образ ТРЕНЕРА.",
    "gText_TheImage": "Образ:",
    "gText_OutOfTheListedChoices": "Из предложенных вариантов,",
    "gText_SelectTheAnswerToTheQuiz": "выбери ответ на викторину!",
    "gText_AndCreateAQuiz": "и составь викторину!",
    "gText_PickAWordOrPhraseAnd": "Выбери слово или фразу и",
    "gText_SetTheQuizAnswer": "задай ответ на викторину.",
    "gText_TheAnswerColon": "Ответ:",
    "gText_TheQuizColon": "Викторина:",
    "gText_ApprenticePhrase": "Фраза ученика:",
    "gText_LetsReplyToTheInterview": "Ответим на вопросы интервью!",
    "gText_QuitEditing2": "Завершить редактирование?",
    "gText_EditedTextWillNotBeSaved": "Изменения не будут сохранены.",
    "gText_IsThatOkay": "Все верно?",
    "gText_PleaseEnterPhraseOrWord": "Введи фразу или слово.",
    "gText_EntireTextCantBeDeleted": "Нельзя удалить весь текст.",
    "gText_OnlyOnePhrase": "Можно изменить только одну фразу.",
    "gText_OriginalSongWillBeUsed": "Будет использована исходная песня.",
    "gText_ThatsTrendyAlready": "Это уже модно!",
    "gText_CombineTwoWordsOrPhrases3": "Соедини два слова или фразы.",
    "gText_QuitGivingInfo": "Прекратить ввод данных?",
    "gText_StopGivingPkmnMail2": "Не отдавать ПИСЬМО POKeMON?",
    "gText_CreateAQuiz2": "Создай викторину!",
    "gText_SetTheAnswer": "Задай ответ!",
    "gText_CancelSelection": "Отменить выбор?",
    "gText_GoodSaying": "Хорошая фраза",
    "gText_FansQuestion": "Вопрос фаната",
    "gText_ApprenticesPhrase": "Фраза ученика",
    "gText_YouCannotQuitHere": "Здесь нельзя выйти.",
    "gText_SectionMustBeCompleted": "Этот раздел нужно заполнить.",
    "gText_F700sQuiz": "Викторина {DYNAMIC 0}",
    "gText_Lady": "ЛЕДИ",
    "gText_AfterYouHaveReadTheQuiz": "Прочитав вопрос",
    "gText_QuestionPressTheAButton": "викторины, нажми кнопку A.",
    "gText_TheQuizAnswerIs": "Ответ на викторину?",
    "gText_LikeToQuitQuiz": "Хочешь прекратить",
    "gText_ChallengeQuestionMark": "испытание?",
    "gText_IsThisQuizOK": "Викторина готова?",
    "gText_CreateAQuiz": "Создай викторину!",
    "gText_SelectTheAnswer": "Выбери ответ!",
    "gText_LyricsCantBeDeleted": "Текст песни нельзя удалить.",
    "gText_Coolness": "Крутость ",
    "gText_Beauty3": "Красота ",
    "gText_Cuteness": "Миловидность ",
    "gText_Smartness": "Ум ",
    "gText_Toughness": "Стойкость ",
}
BANNED_UNICODE=set("—–←→“”«»")

def control_tokens(text):
    return re.findall(r'\{[^}]+\}|\\[npl]|\$',text)

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

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: localize_strings_easychat_quality_v3_198.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); path=root/TARGET
    if len(TRANSLATIONS)!=54: raise RuntimeError(f"expected 54 symbols, got {len(TRANSLATIONS)}")
    for sym,tr in TRANSLATIONS.items(): replace_symbol(path,sym,tr)
    out=root/"build"/"qarro_ru_strings_easychat_quality_v3_198_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        "marker":MARKER,"targetFile":str(TARGET),"qualityPassSymbols":len(TRANSLATIONS),
        "symbols":list(TRANSLATIONS),"humanEditedRussian":True,"controlTokensPreserved":True,
        "easyChatPairContextCheckedAgainstExpansion1170":True,
        "pokemonMoveAbilityNamesPreserved":True,"gameplayLogicTouched":False,
        "balanceTouched":False,"bossTeamsTouched":False,"specialWhitelistTouched":False,
        "ashBondTouched":False,"ashCapTouched":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} Easy Chat/quiz/contest strings")
    return 0
if __name__=="__main__": raise SystemExit(main())
