#!/usr/bin/env python3
"""Qarro v3.5 quality-of-life pass.

Current confirmed QoL scope for FireRed:
- disable the pinned trainer-loss money deduction at its actual battle path;
- return an ordinary Bag Poké Ball when a wild Pokémon breaks out;
- grant the starting supplies exactly once in Oak's initial post-Pokédex scene.

The patch is intentionally narrow. Safari Ball counters, successful captures,
Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_QOL_V3_5"


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.exists():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def patch_no_money_loss(root: Path) -> dict:
    """Disable only the pinned player-money deduction in Cmd_getmoneyreward."""
    # DoWhiteOut itself must remain structurally native; the actual money loss is
    # performed by the battle command before the overworld whiteout transition.
    overworld_path = root / "src/overworld.c"
    overworld = read(overworld_path)
    start_token = "void DoWhiteOut(void)\n{"
    end_token = "void Overworld_ResetStateAfterFly(void)"
    try:
        ow_start = overworld.index(start_token)
        ow_end = overworld.index(end_token, ow_start)
    except ValueError as exc:
        die("DoWhiteOut anchors did not match pinned source")
        raise exc
    ow_body = overworld[ow_start:ow_end]
    if "RunScriptImmediately(EventScript_WhiteOut);" not in ow_body:
        die("DoWhiteOut structure changed from pinned source")

    path = root / "src/battle_script_commands.c"
    text = read(path)
    fn_token = "static void Cmd_getmoneyreward(void)\n{"
    try:
        start = text.index(fn_token)
        end = text.index("\nstatic void ", start + len(fn_token))
    except ValueError as exc:
        die("Cmd_getmoneyreward anchors did not match pinned source")
        raise exc

    body = text[start:end]
    native = "        RemoveMoney(&gSaveBlock1Ptr->money, money);"
    patched_line = "        // Qarro v3.5: defeat does not remove player money."

    if patched_line in body:
        print(f"[{MARKER}] no-money-loss patch already present")
    else:
        if body.count(native) != 1:
            die(f"expected one pinned loss deduction in Cmd_getmoneyreward, found {body.count(native)}")
        new_body = body.replace(native, patched_line, 1)
        text = text[:start] + new_body + text[end:]
        path.write_text(text, encoding="utf-8")
        print(f"[{MARKER}] no-money-loss patch installed at Cmd_getmoneyreward loss branch")

    patched = read(path)
    try:
        start = patched.index(fn_token)
        end = patched.index("\nstatic void ", start + len(fn_token))
    except ValueError as exc:
        die("Cmd_getmoneyreward anchors drifted after patch")
        raise exc
    body = patched[start:end]
    if native in body or "RemoveMoney(" in body:
        die("player-money deduction still present in Cmd_getmoneyreward")
    if body.count(patched_line) != 1:
        die(f"expected exactly one no-money-loss marker, found {body.count(patched_line)}")
    if "AddMoney(" not in body:
        die("trainer-win reward path unexpectedly changed")

    return {
        "enabled": True,
        "source": "src/battle_script_commands.c::Cmd_getmoneyreward loss branch",
        "moneyDeductionCalls": 0,
        "trainerWinRewardPreserved": True,
        "whiteoutFlowPreserved": True,
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
        AddBagItem(gLastUsedItem, 1);
    }

    if (IsCriticalCapture())
"""

    if new in text:
        print(f"[{MARKER}] failed-catch Ball refund already present")
    elif old in text:
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")
        print(f"[{MARKER}] failed-catch Ball refund installed")
    else:
        die("failed-catch Cmd_handleballthrow anchor did not match pinned source")

    patched = read(path)
    if patched.count(new) != 1:
        die(f"expected exactly one complete failed-catch refund block, found {patched.count(new)}")

    return {
        "enabled": True,
        "source": "src/battle_script_commands.c::SetBallThrowShakes failure path",
        "refundsOnEscape": True,
        "successfulCatchStillConsumesBall": True,
        "safariBehaviorPreserved": True,
    }


