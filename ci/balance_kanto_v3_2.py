#!/usr/bin/env python3
"""Qarro v3.2 Kanto gym balance + synchronized level-cap pass.

Lower the eight FIRST PLAYABLE Kanto leader teams so difficulty comes from
six-Pokemon rosters / builds / AI rather than mandatory grinding. Then enable
the Expansion's native hard level caps, keyed to Kanto badge flags, with each
cap matching the ace of the next required boss.

Fails closed if the expected v3.0/v3.1 trainer blocks, cap config, or upstream
cap table changed. No Ash Bond / Ash Cap changes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TARGETS = {
    "TRAINER_LEADER_BROCK": ([21, 21, 22, 22, 23, 24], [13, 13, 14, 14, 15, 16]),
    "TRAINER_LEADER_MISTY": ([27, 27, 28, 28, 29, 30], [19, 19, 20, 20, 21, 22]),
    "TRAINER_LEADER_LT_SURGE": ([33, 33, 34, 34, 35, 36], [25, 25, 26, 26, 27, 28]),
    "TRAINER_LEADER_ERIKA": ([39, 39, 40, 40, 41, 42], [31, 31, 32, 32, 33, 34]),
    "TRAINER_LEADER_KOGA": ([45, 45, 46, 46, 47, 48], [37, 37, 38, 38, 39, 40]),
    "TRAINER_LEADER_SABRINA": ([51, 51, 52, 52, 53, 54], [43, 43, 44, 44, 45, 46]),
    "TRAINER_LEADER_BLAINE": ([57, 57, 58, 58, 59, 60], [49, 49, 50, 50, 51, 52]),
    "TRAINER_LEADER_GIOVANNI": ([63, 63, 64, 64, 65, 66], [55, 55, 56, 56, 57, 58]),
}

CAP_CONFIG = {
    "B_EXP_CAP_TYPE": ("EXP_CAP_NONE", "EXP_CAP_HARD"),
    "B_LEVEL_CAP_TYPE": ("LEVEL_CAP_NONE", "LEVEL_CAP_FLAG_LIST"),
    "B_RARE_CANDY_CAP": ("FALSE", "TRUE"),
}

CAP_LEVELS_EXPECTED = [
    ("FLAG_BADGE01_GET", 15),
    ("FLAG_BADGE02_GET", 19),
    ("FLAG_BADGE03_GET", 24),
    ("FLAG_BADGE04_GET", 29),
    ("FLAG_BADGE05_GET", 31),
    ("FLAG_BADGE06_GET", 33),
    ("FLAG_BADGE07_GET", 42),
    ("FLAG_BADGE08_GET", 46),
    ("FLAG_IS_CHAMPION", 58),
]

# Hard cap before each milestone = ace of the next required boss.
# After Champion, GetCurrentLevelCap() naturally falls through to MAX_LEVEL.
CAP_LEVELS_DESIRED = [
    ("FLAG_BADGE01_GET", 16),
    ("FLAG_BADGE02_GET", 22),
    ("FLAG_BADGE03_GET", 28),
    ("FLAG_BADGE04_GET", 34),
    ("FLAG_BADGE05_GET", 40),
    ("FLAG_BADGE06_GET", 46),
    ("FLAG_BADGE07_GET", 52),
    ("FLAG_BADGE08_GET", 58),
    ("FLAG_IS_CHAMPION", 63),
]


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


def patch_define(text: str, name: str, expected: str, desired: str) -> str:
    pattern = re.compile(rf"(?m)^(#define\s+{re.escape(name)}\s+)(\S+)(.*)$")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{name}: expected exactly one define, got {len(matches)}")
    current = matches[0].group(2)
    if current == desired:
        print(f"[level-cap] {name}: already {desired}")
        return text
    if current != expected:
        raise RuntimeError(f"{name}: expected {expected}, got {current}; refusing broad edit")
    text = pattern.sub(lambda m: f"{m.group(1)}{desired}{m.group(3)}", text, count=1)
    print(f"[level-cap] {name}: {expected} -> {desired}")
    return text


def patch_level_cap_table(text: str) -> str:
    pattern = re.compile(
        r"(static const u32 sLevelCapFlagMap\[\]\[2\]\s*=\s*\{\s*\n)(.*?)(\n\s*\};)",
        re.S,
    )
    match = pattern.search(text)
    if not match:
        raise RuntimeError("missing sLevelCapFlagMap in src/caps.c")

    body = match.group(2)
    observed = [
        (flag, int(level))
        for flag, level in re.findall(r"\{\s*(FLAG_[A-Z0-9_]+)\s*,\s*(\d+)\s*\}", body)
    ]
    if observed == CAP_LEVELS_DESIRED:
        print(f"[level-cap] sLevelCapFlagMap: already {CAP_LEVELS_DESIRED}")
        return text
    if observed != CAP_LEVELS_EXPECTED:
        raise RuntimeError(
            f"sLevelCapFlagMap: expected {CAP_LEVELS_EXPECTED}, got {observed}; refusing broad edit"
        )

    desired_by_flag = dict(CAP_LEVELS_DESIRED)

    def repl(pair_match: re.Match[str]) -> str:
        flag = pair_match.group(1)
        old_level = int(pair_match.group(2))
        if flag not in desired_by_flag:
            return pair_match.group(0)
        new_level = desired_by_flag[flag]
        return pair_match.group(0).replace(str(old_level), str(new_level), 1)

    body2 = re.sub(r"\{\s*(FLAG_[A-Z0-9_]+)\s*,\s*(\d+)\s*\}", repl, body)
    text = text[:match.start()] + match.group(1) + body2 + match.group(3) + text[match.end():]
    print(f"[level-cap] sLevelCapFlagMap: {CAP_LEVELS_EXPECTED} -> {CAP_LEVELS_DESIRED}")
    return text


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    trainer_path = root / "src/data/trainers_frlg.party"
    if not trainer_path.exists():
        raise SystemExit(f"missing {trainer_path}")
    trainer_text = trainer_path.read_text(encoding="utf-8")
    for trainer, (expected, desired) in TARGETS.items():
        trainer_text = patch_block(trainer_text, trainer, expected, desired)
    trainer_path.write_text(trainer_text, encoding="utf-8")

    cap_config_path = root / "include/config/caps.h"
    if not cap_config_path.exists():
        raise SystemExit(f"missing {cap_config_path}")
    cap_config_text = cap_config_path.read_text(encoding="utf-8")
    for name, (expected, desired) in CAP_CONFIG.items():
        cap_config_text = patch_define(cap_config_text, name, expected, desired)
    cap_config_path.write_text(cap_config_text, encoding="utf-8")

    caps_path = root / "src/caps.c"
    if not caps_path.exists():
        raise SystemExit(f"missing {caps_path}")
    caps_text = patch_level_cap_table(caps_path.read_text(encoding="utf-8"))
    caps_path.write_text(caps_text, encoding="utf-8")

    print(
        "[QARRO_BALANCE_V3_2] PASS: Kanto leader levels reduced; native hard level caps "
        "synchronized to next-boss aces; Rare Candy cap enabled; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
