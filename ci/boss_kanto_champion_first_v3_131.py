#!/usr/bin/env python3
"""Qarro v3.131: install final-canon Kanto Champion Gary first-clear team.

FireRed exposes three first-clear Champion trainer IDs selected from the
player's starter. Qarro's final story canon is one fixed Gary 6v6 team, so this
pass replaces only those three original first-clear party blocks with the same
DESIGN FINAL build while preserving the original starter selector and trainer
headers. Elite Four, rematches, Gyms, ordinary trainers, localization, font,
Ash Bond and Ash Cap are untouched.

The patch is fail-closed: each target must still have its exact pinned-upstream
vanilla species sequence before replacement.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_BOSS_KANTO_CHAMPION_CANON_V3_131"
PARTY_PATH = Path("src/data/trainers_frlg.party")
AUDIT_NAME = "qarro_boss_kanto_champion_canon_v3_131_audit.json"

TARGETS = (
    "TRAINER_CHAMPION_FIRST_SQUIRTLE",
    "TRAINER_CHAMPION_FIRST_BULBASAUR",
    "TRAINER_CHAMPION_FIRST_CHARMANDER",
)

EXPECTED_ORIGINAL = {
    "TRAINER_CHAMPION_FIRST_SQUIRTLE": [
        "Pidgeot", "Alakazam", "Rhydon", "Arcanine", "Exeggutor", "Blastoise"
    ],
    "TRAINER_CHAMPION_FIRST_BULBASAUR": [
        "Pidgeot", "Alakazam", "Rhydon", "Gyarados", "Arcanine", "Venusaur"
    ],
    "TRAINER_CHAMPION_FIRST_CHARMANDER": [
        "Pidgeot", "Alakazam", "Rhydon", "Exeggutor", "Gyarados", "Charizard"
    ],
}

TEAM = [
    {
        "species": "Blastoise", "level": 63, "nature": "Bold",
        "ability": "Torrent", "item": "Leftovers",
        "ivs": "31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe",
        "evs": "252 HP / 252 Def / 4 SpD",
        "moves": ["Scald", "Ice Beam", "Rapid Spin", "Roar"], "ace": True,
    },
    {
        "species": "Alakazam", "level": 62, "nature": "Timid",
        "ability": "Magic Guard", "item": "Life Orb",
        "ivs": "31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe",
        "evs": "4 HP / 252 SpA / 252 Spe",
        "moves": ["Psychic", "Focus Blast", "Shadow Ball", "Calm Mind"], "ace": False,
    },
    {
        "species": "Arcanine", "level": 62, "nature": "Adamant",
        "ability": "Intimidate", "item": "Life Orb",
        "ivs": "31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe",
        "evs": "4 HP / 252 Atk / 252 Spe",
        "moves": ["Flare Blitz", "Extreme Speed", "Wild Charge", "Crunch"], "ace": False,
    },
    {
        "species": "Nidoking", "level": 62, "nature": "Modest",
        "ability": "Sheer Force", "item": "Life Orb",
        "ivs": "31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe",
        "evs": "4 HP / 252 SpA / 252 Spe",
        "moves": ["Earth Power", "Sludge Wave", "Ice Beam", "Thunderbolt"], "ace": False,
    },
    {
        "species": "Scizor", "level": 62, "nature": "Adamant",
        "ability": "Technician", "item": "Choice Band",
        "ivs": "31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe",
        "evs": "4 HP / 252 Atk / 252 Spe",
        "moves": ["Bullet Punch", "U-turn", "Superpower", "Pursuit"], "ace": False,
    },
    {
        "species": "Electivire", "level": 62, "nature": "Jolly",
        "ability": "Motor Drive", "item": "Expert Belt",
        "ivs": "31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe",
        "evs": "4 HP / 252 Atk / 252 Spe",
        "moves": ["Wild Charge", "Ice Punch", "Earthquake", "Cross Chop"], "ace": False,
    },
]

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
    marker = f"=== {trainer} ==="
    start = text.find(marker)
    if start < 0:
        die(f"missing trainer block {trainer}")
    if text.find(marker, start + len(marker)) >= 0:
        die(f"duplicate trainer block {trainer}")
    next_match = re.search(r"(?m)^=== TRAINER_[A-Z0-9_]+ ===$", text[start + len(marker):])
    end = len(text) if next_match is None else start + len(marker) + next_match.start()
    return start, end, text[start:end]


def party_body_start(block: str, trainer: str) -> int:
    # First-clear Champion headers in pinned FireRed end in Mugshot: Yellow.
    match = re.search(r"(?m)^Mugshot: Yellow\s*\n\s*\n", block)
    if not match:
        die(f"unexpected/missing Champion header terminator for {trainer}")
    header = block[:match.end()]
    required = (
        "Class: Champion Frlg", "Pic: Champion Rival Frlg", "Double Battle: No",
        "AI: Check Bad Move / Try To Faint / Check Viability",
        "Items: Full Restore / Full Restore / Full Restore / Full Restore",
    )
    for token in required:
        if token not in header:
            die(f"unexpected Champion header for {trainer}: missing {token!r}")
    return match.end()


def extract_species_from_party(body: str) -> list[str]:
    species: list[str] = []
    for chunk in re.split(r"\n\s*\n", body.strip()):
        if not chunk.strip():
            continue
        first = chunk.splitlines()[0].strip()
        if not first or first.startswith("-") or first.startswith("==="):
            continue
        species.append(first.split(" @ ", 1)[0].strip())
    return species


def render_mon(mon: dict) -> str:
    lines = [
        f"{mon['species']} @ {mon['item']}",
        f"Level: {mon['level']}",
        f"IVs: {mon['ivs']}",
        f"EVs: {mon['evs']}",
        f"{mon['nature']} Nature",
        f"Ability: {mon['ability']}",
    ]
    lines.extend(f"- {move}" for move in mon["moves"])
    return "\n".join(lines)


def validate_canon() -> None:
    if len(TEAM) != 6:
        die(f"Champion canon must contain 6 Pokemon, got {len(TEAM)}")
    species = [mon["species"] for mon in TEAM]
    if species != ["Blastoise", "Alakazam", "Arcanine", "Nidoking", "Scizor", "Electivire"]:
        die(f"unexpected Gary species order: {species}")
    if set(species) & BANNED:
        die(f"Legendary/Mythical leaked into Gary canon: {sorted(set(species) & BANNED)}")
    aces = [mon for mon in TEAM if mon.get("ace")]
    if len(aces) != 1 or aces[0]["species"] != "Blastoise" or aces[0]["level"] != 63:
        die("Gary must have exactly one Lv63 ace: Blastoise")
    for mon in TEAM:
        expected_level = 63 if mon.get("ace") else 62
        if mon["level"] != expected_level:
            die(f"bad level for {mon['species']}: {mon['level']} != {expected_level}")
        if mon["ivs"] != "31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe":
            die(f"non-31 IV spread for {mon['species']}")
        if len(mon["moves"]) != 4:
            die(f"{mon['species']} must have exactly four moves")
        ev_numbers = [int(x) for x in re.findall(r"(\d+)\s+(?:HP|Atk|Def|SpA|SpD|Spe)", mon["evs"])]
        if sum(ev_numbers) != 508:
            # Standard 252/252/4 competitive spread totals 508 effective EVs.
            die(f"unexpected EV total for {mon['species']}: {sum(ev_numbers)}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    path = root / PARTY_PATH
    if not path.is_file():
        die(f"missing {PARTY_PATH}")

    validate_canon()
    text = path.read_text(encoding="utf-8")
    before = text
    audit_targets: dict[str, dict] = {}

    # Replace from later offsets to earlier offsets so stored bounds stay valid.
    replacements = []
    for trainer in TARGETS:
        start, end, block = trainer_bounds(text, trainer)
        body_pos = party_body_start(block, trainer)
        current_species = extract_species_from_party(block[body_pos:])
        expected = EXPECTED_ORIGINAL[trainer]
        if current_species != expected:
            die(f"{trainer} species mismatch: {current_species} != pinned {expected}")
        new_body = "\n\n".join(render_mon(mon) for mon in TEAM) + "\n\n"
        new_block = block[:body_pos] + new_body
        replacements.append((start, end, new_block, trainer, current_species))

    for start, end, new_block, trainer, current_species in sorted(replacements, reverse=True):
        text = text[:start] + new_block + text[end:]
        audit_targets[trainer] = {
            "beforeSpecies": current_species,
            "afterSpecies": [mon["species"] for mon in TEAM],
            "partySize": 6,
            "ace": "Blastoise",
            "aceLevel": 63,
            "nonAceLevel": 62,
        }

    if text == before:
        die("patch produced no changes")

    # Verify exactly the intended three first-clear blocks now carry canon.
    for trainer in TARGETS:
        _, _, block = trainer_bounds(text, trainer)
        body_pos = party_body_start(block, trainer)
        after_species = extract_species_from_party(block[body_pos:])
        expected_after = [mon["species"] for mon in TEAM]
        if after_species != expected_after:
            die(f"post-patch verify failed for {trainer}: {after_species}")

    path.write_text(text, encoding="utf-8")

    audit = {
        "marker": MARKER,
        "partySource": str(PARTY_PATH),
        "targets": audit_targets,
        "fixedGaryTeamAcrossStarterSelectors": True,
        "starterSelectionScriptModified": False,
        "eliteFourTouched": False,
        "championRematchesTouched": False,
        "gymLeadersTouched": False,
        "ordinaryTrainersTouched": False,
        "localizationTouched": False,
        "fontTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    build = root / "build"
    build.mkdir(parents=True, exist_ok=True)
    (build / AUDIT_NAME).write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: installed fixed DESIGN FINAL Gary 6v6 on all three "
        "first-clear Champion IDs; rematches/selector/E4/Gyms/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
