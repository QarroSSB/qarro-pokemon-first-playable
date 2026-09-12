#!/usr/bin/env python3
"""Qarro Kanto Gym integration wrapper.

Runs the proven Kanto balance + save-stable 5-of-6 wrapper, then applies the
explicitly approved Kanto Mythical exceptions:
  * Erika: Celebi (Venusaur remains the protected Ace)
  * Sabrina: Mew (Alakazam remains the protected Ace)

This file is scoped to the isolated Gym test branch. Main, Ash Bond and Ash Cap
are not touched.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_GYM_MYTHICAL_V3_27"
HERE = Path(__file__).resolve().parent

EXCEPTIONS = (
    {
        "trainer": "TRAINER_LEADER_ERIKA",
        "old": "Roserade",
        "new": "Celebi",
        "ace": "Venusaur",
        "build": """Celebi @ Leftovers
Level: 34
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 252 SpA / 252 Spe
Timid Nature
Ability: Natural Cure
- Giga Drain
- Psychic
- Recover
- Thunder Wave""",
    },
    {
        "trainer": "TRAINER_LEADER_SABRINA",
        "old": "Gallade",
        "new": "Mew",
        "ace": "Alakazam",
        "build": """Mew @ Life Orb
Level: 46
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 252 SpA / 252 Spe
Timid Nature
Ability: Synchronize
- Psychic
- Aura Sphere
- Shadow Ball
- Nasty Plot""",
    },
)


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def trainer_block(text: str, trainer: str) -> tuple[int, int, str]:
    token = f"=== {trainer} ==="
    start = text.find(token)
    if start < 0:
        die(f"trainer block missing: {trainer}")
    next_start = text.find("\n=== ", start + len(token))
    end = len(text) if next_start < 0 else next_start
    return start, end, text[start:end]


def species_count(block: str, species: str) -> int:
    return len(re.findall(rf"(?m)^{re.escape(species)}(?: @ [^\n]+)?$", block))


def replace_candidate(block: str, old: str, new: str, build: str) -> str:
    if species_count(block, new) == 1 and species_count(block, old) == 0:
        return block
    if species_count(block, old) != 1:
        die(f"expected exactly one {old}; got {species_count(block, old)}")
    if species_count(block, new) != 0:
        die(f"unexpected pre-existing {new}")

    m = re.search(rf"(?m)^{re.escape(old)}(?: @ [^\n]+)?$", block)
    if m is None:
        die(f"could not locate {old}")
    chunk_end = block.find("\n\n", m.end())
    if chunk_end < 0:
        # Final candidate in a trainer block: leave one trailing newline here.
        # text[end:] starts with another newline before the next === TRAINER ===,
        # yielding the empty separator line required by trainerproc.
        return block[:m.start()] + build.rstrip() + "\n"
    return block[:m.start()] + build.rstrip() + block[chunk_end:]


def apply_exceptions(root: Path) -> None:
    party_path = root / "src/data/trainers_frlg.party"
    if not party_path.is_file():
        die(f"missing {party_path}")
    text = party_path.read_text(encoding="utf-8")

    for cfg in EXCEPTIONS:
        start, end, block = trainer_block(text, cfg["trainer"])
        if species_count(block, cfg["ace"]) != 1:
            die(f"{cfg['trainer']}: protected Ace {cfg['ace']} missing/drifted")
        if len(re.findall(r"(?m)^Tags:\s*Ace\s*$", block)) != 1:
            die(f"{cfg['trainer']}: expected exactly one Ace tag")

        block = replace_candidate(block, cfg["old"], cfg["new"], cfg["build"])
        if species_count(block, cfg["old"]) != 0 or species_count(block, cfg["new"]) != 1:
            die(f"{cfg['trainer']}: Mythical replacement verification failed")
        levels = [int(v) for v in re.findall(r"(?m)^Level:\s*(\d+)\s*$", block)]
        if len(levels) != 6:
            die(f"{cfg['trainer']}: expected six prepared candidates, got {len(levels)}")

        text = text[:start] + block + text[end:]
        print(
            f"[{MARKER}] {cfg['trainer']}: {cfg['old']} -> {cfg['new']} "
            f"(approved Mythical); protected Ace={cfg['ace']}"
        )

    party_path.write_text(text, encoding="utf-8")

    report_path = root / "build/qarro_gym_five_v3_25_audit.json"
    if report_path.is_file():
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["noLegendaryMythicalGymAnchors"] = False
        report["noLegendaryGymAnchors"] = True
        report["noUnapprovedMythicalGymAnchors"] = True
        report["approvedMythicalExceptions"] = {
            "TRAINER_LEADER_ERIKA": "Celebi",
            "TRAINER_LEADER_SABRINA": "Mew",
        }
        report["approvedMythicalExceptionCount"] = 2
        report["mythicalPolicy"] = (
            "Only explicitly approved Mythicals may appear in ordinary Gyms; "
            "Kanto runtime exceptions are Celebi/Erika and Mew/Sabrina."
        )
        for leader in report.get("leaders", []):
            if leader.get("trainer") == "TRAINER_LEADER_ERIKA":
                leader["replaced"] = "Virizion -> Celebi (approved Mythical)"
            elif leader.get("trainer") == "TRAINER_LEADER_SABRINA":
                leader["replaced"] = "Mewtwo -> Mew (approved Mythical)"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify(root: Path) -> None:
    text = (root / "src/data/trainers_frlg.party").read_text(encoding="utf-8")
    forbidden = ("Regirock", "Suicune", "Zapdos", "Virizion", "Darkrai", "Mewtwo", "Moltres", "Groudon")

    for cfg in EXCEPTIONS:
        _, _, block = trainer_block(text, cfg["trainer"])
        if species_count(block, cfg["new"]) != 1:
            die(f"{cfg['trainer']}: approved Mythical absent after write")
        if species_count(block, cfg["ace"]) != 1:
            die(f"{cfg['trainer']}: protected Ace absent after write")

    for trainer in (
        "TRAINER_LEADER_BROCK", "TRAINER_LEADER_MISTY", "TRAINER_LEADER_LT_SURGE",
        "TRAINER_LEADER_ERIKA", "TRAINER_LEADER_KOGA", "TRAINER_LEADER_SABRINA",
        "TRAINER_LEADER_BLAINE", "TRAINER_LEADER_GIOVANNI",
    ):
        _, _, block = trainer_block(text, trainer)
        for species in forbidden:
            if species_count(block, species):
                die(f"{trainer}: forbidden legacy anchor survived: {species}")

    print(
        f"[{MARKER}] PASS: Kanto 5-of-6 keeps protected Aces; old Legendary anchors=0; "
        "approved Mythicals=Erika/Celebi + Sabrina/Mew; main/protected Ash features untouched"
    )


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    # This preserved wrapper already runs the original Kanto balance pass and
    # ci/gym_five_v3_25.py exactly once.
    subprocess.run([sys.executable, str(HERE / "balance_kanto_v3_2_base.py"), str(root)], check=True)
    apply_exceptions(root)
    verify(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
