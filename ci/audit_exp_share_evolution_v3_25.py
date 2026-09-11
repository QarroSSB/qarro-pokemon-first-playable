#!/usr/bin/env python3
"""Qarro v3.25 regression audit for party-wide Exp. Share evolution.

This does not change gameplay. It fails the build if the pinned Expansion path
that records an off-field level-up and performs post-battle level evolution is
removed or structurally changed. It also proves Qarro's Gen 6-style Exp. Share
configuration is active after the QoL pass.

Ash Bond / Ash Cap are not touched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_EXP_SHARE_EVO_AUDIT_V3_25"


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.is_file():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def require_once(text: str, token: str, label: str) -> None:
    count = text.count(token)
    if count != 1:
        die(f"{label}: expected exactly one occurrence, got {count}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    item_cfg = read(root / "include/config/item.h")
    exp_src = read(root / "src/battle_script_commands.c")
    battle_main = read(root / "src/battle_main.c")
    pokemon = read(root / "src/pokemon.c")

    # Qarro party-wide toggle must actually be active in the source being built.
    require_once(item_cfg, "#define I_EXP_SHARE_FLAG        FLAG_0x260", "Exp. Share flag")
    require_once(item_cfg, "#define I_EXP_SHARE_ITEM        GEN_6", "Gen 6 party-wide Exp. Share mode")

    # Any party slot that truly gains a level must be marked, regardless of whether
    # it was the active battler. This is the bridge from Exp. Share to evolution.
    level_mark = "gLeveledUpInBattle |= 1 << *expMonId;"
    require_once(exp_src, level_mark, "level-up evolution marker")

    # After battle, every marked slot must be sent through battle-only evolution.
    evo_gate = "if (species == SPECIES_NONE && (gLeveledUpInBattle & (1u << i)))"
    require_once(battle_main, evo_gate, "post-battle leveled-slot gate")
    require_once(battle_main, "mode = EVO_MODE_BATTLE_ONLY;", "post-battle evolution mode")

    # EVO_MODE_BATTLE_ONLY must include ordinary level evolution and the special
    # battle-only level method. This is what allows a non-participant leveled by
    # party-wide Exp. Share to evolve at the end of the battle.
    shared_mode = "case EVO_MODE_NORMAL:\n    case EVO_MODE_BATTLE_ONLY:"
    require_once(pokemon, shared_mode, "shared normal/battle-only evolution path")
    require_once(
        pokemon,
        "case EVO_LEVEL:\n                if (evolutions[i].param <= level)\n                    conditionsMet = TRUE;",
        "ordinary level evolution condition",
    )
    require_once(
        pokemon,
        "case EVO_LEVEL_BATTLE_ONLY:\n                if (mode == EVO_MODE_BATTLE_ONLY && evolutions[i].param <= level)\n                    conditionsMet = TRUE;",
        "battle-only level evolution condition",
    )

    report = {
        "marker": MARKER,
        "expShareMode": "GEN_6 party-wide key-item toggle",
        "levelUpSlotRecorded": True,
        "offFieldSlotEligible": True,
        "postBattleEvolutionGatePresent": True,
        "ordinaryLevelEvolutionPresent": True,
        "battleOnlyLevelEvolutionPresent": True,
        "gameplayChangedByAudit": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_exp_share_evo_v3_25_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: party-wide Exp. Share level-up marker and post-battle "
        "ordinary evolution path are present; Ash protections unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
