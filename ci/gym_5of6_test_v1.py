#!/usr/bin/env python3
"""Qarro Gym 5-of-6 test pass.

Uses Expansion 1.17.0's native trainer pool system instead of custom battle code:
- each of the eight Kanto Gym Leaders keeps a six-Pokemon source roster;
- Party Size is set to 5, so trainerproc emits partySize=5 and poolSize=6;
- consistent pool RNG is enabled so the same save gets the same five for the
  same Leader across resets/retries;
- Elite Four, Champions and postgame trainers are untouched.

This is a focused test implementation. No Ash Bond / Ash Cap code is touched.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "QARRO_GYM_5OF6_TEST_V1"
LEADERS = [
    "TRAINER_LEADER_BROCK",
    "TRAINER_LEADER_MISTY",
    "TRAINER_LEADER_LT_SURGE",
    "TRAINER_LEADER_ERIKA",
    "TRAINER_LEADER_KOGA",
    "TRAINER_LEADER_SABRINA",
    "TRAINER_LEADER_BLAINE",
    "TRAINER_LEADER_GIOVANNI",
]


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def section_span(text: str, trainer: str) -> tuple[int, int, str]:
    token = f"=== {trainer} ==="
    start = text.find(token)
    if start < 0:
        die(f"missing trainer section: {trainer}")
    nxt = text.find("\n=== ", start + len(token))
    end = len(text) if nxt < 0 else nxt
    return start, end, text[start:end]


def patch_leader(text: str, trainer: str) -> str:
    start, end, block = section_span(text, trainer)
    if "\n\n" not in block:
        die(f"{trainer}: missing metadata/party separator")
    meta, party = block.split("\n\n", 1)

    # The active Kanto pass must still provide exactly six prepared mons.
    levels = re.findall(r"(?m)^Level:\s*\d+\s*$", party)
    if len(levels) != 6:
        die(f"{trainer}: expected six prepared Pokemon, found {len(levels)}")

    party_size_lines = re.findall(r"(?m)^Party Size:\s*\d+\s*$", meta)
    if len(party_size_lines) > 1:
        die(f"{trainer}: duplicate Party Size metadata")
    if party_size_lines:
        meta2 = re.sub(r"(?m)^Party Size:\s*\d+\s*$", "Party Size: 5", meta, count=1)
    else:
        lines = meta.splitlines()
        # Keep metadata readable: put Party Size immediately after AI when possible.
        insert_at = len(lines)
        for i, line in enumerate(lines):
            if line.startswith("AI:"):
                insert_at = i + 1
                break
        lines.insert(insert_at, "Party Size: 5")
        meta2 = "\n".join(lines)

    new_block = meta2 + "\n\n" + party
    print(f"[{MARKER}] {trainer}: source roster=6, battle party=5")
    return text[:start] + new_block + text[end:]


def patch_consistent_rng(root: Path) -> None:
    path = root / "include/config/battle.h"
    if not path.exists():
        die(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"(?m)^(#define\s+B_POOL_SETTING_CONSISTENT_RNG\s+)(TRUE|FALSE)(\s*//.*)$")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        die(f"expected exactly one B_POOL_SETTING_CONSISTENT_RNG define, got {len(matches)}")
    current = matches[0].group(2)
    if current == "FALSE":
        text = pattern.sub(lambda m: f"{m.group(1)}TRUE{m.group(3)}", text, count=1)
        path.write_text(text, encoding="utf-8")
        print(f"[{MARKER}] consistent trainer-pool RNG: FALSE -> TRUE")
    elif current == "TRUE":
        print(f"[{MARKER}] consistent trainer-pool RNG already TRUE")
    else:
        die(f"unexpected consistent RNG value: {current}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    trainers = root / "src/data/trainers_frlg.party"
    if not trainers.exists():
        die(f"missing {trainers}")

    text = trainers.read_text(encoding="utf-8")
    for trainer in LEADERS:
        text = patch_leader(text, trainer)
    trainers.write_text(text, encoding="utf-8")
    patch_consistent_rng(root)

    # Scope is deliberately limited to the trainer party source and battle
    # pool RNG config above. No Ash-specific source, item, form, or script is opened.
    print(
        f"[{MARKER}] PASS: 8 Kanto Leaders use native 5-of-6 pools with save-stable selection; "
        "Elite Four/Champion/postgame untouched; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
