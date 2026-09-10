#!/usr/bin/env python3
"""Qarro v3.5 quality-of-life pass: starting supplies.

This first v3.5 step applies the already-agreed starting inventory for FireRed:
- 20 Poké Balls
- 10 Potions
- 5 Antidotes
- 5 Paralyze Heals

The patch is intentionally narrow. No Ash Bond / Ash Cap code is touched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_QOL_V3_5"


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.exists():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def patch_starting_supplies(root: Path) -> dict:
    path = root / "src/new_game.c"
    text = read(path)

    old = """    ClearBag();
    NewGameInitPCItems();
"""
    new = """    ClearBag();
#if IS_FRLG
    // Qarro v3.5: practical starting supplies with minimal early grind.
    AddBagItem(ITEM_POKE_BALL, 20);
    AddBagItem(ITEM_POTION, 10);
    AddBagItem(ITEM_ANTIDOTE, 5);
    AddBagItem(ITEM_PARALYZE_HEAL, 5);
#endif
    NewGameInitPCItems();
"""

    if new in text:
        print(f"[{MARKER}] starting supplies already present")
    elif old in text:
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")
        print(f"[{MARKER}] starting supplies installed")
    else:
        die("NewGameInitData ClearBag/NewGameInitPCItems anchor did not match pinned source")

    patched = read(path)
    required = {
        "ITEM_POKE_BALL": 20,
        "ITEM_POTION": 10,
        "ITEM_ANTIDOTE": 5,
        "ITEM_PARALYZE_HEAL": 5,
    }
    for item, qty in required.items():
        needle = f"AddBagItem({item}, {qty});"
        if patched.count(needle) != 1:
            die(f"expected exactly one {needle!r}")

    return {
        "enabledFor": "FireRed",
        "items": {
            "PokeBall": 20,
            "Potion": 10,
            "Antidote": 5,
            "ParalyzeHeal": 5,
        },
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    supplies = patch_starting_supplies(root)

    audit = {
        "marker": MARKER,
        "startingSupplies": supplies,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_qol_v3_5_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: starting supplies installed; Ash code untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
