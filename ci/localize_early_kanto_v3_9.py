#!/usr/bin/env python3
"""Qarro v3.9 early-Kanto Russian runtime localization.

Translates only verified pinned FireRed blocks after the starter sequence:
Oak's Parcel/Pokedex continuation, Route 1, Viridian City/Mart, and Daisy's
early Town Map path. Exact source-block hashes keep the pass fail-closed.

Pokemon species names and move proper names remain English. Ash Bond / Ash Cap
are not referenced or changed.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_EARLY_KANTO_V3_9"
PATCHES = json.loads('{"data/maps/Route1_Frlg/scripts.inc":{"Route1_Text_WorkAtPokeMartTakeSample":["78f00249b4b15f4df03ad5355b323407b3a083e6a92db2bf54a571529f1e19b6",["Привет!\\\\n","Я работаю в ПОКЕ-МАРКЕТЕ.\\\\p","Это часть большой сети\\\\n","магазинов с разными товарами.\\\\p","Заходи в ВИРИДИАН-СИТИ.\\\\p","Держи бесплатный образец!\\\\n","Вот, бери!$"]],"Route1_Text_ComeSeeUsIfYouNeedPokeBalls":["648c54b822cc17f913c5e4a41612796419d4c8bf1dc97401ee966a6ec0980399",["Заходи к нам, если понадобятся\\\\n","ПОКЕБОЛЫ для ловли ПОКЕМОНОВ.$"]],"Route1_Text_PutPotionAway":["0fc7fff19201450fffef7a431131b401e8a233711385e4517c55fcfe25fe2dad",["{PLAYER} убрал ЗЕЛЬЕ в КАРМАН\\\\n","ПРЕДМЕТОВ СУМКИ.$"]],"Route1_Text_CanJumpFromLedges":["a72f21cd4411bdfbd5233377ed6566ea3f66cbc5b4a448c303f68a8894205280",["Видишь уступы вдоль дороги?\\\\p","Немного страшно, но с них\\\\n","можно спрыгивать.\\\\p","Так ты быстрее вернёшься\\\\n","в ПАЛЛЕТ-ТАУН.$"]],"Route1_Text_RouteSign":["f36b475fcdc576f76d187bd2b0d1d9b590eb4d859d634bdb9dce631a0ea707f2",["МАРШРУТ 1\\\\n","ПАЛЛЕТ-ТАУН - ВИРИДИАН-СИТИ$"]]},"data/maps/ViridianCity_Mart_Frlg/scripts.inc":{"ViridianCity_Mart_Text_YouCameFromPallet":["c4b0d153ca7962572938023b94829efe90e1872cd294cbdb9688684a5e268265",["Эй!\\\\n","Ты из ПАЛЛЕТ-ТАУНА?$"]],"ViridianCity_Mart_Text_TakeThisToProfOak":["3f5e6b38cc46ed29a2682f14aee96a0e75de15ed7a1fe128caf9a0310d93c4a6",["Ты ведь знаешь ПРОФ. ОУКА?\\\\p","Пришёл его заказ.\\\\n","Отнесёшь ему?$"]],"ViridianCity_Mart_Text_ReceivedOaksParcelFromClerk":["9abe00281a9585b1e4295e40d57e9e752a05af2a46eec3f21ea9bcfd38260470",["{PLAYER} получил ПОСЫЛКУ ОУКА\\\\n","от продавца ПОКЕ-МАРКЕТА.$"]],"ViridianCity_Mart_Text_SayHiToOakForMe":["a5dccc3b0a79f96439bd977a568d131b674b7f2a9146906239036eb193827bff",["Спасибо! И передавай привет\\\\n","ПРОФ. ОУКУ от меня.$"]],"ViridianCity_Mart_Text_ShopDoesGoodBusinessInAntidotes":["f0de6ea22a900c36030cf8657e9723271c6e4b530cf7abf9f4cea6c393d048b2",["Говорят, здесь отлично продаются\\\\n","ПРОТИВОЯДИЯ.$"]],"ViridianCity_Mart_Text_GotToBuySomePotions":["16acc171477d0af1f1cab8aafa7ee1a816cbce1e495de666943d7a625f845d99",["Нужно купить немного ЗЕЛИЙ.\\\\p","Никогда не знаешь, когда\\\\n","ПОКЕМОНУ понадобится лечение.$"]]},"data/maps/ViridianCity_Frlg/scripts.inc":{"ViridianCity_Text_CanCarryMonsAnywhere":["1414e51c77226a28e63b41f09ff069fbae21a8bf9ea6f3e60a0c72d8fc839a2a",["У тебя ПОКЕБОЛЫ на поясе!\\\\n","Значит, есть ПОКЕМОНЫ?\\\\p","Здорово, что ПОКЕМОНОВ можно\\\\n","брать с собой куда угодно.$"]],"ViridianCity_Text_GymClosedWonderWhoLeaderIs":["6d92f337070319c154492ba04a8bc1c7543da5c2c557d5e26555e2a5ccfa11be",["Этот ПОКЕМОН-ГИМ всегда закрыт.\\\\p","Интересно, кто здесь ЛИДЕР?$"]],"ViridianCity_Text_ViridiansGymLeaderReturned":["ae45ad08381551254b9bf0620c3a0998f4398636d9f4ad8d45ba32a1067ee5ca",["ЛИДЕР ВИРИДИАН-ГИМА вернулся!$"]],"ViridianCity_Text_WantToKnowAboutCaterpillarMons":["4c367070d739a565ab5f38a5af22a2fe79de9d4b32dadd7922548423bb73421d",["Хочешь узнать о двух видах\\\\n","ПОКЕМОНОВ-гусениц?$"]],"ViridianCity_Text_OhOkayThen":["1de0a43ec9d77ba1479c64d27f5abb0c51803e4745292df88ad92cc9f4af30d7",["А, ну ладно!$"]],"ViridianCity_Text_ExplainCaterpieWeedle":["d08bb1276dd0933330146ca590d771a906593949b7e1437de8011ccde24259a7",["CATERPIE не ядовит,\\\\n","а WEEDLE - ядовит.\\\\p","Береги ПОКЕМОНОВ от атаки\\\\n","WEEDLE - POISON STING.$"]],"ViridianCity_Text_GrandpaHasntHadCoffeeYet":["437283666052208ebac0bdf34762af8f6a23c84b250313a89728c18f108e45f5",["Ох, дедушка!\\\\n","Не будь таким грубым!\\\\p","Прости его.\\\\n","Он ещё не пил кофе.$"]],"ViridianCity_Text_GoShoppingInPewterOccasionally":["bf495d23a2ea0e0f8b26c868a4e16c083b870eddf620b2019c3a1cc0e4d95bbf",["Иногда я хожу за покупками\\\\n","в ПЬЮТЕР-СИТИ.\\\\p","Туда ведёт извилистая тропа\\\\n","через ВИРИДИАНСКИЙ ЛЕС.$"]],"ViridianCity_Text_ThisIsPrivateProperty":["18d5d6e9ba8dedeafeb9708845fb6c75ff26d017eaa9f51d300c37ac0f41da7e",["Я запрещаю тебе здесь проходить!\\\\p","Это частная территория!$"]],"ViridianCity_Text_ShowYouHowToCatchMons":["1aee9be4377ee651a24f9bb1d3f3ce9606299a04c52a0a1f716638a2f8d18f3c",["Вот теперь я выпил кофе\\\\n","и снова полон сил!\\\\p","Хм?\\\\n","Что это за красная штука?\\\\p","А, ты заполняешь ПОКЕДЕКС.\\\\p","Тогда дам тебе совет.\\\\p","Поймаешь ПОКЕМОНА - ПОКЕДЕКС\\\\n","сам обновит его данные.\\\\p","Что? Не знаешь, как ловить\\\\n","ПОКЕМОНОВ?\\\\p","Тогда я лучше покажу тебе!$"]],"ViridianCity_Text_ThatWasEducationalTakeThis":["3f848e15ce4b13230c2ad181f1f85685538fa4f814a9c355b85b3c10c7b8813f",["Вот так! Полезный урок, правда?\\\\p","И ещё вот это возьми.$"]],"ViridianCity_Text_WatchThatToLearnBasics":["148375975514211c41572dec7496079ebd68564803d86919652106418b9a7040",["Если что-то непонятно,\\\\n","посмотри это.\\\\p","Там объясняются основы\\\\n","работы ТРЕНЕРА ПОКЕМОНОВ.$"]],"ViridianCity_Text_WeakenMonsFirstToCatch":["05a4bffaada5252d5482ba67eb1b3230d0d7e4fd9d3c73ff01ef7a186d4dd5bb",["Вот теперь я выпил кофе\\\\n","и снова полон сил!\\\\p","Но кофе вышел слишком крепким.\\\\n","Голова разболелась...\\\\p","Кстати, заполняешь ПОКЕДЕКС?\\\\p","Сначала ослабь ПОКЕМОНА,\\\\n","а уже потом лови его.$"]],"ViridianCity_Text_HowsTeachyTVHelping":["7af8f3a644e79b039b161e0e321e4df47106f27cd7a0ac9ec410a62e0e341dbe",["Вот теперь я выпил кофе\\\\n","и снова полон сил!\\\\p","Но кофе вышел слишком крепким.\\\\n","Голова разболелась...\\\\p","Кстати, помогает тебе моё\\\\n","ОБУЧАЮЩЕЕ ТВ?$"]],"ViridianCity_Text_MyGrandsonOnTheShow":["e30077ae7ceb688c3913364ad173c104020cf1e118af0f783708b99553b46d99",["Ха-ха-ха!\\\\n","На экране мой внук!\\\\p","Раз он там учит,\\\\n","ты точно чему-нибудь научишься.$"]],"ViridianCity_Text_TooBusyForTeachyTV":["9321d346b2323f91c1b407c8f6e7e550547cc983f4cb71a8edc63c220980fd1b",["Хм... Ты так занят, что даже\\\\n","нет времени на ОБУЧАЮЩЕЕ ТВ?\\\\p","Время - деньги. Не трать\\\\n","ни то ни другое зря.$"]],"ViridianCity_Text_CitySign":["c95cf51f0ddc0babe02be1adf9ecd8ed622044374eb214f15783e9d883a07aac",["ВИРИДИАН-СИТИ\\\\n","Вечно зелёный рай$"]],"ViridianCity_Text_CatchMonsForEasierBattles":["523ec8719489755c2c9714f5f34488e5877de30fc75df831647436897179b76c",["СОВЕТЫ ТРЕНЕРА\\\\p","Лови ПОКЕМОНОВ и пополняй\\\\n","свою коллекцию.\\\\p","Чем их больше, тем проще\\\\n","вести сражения.$"]],"ViridianCity_Text_MovesLimitedByPP":["8b02e39ae3b95687b43125ef8b02f54514617a93832137610383378f518474b1",["СОВЕТЫ ТРЕНЕРА\\\\p","У атак ПОКЕМОНОВ есть запас\\\\n","очков PP.\\\\p","Чтобы восстановить PP, отдохни\\\\n","в ПОКЕМОН-ЦЕНТРЕ.$"]],"ViridianCity_Text_GymSign":["20d5552c25c90c111d9e28c5f872a34059f73858a8e33aea5f1e750051b8274c",["ПОКЕМОН-ГИМ ВИРИДИАН-СИТИ$"]],"ViridianCity_Text_GymDoorsAreLocked":["62d99ad7a3b02158280cbaa089e1c044c8d5b4badd261fc6e3d4c730fd0936ae",["Двери ВИРИДИАН-ГИМА заперты...$"]]},"data/maps/PalletTown_RivalsHouse_Frlg/scripts.inc":{"PalletTown_RivalsHouse_Text_HiBrothersAtLab":["caf5171d59888459c757b9fb544ec4cfba6d06a8965bcc6193f298aec7bfe6dc",["ДЕЙЗИ: Привет, {PLAYER}!\\\\p","Мой брат {RIVAL} сейчас\\\\n","в лаборатории дедушки.$"]],"PalletTown_RivalsHouse_Text_HeardYouBattledRival":["5972049f518c5459456bb0e6fc47cc3520301d3d87ec336b28081826c19f9889",["ДЕЙЗИ: {PLAYER}, я слышала,\\\\n","ты сражался с {RIVAL}.\\\\p","Жаль, я этого не видела!$"]],"PalletTown_RivalsHouse_Text_ErrandForGrandpaThisWillHelp":["028ea090528038912d81e721f1fefc18bd8c38c4264fc5d9750f84644e0c500a",["Дедушка дал тебе поручение?\\\\p","Ну и лентяй же он.\\\\n","Вот, это тебе поможет.$"]],"PalletTown_RivalsHouse_Text_ReceivedTownMapFromDaisy":["2b57ec5b2020e9bb988bc125c9637aff6382129bc7b63cac8840782d49efc4be",["{PLAYER} получил КАРТУ КАНТО\\\\n","от ДЕЙЗИ.$"]],"PalletTown_RivalsHouse_Text_DontHaveSpaceForThis":["9eef568d0d31fef0d8defff64d338f741607eadd71c76621d5e79c71c338c546",["В СУМКЕ нет места\\\\n","для этого предмета.$"]],"PalletTown_RivalsHouse_Text_ExplainTownMap":["472a165e4f0119e6fc432bfd3fee2c013868ba41ca74164f6899ca9626406d05",["На КАРТЕ КАНТО видно,\\\\n","где ты находишься,\\\\l","и как называются места.$"]],"PalletTown_RivalsHouse_Text_PleaseGiveMonsRest":["e81df081ab3164eb9947e8671af41a1a4d769984a98167900f8e613920b92ed7",["ДЕЙЗИ: ПОКЕМОНЫ, как и люди,\\\\n","тоже живые существа.\\\\p","Если они устали,\\\\n","дай им отдохнуть.$"]],"PalletTown_RivalsHouse_Text_ItsBigMapOfKanto":["0fd72d7da8e29aa6d8a145a8a37a405a799ae61bae70ecd9bac500a9a4562a80",["Это большая карта региона КАНТО.\\\\n","Она бы пригодилась!$"]],"PalletTown_RivalsHouse_Text_ShelvesCrammedFullOfBooks":["14d7457fc84e87ed389b388fa7fe6dc26c6f7279e7fff1237393aa88ed12da90",["Полки забиты книгами\\\\n","о ПОКЕМОНАХ.$"]],"PalletTown_RivalsHouse_Text_LovelyAndSweetClefairy":["80c8214f13b44f16eaa9df8c8352085ab272d2e261ccac1a2b8d2bf31c1d7cbd",["«Милый и очаровательный\\\\n","CLEFAIRY»$"]]},"data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc":{"PalletTown_ProfessorOaksLab_Text_RivalGramps":["47add9737b23bfa0733695318cc32ddfdca08861cc590db71a482aeb0d5989b1",["{RIVAL}: Дедушка!$"]],"PalletTown_ProfessorOaksLab_Text_RivalWhatDidYouCallMeFor":["37d895a609134c30db7d535d2f8a350341c7b5367579e8447fd8602f71d35827",["{RIVAL}: Чуть не забыл!\\\\n","Зачем ты меня звал?$"]],"PalletTown_ProfessorOaksLab_Text_RivalLeaveItToMeGramps":["72839f6b77e3f78fd927b17ef0b18a3df1a5d66368f9af8e831c1357afa6ecdd",["{RIVAL}: Хорошо, дедушка!\\\\n","Я всё сделаю!$"]],"PalletTown_ProfessorOaksLab_Text_RivalTellSisNotToGiveYouMap":["2912725ff58e14b4b4b841ce1c625b3d5842bd431364f6f6a3a1715f8eb6f17f",["{PLAYER}, без тебя обойдёмся.\\\\p","Возьму КАРТУ КАНТО у сестры.\\\\p","И скажу ей не давать карту\\\\n","тебе, {PLAYER}! Ха-ха!\\\\p","Даже не приходи ко мне!$"]],"PalletTown_ProfessorOaksLab_Text_OakHaveSomethingForMe":["81fab35e7b2a42c67fb64a76dbdde8900b5c158fb3d162228ee448deace5c462",["ОУК: О, {PLAYER}!\\\\n","Как мой старый ПОКЕМОН?\\\\p","Похоже, он всё сильнее\\\\n","привязывается к тебе.\\\\p","У тебя талант ТРЕНЕРА.\\\\p","Что это?\\\\n","У тебя что-то для меня?$"]],"PalletTown_ProfessorOaksLab_Text_DeliveredOaksParcel":["bf21c62d678fb7c585d52adfdae5b426fa4465f64f1d6c47b95e7d684d669e1e",["{PLAYER} доставил ПОСЫЛКУ ОУКА.$"]],"PalletTown_ProfessorOaksLab_Text_OakCustomBallIOrdered":["b6a2a6af012d95ebc7bb931bd0247b8dad6e7f3e744bd75f8f53087f93334841",["А!\\\\n","Это мой особый ПОКЕБОЛ!\\\\p","Я как раз ждал этот заказ.\\\\n","Спасибо!$"]],"PalletTown_ProfessorOaksLab_Text_OakHaveRequestForYouTwo":["f7e8d8c308ee20f9899f8f7f3a1e6c5dc11f7a5485484c3dad29b7b5a46c8a63",["ОУК: Ах да!\\\\n","У меня просьба к вам обоим.$"]],"PalletTown_ProfessorOaksLab_Text_OakPokedexOnDesk":["0eeaa83b7073b957ff3ceb408031ac95765f3489b5fe6f12263b1dbd1559eb18",["На столе моё изобретение -\\\\n","ПОКЕДЕКС!\\\\p","Он сам записывает данные\\\\n","об увиденных и пойманных\\\\p","ПОКЕМОНАХ.\\\\p","Это высокотехнологичная\\\\n","энциклопедия!$"]],"PalletTown_ProfessorOaksLab_Text_OakTakeTheseWithYou":["3a383fb3ea4a2b3308933d13c33a7a0a414e5e3a8c580380084d7dcf1e775398",["ОУК: {PLAYER} и {RIVAL}.\\\\n","Возьмите их с собой.$"]],"PalletTown_ProfessorOaksLab_Text_ReceivedPokedexFromOak":["5e153a858b87a0c6758a6780bf3a2243a2aa38d9691f344d158b309b684926ea",["{PLAYER} получил ПОКЕДЕКС\\\\n","от ПРОФ. ОУКА.$"]],"PalletTown_ProfessorOaksLab_Text_OakCatchMonsForDataTakeThese":["e5e01dc7f1640ff08e008b6cc3402488e7b4b47192399c95180d124258fcc646",["ОУК: Одних встреч недостаточно,\\\\n","чтобы получить все данные.\\\\p","Нужно ловить ПОКЕМОНОВ.\\\\p","Поэтому вот инструменты\\\\n","для их поимки.$"]],"PalletTown_ProfessorOaksLab_Text_ReceivedFivePokeBalls":["bf0af6df8cec65bb0c58810ee454f3540be886438d9e214793ce6514366b42d3",["{PLAYER} получил 20 ПОКЕБОЛОВ.$"]],"PalletTown_ProfessorOaksLab_Text_OakExplainCatching":["8e746df11a8864b40822a4cc0b08d6b1aa4e1b519e761cd53fd92b70d7cd4ae8",["Встретил дикого ПОКЕМОНА -\\\\n","можешь попробовать поймать.\\\\p","Брось в него ПОКЕБОЛ.\\\\p","Но это не всегда сработает.\\\\p","Здоровый ПОКЕМОН может\\\\n","вырваться. Нужна удача!$"]],"PalletTown_ProfessorOaksLab_Text_OakCompleteMonGuideWasMyDream":["b5453111d264c126c407df56aed29b4defee1489ec861e4338c1d908f4bb340b",["Создать полный справочник\\\\n","всех ПОКЕМОНОВ мира...\\\\p","Это была моя мечта!\\\\p","Но я уже слишком стар.\\\\n","Сам я не справлюсь.\\\\p","Поэтому прошу вас двоих\\\\n","осуществить мою мечту.\\\\p","В путь!\\\\p","Это великое дело в истории\\\\n","ПОКЕМОНОВ!$"]],"PalletTown_ProfessorOaksLab_Text_OakMonsAroundWorldWait":["bfa7ae7da729987bc71d5c8fc13e69f0c1d0b2e7f71159b0eb53c7d05199a262",["ПОКЕМОНЫ всего мира ждут\\\\n","тебя, {PLAYER}!$"]],"PalletTown_ProfessorOaksLab_Text_OakComeSeeMeSometime":["5061233963ca972dca8ee09ac4aecb9589476e0b197ed274093050532aecd323",["ОУК: Заходи ко мне иногда.\\\\p","Мне интересно, как продвигается\\\\n","твой ПОКЕДЕКС.$"]],"PalletTown_ProfessorOaksLab_Text_BlankEncyclopedia":["bfee3de273b9858d83ac1faa7bd7babff965b85047e847461fec12a129530551",["Похоже на энциклопедию,\\\\n","но страницы пока пусты.$"]],"PalletTown_ProfessorOaksLab_Text_PressStartToOpenMenu":["1c8c4a98db3f2db3827f7fc4e6d2489d144df2f4b123e34f56925293728eb29a",["Нажми START, чтобы открыть МЕНЮ!$"]],"PalletTown_ProfessorOaksLab_Text_SaveOptionInMenu":["e0894d401ecca7e7f332f31bb7a20d47084de02b7743156ff353d2953199dfdf",["В МЕНЮ есть пункт СОХРАНИТЬ.\\\\n","Пользуйся им регулярно.$"]],"PalletTown_ProfessorOaksLab_Text_AllMonTypesHaveStrongAndWeakPoints":["287d695056c1c42287f95ea5fddc0d06d66ed6d8916d3610c45d600e68b29687",["У всех типов ПОКЕМОНОВ есть\\\\n","сильные и слабые стороны.$"]],"PalletTown_ProfessorOaksLab_Text_StudyAsOaksAide":["930ff9d859dd160927e548c9da37a519404c27fab899b4b8e3d71915f57ce6b8",["Я изучаю ПОКЕМОНОВ\\\\n","как ПОМОЩНИК ПРОФ. ОУКА.$"]]}}')


def render_block(label: str, lines: list[str]) -> str:
    return label + "::\n" + "\n".join(f'\t.string "{line}"' for line in lines)


def extract_block(text: str, label: str) -> tuple[int, int, str]:
    token = label + "::\n"
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"missing text label: {label}")
    end = text.find("\n\n", start)
    if end < 0:
        end = len(text)
    return start, end, text[start:end]


def patch_file(root: Path, rel: str, blocks: dict) -> int:
    path = root / rel
    if not path.is_file():
        raise RuntimeError(f"missing pinned FireRed source: {path}")
    text = path.read_text(encoding="utf-8")
    changed = 0
    for label, (old_sha, russian) in blocks.items():
        start, end, current = extract_block(text, label)
        new = render_block(label, russian)
        current_sha = hashlib.sha256(current.encode("utf-8")).hexdigest()
        if current_sha == old_sha:
            text = text[:start] + new + text[end:]
            changed += 1
            print(f"[ru-early-kanto] {label}: localized")
        elif current == new:
            print(f"[ru-early-kanto] {label}: already localized")
        else:
            raise RuntimeError(f"{rel}::{label} fail-closed SHA mismatch: {current_sha}")
    path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    changed = 0
    per_file = {}
    for rel, blocks in PATCHES.items():
        count = patch_file(root, rel, blocks)
        changed += count
        per_file[rel] = {"selectedBlocks": len(blocks), "changedThisRun": count}
    audit = {
        "marker": MARKER,
        "selectedBlocksLocalized": sum(len(v) for v in PATCHES.values()),
        "blocksChangedThisRun": changed,
        "files": per_file,
        "route1Localized": True,
        "viridianCityLocalized": True,
        "viridianMartParcelLoopLocalized": True,
        "oakParcelAndPokedexContinuationLocalized": True,
        "daisyTownMapPathLocalized": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_early_kanto_v3_9_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: {audit['selectedBlocksLocalized']} verified blocks localized across {len(PATCHES)} files; names/Ash protected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
