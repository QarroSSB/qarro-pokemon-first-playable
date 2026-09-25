#!/usr/bin/env python3
"""Qarro v3.45 mandatory Sevii entry Russian runtime localization.

Translates only the verified pinned continuous first-trip path from Bill's
post-Blaine invitation on Cinnabar through arrival on One Island and the forced
first Celio meeting that grants the Meteorite / Tri-Pass. Optional island NPCs
and later Ruby/Sapphire postgame text are intentionally untouched. Pokemon
species / move / ability proper names remain English. Ash Bond / Ash Cap are
not referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_SEVII_ENTRY_V3_45"

PATCHES = {
    Path("data/maps/CinnabarIsland_Frlg/scripts.inc"): {
        "CinnabarIsland_Text_HeyIfItIsntPlayer": (
            "CinnabarIsland_Text_HeyIfItIsntPlayer::\n"
            "\t.string \"Huh?\\n\"\n"
            "\t.string \"Hey, if it isn't {PLAYER}!$\"\n",
            "CinnabarIsland_Text_HeyIfItIsntPlayer::\n"
            "\t.string \"А?\\n\"\n"
            "\t.string \"Эй, да это же {PLAYER}!$\"\n",
        ),
        "CinnabarIsland_Text_ComeWithMeToOneIsland": (
            "CinnabarIsland_Text_ComeWithMeToOneIsland::\n"
            "\t.string \"Look, it's me, BILL.\\n\"\n"
            "\t.string \"Long time no see!\\p\"\n"
            "\t.string \"I hope you're still using my\\n\"\n"
            "\t.string \"PC system.\\p\"\n"
            "\t.string \"Well, listen, since we met up here,\\n\"\n"
            "\t.string \"how about spending time with me?\\p\"\n"
            "\t.string \"There's this little island in the far\\n\"\n"
            "\t.string \"south called ONE ISLAND.\\p\"\n"
            "\t.string \"A friend invited me, so I'm on my\\n\"\n"
            "\t.string \"way out there.\\p\"\n"
            "\t.string \"How about it?\\n\"\n"
            "\t.string \"Do you feel like coming with me?$\"\n",
            "CinnabarIsland_Text_ComeWithMeToOneIsland::\n"
            "\t.string \"Это я, BILL.\\n\"\n"
            "\t.string \"Давно не виделись!\\p\"\n"
            "\t.string \"Надеюсь, ты всё ещё пользуешься\\n\"\n"
            "\t.string \"моей системой PC.\\p\"\n"
            "\t.string \"Раз уж мы встретились здесь,\\n\"\n"
            "\t.string \"может, составишь мне компанию?\\p\"\n"
            "\t.string \"Далеко на юге есть небольшой\\n\"\n"
            "\t.string \"остров - ONE ISLAND.\\p\"\n"
            "\t.string \"Меня пригласил друг, и я как раз\\n\"\n"
            "\t.string \"собираюсь туда.\\p\"\n"
            "\t.string \"Ну как?\\n\"\n"
            "\t.string \"Поедешь со мной?$\"\n",
        ),
        "CinnabarIsland_Text_AllRightLetsGo": (
            "CinnabarIsland_Text_AllRightLetsGo::\n"
            "\t.string \"All right, then.\\n\"\n"
            "\t.string \"Let's go!$\"\n",
            "CinnabarIsland_Text_AllRightLetsGo::\n"
            "\t.string \"Отлично.\\n\"\n"
            "\t.string \"Тогда в путь!$\"\n",
        ),
        "CinnabarIsland_Text_IllBeWaitingInPokeCenter": (
            "CinnabarIsland_Text_IllBeWaitingInPokeCenter::\n"
            "\t.string \"What, are you too busy?\\p\"\n"
            "\t.string \"Well, all right.\\n\"\n"
            "\t.string \"The boat hasn't arrived yet anyway.\\p\"\n"
            "\t.string \"I'll be waiting at the POKéMON\\n\"\n"
            "\t.string \"CENTER over there.\\p\"\n"
            "\t.string \"Come see me when you're done with\\n\"\n"
            "\t.string \"your business here.$\"\n",
            "CinnabarIsland_Text_IllBeWaitingInPokeCenter::\n"
            "\t.string \"Что, ты пока занят?\\p\"\n"
            "\t.string \"Ладно.\\n\"\n"
            "\t.string \"Корабль всё равно ещё не прибыл.\\p\"\n"
            "\t.string \"Я подожду тебя в ЦЕНТРЕ\\n\"\n"
            "\t.string \"ПОКЕМОНОВ неподалёку.\\p\"\n"
            "\t.string \"Загляни ко мне, когда закончишь\\n\"\n"
            "\t.string \"свои дела здесь.$\"\n",
        ),
        "CinnabarIsland_Text_MyPalsBoatArrived": (
            "CinnabarIsland_Text_MyPalsBoatArrived::\n"
            "\t.string \"Looks like my pal's boat arrived,\\n\"\n"
            "\t.string \"too.\\p\"\n"
            "\t.string \"He sent it specially here to\\n\"\n"
            "\t.string \"CINNABAR to pick me up.$\"\n",
            "CinnabarIsland_Text_MyPalsBoatArrived::\n"
            "\t.string \"Похоже, корабль моего друга\\n\"\n"
            "\t.string \"уже прибыл.\\p\"\n"
            "\t.string \"Он специально прислал его\\n\"\n"
            "\t.string \"на CINNABAR за мной.$\"\n",
        ),
    },
    Path("data/maps/OneIsland_Frlg/scripts.inc"): {
        "OneIsland_Text_BillLetsGoSeeCelio": (
            "OneIsland_Text_BillLetsGoSeeCelio::\n"
            "\t.string \"BILL: Here we are!\\n\"\n"
            "\t.string \"This is ONE ISLAND.\\p\"\n"
            "\t.string \"There are several islands around\\n\"\n"
            "\t.string \"here, and this is one of them.\\p\"\n"
            "\t.string \"My friend CELIO sent the boat to\\n\"\n"
            "\t.string \"fetch me here.\\p\"\n"
            "\t.string \"He's in charge of the island's PC\\n\"\n"
            "\t.string \"network by his lonesome.\\p\"\n"
            "\t.string \"…Why am I telling you this now?\\n\"\n"
            "\t.string \"Let's just go see CELIO!$\"\n",
            "OneIsland_Text_BillLetsGoSeeCelio::\n"
            "\t.string \"BILL: Мы на месте!\\n\"\n"
            "\t.string \"Это ONE ISLAND.\\p\"\n"
            "\t.string \"Здесь несколько островов,\\n\"\n"
            "\t.string \"и это один из них.\\p\"\n"
            "\t.string \"Мой друг CELIO прислал за мной\\n\"\n"
            "\t.string \"этот корабль.\\p\"\n"
            "\t.string \"Он один отвечает за сеть PC\\n\"\n"
            "\t.string \"на острове.\\p\"\n"
            "\t.string \"...Зачем я рассказываю это сейчас?\\n\"\n"
            "\t.string \"Пойдём лучше к CELIO!$\"\n",
        ),
    },
    Path("data/maps/OneIsland_PokemonCenter_1F_Frlg/scripts.inc"): {
        "OneIsland_PokemonCenter_1F_Text_BillHeyThereCelio": (
            "OneIsland_PokemonCenter_1F_Text_BillHeyThereCelio::\n"
            "\t.string \"BILL: Hey, there!\\n\"\n"
            "\t.string \"CELIO!$\"\n",
            "OneIsland_PokemonCenter_1F_Text_BillHeyThereCelio::\n"
            "\t.string \"BILL: Привет!\\n\"\n"
            "\t.string \"CELIO!$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_CelioCantBelieveYouCameOut": (
            "OneIsland_PokemonCenter_1F_Text_CelioCantBelieveYouCameOut::\n"
            "\t.string \"CELIO: BILL!\\n\"\n"
            "\t.string \"I can't believe you came out here.$\"\n",
            "OneIsland_PokemonCenter_1F_Text_CelioCantBelieveYouCameOut::\n"
            "\t.string \"CELIO: BILL!\\n\"\n"
            "\t.string \"Не верится, что ты приехал!$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_BillHowsYourResearchComing": (
            "OneIsland_PokemonCenter_1F_Text_BillHowsYourResearchComing::\n"
            "\t.string \"BILL: Well, absolutely!\\n\"\n"
            "\t.string \"How's your research coming along?\\p\"\n"
            "\t.string \"…Oh, wait a sec.$\"\n",
            "OneIsland_PokemonCenter_1F_Text_BillHowsYourResearchComing::\n"
            "\t.string \"BILL: Конечно!\\n\"\n"
            "\t.string \"Как продвигаются исследования?\\p\"\n"
            "\t.string \"...А, погоди.$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_ThisIsMyBuddyCelio": (
            "OneIsland_PokemonCenter_1F_Text_ThisIsMyBuddyCelio::\n"
            "\t.string \"{PLAYER}, this is my buddy CELIO.\\n\"\n"
            "\t.string \"He's one dedicated PC MANIAC!$\"\n",
            "OneIsland_PokemonCenter_1F_Text_ThisIsMyBuddyCelio::\n"
            "\t.string \"{PLAYER}, это мой друг CELIO.\\n\"\n"
            "\t.string \"Он настоящий фанат PC!$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_PlayerIsRisingPokemonChamp": (
            "OneIsland_PokemonCenter_1F_Text_PlayerIsRisingPokemonChamp::\n"
            "\t.string \"CELIO, this is {PLAYER}, a rising\\n\"\n"
            "\t.string \"contender as the POKéMON CHAMP!$\"\n",
            "OneIsland_PokemonCenter_1F_Text_PlayerIsRisingPokemonChamp::\n"
            "\t.string \"CELIO, это {PLAYER}, будущий\\n\"\n"
            "\t.string \"претендент на титул ЧЕМПИОНА!$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_PlayerIsReigningPokemonChamp": (
            "OneIsland_PokemonCenter_1F_Text_PlayerIsReigningPokemonChamp::\n"
            "\t.string \"CELIO, this is {PLAYER}, the\\n\"\n"
            "\t.string \"reigning POKéMON CHAMP!$\"\n",
            "OneIsland_PokemonCenter_1F_Text_PlayerIsReigningPokemonChamp::\n"
            "\t.string \"CELIO, это {PLAYER}, нынешний\\n\"\n"
            "\t.string \"ЧЕМПИОН ПОКЕМОНОВ!$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_CelioThatsReallyImpressive": (
            "OneIsland_PokemonCenter_1F_Text_CelioThatsReallyImpressive::\n"
            "\t.string \"CELIO: That's really impressive.\\p\"\n"
            "\t.string \"I hate to say it, but I have zero\\n\"\n"
            "\t.string \"aptitude for battling.\\p\"\n"
            "\t.string \"Anyways, I'm glad to meet you.$\"\n",
            "OneIsland_PokemonCenter_1F_Text_CelioThatsReallyImpressive::\n"
            "\t.string \"CELIO: Впечатляет.\\p\"\n"
            "\t.string \"Увы, но к битвам у меня\\n\"\n"
            "\t.string \"совсем нет таланта.\\p\"\n"
            "\t.string \"В любом случае, рад знакомству.$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_BillBringMeUpToSpeed": (
            "OneIsland_PokemonCenter_1F_Text_BillBringMeUpToSpeed::\n"
            "\t.string \"BILL: So, bring me up to speed.\\n\"\n"
            "\t.string \"How's your machine running?$\"\n",
            "OneIsland_PokemonCenter_1F_Text_BillBringMeUpToSpeed::\n"
            "\t.string \"BILL: Ну, рассказывай.\\n\"\n"
            "\t.string \"Как работает твоя машина?$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_CelioPCsCantLinkWithYours": (
            "OneIsland_PokemonCenter_1F_Text_CelioPCsCantLinkWithYours::\n"
            "\t.string \"CELIO: It's running fine, but we're\\n\"\n"
            "\t.string \"too remote out here.\\p\"\n"
            "\t.string \"The PCs on this island just can't\\n\"\n"
            "\t.string \"link with your PC, BILL.$\"\n",
            "OneIsland_PokemonCenter_1F_Text_CelioPCsCantLinkWithYours::\n"
            "\t.string \"CELIO: Работает хорошо, но мы\\n\"\n"
            "\t.string \"слишком далеко отсюда.\\p\"\n"
            "\t.string \"PC острова не могут связаться\\n\"\n"
            "\t.string \"с твоим PC, BILL.$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_BillLetMeHelpYou": (
            "OneIsland_PokemonCenter_1F_Text_BillLetMeHelpYou::\n"
            "\t.string \"BILL: Oh, yeah?\\n\"\n"
            "\t.string \"Okay, let me take a look-see.\\p\"\n"
            "\t.string \"…Hang on here…\\n\"\n"
            "\t.string \"I think we can make it work.\\l\"\n"
            "\t.string \"Let me help you, okay?$\"\n",
            "OneIsland_PokemonCenter_1F_Text_BillLetMeHelpYou::\n"
            "\t.string \"BILL: Вот как?\\n\"\n"
            "\t.string \"Дай-ка взглянуть.\\p\"\n"
            "\t.string \"...Секунду...\\n\"\n"
            "\t.string \"Думаю, это можно исправить.\\l\"\n"
            "\t.string \"Давай я помогу.$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_CanYouDeliverThisMeteoritePlayer": (
            "OneIsland_PokemonCenter_1F_Text_CanYouDeliverThisMeteoritePlayer::\n"
            "\t.string \"{PLAYER}, can I get you to wait for\\n\"\n"
            "\t.string \"me just a bit?\\p\"\n"
            "\t.string \"…Actually, can I get you to do\\n\"\n"
            "\t.string \"me a favor?\\p\"\n"
            "\t.string \"The island next to this one's\\n\"\n"
            "\t.string \"called TWO ISLAND.\\p\"\n"
            "\t.string \"There's a guy there that runs\\n\"\n"
            "\t.string \"a GAME CORNER.\\p\"\n"
            "\t.string \"He has this thing for rare rocks\\n\"\n"
            "\t.string \"and gems.\\p\"\n"
            "\t.string \"We keep in touch, being fellow\\n\"\n"
            "\t.string \"maniacs.\\p\"\n"
            "\t.string \"So, can I get you to deliver this\\n\"\n"
            "\t.string \"METEORITE to him?$\"\n",
            "OneIsland_PokemonCenter_1F_Text_CanYouDeliverThisMeteoritePlayer::\n"
            "\t.string \"{PLAYER}, подождёшь меня\\n\"\n"
            "\t.string \"немного?\\p\"\n"
            "\t.string \"...Вообще-то, можешь оказать\\n\"\n"
            "\t.string \"мне услугу?\\p\"\n"
            "\t.string \"Соседний остров называется\\n\"\n"
            "\t.string \"TWO ISLAND.\\p\"\n"
            "\t.string \"Там один парень держит\\n\"\n"
            "\t.string \"GAME CORNER.\\p\"\n"
            "\t.string \"Он обожает редкие камни\\n\"\n"
            "\t.string \"и самоцветы.\\p\"\n"
            "\t.string \"Мы с ним часто общаемся.\\p\"\n"
            "\t.string \"Передашь ему этот\\n\"\n"
            "\t.string \"МЕТЕОРИТ?$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_AcceptedMeteoriteFromBill": (
            "OneIsland_PokemonCenter_1F_Text_AcceptedMeteoriteFromBill::\n"
            "\t.string \"{PLAYER} accepted the METEORITE\\n\"\n"
            "\t.string \"from BILL.$\"\n",
            "OneIsland_PokemonCenter_1F_Text_AcceptedMeteoriteFromBill::\n"
            "\t.string \"{PLAYER} получил МЕТЕОРИТ\\n\"\n"
            "\t.string \"от BILL.$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_CelioPleaseTakeThis": (
            "OneIsland_PokemonCenter_1F_Text_CelioPleaseTakeThis::\n"
            "\t.string \"CELIO: {PLAYER}, if you are going\\n\"\n"
            "\t.string \"to TWO ISLAND, please take this.$\"\n",
            "OneIsland_PokemonCenter_1F_Text_CelioPleaseTakeThis::\n"
            "\t.string \"CELIO: {PLAYER}, если идёшь\\n\"\n"
            "\t.string \"на TWO ISLAND, возьми это.$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_PassLetsYouTravelBetweenIslands": (
            "OneIsland_PokemonCenter_1F_Text_PassLetsYouTravelBetweenIslands::\n"
            "\t.string \"It's a PASS for the ferry service\\n\"\n"
            "\t.string \"serving the local islands.\\p\"\n"
            "\t.string \"It will let you travel between the\\n\"\n"
            "\t.string \"ISLANDS ONE, TWO, and THREE.\\p\"\n"
            "\t.string \"Oh, you should have this, too.$\"\n",
            "OneIsland_PokemonCenter_1F_Text_PassLetsYouTravelBetweenIslands::\n"
            "\t.string \"Это ПРОПУСК на местный паром.\\p\"\n"
            "\t.string \"С ним можно плавать между\\n\"\n"
            "\t.string \"ONE, TWO и THREE ISLAND.\\p\"\n"
            "\t.string \"И вот это тоже возьми.$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_ReceivedExtraPageForTownMap": (
            "OneIsland_PokemonCenter_1F_Text_ReceivedExtraPageForTownMap::\n"
            "\t.string \"{PLAYER} received an extra page\\n\"\n"
            "\t.string \"for the TOWN MAP!$\"\n",
            "OneIsland_PokemonCenter_1F_Text_ReceivedExtraPageForTownMap::\n"
            "\t.string \"{PLAYER} получил новую страницу\\n\"\n"
            "\t.string \"для КАРТЫ МИРА!$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_ReceivedTownMap": (
            "OneIsland_PokemonCenter_1F_Text_ReceivedTownMap::\n"
            "\t.string \"{PLAYER} received\\n\"\n"
            "\t.string \"a TOWN MAP!$\"\n",
            "OneIsland_PokemonCenter_1F_Text_ReceivedTownMap::\n"
            "\t.string \"{PLAYER} получил\\n\"\n"
            "\t.string \"КАРТУ МИРА!$\"\n",
        ),
        "OneIsland_PokemonCenter_1F_Text_BillCatchYouLater": (
            "OneIsland_PokemonCenter_1F_Text_BillCatchYouLater::\n"
            "\t.string \"BILL: I'll catch you later!\\n\"\n"
            "\t.string \"Say hi to the guy for me!$\"\n",
            "OneIsland_PokemonCenter_1F_Text_BillCatchYouLater::\n"
            "\t.string \"BILL: Увидимся позже!\\n\"\n"
            "\t.string \"Передавай ему привет!$\"\n",
        ),
    },
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_sevii_entry_v3_45.py <upstream-root>")
    root = Path(sys.argv[1])
    applied = []
    touched = []

    for rel, patches in PATCHES.items():
        path = root / rel
        text = path.read_text(encoding="utf-8")
        file_applied = []
        for label, (pinned, ru) in patches.items():
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
            file_applied.append(label)
        path.write_text(text, encoding="utf-8")
        touched.append({"file": str(rel), "translatedBlocks": file_applied})

    out = root / "build" / "qarro_ru_sevii_entry_v3_45_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "scope": "Cinnabar Bill invitation -> One Island arrival -> forced first Celio meeting",
        "files": touched,
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Sevii entry runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
