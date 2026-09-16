#!/usr/bin/env python3
"""Qarro v3.132 fix2: final Kanto A/B/C with safe IDs and one packed save var.

Reuses the final v3.132 Kanto B/C roster/build data, but fixes the integration
point against the actual FIRST PLAYABLE source state: Champion postgame owns
trainer IDs 624..643 and content v3.1 owns 644..648, so the sixteen private B/C
party records must occupy 649..664 and TRAINERS_COUNT_FRLG becomes 665.

The runtime state uses one genuinely-unused FireRed save var, 0x40F7.  It stores
eight 2-bit Gym states: 00=uninitialized, 01=A, 10=B, 11=C.  First encounter
derives the choice deterministically from the save OTID and Gym index, then
persists it.  Defeat/reset therefore cannot be used to reroll the team.

Original story Leader IDs remain Variant A; maps, defeat flags, rematches, E4,
Champion, localization/font, Ash Bond and Ash Cap remain outside this pass.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_KANTO_GYM_ABC_V3_132_FIX2"
SAVE_VAR = "0x40F7"
FIRST_NEW_TRAINER_ID = 649
LAST_NEW_TRAINER_ID = 664
EXPECTED_TRAINERS_COUNT = 649
NEW_TRAINERS_COUNT = 665

SELECTOR_CREATE_PARTY = r"""// QARRO_KANTO_GYM_ABC_V3_132_BEGIN
#define QARRO_KANTO_GYM_STATE_VAR 0x40F7

static u8 GetQarroKantoGymIndexV3132(u16 trainerNum)
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

static u8 DeriveQarroKantoGymVariantV3132(u8 gymIndex)
{
    u32 seed = READ_OTID_FROM_SAVE;
    seed ^= 0x9E3779B9u * (gymIndex + 1u);
    seed ^= seed >> 16;
    seed *= 0x7FEB352Du;
    seed ^= seed >> 15;
    return seed % 3u;
}

static u8 GetQarroKantoGymVariantV3132(u8 gymIndex)
{
    u16 packed = VarGet(QARRO_KANTO_GYM_STATE_VAR);
    u8 shift = gymIndex * 2u;
    u8 stored = (packed >> shift) & 3u;

    if (stored == 0u)
    {
        u8 variant = DeriveQarroKantoGymVariantV3132(gymIndex);
        stored = variant + 1u; // 1=A, 2=B, 3=C; zero remains uninitialized.
        packed &= ~(3u << shift);
        packed |= (u16)stored << shift;
        VarSet(QARRO_KANTO_GYM_STATE_VAR, packed);
        return variant;
    }

    return stored - 1u;
}

static u16 GetQarroKantoGymPartyTrainerV3132(u16 trainerNum, u8 variant)
{
    if (variant == 0)
        return trainerNum;

    switch (trainerNum)
    {
    case TRAINER_LEADER_BROCK:
        return variant == 1 ? TRAINER_QARRO_BROCK_B : TRAINER_QARRO_BROCK_C;
    case TRAINER_LEADER_MISTY:
        return variant == 1 ? TRAINER_QARRO_MISTY_B : TRAINER_QARRO_MISTY_C;
    case TRAINER_LEADER_LT_SURGE:
        return variant == 1 ? TRAINER_QARRO_LT_SURGE_B : TRAINER_QARRO_LT_SURGE_C;
    case TRAINER_LEADER_ERIKA:
        return variant == 1 ? TRAINER_QARRO_ERIKA_B : TRAINER_QARRO_ERIKA_C;
    case TRAINER_LEADER_KOGA:
        return variant == 1 ? TRAINER_QARRO_KOGA_B : TRAINER_QARRO_KOGA_C;
    case TRAINER_LEADER_SABRINA:
        return variant == 1 ? TRAINER_QARRO_SABRINA_B : TRAINER_QARRO_SABRINA_C;
    case TRAINER_LEADER_BLAINE:
        return variant == 1 ? TRAINER_QARRO_BLAINE_B : TRAINER_QARRO_BLAINE_C;
    case TRAINER_LEADER_GIOVANNI:
        return variant == 1 ? TRAINER_QARRO_GIOVANNI_B : TRAINER_QARRO_GIOVANNI_C;
    default:
        return trainerNum;
    }
}

