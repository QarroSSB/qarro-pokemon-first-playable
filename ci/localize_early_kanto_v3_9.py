#!/usr/bin/env python3
"""Qarro v3.22: localize Route 24 / Nugget Bridge.

Runs CI-green v3.21 first, then localizes all remaining user-facing FireRed
text blocks in Route24_Frlg/scripts.inc. Pokemon species, Move and Ability
proper names stay English. Gameplay, trainer data, Ash Bond and Ash Cap are
not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "d11d26d9b9c17f51c92b1426bbf84d336166eb17"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_21"
BASE_COUNT = 310
MARKER = "QARRO_RU_EARLY_KANTO_V3_22"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
REL = Path("data/maps/Route24_Frlg/scripts.inc")
SOURCE_BLOB = "75686a2a7f42498deda79f2dd8c776d1ac017c8f"

def B(*lines: str) -> tuple[str, ...]: return lines

BLOCKS = {
"Route24_Text_JustEarnedFabulousPrize": B(
    r"Поздравляем! Ты победил всех\n",
    r"пятерых ТРЕНЕРОВ!\p",
    r"Ты заслужил отличный приз!$"),
"Route24_Text_ReceivedNuggetFromMysteryTrainer": B(
    r"{PLAYER} получил САМОРОДОК\n",
    r"от таинственного ТРЕНЕРА!$"),
"Route24_Text_YouDontHaveAnyRoom": B(
    r"У тебя нет свободного места!$"),
"Route24_Text_JoinTeamRocket": B(
    r"Кстати, не хочешь вступить\n",
    r"в КОМАНДУ R?\p",
    r"Мы профессиональные преступники,\n",
    r"и наша специализация — ПОКЕМОНЫ!\p",
    r"Хочешь к нам?\p",
    r"Точно не хочешь?\p",
    r"Ну же, вступай!\p",
    r"Я говорю: вступай!\p",
    r"…Ладно, тебя надо убедить!\p",
    r"Сделаю предложение, от которого\n",
    r"ты не сможешь отказаться!$"),
"Route24_Text_RocketDefeat": B(
    r"Арргх!\n",
    r"А ты хорош!$"),
"Route24_Text_YoudBecomeTopRocketLeader": B(
    r"С твоими способностями ты стал бы\n",
    r"лучшим лидером КОМАНДЫ R.\p",
    r"Подумай, какая возможность!\n",
    r"Не упускай такой шанс.$"),
"Route24_Text_ShaneIntro": B(
    r"Я видел твой подвиг из травы!$"),
"Route24_Text_ShaneDefeat": B(
    r"Я так и думал!$"),
"Route24_Text_ShanePostBattle": B(
    r"Я спрятался, потому что люди\n",
    r"на мосту меня напугали.$"),
"Route24_Text_EthanIntro": B(
    r"Так! Я номер 5!\n",
    r"Я тебя растопчу!$"),
"Route24_Text_EthanDefeat": B(
    r"Ого!\n",
    r"Это слишком!$"),
"Route24_Text_EthanPostBattle": B(
    r"Я сделал всё, что мог. Без сожалений!$"),
"Route24_Text_ReliIntro": B(
    r"Я номер 4!\n",
    r"Уже устал?$"),
"Route24_Text_ReliDefeat": B(
    r"Я тоже проиграл!$"),
"Route24_Text_ReliPostBattle": B(
    r"Я сделал всё, что мог. Без сожалений!$"),
"Route24_Text_TimmyIntro": B(
    r"А вот и номер 3!\n",
    r"Со мной будет непросто!$"),
"Route24_Text_TimmyDefeat": B(
    r"Ай!\n",
    r"Раздавил в лепёшку!$"),
"Route24_Text_TimmyPostBattle": B(
    r"Я сделал всё, что мог. Без сожалений!$"),
"Route24_Text_AliIntro": B(
    r"Я второй!\n",
    r"Теперь всё серьёзно!$"),
"Route24_Text_AliDefeat": B(
    r"Как я мог проиграть?$"),
"Route24_Text_AliPostBattle": B(
    r"Я сделал всё, что мог. Без сожалений!$"),
"Route24_Text_CaleIntro": B(
    r"Это место зовут МОСТОМ\n",
    r"САМОРОДКА!\p",
    r"Победи пятерых ТРЕНЕРОВ\n",
    r"и получи отличный приз!\p",
    r"Думаешь, справишься?$"),
"Route24_Text_CaleDefeat": B(
    r"Ух!\n",
    r"Отлично!$"),
"Route24_Text_CalePostBattle": B(
    r"Я сделал всё, что мог. Без сожалений!$"),
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
    ns = {"__name__": "qarro_ru_early_kanto_v321_base", "__file__": str(Path(__file__).resolve())}
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
    if changed != 24:
        raise RuntimeError(f"Route 24 scope drift: expected 24 blocks, got {changed}")
    audit.setdefault("files", {})[str(REL)] = {"selectedBlocks": changed, "changedThisRun": changed, "sourceBlob": SOURCE_BLOB}
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + changed,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun", 0)) + changed,
        "route24NuggetBridgeLocalized": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {changed} Route 24 blocks = {BASE_COUNT + changed}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
