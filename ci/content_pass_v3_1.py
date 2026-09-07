#!/usr/bin/env python3
"""Qarro content pass v3.1 for pinned pokeemerald-expansion 1.17.0 FireRed.

Applied *after* FIRST PLAYABLE v3.0 installer:
- Put visible Gen II-V species into early Kanto wild encounter tables.
- Add five new ordinary route trainers (uses the five remaining safe trainer IDs
  before the original FRLG +25-trainer flag-space comment is exhausted).
- Add several extra item balls / hidden items to early routes.

No Ash Bond / Ash Cap changes are made here.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_CONTENT_V3_1"


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.exists():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def patch_wild(root: Path) -> dict:
    path = root / "src/data/wild_encounters.json"
    data = json.loads(read(path))
    group = next((g for g in data.get("wild_encounter_groups", [])
                  if g.get("for_maps") and g.get("label") == "gWildMonHeaders"), None)
    if group is None:
        die("gWildMonHeaders encounter group not found")

    pools = {
        "MAP_ROUTE1": [
            "SPECIES_PIDGEY", "SPECIES_RATTATA", "SPECIES_PIDGEY", "SPECIES_RATTATA",
            "SPECIES_SPEAROW", "SPECIES_SENTRET", "SPECIES_POOCHYENA", "SPECIES_STARLY",
            "SPECIES_LILLIPUP", "SPECIES_HOOTHOOT", "SPECIES_ZIGZAGOON", "SPECIES_PATRAT",
        ],
        "MAP_ROUTE2": [
            "SPECIES_CATERPIE", "SPECIES_WEEDLE", "SPECIES_PIDGEY", "SPECIES_RATTATA",
            "SPECIES_NIDORAN_M", "SPECIES_SPINARAK", "SPECIES_LEDYBA", "SPECIES_WURMPLE",
            "SPECIES_SHINX", "SPECIES_KRICKETOT", "SPECIES_SEWADDLE", "SPECIES_VENIPEDE",
        ],
        "MAP_VIRIDIAN_FOREST": [
            "SPECIES_CATERPIE", "SPECIES_WEEDLE", "SPECIES_METAPOD", "SPECIES_KAKUNA",
            "SPECIES_PIKACHU", "SPECIES_LEDYBA", "SPECIES_SPINARAK", "SPECIES_WURMPLE",
            "SPECIES_SHROOMISH", "SPECIES_BUDEW", "SPECIES_SEWADDLE", "SPECIES_VENIPEDE",
        ],
        "MAP_ROUTE3": [
            "SPECIES_SPEAROW", "SPECIES_SANDSHREW", "SPECIES_JIGGLYPUFF", "SPECIES_MANKEY",
            "SPECIES_NIDORAN_F", "SPECIES_MAREEP", "SPECIES_TAILLOW", "SPECIES_SHINX",
            "SPECIES_BIDOOF", "SPECIES_BLITZLE", "SPECIES_PIDOVE", "SPECIES_TIMBURR",
        ],
        "MAP_MT_MOON_1F": [
            "SPECIES_ZUBAT", "SPECIES_GEODUDE", "SPECIES_PARAS", "SPECIES_CLEFAIRY",
            "SPECIES_WOOPER", "SPECIES_ARON", "SPECIES_NOSEPASS", "SPECIES_BRONZOR",
            "SPECIES_ROGGENROLA", "SPECIES_WOOBAT", "SPECIES_DRILBUR", "SPECIES_TIMBURR",
        ],
        "MAP_MT_MOON_B1F": [
            "SPECIES_ZUBAT", "SPECIES_GEODUDE", "SPECIES_PARAS", "SPECIES_CLEFAIRY",
            "SPECIES_WOOPER", "SPECIES_ARON", "SPECIES_NOSEPASS", "SPECIES_BRONZOR",
            "SPECIES_ROGGENROLA", "SPECIES_WOOBAT", "SPECIES_DRILBUR", "SPECIES_TIMBURR",
        ],
        "MAP_ROUTE4": [
            "SPECIES_SPEAROW", "SPECIES_EKANS", "SPECIES_SANDSHREW", "SPECIES_MANKEY",
            "SPECIES_MAREEP", "SPECIES_HOPPIP", "SPECIES_WINGULL", "SPECIES_SHINX",
            "SPECIES_BUIZEL", "SPECIES_PATRAT", "SPECIES_PIDOVE", "SPECIES_MINCCINO",
        ],
    }

    species_text = read(root / "include/constants/species.h")
    for species in {s for p in pools.values() for s in p}:
        if species not in species_text:
            die(f"species constant missing in pinned source: {species}")

    found = {}
    for rec in group.get("encounters", []):
        if "FireRed" not in rec.get("base_label", ""):
            continue
        map_name = rec.get("map")
        if map_name not in pools or "land_mons" not in rec:
            continue
        mons = rec["land_mons"].get("mons", [])
        if len(mons) != 12:
            die(f"{map_name}: expected 12 land slots, got {len(mons)}")
        before = [m.get("species") for m in mons]
        for mon, species in zip(mons, pools[map_name]):
            mon["species"] = species
        found[map_name] = {"before": before, "after": pools[map_name]}

    required = {"MAP_ROUTE1", "MAP_ROUTE2", "MAP_ROUTE3", "MAP_ROUTE4"}
    if not required.issubset(found):
        die(f"missing early FireRed encounter records: {sorted(required - set(found))}")

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] wild encounters patched: {len(found)} maps")
    return found


def patch_trainer_ids(root: Path) -> None:
    path = root / "include/constants/opponents_frlg.h"
    text = read(path)
    if "TRAINER_QARRO_ROUTE1_NIKO" in text:
        return
    anchor = "#define TRAINERS_COUNT_FRLG                      644"
    if anchor not in text:
        die("expected FIRST PLAYABLE TRAINERS_COUNT_FRLG 644 anchor not found")
    block = """/* QARRO_CONTENT_V3_1_TRAINERS_BEGIN */
