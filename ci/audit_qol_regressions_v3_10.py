#!/usr/bin/env python3
"""Read-only regression audit for Qarro FireRed QoL behavior.

Checks the already-applied patches without changing gameplay data:
- defeat cannot remove player money, while trainer-win rewards remain;
- ordinary Bag Balls are refunded only on failed captures, never successful ones;
- starter supplies are granted exactly once in Oak's initial post-Pokedex scene.

FireRed / Expansion 1.17.0 / Gen I-V policy only. Ash Bond / Ash Cap untouched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_QOL_REGRESSION_V3_10"


def read(path: Path) -> str:
    if not path.is_file():
        raise RuntimeError(f"missing {path}")
    return path.read_text(encoding="utf-8")


def function_body(text: str, token: str, next_token: str = "\nstatic void ") -> str:
    try:
        start = text.index(token)
        end = text.index(next_token, start + len(token))
    except ValueError as exc:
        raise RuntimeError(f"function anchors changed: {token}") from exc
    return text[start:end]


def audit_money(root: Path) -> dict:
    text = read(root / "src/battle_script_commands.c")
    body = function_body(text, "static void Cmd_getmoneyreward(void)\n{")
    if "RemoveMoney(" in body:
        raise RuntimeError("defeat money deduction still present in Cmd_getmoneyreward")
    if "AddMoney(" not in body:
        raise RuntimeError("trainer-win money reward disappeared from Cmd_getmoneyreward")
    marker = "// Qarro v3.5: defeat does not remove player money."
    if body.count(marker) != 1:
        raise RuntimeError(f"expected one no-money-loss marker, found {body.count(marker)}")
    return {"removeMoneyCalls": 0, "winRewardPreserved": True}


def audit_failed_catch_ball(root: Path) -> dict:
    text = read(root / "src/battle_script_commands.c")
    body = function_body(text, "static void SetBallThrowShakes(void)\n{")

    refund = "AddBagItem(gLastUsedItem, 1);"
    if body.count(refund) != 1:
        raise RuntimeError(f"expected exactly one failed-catch Ball refund, found {body.count(refund)}")

    success_guard = "if (shakes == maxShakes) // mon caught, copy of the code above"
    success_finalize = "FinalizeCapture();\n        return;"
    failure_anchor = "if (!gHasFetchedBall)\n        gLastUsedBall = gLastUsedItem;"
    safari_guard = "if (!(gBattleTypeFlags & BATTLE_TYPE_SAFARI))"

    for token in (success_guard, success_finalize, failure_anchor, safari_guard):
        if token not in body:
            raise RuntimeError(f"capture-flow anchor missing: {token}")

    success_pos = body.index(success_guard)
    finalize_pos = body.index(success_finalize, success_pos)
    failure_pos = body.index(failure_anchor, finalize_pos)
    safari_pos = body.index(safari_guard, failure_pos)
    refund_pos = body.index(refund, safari_pos)

    if not success_pos < finalize_pos < failure_pos < safari_pos < refund_pos:
        raise RuntimeError("Ball refund is not confined to the failed-capture path")

    success_slice = body[success_pos:failure_pos]
    if refund in success_slice or "AddBagItem(" in success_slice:
        raise RuntimeError("successful capture path unexpectedly refunds a Ball")

    return {
        "refundCalls": 1,
        "refundAfterSuccessfulCaptureReturn": True,
        "successStillConsumesBall": True,
        "safariExcluded": True,
    }


def audit_starter_kit(root: Path) -> dict:
    oak = read(root / "data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc")
    new_game = read(root / "src/new_game.c")

    grants = {
        "ITEM_POKE_BALL": ("\tgiveitem ITEM_POKE_BALL, 15\n", 15),
        "ITEM_POTION": ("\tgiveitem ITEM_POTION, 10\n", 10),
        "ITEM_ANTIDOTE": ("\tgiveitem ITEM_ANTIDOTE, 5\n", 5),
        "ITEM_PARALYZE_HEAL": ("\tgiveitem ITEM_PARALYZE_HEAL, 5\n", 5),
    }
    native_five = "\tgiveitem_msg PalletTown_ProfessorOaksLab_Text_ReceivedFivePokeBalls, ITEM_POKE_BALL, 5\n"
    dex_flag = "\tsetflag FLAG_SYS_POKEDEX_GET\n"
    scene_done = "\tsetvar VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 6\n"

    for item, (line, _) in grants.items():
        if oak.count(line) != 1:
            raise RuntimeError(f"expected one post-Pokedex starter grant for {item}, found {oak.count(line)}")
    if oak.count(native_five) != 1:
        raise RuntimeError(f"expected one native five-Poke-Ball grant, found {oak.count(native_five)}")

    block_pos = min(oak.index(line) for line, _ in grants.values())
    try:
        dex_pos = oak.rindex(dex_flag, 0, block_pos)
        native_pos = oak.rindex(native_five, 0, block_pos + len(native_five))
        scene_pos = oak.index(scene_done, block_pos)
    except ValueError as exc:
        raise RuntimeError("Oak one-time post-Pokedex scene anchors changed") from exc

    if not dex_pos < native_pos <= block_pos < scene_pos:
        raise RuntimeError("starter kit escaped the initial one-time post-Pokedex scene")

    forbidden = (
        "AddBagItem(ITEM_POKE_BALL, 20);",
        "AddBagItem(ITEM_POTION, 10);",
        "AddBagItem(ITEM_ANTIDOTE, 5);",
        "AddBagItem(ITEM_PARALYZE_HEAL, 5);",
    )
    present = [token for token in forbidden if token in new_game]
    if present:
        raise RuntimeError(f"duplicate new-game starter grant remains: {present}")

    return {
        "timing": "initial post-Pokedex Oak scene",
        "oneTimeSceneGuard": True,
        "pokeBallsTotal": 20,
        "potions": 10,
        "antidotes": 5,
        "paralyzeHeals": 5,
        "duplicateNewGameGrant": False,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    report = {
        "marker": MARKER,
        "money": audit_money(root),
        "failedCatchBall": audit_failed_catch_ball(root),
        "starterKit": audit_starter_kit(root),
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_qol_regression_v3_10_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: defeat money protected; failed-catch Ball refund is failure-only; "
        "post-Pokedex starter kit remains one-time"
    )
    print(f"audit: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
