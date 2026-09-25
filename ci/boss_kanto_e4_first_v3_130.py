#!/usr/bin/env python3
"""Qarro v3.130: install final-canon Kanto Elite Four first-clear teams.

Replaces only the four original first-clear Kanto Elite Four trainer party
blocks with the 2026-09-14 DESIGN FINAL 6v6 builds. Rematch trainers,
Champion trainers, Gym leaders, ordinary trainers, localization, font,
Ash Bond and Ash Cap are untouched.

The patch is fail-closed: it requires the exact pinned-upstream vanilla
first-clear species sequence before replacing a block.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_BOSS_KANTO_E4_CANON_V3_130"

EXPECTED_ORIGINAL = {'TRAINER_ELITE_FOUR_LORELEI': ['Dewgong', 'Cloyster', 'Slowbro', 'Jynx', 'Lapras'],
 'TRAINER_ELITE_FOUR_BRUNO': ['Onix', 'Hitmonchan', 'Hitmonlee', 'Onix', 'Machamp'],
 'TRAINER_ELITE_FOUR_AGATHA': ['Gengar', 'Golbat', 'Haunter', 'Arbok', 'Gengar'],
 'TRAINER_ELITE_FOUR_LANCE': ['Gyarados', 'Dragonair', 'Dragonair', 'Aerodactyl', 'Dragonite']}

TEAMS = {'TRAINER_ELITE_FOUR_LORELEI': [{'species': 'Cloyster',
                                  'level': 58,
                                  'nature': 'Jolly',
                                  'ability': 'Skill Link',
                                  'item': 'White Herb',
                                  'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                  'evs': '4 HP / 252 Atk / 252 Spe',
                                  'moves': ['Shell Smash', 'Icicle Spear', 'Rock Blast', 'Razor Shell'],
                                  'ace': False},
                                 {'species': 'Jynx',
                                  'level': 58,
                                  'nature': 'Timid',
                                  'ability': 'Dry Skin',
                                  'item': 'Focus Sash',
                                  'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                  'evs': '4 HP / 252 SpA / 252 Spe',
                                  'moves': ['Lovely Kiss', 'Ice Beam', 'Psychic', 'Nasty Plot'],
                                  'ace': False},
                                 {'species': 'Lapras',
                                  'level': 59,
                                  'nature': 'Modest',
                                  'ability': 'Water Absorb',
                                  'item': 'Leftovers',
                                  'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                  'evs': '252 HP / 252 SpA / 4 SpD',
                                  'moves': ['Surf', 'Ice Beam', 'Thunderbolt', 'Perish Song'],
                                  'ace': True},
                                 {'species': 'Mamoswine',
                                  'level': 58,
                                  'nature': 'Jolly',
                                  'ability': 'Thick Fat',
                                  'item': 'Life Orb',
                                  'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                  'evs': '4 HP / 252 Atk / 252 Spe',
                                  'moves': ['Earthquake', 'Icicle Crash', 'Ice Shard', 'Stone Edge'],
                                  'ace': False},
                                 {'species': 'Froslass',
                                  'level': 58,
                                  'nature': 'Timid',
                                  'ability': 'Cursed Body',
                                  'item': 'Focus Sash',
                                  'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                  'evs': '4 HP / 252 SpA / 252 Spe',
                                  'moves': ['Spikes', 'Ice Beam', 'Shadow Ball', 'Destiny Bond'],
                                  'ace': False},
                                 {'species': 'Walrein',
                                  'level': 58,
                                  'nature': 'Bold',
                                  'ability': 'Thick Fat',
                                  'item': 'Leftovers',
                                  'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                  'evs': '252 HP / 252 Def / 4 SpD',
                                  'moves': ['Surf', 'Ice Beam', 'Toxic', 'Protect'],
                                  'ace': False}],
 'TRAINER_ELITE_FOUR_BRUNO': [{'species': 'Machamp',
                                'level': 60,
                                'nature': 'Adamant',
                                'ability': 'No Guard',
                                'item': 'Lum Berry',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '4 HP / 252 Atk / 252 Spe',
                                'moves': ['Dynamic Punch', 'Stone Edge', 'Payback', 'Bullet Punch'],
                                'ace': True},
                               {'species': 'Hitmonlee',
                                'level': 59,
                                'nature': 'Jolly',
                                'ability': 'Reckless',
                                'item': 'Life Orb',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '4 HP / 252 Atk / 252 Spe',
                                'moves': ['High Jump Kick', 'Stone Edge', 'Sucker Punch', 'Blaze Kick'],
                                'ace': False},
                               {'species': 'Hitmonchan',
                                'level': 59,
                                'nature': 'Adamant',
                                'ability': 'Iron Fist',
                                'item': 'Life Orb',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '4 HP / 252 Atk / 252 Spe',
                                'moves': ['Drain Punch', 'Mach Punch', 'Ice Punch', 'Thunder Punch'],
                                'ace': False},
                               {'species': 'Poliwrath',
                                'level': 59,
                                'nature': 'Adamant',
                                'ability': 'Water Absorb',
                                'item': 'Leftovers',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '4 HP / 252 Atk / 252 Spe',
                                'moves': ['Substitute', 'Focus Punch', 'Waterfall', 'Ice Punch'],
                                'ace': False},
                               {'species': 'Heracross',
                                'level': 59,
                                'nature': 'Jolly',
                                'ability': 'Guts',
                                'item': 'Choice Scarf',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '4 HP / 252 Atk / 252 Spe',
                                'moves': ['Close Combat', 'Megahorn', 'Stone Edge', 'Night Slash'],
                                'ace': False},
                               {'species': 'Primeape',
                                'level': 59,
                                'nature': 'Jolly',
                                'ability': 'Vital Spirit',
                                'item': 'Choice Scarf',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '4 HP / 252 Atk / 252 Spe',
                                'moves': ['Close Combat', 'U-turn', 'Stone Edge', 'Ice Punch'],
                                'ace': False}],
 'TRAINER_ELITE_FOUR_AGATHA': [{'species': 'Gengar',
                                'level': 61,
                                'nature': 'Timid',
                                'ability': 'Levitate',
                                'item': 'Life Orb',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '4 HP / 252 SpA / 252 Spe',
                                'moves': ['Shadow Ball', 'Sludge Bomb', 'Focus Blast', 'Destiny Bond'],
                                'ace': True},
                               {'species': 'Mismagius',
                                'level': 60,
                                'nature': 'Timid',
                                'ability': 'Levitate',
                                'item': 'Life Orb',
                                'ivs': '31 HP / 31 Atk / 30 Def / 30 SpA / 30 SpD / 30 Spe',
                                'evs': '4 HP / 252 SpA / 252 Spe',
                                'moves': ['Nasty Plot', 'Shadow Ball', 'Thunderbolt', 'Hidden Power'],
                                'ace': False},
                               {'species': 'Spiritomb',
                                'level': 60,
                                'nature': 'Careful',
                                'ability': 'Pressure',
                                'item': 'Leftovers',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '252 HP / 4 Def / 252 SpD',
                                'moves': ['Will-O-Wisp', 'Sucker Punch', 'Pain Split', 'Taunt'],
                                'ace': False},
                               {'species': 'Dusknoir',
                                'level': 60,
                                'nature': 'Adamant',
                                'ability': 'Pressure',
                                'item': 'Leftovers',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '252 HP / 252 Atk / 4 SpD',
                                'moves': ['Shadow Sneak', 'Will-O-Wisp', 'Pain Split', 'Earthquake'],
                                'ace': False},
                               {'species': 'Chandelure',
                                'level': 60,
                                'nature': 'Timid',
                                'ability': 'Flash Fire',
                                'item': 'Life Orb',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '4 HP / 252 SpA / 252 Spe',
                                'moves': ['Fire Blast', 'Shadow Ball', 'Energy Ball', 'Will-O-Wisp'],
                                'ace': False},
                               {'species': 'Froslass',
                                'level': 60,
                                'nature': 'Timid',
                                'ability': 'Cursed Body',
                                'item': 'Focus Sash',
                                'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                                'evs': '4 HP / 252 SpA / 252 Spe',
                                'moves': ['Spikes', 'Ice Beam', 'Shadow Ball', 'Destiny Bond'],
                                'ace': False}],
 'TRAINER_ELITE_FOUR_LANCE': [{'species': 'Dragonite',
                               'level': 62,
                               'nature': 'Adamant',
                               'ability': 'Multiscale',
                               'item': 'Lum Berry',
                               'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                               'evs': '4 HP / 252 Atk / 252 Spe',
                               'moves': ['Dragon Dance', 'Dragon Claw', 'Fire Punch', 'Extreme Speed'],
                               'ace': True},
                              {'species': 'Kingdra',
                               'level': 61,
                               'nature': 'Modest',
                               'ability': 'Swift Swim',
                               'item': 'Life Orb',
                               'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                               'evs': '4 HP / 252 SpA / 252 Spe',
                               'moves': ['Surf', 'Dragon Pulse', 'Ice Beam', 'Rain Dance'],
                               'ace': False},
                              {'species': 'Flygon',
                               'level': 61,
                               'nature': 'Jolly',
                               'ability': 'Levitate',
                               'item': 'Choice Scarf',
                               'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                               'evs': '4 HP / 252 Atk / 252 Spe',
                               'moves': ['Earthquake', 'Outrage', 'U-turn', 'Stone Edge'],
                               'ace': False},
                              {'species': 'Haxorus',
                               'level': 61,
                               'nature': 'Jolly',
                               'ability': 'Mold Breaker',
                               'item': 'Lum Berry',
                               'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                               'evs': '4 HP / 252 Atk / 252 Spe',
                               'moves': ['Dragon Dance', 'Dragon Claw', 'Earthquake', 'Brick Break'],
                               'ace': False},
                              {'species': 'Hydreigon',
                               'level': 61,
                               'nature': 'Timid',
                               'ability': 'Levitate',
                               'item': 'Life Orb',
                               'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                               'evs': '4 HP / 252 SpA / 252 Spe',
                               'moves': ['Draco Meteor', 'Dark Pulse', 'Fire Blast', 'U-turn'],
                               'ace': False},
                              {'species': 'Aerodactyl',
                               'level': 61,
                               'nature': 'Jolly',
                               'ability': 'Pressure',
                               'item': 'Expert Belt',
                               'ivs': '31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe',
                               'evs': '4 HP / 252 Atk / 252 Spe',
                               'moves': ['Rock Slide', 'Earthquake', 'Ice Fang', 'Thunder Fang'],
                               'ace': False}]}

ACES = {
    "TRAINER_ELITE_FOUR_LORELEI": "Lapras",
    "TRAINER_ELITE_FOUR_BRUNO": "Machamp",
    "TRAINER_ELITE_FOUR_AGATHA": "Gengar",
    "TRAINER_ELITE_FOUR_LANCE": "Dragonite",
}

BANNED = {
    "Articuno", "Zapdos", "Moltres", "Mewtwo", "Mew", "Raikou", "Entei", "Suicune",
    "Lugia", "Ho-Oh", "Celebi", "Regirock", "Regice", "Registeel", "Latias", "Latios",
    "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Uxie", "Mesprit", "Azelf",
    "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina", "Cresselia", "Phione",
    "Manaphy", "Darkrai", "Shaymin", "Arceus", "Victini", "Cobalion", "Terrakion",
    "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem",
    "Keldeo", "Meloetta", "Genesect",
}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def trainer_bounds(text: str, trainer: str) -> tuple[int, int, str]:
    token = f"=== {trainer} ==="
    matches = [m for m in re.finditer(rf"(?m)^{re.escape(token)}$", text)]
    if len(matches) != 1:
        die(f"{trainer}: expected one trainer block, got {len(matches)}")
    start = matches[0].start()
    nxt = re.search(r"(?m)^=== [A-Z0-9_]+ ===$", text[matches[0].end():])
    end = len(text) if nxt is None else matches[0].end() + nxt.start()
    return start, end, text[start:end].rstrip()


def extract_species(block: str) -> list[str]:
    parts = block.split("\n\n")
    if len(parts) < 2:
        die("trainer block has no party section")
    out: list[str] = []
    for para in parts[1:]:
        lines = [ln for ln in para.splitlines() if ln.strip()]
        if not lines:
            continue
        first = lines[0]
        if first.startswith(("Name:", "Class:", "Pic:", "Gender:", "Music:", "Items:", "Double Battle:", "AI:", "Mugshot:")):
            continue
        if first.startswith(("Level:", "IVs:", "EVs:", "Ability:", "- ")) or first.endswith(" Nature"):
            continue
        out.append(first.split(" @ ", 1)[0])
    return out


def render_mon(mon: dict) -> str:
    first = mon["species"] if not mon["item"] else f'{mon["species"]} @ {mon["item"]}'
    lines = [
        first,
        f'Level: {mon["level"]}',
        f'IVs: {mon["ivs"]}',
        f'EVs: {mon["evs"]}',
        f'{mon["nature"]} Nature',
        f'Ability: {mon["ability"]}',
    ]
    lines.extend(f"- {move}" for move in mon["moves"])
    return "\n".join(lines)


def validate_canon() -> None:
    if set(TEAMS) != set(EXPECTED_ORIGINAL):
        die("trainer key mismatch")
    total = 0
    for trainer, mons in TEAMS.items():
        if len(mons) != 6:
            die(f"{trainer}: expected 6 canon Pokemon")
        species = [m["species"] for m in mons]
        if ACES[trainer] not in species:
            die(f"{trainer}: canonical Ace missing")
        if any(s in BANNED for s in species):
            die(f"{trainer}: Legendary/Mythical species present")
        if len(set(species)) != len(species):
            die(f"{trainer}: duplicate species in final canon")
        for mon in mons:
            if not (1 <= int(mon["level"]) <= 100):
                die(f"{trainer}: bad level for {mon['species']}")
            if len(mon["moves"]) != 4 or any(not move for move in mon["moves"]):
                die(f"{trainer}: bad moveset for {mon['species']}")
            if not mon["ivs"] or not mon["evs"] or not mon["nature"] or not mon["ability"]:
                die(f"{trainer}: incomplete build for {mon['species']}")
        total += len(mons)
    if total != 24:
        die(f"expected 24 total builds, got {total}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    validate_canon()

    root = Path(sys.argv[1]).resolve()
    party_path = root / "src/data/trainers_frlg.party"
    if not party_path.is_file():
        die("missing src/data/trainers_frlg.party")

    text = party_path.read_text(encoding="utf-8")
    replaced = {}

    for trainer, mons in TEAMS.items():
        start, end, old = trainer_bounds(text, trainer)
        before = extract_species(old)
        if before != EXPECTED_ORIGINAL[trainer]:
            die(f"{trainer}: pinned-upstream species mismatch: {before}")

        header = old.split("\n\n", 1)[0]
        new_block = header + "\n\n" + "\n\n".join(render_mon(mon) for mon in mons)
        text = text[:start] + new_block + "\n\n" + text[end:].lstrip("\n")
        replaced[trainer] = {
            "before": before,
            "after": [m["species"] for m in mons],
            "ace": ACES[trainer],
        }

    for trainer, mons in TEAMS.items():
        _, _, block = trainer_bounds(text, trainer)
        after = extract_species(block)
        expected = [m["species"] for m in mons]
        if after != expected:
            die(f"{trainer}: final party mismatch: {after} != {expected}")

    party_path.write_text(text, encoding="utf-8")

    audit = {
        "marker": MARKER,
        "scope": "Kanto Elite Four original first-clear trainers only",
        "trainersChanged": list(TEAMS.keys()),
        "trainerCount": len(TEAMS),
        "pokemonBuildCount": 24,
        "partySizeEach": 6,
        "ivPolicy": "31 all except explicit Hidden Power IV pattern from canon",
        "evPolicy": "final boss-grade workbook allocations",
        "acesGuaranteed": ACES,
        "noLegendaryMythical": True,
        "rematchTrainersTouched": False,
        "championTrainersTouched": False,
        "gymTrainersTouched": False,
        "ordinaryTrainersTouched": False,
        "replaced": replaced,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_boss_kanto_e4_canon_v3_130_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: 4 Kanto Elite Four first-clear trainers -> 24 final-canon builds; "
        "rematches/Champion/Gyms/ordinary trainers/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
