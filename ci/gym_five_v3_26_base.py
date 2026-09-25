#!/usr/bin/env python3
"""Qarro v3.26: no-legend, Ace-protected deterministic 5-of-6 Kanto Gym parties.

Each story Kanto Leader keeps six prepared candidates. The eight legacy
Legendary/Mythical anchors are replaced with the verified non-legend builds from
the successful isolated Gym test profile. The designated signature Ace is tagged
and can never be selected as the reserve. At battle creation exactly five mons
are copied into a temporary trainer party.

The reserve is derived from save Trainer ID plus Gym index, so reset/reload on
the same save cannot reroll it. Only the eight exact story Leader IDs enter this
path. Elite Four, Champion, postgame and ordinary trainers keep the native party
builder. No font, localization, Ash Bond or Ash Cap code is touched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_GYM_FIVE_V3_26"

TARGETS = [
    {
        "trainer": "TRAINER_LEADER_BROCK",
        "levels": [13, 13, 14, 14, 15, 16],
        "members": ("Golem", "Aerodactyl", "Tyranitar", "Omastar", "Cradily", "Regirock"),
        "legend": "Regirock",
        "replacement_name": "Rhyperior",
        "replacement": """Rhyperior @ Leftovers
Level: 16
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Atk / 4 SpD
Adamant Nature
Ability: Solid Rock
- Earthquake
- Rock Slide
- Megahorn
- Ice Punch""",
        "ace": "Tyranitar",
        "ace_index": 2,
    },
    {
        "trainer": "TRAINER_LEADER_MISTY",
        "levels": [19, 19, 20, 20, 21, 22],
        "members": ("Politoed", "Kingdra", "Starmie", "Gyarados", "Lanturn", "Suicune"),
        "legend": "Suicune",
        "replacement_name": "Milotic",
        "replacement": """Milotic @ Leftovers
Level: 22
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Def / 4 SpD
Bold Nature
Ability: Marvel Scale
- Scald
- Ice Beam
- Recover
- Haze""",
        "ace": "Starmie",
        "ace_index": 2,
    },
    {
        "trainer": "TRAINER_LEADER_LT_SURGE",
        "levels": [25, 25, 26, 26, 27, 28],
        "members": ("Electrode", "Raichu", "Jolteon", "Magneton", "Electivire", "Zapdos"),
        "legend": "Zapdos",
        "replacement_name": "Eelektross",
        "replacement": """Eelektross @ Expert Belt
Level: 28
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 252 SpA / 252 Spe
Modest Nature
Ability: Levitate
- Thunderbolt
- Flamethrower
- Giga Drain
- Volt Switch""",
        "ace": "Electivire",
        "ace_index": 4,
    },
    {
        "trainer": "TRAINER_LEADER_ERIKA",
        "levels": [31, 31, 32, 32, 33, 34],
        "members": ("Ninetales", "Venusaur", "Victreebel", "Vileplume", "Jumpluff", "Virizion"),
        "legend": "Virizion",
        "replacement_name": "Roserade",
        "replacement": """Roserade @ Life Orb
Level: 34
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 252 SpA / 252 Spe
Timid Nature
Ability: Natural Cure
- Giga Drain
- Sludge Bomb
- Sleep Powder
- Toxic Spikes""",
        "ace": "Venusaur",
        "ace_index": 1,
    },
    {
        "trainer": "TRAINER_LEADER_KOGA",
        "levels": [37, 37, 38, 38, 39, 40],
        "members": ("Crobat", "Weezing", "Muk", "Nidoking", "Tentacruel", "Darkrai"),
        "legend": "Darkrai",
        "replacement_name": "Drapion",
        "replacement": """Drapion @ Black Sludge
Level: 40
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 Atk / 4 SpD / 252 Spe
Jolly Nature
Ability: Battle Armor
- Poison Jab
- Crunch
- Earthquake
- Swords Dance""",
        "ace": "Crobat",
        "ace_index": 0,
    },
    {
        "trainer": "TRAINER_LEADER_SABRINA",
        "levels": [43, 43, 44, 44, 45, 46],
        "members": ("Alakazam", "Espeon", "Mr. Mime", "Exeggutor", "Slowking", "Mewtwo"),
        "legend": "Mewtwo",
        "replacement_name": "Gallade",
        "replacement": """Gallade @ Life Orb
Level: 46
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 Atk / 4 SpD / 252 Spe
Jolly Nature
Ability: Steadfast
- Psycho Cut
- Close Combat
- Night Slash
- Swords Dance""",
        "ace": "Alakazam",
        "ace_index": 0,
    },
    {
        "trainer": "TRAINER_LEADER_BLAINE",
        "levels": [49, 49, 50, 50, 51, 52],
        "members": ("Ninetales", "Arcanine", "Rapidash", "Magmar", "Houndoom", "Moltres"),
        "legend": "Moltres",
        "replacement_name": "Chandelure",
        "replacement": """Chandelure @ Life Orb
