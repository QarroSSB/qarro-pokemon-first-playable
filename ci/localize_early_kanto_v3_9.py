#!/usr/bin/env python3
"""Qarro v3.13 early-Kanto Russian localization: finish Pallet Town exterior.

Runs the exact CI-verified v3.12 pass (through Route 3). The core localization
step already translates the starting room, downstairs home and early Pallet
Town interactions, so this pass adds only the four genuinely untranslated
Pallet Town postgame/Oak-rating text blocks. Exact source matching keeps the
pass fail-closed and avoids double-patching text already translated earlier.

Pokemon species, Move and Ability proper names remain English. Gameplay,
trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "c39a990197cf866dfde92836c041de2c630c3b89"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_12"
MARKER = "QARRO_RU_EARLY_KANTO_V3_13"
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
    "data/maps/PalletTown_Frlg/scripts.inc": {
        "PalletTown_Text_OakLetMeSeePokedex": (
            (
                r"OAK: Ah, {PLAYER}!\n",
                r"You're back, are you?\p",
                r"How much have you filled in your\n",
                r"POKéDEX?\p",
                r"May I see it?\p",
                r"Let's see…$",
            ),
            (
                r"ОУК: А, {PLAYER}!\n",
                r"Ты вернулся?\p",
                r"Насколько ты заполнил\n",
                r"ПОКЕДЕКС?\p",
                r"Можно взглянуть?\p",
                r"Посмотрим...$",
            ),
        ),
        "PalletTown_Text_CaughtXPuttingInHonestEffort": (
            (
                r"You've caught {STR_VAR_2}…\p",
                r"Hm, it looks as if you're putting\n",
                r"in an honest effort.\p",
                r"When you manage to fill it some\n",
                r"more, come show me, please.$",
            ),
            (
                r"Поймано: {STR_VAR_2}...\p",
                r"Хм, вижу, ты стараешься.\p",
                r"Заполни ПОКЕДЕКС еще немного\n",
                r"и снова покажи его мне.$",
            ),
        ),
        "PalletTown_Text_CaughtXImpressiveFollowMe": (
            (
                r"You've caught… {STR_VAR_2}!?\n",
                r"Now, this is impressive!\p",
                r"There's something I wanted to ask\n",
                r"of you, {PLAYER}.\p",
                r"Come.\n",
                r"Follow me.$",
            ),
            (
                r"Поймано... {STR_VAR_2}!?\n",
                r"Вот это впечатляет!\p",
                r"Я хотел кое о чем тебя\n",
                r"попросить, {PLAYER}.\p",
                r"Идем.\n",
                r"Следуй за мной.$",
            ),
        ),
        "PalletTown_Text_OakYouEnjoyingTraveling": (
            (
                r"OAK: Ah, {PLAYER}!\n",
                r"You seem to be enjoying traveling.\p",
                r"Knowing you, {PLAYER}, I can easily\n",
                r"imagine you going out to even more\l",
                r"exotic locales.\p",
                r"Good for you, good for you.\n",
                r"Hohoho.$",
            ),
            (
                r"ОУК: А, {PLAYER}!\n",
                r"Похоже, тебе нравится\n",
                r"путешествовать.\p",
                r"Зная тебя, {PLAYER}, уверен:\n",
                r"ты увидишь еще больше\l",
                r"далеких мест.\p",
                r"Так держать!\n",
                r"Хо-хо-хо.$",
            ),
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
        "__name__": "qarro_ru_early_kanto_v312_base",
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
    if audit.get("marker") != BASE_MARKER or audit.get("selectedBlocksLocalized") != 132:
        raise RuntimeError(
            "base localization audit drift: expected marker "
            f"{BASE_MARKER!r} and 132 blocks, got "
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
        print(f"[ru-early-v313] {rel}: {changed}/{len(blocks)} blocks changed")

    expected_new = 4
    if sum(len(v) for v in PATCHES.values()) != expected_new:
        raise RuntimeError("Pallet Town completion scope drift")
    if changed_total != expected_new:
        raise RuntimeError(
            f"fresh pinned checkout should change all {expected_new} new blocks; got {changed_total}"
        )

    audit["previousMarker"] = BASE_MARKER
    audit["marker"] = MARKER
    audit["selectedBlocksLocalized"] = 132 + expected_new
    audit["blocksChangedThisRun"] = int(audit.get("blocksChangedThisRun", 0)) + changed_total
    audit["palletTownExteriorCompleted"] = True
    audit["palletCoreEarlyTextAlreadyHandledByCoreLocalization"] = True
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
        f"localized {changed_total} genuinely untranslated Pallet Town blocks; "
        f"total={audit['selectedBlocksLocalized']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
