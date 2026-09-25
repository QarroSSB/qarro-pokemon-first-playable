#!/usr/bin/env python3
"""Qarro v3.98: strengthen the two pre-Gym Giovanni story boss fights.

These exact two rosters are implementation-derived from the approved project
rules (Rocket bosses competitive but thematic; ordinary Grunts must not become
minibosses) and Giovanni's approved Ground/Sand identity. They are NOT claimed
to be workbook-authored canon. The final Viridian Gym Giovanni 6v6 roster is
left untouched.

Scope:
- TRAINER_BOSS_GIOVANNI: Rocket Hideout, 4 Pokemon
- TRAINER_BOSS_GIOVANNI_2: Silph Co., 5 Pokemon
- strongest honest non-omniscient trainer AI flags
- no Legendary/Mythical Pokemon
- no ordinary Rocket Grunt/Admin edits
- Ash Bond / Ash Cap untouched
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_ROCKET_BOSS_GIOVANNI_V3_98"
REL = Path("src/data/trainers_frlg.party")

TEAMS = {
    "TRAINER_BOSS_GIOVANNI": """=== TRAINER_BOSS_GIOVANNI ===
Name: GIOVANNI
Class: Boss Frlg
Pic: Leader Giovanni Frlg
Gender: Male
Music: Aqua
Items: Hyper Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability

Nidorino
Level: 29
IVs: 22 HP / 22 Atk / 22 Def / 22 SpA / 22 SpD / 22 Spe
EVs: 30 Atk / 30 Spe
Jolly Nature
Ability: Poison Point
- Poison Jab
- Dig
- Double Kick
- Toxic Spikes

Rhyhorn @ Sitrus Berry
Level: 30
IVs: 22 HP / 22 Atk / 22 Def / 22 SpA / 22 SpD / 22 Spe
EVs: 30 HP / 30 Atk
Adamant Nature
Ability: Rock Head
- Bulldoze
- Rock Slide
- Megahorn
- Scary Face

Kangaskhan @ Silk Scarf
Level: 31
IVs: 22 HP / 22 Atk / 22 Def / 22 SpA / 22 SpD / 22 Spe
EVs: 30 Atk / 30 Spe
Adamant Nature
Ability: Scrappy
- Fake Out
- Return
- Crunch
- Brick Break

Nidoking @ Soft Sand
Level: 32
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
EVs: 40 SpA / 40 Spe
Modest Nature
Ability: Sheer Force
- Earth Power
- Sludge Wave
- Ice Beam
- Thunderbolt
""",
    "TRAINER_BOSS_GIOVANNI_2": """=== TRAINER_BOSS_GIOVANNI_2 ===
Name: GIOVANNI
Class: Boss Frlg
Pic: Leader Giovanni Frlg
Gender: Male
Music: Aqua
Items: Hyper Potion / Full Heal
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability

Dugtrio @ Focus Sash
Level: 39
IVs: 26 HP / 26 Atk / 26 Def / 26 SpA / 26 SpD / 26 Spe
EVs: 75 Atk / 75 Spe
Jolly Nature
Ability: Arena Trap
- Earthquake
- Rock Slide
- Sucker Punch
- Stealth Rock

Nidoqueen @ Black Sludge
Level: 40
IVs: 26 HP / 26 Atk / 26 Def / 26 SpA / 26 SpD / 26 Spe
EVs: 75 HP / 75 SpA
Modest Nature
Ability: Sheer Force
- Earth Power
- Sludge Wave
- Ice Beam
- Stealth Rock

Rhydon @ Eviolite
Level: 41
IVs: 26 HP / 26 Atk / 26 Def / 26 SpA / 26 SpD / 26 Spe
EVs: 75 HP / 75 Atk
Adamant Nature
Ability: Lightning Rod
- Earthquake
- Rock Slide
- Megahorn
- Thunder Punch

Kangaskhan @ Silk Scarf
Level: 42
IVs: 26 HP / 26 Atk / 26 Def / 26 SpA / 26 SpD / 26 Spe
EVs: 75 Atk / 75 Spe
Adamant Nature
Ability: Scrappy
- Fake Out
- Return
- Crunch
- Brick Break

