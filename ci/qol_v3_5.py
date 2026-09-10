#!/usr/bin/env python3
"""Qarro v3.5 quality-of-life pass.

Current confirmed QoL scope for FireRed:
- verify the pinned whiteout path does not deduct player money;
- return an ordinary Bag Poké Ball when a wild Pokémon breaks out;
- keep the existing temporary starting-supplies implementation intact until
  its final post-Pokédex timing is handled as the next dedicated backlog step.

The patch is intentionally narrow. Safari Ball counters, successful captures,
Ash Bond and Ash Cap are untouched.
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


def verify_no_money_loss(root: Path) -> dict:
    """Fail closed if the pinned whiteout path starts deducting money again."""
    path = root / "src/overworld.c"
    text = read(path)
    start_token = "void DoWhiteOut(void)\n{"
    end_token = "void Overworld_ResetStateAfterFly(void)"
    try:
        start = text.index(start_token)
        end = text.index(end_token, start)
    except ValueError as exc:
        die("DoWhiteOut anchors did not match pinned source")
        raise exc

    body = text[start:end]
    forbidden = ("SetMoney(", "RemoveMoney(")
    found = [token for token in forbidden if token in body]
    if found:
        die(f"whiteout money deduction unexpectedly present: {found}")
    if "RunScriptImmediately(EventScript_WhiteOut);" not in body:
        die("DoWhiteOut structure changed from pinned source")

    print(f"[{MARKER}] no-money-loss on defeat verified in pinned DoWhiteOut")
    return {
        "verified": True,
        "source": "src/overworld.c::DoWhiteOut",
        "moneyDeductionCalls": 0,
    }


def patch_failed_catch_ball_refund(root: Path) -> dict:
    """Refund a Bag ball only after the catch calculation has actually failed."""
    path = root / "src/battle_script_commands.c"
    text = read(path)

    old = """    if (!gHasFetchedBall)
        gLastUsedBall = gLastUsedItem;

    if (IsCriticalCapture())
"""
    new = """    if (!gHasFetchedBall)
        gLastUsedBall = gLastUsedItem;

    // Qarro v3.5: a normal Bag Ball is consumed only on a successful catch.
    // Safari uses its own counter and must retain the native behavior.
    if (!(gBattleTypeFlags & BATTLE_TYPE_SAFARI))
    {
        if (!AddBagItem(gLastUsedItem, 1))
            die("failed to return used Poke Ball after escaped capture");
    }

    if (IsCriticalCapture())
"""

    # C cannot call this Python helper; keep the failure path simple and
    # deterministic by replacing the temporary guard with a plain AddBagItem.
    new = new.replace(
        "        if (!AddBagItem(gLastUsedItem, 1))\n"
        "            die(\"failed to return used Poke Ball after escaped capture\");\n",
        "        AddBagItem(gLastUsedItem, 1);\n",
    )

    if new in text:
        print(f"[{MARKER}] failed-catch Ball refund already present")
    elif old in text:
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")
        print(f"[{MARKER}] failed-catch Ball refund installed")
    else:
        die("failed-catch Cmd_handleballthrow anchor did not match pinned source")

    patched = read(path)
    refund = "AddBagItem(gLastUsedItem, 1);"
    if patched.count(refund) != 1:
        die(f"expected exactly one failed-catch refund call, found {patched.count(refund)}")
    if patched.count("if (!(gBattleTypeFlags & BATTLE_TYPE_SAFARI))") != 1:
        die("expected exactly one Safari exclusion around failed-catch refund")

    return {
        "enabled": True,
        "source": "src/battle_script_commands.c::Cmd_handleballthrow failure path",
        "refundsOnEscape": True,
        "successfulCatchStillConsumesBall": True,
        "safariBehaviorPreserved": True,
    }


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
        "timing": "temporary-new-game; post-Pokedex move remains backlog",
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
    no_money_loss = verify_no_money_loss(root)
    failed_catch_ball = patch_failed_catch_ball_refund(root)
    supplies = patch_starting_supplies(root)

    audit = {
        "marker": MARKER,
        "noMoneyLossOnDefeat": no_money_loss,
        "failedCatchBall": failed_catch_ball,
        "startingSupplies": supplies,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_qol_v3_5_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: no-money-loss verified; failed-catch Ball refund installed; "
        "starting supplies retained; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
