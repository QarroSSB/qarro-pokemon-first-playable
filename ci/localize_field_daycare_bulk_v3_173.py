#!/usr/bin/env python3
"""Qarro v3.173: field-move + Day Care bulk localization.

Translates all remaining English user-facing string literals in
field_move_scripts.inc, day_care_frlg.inc and day_care.inc while preserving
Move/Pokémon proper-name canon and all control placeholders.
"""
from __future__ import annotations
import json,sys
from pathlib import Path

MARKER="QARRO_RU_FIELD_DAYCARE_BULK_V3_173"

MAPS={
"data/scripts/field_move_scripts.inc":{
"This tree looks like it can be\\n":"Похоже, это дерево можно\\n",
"CUT down!\\p":"срубить приемом CUT!\\p",
"Would you like to CUT it?$":"Использовать CUT?$",
"{STR_VAR_1} used {STR_VAR_2}!$":"{STR_VAR_1} использует {STR_VAR_2}!$",
"CUT down!$":"срубить приемом CUT!$",
"This rock appears to be breakable.\\n":"Похоже, этот камень можно разбить.\\n",
"Would you like to use ROCK SMASH?$":"Использовать ROCK SMASH?$",
"It's a rugged rock, but a POKéMON\\n":"Это прочный камень, но POKeMON\\n",
"may be able to smash it.$":"может суметь разбить его.$",
"It's a big boulder, but a POKéMON\\n":"Это большой валун, но POKeMON\\n",
"may be able to push it aside.\\p":"может суметь оттолкнуть его.\\p",
"Would you like to use STRENGTH?$":"Использовать STRENGTH?$",
"{STR_VAR_1} used STRENGTH!\\p":"{STR_VAR_1} использует STRENGTH!\\p",
"{STR_VAR_1}'s STRENGTH made it\\n":"STRENGTH {STR_VAR_1} позволяет\\n",
"possible to move boulders around!$":"передвигать валуны!$",
"may be able to push it aside.$":"может суметь оттолкнуть его.$",
"STRENGTH made it possible to move\\n":"STRENGTH позволяет передвигать\\n",
"boulders around.$":"валуны.$",
"A wall of water is crashing down with\\n":"Стена воды обрушивается вниз с\\n",
"a mighty roar.$":"оглушительным ревом.$",
"It's a large waterfall.\\n":"Это большой водопад.\\n",
"Would you like to use WATERFALL?$":"Использовать WATERFALL?$",
"{STR_VAR_1} used WATERFALL.$":"{STR_VAR_1} использует WATERFALL.$",
"The sea is deep here. A POKéMON\\n":"Здесь глубокое море. POKeMON\\n",
"may be able to go underwater.$":"может суметь нырнуть под воду.$",
"The sea is deep here.\\n":"Здесь глубокое море.\\n",
"Would you like to use DIVE?$":"Использовать DIVE?$",
"{STR_VAR_1} used DIVE.$":"{STR_VAR_1} использует DIVE.$",
"Light is filtering down from above.\\n":"Сверху пробивается свет.\\n",
"A POKéMON may be able to surface.$":"POKeMON может суметь всплыть.$",
"Looks like there's nothing here…$":"Похоже, здесь ничего нет…$",
"The cliff is steep.\\n":"Утес очень крутой.\\n",
"Would you like to use Rock Climb?$":"Использовать Rock Climb?$",
"{STR_VAR_1} used Rock Climb!$":"{STR_VAR_1} использует Rock Climb!$",
"A Pokémon may be able to climb it.$":"POKeMON может суметь взобраться.$",
},
"data/text/day_care_frlg.inc":{
"I'm the DAY-CARE MAN.\\p":"Я работаю в DAY-CARE.\\p",
"I help take care of the precious\\n":"Я помогаю заботиться о дорогих\\n",
"POKéMON of TRAINERS.\\p":"POKeMON разных TRAINERS.\\p",
"If you'd like me to raise your\\n":"Если хочешь оставить своего\\n",
"POKéMON, have a word with my wife.$":"POKeMON, поговори с моей женой.$",
"Ah, it's you!\\p":"А, это ты!\\p",
"We were raising your POKéMON, and\\n":"Мы присматривали за твоим POKeMON, и\\n",
"my goodness, were we surprised!\\p":"как же мы удивились!\\p",
"Your POKéMON had an EGG!\\p":"У твоего POKeMON появилось EGG!\\p",
"We don't know how it got there,\\n":"Мы не знаем, откуда оно взялось,\\n",
"but your POKéMON had it.\\p":"но оно было у твоего POKeMON.\\p",
"You do want it, yes?$":"Ты ведь хочешь забрать его?$",
"Ah, it's you! Good to see you.\\n":"А, это ты! Рад тебя видеть.\\n",
"Your {STR_VAR_1}'s doing fine.$":"{STR_VAR_1} чувствует себя отлично.$",
"Well then, I'll keep it.\\n":"Хорошо, тогда я оставлю его.\\n",
"Thanks!$":"Спасибо!$",
"You have no room for it…\\n":"У тебя нет для него места…\\n",
"Come back when you've made room.$":"Вернись, когда освободишь место.$",
"{PLAYER} received the EGG from\\n":"{PLAYER} получил EGG от\\n",
"the DAY-CARE MAN.$":"работника DAY-CARE.$",
"Take good care of it.$":"Позаботься о нем.$",
"Ah, it's you! Your {STR_VAR_1} and\\n":"А, это ты! {STR_VAR_1} и\\n",
"{STR_VAR_2} are doing fine.$":"{STR_VAR_2} чувствуют себя отлично.$",
"I really will keep it.\\n":"Я правда оставлю его.\\n",
"You do want this, yes?$":"Ты уверен, что хочешь этого?$",
"I'm the DAY-CARE LADY.\\p":"Я хозяйка DAY-CARE.\\p",
"We can raise POKéMON for you.\\p":"Мы можем присматривать за POKeMON.\\p",
"Would you like us to raise one?$":"Оставишь одного у нас?$",
"Which POKéMON should we raise for\\n":"Какого POKeMON нам оставить\\n",
"you?$":"у себя?$",
"Fine, we'll raise your {STR_VAR_1}\\n":"Хорошо, мы присмотрим за {STR_VAR_1}\\n",
"for a while.\\p":"некоторое время.\\p",
"Come back for it later.$":"Забери его позже.$",
"We can raise two of your POKéMON.\\p":"Мы можем присматривать за двумя POKeMON.\\p",
"Would you like us to raise one\\n":"Хочешь оставить у нас еще\\n",
"more POKéMON for you?$":"одного POKeMON?$",
"My husband was looking for you.$":"Мой муж тебя искал.$",
"Oh, fine, then.\\n":"Ну хорошо.\\n",
"Come again.$":"Приходи еще.$",
"You don't have enough money…$":"У тебя недостаточно денег…$",
"Will you take back the other one,\\n":"Заберешь и второго POKeMON,\\n",
"too?$":"тоже?$",
"Fine.\\n":"Хорошо.\\n",
"Good to see you.\\p":"Рад тебя видеть.\\p",
"Your POKéMON can only be doing\\n":"Твой POKeMON чувствует себя\\n",
"good!$":"отлично!$",
"By level, your {STR_VAR_1} has\\n":"{STR_VAR_1} вырос\\n",
"grown by {STR_VAR_2}.$":"на {STR_VAR_2} уровней.$",
"Your POKéMON party is full.\\n":"Твоя команда POKeMON заполнена.\\n",
"Make room, then come see me.$":"Освободи место и возвращайся.$",
"If you want your {STR_VAR_1} back,\\n":"Чтобы забрать {STR_VAR_1},\\n",
"it will cost ¥{STR_VAR_2}.$":"нужно заплатить ¥{STR_VAR_2}.$",
"Perfect!\\n":"Отлично!\\n",
"Here's your POKéMON.$":"Вот твой POKeMON.$",
"{PLAYER} took back {STR_VAR_1} from\\n":"{PLAYER} забрал {STR_VAR_1} у\\n",
"the DAY-CARE LADY.$":"хозяйки DAY-CARE.$",
"Oh? But you have just one\\n":"О? Но у тебя только один\\n",
"POKéMON.\\p":"POKeMON.\\p",
"Come back another time.$":"Приходи в другой раз.$",
"Will you take your POKéMON back?$":"Заберешь своего POKeMON?$",
"If you leave me that POKéMON,\\n":"Если оставишь мне этого POKeMON,\\n",
"what will you battle with?\\p":"кем ты будешь сражаться?\\p",
"Huh?$":"А?$",
},
"data/scripts/day_care.inc":{
"I'm the DAY-CARE MAN.\\p":"Я работаю в DAY-CARE.\\p",
"I help take care of the precious\\n":"Я помогаю заботиться о дорогих\\n",
"POKéMON of TRAINERS.\\p":"POKeMON разных TRAINERS.\\p",
"If you'd like me to raise your POKéMON,\\n":"Если хочешь оставить своего POKeMON,\\n",
"have a word with my wife.$":"поговори с моей женой.$",
"Ah, it's you!\\p":"А, это ты!\\p",
"We were raising your POKéMON,\\n":"Мы присматривали за твоим POKeMON,\\n",
"and my goodness, were we surprised!\\p":"и как же мы удивились!\\p",
"Your POKéMON had an EGG!\\p":"У твоего POKeMON появилось EGG!\\p",
"We don't know how it got there,\\n":"Мы не знаем, откуда оно взялось,\\n",
"but your POKéMON had it.\\p":"но оно было у твоего POKeMON.\\p",
"You do want it, yes?$":"Ты ведь хочешь забрать его?$",
"Ah, it's you! Good to see you.\\n":"А, это ты! Рад тебя видеть.\\n",
"Your {STR_VAR_1}'s doing fine.$":"{STR_VAR_1} чувствует себя отлично.$",
"Well then, I'll keep it.\\n":"Хорошо, тогда я оставлю его.\\n",
"Thanks!$":"Спасибо!$",
"You have no room for it…\\n":"У тебя нет для него места…\\n",
"Come back when you've made room.$":"Вернись, когда освободишь место.$",
"{PLAYER} received the EGG from\\n":"{PLAYER} получил EGG от\\n",
"the DAY-CARE MAN.$":"работника DAY-CARE.$",
"Take good care of it.$":"Позаботься о нем.$",
"By the way, about your {STR_VAR_1},\\n":"Кстати, твой {STR_VAR_1}\\n",
"it seemed to be friendly with\\l":"похоже, подружился с\\l",
"{STR_VAR_2}'s {STR_VAR_3}.\\p":"{STR_VAR_3} тренера {STR_VAR_2}.\\p",
"I may even have seen it receiving\\n":"Кажется, я даже видел, как он получал\\n",
"a piece of MAIL.$":"MAIL.$",
"If you want to pick up your POKéMON,\\n":"Если хочешь забрать своего POKeMON,\\n",
"Ah, it's you! Your {STR_VAR_1} and\\n":"А, это ты! {STR_VAR_1} и\\n",
"{STR_VAR_2} are doing fine.$":"{STR_VAR_2} чувствуют себя отлично.$",
"I really will keep it.\\n":"Я правда оставлю его.\\n",
"You do want this, yes?$":"Ты уверен, что хочешь этого?$",
"I'm the DAY-CARE LADY.\\p":"Я хозяйка DAY-CARE.\\p",
"We can raise POKéMON for you.\\p":"Мы можем присматривать за POKeMON.\\p",
"Would you like us to raise one?$":"Оставишь одного у нас?$",
"Which POKéMON should we raise for\\n":"Какого POKeMON нам оставить\\n",
"you?$":"у себя?$",
"Fine, we'll raise your {STR_VAR_1}\\n":"Хорошо, мы присмотрим за {STR_VAR_1}\\n",
"for a while.\\p":"некоторое время.\\p",
"Come back for it later.$":"Забери его позже.$",
"We can raise two of your POKéMON.\\n":"Мы можем присматривать за двумя POKeMON.\\n",
"Would you like us to raise one more?$":"Хочешь оставить еще одного?$",
"My husband was looking for you.$":"Мой муж тебя искал.$",
"Oh, fine, then.\\n":"Ну хорошо.\\n",
"Come again.$":"Приходи еще.$",
"You don't have enough money…$":"У тебя недостаточно денег…$",
"Will you take back the other one,\\n":"Заберешь и второго POKeMON,\\n",
"too?$":"тоже?$",
"Fine.\\n":"Хорошо.\\n",

"Your POKéMON can only be doing good!$":"Твой POKeMON чувствует себя отлично!$",
"By level, your {STR_VAR_1} has\\n":"{STR_VAR_1} вырос\\n",
"grown by {STR_VAR_2}.$":"на {STR_VAR_2} уровней.$",
"Your POKéMON team is full.\\n":"Твоя команда POKeMON заполнена.\\n",
"Make room, then come see me.$":"Освободи место и возвращайся.$",
"Which POKéMON will you take back?$":"Какого POKeMON ты заберешь?$",
"If you want your {STR_VAR_1} back,\\n":"Чтобы забрать {STR_VAR_1},\\n",
"it will cost ¥{STR_VAR_2}.$":"нужно заплатить ¥{STR_VAR_2}.$",
"Perfect!\\n":"Отлично!\\n",
"Here's your POKéMON.$":"Вот твой POKeMON.$",
"{PLAYER} took back {STR_VAR_1} from\\n":"{PLAYER} забрал {STR_VAR_1} у\\n",
"the DAY-CARE LADY.$":"хозяйки DAY-CARE.$",
"Oh? But you have just one\\n":"О? Но у тебя только один\\n",
"POKéMON.\\p":"POKeMON.\\p",
"Come back another time.$":"Приходи в другой раз.$",
"Will you take your POKéMON back?$":"Заберешь своего POKeMON?$",
"If you leave me that POKéMON,\\n":"Если оставишь мне этого POKeMON,\\n",
"what will you battle with?\\p":"кем ты будешь сражаться?\\p",
"Huh?$":"А?$",
"Huh?\\n":"А?\\n",
"Now, now.\\p":"Ну-ну.\\p",
"If you leave that POKéMON with\\n":"Если оставишь этого POKeMON\\n",
"me, you'll be left with just one.\\p":"у меня, у тебя останется только один.\\p",
"You will be better off if you catch\\n":"Лучше сначала поймай\\n",
"some more, I dare say.$":"еще нескольких.$",
}
}

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: localize_field_daycare_bulk_v3_173.py <upstream-root>")
    root=Path(sys.argv[1]).resolve()
    operations=0
    for rel,mapping in MAPS.items():
        p=root/rel; text=p.read_text(encoding="utf-8")
        for old,new in mapping.items():
            needle=f'.string "{old}"'
            repl=f'.string "{new}"'
            n=text.count(needle)
            if n<1: raise RuntimeError(f"{rel}: missing literal {old!r}")
            text=text.replace(needle,repl)
            operations+=n
        p.write_text(text,encoding="utf-8")
    out=root/"build"/"qarro_ru_field_daycare_bulk_v3_173_audit.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
      "marker":MARKER,"replacementOccurrences":operations,
      "files":list(MAPS),"logicTouched":False,
      "ashBondTouched":False,"ashCapTouched":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: replaced {operations} English string-line occurrences across 3 text surfaces")
    return 0
if __name__=="__main__": raise SystemExit(main())
