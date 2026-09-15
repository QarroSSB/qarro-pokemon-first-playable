#!/usr/bin/env python3
"""Qarro v3.94 bulk Russian localization: Route 10 + Rock Tunnel + Viridian Forest.

Translates all English-only FireRed runtime _Text_ blocks reported by the
current v3.21 surface audit in these four untouched Kanto map scripts:
21 + 22 + 24 + 23 = 90 blocks.
Pokemon species, Move and Ability proper names remain English by project canon.
Ash Bond / Ash Cap and gameplay logic are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTE10_ROCKTUNNEL_VIRIDIANFOREST_V3_94"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    Path("data/maps/Route10_Frlg/scripts.inc"): {
        "Route10_Text_MarkIntro": "Ого, ты добрался аж сюда?\\nМожет, ты тоже ПОКЕМАНЬЯК?\\lХочешь увидеть мою коллекцию?$",
        "Route10_Text_MarkDefeat": "Хмф.\\nЯ не злюсь!$",
        "Route10_Text_MarkPostBattle": "Дома у меня есть ещё более редкие ПОКЕМОНЫ!$",
        "Route10_Text_ClarkIntro": "Ха-ха-ха-ха-ха!$",
        "Route10_Text_ClarkDefeat": "Ха-ха!\\nЯ не смеюсь!\\lЭто аллергия! Апчхи!$",
        "Route10_Text_ClarkPostBattle": "Апчхи!\\nАпчхи!\\lШмыг! Фыр!$",
        "Route10_Text_HermanIntro": "Привет, малыш!\\nХочешь посмотреть на моих ПОКЕМОНОВ?$",
        "Route10_Text_HermanDefeat": "О нет!\\nМои ПОКЕМОНЫ!$",
        "Route10_Text_HermanPostBattle": "Ты мне не нравишься.\\nНе люблю тех, кто сильнее меня!$",
        "Route10_Text_HeidiIntro": "Я уже несколько раз ходила\\nв ЗАЛ ПОКЕМОНОВ.\\pНо всегда проигрываю.$",
        "Route10_Text_HeidiDefeat": "Ох!\\nИ это после всех моих тренировок!$",
        "Route10_Text_HeidiPostBattle": "Я заметила неподалёку\\nнескольких ПОКЕМАНЬЯКОВ.\\pПредставляешь? Они здесь,\\nв горах?$",
        "Route10_Text_TrentIntro": "Ах!\\nКакой вкусный горный воздух!$",
        "Route10_Text_TrentDefeat": "Голова сразу прояснилась!$",
        "Route10_Text_TrentPostBattle": "Я объелся горным воздухом!$",
        "Route10_Text_CarolIntro": "Мне немного дурно.\\nДавно я не ходила в походы.$",
        "Route10_Text_CarolDefeat": "Я слишком устала.\\nБыла не готова.$",
        "Route10_Text_CarolPostBattle": "Горные ПОКЕМОНЫ здесь\\nтакие крепыши...\\pВот бы встретить розового ПОКЕМОНА\\nс цветочным узором!$",
        "Route10_Text_RockTunnelDetourToLavender": "СКАЛЬНЫЙ ТОННЕЛЬ\\nОбходной путь в ЛАВАНДЕР$",
        "Route10_Text_RockTunnel": "СКАЛЬНЫЙ ТОННЕЛЬ$",
        "Route10_Text_PowerPlant": "ЭЛЕКТРОСТАНЦИЯ$",
    },
    Path("data/maps/RockTunnel_1F_Frlg/scripts.inc"): {
        "RockTunnel_1F_Text_LennyIntro": "Этот тоннель тянется очень далеко, малыш!$",
        "RockTunnel_1F_Text_LennyDefeat": "Эх!\\nТы победил!$",
        "RockTunnel_1F_Text_LennyPostBattle": "Берегись ONIX.\\nОни появляются нечасто.\\pОсобенно сильные могут\\nкак следует тебя сдавить!$",
        "RockTunnel_1F_Text_OliverIntro": "Хм.\\nКажется, я здесь заблудился...$",
        "RockTunnel_1F_Text_OliverDefeat": "Полегче!\\nЧто я вообще делаю?\\lГде здесь выход?$",
        "RockTunnel_1F_Text_OliverPostBattle": "Спящий ПОКЕМОН на МАРШРУТЕ 12\\nзаставил меня идти в обход.$",
        "RockTunnel_1F_Text_LucasIntro": "Чужакам вроде тебя стоит проявлять\\nко мне уважение!$",
        "RockTunnel_1F_Text_LucasDefeat": "Сдаюсь!$",
        "RockTunnel_1F_Text_LucasPostBattle": "С твоими способностями можно смело ходить в горы!$",
        "RockTunnel_1F_Text_AshtonIntro": "Бой ПОКЕМОНОВ!\\nНа старт, внимание, вперёд!$",
        "RockTunnel_1F_Text_AshtonDefeat": "Игра окончена!$",
        "RockTunnel_1F_Text_AshtonPostBattle": "Ну и ладно, по дороге поймаю ZUBAT!$",
        "RockTunnel_1F_Text_LeahIntro": "Ай!\\pТолько не вздумай делать ничего странного\\nв темноте!$",
        "RockTunnel_1F_Text_LeahDefeat": "Было слишком темно...$",
        "RockTunnel_1F_Text_LeahPostBattle": "Я видела в этом тоннеле MACHOP.$",
        "RockTunnel_1F_Text_DanaIntro": "Я забралась так далеко в поисках\\nдиких ПОКЕМОНОВ.$",
        "RockTunnel_1F_Text_DanaDefeat": "У меня закончились ПОКЕМОНЫ!$",
        "RockTunnel_1F_Text_DanaPostBattle": "Ты выглядел таким милым и безобидным.\\nКак же я ошиблась!$",
        "RockTunnel_1F_Text_ArianaIntro": "У тебя есть ПОКЕМОНЫ!\\nНачинаем!$",
        "RockTunnel_1F_Text_ArianaDefeat": "Ты сражаешься всерьёз!$",
        "RockTunnel_1F_Text_ArianaPostBattle": "Фух!\\nЯ вся вспотела.$",
        "RockTunnel_1F_Text_RouteSign": "СКАЛЬНЫЙ ТОННЕЛЬ\\nЦЕРУЛИН - ЛАВАНДЕР$",
    },
    Path("data/maps/RockTunnel_B1F_Frlg/scripts.inc"): {
        "RockTunnel_B1F_Text_SofiaIntro": "Знаешь, как не заблудиться\\nв горах?\\pМожно сгибать веточки,\\nоставляя метки на пути.$",
        "RockTunnel_B1F_Text_SofiaDefeat": "Ох!\\nЯ старалась изо всех сил!$",
        "RockTunnel_B1F_Text_SofiaPostBattle": "Я хочу домой!$",
        "RockTunnel_B1F_Text_DudleyIntro": "Ха-ха-ха!\\nСправишься с моей силой?$",
        "RockTunnel_B1F_Text_DudleyDefeat": "Упс!\\nПересилил меня!$",
        "RockTunnel_B1F_Text_DudleyPostBattle": "Я полагаюсь на силу, потому что\\nтерпеть не могу думать.$",
        "RockTunnel_B1F_Text_CooperIntro": "У тебя есть ПОКЕДЕКС?\\nЯ тоже такой хочу.$",
        "RockTunnel_B1F_Text_CooperDefeat": "Чёрт!\\nКак же я завидую!$",
        "RockTunnel_B1F_Text_CooperPostBattle": "Когда закончишь ПОКЕДЕКС,\\nможно мне его забрать?$",
        "RockTunnel_B1F_Text_SteveIntro": "Эм... Ты знаешь про косплей\\nПОКЕМОНОВ?$",
        "RockTunnel_B1F_Text_SteveDefeat": "Ну, вот и всё.$",
        "RockTunnel_B1F_Text_StevePostBattle": "Косплей ПОКЕМОНОВ - это когда\\nради забавы наряжаются ПОКЕМОНАМИ.\\pОсобенно популярен CLEFAIRY.$",
        "RockTunnel_B1F_Text_AllenIntro": "Приёмы моих ПОКЕМОНОВ заставят\\nтебя плакать!$",
        "RockTunnel_B1F_Text_AllenDefeat": "Сдаюсь!\\nТы техничнее меня!$",
        "RockTunnel_B1F_Text_AllenPostBattle": "В горах часто встречаются\\nПОКЕМОНЫ КАМЕННОГО типа.$",
        "RockTunnel_B1F_Text_MarthaIntro": "Я редко сюда прихожу,\\nно с тобой сражусь.$",
        "RockTunnel_B1F_Text_MarthaDefeat": "Ой!\\nЯ проиграла!$",
        "RockTunnel_B1F_Text_MarthaPostBattle": "Мне нравятся маленькие ПОКЕМОНЫ.\\nБольшие слишком страшные!$",
        "RockTunnel_B1F_Text_EricIntro": "Покажи всё, на что способен!$",
        "RockTunnel_B1F_Text_EricDefeat": "Выстрелил и промахнулся!$",
        "RockTunnel_B1F_Text_EricPostBattle": "Я натренирую ПОКЕМОНОВ так,\\nчтобы победить твоих, малыш.$",
        "RockTunnel_B1F_Text_WinstonIntro": "Дома я рисую иллюстрации\\nс ПОКЕМОНАМИ.$",
        "RockTunnel_B1F_Text_WinstonDefeat": "Фух...\\nЯ вымотался...$",
        "RockTunnel_B1F_Text_WinstonPostBattle": "Я художник, а не боец.\\nПойду домой рисовать.$",
    },
    Path("data/maps/ViridianForest_Frlg/scripts.inc"): {
        "ViridianForest_Text_FriendsItchingToBattle": "Я пришёл сюда с друзьями ловить\\nПОКЕМОНОВ-ЖУКОВ!\\pИм всем не терпится устроить\\nбой ПОКЕМОНОВ!$",
        "ViridianForest_Text_RickIntro": "Эй! У тебя есть ПОКЕМОНЫ!\\nДавай!\\lСразимся ими!$",
        "ViridianForest_Text_RickDefeat": "Нет!\\nCATERPIE не справился!$",
        "ViridianForest_Text_RickPostBattle": "Тсс! Ты распугаешь жуков.\\nВ другой раз, ладно?$",
        "ViridianForest_Text_DougIntro": "Йо!\\nЕсли ты ТРЕНЕР ПОКЕМОНОВ,\\lот боя не отвертишься!$",
        "ViridianForest_Text_DougDefeat": "Что?\\nУ меня кончились ПОКЕМОНЫ!$",
        "ViridianForest_Text_DougPostBattle": "Вот отстой! Пойду поймаю\\nкого-нибудь посильнее!$",
        "ViridianForest_Text_SammyIntro": "Эй, погоди!\\nКуда так спешишь?$",
        "ViridianForest_Text_SammyDefeat": "Сдаюсь!\\nУ тебя здорово получается!$",
        "ViridianForest_Text_SammyPostBattle": "Иногда на земле можно найти\\nразные вещи.\\pЯ ищу то, что потерял.\\nПоможешь мне?$",
        "ViridianForest_Text_AnthonyIntro": "Я маленький, но не вздумай\\nмне поддаваться!$",
        "ViridianForest_Text_AnthonyDefeat": "Эх.\\nВсё пошло наперекосяк.$",
        "ViridianForest_Text_AnthonyPostBattle": "Я потерял часть карманных денег...$",
        "ViridianForest_Text_CharlieIntro": "Ты знал, что ПОКЕМОНЫ эволюционируют?$",
        "ViridianForest_Text_CharlieDefeat": "Ой!\\nЯ проиграл!$",
        "ViridianForest_Text_CharliePostBattle": "ПОКЕМОНЫ-ЖУКИ быстро эволюционируют.\\nС ними очень весело!$",
        "ViridianForest_Text_RanOutOfPokeBalls": "Я бросал ПОКЕБОЛЫ, чтобы ловить\\nПОКЕМОНОВ, и они закончились.\\pВот почему ПОКЕБОЛОВ\\nмного не бывает.$",
        "ViridianForest_Text_AvoidGrassyAreasWhenWeak": "СОВЕТЫ ТРЕНЕРА\\pЕсли твои ПОКЕМОНЫ ослабли и ты\\nхочешь избежать боёв, держись подальше\\lот высокой травы!$",
        "ViridianForest_Text_UseAntidoteForPoison": "При отравлении используй АНТИДОТ!\\nКупи его в МАГАЗИНЕ ПОКЕМОНОВ!$",
        "ViridianForest_Text_ContactOakViaPCToRatePokedex": "СОВЕТЫ ТРЕНЕРА\\pСвяжись с ПРОФ. ОУКОМ через ПК,\\nчтобы он оценил твой ПОКЕДЕКС!$",
        "ViridianForest_Text_CantCatchOwnedMons": "СОВЕТЫ ТРЕНЕРА\\pНельзя поймать ПОКЕМОНА,\\nкоторый принадлежит другому.\\pБросай ПОКЕБОЛЫ только в диких\\nПОКЕМОНОВ, чтобы поймать их!$",
        "ViridianForest_Text_WeakenMonsBeforeCapture": "СОВЕТЫ ТРЕНЕРА\\pОслабь ПОКЕМОНА перед попыткой\\nпоймать его!\\pЕсли он здоров, то может вырваться!$",
        "ViridianForest_Text_LeavingViridianForest": "ВЫХОД ИЗ ВИРИДИАНСКОГО ЛЕСА\\nВПЕРЕДИ ПЬЮТЕР$",
    },
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

    if total != 90:
        die(f"expected 90 translated blocks, got {total}")

    out = root / "build/qarro_ru_route10_rocktunnel_viridianforest_v3_94_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "translatedRuntimeBlocks": total,
        "changedFiles": changed,
        "pokemonMoveAbilityProperNamesStayEnglish": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[{MARKER}] PASS: translated {total} runtime blocks across Route 10 + Rock Tunnel + Viridian Forest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
