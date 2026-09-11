#!/usr/bin/env python3
"""Qarro v3.25: deterministic 5-of-6 parties for the eight Kanto Gym Leaders.

Each of the eight story Kanto Leaders keeps the six prepared mons installed by
our balance pass. At battle creation exactly five are copied into a temporary
trainer party. The omitted slot is derived from the save's immutable Trainer ID
plus the Gym index, so resetting/reloading the same save cannot reroll it.

Only the eight exact story Leader IDs enter this path. Elite Four, Champion,
postgame and ordinary trainers keep the native party builder. No font,
localization, Ash Bond or Ash Cap code is touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_GYM_FIVE_V3_25"

TARGETS = [
    ("TRAINER_LEADER_BROCK",    [13, 13, 14, 14, 15, 16]),
    ("TRAINER_LEADER_MISTY",    [19, 19, 20, 20, 21, 22]),
    ("TRAINER_LEADER_LT_SURGE", [25, 25, 26, 26, 27, 28]),
    ("TRAINER_LEADER_ERIKA",    [31, 31, 32, 32, 33, 34]),
    ("TRAINER_LEADER_KOGA",     [37, 37, 38, 38, 39, 40]),
    ("TRAINER_LEADER_SABRINA",  [43, 43, 44, 44, 45, 46]),
    ("TRAINER_LEADER_BLAINE",   [49, 49, 50, 50, 51, 52]),
    ("TRAINER_LEADER_GIOVANNI", [55, 55, 56, 56, 57, 58]),
]


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.is_file():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def verify_six_mon_rosters(root: Path) -> list[dict]:
    text = read(root / "src/data/trainers_frlg.party")
    opponents = read(root / "include/constants/opponents_frlg.h")
    report = []
    for trainer, expected_levels in TARGETS:
        if trainer not in opponents:
            die(f"trainer constant missing: {trainer}")
        token = f"=== {trainer} ==="
        start = text.find(token)
        if start < 0:
            die(f"trainer block missing: {trainer}")
        next_start = text.find("\n=== ", start + len(token))
        end = len(text) if next_start < 0 else next_start
        block = text[start:end]
        levels = [int(v) for v in re.findall(r"(?m)^Level:\s*(\d+)\s*$", block)]
        if levels != expected_levels:
            die(f"{trainer}: expected six balanced levels {expected_levels}, got {levels}")
        report.append({"trainer": trainer, "prepared": 6, "battle": 5, "levels": levels})
    return report


def patch_battle_setup(root: Path) -> None:
    path = root / "src/battle_setup.c"
    text = read(path)
    marker = "QARRO_GYM_FIVE_V3_25_BEGIN"
    if marker in text:
        return

    start_token = "static void CreateNPCTrainerParty(struct Pokemon *party, u16 trainerNum)\n{"
    end_token = "\nvoid CreateTrainerPartyForPlayer(void)"
    start = text.find(start_token)
    if start < 0:
        die("CreateNPCTrainerParty start anchor not found")
    end = text.find(end_token, start)
    if end < 0:
        die("CreateTrainerPartyForPlayer end anchor not found")
    original = text[start:end]
    if original.count("CreateNPCTrainerPartyFromTrainer") < 2:
        die("native CreateNPCTrainerParty shape drifted; refusing broad replacement")

    replacement = r'''// QARRO_GYM_FIVE_V3_25_BEGIN
static u8 GetQarroKantoGymIndex(u16 trainerNum)
{
    switch (trainerNum)
    {
    case TRAINER_LEADER_BROCK:    return 0;
    case TRAINER_LEADER_MISTY:    return 1;
    case TRAINER_LEADER_LT_SURGE: return 2;
    case TRAINER_LEADER_ERIKA:    return 3;
    case TRAINER_LEADER_KOGA:     return 4;
    case TRAINER_LEADER_SABRINA:  return 5;
    case TRAINER_LEADER_BLAINE:   return 6;
    case TRAINER_LEADER_GIOVANNI: return 7;
    default:                       return 0xFF;
    }
}

static bool8 TryCreateQarroFiveOfSixGymParty(struct Pokemon *party, u16 trainerNum, const struct Trainer *trainer)
{
    u8 gymIndex = GetQarroKantoGymIndex(trainerNum);
    u8 omitted;
    u8 srcIndex;
    u8 dstIndex = 0;
    struct Trainer tempTrainer;
    struct TrainerMon selectedParty[PARTY_SIZE - 1];

    if (gymIndex == 0xFF)
        return FALSE;
    if (trainer->partySize != PARTY_SIZE || trainer->overrideTrainer != TRAINER_NONE)
        return FALSE;

    omitted = (READ_OTID_FROM_SAVE + (gymIndex + 1) * 17) % PARTY_SIZE;
    for (srcIndex = 0; srcIndex < PARTY_SIZE; srcIndex++)
    {
        if (srcIndex == omitted)
            continue;
        selectedParty[dstIndex++] = trainer->party[srcIndex];
    }
    if (dstIndex != PARTY_SIZE - 1)
        return FALSE;

    tempTrainer = *trainer;
    tempTrainer.party = selectedParty;
    tempTrainer.partySize = PARTY_SIZE - 1;
    tempTrainer.poolSize = 0;
    tempTrainer.aiFlags &= ~AI_FLAG_RANDOMIZE_PARTY_INDICES;
    CreateNPCTrainerPartyFromTrainer(party, &tempTrainer);
    return TRUE;
}

static void CreateNPCTrainerParty(struct Pokemon *party, u16 trainerNum)
{
    const struct Trainer *trainer = GetTrainerStructFromId(trainerNum);

    if (TryCreateQarroFiveOfSixGymParty(party, trainerNum, trainer))
        return;

    if (!trainer->overrideTrainer)
    {
        CreateNPCTrainerPartyFromTrainer(party, trainer);
        return;
    }

    struct Trainer tempTrainer;
    memcpy(&tempTrainer, trainer, sizeof(struct Trainer));
    const struct Trainer *origTrainer = GetTrainerStructFromId(tempTrainer.overrideTrainer);

    tempTrainer.party = origTrainer->party;
    tempTrainer.poolSize = origTrainer->poolSize;
    if (tempTrainer.partySize == 0)
        tempTrainer.partySize = origTrainer->partySize;
    CreateNPCTrainerPartyFromTrainer(party, (const struct Trainer *)(&tempTrainer));
}
// QARRO_GYM_FIVE_V3_25_END
'''

    path.write_text(text[:start] + replacement + text[end:], encoding="utf-8")
    check = read(path)
    helper_start = check.index("static u8 GetQarroKantoGymIndex")
    helper_end = check.index("static bool8 TryCreateQarroFiveOfSixGymParty", helper_start)
    cases = re.findall(r"case\s+(TRAINER_[A-Z0-9_]+)\s*:", check[helper_start:helper_end])
    expected = [trainer for trainer, _ in TARGETS]
    if cases != expected:
        die(f"leader whitelist drifted: {cases}")
    if check.count(marker) != 1:
        die("gym patch marker is not unique")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    rosters = verify_six_mon_rosters(root)
    patch_battle_setup(root)

    report = {
        "marker": MARKER,
        "leaders": rosters,
        "preparedPerLeader": 6,
        "battlePartyPerLeader": 5,
        "selectionKey": "save Trainer ID + gym index",
        "resetReroll": False,
        "scope": "exactly eight Kanto story Gym Leaders",
        "eliteFourChampionPostgameNativePath": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
        "fontLocalizationTouched": False,
    }
    out = root / "build/qarro_gym_five_v3_25_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: 8 Leaders keep six prepared mons and battle with a save-stable five")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
