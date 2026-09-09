#!/usr/bin/env python3
"""Qarro test overlay: five-mon Kanto leaders + early party-wide Exp. Share.

This file is intentionally isolated from the production balance pass. It is
meant for a comparison ROM built from the last confirmed v3.2 baseline.

Changes:
- Each of the 8 Kanto Leader blocks is reduced from 6 Pokemon to 5 by removing
  the first (lowest-level) party member after v3.2 balance has been applied.
  The ace/final slot and the remaining four builds stay untouched.
- Expansion 1.17.0's native party-wide Exp. Share is enabled when FireRed's
  FLAG_SYS_POKEDEX_GET is set, so it starts automatically as soon as the player
  receives the Pokedex.

No Ash Bond / Ash Cap changes. Fails closed if the expected v3.2 party levels
or Exp. Share config differ from the verified baseline.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LEADERS = {
    "TRAINER_LEADER_BROCK": [13, 13, 14, 14, 15, 16],
    "TRAINER_LEADER_MISTY": [19, 19, 20, 20, 21, 22],
    "TRAINER_LEADER_LT_SURGE": [25, 25, 26, 26, 27, 28],
    "TRAINER_LEADER_ERIKA": [31, 31, 32, 32, 33, 34],
    "TRAINER_LEADER_KOGA": [37, 37, 38, 38, 39, 40],
    "TRAINER_LEADER_SABRINA": [43, 43, 44, 44, 45, 46],
    "TRAINER_LEADER_BLAINE": [49, 49, 50, 50, 51, 52],
    "TRAINER_LEADER_GIOVANNI": [55, 55, 56, 56, 57, 58],
}


def get_block_bounds(text: str, trainer: str) -> tuple[int, int]:
    token = f"=== {trainer} ==="
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"missing trainer block: {trainer}")
    next_start = text.find("\n=== ", start + len(token))
    return start, len(text) if next_start < 0 else next_start


def reduce_leader_to_five(text: str, trainer: str, expected_levels: list[int]) -> str:
    start, end = get_block_bounds(text, trainer)
    block = text[start:end]
    levels = [int(x) for x in re.findall(r"(?m)^Level:\s*(\d+)\s*$", block)]

    desired_levels = expected_levels[1:]
    if levels == desired_levels:
        print(f"[5mon] {trainer}: already five Pokemon {desired_levels}")
        return text
    if levels != expected_levels:
        raise RuntimeError(
            f"{trainer}: expected v3.2 levels {expected_levels}, got {levels}; refusing broad edit"
        )

    # Trainer metadata is paragraph 0; each Pokemon is one following paragraph.
    paragraphs = block.split("\n\n")
    mon_paragraph_indices = [
        i for i, paragraph in enumerate(paragraphs)
        if re.search(r"(?m)^Level:\s*\d+\s*$", paragraph)
    ]
    if len(mon_paragraph_indices) != 6:
        raise RuntimeError(
            f"{trainer}: expected exactly 6 Pokemon paragraphs, got {len(mon_paragraph_indices)}"
        )

    first_mon_idx = mon_paragraph_indices[0]
    removed_name = paragraphs[first_mon_idx].splitlines()[0].strip()
    del paragraphs[first_mon_idx]
    block2 = "\n\n".join(paragraphs)

    levels2 = [int(x) for x in re.findall(r"(?m)^Level:\s*(\d+)\s*$", block2)]
    if levels2 != desired_levels:
        raise RuntimeError(
            f"{trainer}: post-edit levels {levels2} != expected {desired_levels}"
        )

    print(f"[5mon] {trainer}: removed first slot {removed_name}; levels {levels2}")
    return text[:start] + block2 + text[end:]


def enable_exp_share_after_pokedex(text: str) -> str:
    pattern = re.compile(r"(?m)^(#define\s+I_EXP_SHARE_FLAG\s+)(\S+)(.*)$")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"I_EXP_SHARE_FLAG: expected one define, got {len(matches)}")
    current = matches[0].group(2)
    desired = "FLAG_SYS_POKEDEX_GET"
    if current == desired:
        print("[exp-share] already enabled after Pokedex")
        return text
    if current != "0":
        raise RuntimeError(
            f"I_EXP_SHARE_FLAG: expected verified baseline 0, got {current}; refusing broad edit"
        )
    text = pattern.sub(lambda m: f"{m.group(1)}{desired}{m.group(3)}", text, count=1)
    print("[exp-share] I_EXP_SHARE_FLAG: 0 -> FLAG_SYS_POKEDEX_GET")
    return text


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()

    party_path = root / "src/data/trainers_frlg.party"
    if not party_path.exists():
        raise SystemExit(f"missing {party_path}")
    party_text = party_path.read_text(encoding="utf-8")
    for trainer, levels in LEADERS.items():
        party_text = reduce_leader_to_five(party_text, trainer, levels)
    party_path.write_text(party_text, encoding="utf-8")

    item_cfg_path = root / "include/config/item.h"
    if not item_cfg_path.exists():
        raise SystemExit(f"missing {item_cfg_path}")
    item_cfg = enable_exp_share_after_pokedex(item_cfg_path.read_text(encoding="utf-8"))
    item_cfg_path.write_text(item_cfg, encoding="utf-8")

    print(
        "[QARRO_TEST_5MON_EXP_SHARE] PASS: 8 Kanto Leaders reduced 6->5; "
        "party-wide Exp. Share activates after Pokedex; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
