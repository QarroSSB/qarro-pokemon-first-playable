#!/usr/bin/env python3
"""Qarro v3.24: start Cerulean City exterior localization.

Runs CI-green v3.23 first, then localizes the rival and Team Rocket story
sequence in CeruleanCity_Frlg/scripts.inc. Pokemon species, Move and Ability
proper names stay English. Gameplay, trainer data, Ash Bond and Ash Cap are
not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "28fd5e05d596f4db06b03728b0c6eb6a3f5d52bd"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_23"
BASE_COUNT = 364
MARKER = "QARRO_RU_EARLY_KANTO_V3_24"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
REL = Path("data/maps/CeruleanCity_Frlg/scripts.inc")
SOURCE_BLOB = "dae271fa54770716838b62d66b3b78a4fc785fbc"

def B(*lines: str) -> tuple[str, ...]: return lines

BLOCKS = {
"CeruleanCity_Text_RivalIntro": B(
    r"{RIVAL}: Эй, {PLAYER}!\p",
    r"Ты все еще плетешься где-то\n",
    r"позади?\p",
    r"А у меня все отлично! Я поймал\n",
    r"кучу сильных и умных POKéMON!\p",
    r"Ну-ка покажи, кого поймал ты,\n",
    r"{PLAYER}!$"),
"CeruleanCity_Text_RivalDefeat": B(
    r"Эй!\n",
    r"Полегче!\l",
    r"Ты уже победил!$"),
"CeruleanCity_Text_RivalPostBattle": B(
    r"{RIVAL}: Эй, знаешь что?\p",
    r"Я был у BILL, и он показал мне\n",
    r"своих редких POKéMON.\p",
    r"Мой POKéDEX сразу пополнился\n",
    r"множеством новых страниц!\p",
    r"Все-таки BILL известен во всем\n",
    r"мире как настоящий POKéMANIAC.\p",
    r"Он еще и создал систему хранения\n",
    r"POKéMON на PC.\p",
    r"Раз уж ты пользуешься его системой,\n",
    r"стоит сходить и поблагодарить его.\p",
    r"Ладно, мне пора!\n",
    r"Еще увидимся!$"),
"CeruleanCity_Text_OhRightLittlePresentAsFavor": B(
    r"А, да, точно.\p",
    r"Мне тебя даже жаль. Серьезно.\n",
    r"Ты вечно отстаешь от меня.\p",
    r"Так что держи небольшой подарок\n",
    r"от меня.$"),
"CeruleanCity_Text_ExplainFameCheckerSmellYa": B(
    r"Для такого любителя болтать, как ты,\n",
    r"эта штука подойдет идеально.\p",
    r"Мне она не нужна - чужие дела\n",
    r"меня вообще не волнуют.\p",
    r"Ладно, теперь я правда ухожу.\n",
    r"Увидимся!$"),
"CeruleanCity_Text_GruntIntro": B(
    r"Эй! Не лезь сюда!\n",
    r"Это не твой двор!\p",
    r"...А?\n",
    r"Я?\p",
    r"Я просто невинный прохожий!\n",
    r"Не веришь?{PLAY_BGM}{MUS_RG_ENCOUNTER_ROCKET}$"),
"CeruleanCity_Text_GruntDefeat": B(
    r"GRUNT: Стой! Я сдаюсь!\n",
    r"Я уйду без шума!$"),
"CeruleanCity_Text_OkayIllReturnStolenTM": B(
    r"Ладно! Верну украденный TM!$"),
"CeruleanCity_Text_RecoveredTM28FromGrunt": B(
    r"{PLAYER} вернул TM28 у GRUNT.$"),
"CeruleanCity_Text_BetterGetMovingBye": B(
    r"Мне лучше убираться отсюда!\n",
    r"Пока!$"),
"CeruleanCity_Text_MakeRoomForThisCantRun": B(
    r"Освободи место для этого!\n",
    r"Мне некуда бежать!$"),
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
    code = load_base()
    ns = {"__name__": "qarro_ru_early_kanto_v323_base", "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc:
        return rc

    root = Path(sys.argv[1]).resolve()
    audit_path = root / AUDIT_REL
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != BASE_MARKER or int(audit.get("selectedBlocksLocalized", -1)) != BASE_COUNT:
        raise RuntimeError(f"base localization audit drift: {audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}")

    path = root / REL
    actual = subprocess.check_output(["git", "-C", str(root), "hash-object", str(path)], text=True).strip()
    if actual != SOURCE_BLOB:
        raise RuntimeError(f"{REL}: pinned source blob drift: {actual} != {SOURCE_BLOB}")
    text = path.read_text(encoding="utf-8")
    for label, lines in BLOCKS.items():
        text = patch_label(text, label, lines)
    path.write_text(text, encoding="utf-8")

    changed = len(BLOCKS)
    if changed != 11:
        raise RuntimeError(f"Cerulean City story scope drift: expected 11 blocks, got {changed}")
    audit.setdefault("files", {})[str(REL)] = {"selectedBlocks": changed, "changedThisRun": changed, "sourceBlob": SOURCE_BLOB}
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + changed,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun", 0)) + changed,
        "ceruleanCityStoryLocalized": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {changed} Cerulean City story blocks = {BASE_COUNT + changed}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
