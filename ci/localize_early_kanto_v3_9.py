#!/usr/bin/env python3
"""Qarro v3.18: localize the next verified English Kanto gap, Route 4.

Runs CI-green v3.17 first, then patches only pinned FireRed Route 4 text.
Pokemon species and Move/Ability proper names stay English. Gameplay, trainer
data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "7dc141cba2912d46df59cdc82835a469620052f3"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_17"
BASE_COUNT = 250
MARKER = "QARRO_RU_EARLY_KANTO_V3_18"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
ROUTE4_REL = Path("data/maps/Route4_Frlg/scripts.inc")
# Route4 is intentionally modified by content_pass_v3_1.py before localization.
# Guard the exact deterministic post-content-pass source state seen by this step.
ROUTE4_BLOB = "e5e8ecc7c88aac5a4a4838651c021158e098c714"

def B(*lines: str) -> tuple[str, ...]: return lines

BLOCKS = {
    "Route4_Text_TrippedOverGeodude": B(r"Ай! Я споткнулась о каменного\n", r"ПОКЕМОНА GEODUDE!$"),
    "Route4_Text_CrissyIntro": B(r"Я пришла на MT. MOON искать\n", r"грибных ПОКЕМОНОВ.$"),
    "Route4_Text_CrissyDefeat": B(r"А я так старалась их поймать!$"),
    "Route4_Text_CrissyPostBattle": B(r"Похоже, грибов здесь больше\n", r"не осталось.\p", r"Кажется, я поймала их всех.$"),
    "Route4_Text_MtMoonEntrance": B(r"MT. MOON\n", r"Вход в туннель$"),
    "Route4_Text_RouteSign": B(r"МАРШРУТ 4\n", r"MT. MOON - CERULEAN CITY$"),
    "Text_MegaPunchTeach": B(r"Удар сокрушительной мощи!\p", r"В нем заключена разрушительная сила!\p", r"Когда выбора не остается,\n", r"MEGA PUNCH - лучшая атака!\l", r"Согласен?\p", r"Тогда вперед!\n", r"Я научу ей твоего ПОКЕМОНА!$"),
    "Text_MegaPunchDeclined": B(r"Ты еще вернешься, когда поймешь\n", r"ценность MEGA PUNCH.$"),
    "Text_MegaPunchWhichMon": B(r"Отлично!\n", r"Какой ПОКЕМОН выучит ее?$"),
    "Text_MegaPunchTaught": B(r"Теперь мы товарищи по искусству\n", r"удара!\p", r"Лучше уходи, пока тебя не увидел\n", r"тот заблудший глупец, который\l", r"тренирует только удары ногами.$"),
    "Text_MegaKickTeach": B(r"Удар ногой бешеной силы!\p", r"В нем заключена разрушительная мощь!\p", r"Если говорить начистоту,\n", r"MEGA KICK - лучшая атака!\l", r"Разве не так?\p", r"Хорошо!\n", r"Я научу ей твоего ПОКЕМОНА!$"),
    "Text_MegaKickDeclined": B(r"Ты еще приползешь обратно, когда\n", r"поймешь ценность MEGA KICK.$"),
    "Text_MegaKickWhichMon": B(r"Ладно!\n", r"Какой ПОКЕМОН хочет ее выучить?$"),
    "Text_MegaKickTaught": B(r"Теперь мы родственные души в\n", r"искусстве удара ногой!\p", r"Лучше беги, пока тебя не увидел\n", r"тот заблудший болван, который\l", r"тренирует только удары руками.$"),
    "Route4_Text_PeopleLikeAndRespectBrock": B(r"Ого, это же BOULDERBADGE!\n", r"Ты получил его у BROCK, верно?\p", r"BROCK крут. Он не только силен.\n", r"Его любят и уважают.\p", r"Я тоже хочу стать GYM LEADER,\n", r"как он.$"),
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
    ns = {"__name__": "qarro_ru_early_kanto_v317_base", "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc:
        return rc

    root = Path(sys.argv[1]).resolve()
    audit_path = root / AUDIT_REL
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != BASE_MARKER or int(audit.get("selectedBlocksLocalized", -1)) != BASE_COUNT:
        raise RuntimeError(f"base localization audit drift: {audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}")

    path = root / ROUTE4_REL
    actual = subprocess.check_output(["git", "-C", str(root), "hash-object", str(path)], text=True).strip()
    if actual != ROUTE4_BLOB:
        raise RuntimeError(f"{ROUTE4_REL}: post-content source blob drift: {actual} != {ROUTE4_BLOB}")
    text = path.read_text(encoding="utf-8")
    for label, lines in BLOCKS.items():
        text = patch_label(text, label, lines)
    path.write_text(text, encoding="utf-8")

    changed = len(BLOCKS)
    if changed != 15:
        raise RuntimeError(f"Route 4 scope drift: expected 15 blocks, got {changed}")
    audit.setdefault("files", {})[str(ROUTE4_REL)] = {
        "selectedBlocks": changed,
        "changedThisRun": changed,
        "sourceBlob": ROUTE4_BLOB,
    }
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + changed,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun", 0)) + changed,
        "route4Localized": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {changed} Route 4 blocks = {BASE_COUNT + changed}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
