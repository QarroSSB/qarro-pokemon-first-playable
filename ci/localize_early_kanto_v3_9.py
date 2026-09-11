#!/usr/bin/env python3
"""Qarro v3.26: localize the Route 5 Underground Path sign.

Runs CI-green v3.25 first, then localizes the remaining Route 5 sign text in
Route5_Frlg/scripts.inc. Pokemon species, Move and Ability proper names stay
English. Gameplay, trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BASE_COMMIT = "1d8fe2282b9060d4650d7391d051e9c41d9a26de"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_25"
BASE_COUNT = 396
MARKER = "QARRO_RU_EARLY_KANTO_V3_26"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")
REL = Path("data/maps/Route5_Frlg/scripts.inc")
SOURCE_BLOB = "ff2d0756081c3a5354448bfc2e5b6b679fd64e1f"

def B(*lines: str) -> tuple[str, ...]: return lines

BLOCKS = {
    "Route5_Text_UndergroundPathSign": B(
        r"ПОДЗЕМНЫЙ ПЕРЕХОД\n",
        r"CERULEAN CITY - VERMILION CITY$"),
}

def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT], check=True)
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"], text=True)

def render(label: str, lines: tuple[str, ...]) -> str:
    return label + "::\n" + "".join(f'\t.string "{line}"\n' for line in lines)

def patch_label(text: str, label: str, lines: tuple[str, ...]) -> str:
    pat = re.compile(rf"(?m)^{re.escape(label)}::\n(?:\t\.string .*\n)+")
    hits = list(pat.finditer(text))
    if len(hits) != 1:
        raise RuntimeError(f"{label}: expected exactly one string block, got {len(hits)}")
    old = hits[0].group(0)
    if any("\u0400" <= ch <= "\u04ff" for ch in old):
        raise RuntimeError(f"{label}: source block unexpectedly already contains Cyrillic")
    return text[:hits[0].start()] + render(label, lines) + text[hits[0].end():]

def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <pokeemerald-expansion-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    actual = subprocess.check_output(["git", "-C", str(root), "hash-object", str(path)], text=True).strip()
    if actual != SOURCE_BLOB:
        raise RuntimeError(f"{REL}: pinned source blob drift before base pass: {actual} != {SOURCE_BLOB}")

    code = load_base()
    ns = {"__name__": "qarro_ru_early_kanto_v325_base", "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc:
        return rc

    audit_path = root / AUDIT_REL
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != BASE_MARKER or int(audit.get("selectedBlocksLocalized", -1)) != BASE_COUNT:
        raise RuntimeError(f"base localization audit drift: {audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}")

    text = path.read_text(encoding="utf-8")
    for label, lines in BLOCKS.items():
        text = patch_label(text, label, lines)
    path.write_text(text, encoding="utf-8")

    changed = len(BLOCKS)
    if changed != 1:
        raise RuntimeError(f"Route 5 scope drift: expected 1 block, got {changed}")
    previous = audit.get("files", {}).get(str(REL), {})
    audit.setdefault("files", {})[str(REL)] = {
        "selectedBlocks": int(previous.get("selectedBlocks", 0)) + changed,
        "changedThisRun": changed,
        "sourceBlob": SOURCE_BLOB,
    }
    audit.update({
        "previousMarker": BASE_MARKER,
        "marker": MARKER,
        "selectedBlocksLocalized": BASE_COUNT + changed,
        "blocksChangedThisRun": int(audit.get("blocksChangedThisRun", 0)) + changed,
        "route5ExteriorComplete": True,
        "pokemonSpeciesProperNamesEnglish": True,
        "moveProperNamesEnglish": True,
        "abilityProperNamesEnglish": True,
        "gameplayTouched": False,
        "trainerDataTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    })
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: base {BASE_COUNT} + {changed} Route 5 block = {BASE_COUNT + changed}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
