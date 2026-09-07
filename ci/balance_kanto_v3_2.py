#!/usr/bin/env python3
"""Qarro v3.2 Kanto gym balance pass.

Lower the eight FIRST PLAYABLE Kanto leader teams so difficulty comes from
six-Pokemon rosters / builds / AI rather than mandatory grinding.
Fails closed if the expected v3.0 trainer blocks or level sequences changed.
No Ash Bond / Ash Cap changes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TARGETS = {
    "TRAINER_LEADER_BROCK": ([21, 21, 22, 22, 23, 24], [13, 13, 14, 14, 15, 16]),
    "TRAINER_LEADER_MISTY": ([27, 27, 28, 28, 29, 30], [19, 19, 20, 20, 21, 22]),
    "TRAINER_LEADER_LT_SURGE": ([33, 33, 34, 34, 35, 36], [25, 25, 26, 26, 27, 28]),
    "TRAINER_LEADER_ERIKA": ([49, 49, 50, 50, 51, 52], [31, 31, 32, 32, 33, 34]),
    "TRAINER_LEADER_KOGA": ([57, 57, 58, 58, 59, 60], [37, 37, 38, 38, 39, 40]),
    "TRAINER_LEADER_SABRINA": ([65, 65, 66, 66, 67, 68], [43, 43, 44, 44, 45, 46]),
    "TRAINER_LEADER_BLAINE": ([73, 73, 74, 74, 75, 76], [49, 49, 50, 50, 51, 52]),
    "TRAINER_LEADER_GIOVANNI": ([81, 81, 82, 82, 83, 84], [55, 55, 56, 56, 57, 58]),
}


def patch_block(text: str, trainer: str, expected: list[int], desired: list[int]) -> str:
    start_token = f"=== {trainer} ==="
    start = text.find(start_token)
    if start < 0:
        raise RuntimeError(f"missing trainer block: {trainer}")
    next_start = text.find("\n=== ", start + len(start_token))
    end = len(text) if next_start < 0 else next_start
    block = text[start:end]

    levels = [int(x) for x in re.findall(r"(?m)^Level:\s*(\d+)\s*$", block)]
    if levels == desired:
        print(f"[balance] {trainer}: already {desired}")
        return text
    if levels != expected:
        raise RuntimeError(f"{trainer}: expected levels {expected}, got {levels}; refusing broad edit")

    it = iter(desired)
    block2 = re.sub(r"(?m)^Level:\s*\d+\s*$", lambda _m: f"Level: {next(it)}", block)
    print(f"[balance] {trainer}: {expected} -> {desired}")
    return text[:start] + block2 + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    path = root / "src/data/trainers_frlg.party"
    if not path.exists():
        raise SystemExit(f"missing {path}")

    text = path.read_text(encoding="utf-8")
    for trainer, (expected, desired) in TARGETS.items():
        text = patch_block(text, trainer, expected, desired)
    path.write_text(text, encoding="utf-8")
    print("[QARRO_BALANCE_V3_2] PASS: Kanto leader levels reduced; Ash code untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
