#!/usr/bin/env python3
"""Qarro v3.177 integration test: apply generated static bulk RU patch.

The patch was generated offline from the exact FULL GREEN v3.173 translation
state and is restricted to seven large text-only surfaces that v3.174-v3.176
do not modify. This wrapper is fail-closed: exact target paths only, git
apply --check first, then a normal git apply. No gameplay/Ash paths allowed.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_GENERATED_BULK_V3_177"
PATCH = Path(__file__).with_name("generated_bulk_ru_v3_177.patch")
EXPECTED = {
    "data/scripts/cable_club_frlg.inc",
    "data/text/fame_checker_frlg.inc",
    "data/text/trainers.inc",
    "data/text/trainers_frlg.inc",
    "src/battle_message.c",
    "src/data/items.h",
    "src/strings.c",
}

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply_generated_bulk_ru_v3_177.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    text = PATCH.read_text(encoding="utf-8")
    paths = set(re.findall(r"(?m)^diff --git a/(.+?) b/(.+?)$", text))
    left = {a for a,b in paths}
    right = {b for a,b in paths}
    if left != EXPECTED or right != EXPECTED:
        raise RuntimeError(f"bulk patch path drift: left={sorted(left)} right={sorted(right)}")
    if any("ash" in p.lower() for p in EXPECTED):
        raise RuntimeError("forbidden Ash path in bulk patch")
    subprocess.run(["git","-C",str(root),"apply","--check",str(PATCH)],check=True)
    subprocess.run(["git","-C",str(root),"apply",str(PATCH)],check=True)
    out=root/"build"/"qarro_ru_generated_bulk_v3_177_audit.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
      "marker":MARKER,
      "patchFile":PATCH.name,
      "targetFiles":sorted(EXPECTED),
      "targetFileCount":len(EXPECTED),
      "translationOnly":True,
      "gameplayLogicTouched":False,
      "ashBondTouched":False,
      "ashCapTouched":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: static bulk RU patch applied to {len(EXPECTED)} text surfaces")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
