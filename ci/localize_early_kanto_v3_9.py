#!/usr/bin/env python3
"""Qarro v3.23: localize Route 25.

Runs CI-green v3.22 first, then localizes all remaining user-facing FireRed
text blocks in Route25_Frlg/scripts.inc. Pokemon species, Move and Ability
proper names stay English. Gameplay, trainer data, Ash Bond and Ash Cap are
not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "d4c4a8de52cde2f5cdb53d36ce1159f4e654562e"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_22"
BASE_COUNT = 334
MARKER = "QARRO_RU_EARLY_KANTO_V3_23"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
REL = Path("data/maps/Route25_Frlg/scripts.inc")
SOURCE_BLOB = "a16819121433c92dca1dd8efecb6d4cfec85e620"

def B(*lines: str) -> tuple[str, ...]: return lines

BLOCKS = {
"Route25_Text_JoeyIntro": B(
    r"Местные ТРЕНЕРЫ приходят сюда\n",
    r"тренироваться.$"),
"Route25_Text_JoeyDefeat": B(
    r"Ты неплох.$"),
"Route25_Text_JoeyPostBattle": B(
    r"У всех POKéMON есть слабости.\n",
    r"Даже у самых сильных.\p",
    r"Поэтому лучше растить POKéMON\n",
    r"разных типов.$"),
"Route25_Text_DanIntro": B(
    r"Папа водил меня на отличную\n",
    r"вечеринку на S.S. ANNE в VERMILION CITY.$"),
"Route25_Text_DanDefeat": B(
    r"Я не злюсь!$"),
"Route25_Text_DanPostBattle": B(
    r"На S.S. ANNE я видел ТРЕНЕРОВ\n",
    r"со всего мира.$"),
"Route25_Text_FlintIntro": B(
    r"Я крутой парень.\n",
    r"У меня есть девушка!$"),
"Route25_Text_FlintDefeat": B(
    r"Вот досада...$"),
"Route25_Text_FlintPostBattle": B(
    r"Ну и ладно.\n",
    r"Моя девушка меня подбодрит.$"),
"Route25_Text_KelseyIntro": B(
    r"Привет!\n",
    r"Мой парень крутой!$"),
"Route25_Text_KelseyDefeat": B(
    r"Моя форма не лучшая...$"),
"Route25_Text_KelseyPostBattle": B(
    r"Вот бы мой парень был так же\n",
    r"хорош, как ты.$"),
"Route25_Text_ChadIntro": B(
    r"У меня было предчувствие...\n",
    r"Я знал, что должен сразиться с тобой!$"),
"Route25_Text_ChadDefeat": B(
    r"Я знал, что проиграю!$"),
"Route25_Text_ChadPostBattle": B(
    r"Если твой POKéMON запутался,\n",
    r"замени его.\p",
    r"Это хорошая тактика.$"),
"Route25_Text_HaleyIntro": B(
    r"У моей подруги много милых POKéMON.\n",
    r"Я так завидую!$"),
"Route25_Text_HaleyDefeat": B(
    r"Теперь я не так завидую!$"),
"Route25_Text_HaleyPostBattle": B(
    r"Ты пришел с MT. MOON?\n",
    r"Можно мне CLEFAIRY?$"),
"Route25_Text_FranklinIntro": B(
    r"Я только что спустился с MT. MOON,\n",
    r"но сил у меня еще полно!$"),
"Route25_Text_FranklinDefeat": B(
    r"Ты отлично постарался!$"),
"Route25_Text_FranklinPostBattle": B(
    r"Черт!\n",
    r"В той пещере меня укусил ZUBAT.$"),
"Route25_Text_NobIntro": B(
    r"Я иду посмотреть коллекцию\n",
    r"POKéMANIAC на мысе.$"),
"Route25_Text_NobDefeat": B(
    r"Ты меня здорово уделал!$"),
"Route25_Text_NobPostBattle": B(
    r"POKéMANIAC полностью оправдывает\n",
    r"свое имя.\p",
    r"В его коллекции много редких\n",
    r"видов POKéMON.$"),
"Route25_Text_WayneIntro": B(
    r"Идешь к BILL?\n",
    r"Сначала сразись со мной!$"),
"Route25_Text_WayneDefeat": B(
    r"А ты хорош.$"),
"Route25_Text_WaynePostBattle": B(
    r"Тропа внизу - короткий путь\n",
    r"в CERULEAN CITY.$"),
"Route25_Text_SeaCottageSign": B(
    r"МОРСКОЙ ДОМ\n",
    r"Здесь живет BILL!$"),
"Route25_Text_MistyHighHopesAboutThisPlace": B(
    r"Этот мыс - известное место для свиданий.\p",
    r"MISTY, ЛИДЕР ЗАЛА, возлагает\n",
    r"на это место большие надежды.$"),
"Route25_Text_AreYouHereAlone": B(
    r"Привет, ты здесь один?\p",
    r"Если уж пришел на мыс CERULEAN...\n",
    r"Лучше приходить сюда вдвоем.$"),
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
    ns = {"__name__": "qarro_ru_early_kanto_v322_base", "__file__": str(Path(__file__).resolve())}
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
    if changed != 30:
        raise RuntimeError(f"Route 25 scope drift: expected 30 blocks, got {changed}")
    audit.setdefault("files", {})[str(REL)] = {"selectedBlocks": changed, "changedThisRun": changed, "sourceBlob": SOURCE_BLOB}
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + changed,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun", 0)) + changed,
        "route25Localized": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {changed} Route 25 blocks = {BASE_COUNT + changed}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
