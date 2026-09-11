#!/usr/bin/env python3
"""Qarro v3.16: close untranslated Viridian / Route 2 interior gaps.

Runs CI-green v3.15, then patches only previously untouched pinned FireRed map
files. Every source file is checked against its exact pinned git-blob SHA before
editing. Pokemon species, Move and Ability proper names stay English.
Gameplay, trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "3df3c4dc390d79b56a21c8e365d3d9e9bd8c27c8"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_15"
BASE_COUNT = 177
MARKER = "QARRO_RU_EARLY_KANTO_V3_16"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")

def B(*lines: str) -> tuple[str, ...]: return lines

FILES = {
"data/maps/ViridianCity_House_Frlg/scripts.inc": ("17041c37d73dfbf5465c72e09743626bbf3e7c4d", {
"ViridianCity_House_Text_NicknamingIsFun": B(r"Придумывать прозвища весело,\n",r"но это не так уж просто.\p",r"Хитрые имена хороши, но простые\n",r"легче запомнить.$"),
"ViridianCity_House_Text_MyDaddyLovesMonsToo": B(r"Мой папа тоже любит ПОКЕМОНОВ.$"),
"ViridianCity_House_Text_Speary": B(r"SPEARY: Чирик-чирик!$"),
"ViridianCity_House_Text_SpearowNameSpeary": B(r"SPEAROW\n",r"Имя: SPEARY$"),
}),
"data/maps/ViridianCity_School_Frlg/scripts.inc": ("2c8fe149775d5c8839d79e47a2f6ee630dbc626c", {
"ViridianCity_School_Text_TryingToMemorizeNotes": B(r"Уф! Пытаюсь запомнить все\n",r"свои записи.$"),
"ViridianCity_School_Text_ReadBlackboardCarefully": B(r"Хорошо!\p",r"Обязательно внимательно прочитай,\n",r"что написано на доске!$"),
"ViridianCity_School_Text_NotebookFirstPage": B(r"Посмотрим тетрадь.\p",r"Первая страница...\p",r"ПОКЕБОЛЫ используют, чтобы\n",r"ловить ПОКЕМОНОВ.\p",r"В команде можно носить до шести\n",r"ПОКЕМОНОВ.\p",r"Тех, кто растит ПОКЕМОНОВ и\n",r"сражается ими, зовут ТРЕНЕРАМИ.$"),
"ViridianCity_School_Text_NotebookSecondPage": B(r"Вторая страница...\p",r"Здорового ПОКЕМОНА поймать трудно,\n",r"поэтому сначала ослабь его.\p",r"Яд, ожог или другой статус\n",r"помогут его ослабить.$"),
"ViridianCity_School_Text_NotebookThirdPage": B(r"Третья страница...\p",r"ТРЕНЕРЫ ПОКЕМОНОВ ищут других,\n",r"чтобы сразиться с ними.\p",r"Для ТРЕНЕРА вкус победы\n",r"особенно сладок.\p",r"В ПОКЕМОН-ГИМАХ повсюду\n",r"постоянно идут бои.$"),
"ViridianCity_School_Text_NotebookFourthPage": B(r"Четвертая страница...\p",r"Главная цель каждого ТРЕНЕРА\n",r"ПОКЕМОНОВ проста.\p",r"Победить восемь сильнейших\n",r"ЛИДЕРОВ ПОКЕМОН-ГИМОВ.\p",r"Тогда получишь право встретиться...\p",r"с ЭЛИТНОЙ ЧЕТВЕРКОЙ\n",r"ЛИГИ ПОКЕМОНОВ!$"),
"ViridianCity_School_Text_TurnThePage": B(r"Перевернуть страницу?$"),
"ViridianCity_School_Text_HeyDontLookAtMyNotes": B(r"ДЕВОЧКА: Эй!\n",r"Не смотри мои записи!$"),
"ViridianCity_School_Text_BlackboardListsStatusProblems": B(r"На доске перечислены статусные\n",r"проблемы ПОКЕМОНОВ в бою.$"),
"ViridianCity_School_Text_ReadWhichTopic": B(r"Какую тему хочешь прочитать?$"),
"ViridianCity_School_Text_ExplainSleep": B(r"Спящий ПОКЕМОН не может\n",r"атаковать.\p",r"Сон сохраняется даже после боя.\p",r"Используй ПРОБУЖДЕНИЕ,\n",r"чтобы разбудить ПОКЕМОНА.$"),
"ViridianCity_School_Text_ExplainBurn": B(r"Ожог снижает силу АТАКИ\n",r"и постепенно отнимает HP.\p",r"Ожог остается после боя.\n",r"Используй ЛЕЧЕНИЕ ОЖОГА.$"),
"ViridianCity_School_Text_ExplainPoison": B(r"При отравлении здоровье ПОКЕМОНА\n",r"постепенно уменьшается.\p",r"Яд остается после боя.\n",r"Используй ПРОТИВОЯДИЕ!$"),
"ViridianCity_School_Text_ExplainFreeze": B(r"Замороженный ПОКЕМОН не может\n",r"двигаться.\p",r"Он остается замороженным после боя.\p",r"Используй ЛЕЧЕНИЕ ЛЬДА,\n",r"чтобы отогреть ПОКЕМОНА.$"),
"ViridianCity_School_Text_ExplainParalysis": B(r"Паралич снижает СКОРОСТЬ и может\n",r"помешать ПОКЕМОНУ двигаться.\p",r"Паралич остается после боя.\n",r"Используй ЛЕЧЕНИЕ ПАРАЛИЧА.$"),
}),
"data/maps/ViridianCity_PokemonCenter_1F_Frlg/scripts.inc": ("eb57a4cc12ab8a60ee57972558b1163656091bdf", {
"ViridianCity_PokemonCenter_1F_Text_FeelFreeToUsePC": B(r"Можешь свободно пользоваться ПК\n",r"в углу.\p",r"Так сказала медсестра.\n",r"Очень мило с ее стороны!$"),
"ViridianCity_PokemonCenter_1F_Text_PokeCenterInEveryTown": B(r"В каждом городе впереди есть\n",r"ПОКЕМОН-ЦЕНТР.\p",r"Лечение бесплатное, так что\n",r"смело лечи своих ПОКЕМОНОВ.$"),
"ViridianCity_PokemonCenter_1F_Text_PokeCentersHealMons": B(r"ПОКЕМОН-ЦЕНТРЫ лечат уставших,\n",r"раненых и потерявших сознание.\p",r"Здесь ПОКЕМОНЫ полностью\n",r"восстанавливают здоровье.$"),
}),
"data/maps/Route2_ViridianForest_SouthEntrance_Frlg/scripts.inc": ("6df492b7eaa3f0a026c45fe6e8270a3ac60a0271", {
"Route2_ViridianForest_SouthEntrance_Text_ForestIsMaze": B(r"Идешь в ВИРИДИАНСКИЙ ЛЕС?\n",r"Там настоящий природный лабиринт.\l",r"Смотри не заблудись.$"),
"Route2_ViridianForest_SouthEntrance_Text_RattataHasWickedBite": B(r"RATTATA мал, но не стоит\n",r"недооценивать его укус.\p",r"Ты уже поймал одного?$"),
}),
"data/maps/Route2_ViridianForest_NorthEntrance_Frlg/scripts.inc": ("1778637c8d6238c3019f2f8ea8212b1d46ae906b", {
"Route2_ViridianForest_NorthEntrance_Text_ManyMonsOnlyInForests": B(r"Многие ПОКЕМОНЫ живут только\n",r"в лесах и пещерах.\p",r"Будь настойчив и ищи повсюду,\n",r"чтобы находить разные виды.$"),
"Route2_ViridianForest_NorthEntrance_Text_CanCutSkinnyTrees": B(r"Замечал тонкие деревья у дороги?\p",r"Говорят, их можно срубить\n",r"особой атакой ПОКЕМОНА.$"),
"Route2_ViridianForest_NorthEntrance_Text_CanCancelEvolution": B(r"Знаешь, как отменить эволюцию?\p",r"Когда ПОКЕМОН эволюционирует,\n",r"процесс можно остановить.\p",r"Так можно растить ПОКЕМОНА,\n",r"не меняя его форму.$"),
}),
"data/maps/Route2_House_Frlg/scripts.inc": ("d3aab6eb4777e4963cfe24e9d33e21bd03c60469", {
"Route2_House_Text_FaintedMonsCanUseFieldMoves": B(r"ПОКЕМОН без сознания лишь не может\n",r"продолжать бой.\p",r"Вне боя он все еще может\n",r"использовать атаки вроде CUT.$"),
}),
"data/maps/Route2_EastBuilding_Frlg/scripts.inc": ("eed59e03fb00a397e4c6be6b176d1e7244eb4fbf", {
"Route2_EastBuilding_Text_GiveHM05IfSeen10Mons": B(r"Привет! Помнишь меня?\n",r"Я один из помощников PROF. OAK.\p",r"Если в ПОКЕДЕКСЕ есть данные\n",r"о десяти видах, я должен\l",r"дать тебе награду.\p",r"PROF. OAK доверил мне HM05.\p",r"Итак, {PLAYER}, скажи:\p",r"у тебя есть данные хотя бы\n",r"о десяти видах ПОКЕМОНОВ?$"),
"Route2_EastBuilding_Text_GreatHereYouGo": B(r"Отлично! У тебя есть данные\n",r"о {STR_VAR_3} видах ПОКЕМОНОВ!\p",r"Поздравляю!\n",r"Держи!$"),
"Route2_EastBuilding_Text_ReceivedHM05FromAide": B(r"{PLAYER} получает HM05\n",r"от ПОМОЩНИКА.$"),
"Route2_EastBuilding_Text_ExplainHM05": B(r"В HM05 находится скрытая атака\n",r"FLASH.\p",r"FLASH освещает даже самые темные\n",r"пещеры и подземелья.$"),
"Route2_EastBuilding_Text_CanGetThroughRockTunnel": B(r"Когда ПОКЕМОН выучит FLASH,\n",r"ты сможешь пройти ROCK TUNNEL.$"),
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
    ns = {"__name__":"qarro_ru_early_kanto_v315_base","__file__":str(Path(__file__).resolve())}
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
        print(f"[ru-early-v316] {rel}: {len(blocks)}/{len(blocks)} blocks changed")
    expected_new = sum(len(v[1]) for v in FILES.values())
    if expected_new != 33 or changed_total != expected_new:
        raise RuntimeError(f"Viridian/Route2 scope drift: expected 33, got {expected_new}/{changed_total}")
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + expected_new,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun",0)) + changed_total,
        "viridianAccessibleInteriorsLocalized": True,
        "route2BuildingsAndForestGatesLocalized": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {expected_new} interior/gate blocks = {BASE_COUNT + expected_new}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
