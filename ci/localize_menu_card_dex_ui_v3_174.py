#!/usr/bin/env python3
"""Qarro v3.174: main-menu names + Trainer Card + Pokédex UI."""
from __future__ import annotations
import json,sys
from pathlib import Path
MARKER="QARRO_RU_MENU_CARD_DEX_UI_V3_174"

NAMES={
"STU":"СТЮ","MILTON":"МИЛТОН","TOM":"ТОМ","KENNY":"КЕННИ","REID":"РИД","JUDE":"ДЖУД",
"JAXSON":"ДЖЕКСОН","EASTON":"ИСТОН","WALKER":"УОКЕР","TERU":"ТЕРУ","JOHNNY":"ДЖОННИ",
"BRETT":"БРЕТТ","SETH":"СЕТ","TERRY":"ТЕРРИ","CASEY":"КЕЙСИ","DARREN":"ДАРРЕН",
"LANDON":"ЛЭНДОН","COLLIN":"КОЛЛИН","STANLEY":"СТЭНЛИ","QUINCY":"КУИНСИ",
"KIMMY":"КИММИ","TIARA":"ТИАРА","BELLA":"БЕЛЛА","JAYLA":"ДЖЕЙЛА","ALLIE":"ЭЛЛИ",
"LIANNA":"ЛИАННА","SARA":"САРА","MONICA":"МОНИКА","CAMILA":"КАМИЛА","AUBREE":"ОБРИ",
"RUTHIE":"РУТИ","HAZEL":"ХЕЙЗЕЛ","NADINE":"НАДИН","TANJA":"ТАНЯ","YASMIN":"ЯСМИН",
"NICOLA":"НИКОЛА","LILLIE":"ЛИЛЛИ","TERRA":"ТЕРРА","LUCY":"ЛЮСИ","HALIE":"ХЕЙЛИ",
}

