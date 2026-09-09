#!/usr/bin/env python3
"""Qarro isolated Gym 5-of-6 test mechanic.

Based on the last green v3.4 gameplay baseline. For each of the eight Kanto
Gym Leaders, keep the prepared six-mon roster but make trainerproc select a
five-mon battle party from that six-mon pool. Enable Expansion's consistent
trainer-pool RNG so the same save receives the same selected five on retries
and resets.

This test intentionally changes no Elite Four/Champion/Postgame party sizes.
No Ash Bond / Ash Cap code is touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_GYM_5OF6_TEST"
LEADERS = (
    "TRAINER_LEADER_BROCK",
    "TRAINER_LEADER_MISTY",
    "TRAINER_LEADER_LT_SURGE",
    "TRAINER_LEADER_ERIKA",
    "TRAINER_LEADER_KOGA",
    "TRAINER_LEADER_SABRINA",
    "TRAINER_LEADER_BLAINE",
    "TRAINER_LEADER_GIOVANNI",
)


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def patch_leader_blocks(path: Path) -> list[str]:
    if not path.exists():
        die(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    patched: list[str] = []

    for trainer in LEADERS:
        token = f"=== {trainer} ==="
        start = text.find(token)
        if start < 0:
            die(f"missing leader block {trainer}")
        next_start = text.find("\n=== ", start + len(token))
        end = len(text) if next_start < 0 else next_start
        block = text[start:end]

        levels = re.findall(r"(?m)^Level:\s*\d+\s*$", block)
        if len(levels) != 6:
            die(f"{trainer}: expected exactly 6 prepared Pokemon, got {len(levels)}")

        party_sizes = re.findall(r"(?m)^Party Size:\s*(\d+)\s*$", block)
        if party_sizes == ["5"]:
            patched.append(trainer)
            continue
        if party_sizes:
            die(f"{trainer}: unexpected existing Party Size values {party_sizes}")

        block2 = block.replace(token, token + "\nParty Size: 5", 1)
        text = text[:start] + block2 + text[end:]
        patched.append(trainer)

    path.write_text(text, encoding="utf-8")
    return patched


def patch_consistent_rng(path: Path) -> None:
    if not path.exists():
        die(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"(?m)^(#define\s+B_POOL_SETTING_CONSISTENT_RNG\s+)(TRUE|FALSE)(\s*//.*)?$")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        die(f"expected exactly one B_POOL_SETTING_CONSISTENT_RNG define, got {len(matches)}")
    current = matches[0].group(2)
    if current == "FALSE":
        text = pattern.sub(lambda m: f"{m.group(1)}TRUE{m.group(3) or ''}", text, count=1)
        path.write_text(text, encoding="utf-8")
    elif current != "TRUE":
        die(f"unexpected B_POOL_SETTING_CONSISTENT_RNG value {current}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    patched = patch_leader_blocks(root / "src/data/trainers_frlg.party")
    patch_consistent_rng(root / "include/config/battle.h")

    audit = {
        "marker": MARKER,
        "leaders": patched,
        "preparedRosterSize": 6,
        "battlePartySize": 5,
        "consistentPoolRng": True,
        "retryResetRerollExpected": False,
        "eliteFourChampionPostgamePartySizesChanged": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_gym_5of6_test_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: 8 Kanto leaders use 5 of prepared 6; "
        "consistent save-seeded pool RNG enabled; non-Gym party sizes untouched; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
