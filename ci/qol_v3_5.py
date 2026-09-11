#!/usr/bin/env python3
"""Qarro QoL wrapper: proven v3.5 behavior + toggleable Exp. Share + wild EXP tuning.

Runs the exact Build 249 QoL implementation first, then applies the confirmed
post-Pokedex party-wide Gen 6-style Exp. Share. Finally it raises EXP from wild
Pokemon by 25% while leaving trainer/Gym EXP and the native scaled-EXP formula
unchanged. Species/content policy remains Gen I-V. Ash Bond / Ash Cap remain
untouched.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "cdce73eba8ca7c7b6c2ef12eca199e197abe2687"
BASE_PATH = "ci/qol_v3_5.py"
FOLLOWUP_PATH = "ci/exp_share_v3_22.py"
WILD_EXP_MARKER = "QARRO_WILD_EXP_V3_24"


def load_from_git(repo: Path, commit: str, path: str, module_name: str) -> dict:
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", commit],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        text=True,
    )
    ns = {"__name__": module_name, "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{commit}:{path}", "exec"), ns)
    return ns


def load_followup(repo: Path) -> dict:
    path = repo / FOLLOWUP_PATH
    if not path.is_file():
        raise RuntimeError(f"missing Qarro Exp. Share follow-up: {path}")
    code = path.read_text(encoding="utf-8")
    ns = {"__name__": "qarro_exp_share_v322", "__file__": str(path.resolve())}
    exec(compile(code, str(path), "exec"), ns)
    return ns


def patch_wild_exp(root: Path) -> dict:
    """Give wild battles a modest +25% EXP bonus without changing trainer EXP."""
    path = root / "src/battle_script_commands.c"
    text = path.read_text(encoding="utf-8")

    old = """void ApplyExperienceMultipliers(s32 *expAmount, u8 expGetterMonId, u8 faintedBattler)\n{\n    enum HoldEffect holdEffect = GetMonHoldEffect(&gParties[B_TRAINER_PLAYER][expGetterMonId]);\n\n    if (IsTradedMon(&gParties[B_TRAINER_PLAYER][expGetterMonId]))\n"""
    new = """void ApplyExperienceMultipliers(s32 *expAmount, u8 expGetterMonId, u8 faintedBattler)\n{\n    enum HoldEffect holdEffect = GetMonHoldEffect(&gParties[B_TRAINER_PLAYER][expGetterMonId]);\n\n    // Qarro: slightly reduce early wild grinding without inflating trainer/Gym rewards.\n    // Keep Expansion's scaled-EXP curve; this multiplier applies only to wild battles.\n    if (!(gBattleTypeFlags & BATTLE_TYPE_TRAINER))\n        *expAmount = (*expAmount * 125) / 100;\n\n    if (IsTradedMon(&gParties[B_TRAINER_PLAYER][expGetterMonId]))\n"""

    if new not in text:
        hits = text.count(old)
        if hits != 1:
            raise RuntimeError(
                f"[{WILD_EXP_MARKER}] ApplyExperienceMultipliers anchor drift: expected 1, got {hits}"
            )
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")

    patched = path.read_text(encoding="utf-8")
    if patched.count("*expAmount = (*expAmount * 125) / 100;") != 1:
        raise RuntimeError(f"[{WILD_EXP_MARKER}] wild EXP multiplier missing or duplicated")
    if patched.count("if (!(gBattleTypeFlags & BATTLE_TYPE_TRAINER))") != 1:
        raise RuntimeError(f"[{WILD_EXP_MARKER}] trainer exclusion guard missing or duplicated")

    # Preserve the native modern scaled-EXP path. We want a small boost, not a
    # replacement EXP formula.
    if "if (GetConfig(B_SCALED_EXP) >= GEN_5 && GetConfig(B_SCALED_EXP) != GEN_6)" not in patched:
        raise RuntimeError(f"[{WILD_EXP_MARKER}] native scaled EXP path changed unexpectedly")

    audit = {
        "marker": WILD_EXP_MARKER,
        "target": "src/battle_script_commands.c",
        "wildExpMultiplierPercent": 125,
        "trainerExpMultiplierPercent": 100,
        "scaledExpPreserved": True,
        "expShareTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_wild_exp_v3_24_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    return audit


def main() -> int:
    repo = Path(__file__).resolve().parents[1]

    base = load_from_git(repo, BASE_COMMIT, BASE_PATH, "qarro_qol_build249_baseline")
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    followup = load_followup(repo)
    rc = int(followup["main"]() or 0)
    if rc:
        return rc

    if len(sys.argv) != 2:
        raise RuntimeError("Qarro QoL wrapper expected exactly one upstream-root argument")
    root = Path(sys.argv[1]).resolve()
    patch_wild_exp(root)

    print(
        "[QARRO_QOL_V3_24] PASS: Build 249 QoL and post-Pokedex toggleable party-wide "
        "Exp. Share preserved; wild EXP +25%; trainer/Gym EXP unchanged; scaled EXP and "
        "Gen I-V content policy preserved; Ash protections unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
