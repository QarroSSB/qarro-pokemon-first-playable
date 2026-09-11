#!/usr/bin/env python3
"""Qarro v3.24: persistent 5-of-6 parties for the eight Kanto Gym Leaders.

Each leader keeps the six prepared mons from the balance pass, but exactly five
are materialized for the battle. One omitted slot is selected deterministically
from the save's Trainer ID on first use and stored in a persistent event var.
Thus reset/reload cannot reroll the five, including before the first post-choice
save. Only the eight exact Kanto Leader trainer IDs enter this path; Elite Four,
Champion, postgame and all ordinary trainers keep the native party builder.

Ash Bond / Ash Cap and the frozen font/localization pipeline are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_GYM_FIVE_V3_24"

TARGETS = [
    ("TRAINER_LEADER_BROCK",    "VAR_0x40F8", [13, 13, 14, 14, 15, 16]),
    ("TRAINER_LEADER_MISTY",    "VAR_0x40F9", [19, 19, 20, 20, 21, 22]),
    ("TRAINER_LEADER_LT_SURGE", "VAR_0x40FA", [25, 25, 26, 26, 27, 28]),
    ("TRAINER_LEADER_ERIKA",    "VAR_0x40FB", [31, 31, 32, 32, 33, 34]),
    ("TRAINER_LEADER_KOGA",     "VAR_0x40FC", [37, 37, 38, 38, 39, 40]),
    ("TRAINER_LEADER_SABRINA",  "VAR_0x40FD", [43, 43, 44, 44, 45, 46]),
    ("TRAINER_LEADER_BLAINE",   "VAR_0x40FE", [49, 49, 50, 50, 51, 52]),
    ("TRAINER_LEADER_GIOVANNI", "VAR_0x40FF", [55, 55, 56, 56, 57, 58]),
]


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.is_file():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def verify_six_mon_rosters(root: Path) -> list[dict]:
    party_text = read(root / "src/data/trainers_frlg.party")
    opponents = read(root / "include/constants/opponents_frlg.h")
    report = []
    for trainer, var_name, expected_levels in TARGETS:
        if trainer not in opponents:
            die(f"trainer constant missing: {trainer}")
        start_token = f"=== {trainer} ==="
        start = party_text.find(start_token)
        if start < 0:
            die(f"trainer block missing: {trainer}")
        next_start = party_text.find("\n=== ", start + len(start_token))
        end = len(party_text) if next_start < 0 else next_start
        block = party_text[start:end]
        levels = [int(v) for v in re.findall(r"(?m)^Level:\s*(\d+)\s*$", block)]
        if levels != expected_levels:
            die(f"{trainer}: expected balanced six-mon levels {expected_levels}, got {levels}")
        report.append({"trainer": trainer, "persistentVar": var_name, "levels": levels, "prepared": 6, "battle": 5})
    return report


def verify_persistent_vars_free(root: Path) -> None:
    tokens = [var_name for _, var_name, _ in TARGETS]
    definition_files = {
        Path("include/constants/vars_frlg.h"),
        Path("include/constants/vars.h"),
    }
    collisions: dict[str, list[str]] = {token: [] for token in tokens}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".c", ".h", ".inc", ".s", ".json"}:
            continue
        rel = path.relative_to(root)
        if rel in definition_files:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in tokens:
            if token in text:
                collisions[token].append(str(rel))
    used = {token: paths for token, paths in collisions.items() if paths}
    if used:
        die(f"persistent vars are already consumed at runtime: {used}")


def patch_battle_setup(root: Path) -> None:
    path = root / "src/battle_setup.c"
    text = read(path)

    old = '''static void CreateNPCTrainerParty(struct Pokemon *party, u16 trainerNum)\n{\n    if (!GetTrainerStructFromId(trainerNum)->overrideTrainer)\n    {\n        CreateNPCTrainerPartyFromTrainer(party, GetTrainerStructFromId(trainerNum));\n        return;\n    }\n    struct Trainer tempTrainer;\n    memcpy(&tempTrainer, GetTrainerStructFromId(trainerNum), sizeof(struct Trainer));\n    const struct Trainer *origTrainer = GetTrainerStructFromId(tempTrainer.overrideTrainer);\n\n    tempTrainer.party = origTrainer->party;\n\n    tempTrainer.poolSize = origTrainer->poolSize;\n    if (tempTrainer.partySize == 0)\n        tempTrainer.partySize = origTrainer->partySize;\n    CreateNPCTrainerPartyFromTrainer(party, (const struct Trainer *)(&tempTrainer));\n}\n'''

    new = '''// QARRO_GYM_FIVE_V3_24_BEGIN\n// Return 0..7 only for the eight story Kanto Gym Leaders. Every other trainer,\n// including Elite Four / Champion / postgame, remains on the native path.\nstatic u8 GetQarroKantoGymIndex(u16 trainerNum)\n{\n    switch (trainerNum)\n    {\n    case TRAINER_LEADER_BROCK:    return 0;\n    case TRAINER_LEADER_MISTY:    return 1;\n    case TRAINER_LEADER_LT_SURGE: return 2;\n    case TRAINER_LEADER_ERIKA:    return 3;\n    case TRAINER_LEADER_KOGA:     return 4;\n    case TRAINER_LEADER_SABRINA:  return 5;\n    case TRAINER_LEADER_BLAINE:   return 6;\n    case TRAINER_LEADER_GIOVANNI: return 7;\n    default:                       return 0xFF;\n    }\n}\n\nstatic bool8 TryCreateQarroFiveOfSixGymParty(struct Pokemon *party, u16 trainerNum, const struct Trainer *trainer)\n{\n    u8 gymIndex = GetQarroKantoGymIndex(trainerNum);\n    u16 storedChoice;\n    u8 omitted;\n    u8 sourceIndex;\n    u8 outputIndex = 0;\n    u32 trainerId;\n    struct TrainerGenerator *trainerGen;\n\n    if (gymIndex == 0xFF)\n        return FALSE;\n\n    // Qarro's eight Leader data blocks are statically audited as exactly six.\n    // If source data ever drifts, retain the native builder rather than reading\n    // outside the prepared party.\n    if (trainer->partySize != PARTY_SIZE)\n        return FALSE;\n\n    // 0x40F8..0x40FF are persistent FRLG vars, one per Kanto Gym. A stored\n    // value of 1..6 means "omit source slot value-1". Zero means uninitialized.\n    storedChoice = VarGet(0x40F8 + gymIndex);\n    if (storedChoice < 1 || storedChoice > PARTY_SIZE)\n    {\n        // Trainer ID is immutable for the save. This makes the initial choice\n        // stable even if the player resets before saving after first entering\n        // the battle; VarSet then persists the same choice normally thereafter.\n        trainerId = READ_OTID_FROM_SAVE;\n        omitted = (trainerId + (gymIndex + 1) * 17) % PARTY_SIZE;\n        VarSet(0x40F8 + gymIndex, omitted + 1);\n    }\n    else\n    {\n        omitted = storedChoice - 1;\n    }\n\n    ZeroPartyMons(party);\n    trainerGen = AllocZeroed(sizeof(struct TrainerGenerator));\n    MakeTrainerGenerator(trainerGen, trainer);\n    for (sourceIndex = 0; sourceIndex < PARTY_SIZE; sourceIndex++)\n    {\n        if (sourceIndex == omitted)\n            continue;\n        GenerateMonFromTrainerMon(&party[outputIndex], &trainer->party[sourceIndex], trainerGen);\n        outputIndex++;\n    }\n    Free(trainerGen);\n    return TRUE;\n}\n// QARRO_GYM_FIVE_V3_24_END\n\nstatic void CreateNPCTrainerParty(struct Pokemon *party, u16 trainerNum)\n{\n    const struct Trainer *trainer = GetTrainerStructFromId(trainerNum);\n\n    if (TryCreateQarroFiveOfSixGymParty(party, trainerNum, trainer))\n        return;\n\n    if (!trainer->overrideTrainer)\n    {\n        CreateNPCTrainerPartyFromTrainer(party, trainer);\n        return;\n    }\n    struct Trainer tempTrainer;\n    memcpy(&tempTrainer, trainer, sizeof(struct Trainer));\n    const struct Trainer *origTrainer = GetTrainerStructFromId(tempTrainer.overrideTrainer);\n\n    tempTrainer.party = origTrainer->party;\n\n    tempTrainer.poolSize = origTrainer->poolSize;\n    if (tempTrainer.partySize == 0)\n        tempTrainer.partySize = origTrainer->partySize;\n    CreateNPCTrainerPartyFromTrainer(party, (const struct Trainer *)(&tempTrainer));\n}\n'''

    if "QARRO_GYM_FIVE_V3_24_BEGIN" in text:
        # Idempotence is useful for local reruns, but still prove exact whitelist.
        patched = text
    else:
        if text.count(old) != 1:
            die(f"native CreateNPCTrainerParty anchor drifted; expected 1, found {text.count(old)}")
        patched = text.replace(old, new, 1)
        path.write_text(patched, encoding="utf-8")

    patched = read(path)
    if patched.count("QARRO_GYM_FIVE_V3_24_BEGIN") != 1:
        die("gym 5-of-6 marker is not unique")
    helper_start = patched.index("static u8 GetQarroKantoGymIndex")
    helper_end = patched.index("static bool8 TryCreateQarroFiveOfSixGymParty", helper_start)
    helper = patched[helper_start:helper_end]
    cases = re.findall(r"case\s+(TRAINER_[A-Z0-9_]+)\s*:", helper)
    expected_cases = [trainer for trainer, _, _ in TARGETS]
    if cases != expected_cases:
        die(f"leader whitelist drifted: expected {expected_cases}, got {cases}")
    if "CreateNPCTrainerPartyFromTrainer(party, trainer);" not in patched:
        die("native non-gym trainer path was not preserved")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    rosters = verify_six_mon_rosters(root)
    verify_persistent_vars_free(root)
    patch_battle_setup(root)

    report = {
        "marker": MARKER,
        "leaders": rosters,
        "preparedPerLeader": 6,
        "battlePartyPerLeader": 5,
        "selection": "one omitted slot derived from immutable save Trainer ID, then stored",
        "resetReroll": False,
        "persistentVars": [f"0x{value:04X}" for value in range(0x40F8, 0x4100)],
        "scope": "exactly eight Kanto Gym Leader trainer IDs",
        "eliteFourChampionPostgameNativePath": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
        "fontLocalizationTouched": False,
    }
    out = root / "build/qarro_gym_five_v3_24_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: 8 Kanto Leaders keep six prepared mons but battle with a "
        f"save-stable five; all non-gym trainers retain native party creation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
