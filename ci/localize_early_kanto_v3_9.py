#!/usr/bin/env python3
"""Qarro v3.20: localize Route 22 rival encounters and League gate sign.

Runs CI-green v3.19 first, then localizes all 9 user-facing FireRed text
blocks in Route22_Frlg/scripts.inc, including the two upstream Japanese-only
rival blocks. Pokemon species, Move and Ability proper names stay English.
Gameplay, trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "403027433672a86992b73ed0a919f3157c2a430d"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_19"
BASE_COUNT = 300
MARKER = "QARRO_RU_EARLY_KANTO_V3_20"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
REL = Path("data/maps/Route22_Frlg/scripts.inc")
SOURCE_BLOB = "0497ab4dccbcd21feee5d5ab90ef2baef0ff0625"

def B(*lines: str) -> tuple[str, ...]: return lines

BLOCKS = {
"Route22_Text_EarlyRivalIntro": B(
    r"{RIVAL}: Эй, {PLAYER}!\p",
    r"Ты идешь в ЛИГУ ПОКЕМОНОВ?\n",
    r"Даже не мечтай!\p",
    r"У тебя ведь наверняка нет\n",
    r"ни одного ЗНАЧКА, да?\p",
    r"Без них охранник тебя\n",
    r"не пропустит.\p",
    r"Кстати, твои ПОКЕМОНЫ стали\n",
    r"сильнее?$"),
"Route22_Text_EarlyRivalDefeat": B(
    r"О-ох!\n", r"Тебе просто повезло!$"),
"Route22_Text_EarlyRivalPostBattle": B(
    r"Я слышал, в ЛИГЕ ПОКЕМОНОВ\n",
    r"полно сильных ТРЕНЕРОВ.\p",
    r"Мне надо придумать, как их\n",
    r"одолеть.\p",
    r"А ты хватит копаться -\n",
    r"пора двигаться дальше!$"),
"Route22_Text_RivalShouldCatchSomeMons": B(
    r"{RIVAL}: Что? Почему у меня\n",
    r"два ПОКЕМОНА?\p",
    r"Так и ты поймай себе\n",
    r"еще!$"),
"Route22_Text_LateRivalIntro": B(
    r"{RIVAL}: Что? {PLAYER}!\n",
    r"Вот уж не ожидал тебя здесь!\p",
    r"Так ты идешь в ЛИГУ\n",
    r"ПОКЕМОНОВ?\p",
    r"И все ЗНАЧКИ уже собрал?\n",
    r"Неплохо!\p",
    r"Тогда я разомнусь на тебе,\n",
    r"{PLAYER}, перед ЛИГОЙ ПОКЕМОНОВ!\p",
    r"Давай!$"),
"Route22_Text_LateRivalDefeat": B(
    r"Что!?\p", r"Я просто был неосторожен!$"),
"Route22_Text_LateRivalPostBattle": B(
    r"Вот теперь я размялся.\n",
    r"Я готов к ЛИГЕ ПОКЕМОНОВ!\p",
    r"{PLAYER}, тебе надо еще\n",
    r"потренироваться.\p",
    r"Хотя ты и сам это знаешь!\n",
    r"Я пошел. Бывай!$"),
"Route22_Text_LateRivalVictory": B(
    r"{RIVAL}: Ха-ха! {PLAYER}!\n",
    r"И это все, на что ты способен?\l",
    r"До моего уровня тебе\l",
    r"еще далеко!\p",
    r"Иди потренируйся еще!\n",
    r"Ха-ха-ха!$"),
"Route22_Text_LeagueGateSign": B(
    r"ЛИГА ПОКЕМОНОВ\n", r"ГЛАВНЫЕ ВОРОТА$"),
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
    ns = {"__name__": "qarro_ru_early_kanto_v319_base", "__file__": str(Path(__file__).resolve())}
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
    if changed != 9:
        raise RuntimeError(f"Route 22 scope drift: expected 9 blocks, got {changed}")
    audit.setdefault("files", {})[str(REL)] = {"selectedBlocks": changed, "changedThisRun": changed, "sourceBlob": SOURCE_BLOB}
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + changed,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun", 0)) + changed,
        "route22Localized": True,
        "route22JapaneseOnlyBlocksLocalized": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {changed} Route 22 blocks = {BASE_COUNT + changed}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
