#!/usr/bin/env python3
"""Qarro v3.88: finalize the Kanto 6v6 migration for compile/play testing.

Repairs trainer metadata headers that the first v3.86 roster replacement pass
intentionally exposed during CI diagnosis, and removes the historical 5-of-6
runtime interception so a six-mon trainer party actually enters battle as 6v6.

This pass does NOT implement final A/B/C selection yet. It establishes a clean,
compilable Variant-A 6v6 baseline first. Ash Bond / Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_GYM_SIX_FINALIZE_V3_88"

HEADERS = {
    "TRAINER_LEADER_BROCK": """Name: BROCK
Class: Leader Frlg
Pic: Leader Brock Frlg
Gender: Male
Music: Male
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
""",
    "TRAINER_LEADER_MISTY": """Name: MISTY
Class: Leader Frlg
Pic: Leader Misty Frlg
Gender: Male
Music: Female
Items: Super Potion
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
""",
    "TRAINER_LEADER_LT_SURGE": """Name: LT. SURGE
Class: Leader Frlg
Pic: Leader Lt Surge Frlg
Gender: Male
Music: Male
Items: Super Potion / Full Heal
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
""",
    "TRAINER_LEADER_ERIKA": """Name: ERIKA
Class: Leader Frlg
Pic: Leader Erika Frlg
Gender: Male
Music: Female
Items: Hyper Potion / Full Heal
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
""",
    "TRAINER_LEADER_KOGA": """Name: KOGA
Class: Leader Frlg
Pic: Leader Koga Frlg
Gender: Male
Music: Male
Items: Hyper Potion / Hyper Potion / Full Heal
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
""",
    "TRAINER_LEADER_SABRINA": """Name: SABRINA
Class: Leader Frlg
Pic: Leader Sabrina Frlg
Gender: Male
Music: Female
Items: Hyper Potion / Hyper Potion / Full Heal
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
""",
    "TRAINER_LEADER_BLAINE": """Name: BLAINE
Class: Leader Frlg
Pic: Leader Blaine Frlg
Gender: Male
Music: Male
Items: Hyper Potion / Hyper Potion / Full Heal
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
""",
    "TRAINER_LEADER_GIOVANNI": """Name: GIOVANNI
Class: Leader Frlg
Pic: Leader Giovanni Frlg
Gender: Male
Music: Aqua
Items: Hyper Potion / Hyper Potion / Full Heal
Double Battle: No
AI: Check Bad Move / Try To Faint / Check Viability
""",
}

ORIGINAL_CREATE_PARTY = '''static void CreateNPCTrainerParty(struct Pokemon *party, u16 trainerNum)
{
    if (!GetTrainerStructFromId(trainerNum)->overrideTrainer)
    {
        CreateNPCTrainerPartyFromTrainer(party, GetTrainerStructFromId(trainerNum));
        return;
    }

    struct Trainer tempTrainer;
    memcpy(&tempTrainer, GetTrainerStructFromId(trainerNum), sizeof(struct Trainer));
    const struct Trainer *origTrainer = GetTrainerStructFromId(tempTrainer.overrideTrainer);

    tempTrainer.party = origTrainer->party;
    tempTrainer.poolSize = origTrainer->poolSize;
    if (tempTrainer.partySize == 0)
        tempTrainer.partySize = origTrainer->partySize;
    CreateNPCTrainerPartyFromTrainer(party, (const struct Trainer *)(&tempTrainer));
}
'''


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def restore_headers(party_path: Path) -> list[str]:
    text = party_path.read_text(encoding="utf-8")
    repaired = []
    for trainer, header in HEADERS.items():
        token = f"=== {trainer} ===\n"
        pos = text.find(token)
        if pos < 0:
            die(f"missing trainer block {trainer}")
        body = pos + len(token)
        if text.startswith("Name:", body):
            # Already correct/idempotent path.
            continue
        text = text[:body] + header + "\n" + text[body:]
        repaired.append(trainer)

    party_path.write_text(text, encoding="utf-8")

    # Verify every target now has parser-required metadata before first Pokemon.
    for trainer in HEADERS:
        token = f"=== {trainer} ===\n"
        pos = text.find(token)
        next_block = text.find("\n=== ", pos + len(token))
        block = text[pos:] if next_block < 0 else text[pos:next_block]
        for required in ("Name:", "Class:", "Pic:", "Gender:", "Music:", "Double Battle:", "AI:"):
            if required not in block.split("\n\n", 1)[0]:
                die(f"{trainer}: missing metadata field {required}")
    return repaired


def remove_legacy_five_of_six(battle_setup: Path) -> bool:
    text = battle_setup.read_text(encoding="utf-8")
    begin = "// QARRO_GYM_FIVE_V3_26_BEGIN"
    end = "// QARRO_GYM_FIVE_V3_26_END"
    if begin not in text and end not in text:
        return False
    if text.count(begin) != 1 or text.count(end) != 1:
        die("legacy 5-of-6 markers are incomplete or duplicated")
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    text, n = pattern.subn(ORIGINAL_CREATE_PARTY.rstrip(), text, count=1)
    if n != 1:
        die("failed to remove legacy 5-of-6 runtime block")
    if "TryCreateQarroFiveOfSixGymParty" in text or "QARRO_GYM_FIVE_V3_26" in text:
        die("legacy 5-of-6 runtime code remained after removal")
    battle_setup.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    party_path = root / "src/data/trainers_frlg.party"
    battle_setup = root / "src/battle_setup.c"
    if not party_path.is_file() or not battle_setup.is_file():
        die("required trainer/battle source missing")

    repaired = restore_headers(party_path)
    removed = remove_legacy_five_of_six(battle_setup)

    out = root / "build/qarro_gym_six_finalize_v3_88_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "leaderHeadersRepaired": repaired,
        "leaderHeaderCount": len(HEADERS),
        "legacyFiveOfSixRemoved": removed,
        "battleMode": "6v6 Variant A compile/play-test baseline",
        "nextStep": "Add save-fixed A/B/C selector only after this baseline is green.",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[{MARKER}] PASS: leader metadata valid; legacy 5-of-6 removed={removed}; 6v6 baseline ready for trainerproc")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
