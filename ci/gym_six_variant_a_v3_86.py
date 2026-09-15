#!/usr/bin/env python3
"""Qarro v3.86: install final-canon Kanto Gym Leader Variant A as 6v6.

This is the first executable 6v6 migration step from the historical 5-of-6
prototype.  It installs the CURRENT CANON Variant A roster for all eight Kanto
story leaders, with the badge-scaled IV/EV/item budgets from the 2026-09-14
6v6 honest-AI workbook.  It intentionally does not implement A/B/C save-fixed
selection yet; Variant A is installed first so the full 6v6 data path can be
compiled and play-tested before adding the selector.

No ordinary trainer, Elite Four, Champion, localization, font, Ash Bond or Ash
Cap data is touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_GYM_SIX_VARIANT_A_V3_86"


def mon(name: str, level: int, iv: int, nature: str, ability: str, moves: list[str], *, item: str | None = None, evs: str | None = None) -> str:
    first = name if item is None else f"{name} @ {item}"
    lines = [
        first,
        f"Level: {level}",
        f"IVs: {iv} HP / {iv} Atk / {iv} Def / {iv} SpA / {iv} SpD / {iv} Spe",
    ]
    if evs:
        lines.append(f"EVs: {evs}")
    lines += [f"{nature} Nature", f"Ability: {ability}"]
    lines += [f"- {move}" for move in moves]
    return "\n".join(lines)


TEAMS = {
    "TRAINER_LEADER_BROCK": {
        "ace": "Tyranitar", "iv": 12, "ev_budget": 0, "items": 2,
        "party": [
            mon("Golem", 13, 12, "Adamant", "Sturdy", ["Earthquake", "Rock Polish", "Rock Slide", "Explosion"]),
            mon("Aerodactyl", 13, 12, "Jolly", "Pressure", ["Rock Slide", "Earthquake", "Ice Fang", "Thunder Fang"]),
            mon("Tyranitar", 14, 12, "Adamant", "Sand Stream", ["Crunch", "Rock Slide", "Earthquake", "Dragon Dance"], item="Chople Berry"),
            mon("Omastar", 14, 12, "Modest", "Shell Armor", ["Surf", "Ice Beam", "Earth Power", "Shell Smash"]),
            mon("Cradily", 15, 12, "Calm", "Storm Drain", ["Toxic", "Recover", "Giga Drain", "Ancient Power"], item="Leftovers"),
            mon("Kabutops", 16, 12, "Adamant", "Battle Armor", ["Waterfall", "Rock Slide", "Aqua Jet", "Swords Dance"]),
        ],
    },
    "TRAINER_LEADER_MISTY": {
        "ace": "Starmie", "iv": 16, "ev_budget": 0, "items": 3,
        "party": [
            mon("Politoed", 19, 16, "Bold", "Drizzle", ["Scald", "Ice Beam", "Encore", "Perish Song"], item="Damp Rock"),
            mon("Lapras", 19, 16, "Modest", "Water Absorb", ["Surf", "Ice Beam", "Thunderbolt", "Perish Song"]),
            mon("Starmie", 20, 16, "Timid", "Natural Cure", ["Thunderbolt", "Scald", "Telekinesis", "Ice Beam"], item="Expert Belt"),
            mon("Vaporeon", 20, 16, "Bold", "Water Absorb", ["Scald", "Ice Beam", "Wish", "Protect"]),
            mon("Lanturn", 21, 16, "Calm", "Volt Absorb", ["Scald", "Volt Switch", "Ice Beam", "Thunder Wave"]),
            mon("Slowbro", 22, 16, "Bold", "Regenerator", ["Scald", "Psychic", "Slack Off", "Thunder Wave"], item="Leftovers"),
        ],
    },
    "TRAINER_LEADER_LT_SURGE": {
        "ace": "Electivire", "iv": 20, "ev_budget": 80, "items": 4,
        "party": [
            mon("Electrode", 25, 20, "Timid", "Soundproof", ["Rain Dance", "Thunder", "Taunt", "Volt Switch"], evs="40 SpA / 40 Spe"),
            mon("Raichu", 25, 20, "Timid", "Lightning Rod", ["Thunderbolt", "Focus Blast", "Grass Knot", "Nasty Plot"], item="Life Orb", evs="40 SpA / 40 Spe"),
            mon("Jolteon", 26, 20, "Timid", "Volt Absorb", ["Thunderbolt", "Volt Switch", "Shadow Ball", "Hidden Power"], item="Choice Specs", evs="40 SpA / 40 Spe"),
            mon("Magneton", 26, 20, "Timid", "Magnet Pull", ["Thunderbolt", "Flash Cannon", "Volt Switch", "Hidden Power"], item="Eviolite", evs="40 SpA / 40 Spe"),
            mon("Electivire", 27, 20, "Jolly", "Motor Drive", ["Wild Charge", "Ice Punch", "Earthquake", "Cross Chop"], item="Expert Belt", evs="40 Atk / 40 Spe"),
            mon("Ampharos", 28, 20, "Modest", "Static", ["Thunderbolt", "Focus Blast", "Signal Beam", "Volt Switch"], evs="40 HP / 40 SpA"),
        ],
    },
    "TRAINER_LEADER_ERIKA": {
        "ace": "Venusaur", "iv": 24, "ev_budget": 160, "items": 5,
        "party": [
            mon("Ninetales", 31, 24, "Timid", "Drought", ["Fire Blast", "Solarbeam", "Will-O-Wisp", "Nasty Plot"], item="Heat Rock", evs="80 SpA / 80 Spe"),
            mon("Venusaur", 31, 24, "Timid", "Chlorophyll", ["Growth", "Giga Drain", "Sludge Bomb", "Sleep Powder"], item="Life Orb", evs="80 SpA / 80 Spe"),
            mon("Victreebel", 32, 24, "Adamant", "Chlorophyll", ["Swords Dance", "Leaf Blade", "Sucker Punch", "Poison Jab"], item="Life Orb", evs="80 Atk / 80 Spe"),
            mon("Vileplume", 32, 24, "Bold", "Effect Spore", ["Giga Drain", "Sludge Bomb", "Sleep Powder", "Synthesis"], evs="80 HP / 80 Def"),
            mon("Jumpluff", 33, 24, "Jolly", "Chlorophyll", ["Sleep Powder", "Leech Seed", "Substitute", "Encore"], item="Leftovers", evs="80 HP / 80 Spe"),
            mon("Celebi", 34, 24, "Timid", "Natural Cure", ["Giga Drain", "Psychic", "Recover", "Thunder Wave"], item="Leftovers", evs="80 SpA / 80 Spe"),
        ],
    },
    "TRAINER_LEADER_KOGA": {
        "ace": "Crobat", "iv": 26, "ev_budget": 252, "items": 6,
        "party": [
            mon("Crobat", 37, 26, "Jolly", "Inner Focus", ["Brave Bird", "U-Turn", "Roost", "Taunt"], item="Black Sludge", evs="252 Spe"),
            mon("Weezing", 37, 26, "Bold", "Levitate", ["Will-O-Wisp", "Sludge Bomb", "Fire Blast", "Pain Split"], item="Black Sludge", evs="252 Def"),
            mon("Muk", 38, 26, "Adamant", "Sticky Hold", ["Poison Jab", "Shadow Sneak", "Ice Punch", "Curse"], item="Black Sludge", evs="252 Atk"),
            mon("Venomoth", 38, 26, "Timid", "Tinted Lens", ["Quiver Dance", "Bug Buzz", "Sleep Powder", "Roost"], item="Leftovers", evs="252 Spe"),
            mon("Tentacruel", 39, 26, "Timid", "Rain Dish", ["Scald", "Rapid Spin", "Toxic Spikes", "Ice Beam"], item="Black Sludge", evs="252 Spe"),
            mon("Qwilfish", 40, 26, "Impish", "Intimidate", ["Spikes", "Toxic Spikes", "Waterfall", "Taunt"], item="Black Sludge", evs="252 Def"),
        ],
    },
    "TRAINER_LEADER_SABRINA": {
        "ace": "Alakazam", "iv": 28, "ev_budget": 360, "items": 6,
        "party": [
            mon("Alakazam", 43, 28, "Timid", "Magic Guard", ["Psychic", "Focus Blast", "Shadow Ball", "Calm Mind"], item="Life Orb", evs="252 SpA / 108 Spe"),
            mon("Espeon", 43, 28, "Timid", "Magic Bounce", ["Psychic", "Shadow Ball", "Morning Sun", "Calm Mind"], item="Leftovers", evs="252 SpA / 108 Spe"),
            mon("Mr. Mime", 44, 28, "Timid", "Filter", ["Reflect", "Light Screen", "Psychic", "Baton Pass"], item="Light Clay", evs="252 Spe / 108 HP"),
            mon("Exeggutor", 44, 28, "Modest", "Chlorophyll", ["Psychic", "Giga Drain", "Sleep Powder", "Hidden Power"], item="Life Orb", evs="252 SpA / 108 HP"),
            mon("Slowking", 45, 28, "Calm", "Regenerator", ["Scald", "Psychic", "Slack Off", "Ice Beam"], item="Leftovers", evs="252 HP / 108 SpD"),
            mon("Mew", 46, 28, "Timid", "Synchronize", ["Psychic", "Aura Sphere", "Recover", "Thunder Wave"], item="Leftovers", evs="252 SpA / 108 Spe"),
        ],
    },
    "TRAINER_LEADER_BLAINE": {
        "ace": "Arcanine", "iv": 30, "ev_budget": 420, "items": 6,
        "party": [
            mon("Ninetales", 49, 30, "Timid", "Drought", ["Fire Blast", "Solarbeam", "Will-O-Wisp", "Nasty Plot"], item="Heat Rock", evs="252 SpA / 168 Spe"),
            mon("Arcanine", 49, 30, "Adamant", "Intimidate", ["Flare Blitz", "Extreme Speed", "Wild Charge", "Crunch"], item="Life Orb", evs="252 Atk / 168 Spe"),
            mon("Rapidash", 50, 30, "Jolly", "Flash Fire", ["Flare Blitz", "Wild Charge", "Megahorn", "Morning Sun"], item="Life Orb", evs="252 Atk / 168 Spe"),
            mon("Magmar", 50, 30, "Timid", "Vital Spirit", ["Fire Blast", "Focus Blast", "Thunderbolt", "Will-O-Wisp"], item="Eviolite", evs="252 SpA / 168 Spe"),
            mon("Houndoom", 51, 30, "Timid", "Flash Fire", ["Nasty Plot", "Dark Pulse", "Fire Blast", "Hidden Power"], item="Life Orb", evs="252 SpA / 168 Spe"),
            mon("Magcargo", 52, 30, "Bold", "Flame Body", ["Lava Plume", "Recover", "Stealth Rock", "Toxic"], item="Leftovers", evs="252 HP / 168 Def"),
        ],
    },
    "TRAINER_LEADER_GIOVANNI": {
        "ace": "Nidoking", "iv": 31, "ev_budget": 510, "items": 6,
        "party": [
            mon("Nidoking", 55, 31, "Modest", "Sheer Force", ["Earth Power", "Sludge Wave", "Ice Beam", "Thunderbolt"], item="Life Orb", evs="252 SpA / 252 Spe / 6 HP"),
            mon("Nidoqueen", 55, 31, "Modest", "Sheer Force", ["Earth Power", "Sludge Wave", "Ice Beam", "Stealth Rock"], item="Life Orb", evs="252 HP / 252 SpA / 6 Def"),
            mon("Rhydon", 56, 31, "Adamant", "Lightning Rod", ["Earthquake", "Rock Slide", "Megahorn", "Thunder Punch"], item="Eviolite", evs="252 HP / 252 Atk / 6 SpD"),
            mon("Dugtrio", 56, 31, "Jolly", "Arena Trap", ["Earthquake", "Stone Edge", "Sucker Punch", "Stealth Rock"], item="Focus Sash", evs="252 Atk / 252 Spe / 6 HP"),
            mon("Donphan", 57, 31, "Adamant", "Sturdy", ["Earthquake", "Ice Shard", "Rapid Spin", "Stealth Rock"], item="Leftovers", evs="252 HP / 252 Atk / 6 Def"),
            mon("Hippowdon", 58, 31, "Impish", "Sand Stream", ["Earthquake", "Stone Edge", "Slack Off", "Stealth Rock"], item="Leftovers", evs="252 HP / 252 Def / 6 SpD"),
        ],
    },
}

BANNED = {"Regirock", "Suicune", "Zapdos", "Virizion", "Darkrai", "Mewtwo", "Moltres", "Groudon"}
APPROVED_MYTHICAL = {"Celebi", "Mew"}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def trainer_block(text: str, trainer: str) -> tuple[int, int, str]:
    token = f"=== {trainer} ==="
    start = text.find(token)
    if start < 0:
        die(f"trainer block missing: {trainer}")
    next_start = text.find("\n=== ", start + len(token))
    end = len(text) if next_start < 0 else next_start
    return start, end, text[start:end]


def species_lines(block: str) -> list[str]:
    out = []
    for line in block.splitlines()[1:]:
        if not line or line.startswith(("Level:", "IVs:", "EVs:", "Ability:", "- ")) or line.endswith(" Nature"):
            continue
        out.append(line.split(" @ ", 1)[0])
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    party_path = root / "src/data/trainers_frlg.party"
    opponents_path = root / "include/constants/opponents_frlg.h"
    if not party_path.is_file() or not opponents_path.is_file():
        die("missing FireRed trainer party/opponent source")

    text = party_path.read_text(encoding="utf-8")
    opponents = opponents_path.read_text(encoding="utf-8")
    report = []

    for trainer, cfg in TEAMS.items():
        if trainer not in opponents:
            die(f"trainer constant missing: {trainer}")
        start, end, old = trainer_block(text, trainer)
        body = "\n\n".join(cfg["party"])
        new = f"=== {trainer} ===\n\n{body}\n"
        text = text[:start] + new + text[end:]

        found = species_lines(new)
        expected = [set_text.splitlines()[0].split(" @ ", 1)[0] for set_text in cfg["party"]]
        if found != expected:
            die(f"{trainer}: roster parse mismatch: {found} != {expected}")
        if len(found) != 6 or cfg["ace"] not in found:
            die(f"{trainer}: invalid 6v6/ace roster: {found}")
        forbidden = sorted(set(found) & BANNED)
        if forbidden:
            die(f"{trainer}: banned legacy boss species remain: {forbidden}")

        item_count = sum(" @ " in set_text.splitlines()[0] for set_text in cfg["party"])
        if item_count != cfg["items"]:
            die(f"{trainer}: held item count {item_count} != canon {cfg['items']}")

        report.append({
            "trainer": trainer,
            "variant": "A",
            "partySize": 6,
            "roster": found,
            "ace": cfg["ace"],
            "iv": cfg["iv"],
            "evBudgetPerPokemon": cfg["ev_budget"],
            "meaningfulHeldItems": item_count,
        })

    party_path.write_text(text, encoding="utf-8")

    audit_dir = root / "build"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_path = audit_dir / "qarro_gym_six_variant_a_v3_86_audit.json"
    audit_path.write_text(json.dumps({
        "marker": MARKER,
        "mode": "6v6 Variant A test migration",
        "leaders": report,
        "leaderCount": len(report),
        "allPartiesSix": all(x["partySize"] == 6 for x in report),
        "approvedMythicalUsed": sorted(APPROVED_MYTHICAL),
        "legacy5of6RuntimeSelector": False,
        "nextStep": "Implement save-fixed A/B/C selection after this 6v6 data path is green.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[{MARKER}] PASS: installed 8 Kanto story Leader Variant A parties at 6v6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
