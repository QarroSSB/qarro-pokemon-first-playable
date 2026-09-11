#!/usr/bin/env python3
"""Qarro v3.25: complete Cerulean City exterior localization.

Runs CI-green v3.24 first, then localizes the remaining NPC, Slowbro and sign
text in CeruleanCity_Frlg/scripts.inc. Pokemon species, Move and Ability
proper names stay English. Gameplay, trainer data, Ash Bond and Ash Cap are
not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "0666b350ee7de6ef9e5634b69f08a8506a279004"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_24"
BASE_COUNT = 375
MARKER = "QARRO_RU_EARLY_KANTO_V3_25"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
REL = Path("data/maps/CeruleanCity_Frlg/scripts.inc")
SOURCE_BLOB = "dae271fa54770716838b62d66b3b78a4fc785fbc"

def B(*lines: str) -> tuple[str, ...]: return lines

BLOCKS = {
"CeruleanCity_Text_TrainerLifeIsToughIsntIt": B(
    r"Ты тоже TRAINER?\p",
    r"Ловить, сражаться...\n",
    r"Нелегкая жизнь, правда?$"),
"CeruleanCity_Text_YouCanCutDownSmallTrees": B(
    r"Ты знаешь, что маленькие деревья\n",
    r"можно срубать приемом CUT?\p",
    r"Даже то маленькое дерево перед\n",
    r"магазином можно срубить CUT.\p",
    r"Хотя, думаю, его можно как-то\n",
    r"обойти.$"),
"CeruleanCity_Text_IfSlowbroWasntThereCouldCutTree": B(
    r"Если бы там не стоял SLOWBRO,\n",
    r"можно было бы срубить дерево CUT.\p",
    r"Так можно было бы попасть\n",
    r"на другую сторону.\p",
    r"Хотя, думаю, его можно как-то\n",
    r"обойти.$"),
"CeruleanCity_Text_PokemonEncyclopediaAmusing": B(
    r"Ты составляешь энциклопедию\n",
    r"POKéMON? Звучит занятно.$"),
"CeruleanCity_Text_PeopleHereWereRobbed": B(
    r"Людей в этом доме ограбили.\p",
    r"Очевидно, за этим ужасным\n",
    r"преступлением стоит TEAM ROCKET!\p",
    r"Даже нашей полиции трудно\n",
    r"справиться с ROCKETS!$"),
"CeruleanCity_Text_SlowbroUseSonicboom": B(
    r"Ладно, SLOWBRO!\n",
    r"Используй SONICBOOM!$"),
"CeruleanCity_Text_SlowbroPayAttention": B(
    r"Ну же, SLOWBRO, внимательнее!$"),
"CeruleanCity_Text_SlowbroPunch": B(
    r"SLOWBRO, бей!$"),
"CeruleanCity_Text_NoYouBlewItAgain": B(
    r"Нет!\n",
    r"Ты опять все испортил!$"),
"CeruleanCity_Text_SlowbroWithdraw": B(
    r"SLOWBRO, используй WITHDRAW!$"),
"CeruleanCity_Text_HardToControlMonsObedience": B(
    r"Нет! Не так!\n",
    r"Как же трудно управлять POKéMON!\p",
    r"Послушание твоих POKéMON зависит\n",
    r"от твоих навыков TRAINER.$"),
"CeruleanCity_Text_SlowbroTookSnooze": B(
    r"SLOWBRO задремал...$"),
"CeruleanCity_Text_SlowbroLoafingAround": B(
    r"SLOWBRO бездельничает...$"),
"CeruleanCity_Text_SlowbroTurnedAway": B(
    r"SLOWBRO отвернулся...$"),
"CeruleanCity_Text_SlowbroIgnoredOrders": B(
    r"SLOWBRO проигнорировал приказ...$"),
"CeruleanCity_Text_WantBrightRedBicycle": B(
    r"Я хочу ярко-красный велосипед.\p",
    r"Буду держать его дома, чтобы\n",
    r"он не испачкался.$"),
"CeruleanCity_Text_ThisIsCeruleanCave": B(
    r"Это CERULEAN CAVE.\p",
    r"Внутри живут невероятно сильные\n",
    r"POKéMON.\p",
    r"Войти туда разрешают только\n",
    r"особенным TRAINER.\p",
    r"Для начала нужно быть достаточно\n",
    r"сильным, чтобы стать CHAMPION\l",
    r"POKéMON LEAGUE.\p",
    r"И кроме того, нужно совершить\n",
    r"по-настоящему великое достижение.$"),
"CeruleanCity_Text_CitySign": B(
    r"CERULEAN CITY\n",
    r"Город, окруженный таинственной\l",
    r"голубой аурой$"),
"CeruleanCity_Text_TrainerTipsHeldItems": B(
    r"СОВЕТЫ TRAINER\p",
    r"POKéMON может держать предмет.\p",
    r"Некоторые предметы POKéMON даже\n",
    r"может использовать в бою.$"),
"CeruleanCity_Text_BikeShopSign": B(
    r"По траве и пещерам - без проблем!\n",
    r"МАГАЗИН ВЕЛОСИПЕДОВ$"),
"CeruleanCity_Text_GymSign": B(
    r"CERULEAN CITY POKéMON GYM\n",
    r"LEADER: MISTY\l",
    r"Русалка-сорванец!$"),
}

def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT], check=True)
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"], text=True)

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
        print(f"usage: {Path(sys.argv[0]).name} <pokeemerald-expansion-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    actual = subprocess.check_output(["git", "-C", str(root), "hash-object", str(path)], text=True).strip()
    if actual != SOURCE_BLOB:
        raise RuntimeError(f"{REL}: pinned source blob drift before base pass: {actual} != {SOURCE_BLOB}")

    code = load_base()
    ns = {"__name__": "qarro_ru_early_kanto_v324_base", "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc:
        return rc

    audit_path = root / AUDIT_REL
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != BASE_MARKER or int(audit.get("selectedBlocksLocalized", -1)) != BASE_COUNT:
        raise RuntimeError(f"base localization audit drift: {audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}")

    text = path.read_text(encoding="utf-8")
    for label, lines in BLOCKS.items():
        text = patch_label(text, label, lines)
    path.write_text(text, encoding="utf-8")

    changed = len(BLOCKS)
    if changed != 21:
        raise RuntimeError(f"Cerulean City remainder scope drift: expected 21 blocks, got {changed}")
    previous = audit.get("files", {}).get(str(REL), {})
    audit.setdefault("files", {})[str(REL)] = {
        "selectedBlocks": int(previous.get("selectedBlocks", 0)) + changed,
        "changedThisRun": changed,
        "sourceBlob": SOURCE_BLOB,
    }
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + changed,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun", 0)) + changed,
        "ceruleanCityExteriorComplete": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {changed} Cerulean City remainder blocks = {BASE_COUNT + changed}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
