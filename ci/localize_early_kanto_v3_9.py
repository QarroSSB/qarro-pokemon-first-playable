#!/usr/bin/env python3
"""Qarro v3.15 early-Kanto Russian localization: complete Pewter City exterior.

Runs the exact CI-verified v3.14 pass from cd003c8, then localizes the remaining
user-facing English text in PewterCity_Frlg/scripts.inc. Exact source matching
keeps the pass fail-closed. Pokemon species, Move and Ability proper names stay
English. Gameplay, trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

BASE_COMMIT = "cd003c8fa30685d9e1b77c5d466e6ca7f6bf0a69"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_14"
MARKER = "QARRO_RU_EARLY_KANTO_V3_15"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
REL = "data/maps/PewterCity_Frlg/scripts.inc"

def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT], check=True)
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"], text=True)

def B(*lines: str) -> tuple[str, ...]: return lines

PATCHES = {
"Text_DreamEaterTeach": (B(r"Yawn!\n",r"I must have dozed off in the sun.\p",r"I had this weird dream about\n",r"a DROWZEE eating my dream.\p",r"And…\n",r"I learned how to eat dreams…\p",r"Oogh, this is too spooky!\p",r"Let me teach it to a POKéMON so\n",r"I can forget about it!$"), B(r"Зеваю!\n",r"Кажется, я задремал на солнце.\p",r"Мне приснился странный сон:\n",r"DROWZEE пожирал мой сон.\p",r"А потом...\n",r"я научился пожирать сны...\p",r"Ух, жутковато!\p",r"Научу этому ПОКЕМОНА,\n",r"чтобы самому забыть!$")),
"Text_DreamEaterDeclined": (B(r"…Snore…$"), B(r"...Хр-р-р...$")),
"Text_DreamEaterWhichMon": (B(r"Which POKéMON wants to learn\n",r"DREAM EATER?$"), B(r"Какой ПОКЕМОН хочет выучить\n",r"DREAM EATER?$")),
"Text_DreamEaterTaught": (B(r"…ZZZ…\n",r"I…can't eat…anymore…$"), B(r"...Хр-р-р...\n",r"Я... больше не могу есть...$")),
"PewterCity_Text_ClefairyCameFromMoon": (B(r"CLEFAIRY came from the moon.\n",r"That's what the rumor is.\p",r"They appeared after MOON STONES\n",r"fell on MT. MOON.$"), B(r"Говорят, CLEFAIRY пришли с Луны.\p",r"Они появились после того, как\n",r"MOON STONES упали на MT. MOON.$")),
"PewterCity_Text_BrockOnlySeriousTrainerHere": (B(r"There aren't many serious POKéMON\n",r"TRAINERS here.\p",r"They're all like BUG CATCHERS,\n",r"you know, just hobbyists.\p",r"But PEWTER GYM's BROCK isn't like\n",r"that, not one bit.$"), B(r"Здесь мало серьезных тренеров.\p",r"В основном любители вроде\n",r"ловцов жуков.\p",r"Но BROCK из PEWTER GYM\n",r"совсем другой.$")),
"PewterCity_Text_DidYouCheckOutMuseum": (B(r"Did you check out the MUSEUM?$"), B(r"Ты уже был в МУЗЕЕ?$")),
"PewterCity_Text_WerentThoseFossilsAmazing": (B(r"Weren't those fossils from MT. MOON\n",r"amazing?$"), B(r"Правда, окаменелости с MT. MOON\n",r"потрясающие?$")),
"PewterCity_Text_ReallyYouHaveToGo": (B(r"Really?\n",r"You absolutely have to go!$"), B(r"Правда?\n",r"Тогда тебе обязательно надо туда!$")),
"PewterCity_Text_ThisIsTheMuseum": (B(r"This is it, the MUSEUM.\p",r"You have to pay to get in, but it's\n",r"worth it. See you around!$"), B(r"Вот он, МУЗЕЙ.\p",r"Вход платный, но оно того стоит.\n",r"Еще увидимся!$")),
"PewterCity_Text_DoYouKnowWhatImDoing": (B(r"Psssst!\n",r"Do you know what I'm doing?$"), B(r"Пс-с-с!\n",r"Знаешь, что я делаю?$")),
"PewterCity_Text_ThatsRightItsHardWork": (B(r"That's right!\n",r"It's hard work!$"), B(r"Верно!\n",r"Работа непростая!$")),
"PewterCity_Text_SprayingRepelToKeepWildMonsOut": (B(r"I'm spraying REPEL to keep wild\n",r"POKéMON out of my garden!$"), B(r"Я распыляю REPEL, чтобы дикие\n",r"ПОКЕМОНЫ не лезли в мой сад!$")),
"PewterCity_Text_BrocksLookingForChallengersFollowMe": (B(r"You're a TRAINER, right?\p",r"BROCK's looking for new\n",r"challengers. Follow me!$"), B(r"Ты тренер, верно?\p",r"BROCK ищет новых соперников.\n",r"Иди за мной!$")),
"PewterCity_Text_GoTakeOnBrock": (B(r"If you have the right stuff,\n",r"go take on BROCK!$"), B(r"Если уверен в себе,\n",r"брось вызов BROCK!$")),
"PewterCity_Text_TrainerTipsEarningEXP": (B(r"TRAINER TIPS\p",r"All POKéMON that appear in battle,\n",r"however briefly, earn EXP Points.$"), B(r"СОВЕТ ТРЕНЕРУ\p",r"Все ПОКЕМОНЫ, участвовавшие\n",r"в бою, получают EXP Points.$")),
"PewterCity_Text_CallPoliceIfInfoOnThieves": (B(r"NOTICE!\p",r"Thieves have been stealing POKéMON\n",r"fossils from MT. MOON.\p",r"Please call the PEWTER POLICE if\n",r"you have any information.$"), B(r"ОБЪЯВЛЕНИЕ!\p",r"Воры крадут окаменелости\n",r"ПОКЕМОНОВ с MT. MOON.\p",r"Если что-то знаете, сообщите\n",r"полиции ПЬЮТЕРА.$")),
"PewterCity_Text_MuseumOfScience": (B(r"PEWTER MUSEUM OF SCIENCE$"), B(r"МУЗЕЙ НАУКИ ПЬЮТЕРА$")),
"PewterCity_Text_GymSign": (B(r"PEWTER CITY POKéMON GYM\n",r"LEADER: BROCK\l",r"The Rock-Solid POKéMON TRAINER!$"), B(r"ПОКЕМОН-ГИМ ПЬЮТЕРА\n",r"ЛИДЕР: BROCK\l",r"Непоколебимый каменный тренер!$")),
"PewterCity_Text_CitySign": (B(r"PEWTER CITY\n",r"A Stone Gray City$"), B(r"ПЬЮТЕР-СИТИ\n",r"Город каменно-серого цвета$")),
"PewterCity_Text_OhPlayer": (B(r"Oh, {PLAYER}{KUN}!$"), B(r"О, {PLAYER}{KUN}!$")),
"PewterCity_Text_AskedToDeliverThis": (B(r"I'm glad I caught up to you.\n",r"I'm PROF. OAK's AIDE.\p",r"I've been asked to deliver this,\n",r"so here you go.$"), B(r"Хорошо, что я тебя догнал.\n",r"Я помощник PROF. OAK.\p",r"Меня просили передать это тебе.\n",r"Держи.$")),
"PewterCity_Text_ReceivedRunningShoesFromAide": (B(r"{PLAYER} received the\n",r"RUNNING SHOES from the AIDE.$"), B(r"{PLAYER} получает\n",r"RUNNING SHOES от ПОМОЩНИКА.$")),
"PewterCity_Text_SwitchedShoesWithRunningShoes": (B(r"{PLAYER} switched shoes with the\n",r"RUNNING SHOES.$"), B(r"{PLAYER} переобувается\n",r"в RUNNING SHOES.$")),
"PewterCity_Text_ExplainRunningShoes": (B(r"Press the B Button to run.\n",r"But only where there's room to run!$"), B(r"Нажми кнопку B, чтобы бежать.\n",r"Но только там, где хватает места!$")),
"PewterCity_Text_MustBeGoingBackToLab": (B(r"Well, I must be going back to\n",r"the LAB.\p",r"Bye-bye!$"), B(r"Ну, мне пора возвращаться\n",r"в ЛАБОРАТОРИЮ.\p",r"Пока!$")),
"PewterCity_Text_RunningShoesLetterFromMom": (B(r"There's a letter attached…\p",r"Dear {PLAYER},\p",r"Here is a pair of RUNNING SHOES\n",r"for my beloved challenger.\p",r"Remember, I'll always cheer for\n",r"you! Don't ever give up!\p",r"From Mom$"), B(r"К обуви прикреплено письмо...\p",r"Дорогой {PLAYER},\p",r"Вот RUNNING SHOES для моего\n",r"любимого чемпиона.\p",r"Помни: я всегда болею за тебя!\n",r"Никогда не сдавайся!\p",r"Мама$")),
}

def render(label: str, lines: tuple[str, ...]) -> str:
    return label + "::\n" + "".join(f'\t.string "{line}"\n' for line in lines)

def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <pokeemerald-expansion-root>", file=sys.stderr); return 2
    code = load_base()
    ns = {"__name__":"qarro_ru_early_kanto_v314_base", "__file__":str(Path(__file__).resolve())}
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc: return rc
    root = Path(sys.argv[1]).resolve()
    audit_path = root / AUDIT_REL
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != BASE_MARKER or audit.get("selectedBlocksLocalized") != 150:
        raise RuntimeError(f"base localization audit drift: {audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}")
    path = root / REL
    text = path.read_text(encoding="utf-8")
    changed = 0
    for label, (old_lines, new_lines) in PATCHES.items():
        old, new = render(label, old_lines), render(label, new_lines)
        oc, nc = text.count(old), text.count(new)
        if oc == 1 and nc == 0:
            text = text.replace(old, new, 1); changed += 1
        elif oc == 0 and nc == 1:
            pass
        else:
            raise RuntimeError(f"{REL}: {label}: expected one untouched or translated block; old={oc}, new={nc}")
    if changed != len(PATCHES):
        raise RuntimeError(f"fresh pinned checkout should change all {len(PATCHES)} Pewter blocks; got {changed}")
    path.write_text(text, encoding="utf-8")
    audit.setdefault("files", {})[REL] = {"selectedBlocks": len(PATCHES), "changedThisRun": changed}
    audit["previousMarker"] = BASE_MARKER
    audit["marker"] = MARKER
    audit["selectedBlocksLocalized"] = 150 + changed
    audit["blocksChangedThisRun"] = int(audit.get("blocksChangedThisRun", 0)) + changed
    audit["pewterCityExteriorLocalized"] = True
    audit["pewterRunningShoesLocalized"] = True
    audit["dreamEaterTutorDialogueLocalized"] = True
    audit["pokemonSpeciesProperNamesEnglish"] = True
    audit["moveProperNamesEnglish"] = True
    audit["abilityProperNamesEnglish"] = True
    audit["gameplayTouched"] = False
    audit["trainerDataTouched"] = False
    audit["ashBondTouched"] = False
    audit["ashCapTouched"] = False
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base 150 + {changed} Pewter City blocks = {150 + changed} localized blocks")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
