#!/usr/bin/env python3
"""Qarro runtime wrapper: proven Build 249 v3.3 + post-Viridian item pass.

Preserves the exact green Build 249 runtime-content implementation, then applies
our confirmed ground-item rule:
- no custom accessible ground/hidden pickups before Viridian City;
- custom pickups begin on Route 2 and use visible persistent item balls;
- Route 2 / Route 3 / Route 4 early progression gets useful, modest supplies;
- wild encounter work from v3.3 is preserved exactly;
- Ash Bond / Ash Cap remain untouched.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "cdce73eba8ca7c7b6c2ef12eca199e197abe2687"
BASE_PATH = "ci/runtime_content_v3_3.py"
MARKER = "QARRO_GROUND_ITEMS_V3_23"


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.is_file():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def load_base(repo: Path) -> dict:
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )
    ns = {"__name__": "qarro_runtime_build249_baseline", "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    return ns


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def item_obj(x: int, y: int, script: str, flag: str) -> dict:
    return {
        "type": "object",
        "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL",
        "x": x,
        "y": y,
        "elevation": 3,
        "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
        "movement_range_x": 1,
        "movement_range_y": 1,
        "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0",
        "script": script,
        "flag": flag,
    }


def assert_object_flags_free(root: Path, flags: set[str]) -> None:
    # These generic flags were originally selected by Qarro's v3.1 content pass
    # for these same pickups before hidden-item range validation moved the hidden
    # versions to 0x4A7..0x4AA. Re-prove they have no runtime consumers before
    # converting the pickups into visible item objects.
    definition_files = {
        Path("include/constants/flags.h"),
        Path("include/constants/flags_frlg.h"),
    }
    collisions: dict[str, list[str]] = {flag: [] for flag in flags}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".c", ".h", ".inc", ".s", ".json"}:
            continue
        rel = path.relative_to(root)
        if rel in definition_files:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for flag in flags:
            if flag in text:
                collisions[flag].append(str(rel))
    bad = {flag: paths for flag, paths in collisions.items() if paths}
    if bad:
        die(f"visible-item object flags are not free: {bad}")


def remove_hidden(data: dict, *, flag: str, item: str, required: bool = True) -> int:
    events = data.get("bg_events", [])
    matches = [
        event for event in events
        if isinstance(event, dict)
        and event.get("type") == "hidden_item"
        and event.get("flag") == flag
        and event.get("item") == item
    ]
    if required and len(matches) != 1:
        die(f"expected one hidden {item}/{flag}, found {len(matches)}")
    data["bg_events"] = [event for event in events if event not in matches]
    return len(matches)


def add_visible(data: dict, obj: dict) -> None:
    objects = data.setdefault("object_events", [])
    same_script = [o for o in objects if isinstance(o, dict) and o.get("script") == obj["script"]]
    same_flag = [o for o in objects if isinstance(o, dict) and o.get("flag") == obj["flag"]]
    if same_script or same_flag:
        die(f"duplicate visible item script/flag for {obj['script']} / {obj['flag']}")
    objects.append(obj)


def append_finditem_script(path: Path, label: str, item: str) -> None:
    text = read(path)
    if f"{label}::" in text:
        die(f"duplicate item script label {label}")
    text = text.rstrip() + f"\n\n{label}::\n    finditem {item}\n    end\n"
    path.write_text(text, encoding="utf-8")


def apply_ground_items(root: Path) -> dict:
    visible_flags = {"FLAG_0x0B2", "FLAG_0x0B3", "FLAG_0x0B4"}
    assert_object_flags_free(root, visible_flags)

    # Route 1 is before the first city. v3.3 already removes both custom visible
    # balls; remove the remaining custom hidden Oran Berry as well.
    route1_path = root / "data/maps/Route1_Frlg/map.json"
    route1 = json.loads(read(route1_path))
    removed_route1_hidden = remove_hidden(
        route1, flag="FLAG_UNUSED_0x4A9", item="ITEM_ORAN_BERRY", required=True
    )
    custom_route1_visible = [
        o for o in route1.get("object_events", [])
        if isinstance(o, dict) and str(o.get("script", "")).startswith("Route1_EventScript_QarroItem")
    ]
    if custom_route1_visible:
        die(f"pre-Viridian custom visible pickups remain: {custom_route1_visible}")
    custom_route1_hidden = [
        e for e in route1.get("bg_events", [])
        if isinstance(e, dict) and e.get("flag") in {
            "FLAG_UNUSED_0x4A7", "FLAG_UNUSED_0x4A8", "FLAG_UNUSED_0x4A9", "FLAG_UNUSED_0x4AA"
        }
    ]
    if custom_route1_hidden:
        die(f"pre-Viridian custom hidden pickups remain: {custom_route1_hidden}")
    save_json(route1_path, route1)

    conversions = [
        {
            "map": "Route2_Frlg",
            "hidden_flag": "FLAG_UNUSED_0x4AA",
            "hidden_item": "ITEM_SUPER_POTION",
            "x": 16,
            "y": 54,
            "script": "Route2_EventScript_QarroItemSuperPotion",
            "object_flag": "FLAG_0x0B2",
            "item": "ITEM_SUPER_POTION",
        },
        {
            "map": "Route3_Frlg",
            "hidden_flag": "FLAG_UNUSED_0x4A7",
            "hidden_item": "ITEM_GREAT_BALL",
            "x": 27,
            "y": 9,
            "script": "Route3_EventScript_QarroItemGreatBall",
            "object_flag": "FLAG_0x0B3",
            "item": "ITEM_GREAT_BALL",
        },
        {
            "map": "Route4_Frlg",
            "hidden_flag": "FLAG_UNUSED_0x4A8",
            "hidden_item": "ITEM_SUPER_REPEL",
            "x": 68,
            "y": 17,
            "script": "Route4_EventScript_QarroItemSuperRepel",
            "object_flag": "FLAG_0x0B4",
            "item": "ITEM_SUPER_REPEL",
        },
    ]

    for spec in conversions:
        map_path = root / f"data/maps/{spec['map']}/map.json"
        data = json.loads(read(map_path))
        remove_hidden(data, flag=spec["hidden_flag"], item=spec["hidden_item"], required=True)
        add_visible(
            data,
            item_obj(spec["x"], spec["y"], spec["script"], spec["object_flag"]),
        )
        save_json(map_path, data)
        append_finditem_script(
            root / f"data/maps/{spec['map']}/scripts.inc",
            spec["script"],
            spec["item"],
        )

    # Validate the already-existing Route 2 Repel from v3.3 remains visible and
    # persistent. Together with the three conversions this is the first ground-
    # item tranche after Viridian, without front-loading Pallet/Route 1.
    route2 = json.loads(read(root / "data/maps/Route2_Frlg/map.json"))
    repel = [
        o for o in route2.get("object_events", [])
        if isinstance(o, dict)
        and o.get("script") == "Route2_EventScript_QarroItemRepel"
        and o.get("flag") == "FLAG_0x0B1"
    ]
    if len(repel) != 1:
        die(f"Route2 persistent Repel pickup changed; expected one, found {len(repel)}")

    report = {
        "marker": MARKER,
        "rule": "no custom accessible pickups before Viridian; visible ground items begin Route 2",
        "preViridianHiddenRemoved": removed_route1_hidden,
        "visiblePostViridianPickups": [
            {"map": "Route2_Frlg", "item": "ITEM_REPEL", "flag": "FLAG_0x0B1", "source": "v3.3"},
            *[
                {
                    "map": spec["map"],
                    "item": spec["item"],
                    "flag": spec["object_flag"],
                    "convertedFromHidden": spec["hidden_flag"],
                }
                for spec in conversions
            ],
        ],
        "visibleCustomPickupCount": 4,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ground_items_v3_23_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: removed final pre-Viridian custom hidden pickup; "
        f"4 persistent visible custom pickups now begin on Route 2"
    )
    return report


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    repo = Path(__file__).resolve().parents[1]
    base = load_base(repo)
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    root = Path(sys.argv[1]).resolve()
    apply_ground_items(root)
    print(
        f"[{MARKER}] runtime baseline preserved; ground-item progression advanced; "
        f"Ash Bond / Ash Cap untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
