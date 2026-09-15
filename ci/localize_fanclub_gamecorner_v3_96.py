#!/usr/bin/env python3
"""Qarro v3.96 bulk Russian localization: Saffron Trainer Fan Club + Celadon Game Corner.

Translates the 38 + 35 English-only FireRed runtime _Text_ blocks reported by
current surface audit in these two untouched interiors (73 total).
Pokemon species, Move and Ability proper names remain English by project canon.
Ash Bond / Ash Cap and gameplay logic are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FANCLUB_GAMECORNER_V3_96"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    Path("data/maps/SaffronCity_PokemonTrainerFanClub_Frlg/scripts.inc"): {
        "SaffronCity_PokemonTrainerFanClub_Text_HuhYou": "Хм?\\nТы...$",
        "SaffronCity_PokemonTrainerFanClub_Text_YourePlayerWereYourFansNow": "Неужели...\\n...\\pТочно!\\nТы {PLAYER}!\\pМы только что говорили о тебе!\\pО том, что появился невероятно\\nсильный ТРЕНЕР.\\pИ это ты!\\nТы такой крутой!\\pМы решили создать твой\\nФАН-КЛУБ!\\pНадеемся, ты продолжишь сражаться\\nи показывать, чего стоишь.\\pМожет, тогда появятся и другие\\nтвои поклонники.$",
        "SaffronCity_PokemonTrainerFanClub_Text_AlwaysCheerForYou": "Я всегда буду болеть за тебя!\\pВперёд, {PLAYER}, вперёд!$",
        "SaffronCity_PokemonTrainerFanClub_Text_IllAlwaysBelieveInYou": "Я всегда буду верить в тебя,\\n{PLAYER}.\\pПокажи остальным, на что ты\\nспособен в серьёзном бою.$",
        "SaffronCity_PokemonTrainerFanClub_Text_WasYourFanNotAnymore": "Прости.\\nРаньше я был твоим фанатом.\\pНо теперь ты будто потерял\\nпрежний огонь.\\pВ последнее время {STR_VAR_1}\\nкажется мне куда круче.$",
        "SaffronCity_PokemonTrainerFanClub_Text_EveryonesYourFanButICantBe": "О!\\n{PLAYER}!\\pВсе вокруг в последнее время\\nтолько о тебе и говорят.\\pЯ понимаю почему.\\nЯ знаю, что ты силён.\\pНо знаешь что?\\pСтав фанатом {STR_VAR_1},\\nя не могу просто так передумать.$",
        "SaffronCity_PokemonTrainerFanClub_Text_TrainersCoolWhenBattling": "ТРЕНЕРЫ так круто выглядят\\nво время боя.\\pПравда ведь?$",
        "SaffronCity_PokemonTrainerFanClub_Text_CanYouAutographShorts": "О! Это {PLAYER}!\\nВот это круто!\\pА!\\nТочно!\\pДашь автограф?\\nМожет, прямо на моих шортах?$",
        "SaffronCity_PokemonTrainerFanClub_Text_CountingOnYou": "Как бы жарко ни было...\\pИ как бы холодно ни стало...\\pЯ всегда верил в шорты\\nи всегда их носил!\\pРассчитываю, что ты продолжишь\\nпобеждать!\\pЯ верю в тебя так же сильно,\\nкак в свои шорты!$",
        "SaffronCity_PokemonTrainerFanClub_Text_BrocksMyHero": "БРОК - мой герой!\\nНастоящий мужик!\\pХе-хе, я кое-что попросил\\nу мамы.\\pОна вышила БРОК на\\nмоих шортах!$",
        "SaffronCity_PokemonTrainerFanClub_Text_BrocksFanToBitterEnd": "...\\p...\\nЯ фанат БРОКА!\\pДаже если останусь единственным,\\nклянусь своей каменной волей\\lи своими шортами!\\pБуду его фанатом до самого конца!$",
        "SaffronCity_PokemonTrainerFanClub_Text_BrocksLastWordOnCool": "БРОК - воплощение крутости,\\nи точка!\\pВот на кого я хочу\\nбыть похожим!$",
        "SaffronCity_PokemonTrainerFanClub_Text_HadPleasureOfWatchingYouBattle": "{PLAYER}, мне довелось наблюдать\\nза твоими боями.\\pОни напоминают мне о сладких днях\\nмоей далёкой юности.\\pЖелаю тебе новых побед.\\nУ тебя есть преданный фанат!$",
        "SaffronCity_PokemonTrainerFanClub_Text_NeverSeenTrainerOfYourMagnificence": "Я объездил многие края.\\pНо никогда не видел ТРЕНЕРА\\nтакого уровня, как ты.\\pВерь в свои силы\\nи продолжай сражаться!\\pОбещай мне это,\\nмой юный кумир!$",
        "SaffronCity_PokemonTrainerFanClub_Text_HmmAndYouAre": "Хм...\\nА ты кто?\\pХотел вступить\\nв наш ФАН-КЛУБ?$",
        "SaffronCity_PokemonTrainerFanClub_Text_YouveStillAWaysToGo": "А, так ты тот самый\\n{PLAYER}, о котором все говорят.\\pВыглядишь как настоящий\\nпобедитель.\\pНо чтобы я признал тебя\\nвеликим ТРЕНЕРОМ ПОКЕМОНОВ...\\p...\\pТебе ещё есть куда расти!$",
        "SaffronCity_PokemonTrainerFanClub_Text_YoullBeTalkedAboutIfYouKeepWinning": "Все здесь - поклонники\\nТРЕНЕРОВ ПОКЕМОНОВ.\\pПосмотри, как они держатся в бою...\\nСамо воплощение крутости.\\pЕсли продолжишь побеждать,\\nможет, и о тебе здесь заговорят.$",
        "SaffronCity_PokemonTrainerFanClub_Text_WantToBeLikeYouOneDay": "Это {PLAYER}!\\nЭто {PLAYER}!\\pКогда-нибудь я хочу стать\\nкак {PLAYER}!$",
        "SaffronCity_PokemonTrainerFanClub_Text_EveryoneButMeStoppedBeingYourFan": "Все перестали быть фанатами\\n{PLAYER}...\\pЗато теперь {PLAYER}\\nцеликом мой!\\pУра! Вперёд!\\nМой единственный {PLAYER}!$",
        "SaffronCity_PokemonTrainerFanClub_Text_WantToBeLikeSabrina": "Знаешь что?\\nЯ хочу быть как САБРИНА!\\pХочу стать девочкой-экстрасенсом,\\nсовсем как она!$",
        "SaffronCity_PokemonTrainerFanClub_Text_WontStopBeingSabrinasFan": "Даже если останусь одна,\\nне перестану быть фанаткой САБРИНЫ.\\pМечтаю стать как САБРИНА:\\nмилой, но крутой.\\pХочу быть девочкой-экстрасенсом,\\nсовсем как она!$",
        "SaffronCity_PokemonTrainerFanClub_Text_CanIBecomeCoolTrainerOneDay": "Интересно, смогу ли я однажды\\nстать крутым ТРЕНЕРОМ?$",
        "SaffronCity_PokemonTrainerFanClub_Text_TheWayYouBattleIsCool": "Ого, ого!\\nКруто! Очень круто!\\p...Что?\\nНет, не ты.\\pТвой стиль боя.\\nВот он крутой.$",
        "SaffronCity_PokemonTrainerFanClub_Text_ImOnlyOneLeftOfYourFans": "Йо, {PLAYER}!\\pПохоже, из твоих фанатов\\nостался только я.\\pНо знаешь, мне даже нравится\\nбыть единственным. Меньше нервов.\\pНе сдавайся и продолжай!$",
        "SaffronCity_PokemonTrainerFanClub_Text_LoveWayTrainerTalks": "{STR_VAR_1} крут, да?\\nМне нравится, как он говорит.\\pОчень хочу однажды\\nвстретиться с ним лично.$",
        "SaffronCity_PokemonTrainerFanClub_Text_ImLoneTrainerFan": "Можешь поверить?\\nВсе стали твоими фанатами.\\pИ после всего этого только я\\nостался фанатом {STR_VAR_1}?\\pНу и ладно. Быть единственным\\nфанатом {STR_VAR_1} - это в моём стиле.$",
        "SaffronCity_PokemonTrainerFanClub_Text_AdoreWayYouBattle": "О боже!\\nЭто правда ты, {PLAYER}?\\pДолжна сказать: мне очень нравится,\\nкак ты сражаешься.\\pПродолжай в том же духе.\\nЯ буду твоей главной фанаткой!$",
        "SaffronCity_PokemonTrainerFanClub_Text_ImYourNumberOneFan": "О боже!\\nДа это же {PLAYER}!\\pКак обидно... Я поняла,\\nчто я твоя единственная фанатка!\\pНу ничего не поделать!\\nХотя бы поддержу тебя!\\pУра, ура, {PLAYER}!$",
        "SaffronCity_PokemonTrainerFanClub_Text_TrainerHasBeenOnFire": "В последнее время {STR_VAR_1}\\nпросто в ударе.\\pТо, как он сражается...\\nИменно это мне и нравится!$",
        "SaffronCity_PokemonTrainerFanClub_Text_EveryoneTalksAboutYou": "О, привет!\\nДа это же {PLAYER}!\\pВ последнее время все говорят\\nтолько о тебе.\\pМне даже одиноко, ведь я\\nпо-прежнему предпочитаю {STR_VAR_1}.$",
        "SaffronCity_PokemonTrainerFanClub_Text_YouReallyAreAmazing": "Невероятно!\\n{PLAYER}, ты и правда великолепен!\\pМожет, хватит просто смотреть,\\nи мне тоже стать ТРЕНЕРОМ?$",
        "SaffronCity_PokemonTrainerFanClub_Text_ImYourOnlyFan": "Я твоя единственная фанатка...\\nЭх... Одиноко...\\pМожет, постараешься сильнее,\\nчтобы остальные тебя заметили?$",
        "SaffronCity_PokemonTrainerFanClub_Text_WhyCantOthersSeeMastersDignity": "Мастер {STR_VAR_1} такой величественный...\\nОн прямо в моём вкусе.\\pПочему остальные не видят,\\nсколько в нём достоинства?$",
        "SaffronCity_PokemonTrainerFanClub_Text_BelieveInMasterWithAllMyHeart": "Я всем сердцем верю\\nв мастера {STR_VAR_1}.\\pДаже если только я одна\\nбуду верить в него.\\pМне всё равно не будет одиноко.\\pПока я думаю о мастере\\n{STR_VAR_1}.$",
        "SaffronCity_PokemonTrainerFanClub_Text_YourBattleStyleIsEducational": "Хия!\\pТвой стиль боя очень\\nпоучителен.\\pНадеюсь, ты продолжишь идти\\nк успеху. Хия!$",
        "SaffronCity_PokemonTrainerFanClub_Text_WontStopBeingYourFan": "Мастер сказал мне:\\nХватит смотреть - сражайся сам!\\pТак меня отчитали в ДОЖО...\\pНо это не помешает мне\\nоставаться твоим фанатом!\\pЯ просто не могу перестать!$",
        "SaffronCity_PokemonTrainerFanClub_Text_OnlyMasterHasMyRespect": "Хия! Я уважаю только одного\\nТРЕНЕРА.\\pЭто мой МАСТЕР\\nиз БОЕВОГО ДОЖО.\\pТебе тоже стоит стать\\nего фанатом! Хия!$",
        "SaffronCity_PokemonTrainerFanClub_Text_NeverBeFanOfAnyoneButMaster": "Хия! Я уважаю своего МАСТЕРА\\nиз БОЕВОГО ДОЖО.\\pЯ никогда не стану фанатом\\nникого другого!\\pДаже тайком выхожу из ДОЖО,\\nчтобы рассказывать о его величии.\\pХия!$"
    },
    Path("data/maps/CeladonCity_GameCorner_Frlg/scripts.inc"): {
        "CeladonCity_GameCorner_Text_CanExchangeCoinsNextDoor": "Добро пожаловать!\\pВ соседнем помещении можно обменять\\nМОНЕТЫ на отличные призы.$",
        "CeladonCity_GameCorner_Text_WelcomeBuySomeCoins": "Добро пожаловать в ИГРОВОЙ УГОЛОК\\nКОМАНДЫ R!\\pНужны игровые МОНЕТЫ?\\nХочешь купить?$",
        "CeladonCity_GameCorner_Text_ComePlaySometime": "Нет?\\nПриходи поиграть в другой раз!$",
        "CeladonCity_GameCorner_Text_SorryDontHaveCoinCase": "Ой, прости.\\nУ тебя нет КОШЕЛЬКА ДЛЯ МОНЕТ.$",
        "CeladonCity_GameCorner_Text_CoinCaseIsFull": "Ой!\\nТвой КОШЕЛЁК ДЛЯ МОНЕТ полон.$",
        "CeladonCity_GameCorner_Text_CantAffordCoins": "Тебе не хватает денег на МОНЕТЫ.$",
        "CeladonCity_GameCorner_Text_HereAreYourCoins": "Спасибо.\\nВот твои МОНЕТЫ!$",
        "CeladonCity_GameCorner_Text_RumoredTeamRocketRunsThisPlace": "Только никому не говори.\\pХодят слухи, что этим местом\\nуправляет КОМАНДА R.$",
        "CeladonCity_GameCorner_Text_ThinkMachinesHaveDifferentOdds": "Мне кажется, у разных автоматов\\nразные шансы на выигрыш.$",
        "CeladonCity_GameCorner_Text_DoYouWantToPlay": "Эй, малыш, хочешь сыграть?$",
        "CeladonCity_GameCorner_Text_Received10CoinsFromMan": "{PLAYER} получил 10 МОНЕТ\\nот мужчины.$",
        "CeladonCity_GameCorner_Text_DontNeedMyCoins": "Тебе мои МОНЕТЫ не нужны!$",
        "CeladonCity_GameCorner_Text_WinsComeAndGo": "Победы приходят и уходят.\\nЗдесь нет ничего наверняка.$",
        "CeladonCity_GameCorner_Text_WinOrLoseItsOnlyLuck": "Эти игровые автоматы...\\nПобеда или поражение - чистая удача.$",
        "CeladonCity_GameCorner_Text_GymGuyAdvice": "Эй!\\pУ тебя есть дела поважнее,\\nбудущий чемпион!\\pЛИДЕР ЗАЛА СЕЛАДОНА - ЭРИКА.\\pОна использует ПОКЕМОНОВ ТРАВЯНОГО типа\\nи живёт в гармонии с природой.\\pИз-за увлечения цветами она\\nможет казаться тихой...\\pНо недооценивать её нельзя!$",
        "CeladonCity_GameCorner_Text_RareMonsForCoins": "За МОНЕТЫ здесь дают\\nредких ПОКЕМОНОВ.\\pНо я никак не могу выиграть!$",
        "CeladonCity_GameCorner_Text_SoEasyToGetHooked": "Игры - страшная вещь!\\nТак легко втянуться!$",
        "CeladonCity_GameCorner_Text_WantSomeCoins": "Что такое?\\nХочешь немного МОНЕТ?$",
        "CeladonCity_GameCorner_Text_Received20CoinsFromNiceGuy": "{PLAYER} получил 20 МОНЕТ\\nот доброго мужчины.$",
        "CeladonCity_GameCorner_Text_YouHaveLotsOfCoins": "У тебя и так полно МОНЕТ!$",
        "CeladonCity_GameCorner_Text_NeedMoreCoinsForMonIWant": "Чёрт! Мне нужно ещё МОНЕТ,\\nчтобы получить нужного ПОКЕМОНА!$",
        "CeladonCity_GameCorner_Text_HereAreSomeCoinsShoo": "Эй, что? Ты мне мешаешь!\\nВот тебе МОНЕТЫ и уходи!$",
        "CeladonCity_GameCorner_Text_Received20CoinsFromMan": "{PLAYER} получил 20 МОНЕТ\\nот мужчины.$",
        "CeladonCity_GameCorner_Text_YouveGotPlentyCoins": "У тебя и своих МОНЕТ\\nпредостаточно!$",
        "CeladonCity_GameCorner_Text_WatchReelsClosely": "Секрет в том, чтобы внимательно\\nследить за барабанами.$",
        "CeladonCity_GameCorner_Text_GruntIntro": "Я охраняю этот плакат!\\nУходи, а не то пожалеешь!$",
        "CeladonCity_GameCorner_Text_GruntDefeat": "Чёрт!$",
        "CeladonCity_GameCorner_Text_GruntPostBattle": "УБЕЖИЩЕ КОМАНДЫ R могут\\nобнаружить!\\pНадо сообщить БОССУ!$",
        "CeladonCity_GameCorner_Text_SwitchBehindPosterPushIt": "Эй!\\pЗа плакатом переключатель?!\\nНажмём его!$",
        "CeladonCity_GameCorner_Text_CoinCaseIsRequired": "Нужен КОШЕЛЁК ДЛЯ МОНЕТ...$",
        "CeladonCity_GameCorner_Text_DontHaveCoinCase": "Ой!\\nУ тебя нет КОШЕЛЬКА ДЛЯ МОНЕТ!$",
        "CeladonCity_GameCorner_Text_SlotMachineWantToPlay": "Игровой автомат!\\nХочешь сыграть?$",
        "CeladonCity_GameCorner_Text_OutOfOrder": "НЕ РАБОТАЕТ\\nАвтомат сломан.$",
        "CeladonCity_GameCorner_Text_OutToLunch": "ОБЕДЕННЫЙ ПЕРЕРЫВ\\nАвтомат занят.$",
        "CeladonCity_GameCorner_Text_SomeonesKeys": "Чьи-то ключи!\\nЗа ними наверняка вернутся.$"
    }
}

def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")

def asm_quote(text: str) -> str:
    return text.replace('"', '\\"')

def replace_block(text: str, label: str, translated: str) -> str:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, got {len(matches)}")
    match = matches[0]
    next_label = LABEL_RE.search(text, match.end())
    end = next_label.start() if next_label else len(text)
    old = text[match.start():end]
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: block already contains Cyrillic; refusing to overwrite")
    block = f'{label}::\n\t.string "{asm_quote(translated)}"\n\n'
    return text[:match.start()] + block + text[end:]

def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    total = 0
    changed = []
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
    if total != 73:
        die(f"expected 73 translated blocks, got {total}")
    out = root / "build/qarro_ru_fanclub_gamecorner_v3_96_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"marker": MARKER, "translatedRuntimeBlocks": total, "changedFiles": changed, "pokemonMoveAbilityProperNamesStayEnglish": True, "ashBondTouched": False, "ashCapTouched": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} runtime blocks across Saffron Trainer Fan Club + Celadon Game Corner")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
