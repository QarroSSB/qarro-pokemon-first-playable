#!/usr/bin/env python3
"""Targeted v3.5 follow-up for conditional move descriptions.

Execute the exact phase-1 RU description patch from commit 1a5adc5d, while
handling only verified conditional description branches in pinned Expansion
1.17.0. Every other conditional entry remains fail-closed and preserved until
it is inspected separately.

No Ash Bond / Ash Cap changes.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "1a5adc5d6ea94574c8b26d0347eb2f134066e5a4"
BASE_PATH = "ci/localization_ru_core_v3_3.py"


def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    return subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )


def encode_description(lines: tuple[str, str]) -> str:
    if len(lines) != 2 or any(not line for line in lines):
        raise RuntimeError(f"invalid two-line description: {lines!r}")
    if any("—" in line or "…" in line for line in lines):
        raise RuntimeError(f"unsupported typography in description: {lines!r}")
    return lines[0].replace('"', '\\"') + "\\n" + lines[1].replace('"', '\\"')


def c_source_description(lines: tuple[str, str]) -> str:
    if len(lines) != 2 or any(not line for line in lines):
        raise RuntimeError(f"invalid two-line source description: {lines!r}")
    if any("—" in line or "…" in line for line in lines):
        raise RuntimeError(f"unsupported typography in source description: {lines!r}")
    return (
        '"' + lines[0].replace('"', '\\"') + '\\n"' + '\n'
        '            "' + lines[1].replace('"', '\\"') + '"),'
    )


def patch_rapid_spin(block: str) -> tuple[str, bool]:
    if "#if B_SPEED_BUFFING_RAPID_SPIN >= GEN_8" not in block:
        raise RuntimeError("MOVE_RAPID_SPIN: expected Gen 8 Speed conditional missing")
    if block.count("#else") != 1 or block.count("#endif") < 1:
        raise RuntimeError("MOVE_RAPID_SPIN: expected exactly one description #else branch")

    branches = (
        (
            re.compile(r'"Spins to remove traps\\n"\s*"and raise Speed\."\),'),
            ("Убирает ловушки и", "повышает Скорость."),
            "Gen8+",
        ),
        (
            re.compile(r'"Spins the body at high\\n"\s*"speed to remove traps\."\),'),
            ("Вращается и убирает", "ловушки с поля."),
            "pre-Gen8",
        ),
    )

    changed = False
    for rx, translated, branch_name in branches:
        matches = list(rx.finditer(block))
        if len(matches) != 1:
            raise RuntimeError(
                f"MOVE_RAPID_SPIN: {branch_name} description expected once, got {len(matches)}"
            )
        replacement = c_source_description(translated)
        block = block[:matches[0].start()] + replacement + block[matches[0].end():]
        changed = True

    if "Spins to remove traps" in block or "speed to remove traps" in block:
        raise RuntimeError("MOVE_RAPID_SPIN: English description text remained after patch")
    return block, changed


def patch_rock_slide(block: str) -> tuple[str, bool]:
    if "#if B_UPDATED_MOVE_DATA >= GEN_2" not in block:
        raise RuntimeError("MOVE_ROCK_SLIDE: expected updated-move-data conditional missing")
    if block.count("#else") != 1 or block.count("#endif") < 1:
        raise RuntimeError("MOVE_ROCK_SLIDE: expected exactly one description #else branch")

    branches = (
        (
            re.compile(
                r'"Large boulders are hurled\.(?:\\n|\\\s*)"\s*'
                r'"May cause flinching\."\),'
            ),
            ("Обрушивает камни.", "Может вызвать испуг."),
            "Gen2+",
        ),
        (
            re.compile(
                r'"Hits the foes with an(?:\\n|\\\s*)"\s*'
                r'"avalanche of boulders\."\),'
            ),
            ("Обрушивает на врагов", "лавину валунов."),
            "Gen1",
        ),
    )

    changed = False
    for rx, translated, branch_name in branches:
        matches = list(rx.finditer(block))
        if len(matches) != 1:
            raise RuntimeError(
                f"MOVE_ROCK_SLIDE: {branch_name} description expected once, got {len(matches)}"
            )
        replacement = c_source_description(translated)
        block = block[:matches[0].start()] + replacement + block[matches[0].end():]
        changed = True

    if "Large boulders are hurled" in block or "avalanche of boulders" in block:
        raise RuntimeError("MOVE_ROCK_SLIDE: English description text remained after patch")
    return block, changed


def patch_ice_fang(block: str) -> tuple[str, bool]:
    if "#if B_USE_FROSTBITE" not in block:
        raise RuntimeError("MOVE_ICE_FANG: expected frostbite conditional missing")
    if block.count("#else") != 1 or block.count("#endif") < 1:
        raise RuntimeError("MOVE_ICE_FANG: expected exactly one description #else branch")

    prefix = re.compile(r'"May cause flinching or(?:\\n|\\\s*)"\s*')
    matches = list(prefix.finditer(block))
    if len(matches) != 1:
        raise RuntimeError(f"MOVE_ICE_FANG: shared description prefix expected once, got {len(matches)}")
    block = block[:matches[0].start()] + '"Может вызвать испуг или\\n"\n            ' + block[matches[0].end():]

    branches = (
        (
            re.compile(r'"leave the foe with frostbite\."\),'),
            '"обморожение у цели."),',
            "frostbite",
        ),
        (
            re.compile(r'"freeze the foe\."\),'),
            '"заморозить цель."),',
            "freeze",
        ),
    )
    for rx, replacement, branch_name in branches:
        matches = list(rx.finditer(block))
        if len(matches) != 1:
            raise RuntimeError(
                f"MOVE_ICE_FANG: {branch_name} branch expected once, got {len(matches)}"
            )
        block = block[:matches[0].start()] + replacement + block[matches[0].end():]

    if "May cause flinching or" in block or "leave the foe with frostbite" in block or "freeze the foe" in block:
        raise RuntimeError("MOVE_ICE_FANG: English description text remained after patch")
    return block, True


def patch_table(path: Path, entries: dict[str, tuple[str, str]], prefix: str) -> int:
    text = path.read_text(encoding="utf-8")
    changed_entries = 0
    for key, lines in entries.items():
        token = f"[{key}] ="
        start = text.find(token)
        if start < 0:
            raise RuntimeError(f"{path}: missing entry {key}")
        next_start = text.find(f"\n    [{prefix}", start + len(token))
        end = len(text) if next_start < 0 else next_start
        block = text[start:end]

        desc_start = block.find(".description")
        if desc_start < 0:
            raise RuntimeError(f"{path}: {key} missing description")
        first_close = block.find("),", desc_start)
        if first_close < 0:
            raise RuntimeError(f"{path}: {key} unterminated description")

        special = {
            "MOVE_RAPID_SPIN": (patch_rapid_spin, "both conditional descriptions localized"),
            "MOVE_ROCK_SLIDE": (patch_rock_slide, "both conditional descriptions localized"),
            "MOVE_ICE_FANG": (patch_ice_fang, "both conditional descriptions localized"),
        }.get(key)
        if special is not None:
            func, message = special
            block, changed = func(block)
            if changed:
                text = text[:start] + block + text[end:]
                changed_entries += 1
                print(f"[ru-desc] {key}: {message}")
            continue

        if re.search(r"(?m)^\s*#(?:if|elif|else|endif)\b", block):
            print(f"[ru-desc] {key}: conditional description preserved (English)")
            continue

        rx = re.compile(r"(?s)(\.description\s*=\s*COMPOUND_STRING\()(.*?)(\),)")
        match = rx.search(block)
        if match is None:
            raise RuntimeError(f"{path}: {key} description parse failed")

        encoded = encode_description(lines)
        replacement = f'.description = COMPOUND_STRING("{encoded}"),'
        if match.group(0) == replacement:
            continue

        block = block[:match.start()] + replacement + block[match.end():]
        text = text[:start] + block + text[end:]
        changed_entries += 1
        print(f"[ru-desc] {key}: description localized")

    path.write_text(text, encoding="utf-8")
    return changed_entries


def main() -> int:
    code = load_base()
    ns = {
        "__name__": "qarro_ru_desc_v35_base",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    ns["patch_table"] = patch_table
    return int(ns["main"]() or 0)


if __name__ == "__main__":
    raise SystemExit(main())
