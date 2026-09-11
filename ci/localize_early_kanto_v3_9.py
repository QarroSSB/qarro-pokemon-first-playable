#!/usr/bin/env python3
"""Qarro v3.17: close untranslated Pewter City interior gaps.

Runs CI-green v3.16, then patches only previously untouched pinned FireRed
Pewter interior files. Each source file is verified against its exact pinned
git-blob SHA before editing. Pokemon species, Move and Ability proper names
stay English. Gameplay, trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "2585e018f0e6c0243c1781d876fd3fd41c44147d"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_16"
BASE_COUNT = 210
MARKER = "QARRO_RU_EARLY_KANTO_V3_17"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")

def B(*lines: str) -> tuple[str, ...]: return lines

FILES = {
"data/maps/PewterCity_Museum_1F_Frlg/scripts.inc": ("a30b96ac99b5b88afeaa1991bd5cde2e7a800d3b", {
"PewterCity_Museum_1F_Text_Its50YForChildsTicket": B(r"Да-да.\n",r"Детский билет стоит ¥50.\p",r"Хочешь войти?$"),
"PewterCity_Museum_1F_Text_ComeAgain": B(r"Приходи еще!$"),
"PewterCity_Museum_1F_Text_Right50YThankYou": B(r"Верно, ¥50!\n",r"Спасибо!$"),
"PewterCity_Museum_1F_Text_DontHaveEnoughMoney": B(r"У тебя недостаточно денег.$"),
"PewterCity_Museum_1F_Text_PleaseEnjoyYourself": B(r"Приятного посещения.$"),
"PewterCity_Museum_1F_Text_DoYouKnowWhatAmberIs": B(r"С черного хода не проскользнуть!\n",r"Хорошая попытка, но нет.\p",r"Ладно!\n",r"Ты знаешь, что такое ЯНТАРЬ?$"),
"PewterCity_Museum_1F_Text_AmberContainsGeneticMatter": B(r"В ЯНТАРЕ сохраняется генетический\n",r"материал древних ПОКЕМОНОВ.\p",r"Где-то есть ЛАБОРАТОРИЯ,\n",r"пытающаяся оживлять их из ЯНТАРЯ.$"),
"PewterCity_Museum_1F_Text_AmberIsFossilizedSap": B(r"ЯНТАРЬ - это окаменевшая смола,\n",r"которая когда-то текла из деревьев.\p",r"Древняя смола со временем\n",r"окаменела и стала ЯНТАРЕМ.$"),
"PewterCity_Museum_1F_Text_ShouldBeGratefulForLongLife": B(r"Надо ценить мою долгую жизнь.\p",r"Никогда не думал, что увижу\n",r"кости настоящего дракона!$"),
"PewterCity_Museum_1F_Text_WantYouToGetAmberExamined": B(r"Тсс! Мне нужно поделиться\n",r"с кем-нибудь секретом.\p",r"Думаю, в этом куске ЯНТАРЯ\n",r"есть ДНК ПОКЕМОНА!\p",r"Если ПОКЕМОНОВ можно оживлять,\n",r"это будет научный прорыв.\p",r"Но коллеги меня не слушают.\p",r"Поэтому прошу тебя:\p",r"отнеси его на исследование\n",r"в какую-нибудь ЛАБОРАТОРИЮ.$"),
"PewterCity_Museum_1F_Text_ReceivedOldAmberFromMan": B(r"{PLAYER} получает СТАРЫЙ ЯНТАРЬ\n",r"от мужчины.$"),
"PewterCity_Museum_1F_Text_GetOldAmberChecked": B(r"Тсс!\n",r"Проверь СТАРЫЙ ЯНТАРЬ!$"),
"PewterCity_Museum_1F_Text_DontHaveSpaceForThis": B(r"Для этого нет места.$"),
"PewterCity_Museum_1F_Text_WeHaveTwoFossilsOnExhibit": B(r"У нас выставлены две окаменелости\n",r"редких древних ПОКЕМОНОВ.$"),
"PewterCity_Museum_1F_Text_BeautifulPieceOfAmber": B(r"Здесь красивый кусок прозрачного\n",r"золотистого ЯНТАРЯ.$"),
"PewterCity_Museum_1F_Text_AerodactylFossil": B(r"Окаменелость AERODACTYL\n",r"Редкий древний ПОКЕМОН.$"),
"PewterCity_Museum_1F_Text_KabutopsFossil": B(r"Окаменелость KABUTOPS\n",r"Редкий древний ПОКЕМОН.$"),
}),
"data/maps/PewterCity_Museum_2F_Frlg/scripts.inc": ("65ed5bdc4838b943242866fc1cda67fe7b67f763", {
"Text_SeismicTossTeach": B(r"Тайны космоса...\n",r"Загадки Земли...\p",r"Мы так мало знаем\n",r"о стольких вещах.\p",r"Но это повод учиться усерднее,\n",r"а не сдаваться.\p",r"Бросать стоит кое-что другое...\p",r"Например, SEISMIC TOSS.\n",r"Научить этой атаке ПОКЕМОНА?$"),
"Text_SeismicTossDeclined": B(r"Вот как?\n",r"Уверен, ты еще вернешься.$"),
"Text_SeismicTossWhichMon": B(r"Какой ПОКЕМОН хочет выучить\n",r"SEISMIC TOSS?$"),
"Text_SeismicTossTaught": B(r"Надеюсь, ты не сдашься.\n",r"Продолжай в том же духе.$"),
"PewterCity_Museum_1F_Text_WhatsSpecialAboutMoonStone": B(r"ЛУННЫЙ КАМЕНЬ, значит?\p",r"Что в нем особенного?\n",r"По мне, обычный камень.$"),
"PewterCity_Museum_1F_Text_BoughtColorTVForMoonLanding": B(r"20 июля 1969 года!\p",r"В тот день человек впервые\n",r"ступил на Луну.\p",r"Я купил цветной телевизор,\n",r"чтобы увидеть эти новости.$"),
"PewterCity_Museum_1F_Text_RunningSpaceExhibitThisMonth": B(r"В этом месяце у нас проходит\n",r"выставка о космосе.$"),
"PewterCity_Museum_1F_Text_AskedDaddyToCatchPikachu": B(r"Я хочу PIKACHU!\n",r"Он такой милый!\p",r"Я попросила папу поймать мне его!$"),
"PewterCity_Museum_1F_Text_PikachuSoonIPromise": B(r"Да, скоро будет PIKACHU, обещаю!$"),
"PewterCity_Museum_1F_Text_SpaceShuttle": B(r"Космический шаттл$"),
"PewterCity_Museum_1F_Text_MeteoriteThatFellOnMtMoon": B(r"Метеорит, упавший на MT. MOON.\n",r"Считается ЛУННЫМ КАМНЕМ.$"),
}),
"data/maps/PewterCity_Mart_Frlg/scripts.inc": ("2fa94240bf53a2010e4cfd65f5d9cbc7f2b1385e", {
"PewterCity_Mart_Text_BoughtWeirdFishFromShadyGuy": B(r"Какой-то мутный старик уговорил\n",r"меня купить странного рыбного ПОКЕМОНА!\p",r"Он совсем слабый и стоил ¥500!$"),
"PewterCity_Mart_Text_GoodThingsIfRaiseMonsDiligently": B(r"Если усердно растить ПОКЕМОНОВ,\n",r"может случиться что-то хорошее.\p",r"Даже слабые способны удивить,\n",r"если не сдаваться.$"),
}),
"data/maps/PewterCity_House1_Frlg/scripts.inc": ("c83439961247ea1ec4d03fb0f3383a8e5fe4ff90", {
"PewterCity_House1_Text_Nidoran": B(r"NIDORAN♂: Гав-гав!$"),
"PewterCity_House1_Text_NidoranSit": B(r"NIDORAN, сидеть!$"),
"PewterCity_House1_Text_TradeMonsAreFinicky": B(r"Наш ПОКЕМОН получен обменом,\n",r"поэтому с ним непросто.\p",r"Чужой ПОКЕМОН - тот, которого\n",r"ты получил в обмене.\p",r"Он быстро растет, но может\n",r"не слушаться неопытного ТРЕНЕРА.\p",r"Вот бы у нас были ЗНАЧКИ...$"),
}),
"data/maps/PewterCity_House2_Frlg/scripts.inc": ("dc1a88233531001f8543f86d6383b455582777d7", {
"PewterCity_House2_Text_MonsLearnTechniquesAsTheyGrow": B(r"По мере роста ПОКЕМОНЫ учат\n",r"новые приемы.\p",r"Но некоторым атакам их должны\n",r"обучать люди.$"),
"PewterCity_House2_Text_MonsEasierCatchIfStatused": B(r"ПОКЕМОНА легче поймать,\n",r"если у него есть статус.\p",r"Сон, яд, ожог или паралич -\n",r"все это помогает.\p",r"Но поимка ПОКЕМОНА никогда\n",r"не гарантирована!$"),
}),
"data/maps/PewterCity_PokemonCenter_1F_Frlg/scripts.inc": ("d4a7e9ef7894e4ee171f6a7173a6c5fa4685a53", {
"PewterCity_PokemonCenter_1F_Text_TeamRocketMtMoonImOnPhone": B(r"Что!?\p",r"КОМАНДА R на MT. MOON?\n",r"Что?\p",r"Я по телефону говорю!\n",r"Отойди!$"),
"PewterCity_PokemonCenter_1F_Text_Jigglypuff": B(r"JIGGLYPUFF: Пуу-пупуу!$"),
"PewterCity_PokemonCenter_1F_Text_WhenJiggylypuffSingsMonsGetDrowsy": B(r"Зеваю!\p",r"Когда JIGGLYPUFF поет,\n",r"ПОКЕМОНОВ клонит в сон...\p",r"...Меня тоже...\n",r"Хр-р-р...$"),
"PewterCity_PokemonCenter_1F_Text_TradingMyClefairyForPikachu": B(r"Я очень хочу PIKACHU,\n",r"поэтому меняю на него CLEFAIRY.$"),
"PewterCity_PokemonCenter_1F_Text_TradingPikachuWithKid": B(r"Я обмениваюсь ПОКЕМОНАМИ\n",r"с тем парнем.\p",r"У меня два PIKACHU, так что\n",r"одного можно обменять.$"),
}),
}

def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(["git","-C",str(repo),"fetch","--quiet","--depth=1","origin",BASE_COMMIT], check=True)
    return subprocess.check_output(["git","-C",str(repo),"show",f"{BASE_COMMIT}:{BASE_PATH}"], text=True)

def render(label: str, lines: tuple[str, ...]) -> str:
    return label + "::\n" + "".join(f'\t.string "{line}"\n' for line in lines)

def patch_label(text: str, label: str, lines: tuple[str, ...]) -> str:
    pat = re.compile(rf"(?m)^{re.escape(label)}::\n(?:\t\.string .*\n)+")
    hits = list(pat.finditer(text))
    if len(hits) != 1:
        raise RuntimeError(f"{label}: expected exactly one string block, got {len(hits)}")
    old = hits[0].group(0)
    if any("\u0400" <= ch <= "\u04ff" for ch in old):
        raise RuntimeError(f"{label}: source block unexpectedly already contains Cyrillic")
    return text[:hits[0].start()] + render(label, lines) + text[hits[0].end():]

def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <pokeemerald-expansion-root>", file=sys.stderr); return 2
    code = load_base()
    ns = {"__name__":"qarro_ru_early_kanto_v316_base","__file__":str(Path(__file__).resolve())}
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc: return rc
    root = Path(sys.argv[1]).resolve()
    audit_path = root / AUDIT_REL
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != BASE_MARKER or audit.get("selectedBlocksLocalized") != BASE_COUNT:
        raise RuntimeError(f"base localization audit drift: {audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}")
    changed_total = 0
    for rel, (blob, blocks) in FILES.items():
        path = root / rel
        actual = subprocess.check_output(["git","-C",str(root),"hash-object",str(path)], text=True).strip()
        if actual != blob:
            raise RuntimeError(f"{rel}: pinned source blob drift: {actual} != {blob}")
        text = path.read_text(encoding="utf-8")
        for label, lines in blocks.items():
            text = patch_label(text, label, lines)
            changed_total += 1
        path.write_text(text, encoding="utf-8")
        audit.setdefault("files", {})[rel] = {"selectedBlocks":len(blocks),"changedThisRun":len(blocks),"sourceBlob":blob}
        print(f"[ru-early-v317] {rel}: {len(blocks)}/{len(blocks)} blocks changed")
    expected_new = sum(len(v[1]) for v in FILES.values())
    if expected_new != 40 or changed_total != expected_new:
        raise RuntimeError(f"Pewter interior scope drift: expected 40, got {expected_new}/{changed_total}")
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + expected_new,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun",0)) + changed_total,
        "pewterAccessibleInteriorsLocalized": True,
        "pewterMuseumLocalized": True,
        "pewterMartHouseCenterLocalized": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {expected_new} Pewter interior blocks = {BASE_COUNT + expected_new}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
