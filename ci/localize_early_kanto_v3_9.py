#!/usr/bin/env python3
"""Qarro v3.12 early-Kanto Russian localization continuation.

Runs the exact CI-verified v3.11 pass (through Pewter Gym/Brock), then
localizes the full Route 3 text set on the pinned FireRed source. The pass is
fail-closed: every untouched English block must match exactly once.

Pokemon species, Move and Ability proper names remain English. Gameplay,
trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "bd347c3158a54679bd8280dacf0d015a0b1600ed"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_11"
MARKER = "QARRO_RU_EARLY_KANTO_V3_12"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")


def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    return subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )


PATCHES = {
    "data/maps/Route3_Frlg/scripts.inc": {
        "Route3_Text_TunnelFromCeruleanTiring": (
            (r"Whew… I better take a rest…\n", r"Groan…\p", r"That tunnel from CERULEAN takes a\n", r"lot out of you!$"),
            (r"Уф... Надо немного отдохнуть...\n", r"Ох...\p", r"Тоннель из CERULEAN здорово\n", r"выматывает!$"),
        ),
        "Route3_Text_ColtonIntro": (
            (r"Hey!\n", r"I saw you in VIRIDIAN FOREST!$"),
            (r"Эй!\n", r"Я видел тебя в VIRIDIAN FOREST!$"),
        ),
        "Route3_Text_ColtonDefeat": ((r"You beat me again!$",), (r"Ты снова меня победил!$",)),
        "Route3_Text_ColtonPostBattle": (
            (r"There are other kinds of POKéMON\n", r"than the ones you find in forests.$"),
            (r"Есть и другие виды ПОКЕМОНОВ,\n", r"не только лесные.$"),
        ),
        "Route3_Text_BenIntro": (
            (r"Hi!\n", r"I like shorts!\p", r"They're delightfully comfy and\n", r"easy to wear!$"),
            (r"Привет!\n", r"Я люблю шорты!\p", r"Они такие удобные,\n", r"и носить их легко!$"),
        ),
        "Route3_Text_BenDefeat": ((r"I don't believe it!$",), (r"Не могу поверить!$",)),
        "Route3_Text_BenPostBattle": (
            (r"Are you using a POKéMON CENTER's\n", r"PC for storing your POKéMON?\p", r"Each BOX can hold up to\n", r"30 POKéMON.$"),
            (r"Ты хранишь ПОКЕМОНОВ в ПК\n", r"ПОКЕМОН-ЦЕНТРА?\p", r"В каждом БОКСЕ помещается\n", r"до 30 ПОКЕМОНОВ.$"),
        ),
        "Route3_Text_JaniceIntro": (
            (r"Excuse me!\n", r"You looked at me, didn't you?$"),
            (r"Эй!\n", r"Ты ведь посмотрел на меня?$"),
        ),
        "Route3_Text_JaniceDefeat": ((r"You're mean!$",), (r"Ну и вредина!$",)),
        "Route3_Text_JanicePostBattle": (
            (r"You shouldn't be staring if you\n", r"don't want to battle!$"),
            (r"Не смотри на ТРЕНЕРОВ, если\n", r"не хочешь сражаться!$"),
        ),
        "Route3_Text_GregIntro": (
            (r"Are you a TRAINER?\n", r"Let's get with it right away!$"),
            (r"Ты ТРЕНЕР?\n", r"Тогда сразу к делу!$"),
        ),
        "Route3_Text_GregDefeat": (
            (r"If I had new POKéMON, I would've\n", r"won!$"),
            (r"Будь у меня новые ПОКЕМОНЫ,\n", r"я бы победил!$"),
        ),
        "Route3_Text_GregPostBattle": (
            (r"If a POKéMON BOX on the PC gets\n", r"full, just switch to another BOX.$"),
            (r"Если БОКС ПОКЕМОНОВ в ПК\n", r"заполнен, выбери другой БОКС.$"),
        ),
        "Route3_Text_SallyIntro": (
            (r"That look you gave me…\n", r"It's so intriguing!$"),
            (r"Этот твой взгляд...\n", r"Так интригует!$"),
        ),
        "Route3_Text_SallyDefeat": ((r"Be nice!$",), (r"Будь добрее!$",)),
        "Route3_Text_SallyPostBattle": (
            (r"You can avoid battles by not\n", r"letting TRAINERS see you.$"),
            (r"Можно избегать боёв, если\n", r"не попадаться ТРЕНЕРАМ на глаза.$"),
        ),
        "Route3_Text_CalvinIntro": (
            (r"Hey! You're not wearing shorts!\n", r"What's wrong with you?$"),
            (r"Эй! Ты не в шортах!\n", r"Что с тобой не так?$"),
        ),
        "Route3_Text_CalvinDefeat": (
            (r"Lost!\n", r"Lost! Lost!$"),
            (r"Проиграл!\n", r"Проиграл! Проиграл!$"),
        ),
        "Route3_Text_CalvinPostBattle": (
            (r"I always wear shorts, even in\n", r"winter. That's my policy.$"),
            (r"Я всегда ношу шорты, даже\n", r"зимой. Это мой принцип.$"),
        ),
        "Route3_Text_JamesIntro": (
            (r"I'll battle you with the POKéMON\n", r"I just caught.$"),
            (r"Я сражусь ПОКЕМОНОМ,\n", r"которого только что поймал.$"),
        ),
        "Route3_Text_JamesDefeat": ((r"Done like dinner!$",), (r"Вот и всё!$",)),
        "Route3_Text_JamesPostBattle": (
            (r"Trained POKéMON are stronger than\n", r"the wild ones.$"),
            (r"Тренированные ПОКЕМОНЫ сильнее\n", r"диких.$"),
        ),
        "Route3_Text_RobinIntro": (
            (r"Eek!\n", r"Did you touch me?$"),
            (r"Ай!\n", r"Ты меня тронул?$"),
        ),
        "Route3_Text_RobinDefeat": ((r"That's it?$",), (r"И это всё?$",)),
        "Route3_Text_RobinPostBattle": (
            (r"ROUTE 4 is at the foot of\n", r"MT. MOON.$"),
            (r"МАРШРУТ 4 находится у подножия\n", r"MT. MOON.$"),
        ),
        "Route3_Text_RouteSign": (
            (r"ROUTE 3\n", r"MT. MOON AHEAD$"),
            (r"МАРШРУТ 3\n", r"ВПЕРЕДИ MT. MOON$"),
        ),
    },
}


def render_block(label: str, lines: tuple[str, ...]) -> str:
    return label + "::\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def patch_file(path: Path, blocks: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    for label, (old_lines, new_lines) in blocks.items():
        old = render_block(label, old_lines)
        new = render_block(label, new_lines)
        old_count = text.count(old)
        new_count = text.count(new)
        if old_count == 1 and new_count == 0:
            text = text.replace(old, new, 1)
            changed += 1
        elif old_count == 0 and new_count == 1:
            continue
        else:
            raise RuntimeError(
                f"{path}: {label}: expected exactly one untouched or translated block; "
                f"old={old_count}, new={new_count}"
            )
    path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <pokeemerald-expansion-root>", file=sys.stderr)
        return 2

    code = load_base()
    ns = {
        "__name__": "qarro_ru_early_kanto_v311_base",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc:
        return rc

    root = Path(sys.argv[1]).resolve()
    audit_path = root / AUDIT_REL
    if not audit_path.is_file():
        raise RuntimeError(f"base localization audit missing: {AUDIT_REL}")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != BASE_MARKER or audit.get("selectedBlocksLocalized") != 106:
        raise RuntimeError(
            "base localization audit drift: expected marker "
            f"{BASE_MARKER!r} and 106 blocks, got "
            f"{audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}"
        )

    changed_total = 0
    for rel, blocks in PATCHES.items():
        path = root / rel
        if not path.is_file():
            raise RuntimeError(f"missing pinned source file: {rel}")
        changed = patch_file(path, blocks)
        changed_total += changed
        audit.setdefault("files", {})[rel] = {
            "selectedBlocks": len(blocks),
            "changedThisRun": changed,
        }
        print(f"[ru-early-v312] {rel}: {changed}/{len(blocks)} blocks changed")

    expected_new = 26
    if sum(len(v) for v in PATCHES.values()) != expected_new:
        raise RuntimeError("Route 3 localization scope drift")
    if changed_total != expected_new:
        raise RuntimeError(
            f"fresh pinned checkout should change all {expected_new} new blocks; got {changed_total}"
        )

    audit["previousMarker"] = BASE_MARKER
    audit["marker"] = MARKER
    audit["selectedBlocksLocalized"] = 106 + expected_new
    audit["blocksChangedThisRun"] = int(audit.get("blocksChangedThisRun", 0)) + changed_total
    audit["route3Localized"] = True
    audit["route3TrainerDialogueLocalized"] = True
    audit["route3SignLocalized"] = True
    audit["pokemonSpeciesNamesEnglish"] = True
    audit["moveNamesEnglish"] = True
    audit["abilityNamesEnglish"] = True
    audit["gameplayTouched"] = False
    audit["trainerDataTouched"] = False
    audit["ashBondTouched"] = False
    audit["ashCapTouched"] = False
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: base {BASE_MARKER} preserved; "
        f"localized {changed_total} Route 3 blocks; total={audit['selectedBlocksLocalized']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
