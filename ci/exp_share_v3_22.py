#!/usr/bin/env python3
"""Qarro v3.22 early toggleable Exp. Share pass.

Confirmed project behavior:
- give Exp. Share once in Oak's initial post-Pokedex scene;
- use Expansion's built-in Gen 6-style Key Item toggle behavior;
- start party-wide Exp. Share enabled, while allowing the player to switch it off/on;
- keep the project species/content policy Gen I-V;
- keep Ash Bond / Ash Cap untouched.

The patch uses FireRed's generic FLAG_0x260 only after proving that the pinned
source does not use it anywhere else at runtime. It fails closed on source drift.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_EXP_SHARE_V3_22"
FLAG = "FLAG_0x260"


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.is_file():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def prove_flag_is_available(root: Path) -> dict:
    flags_path = root / "include/constants/flags_frlg.h"
    flags = read(flags_path)
    expected_define = "#define FLAG_0x260                                       0x260"
    if expected_define not in flags:
        die("FLAG_0x260 definition changed in pinned FireRed constants")

    # These are definition/aggregation headers, not runtime consumers.
    constant_definition_files = {
        Path("include/constants/flags_frlg.h"),
        Path("include/constants/flags.h"),
    }
    allowed_after_patch = {
        Path("include/config/item.h"),
        Path("data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc"),
    }
    unexpected = []
    observed = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".c", ".h", ".inc", ".s"}:
            continue
        rel = path.relative_to(root)
        if rel in constant_definition_files:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if FLAG in text:
            observed.append(str(rel))
            if rel not in allowed_after_patch:
                unexpected.append(str(rel))
    if unexpected:
        die(f"{FLAG} is already used outside Qarro Exp. Share patch: {unexpected}")
    return {
        "flag": FLAG,
        "value": "0x260",
        "runtimeConsumersBeforeOrAfterPatch": observed,
        "reservedForExpShare": True,
    }


def patch_config(root: Path) -> dict:
    path = root / "include/config/item.h"
    text = read(path)

    old_flag = "#define I_EXP_SHARE_FLAG        0"
    new_flag = f"#define I_EXP_SHARE_FLAG        {FLAG}"
    old_item = "#define I_EXP_SHARE_ITEM        GEN_5"
    new_item = "#define I_EXP_SHARE_ITEM        GEN_6"

    if new_flag not in text:
        if text.count(old_flag) != 1:
            die(f"expected one native I_EXP_SHARE_FLAG define, found {text.count(old_flag)}")
        text = text.replace(old_flag, new_flag, 1)
    if new_item not in text:
        if text.count(old_item) != 1:
            die(f"expected one native I_EXP_SHARE_ITEM define, found {text.count(old_item)}")
        text = text.replace(old_item, new_item, 1)
    path.write_text(text, encoding="utf-8")

    patched = read(path)
    if patched.count(new_flag) != 1 or patched.count(new_item) != 1:
        die("Exp. Share config did not settle on exactly one toggleable configuration")

    item_use = read(root / "src/item_use.c")
    required_support = (
        "STATIC_ASSERT(I_EXP_SHARE_ITEM < GEN_6 || I_EXP_SHARE_FLAG > TEMP_FLAGS_END",
        "void ItemUseOutOfBattle_ExpShare(u8 taskId)",
        "FlagToggle(I_EXP_SHARE_FLAG);",
    )
    for token in required_support:
        if token not in item_use:
            die(f"built-in Exp. Share toggle support changed: {token}")

    items = read(root / "src/data/items.h")
    try:
        start = items.index("[ITEM_EXP_SHARE] =")
        end = items.index("\n    [ITEM_", start + 1)
    except ValueError as exc:
        die("ITEM_EXP_SHARE data block anchors changed")
        raise exc
    block = items[start:end]
    for token in ("#if I_EXP_SHARE_ITEM >= GEN_6", "ItemUseOutOfBattle_ExpShare"):
        if token not in block:
            die(f"Gen 6-style Exp. Share item support missing from item block: {token}")

    return {
        "partyWideFlag": FLAG,
        "itemMode": "GEN_6 key-item toggle",
        "genIVWildContentPolicyChanged": False,
    }


def patch_oak_grant(root: Path) -> dict:
    path = root / "data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc"
    text = read(path)

    old = """\tgiveitem ITEM_ANTIDOTE, 5
