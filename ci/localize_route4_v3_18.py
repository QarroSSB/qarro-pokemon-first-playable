#!/usr/bin/env python3
"""Qarro v3.18: localize the next verified English Kanto gap, Route 4.

Runs after the CI-green v3.17 early-Kanto localization. The pinned Route 4
script blob must still match Expansion 1.17.0 exactly before editing. Pokemon
species and Move/Ability proper names stay English. Gameplay, trainer data,
Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

PINNED_BLOB = "c93e60ba5443fc44fdc8a6371e5d0b1311442be5"
REL = Path("data/maps/Route4_Frlg/scripts.inc")
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
PREVIOUS_MARKER = "QARRO_RU_EARLY_KANTO_V3_17"
PREVIOUS_COUNT = 250
MARKER = "QARRO_RU_EARLY_KANTO_V3_18"

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
    target = root / REL
    if not target.is_file():
        raise RuntimeError(f"missing pinned Route 4 source: {target}")
    blob = subprocess.check_output(["git", "-C", str(root), "hash-object", str(REL)], text=True).strip()
    if blob != PINNED_BLOB:
        raise RuntimeError(f"Route 4 blob drift: expected {PINNED_BLOB}, got {blob}")
    text = target.read_text(encoding="utf-8")
    changed = 0
    for label, lines in BLOCKS.items():
        text = patch_label(text, label, lines)
        changed += 1
    if changed != 15:
        raise RuntimeError(f"Route 4 scope drift: expected 15 blocks, got {changed}")
    target.write_text(text, encoding="utf-8")

    audit_path = root / AUDIT_REL
    if not audit_path.is_file():
        raise RuntimeError(f"missing early-Kanto audit: {audit_path}")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != PREVIOUS_MARKER:
        raise RuntimeError(f"unexpected previous localization marker: {audit.get('marker')!r}")
    if int(audit.get("selectedBlocksLocalized", -1)) != PREVIOUS_COUNT:
        raise RuntimeError(f"unexpected previous localization count: {audit.get('selectedBlocksLocalized')!r}")
    audit.update({
        "previousMarker": PREVIOUS_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": PREVIOUS_COUNT + changed,
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
    print(f"[{MARKER}] PASS: Route 4 localized, {changed} blocks; total {PREVIOUS_COUNT + changed}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