#define TRAINER_QARRO_ROUTE1_NIKO                         644
#define TRAINER_QARRO_ROUTE1_MIRA                         645
#define TRAINER_QARRO_ROUTE2_LEO                          646
#define TRAINER_QARRO_ROUTE2_AYA                          647
#define TRAINER_QARRO_ROUTE4_TOM                          648
/* QARRO_CONTENT_V3_1_TRAINERS_END */

#define TRAINERS_COUNT_FRLG                      649"""
    text = text.replace(anchor, block, 1)
    write(path, text)
    print(f"[{MARKER}] added trainer IDs 644-648; count=649")


def patch_trainer_parties(root: Path) -> None:
    path = root / "src/data/trainers_frlg.party"
    text = read(path)
    if "=== TRAINER_QARRO_ROUTE1_NIKO ===" in text:
        return
    block = r'''

# QARRO_CONTENT_V3_1_TRAINERS_BEGIN
=== TRAINER_QARRO_ROUTE1_NIKO ===
Name: NIKO
Class: Youngster Frlg
Pic: Youngster Frlg
Gender: Male
Music: Male
Double Battle: No
AI: Basic Trainer / Smart Switching / HP Aware

Sentret
Level: 5
IVs: 8 HP / 8 Atk / 8 Def / 8 SpA / 8 SpD / 8 Spe

Poochyena
Level: 5
IVs: 8 HP / 8 Atk / 8 Def / 8 SpA / 8 SpD / 8 Spe

Patrat
Level: 6
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe

=== TRAINER_QARRO_ROUTE1_MIRA ===
Name: MIRA
Class: Lass Frlg
Pic: Lass Frlg
Gender: Female
Music: Female
Double Battle: No
AI: Basic Trainer / Smart Switching / HP Aware

Hoothoot
Level: 5
IVs: 8 HP / 8 Atk / 8 Def / 8 SpA / 8 SpD / 8 Spe

Starly
Level: 5
IVs: 8 HP / 8 Atk / 8 Def / 8 SpA / 8 SpD / 8 Spe

Pidove
Level: 6
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe

=== TRAINER_QARRO_ROUTE2_LEO ===
Name: LEO
Class: Youngster Frlg
Pic: Youngster Frlg
Gender: Male
Music: Male
Double Battle: No
AI: Basic Trainer / Smart Switching / HP Aware

Mareep
Level: 8
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe

Shinx
Level: 8
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe

Blitzle
Level: 9
IVs: 14 HP / 14 Atk / 14 Def / 14 SpA / 14 SpD / 14 Spe

=== TRAINER_QARRO_ROUTE2_AYA ===
Name: AYA
Class: Bug Catcher Frlg
Pic: Bug Catcher Frlg
Gender: Female
Music: Female
Double Battle: No
AI: Basic Trainer / Smart Switching / HP Aware

Spinarak
Level: 8
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe

Wurmple
Level: 8
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe

Sewaddle
Level: 9
IVs: 14 HP / 14 Atk / 14 Def / 14 SpA / 14 SpD / 14 Spe

=== TRAINER_QARRO_ROUTE4_TOM ===
Name: TOM
Class: Youngster Frlg
Pic: Youngster Frlg
Gender: Male
Music: Male
Double Battle: No
AI: Basic Trainer / Smart Switching / HP Aware

Wooper
Level: 16
IVs: 16 HP / 16 Atk / 16 Def / 16 SpA / 16 SpD / 16 Spe

Wingull
Level: 16
IVs: 16 HP / 16 Atk / 16 Def / 16 SpA / 16 SpD / 16 Spe

Buizel
Level: 17
IVs: 18 HP / 18 Atk / 18 Def / 18 SpA / 18 SpD / 18 Spe
# QARRO_CONTENT_V3_1_TRAINERS_END
'''
    write(path, text.rstrip() + block + "\n")
    print(f"[{MARKER}] appended 5 multi-generation route trainer parties")