\tgiveitem ITEM_PARALYZE_HEAL, 5
\tmsgbox PalletTown_ProfessorOaksLab_Text_OakExplainCatching
"""
    new = """\tgiveitem ITEM_ANTIDOTE, 5
\tgiveitem ITEM_PARALYZE_HEAL, 5
\t@ Qarro v3.22: give toggleable party-wide Exp. Share after the Pokedex.
\t@ It starts ON; using the Key Item toggles it OFF/ON at any time.
\tgiveitem ITEM_EXP_SHARE, 1
\tsetflag FLAG_0x260
\tmsgbox PalletTown_ProfessorOaksLab_Text_OakExplainCatching
"""

    if new not in text:
        if text.count(old) != 1:
            die(f"Oak post-Pokedex starter-kit anchor changed; expected one block, found {text.count(old)}")
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")

    patched = read(path)
    if patched.count(new) != 1:
        die(f"expected one Exp. Share grant block, found {patched.count(new)}")

    grant_pos = patched.index("\tgiveitem ITEM_EXP_SHARE, 1\n")
    flag_pos = patched.index("\tsetflag FLAG_0x260\n", grant_pos)
    dex_flag = "\tsetflag FLAG_SYS_POKEDEX_GET\n"
    scene_done = "\tsetvar VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 6\n"
    try:
        dex_pos = patched.rindex(dex_flag, 0, grant_pos)
        done_pos = patched.index(scene_done, flag_pos)
    except ValueError as exc:
        die("Oak one-time post-Pokedex scene guards changed")
        raise exc
    if not dex_pos < grant_pos < flag_pos < done_pos:
        die("Exp. Share grant escaped Oak's initial one-time post-Pokedex scene")

    return {
        "timing": "Oak initial post-Pokedex scene",
        "quantity": 1,
        "startsEnabled": True,
        "oneTimeSceneGuard": True,
    }


def patch_toggle_messages(root: Path) -> dict:
    path = root / "src/strings.c"
    text = read(path)
    pairs = {
        'const u8 gText_ExpShareOn[] = _("The Exp. Share has been turned on.{PAUSE_UNTIL_PRESS}");':
            'const u8 gText_ExpShareOn[] = _("Доля опыта включена.{PAUSE_UNTIL_PRESS}");',
        'const u8 gText_ExpShareOff[] = _("The Exp. Share has been turned off.{PAUSE_UNTIL_PRESS}");':
            'const u8 gText_ExpShareOff[] = _("Доля опыта выключена.{PAUSE_UNTIL_PRESS}");',
    }
    changed = 0
    for old, new in pairs.items():
        if new in text:
            continue
        if text.count(old) != 1:
            die(f"Exp. Share UI string anchor changed: {old}")
        text = text.replace(old, new, 1)
        changed += 1
    path.write_text(text, encoding="utf-8")

    patched = read(path)
    for new in pairs.values():
        if patched.count(new) != 1:
            die("Russian Exp. Share toggle message missing after patch")
    return {"russianToggleMessages": True, "stringsChanged": changed}


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    flag_audit = prove_flag_is_available(root)
    config_audit = patch_config(root)
    grant_audit = patch_oak_grant(root)
    ui_audit = patch_toggle_messages(root)

    report = {
        "marker": MARKER,
        "flag": flag_audit,
        "config": config_audit,
        "grant": grant_audit,
        "ui": ui_audit,
        "speciesPolicy": "Gen I-V unchanged",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_exp_share_v3_22_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: Exp. Share granted after Pokedex; party-wide toggle ON by default; "
        f"player can switch it OFF/ON; Gen I-V content policy and Ash protections unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