static void CreateNPCTrainerParty(struct Pokemon *party, u16 trainerNum)
{
    const struct Trainer *trainer = GetTrainerStructFromId(trainerNum);
    u8 gymIndex;

    if (!trainer->overrideTrainer)
    {
        gymIndex = GetQarroKantoGymIndexV3132(trainerNum);
        if (gymIndex != 0xFF)
        {
            u8 variant = GetQarroKantoGymVariantV3132(gymIndex);
            u16 partyTrainerNum = GetQarroKantoGymPartyTrainerV3132(trainerNum, variant);
            CreateNPCTrainerPartyFromTrainer(party, GetTrainerStructFromId(partyTrainerNum));
            return;
        }

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
// QARRO_KANTO_GYM_ABC_V3_132_END
"""


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def validate_save_var(root: Path) -> None:
    vars_frlg = (root / "include/constants/vars_frlg.h").resolve()
    vars_common = (root / "include/constants/vars.h").resolve()
    if not vars_frlg.is_file() or not vars_common.is_file():
        die("variable definition headers missing")

    frlg_text = vars_frlg.read_text(encoding="utf-8")
    common_text = vars_common.read_text(encoding="utf-8")
    if "#define VAR_0x40F7                 0x40F7" not in frlg_text:
        die("FireRed 0x40F7 is no longer the expected anonymous slot")
    if "#define VAR_UNUSED_0x40F7" not in common_text or "0x40F7 // Unused Var" not in common_text:
        die("shared 0x40F7 is no longer explicitly marked unused")

    definition_headers = {vars_frlg, vars_common}
    needles = ("VAR_0x40F7", "VAR_UNUSED_0x40F7", "0x40F7")
    hits: list[str] = []
    for base in (root / "src", root / "data", root / "include"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".c", ".h", ".inc", ".s", ".txt"}:
                continue
            if path.resolve() in definition_headers:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if any(needle in text for needle in needles):
                hits.append(str(path.relative_to(root)))
                if len(hits) >= 10:
                    break
        if hits:
            break
    if hits:
        die(f"save var 0x40F7 has runtime references: {hits}")


def load_base() -> object:
    base_script = Path(__file__).resolve().with_name("gym_kanto_abc_v3_132.py")
    if not base_script.is_file():
        die(f"base v3.132 script missing: {base_script}")
    spec = importlib.util.spec_from_file_location("qarro_gym_kanto_abc_v3_132_base", base_script)
    if spec is None or spec.loader is None:
        die("could not load base v3.132 module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def patch_opponents(module: object, path: Path) -> None:
    text = module.read(path)
    if module.MARKER in text or "TRAINER_QARRO_BROCK_B" in text:
        die("v3.132 trainer constants already present; refusing duplicate installation")

    count_match = re.search(r"(?m)^#define\s+TRAINERS_COUNT_FRLG\s+(\d+)\s*$", text)
    if not count_match:
        die("TRAINERS_COUNT_FRLG missing")
    current_count = int(count_match.group(1))
    if current_count != EXPECTED_TRAINERS_COUNT:
        die(f"expected TRAINERS_COUNT_FRLG={EXPECTED_TRAINERS_COUNT}, got {current_count}")
    if not re.search(r"(?m)^#define\s+MAX_TRAINERS_COUNT_FRLG\s+768\s*$", text):
        die("MAX_TRAINERS_COUNT_FRLG drifted; refusing to consume trainer flag space")

    numeric_ids = [
        int(m.group(1))
        for m in re.finditer(r"(?m)^#define\s+TRAINER_[A-Z0-9_]+\s+(\d+)\s*$", text)
    ]
    if not numeric_ids or max(numeric_ids) != FIRST_NEW_TRAINER_ID - 1:
        die(
            f"trainer ID extension point drifted: expected last numeric ID "
            f"{FIRST_NEW_TRAINER_ID - 1}, got {max(numeric_ids) if numeric_ids else 'missing'}"
        )

    define_lines = [
        f"#define {name:<48} {FIRST_NEW_TRAINER_ID + i}"
        for i, name in enumerate(module.TRAINER_ID_ORDER)
    ]
    insertion = (
        "// QARRO_KANTO_GYM_ABC_V3_132 trainer-only B/C party records\n"
        + "\n".join(define_lines)
        + "\n"
        + f"#define TRAINERS_COUNT_FRLG                      {NEW_TRAINERS_COUNT}"
    )
    text = text[:count_match.start()] + insertion + text[count_match.end():]
    path.write_text(text, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    module = load_base()

    party_path = root / "src/data/trainers_frlg.party"
    opponents_path = root / "include/constants/opponents_frlg.h"
    battle_setup = root / "src/battle_setup.c"
    for path in (party_path, opponents_path, battle_setup):
        if not path.is_file():
            die(f"required source missing: {path}")

    validate_save_var(root)
    patch_opponents(module, opponents_path)
    variants = module.patch_parties(party_path)

    module.SELECTOR_CREATE_PARTY = SELECTOR_CREATE_PARTY
    module.patch_battle_setup(battle_setup)

    opponents = module.read(opponents_path)
    if not re.search(
        rf"(?m)^#define\s+TRAINERS_COUNT_FRLG\s+{NEW_TRAINERS_COUNT}\s*$",
        opponents,
    ):
        die(f"post-write trainer count is not {NEW_TRAINERS_COUNT}")
    for i, name in enumerate(module.TRAINER_ID_ORDER):
        wanted = FIRST_NEW_TRAINER_ID + i
        if not re.search(rf"(?m)^#define\s+{re.escape(name)}\s+{wanted}\s*$", opponents):
            die(f"missing exact trainer id {name}={wanted}")

    selector_text = module.read(battle_setup)
    if selector_text.count("QARRO_KANTO_GYM_STATE_VAR 0x40F7") != 1:
        die("single-var selector postcondition failed")
    if "0x40BD" in selector_text or "0x40BE" in selector_text:
        die("retired two-var selector constants leaked into runtime source")

    audit = {
        "marker": MARKER,
        "battleMode": "Kanto story Gym 6v6 A/B/C",
        "storyLeaderCount": 8,
        "newPartyOnlyTrainerRecords": 16,
        "newTrainerIdRange": [FIRST_NEW_TRAINER_ID, LAST_NEW_TRAINER_ID],
        "trainersCountBefore": EXPECTED_TRAINERS_COUNT,
        "trainersCountAfter": NEW_TRAINERS_COUNT,
        "selector": {
            "stateVar": SAVE_VAR,
            "selection": "save-OTID-derived A/B/C on first story-Leader party creation",
            "persistence": "one packed u16; per-Gym 00/01/10/11 state; deterministic fallback prevents reset reroll",
            "storedEncoding": {"uninitialized": 0, "A": 1, "B": 2, "C": 3},
        },
        "variantRecords": variants,
        "originalStoryLeaderIdsRemainVariantA": True,
        "rematchesTouched": False,
        "eliteFourTouched": False,
        "championTouched": False,
        "localizationTouched": False,
        "fontTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_kanto_gym_abc_v3_132_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: 8 Kanto story Leaders use save-fixed A/B/C 6v6; "
        f"16 B/C records installed at IDs {FIRST_NEW_TRAINER_ID}-{LAST_NEW_TRAINER_ID}; "
        f"TRAINERS_COUNT_FRLG={NEW_TRAINERS_COUNT}; one-var 0x40F7 persistence; "
        "rematches/E4/Champion/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