def add_object(map_data: dict, obj: dict, script: str) -> None:
    objs = map_data.setdefault("object_events", [])
    if any(o.get("script") == script for o in objs if isinstance(o, dict)):
        return
    objs.append(obj)


def add_hidden_item(map_data: dict, *, x: int, y: int, item: str, flag: str) -> None:
    bg = map_data.setdefault("bg_events", [])
    if any(e.get("flag") == flag for e in bg if isinstance(e, dict)):
        return
    bg.append({
        "type": "hidden_item", "x": x, "y": y, "elevation": 3,
        "item": item, "flag": flag, "quantity": 1, "underfoot": False,
    })


def patch_map(root: Path, map_dir: str, objects: list[dict], hidden: list[dict]) -> None:
    path = root / f"data/maps/{map_dir}/map.json"
    data = json.loads(read(path))
    for obj in objects:
        add_object(data, obj, obj["script"])
    for h in hidden:
        add_hidden_item(data, **h)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] map content patched: {map_dir}")


def trainer_obj(gfx: str, x: int, y: int, movement: str, sight: int, script: str) -> dict:
    return {
        "type": "object", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
        "movement_type": movement, "movement_range_x": 1, "movement_range_y": 1,
        "trainer_type": "TRAINER_TYPE_NORMAL", "trainer_sight_or_berry_tree_id": str(sight),
        "script": script, "flag": "0",
    }


def item_obj(x: int, y: int, script: str, flag: str) -> dict:
    return {
        "type": "object", "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": x, "y": y, "elevation": 3,
        "movement_type": "MOVEMENT_TYPE_FACE_DOWN", "movement_range_x": 1, "movement_range_y": 1,
        "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
        "script": script, "flag": flag,
    }