Nidoking @ Life Orb
Level: 43
IVs: 26 HP / 26 Atk / 26 Def / 26 SpA / 26 SpD / 26 Spe
EVs: 75 SpA / 75 Spe
Modest Nature
Ability: Sheer Force
- Earth Power
- Sludge Wave
- Ice Beam
- Thunderbolt
""",
}

EXPECTED_SPECIES = {
    "TRAINER_BOSS_GIOVANNI": ["Nidorino", "Rhyhorn", "Kangaskhan", "Nidoking"],
    "TRAINER_BOSS_GIOVANNI_2": ["Dugtrio", "Nidoqueen", "Rhydon", "Kangaskhan", "Nidoking"],
}


def die(message: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {message}")


def bounds(text: str, trainer: str) -> tuple[int, int, str]:
    token = f"=== {trainer} ==="
    start = text.find(token)
    if start < 0:
        die(f"missing trainer block: {trainer}")
    nxt = text.find("\n=== ", start + len(token))
    end = len(text) if nxt < 0 else nxt + 1
    return start, end, text[start:end]


def species(block: str) -> list[str]:
    values: list[str] = []
    for line in block.splitlines()[1:]:
        if not line or ":" in line or line.startswith("- ") or line.endswith(" Nature"):
            continue
        values.append(line.split(" @ ", 1)[0])
    return values


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / REL
    if not path.is_file():
        die(f"missing {REL}")
    text = path.read_text(encoding="utf-8")

    # Verify the final Gym leader is present but never rewrite it here.
    if "=== TRAINER_LEADER_GIOVANNI ===" not in text:
        die("final Viridian Gym Giovanni block is missing")

    changed: list[str] = []
    for trainer, replacement in TEAMS.items():
        start, end, old = bounds(text, trainer)
        if "AI: Check Bad Move / Try To Faint / Check Viability" in old and species(old) == EXPECTED_SPECIES[trainer]:
            continue
        # Refuse broad edits if the target no longer looks like Giovanni.
        for anchor in ("Name: GIOVANNI", "Class: Boss Frlg", "Pic: Leader Giovanni Frlg"):
            if anchor not in old:
                die(f"{trainer}: source shape drifted; missing {anchor}")
        text = text[:start] + replacement.rstrip() + "\n\n" + text[end:]
        changed.append(trainer)

    path.write_text(text, encoding="utf-8")

    # Fail closed on the final authored source, not just our replacement strings.
    final = path.read_text(encoding="utf-8")
    reports = []
    for trainer, expected in EXPECTED_SPECIES.items():
        _, _, block = bounds(final, trainer)
        got = species(block)
        if got != expected:
            die(f"{trainer}: species mismatch {got} != {expected}")
        if "AI: Check Bad Move / Try To Faint / Check Viability" not in block:
            die(f"{trainer}: honest competitive AI flags missing")
        if any(name in block for name in ("Mewtwo", "Groudon", "Darkrai", "Zapdos", "Moltres", "Suicune", "Regirock", "Virizion")):
            die(f"{trainer}: forbidden Legendary/Mythical anchor present")
        levels = [int(v) for v in re.findall(r"(?m)^Level:\s*(\d+)\s*$", block)]
        reports.append({"trainer": trainer, "partySize": len(got), "species": got, "levels": levels})

    out = root / "build/qarro_rocket_boss_giovanni_v3_98_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "implementationSource": "implementation-derived from approved qualitative Rocket/Giovanni rules; exact rosters are not workbook-authored canon",
        "teams": reports,
        "ordinaryRocketGruntsTouched": False,
        "rocketAdminsTouched": False,
        "finalGymGiovanniTouched": False,
        "honestAi": True,
        "omniscientAi": False,
        "legendaryMythicalCount": 0,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: story Giovanni 4-mon + 5-mon teams installed; final Gym/Grunts/Admins/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
