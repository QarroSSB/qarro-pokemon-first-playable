#!/usr/bin/env python3
"""Qarro v3.24 Route 25 Bill Sea Cottage Russian runtime localization.

Translates the complete verified pinned Sea Cottage runtime text surface used by
Bill's mandatory progression and its local optional responses. Pokemon species /
move / ability proper names remain English. Ash Bond / Ash Cap are not
referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_ROUTE25_BILL_V3_24"
REL = Path("data/maps/Route25_SeaCottage_Frlg/scripts.inc")

PATCHES = {
    "Route25_SeaCottage_Text_ImBillHelpMeOutPal": (
        "Route25_SeaCottage_Text_ImBillHelpMeOutPal::\n"
        "\t.string \"Hiya! I'm a POKéMON…\\n\"\n"
        "\t.string \"…No I'm not!\\p\"\n"
        "\t.string \"Call me BILL!\\n\"\n"
        "\t.string \"I'm a true-blue POKéMANIAC!\\p\"\n"
        "\t.string \"Hey!\\n\"\n"
        "\t.string \"What's with that skeptical look?\\p\"\n"
        "\t.string \"I'm not joshing you, pal.\\p\"\n"
        "\t.string \"I screwed up an experiment and got\\n\"\n"
        "\t.string \"combined with a POKéMON!\\p\"\n"
        "\t.string \"So, how about it?\\n\"\n"
        "\t.string \"Help me out here!$\"\n",
        "Route25_SeaCottage_Text_ImBillHelpMeOutPal::\n"
        "\t.string \"Привет! Я ПОКЕМОН…\\n\"\n"
        "\t.string \"…Да нет же!\\p\"\n"
        "\t.string \"Зови меня БИЛЛ!\\n\"\n"
        "\t.string \"Я настоящий ПОКЕМАНЬЯК!\\p\"\n"
        "\t.string \"Эй!\\n\"\n"
        "\t.string \"Что за недоверчивый взгляд?\\p\"\n"
        "\t.string \"Я не шучу, приятель.\\p\"\n"
        "\t.string \"Эксперимент пошёл не так, и я\\n\"\n"
        "\t.string \"слился с ПОКЕМОНОМ!\\p\"\n"
        "\t.string \"Ну так что?\\n\"\n"
        "\t.string \"Поможешь мне?$\"\n",
    ),
    "Route25_SeaCottage_Text_ImBillHelpMeOutLady": (
        "Route25_SeaCottage_Text_ImBillHelpMeOutLady::\n"
        "\t.string \"Hiya! I'm a POKéMON…\\n\"\n"
        "\t.string \"…No I'm not!\\p\"\n"
        "\t.string \"Call me BILL!\\n\"\n"
        "\t.string \"I'm a true-blue POKéMANIAC!\\p\"\n"
        "\t.string \"Hey!\\n\"\n"
        "\t.string \"What's with that skeptical look?\\p\"\n"
        "\t.string \"I'm not joshing you, lady.\\p\"\n"
        "\t.string \"I screwed up an experiment and got\\n\"\n"
        "\t.string \"combined with a POKéMON!\\p\"\n"
        "\t.string \"So, how about it?\\n\"\n"
        "\t.string \"Help me out here!$\"\n",
        "Route25_SeaCottage_Text_ImBillHelpMeOutLady::\n"
        "\t.string \"Привет! Я ПОКЕМОН…\\n\"\n"
        "\t.string \"…Да нет же!\\p\"\n"
        "\t.string \"Зови меня БИЛЛ!\\n\"\n"
        "\t.string \"Я настоящий ПОКЕМАНЬЯК!\\p\"\n"
        "\t.string \"Эй!\\n\"\n"
        "\t.string \"Что за недоверчивый взгляд?\\p\"\n"
        "\t.string \"Я не шучу, красавица.\\p\"\n"
        "\t.string \"Эксперимент пошёл не так, и я\\n\"\n"
        "\t.string \"слился с ПОКЕМОНОМ!\\p\"\n"
        "\t.string \"Ну так что?\\n\"\n"
        "\t.string \"Поможешь мне?$\"\n",
    ),
    "Route25_SeaCottage_Text_RunCellSeparationOnPC": (
        "Route25_SeaCottage_Text_RunCellSeparationOnPC::\n"
        "\t.string \"Wait till I get inside the\\n\"\n"
        "\t.string \"TELEPORTER.\\p\"\n"
        "\t.string \"When I do, go to my PC and run\\n\"\n"
        "\t.string \"the Cell Separation System.$\"\n",
        "Route25_SeaCottage_Text_RunCellSeparationOnPC::\n"
        "\t.string \"Подожди, пока я войду в\\n\"\n"
        "\t.string \"ТЕЛЕПОРТЕР.\\p\"\n"
        "\t.string \"Потом подойди к моему ПК и\\n\"\n"
        "\t.string \"запусти разделение клеток.$\"\n",
    ),
    "Route25_SeaCottage_Text_NoPleaseChief": (
        "Route25_SeaCottage_Text_NoPleaseChief::\n"
        "\t.string \"No!?\\n\"\n"
        "\t.string \"Now don't be so cold!\\p\"\n"
        "\t.string \"Come on, you gotta help a guy in\\n\"\n"
        "\t.string \"deep, deep trouble!\\p\"\n"
        "\t.string \"What do you say, chief?\\n\"\n"
        "\t.string \"Please?\\l\"\n"
        "\t.string \"Okay?\\l\"\n"
        "\t.string \"All right!$\"\n",
        "Route25_SeaCottage_Text_NoPleaseChief::\n"
        "\t.string \"Нет!?\\n\"\n"
        "\t.string \"Ну не будь таким холодным!\\p\"\n"
        "\t.string \"Мне правда очень нужна твоя\\n\"\n"
        "\t.string \"помощь!\\p\"\n"
        "\t.string \"Ну что, дружище?\\n\"\n"
        "\t.string \"Пожалуйста?\\l\"\n"
        "\t.string \"Ладно?\\l\"\n"
        "\t.string \"Отлично!$\"\n",
    ),
    "Route25_SeaCottage_Text_NoPleaseBeautiful": (
        "Route25_SeaCottage_Text_NoPleaseBeautiful::\n"
        "\t.string \"No!?\\n\"\n"
        "\t.string \"Now don't be so cold!\\p\"\n"
        "\t.string \"Come on, you gotta help a guy in\\n\"\n"
        "\t.string \"deep, deep trouble!\\p\"\n"
        "\t.string \"What do you say, beautiful?\\n\"\n"
        "\t.string \"Please?\\l\"\n"
        "\t.string \"Okay?\\l\"\n"
        "\t.string \"All right!$\"\n",
        "Route25_SeaCottage_Text_NoPleaseBeautiful::\n"
        "\t.string \"Нет!?\\n\"\n"
        "\t.string \"Ну не будь такой холодной!\\p\"\n"
        "\t.string \"Мне правда очень нужна твоя\\n\"\n"
        "\t.string \"помощь!\\p\"\n"
        "\t.string \"Ну что, красавица?\\n\"\n"
        "\t.string \"Пожалуйста?\\l\"\n"
        "\t.string \"Ладно?\\l\"\n"
        "\t.string \"Отлично!$\"\n",
    ),
    "Route25_SeaCottage_Text_ThanksBudTakeThis": (
        "Route25_SeaCottage_Text_ThanksBudTakeThis::\n"
        "\t.string \"BILL: Yeehah!\\n\"\n"
        "\t.string \"Thanks, bud! I owe you one!\\p\"\n"
        "\t.string \"So, did you come to see my\\n\"\n"
        "\t.string \"POKéMON collection?\\p\"\n"
        "\t.string \"You didn't?\\n\"\n"
        "\t.string \"That's a bummer.\\p\"\n"
        "\t.string \"I've got to thank you…\\n\"\n"
        "\t.string \"Oh, here, maybe this'll do.$\"\n",
        "Route25_SeaCottage_Text_ThanksBudTakeThis::\n"
        "\t.string \"БИЛЛ: Ура!\\n\"\n"
        "\t.string \"Спасибо, дружище! Я твой должник!\\p\"\n"
        "\t.string \"Ты пришёл посмотреть мою\\n\"\n"
        "\t.string \"коллекцию ПОКЕМОНОВ?\\p\"\n"
        "\t.string \"Нет?\\n\"\n"
        "\t.string \"Вот досада.\\p\"\n"
        "\t.string \"Но я должен тебя отблагодарить…\\n\"\n"
        "\t.string \"Вот, пожалуй, это подойдёт.$\"\n",
    ),
    "Route25_SeaCottage_Text_ThanksLadyTakeThis": (
        "Route25_SeaCottage_Text_ThanksLadyTakeThis::\n"
        "\t.string \"BILL: Yeehah!\\n\"\n"
        "\t.string \"Thanks, lady! I owe you one!\\p\"\n"
        "\t.string \"So, did you come to see my\\n\"\n"
        "\t.string \"POKéMON collection?\\p\"\n"
        "\t.string \"You didn't?\\n\"\n"
        "\t.string \"That's a bummer.\\p\"\n"
        "\t.string \"I've got to thank you…\\n\"\n"
        "\t.string \"Oh, here, maybe this'll do.$\"\n",
        "Route25_SeaCottage_Text_ThanksLadyTakeThis::\n"
        "\t.string \"БИЛЛ: Ура!\\n\"\n"
        "\t.string \"Спасибо! Я твой должник!\\p\"\n"
        "\t.string \"Ты пришла посмотреть мою\\n\"\n"
        "\t.string \"коллекцию ПОКЕМОНОВ?\\p\"\n"
        "\t.string \"Нет?\\n\"\n"
        "\t.string \"Вот досада.\\p\"\n"
        "\t.string \"Но я должен тебя отблагодарить…\\n\"\n"
        "\t.string \"Вот, пожалуй, это подойдёт.$\"\n",
    ),
    "Route25_SeaCottage_Text_ReceivedSSTicketFromBill": (
        "Route25_SeaCottage_Text_ReceivedSSTicketFromBill::\n"
        "\t.string \"{PLAYER} received an S.S. TICKET\\n\"\n"
        "\t.string \"from BILL.$\"\n",
        "Route25_SeaCottage_Text_ReceivedSSTicketFromBill::\n"
        "\t.string \"{PLAYER} получил БИЛЕТ S.S. ANNE\\n\"\n"
        "\t.string \"от БИЛЛА.$\"\n",
    ),
    "Route25_SeaCottage_Text_YouveGotTooMuchStuff": (
        "Route25_SeaCottage_Text_YouveGotTooMuchStuff::\n"
        "\t.string \"You've got too much stuff!$\"\n",
        "Route25_SeaCottage_Text_YouveGotTooMuchStuff::\n"
        "\t.string \"В СУМКЕ нет свободного места!$\"\n",
    ),
    "Route25_SeaCottage_Text_SSAnnePartyYouGoInstead": (
        "Route25_SeaCottage_Text_SSAnnePartyYouGoInstead::\n"
        "\t.string \"That cruise ship S.S. ANNE is in\\n\"\n"
        "\t.string \"VERMILION CITY.\\p\"\n"
        "\t.string \"I hear there are lots of TRAINERS\\n\"\n"
        "\t.string \"on board, too.\\p\"\n"
        "\t.string \"They invited me to their party, but\\n\"\n"
        "\t.string \"I can't stand fancy do's.\\p\"\n"
        "\t.string \"Why don't you go instead of me?\\n\"\n"
        "\t.string \"Go on and have a good time.$\"\n",
        "Route25_SeaCottage_Text_SSAnnePartyYouGoInstead::\n"
        "\t.string \"Круизный лайнер S.S. ANNE стоит в\\n\"\n"
        "\t.string \"VERMILION CITY.\\p\"\n"
        "\t.string \"Говорят, на борту полно ТРЕНЕРОВ.\\p\"\n"
        "\t.string \"Меня звали на их вечеринку, но\\n\"\n"
        "\t.string \"я не люблю светские приёмы.\\p\"\n"
        "\t.string \"Почему бы тебе не пойти вместо меня?\\n\"\n"
        "\t.string \"Отдохни как следует.$\"\n",
    ),
    "Route25_SeaCottage_Text_CheckOutRareMonsOnPC": (
        "Route25_SeaCottage_Text_CheckOutRareMonsOnPC::\n"
        "\t.string \"BILL: Feel like checking out some\\n\"\n"
        "\t.string \"of my rare POKéMON on my PC?\\p\"\n"
        "\t.string \"Go on, check out my PC.$\"\n",
        "Route25_SeaCottage_Text_CheckOutRareMonsOnPC::\n"
        "\t.string \"БИЛЛ: Хочешь увидеть моих редких\\n\"\n"
        "\t.string \"ПОКЕМОНОВ на ПК?\\p\"\n"
        "\t.string \"Давай, посмотри мой ПК.$\"\n",
    ),
    "Route25_SeaCottage_Text_TeleporterIsDisplayed": (
        "Route25_SeaCottage_Text_TeleporterIsDisplayed::\n"
        "\t.string \"TELEPORTER is displayed on the PC\\n\"\n"
        "\t.string \"monitor.$\"\n",
        "Route25_SeaCottage_Text_TeleporterIsDisplayed::\n"
        "\t.string \"На мониторе ПК показан\\n\"\n"
        "\t.string \"ТЕЛЕПОРТЕР.$\"\n",
    ),
    "Route25_SeaCottage_Text_InitiatedTeleportersCellSeparator": (
        "Route25_SeaCottage_Text_InitiatedTeleportersCellSeparator::\n"
        "\t.string \"{PLAYER} initiated the TELEPORTER's\\n\"\n"
        "\t.string \"Cell Separator.$\"\n",
        "Route25_SeaCottage_Text_InitiatedTeleportersCellSeparator::\n"
        "\t.string \"{PLAYER} запустил разделитель клеток\\n\"\n"
        "\t.string \"ТЕЛЕПОРТЕРА.$\"\n",
    ),
    "Route25_SeaCottage_Text_BillsFavoriteMonList": (
        "Route25_SeaCottage_Text_BillsFavoriteMonList::\n"
        "\t.string \"BILL's favorite POKéMON list!$\"\n",
        "Route25_SeaCottage_Text_BillsFavoriteMonList::\n"
        "\t.string \"Любимые ПОКЕМОНЫ БИЛЛА!$\"\n",
    ),
    "Route25_SeaCottage_Text_SeeWhichMon": (
        "Route25_SeaCottage_Text_SeeWhichMon::\n"
        "\t.string \"Which POKéMON do you want to see?$\"\n",
        "Route25_SeaCottage_Text_SeeWhichMon::\n"
        "\t.string \"Какого ПОКЕМОНА хочешь увидеть?$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_route25_bill_v3_24.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied = []

    for label, (pinned, ru) in PATCHES.items():
        variants = [pinned]
        normalized = pinned.replace("é", "e").replace("É", "E")
        if normalized != pinned:
            variants.append(normalized)
        hits = [(variant, text.count(variant)) for variant in variants]
        total = sum(count for _, count in hits)
        if total != 1:
            raise SystemExit(f"{MARKER}: {label}: expected exactly one pinned/normalized anchor, found {total}")
        source = next(variant for variant, count in hits if count == 1)
        text = text.replace(source, ru, 1)
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_route25_bill_v3_24_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names may remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Route 25 Bill runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