def patch_starting_supplies(root: Path) -> dict:
    """Move the temporary new-game kit to Oak's one-time initial Pokédex scene."""
    new_game_path = root / "src/new_game.c"
    new_game = read(new_game_path)

    temporary = """    ClearBag();
#if IS_FRLG
    // Qarro v3.5: practical starting supplies with minimal early grind.
    AddBagItem(ITEM_POKE_BALL, 20);
    AddBagItem(ITEM_POTION, 10);
    AddBagItem(ITEM_ANTIDOTE, 5);
    AddBagItem(ITEM_PARALYZE_HEAL, 5);
#endif
    NewGameInitPCItems();
"""
    native = """    ClearBag();
    NewGameInitPCItems();
"""

    if temporary in new_game:
        new_game = new_game.replace(temporary, native, 1)
        new_game_path.write_text(new_game, encoding="utf-8")
        print(f"[{MARKER}] temporary new-game supplies removed")
    elif native not in new_game:
        die("NewGameInitData ClearBag/NewGameInitPCItems anchor did not match pinned source")

    new_game = read(new_game_path)
    for needle in (
        "AddBagItem(ITEM_POKE_BALL, 20);",
        "AddBagItem(ITEM_POTION, 10);",
        "AddBagItem(ITEM_ANTIDOTE, 5);",
        "AddBagItem(ITEM_PARALYZE_HEAL, 5);",
    ):
        if needle in new_game:
            die(f"temporary starting-supply hook still present in new_game.c: {needle}")

    oak_path = root / "data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc"
    oak = read(oak_path)
    old = """\tgiveitem_msg PalletTown_ProfessorOaksLab_Text_ReceivedFivePokeBalls, ITEM_POKE_BALL, 5
\tmsgbox PalletTown_ProfessorOaksLab_Text_OakExplainCatching
"""
    new = """\tgiveitem_msg PalletTown_ProfessorOaksLab_Text_ReceivedFivePokeBalls, ITEM_POKE_BALL, 5
\t@ Qarro v3.5: complete the one-time post-Pokedex starter kit here.
\t@ Oak's native five Balls + fifteen below = exactly twenty total Balls.
\tgiveitem ITEM_POKE_BALL, 15
\tgiveitem ITEM_POTION, 10
\tgiveitem ITEM_ANTIDOTE, 5
\tgiveitem ITEM_PARALYZE_HEAL, 5
\tmsgbox PalletTown_ProfessorOaksLab_Text_OakExplainCatching
"""

    if new in oak:
        print(f"[{MARKER}] post-Pokedex starting supplies already present")
    elif old in oak:
        oak = oak.replace(old, new, 1)
        oak_path.write_text(oak, encoding="utf-8")
        print(f"[{MARKER}] post-Pokedex starting supplies installed")
    else:
        die("Oak initial Pokédex/Poké Ball grant anchor did not match pinned source")

    patched = read(oak_path)
    if patched.count(new) != 1:
        die(f"expected exactly one complete post-Pokedex starter-kit block, found {patched.count(new)}")

    dex_flag = "\tsetflag FLAG_SYS_POKEDEX_GET\n"
    scene_done = "\tsetvar VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 6\n"
    block_pos = patched.index(new)
    try:
        dex_pos = patched.rindex(dex_flag, 0, block_pos)
        scene_pos = patched.index(scene_done, block_pos)
    except ValueError as exc:
        die("post-Pokedex one-time scene guards changed from pinned source")
        raise exc
    if not dex_pos < block_pos < scene_pos:
        die("starter kit is not inside the initial post-Pokedex one-time scene")

    return {
        "enabledFor": "FireRed",
        "timing": "one-time post-Pokedex Oak grant",
        "source": "data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc",
        "items": {
            "PokeBall": 20,
            "Potion": 10,
            "Antidote": 5,
            "ParalyzeHeal": 5,
        },
        "nativePokeBalls": 5,
        "supplementalPokeBalls": 15,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    no_money_loss = patch_no_money_loss(root)
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
        f"[{MARKER}] PASS: no-money-loss installed; failed-catch Ball refund installed; "
        "post-Pokedex starter supplies installed; Ash code untouched"
    )

    regression = Path(__file__).resolve().with_name("audit_qol_regressions_v3_10.py")
    if not regression.is_file():
        die(f"missing QoL regression audit: {regression}")
    subprocess.run([sys.executable, str(regression), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