Level: 52
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 252 SpA / 252 Spe
Timid Nature
Ability: Flash Fire
- Flamethrower
- Shadow Ball
- Energy Ball
- Will-O-Wisp""",
        "ace": "Arcanine",
        "ace_index": 1,
    },
    {
        "trainer": "TRAINER_LEADER_GIOVANNI",
        "levels": [55, 55, 56, 56, 57, 58],
        "members": ("Nidoking", "Nidoqueen", "Rhydon", "Dugtrio", "Donphan", "Groudon"),
        "legend": "Groudon",
        "replacement_name": "Hippowdon",
        "replacement": """Hippowdon @ Leftovers
Level: 58
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Def / 4 SpD
Impish Nature
Ability: Sand Stream
- Earthquake
- Stone Edge
- Slack Off
- Stealth Rock""",
        "ace": "Nidoking",
        "ace_index": 0,
    },
]


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def read(path: Path) -> str:
    if not path.is_file():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def species_line_count(block: str, species: str) -> int:
    return len(re.findall(rf"(?m)^{re.escape(species)}(?: @ [^\n]+)?$", block))


def trainer_block(text: str, trainer: str) -> tuple[int, int, str]:
    token = f"=== {trainer} ==="
    start = text.find(token)
    if start < 0:
        die(f"trainer block missing: {trainer}")
    next_start = text.find("\n=== ", start + len(token))
    end = len(text) if next_start < 0 else next_start
    return start, end, text[start:end]


def patch_no_legend_rosters(root: Path) -> list[dict]:
    path = root / "src/data/trainers_frlg.party"
    text = read(path)
    opponents = read(root / "include/constants/opponents_frlg.h")
    report = []

    for cfg in TARGETS:
        trainer = cfg["trainer"]
        if trainer not in opponents:
            die(f"trainer constant missing: {trainer}")

        start, end, block = trainer_block(text, trainer)
        old_members = cfg["members"]
        final_members = tuple(old_members[:-1]) + (cfg["replacement_name"],)

        # Clean upstream + installed Qarro kit contains the legacy final anchor.
        # Also accept an already-patched block to keep the pass idempotent.
        has_legend = species_line_count(block, cfg["legend"]) == 1
        has_replacement = species_line_count(block, cfg["replacement_name"]) == 1
        if has_legend and has_replacement:
            die(f"{trainer}: both legacy anchor and replacement are present")

        if has_legend:
            for species in old_members:
                if species_line_count(block, species) != 1:
                    die(f"{trainer}: expected one {species} candidate before replacement")

            match = re.search(rf"(?m)^{re.escape(cfg['legend'])}(?: @ [^\n]+)?$", block)
            if match is None:
                die(f"{trainer}: missing legacy anchor {cfg['legend']}")
            # The verified v3.2-v3.8 Kanto legacy anchor is the final candidate.
            for species in old_members[:-1]:
                if re.search(rf"(?m)^{re.escape(species)}(?: @ [^\n]+)?$", block[match.end():]):
                    die(f"{trainer}: {cfg['legend']} is no longer final; refusing broad edit")
            block = block[:match.start()] + cfg["replacement"].rstrip() + "\n"
        elif not has_replacement:
            die(f"{trainer}: neither {cfg['legend']} nor {cfg['replacement_name']} found")

        ace = cfg["ace"]
        ace_match = re.search(rf"(?m)^{re.escape(ace)}(?: @ [^\n]+)?$", block)
        if ace_match is None:
            die(f"{trainer}: missing designated Ace {ace}")
        ace_end = block.find("\n\n", ace_match.end())
        if ace_end < 0:
            ace_end = len(block)
        ace_chunk = block[ace_match.start():ace_end]
        if "Tags: Ace" not in ace_chunk:
            ace_chunk2, count = re.subn(r"(?m)^(Ability:.*)$", r"\1\nTags: Ace", ace_chunk, count=1)
            if count != 1:
                die(f"{trainer}: could not tag {ace} as Ace")
            block = block[:ace_match.start()] + ace_chunk2 + block[ace_end:]

        if species_line_count(block, cfg["legend"]) != 0:
            die(f"{trainer}: legacy anchor {cfg['legend']} survived replacement")
        for species in final_members:
            if species_line_count(block, species) != 1:
                die(f"{trainer}: final candidate verification failed for {species}")
        if len(re.findall(r"(?m)^Tags:\s*Ace\s*$", block)) != 1:
            die(f"{trainer}: expected exactly one Ace tag")

        levels = [int(v) for v in re.findall(r"(?m)^Level:\s*(\d+)\s*$", block)]
        if levels != cfg["levels"]:
            die(f"{trainer}: expected six balanced levels {cfg['levels']}, got {levels}")

        text = text[:start] + block + text[end:]
        report.append(
            {
                "trainer": trainer,
                "prepared": 6,
                "battle": 5,
                "levels": levels,
                "replaced": f"{cfg['legend']} -> {cfg['replacement_name']}",
                "ace": ace,
                "aceIndex": cfg["ace_index"],
            }
        )
        print(
            f"[{MARKER}] {trainer}: {cfg['legend']} -> {cfg['replacement_name']}; "
            f"protected Ace={ace} at index {cfg['ace_index']}"
        )

    path.write_text(text, encoding="utf-8")
    return report


def patch_battle_setup(root: Path) -> None:
    path = root / "src/battle_setup.c"
    text = read(path)
    marker = "QARRO_GYM_FIVE_V3_26_BEGIN"
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

    replacement = r'''// QARRO_GYM_FIVE_V3_26_BEGIN
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

static u8 GetQarroKantoGymAceIndex(u16 trainerNum)
{
    switch (trainerNum)
    {
    case TRAINER_LEADER_BROCK:    return 2; // Tyranitar
    case TRAINER_LEADER_MISTY:    return 2; // Starmie
    case TRAINER_LEADER_LT_SURGE: return 4; // Electivire
    case TRAINER_LEADER_ERIKA:    return 1; // Venusaur
    case TRAINER_LEADER_KOGA:     return 0; // Crobat
    case TRAINER_LEADER_SABRINA:  return 0; // Alakazam
    case TRAINER_LEADER_BLAINE:   return 1; // Arcanine
    case TRAINER_LEADER_GIOVANNI: return 0; // Nidoking
    default:                       return 0xFF;
    }
}

static bool8 TryCreateQarroFiveOfSixGymParty(struct Pokemon *party, u16 trainerNum, const struct Trainer *trainer)
{
    u8 gymIndex = GetQarroKantoGymIndex(trainerNum);
    u8 aceIndex = GetQarroKantoGymAceIndex(trainerNum);
    u8 reservePick;
    u8 omitted;
    u8 srcIndex;
    u8 dstIndex = 0;
    struct Trainer tempTrainer;
    struct TrainerMon selectedParty[PARTY_SIZE - 1];

    if (gymIndex == 0xFF || aceIndex == 0xFF || aceIndex >= PARTY_SIZE)
        return FALSE;
    if (trainer->partySize != PARTY_SIZE || trainer->overrideTrainer != TRAINER_NONE)
        return FALSE;

    // Pick one of the five non-Ace candidates. Mapping skips aceIndex entirely,
    // so the designated Ace is guaranteed in every 5-mon battle party.
    reservePick = (READ_OTID_FROM_SAVE + (gymIndex + 1) * 17) % (PARTY_SIZE - 1);
    omitted = reservePick;
    if (omitted >= aceIndex)
        omitted++;

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
// QARRO_GYM_FIVE_V3_26_END
'''

    path.write_text(text[:start] + replacement + text[end:], encoding="utf-8")
    check = read(path)

    gym_start = check.index("static u8 GetQarroKantoGymIndex")
    gym_end = check.index("static u8 GetQarroKantoGymAceIndex", gym_start)
    gym_cases = re.findall(r"case\s+(TRAINER_[A-Z0-9_]+)\s*:", check[gym_start:gym_end])
    expected = [cfg["trainer"] for cfg in TARGETS]
    if gym_cases != expected:
        die(f"leader whitelist drifted: {gym_cases}")

    ace_start = gym_end
    ace_end = check.index("static bool8 TryCreateQarroFiveOfSixGymParty", ace_start)
    ace_cases = re.findall(r"case\s+(TRAINER_[A-Z0-9_]+)\s*:", check[ace_start:ace_end])
    if ace_cases != expected:
        die(f"Ace whitelist drifted: {ace_cases}")

    for cfg in TARGETS:
        pattern = rf"case\s+{re.escape(cfg['trainer'])}:\s+return\s+{cfg['ace_index']};"
        if re.search(pattern, check[ace_start:ace_end]) is None:
            die(f"Ace index mapping missing/drifted for {cfg['trainer']}")

    if check.count(marker) != 1:
        die("gym patch marker is not unique")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()

    rosters = patch_no_legend_rosters(root)
    patch_battle_setup(root)

    report = {
        "marker": MARKER,
        "leaders": rosters,
        "preparedPerLeader": 6,
        "battlePartyPerLeader": 5,
        "selectionKey": "save Trainer ID + gym index; mapped across five non-Ace candidates",
        "designatedAceGuaranteed": True,
        "resetReroll": False,
        "reserveIndexStoredSeparately": False,
        "scope": "exactly eight Kanto story Gym Leaders",
        "noLegendaryMythicalGymAnchors": True,
        "eliteFourChampionPostgameNativePath": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
        "fontLocalizationTouched": False,
    }
    out = root / "build/qarro_gym_five_v3_25_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: 8 Kanto Leaders use verified no-legend six-mon pools; "
        "battle with a save-stable five and designated Ace always present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