CARD={
"It's a POKeMON PRINTER!\\p":"Это POKeMON PRINTER!\\p",
"It can put a print of your POKeMON\\n":"Он напечатает твоего POKeMON\\n",
"on the back of your TRAINER CARD.\\p":"на обратной стороне TRAINER CARD.\\p",
"It costs only ¥50.\\n":"Это стоит всего ¥50.\\n",
"Would you like to try it?$":"Хочешь попробовать?$",
"You don't have enough money.$":"У тебя недостаточно денег.$",
"Please choose the print type.$":"Выбери тип печати.$",
"A big smile for the photo, please!\\n":"Улыбнись для фотографии!\\n",
"Three… Two… One…\\p":"Три… Два… Один…\\p",
"Flash!$":"Вспышка!$",
"Your POKeMON print is ready!\\n":"Печать POKeMON готова!\\n",
"Check your TRAINER CARD.$":"Проверь TRAINER CARD.$",
"Giggle…\\n":"Хи-хи…\\n",
"I collected a ton of STICKERS.\\l":"Я собрал целую кучу STICKERS.\\l",
"I wish I could show them off…$":"Вот бы показать их кому-нибудь…$",
"Oh, excellent!\\n":"О, отлично!\\n",
"You've come to the right place!\\p":"Ты пришел куда надо!\\p",
"Look, look! See? See?\\n":"Смотри! Видишь?\\n",
"These are my STICKERS!\\l":"Это мои STICKERS!\\l",
"Look how many I got!\\p":"Посмотри, сколько их!\\p",
"I bet you want some.\\n":"Наверняка тоже хочешь.\\n",
"I bet you do!\\p":"Точно хочешь!\\p",
"I'll give a STICKER if you can tell\\n":"Я дам STICKER, если расскажешь\\n",
"me something awesome about\\l":"что-нибудь потрясающее\\l",
"yourself.\\p":"о себе.\\p",
"What will you brag about?$":"Чем будешь хвастаться?$",
"Brag about something for me.\\n":"Похвастайся чем-нибудь.\\n",
"I'll give you a STICKER.$":"Я дам тебе STICKER.$",
"Oh, hi!\\n":"О, привет!\\n",
"Here comes the braggart.\\p":"А вот и хвастунишка.\\p",
"What are you going to brag about\\n":"Чем будешь хвастаться\\n",
"today?$":"сегодня?$",
"Oh, wow, you made it into the\\n":"Ого, ты попал в\\n",
"HALL OF FAME.\\p":"HALL OF FAME.\\p",
"That's pretty good, yup!\\n":"Очень неплохо!\\n",
"I'll give you one of these.$":"Дам тебе одну из этих.$",
"Oh, wow, you've entered the\\n":"Ого, ты входил в\\n",
"HALL OF FAME often!\\p":"HALL OF FAME много раз!\\p",
"That's impressive, yup!\\n":"Впечатляет!\\n",
"Whoa! You've made it into the\\n":"Ничего себе! Ты входил в\\n",
"HALL OF FAME that often?\\l":"HALL OF FAME столько раз?\\l",
"That's seriously incredible, yup!\\p":"Это действительно невероятно!\\p",
"You own the POKeMON LEAGUE!\\n":"POKeMON LEAGUE тебе покорилась!\\n",
"No way! You've gone into the\\n":"Не может быть! Ты входил в\\n",
"HALL OF FAME that many times?\\p":"HALL OF FAME столько раз?\\p",
"You're beyond incredible, yup!\\n":"Ты просто невероятен!\\n",
"That's it, I have to give you this.$":"Все, я обязан дать тебе это.$",
"The HALL OF FAME STICKER was\\n":"HALL OF FAME STICKER\\n",
"applied to the TRAINER CARD.$":"наклеен на TRAINER CARD.$",
"Hmm…\\p":"Хм…\\p",
"Come back with a better story next\\n":"В следующий раз приходи с историей\\n",
"time, okay?$":"получше, ладно?$",
"Oh, no, no can do.\\p":"Нет-нет, больше не могу.\\p",
"You're practically a living legend.\\n":"Ты практически живая легенда.\\n",
"I have no SITCKERS left to give.$":"У меня не осталось STICKERS.$",
"Oh, wow, there are POKeMON EGGS?\\n":"Ого, существуют POKeMON EGGS?\\n",
"I didn't know that!\\p":"Я и не знал!\\p",
"You've hatched that many EGGS?\\n":"Ты вывел столько EGGS?\\n",
"You really must like them!\\p":"Наверное, ты их очень любишь!\\p",
"Whoa! You've hatched a whole\\n":"Ничего себе! Ты вывел целую\\n",
"bunch of EGGS!\\p":"кучу EGGS!\\p",
"You're an EGG-hatching machine!\\n":"Да ты машина по выведению EGGS!\\n",
"Wh… You hatched that many EGGS?\\p":"Ч-что… Ты вывел столько EGGS?\\p",
"What's behind your love of EGGS?\\n":"Откуда такая любовь к EGGS?\\n",
"It's beyond incredible, yup!\\p":"Это просто невероятно!\\p",
"You're too awesome, I tell you.\\n":"Ты просто потрясающий.\\n",
"The EGG STICKER was applied\\n":"EGG STICKER\\n",
"to the TRAINER CARD.$":"наклеен на TRAINER CARD.$",
"Oh, wow, you've had success\\n":"Ого, ты побеждал\\n",
"link battling?\\p":"в link-боях?\\p",
"You're pretty strong, yup!\\n":"Ты довольно силен!\\n",
"You've beaten your friends a lot\\n":"Ты много раз побеждал друзей\\n",
"link battling, huh?\\p":"в link-боях, да?\\p",
"You're impressively strong, yup!\\n":"Ты впечатляюще силен!\\n",
"Whoa! You've beaten your friends\\n":"Ого! Ты побеждал друзей\\n",
"a frightful number of times.\\p":"пугающе много раз.\\p",
"Have you lost friends over this?\\n":"Ты из-за этого друзей не потерял?\\n",
"Wh… Wickedly whoa!\\n":"Ч-что… Вот это да!\\n",
"You've won mind-blowingly often!\\p":"Ты побеждал невероятно часто!\\p",
"It just knocks me out thinking\\n":"У меня голова кругом от мысли,\\n",
"about how tough you are.\\p":"насколько ты силен.\\p",
"You're the stuff of nightmares!\\n":"Ты настоящий кошмар соперников!\\n",
"The VICTORY STICKER was applied\\n":"VICTORY STICKER\\n",
}

