#!/usr/bin/env python3
"""Qarro v3.132 fix2: use one genuinely-unused packed FireRed save var.

The base v3.132 team data and private trainer IDs remain unchanged.  Only the
save-state implementation is replaced: FireRed var 0x40F7 stores eight 2-bit
Gym states, one per Kanto story Gym.

Per Gym: 00 = uninitialized, 01 = Variant A, 10 = Variant B, 11 = Variant C.
Thus one u16 stores both initialization and chosen variant for all eight Gyms.
The first encounter derives A/B/C deterministically from the save OTID and Gym
index, then persists variant+1. A reset before saving re-derives the same value,
so resets cannot reroll the opponent.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MARKER = "QARRO_KANTO_GYM_ABC_V3_132_FIX2"
SAVE_VAR = "0x40F7"

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


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    validate_save_var(root)

    base_script = Path(__file__).resolve().with_name("gym_kanto_abc_v3_132.py")
    if not base_script.is_file():
        die(f"base v3.132 script missing: {base_script}")

    spec = importlib.util.spec_from_file_location("qarro_gym_kanto_abc_v3_132_base", base_script)
    if spec is None or spec.loader is None:
        die("could not load base v3.132 module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # The dedicated validation above proves 0x40F7 is unused across this pinned
    # source. Prevent the base two-var validator from testing the retired slots.
    module.validate_free_save_vars = lambda _root: None
    module.SELECTOR_CREATE_PARTY = SELECTOR_CREATE_PARTY
    module.VARIANT_BITS_VAR = SAVE_VAR
    module.VARIANT_INIT_VAR = "embedded: 00/01/10/11 state in the same 0x40F7 u16"

    rc = int(module.main() or 0)
    if rc == 0:
        print(
            f"[{MARKER}] PASS: base v3.132 teams/IDs retained; one-u16 0x40F7 selector "
            "stores 8 independent uninitialized/A/B/C states"
        )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
