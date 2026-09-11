#!/usr/bin/env python3
"""Qarro v3.14 early-Kanto Russian localization: finish Rival's House.

Runs the exact CI-verified v3.13 pass, then closes the remaining user-facing
English text in Daisy's / Rival's House. Early Town Map dialogue was already
translated by v3.9; this pass adds only the fourteen postgame grooming and
friendship-rating blocks. Exact source matching keeps the pass fail-closed.

Pokemon species, Move and Ability proper names remain English. Gameplay,
trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "b6e4d55797d234e7105fed0f5288ff348a4a3602"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_13"
MARKER = "QARRO_RU_EARLY_KANTO_V3_14"
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
    "data/maps/PalletTown_RivalsHouse_Frlg/scripts.inc": {
        "PalletTown_RivalsHouse_Text_LikeMeToGroomMon": (
            (
                r"DAISY: Hi, {PLAYER}!\n",
                r"Good timing.\p",
                r"I'm about to have some tea.\n",
                r"Would you like to join me?\p",
                r"Oh, but look.\n",
                r"Your POKéMON are a little dirty.\p",
                r"Would you like me to groom one?$",
            ),
            (
                r"ДЕЙЗИ: Привет, {PLAYER}!\n",
                r"Как раз вовремя.\p",
                r"Я собиралась выпить чаю.\n",
                r"Хочешь присоединиться?\p",
                r"Ой, только посмотри.\n",
                r"Твои ПОКЕМОНЫ немного грязные.\p",
                r"Хочешь, я приведу одного\n",
                r"из них в порядок?$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_DontNeedAnyGrooming": (
            (
                r"You don't need any grooming done?\n",
                r"Okay, we'll just have tea.$",
            ),
            (
                r"Не нужно приводить их в порядок?\n",
                r"Ладно, тогда просто попьем чаю.$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_GroomWhichOne": (
            (r"Which one should I groom?$",),
            (r"Кого привести в порядок?$",),
        ),
        "PalletTown_RivalsHouse_Text_LookingNiceInNoTime": (
            (
                r"DAISY: Okay, I'll get it looking\n",
                r"nice in no time.$",
            ),
            (
                r"ДЕЙЗИ: Хорошо, сейчас я быстро\n",
                r"приведу его в порядок.$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_CantGroomAnEgg": (
            (
                r"Oh, sorry. I honestly can't\n",
                r"groom an EGG.$",
            ),
            (
                r"Ой, прости. Я правда не могу\n",
                r"ухаживать за ЯЙЦОМ.$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_MayISeeFirstMon": (
            (
                r"DAISY: Your POKéMON grow to love\n",
                r"you if you raise them with love.\p",
                r"For example, {PLAYER}, may I see\n",
                r"your first POKéMON?$",
            ),
            (
                r"ДЕЙЗИ: ПОКЕМОНЫ полюбят тебя,\n",
                r"если растить их с заботой.\p",
                r"Например, {PLAYER}, можно взглянуть\n",
                r"на твоего первого ПОКЕМОНА?$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_CouldntLoveYouMore": (
            (
                r"It couldn't possibly love you\n",
                r"any more than it does now.\p",
                r"Your POKéMON is happy beyond\n",
                r"words.$",
            ),
            (
                r"Он уже не может любить тебя\n",
                r"сильнее, чем сейчас.\p",
                r"Твой ПОКЕМОН безмерно счастлив.$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_ItLooksVeryHappy": (
            (
                r"It looks very happy.\p",
                r"I wish {RIVAL} could see this and\n",
                r"learn something from it.$",
            ),
            (
                r"Он выглядит очень счастливым.\p",
                r"Жаль, {RIVAL} этого не видит.\n",
                r"Ему стоило бы поучиться.$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_ItsQuiteFriendly": (
            (
                r"It's quite friendly with you.\n",
                r"Keep being good to it!$",
            ),
            (
                r"Он очень дружелюбен с тобой.\n",
                r"Продолжай заботиться о нем!$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_ItsWarmingUpToYou": (
            (
                r"It's warming up to you.\n",
                r"Trust must be growing between you.$",
            ),
            (
                r"Он начинает к тебе привыкать.\n",
                r"Доверие между вами растет.$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_NotFamiliarWithYouYet": (
            (
                r"It's not quite familiar with you\n",
                r"yet.\p",
                r"POKéMON are all quite wary when\n",
                r"you first get them.$",
            ),
            (
                r"Он пока еще не совсем\n",
                r"к тебе привык.\p",
                r"Сначала ПОКЕМОНЫ всегда\n",
                r"немного насторожены.$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_DontLikeWayItGlaresAtYou": (
            (
                r"{PLAYER}, I don't like the way it\n",
                r"glares at you.\p",
                r"Could you try being a little nicer\n",
                r"to it?$",
            ),
            (
                r"{PLAYER}, мне не нравится,\n",
                r"как он на тебя смотрит.\p",
                r"Попробуй быть с ним\n",
                r"немного добрее.$",
            ),
        ),
        "PalletTown_RivalsHouse_Text_WhyWouldMonHateYouSoMuch": (
            (
                r"…Um, it's not easy for me to say\n",
                r"this, but…\p",
                r"Is there some reason why your\n",
                r"POKéMON would hate you so much?$",
            ),
            (
                r"...Эм, мне нелегко это говорить,\n",
                r"но...\p",
                r"Есть причина, почему твой\n",
                r"ПОКЕМОН так тебя ненавидит?$",
            ),
        ),
    },
}

RAW_PATCHES = {
    "data/maps/PalletTown_RivalsHouse_Frlg/scripts.inc": (
        (
            'PalletTown_RivalsHouse_Text_ThereYouGoAllDone::\n'
            '#ifdef BUGFIX @ The localizers missed what should be a textcolor change in the localizations.\n'
            '\t.string "{COLOR DARK_GRAY}{STR_VAR_1} looks dreamily content…\\p"\n'
            '\t.string "{COLOR RED}DAISY: There you go! All done.\\n"\n'
            '#else @ In the JP games, gender-based text used a different font instead of different colors.\n'
            '\t.string "{FONT_NORMAL}{STR_VAR_1} looks dreamily content…\\p"\n'
            '\t.string "{FONT_FEMALE}DAISY: There you go! All done.\\n"\n'
            '#endif\n'
            '\t.string "See? Doesn\'t it look nice?\\p"\n'
            '\t.string "Giggle…\\n"\n'
            '\t.string "It\'s such a cute POKéMON.$"\n'
        ),
        (
            'PalletTown_RivalsHouse_Text_ThereYouGoAllDone::\n'
            '#ifdef BUGFIX @ The localizers missed what should be a textcolor change in the localizations.\n'
            '\t.string "{COLOR DARK_GRAY}{STR_VAR_1} выглядит очень довольным...\\p"\n'
            '\t.string "{COLOR RED}ДЕЙЗИ: Вот и все! Готово.\\n"\n'
            '#else @ In the JP games, gender-based text used a different font instead of different colors.\n'
            '\t.string "{FONT_NORMAL}{STR_VAR_1} выглядит очень довольным...\\p"\n'
            '\t.string "{FONT_FEMALE}ДЕЙЗИ: Вот и все! Готово.\\n"\n'
            '#endif\n'
            '\t.string "Видишь? Теперь намного лучше!\\p"\n'
            '\t.string "Хи-хи...\\n"\n'
            '\t.string "Какой милый ПОКЕМОН.$"\n'
        ),
    ),
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


def patch_raw(path: Path, old: str, new: str) -> int:
    text = path.read_text(encoding="utf-8")
    old_count = text.count(old)
    new_count = text.count(new)
    if old_count == 1 and new_count == 0:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        return 1
    if old_count == 0 and new_count == 1:
        return 0
    raise RuntimeError(
        f"{path}: conditional Daisy grooming block mismatch; old={old_count}, new={new_count}"
    )


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <pokeemerald-expansion-root>", file=sys.stderr)
        return 2

    code = load_base()
    ns = {
        "__name__": "qarro_ru_early_kanto_v313_base",
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
    if audit.get("marker") != BASE_MARKER or audit.get("selectedBlocksLocalized") != 136:
        raise RuntimeError(
            "base localization audit drift: expected marker "
            f"{BASE_MARKER!r} and 136 blocks, got "
            f"{audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}"
        )

    changed_total = 0
    for rel, blocks in PATCHES.items():
        path = root / rel
        if not path.is_file():
            raise RuntimeError(f"missing pinned source file: {rel}")
        changed = patch_file(path, blocks)
        changed_total += changed
        print(f"[ru-early-v314] {rel}: {changed}/{len(blocks)} standard blocks changed")

    for rel, (old, new) in RAW_PATCHES.items():
        path = root / rel
        if not path.is_file():
            raise RuntimeError(f"missing pinned source file: {rel}")
        changed = patch_raw(path, old, new)
        changed_total += changed
        print(f"[ru-early-v314] {rel}: {changed}/1 conditional block changed")

    expected_new = 14
    if sum(len(v) for v in PATCHES.values()) + len(RAW_PATCHES) != expected_new:
        raise RuntimeError("Rival's House completion scope drift")
    if changed_total != expected_new:
        raise RuntimeError(
            f"fresh pinned checkout should change all {expected_new} new blocks; got {changed_total}"
        )

    rel = "data/maps/PalletTown_RivalsHouse_Frlg/scripts.inc"
    audit.setdefault("files", {})[rel] = {
        "selectedBlocks": 24,
        "changedThisRun": expected_new,
        "alreadyLocalizedByEarlierPass": 10,
    }
    audit["previousMarker"] = BASE_MARKER
    audit["marker"] = MARKER
    audit["selectedBlocksLocalized"] = 136 + expected_new
    audit["blocksChangedThisRun"] = int(audit.get("blocksChangedThisRun", 0)) + changed_total
    audit["palletRivalsHouseCompleted"] = True
    audit["daisyGroomingLocalized"] = True
    audit["daisyFriendshipRatingLocalized"] = True
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
        f"localized {changed_total} remaining Rival's House blocks; "
        f"total={audit['selectedBlocksLocalized']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