DEX={
"POKeDEX registration completed.":"Регистрация в POKeDEX завершена.",
"Searching…\\nPlease wait.":"Поиск…\\nПодожди.",
"Search completed.":"Поиск завершен.",
"No matching POKeMON were found.":"Подходящие POKeMON не найдены.",
"Switch POKeDEX listings.":"Сменить список POKeDEX.",
"Return to the POKeDEX.":"Вернуться в POKeDEX.",
"Select the POKeDEX mode.":"Выбери режим POKeDEX.",
"Select the POKeDEX listing mode.":"Выбери порядок списка POKeDEX.",
"List by body color.\\nSpotted POKeMON only.":"Список по цвету тела.\\nТолько замеченные POKeMON.",
"List by type.\\nOwned POKeMON only.":"Список по типу.\\nТолько пойманные POKeMON.",
"Execute search/switch.":"Выполнить поиск/смену.",
"DON'T SPECIFY.":"НЕ УКАЗЫВАТЬ.",
"NONE":"НЕТ",
"HOENN region's POKeDEX":"POKeDEX региона HOENN",
"National edition POKeDEX":"Национальный POKeDEX",
"POKeMON are listed according to their\\nnumber.":"POKeMON перечислены по\\nномеру.",
"NUMERICAL MODE":"ПО НОМЕРАМ",
"A TO Z MODE":"A-Z РЕЖИМ",
"HEAVIEST MODE":"САМЫЕ ТЯЖ.",
"LIGHTEST MODE":"САМЫЕ ЛЕГК.",
"TALLEST MODE":"САМЫЕ ВЫС.",
"SMALLEST MODE":"САМЫЕ НИЗ.",
"RED":"КРАСНЫЙ","BLUE":"СИНИЙ","YELLOW":"ЖЕЛТЫЙ","GREEN":"ЗЕЛЕНЫЙ","BLACK":"ЧЕРНЫЙ",
"BROWN":"КОРИЧН.","PURPLE":"ФИОЛЕТ.","GRAY":"СЕРЫЙ","WHITE":"БЕЛЫЙ","PINK":"РОЗОВЫЙ",
}

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: localize_menu_card_dex_ui_v3_174.py <upstream-root>")
    root=Path(sys.argv[1]).resolve(); ops=0

    p=root/"src/main_menu.c"; t=p.read_text(encoding="utf-8")
    for old,new in NAMES.items():
        a=f'COMPOUND_STRING("{old}")'; b=f'COMPOUND_STRING("{new}")'
        if t.count(a)!=1: raise RuntimeError(f"main_menu preset {old}: {t.count(a)}")
        t=t.replace(a,b,1); ops+=1
    p.write_text(t,encoding="utf-8")

    p=root/"data/text/trainer_card_frlg.inc"; t=p.read_text(encoding="utf-8")
    for old,new in CARD.items():
        variants=[old,old.replace("POKe","POKé")]
        n=sum(t.count(v) for v in variants)
        if n:
            for v in variants:
                c=t.count(v)
                if c: t=t.replace(v,new); ops+=c
    p.write_text(t,encoding="utf-8")

    p=root/"src/pokedex.c"; t=p.read_text(encoding="utf-8")
    # Only replace complete translatable string literals. Never raw substrings:
    # entries such as BLACK / RED / NONE also occur inside C identifiers
    # (RGB_BLACK, BODY_COLOR_RED, etc.) and must remain source code.
    for old,new in DEX.items():
        variants=[old,old.replace("POKe","POKé")]
        for v in variants:
            patterns = (
                (f'_("{v}")', f'_("{new}")'),
                (f'COMPOUND_STRING("{v}")', f'COMPOUND_STRING("{new}")'),
            )
            for src,dst in patterns:
                n=t.count(src)
                if n:
                    t=t.replace(src,dst)
                    ops+=n
    p.write_text(t,encoding="utf-8")

    out=root/"build"/"qarro_ru_menu_card_dex_ui_v3_174_audit.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"operations":ops,
      "files":["src/main_menu.c","data/text/trainer_card_frlg.inc","src/pokedex.c"],
      "logicTouched":False,"ashBondTouched":False,"ashCapTouched":False},
      ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: {ops} UI/dialogue replacements across 3 files")
    return 0
if __name__=="__main__": raise SystemExit(main())