def append_scripts(path: Path, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def patch_route_scripts(root: Path) -> None:
    append_scripts(root / "data/maps/Route1_Frlg/scripts.inc", "QarroV31_Route1",
'''# QarroV31_Route1
Route1_EventScript_QarroNiko::
    trainerbattle_single TRAINER_QARRO_ROUTE1_NIKO, Route1_Text_QarroNikoIntro, Route1_Text_QarroNikoDefeat
    msgbox Route1_Text_QarroNikoPost, MSGBOX_AUTOCLOSE
    end

Route1_EventScript_QarroMira::
    trainerbattle_single TRAINER_QARRO_ROUTE1_MIRA, Route1_Text_QarroMiraIntro, Route1_Text_QarroMiraDefeat
    msgbox Route1_Text_QarroMiraPost, MSGBOX_AUTOCLOSE
    end

Route1_EventScript_QarroItemPokeballs::
    giveitem ITEM_POKE_BALL, 5
    end

Route1_EventScript_QarroItemPotion::
    giveitem ITEM_POTION, 2
    end

Route1_Text_QarroNikoIntro:
    .string "KANTO isn't the whole world!\\nLet's battle!$"
Route1_Text_QarroNikoDefeat:
    .string "Okay, your team is stronger!$"
Route1_Text_QarroNikoPost:
    .string "You'll meet POKéMON from many regions.$"
Route1_Text_QarroMiraIntro:
    .string "My POKéMON came from far away.\\nReady?$"
Route1_Text_QarroMiraDefeat:
    .string "That was a good battle!$"
Route1_Text_QarroMiraPost:
    .string "Different regions mean different tactics.$"''')

    append_scripts(root / "data/maps/Route2_Frlg/scripts.inc", "QarroV31_Route2",
'''# QarroV31_Route2
Route2_EventScript_QarroLeo::
    trainerbattle_single TRAINER_QARRO_ROUTE2_LEO, Route2_Text_QarroLeoIntro, Route2_Text_QarroLeoDefeat
    msgbox Route2_Text_QarroLeoPost, MSGBOX_AUTOCLOSE
    end

Route2_EventScript_QarroAya::
    trainerbattle_single TRAINER_QARRO_ROUTE2_AYA, Route2_Text_QarroAyaIntro, Route2_Text_QarroAyaDefeat
    msgbox Route2_Text_QarroAyaPost, MSGBOX_AUTOCLOSE
    end

Route2_EventScript_QarroItemRepel::
    giveitem ITEM_REPEL, 2
    end

Route2_Text_QarroLeoIntro:
    .string "Electric POKéMON aren't just PIKACHU!$"
Route2_Text_QarroLeoDefeat:
    .string "You grounded my plan!$"
Route2_Text_QarroLeoPost:
    .string "I'll train with POKéMON from every region.$"
Route2_Text_QarroAyaIntro:
    .string "Bugs evolved in every region.\\nTake a look!$"
Route2_Text_QarroAyaDefeat:
    .string "My bugs need more training!$"
Route2_Text_QarroAyaPost:
    .string "Forests hide many different species.$"''')

    append_scripts(root / "data/maps/Route4_Frlg/scripts.inc", "QarroV31_Route4",
'''# QarroV31_Route4
Route4_EventScript_QarroTom::
    trainerbattle_single TRAINER_QARRO_ROUTE4_TOM, Route4_Text_QarroTomIntro, Route4_Text_QarroTomDefeat
    msgbox Route4_Text_QarroTomPost, MSGBOX_AUTOCLOSE
    end

Route4_Text_QarroTomIntro:
    .string "I trained by MT. MOON.\\nLet's see what you learned!$"
Route4_Text_QarroTomDefeat:
    .string "You made it through!$"
Route4_Text_QarroTomPost:
    .string "Your PC will need room for many species.$"''')


def patch_maps(root: Path) -> None:
    patch_map(root, "Route1_Frlg", [
        trainer_obj("OBJ_EVENT_GFX_YOUNGSTER_FRLG", 12, 24, "MOVEMENT_TYPE_FACE_DOWN", 4, "Route1_EventScript_QarroNiko"),
        trainer_obj("OBJ_EVENT_GFX_LASS_FRLG", 15, 11, "MOVEMENT_TYPE_FACE_LEFT", 3, "Route1_EventScript_QarroMira"),
        item_obj(8, 27, "Route1_EventScript_QarroItemPokeballs", "FLAG_0x0AF"),
        item_obj(18, 17, "Route1_EventScript_QarroItemPotion", "FLAG_0x0B0"),
    ], [
        {"x": 7, "y": 29, "item": "ITEM_ORAN_BERRY", "flag": "FLAG_0x0B4"},
    ])

    patch_map(root, "Route2_Frlg", [
        trainer_obj("OBJ_EVENT_GFX_YOUNGSTER_FRLG", 8, 72, "MOVEMENT_TYPE_FACE_DOWN", 4, "Route2_EventScript_QarroLeo"),
        trainer_obj("OBJ_EVENT_GFX_BUG_CATCHER_FRLG", 16, 55, "MOVEMENT_TYPE_FACE_LEFT", 3, "Route2_EventScript_QarroAya"),
        item_obj(16, 64, "Route2_EventScript_QarroItemRepel", "FLAG_0x0B1"),
    ], [
        {"x": 16, "y": 54, "item": "ITEM_SUPER_POTION", "flag": "FLAG_0x0B5"},
    ])

    patch_map(root, "Route3_Frlg", [], [
        {"x": 27, "y": 9, "item": "ITEM_GREAT_BALL", "flag": "FLAG_0x0B2"},
    ])

    patch_map(root, "Route4_Frlg", [
        trainer_obj("OBJ_EVENT_GFX_YOUNGSTER_FRLG", 72, 5, "MOVEMENT_TYPE_FACE_LEFT", 3, "Route4_EventScript_QarroTom"),
    ], [
        {"x": 68, "y": 17, "item": "ITEM_SUPER_REPEL", "flag": "FLAG_0x0B3"},
    ])

    patch_route_scripts(root)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not (root / "Makefile").exists():
        die("target is not a pokeemerald-expansion checkout")

    wild = patch_wild(root)
    patch_trainer_ids(root)
    patch_trainer_parties(root)
    patch_maps(root)

    audit = {
        "version": "v3.1-content-pass-1",
        "wildMapsPatched": sorted(wild),
        "newTrainerIds": [644, 645, 646, 647, 648],
        "newTrainerCount": 5,
        "visibleItemBallsAdded": 3,
        "hiddenItemsAdded": 4,
        "startersAddedToOrdinaryWild": False,
        "legendaryMythicalAddedToOrdinaryWild": False,
        "ashBondTouched": False,
        "ashCapTouched": False
    }
    out = root / "build/qarro_content_v3_1_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: content pass applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
