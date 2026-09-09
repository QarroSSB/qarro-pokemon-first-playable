#!/usr/bin/env python3
"""TEST-ONLY profile: 5 Pokemon per Kanto gym + always-on Gen VI party Exp Share.

This script is intentionally isolated to the test/gym5-exp-share branch. It runs
after the normal v3.2 balance pass, removes the first (lowest-priority) member
from each six-Pokemon Kanto leader roster while preserving the ace as the final
member, then forces the Expansion's native Gen VI Exp Share path on for the
whole party.

Ash Bond / Ash Cap are untouched.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

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


def trim_party(text: str, trainer: str) -> str:
    token = f"=== {trainer} ==="
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"missing trainer block: {trainer}")
    next_start = text.find("\n=== ", start + len(token))
    end = len(text) if next_start < 0 else next_start
    block = text[start:end]

    species_matches = list(re.finditer(r"(?m)^Species:\s*(\S+)\s*$", block))
    if len(species_matches) == 5:
        print(f"[gym5-test] {trainer}: already 5 Pokemon")
        return text
    if len(species_matches) != 6:
        raise RuntimeError(
            f"{trainer}: expected exactly 6 Species entries, got {len(species_matches)}"
        )

    removed = species_matches[0].group(1)
    first = species_matches[0].start()
    second = species_matches[1].start()
    # Keep trainer header/options, then keep Pokemon 2..6 unchanged. This preserves
    # the existing ace as the fifth/final party member.
    block2 = block[:first] + block[second:]
    if len(re.findall(r"(?m)^Species:\s*\S+\s*$", block2)) != 5:
        raise RuntimeError(f"{trainer}: trim verification failed")
    print(f"[gym5-test] {trainer}: removed {removed}; ace preserved last")
    return text[:start] + block2 + text[end:]


def force_gen6_exp_share(root: Path) -> Path:
    candidates: list[tuple[Path, int, int]] = []
    name = "IsGen6ExpShareEnabled"

    for path in (root / "src").rglob("*.c"):
        text = path.read_text(encoding="utf-8")
        pos = text.find(name + "(")
        while pos >= 0:
            # A real definition must have a body-opening brace after the signature
            # and before a terminating semicolon.
            paren = text.find("(", pos)
            depth = 0
            close = -1
            for i in range(paren, len(text)):
                if text[i] == "(":
                    depth += 1
                elif text[i] == ")":
                    depth -= 1
                    if depth == 0:
                        close = i
                        break
            if close >= 0:
                brace = text.find("{", close + 1)
                semi = text.find(";", close + 1)
                if brace >= 0 and (semi < 0 or brace < semi):
                    bdepth = 0
                    body_end = -1
                    for j in range(brace, len(text)):
                        if text[j] == "{":
                            bdepth += 1
                        elif text[j] == "}":
                            bdepth -= 1
                            if bdepth == 0:
                                body_end = j + 1
                                break
                    if body_end > 0:
                        candidates.append((path, brace, body_end))
            pos = text.find(name + "(", pos + len(name))

    # Deduplicate definitions if the name also appears inside its own body/comments.
    unique = []
    seen = set()
    for item in candidates:
        key = (item[0], item[1], item[2])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    if len(unique) != 1:
        raise RuntimeError(f"expected one {name} definition, found {len(unique)}")

    path, body_start, body_end = unique[0]
    text = path.read_text(encoding="utf-8")
    old_body = text[body_start:body_end]
    if "return TRUE;" in old_body and "QARRO_TEST_GYM5_EXP_SHARE" in old_body:
        print(f"[exp-share-test] already forced on in {path.relative_to(root)}")
        return path

    new_body = "{\n    // QARRO_TEST_GYM5_EXP_SHARE: test build only.\n    return TRUE;\n}"
    path.write_text(text[:body_start] + new_body + text[body_end:], encoding="utf-8")
    print(f"[exp-share-test] forced native Gen VI party Exp Share ON in {path.relative_to(root)}")
    return path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    party_path = root / "src/data/trainers_frlg.party"
    if not party_path.exists():
        raise SystemExit(f"missing {party_path}")
    text = party_path.read_text(encoding="utf-8")
    for trainer in LEADERS:
        text = trim_party(text, trainer)
    party_path.write_text(text, encoding="utf-8")

    exp_path = force_gen6_exp_share(root)

    # Fail closed: all eight leaders must now be exactly five Pokemon.
    final = party_path.read_text(encoding="utf-8")
    for trainer in LEADERS:
        start = final.index(f"=== {trainer} ===")
        next_start = final.find("\n=== ", start + 1)
        end = len(final) if next_start < 0 else next_start
        count = len(re.findall(r"(?m)^Species:\s*\S+\s*$", final[start:end]))
        if count != 5:
            raise RuntimeError(f"{trainer}: final party count is {count}, expected 5")

    print(
        "[QARRO_TEST_GYM5_EXP_SHARE] PASS: all 8 Kanto gyms use 5 Pokemon; "
        f"native party-wide Exp Share forced ON via {exp_path.relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
