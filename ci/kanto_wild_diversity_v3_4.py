#!/usr/bin/env python3
"""Qarro v3.4 full FireRed/Kanto land-encounter diversity pass.

Runs after v3.3. Early maps explicitly designed in v3.3 are kept intact. Every
other FireRed land table keeps its three highest-frequency vanilla slots, then
receives biome-appropriate Gen II-V species in the remaining slots.

With the standard 12-slot encounter weights this leaves roughly half of each
late table as its original Kanto core while making Gen II/III/IV/V consistently
available. Levels and encounter rates are never changed.

No starters, Legendary/Mythical species, Gen VI+ species, Ash Bond or Ash Cap.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_KANTO_WILD_V3_4"

# Each biome supplies multiple species from each later generation. Selection is
# deterministic per map so neighboring locations are diverse without RNG builds.
BIOMES = {
    "route": {
        2: ["SPECIES_HOPPIP", "SPECIES_MAREEP", "SPECIES_SENTRET"],
        3: ["SPECIES_ZIGZAGOON", "SPECIES_SHROOMISH", "SPECIES_ELECTRIKE"],
        4: ["SPECIES_BUDEW", "SPECIES_SHINX", "SPECIES_STARLY"],
        5: ["SPECIES_LILLIPUP", "SPECIES_DEERLING", "SPECIES_SEWADDLE"],
    },
    "forest": {
        2: ["SPECIES_HOPPIP", "SPECIES_SPINARAK", "SPECIES_PINECO"],
        3: ["SPECIES_SHROOMISH", "SPECIES_SEEDOT", "SPECIES_WURMPLE"],
        4: ["SPECIES_BUDEW", "SPECIES_KRICKETOT", "SPECIES_BURMY"],
        5: ["SPECIES_SEWADDLE", "SPECIES_COTTONEE", "SPECIES_PETILIL"],
    },
    "cave": {
        2: ["SPECIES_LARVITAR", "SPECIES_WOOPER", "SPECIES_SNEASEL"],
        3: ["SPECIES_ARON", "SPECIES_MAWILE", "SPECIES_MAKUHITA"],
        4: ["SPECIES_BRONZOR", "SPECIES_RIOLU", "SPECIES_HIPPOPOTAS"],
        5: ["SPECIES_ROGGENROLA", "SPECIES_KLINK", "SPECIES_TIMBURR"],
    },
    "ghost": {
        2: ["SPECIES_MISDREAVUS", "SPECIES_MURKROW", "SPECIES_SNEASEL"],
        3: ["SPECIES_SHUPPET", "SPECIES_DUSKULL", "SPECIES_SABLEYE"],
        4: ["SPECIES_DRIFLOON", "SPECIES_BRONZOR", "SPECIES_SKORUPI"],
        5: ["SPECIES_LITWICK", "SPECIES_YAMASK", "SPECIES_FRILLISH"],
    },
    "electric": {
        2: ["SPECIES_MAREEP", "SPECIES_ELEKID", "SPECIES_CHINCHOU"],
        3: ["SPECIES_ELECTRIKE", "SPECIES_PLUSLE", "SPECIES_MINUN"],
        4: ["SPECIES_SHINX", "SPECIES_ROTOM", "SPECIES_BRONZOR"],
        5: ["SPECIES_BLITZLE", "SPECIES_KLINK", "SPECIES_EMOLGA"],
    },
    "fire": {
        2: ["SPECIES_SLUGMA", "SPECIES_HOUNDOUR", "SPECIES_MAGBY"],
        3: ["SPECIES_NUMEL", "SPECIES_TORKOAL", "SPECIES_CACNEA"],
        4: ["SPECIES_HIPPOPOTAS", "SPECIES_SKORUPI", "SPECIES_BRONZOR"],
        5: ["SPECIES_DARUMAKA", "SPECIES_LITWICK", "SPECIES_SANDILE"],
    },
    "ice": {
        2: ["SPECIES_SNEASEL", "SPECIES_DELIBIRD", "SPECIES_SWINUB"],
        3: ["SPECIES_SNORUNT", "SPECIES_SPHEAL", "SPECIES_SABLEYE"],
        4: ["SPECIES_SNOVER", "SPECIES_FROSLASS", "SPECIES_BRONZOR"],
        5: ["SPECIES_CUBCHOO", "SPECIES_VANILLITE", "SPECIES_CRYOGONAL"],
    },
    "safari": {
        2: ["SPECIES_GIRAFARIG", "SPECIES_PHANPY", "SPECIES_HOUNDOUR"],
        3: ["SPECIES_TROPIUS", "SPECIES_KECLEON", "SPECIES_CACNEA"],
        4: ["SPECIES_CARNIVINE", "SPECIES_SKORUPI", "SPECIES_HIPPOPOTAS"],
        5: ["SPECIES_MARACTUS", "SPECIES_DEERLING", "SPECIES_MINCCINO"],
    },
}

# Standard FireRed 12-slot weights are approximately
# 20,20,10,10,10,10,5,5,4,4,1,1. Keep slots 0-2 untouched (50% total).
# Replacement weight by generation is ~19% Gen II, 15% Gen III,
# 11% Gen IV, 5% Gen V: close to the project's Kanto regional bias while
# preserving a majority/near-majority Kanto identity on each late map.
SLOTS_BY_GEN = {
    2: [3, 6, 8],
    3: [4, 7],
    4: [5, 10],
    5: [9, 11],
}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def biome_for(map_name: str) -> str:
    name = map_name.upper()
    if "POWER_PLANT" in name:
        return "electric"
    if any(x in name for x in ("POKEMON_TOWER", "LOST_CAVE")):
        return "ghost"
    if "SEAFOAM" in name:
        return "ice"
    if any(x in name for x in ("POKEMON_MANSION", "MT_EMBER")):
        return "fire"
    if "SAFARI_ZONE" in name:
        return "safari"
    if any(x in name for x in ("BERRY_FOREST", "PATTERN_BUSH", "VIRIDIAN_FOREST")):
        return "forest"
    if any(x in name for x in (
        "ROCK_TUNNEL", "VICTORY_ROAD", "CERULEAN_CAVE", "DIGLETTS_CAVE",
        "MT_MOON", "ALTERING_CAVE",
    )):
        return "cave"
    return "route"


def deterministic_pick(pool: list[str], map_name: str, offset: int) -> str:
    seed = sum((i + 1) * ord(ch) for i, ch in enumerate(map_name))
    return pool[(seed + offset) % len(pool)]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    path = root / "src/data/wild_encounters.json"
    if not path.exists():
        die(f"missing {path}")
    data = json.loads(path.read_text(encoding="utf-8"))

    # Read v3.3 audit so we preserve exactly the hand-designed early tables that
    # were actually found/patched on this pinned FireRed source.
    audit_path = root / "build/qarro_runtime_v3_3_audit.json"
    if not audit_path.exists():
        die("v3.3 runtime audit missing; refusing to guess early-map ownership")
    v33 = json.loads(audit_path.read_text(encoding="utf-8"))
    explicit_maps = set(v33.get("wild", {}).get("mapsPatched", []))
    if not explicit_maps:
        die("v3.3 audit contains no explicitly patched wild maps")

    species_header = (root / "include/constants/species.h").read_text(encoding="utf-8")
    requested = {species for biome in BIOMES.values() for pool in biome.values() for species in pool}
    missing_species = sorted(species for species in requested if species not in species_header)
    if missing_species:
        die(f"missing species constants in pinned source: {missing_species}")

    group = next((g for g in data.get("wild_encounter_groups", [])
                  if g.get("for_maps") and g.get("label") == "gWildMonHeaders"), None)
    if group is None:
        die("gWildMonHeaders encounter group not found")

    patched = []
    skipped_explicit = []
    biome_counts = {name: 0 for name in BIOMES}
    for rec in group.get("encounters", []):
        map_name = rec.get("map")
        if not isinstance(map_name, str):
            continue
        if "FireRed" not in rec.get("base_label", ""):
            continue
        land = rec.get("land_mons")
        if not isinstance(land, dict):
            continue
        mons = land.get("mons", [])
        if len(mons) != 12:
            die(f"{map_name}: expected 12 FireRed land slots, got {len(mons)}")
        if map_name in explicit_maps:
            skipped_explicit.append(map_name)
            continue

        biome = biome_for(map_name)
        pools = BIOMES[biome]
        before = [m.get("species") for m in mons]
        for gen, slots in SLOTS_BY_GEN.items():
            pool = pools[gen]
            for offset, slot in enumerate(slots):
                mons[slot]["species"] = deterministic_pick(pool, map_name, offset)
        after = [m.get("species") for m in mons]
        if before != after:
            patched.append({"map": map_name, "biome": biome, "before": before, "after": after})
            biome_counts[biome] += 1

    if not patched:
        die("no additional FireRed land tables were patched")

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out = root / "build/qarro_kanto_wild_v3_4_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "explicitV33MapsPreserved": sorted(skipped_explicit),
        "additionalFireRedLandMapsPatched": len(patched),
        "biomeCounts": biome_counts,
        "maps": patched,
        "levelsChanged": False,
        "encounterRatesChanged": False,
        "startersAddedToOrdinaryWild": False,
        "legendaryMythicalAddedToOrdinaryWild": False,
        "gen6PlusAdded": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: diversified {len(patched)} additional FireRed land maps; "
        f"preserved {len(skipped_explicit)} explicit v3.3 maps; biomes={biome_counts}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
