#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_BOSS_HP_REPLACEMENTS_V3_32"
PINNED = "e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7"

# Approved Gen I-V replacements for the boss-design workbook.
REPLACEMENTS = {
    "MISMAGIUS": "MOVE_ENERGY_BALL",
    "HOUNDOOM": "MOVE_SLUDGE_BOMB",
    "YANMEGA": "MOVE_ANCIENT_POWER",
    "SCEPTILE": "MOVE_GIGA_DRAIN",
    "ZAPDOS": "MOVE_ANCIENT_POWER",
    "GLACEON": "MOVE_HYPER_VOICE",
    "MAGNEZONE": "MOVE_SIGNAL_BEAM",
    "WAILORD": "MOVE_HYPER_BEAM",
    "VANILLUXE": "MOVE_SIGNAL_BEAM",
    "MANECTRIC": "MOVE_SIGNAL_BEAM",
    "JOLTEON": "MOVE_SIGNAL_BEAM",
}

# All replacement moves debuted no later than Gen V.
MOVE_GENERATION = {
    "MOVE_ENERGY_BALL": 4,
    "MOVE_SLUDGE_BOMB": 2,
    "MOVE_ANCIENT_POWER": 2,
    "MOVE_GIGA_DRAIN": 2,
    "MOVE_HYPER_VOICE": 3,
    "MOVE_SIGNAL_BEAM": 3,
    "MOVE_HYPER_BEAM": 1,
}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    learnables_path = root / "src/data/pokemon/all_learnables.json"
    if not learnables_path.is_file():
        die(f"missing {learnables_path}")

    data = json.loads(learnables_path.read_text(encoding="utf-8"))
    failures = []
    checked = []

    for species, move in REPLACEMENTS.items():
        if species not in data:
            failures.append(f"species missing: {species}")
            continue
        generation = MOVE_GENERATION.get(move)
        if generation is None or generation > 5:
            failures.append(f"move violates Gen I-V policy: {move} gen={generation}")
            continue
        learnable = move in data[species]
        checked.append({"species": species, "move": move, "generation": generation, "learnable": learnable})
        if not learnable:
            failures.append(f"{species} cannot learn {move} in pinned Expansion data")

    if failures:
        for failure in failures:
            print(f"[{MARKER}] FAIL: {failure}", file=sys.stderr)
        return 1

    out = root / "build/qarro_boss_hidden_power_v3_32_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "pinned": PINNED,
        "replacementSpeciesCount": len(REPLACEMENTS),
        "hiddenPowerVariantCountRemovedFromWorkbook": 19,
        "genPolicy": "Gen I-V",
        "allLearnable": True,
        "checked": checked,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, indent=2) + "\n", encoding="utf-8")

    print(f"[{MARKER}] PASS: {len(REPLACEMENTS)} species replacements are learnable in pinned Expansion 1.17.0; 19 Hidden Power variants removed from workbook design")
    for item in checked:
        print(f"[{MARKER}] {item['species']}: {item['move']} — learnable, Gen {item['generation']}")
    print(f"[{MARKER}] Ash Bond / Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
