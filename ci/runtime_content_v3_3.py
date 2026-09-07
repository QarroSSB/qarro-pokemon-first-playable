#!/usr/bin/env python3
"""Qarro v3.3 runtime content corrections.

Applied after the proven v3.1 content pass and v3.2 Kanto balance pass.

Goals:
- Remove the two custom Route 1 item balls that were placed before Viridian City.
- Make the remaining custom visible item ball use FireRed's standard `finditem`
  flow so its object flag is set and the ball stays gone after pickup.
- Broaden early FireRed land encounters with Gen I-V species, with extra Grass,
  Fighting and Steel representation while preserving the original slot levels.

Ordinary wild tables never add starters, Legendary/Mythical species or Gen VI+.
No Ash Bond / Ash Cap code is touched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RUNTIME_V3_3"


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.exists():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def patch_item_balls(root: Path) -> dict:
    # These two objects were accidentally placed before the first city in v3.1.
    # Remove only those exact custom objects; vanilla Route 1 content is untouched.
    route1 = root / "data/maps/Route1_Frlg/map.json"
    data = json.loads(read(route1))
    scripts_to_remove = {
        "Route1_EventScript_QarroItemPokeballs",
        "Route1_EventScript_QarroItemPotion",
    }
    before = list(data.get("object_events", []))
    removed = [obj for obj in before if obj.get("script") in scripts_to_remove]
    if len(removed) != 2:
        die(f"Route1: expected exactly 2 pre-Viridian Qarro item balls, got {len(removed)}")
    data["object_events"] = [obj for obj in before if obj.get("script") not in scripts_to_remove]
    route1.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # FireRed's normal visible pickup scripts use `finditem`, which runs the
    # standard find-item flow and causes the selected object's visibility flag
    # to be set. v3.1 used `giveitem`, so the ball could be collected repeatedly.
    route2 = root / "data/maps/Route2_Frlg/scripts.inc"
    text = read(route2)
    old = """Route2_EventScript_QarroItemRepel::\n    giveitem ITEM_REPEL, 2\n    end\n"""
    new = """Route2_EventScript_QarroItemRepel::\n    finditem ITEM_REPEL\n    end\n"""
    if new in text:
        pass
    elif old in text:
        text = text.replace(old, new, 1)
        route2.write_text(text, encoding="utf-8")
    else:
        die("Route2 custom Repel item script did not match v3.1 baseline")

    print(f"[{MARKER}] item balls: removed 2 pre-Viridian objects; Route2 pickup now uses finditem")
    return {
        "preViridianItemBallsRemoved": 2,
        "route2PersistentPickupFixed": True,
    }


# Core v3.1 maps are required. Extra nearby maps are patched when their FireRed
# land tables exist, so early Kanto does not abruptly fall back to vanilla-only
# species after one screen/cave floor.
POOLS = {
    "MAP_ROUTE1": [
        "SPECIES_PIDGEY", "SPECIES_ODDISH", "SPECIES_SENTRET", "SPECIES_HOPPIP",
        "SPECIES_POOCHYENA", "SPECIES_SEEDOT", "SPECIES_STARLY", "SPECIES_BUDEW",
        "SPECIES_LILLIPUP", "SPECIES_SEWADDLE", "SPECIES_MANKEY", "SPECIES_FERROSEED",
    ],
    "MAP_ROUTE2": [
        "SPECIES_CATERPIE", "SPECIES_BELLSPROUT", "SPECIES_SPINARAK", "SPECIES_HOPPIP",
        "SPECIES_WURMPLE", "SPECIES_SHROOMISH", "SPECIES_KRICKETOT", "SPECIES_BUDEW",
        "SPECIES_SEWADDLE", "SPECIES_PETILIL", "SPECIES_MANKEY", "SPECIES_MAGNEMITE",
    ],
    "MAP_VIRIDIAN_FOREST": [
        "SPECIES_CATERPIE", "SPECIES_WEEDLE", "SPECIES_PIKACHU", "SPECIES_HOPPIP",
        "SPECIES_PINECO", "SPECIES_SHROOMISH", "SPECIES_SEEDOT", "SPECIES_BUDEW",
        "SPECIES_BRONZOR", "SPECIES_SEWADDLE", "SPECIES_COTTONEE", "SPECIES_FERROSEED",
    ],
    "MAP_ROUTE3": [
        "SPECIES_SPEAROW", "SPECIES_MANKEY", "SPECIES_HOPPIP", "SPECIES_MAREEP",
        "SPECIES_MAKUHITA", "SPECIES_ARON", "SPECIES_SHINX", "SPECIES_RIOLU",
        "SPECIES_BUDEW", "SPECIES_TIMBURR", "SPECIES_DEERLING", "SPECIES_KLINK",
    ],
    "MAP_MT_MOON_1F": [
        "SPECIES_ZUBAT", "SPECIES_GEODUDE", "SPECIES_MACHOP", "SPECIES_ONIX",
        "SPECIES_WOOPER", "SPECIES_PINECO", "SPECIES_MAKUHITA", "SPECIES_ARON",
        "SPECIES_BRONZOR", "SPECIES_RIOLU", "SPECIES_ROGGENROLA", "SPECIES_KLINK",
    ],
    "MAP_MT_MOON_B1F": [
        "SPECIES_ZUBAT", "SPECIES_GEODUDE", "SPECIES_MACHOP", "SPECIES_CLEFAIRY",
        "SPECIES_WOOPER", "SPECIES_PINECO", "SPECIES_MAWILE", "SPECIES_ARON",
        "SPECIES_BRONZOR", "SPECIES_RIOLU", "SPECIES_FERROSEED", "SPECIES_TIMBURR",
    ],
    "MAP_MT_MOON_B2F": [
        "SPECIES_ZUBAT", "SPECIES_GEODUDE", "SPECIES_CLEFAIRY", "SPECIES_MACHOP",
        "SPECIES_WOOPER", "SPECIES_PINECO", "SPECIES_ARON", "SPECIES_MAWILE",
        "SPECIES_BRONZOR", "SPECIES_RIOLU", "SPECIES_FERROSEED", "SPECIES_KLINK",
    ],
    "MAP_ROUTE4": [
        "SPECIES_SPEAROW", "SPECIES_ODDISH", "SPECIES_MANKEY", "SPECIES_HOPPIP",
        "SPECIES_MAREEP", "SPECIES_SEEDOT", "SPECIES_MAKUHITA", "SPECIES_ARON",
        "SPECIES_BUDEW", "SPECIES_RIOLU", "SPECIES_DEERLING", "SPECIES_TIMBURR",
    ],
    "MAP_ROUTE22": [
        "SPECIES_NIDORAN_M", "SPECIES_MANKEY", "SPECIES_ODDISH", "SPECIES_HOPPIP",
        "SPECIES_MAREEP", "SPECIES_POOCHYENA", "SPECIES_SEEDOT", "SPECIES_STARLY",
        "SPECIES_BUDEW", "SPECIES_LILLIPUP", "SPECIES_DEERLING", "SPECIES_TIMBURR",
    ],
    "MAP_ROUTE5": [
        "SPECIES_ODDISH", "SPECIES_BELLSPROUT", "SPECIES_MEOWTH", "SPECIES_HOPPIP",
        "SPECIES_MAREEP", "SPECIES_SHROOMISH", "SPECIES_ELECTRIKE", "SPECIES_BUDEW",
        "SPECIES_RIOLU", "SPECIES_DEERLING", "SPECIES_TIMBURR", "SPECIES_KLINK",
    ],
    "MAP_ROUTE6": [
        "SPECIES_ODDISH", "SPECIES_BELLSPROUT", "SPECIES_MEOWTH", "SPECIES_HOPPIP",
        "SPECIES_MAREEP", "SPECIES_SHROOMISH", "SPECIES_ELECTRIKE", "SPECIES_BUDEW",
        "SPECIES_RIOLU", "SPECIES_DEERLING", "SPECIES_TIMBURR", "SPECIES_MAGNEMITE",
    ],
    "MAP_ROUTE24": [
        "SPECIES_ODDISH", "SPECIES_BELLSPROUT", "SPECIES_ABRA", "SPECIES_HOPPIP",
        "SPECIES_MAREEP", "SPECIES_SHROOMISH", "SPECIES_MAKUHITA", "SPECIES_BUDEW",
        "SPECIES_RIOLU", "SPECIES_PETILIL", "SPECIES_TIMBURR", "SPECIES_FERROSEED",
    ],
    "MAP_ROUTE25": [
        "SPECIES_ODDISH", "SPECIES_BELLSPROUT", "SPECIES_ABRA", "SPECIES_HOPPIP",
        "SPECIES_MAREEP", "SPECIES_SEEDOT", "SPECIES_MAKUHITA", "SPECIES_BUDEW",
        "SPECIES_RIOLU", "SPECIES_COTTONEE", "SPECIES_TIMBURR", "SPECIES_KLINK",
    ],
}

REQUIRED_CORE = {
    "MAP_ROUTE1", "MAP_ROUTE2", "MAP_VIRIDIAN_FOREST", "MAP_ROUTE3",
    "MAP_MT_MOON_1F", "MAP_MT_MOON_B1F", "MAP_ROUTE4",
}

FORBIDDEN_ORDINARY_WILD = (
    "BULBASAUR", "IVYSAUR", "VENUSAUR", "CHARMANDER", "CHARMELEON", "CHARIZARD",
    "SQUIRTLE", "WARTORTLE", "BLASTOISE", "CHIKORITA", "CYNDAQUIL", "TOTODILE",
    "TREECKO", "TORCHIC", "MUDKIP", "TURTWIG", "CHIMCHAR", "PIPLUP",
    "SNIVY", "TEPIG", "OSHAWOTT",
)


def patch_wild(root: Path) -> dict:
    path = root / "src/data/wild_encounters.json"
    data = json.loads(read(path))
    group = next((g for g in data.get("wild_encounter_groups", [])
                  if g.get("for_maps") and g.get("label") == "gWildMonHeaders"), None)
    if group is None:
        die("gWildMonHeaders encounter group not found")

    species_text = read(root / "include/constants/species.h")
    all_species = {s for pool in POOLS.values() for s in pool}
    for species in sorted(all_species):
        if species not in species_text:
            die(f"species constant missing in pinned source: {species}")
        if any(name in species for name in FORBIDDEN_ORDINARY_WILD):
            die(f"starter family accidentally requested for ordinary wild table: {species}")

    found: dict[str, dict] = {}
    for rec in group.get("encounters", []):
        map_name = rec.get("map")
        if map_name not in POOLS or "FireRed" not in rec.get("base_label", ""):
            continue
        land = rec.get("land_mons")
        if not isinstance(land, dict):
            continue
        mons = land.get("mons", [])
        if len(mons) != 12:
            die(f"{map_name}: expected 12 FireRed land slots, got {len(mons)}")
        before = [m.get("species") for m in mons]
        after = POOLS[map_name]
        for mon, species in zip(mons, after):
            mon["species"] = species
        found[map_name] = {"before": before, "after": after}

    missing_core = sorted(REQUIRED_CORE - set(found))
    if missing_core:
        die(f"missing required early FireRed encounter records: {missing_core}")

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    optional_patched = sorted(set(found) - REQUIRED_CORE)
    optional_missing = sorted((set(POOLS) - REQUIRED_CORE) - set(found))
    print(
        f"[{MARKER}] wild encounters: patched {len(found)} FireRed maps; "
        f"optional patched={optional_patched}; optional absent={optional_missing}"
    )
    return {
        "mapsPatched": sorted(found),
        "optionalMissing": optional_missing,
        "grassFightingSteelBias": True,
        "genRange": "I-V",
        "startersAddedToOrdinaryWild": False,
        "legendaryMythicalAddedToOrdinaryWild": False,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    item_audit = patch_item_balls(root)
    wild_audit = patch_wild(root)

    audit = {
        "marker": MARKER,
        "items": item_audit,
        "wild": wild_audit,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_runtime_v3_3_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: runtime items + early Gen I-V encounters corrected; Ash code untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
