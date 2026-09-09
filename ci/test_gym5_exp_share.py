#!/usr/bin/env python3
"""TEST ONLY: native 5-of-6 Kanto gyms, no legends, party-wide Exp Share.

The six-candidate pools remain intact, but every Gym Leader uses native
Party Size: 5. Each former legendary sixth candidate is replaced by a strong
non-legendary thematic Pokemon and a signature non-legend is tagged Ace.
This branch is for difficulty / EXP-curve testing only. Main, Ash Bond and
Ash Cap are untouched.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LEADERS = {
    "TRAINER_LEADER_BROCK": {
        "members": ("Golem", "Aerodactyl", "Tyranitar", "Omastar", "Cradily", "Regirock"),
        "legend": "Regirock",
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
        "replacement_name": "Rhyperior",
        "ace": "Tyranitar",
    },
    "TRAINER_LEADER_MISTY": {
        "members": ("Politoed", "Kingdra", "Starmie", "Gyarados", "Lanturn", "Suicune"),
        "legend": "Suicune",
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
        "replacement_name": "Milotic",
        "ace": "Starmie",
    },
    "TRAINER_LEADER_LT_SURGE": {
        "members": ("Electrode", "Raichu", "Jolteon", "Magneton", "Electivire", "Zapdos"),
        "legend": "Zapdos",
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
        "replacement_name": "Eelektross",
        "ace": "Electivire",
    },
    "TRAINER_LEADER_ERIKA": {
        "members": ("Ninetales", "Venusaur", "Victreebel", "Vileplume", "Jumpluff", "Virizion"),
        "legend": "Virizion",
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
        "replacement_name": "Roserade",
        "ace": "Venusaur",
    },
    "TRAINER_LEADER_KOGA": {
        "members": ("Crobat", "Weezing", "Muk", "Nidoking", "Tentacruel", "Darkrai"),
        "legend": "Darkrai",
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
        "replacement_name": "Drapion",
        "ace": "Crobat",
    },
    "TRAINER_LEADER_BLAINE": {
        "members": ("Ninetales", "Arcanine", "Rapidash", "Magmar", "Houndoom", "Moltres"),
        "legend": "Moltres",
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
        "replacement_name": "Chandelure",
        "ace": "Arcanine",
    },
    "TRAINER_LEADER_SABRINA": {
        "members": ("Alakazam", "Espeon", "Mr. Mime", "Exeggutor", "Slowking", "Mewtwo"),
        "legend": "Mewtwo",
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
        "replacement_name": "Gallade",
        "ace": "Alakazam",
    },
    "TRAINER_LEADER_GIOVANNI": {
        "members": ("Nidoking", "Nidoqueen", "Rhydon", "Dugtrio", "Donphan", "Groudon"),
        "legend": "Groudon",
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
        "replacement_name": "Hippowdon",
        "ace": "Nidoking",
    },
}


def species_line_count(block: str, species: str) -> int:
    return len(re.findall(rf"(?m)^{re.escape(species)}(?: @ [^\n]+)?$", block))


def patch_leader(text: str, trainer: str, cfg: dict) -> str:
    token = f"=== {trainer} ==="
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"missing trainer block: {trainer}")
    next_start = text.find("\n=== ", start + len(token))
    end = len(text) if next_start < 0 else next_start
    block = text[start:end]

    for species in cfg["members"]:
        if species_line_count(block, species) != 1:
            raise RuntimeError(f"{trainer}: expected one {species} candidate")

    party_size = re.findall(r"(?m)^Party Size:\s*(\d+)\s*$", block)
    if party_size:
        if party_size != ["5"]:
            raise RuntimeError(f"{trainer}: unexpected Party Size {party_size}")
    else:
        block, count = re.subn(r"(?m)^(AI:.*)$", r"\1\nParty Size: 5", block, count=1)
        if count != 1:
            raise RuntimeError(f"{trainer}: could not add Party Size: 5")

    legend = cfg["legend"]
    match = re.search(rf"(?m)^{re.escape(legend)}(?: @ [^\n]+)?$", block)
    if match is None:
        raise RuntimeError(f"{trainer}: missing legendary candidate {legend}")
    # All eight verified v3.2 legendary candidates are the sixth/final block.
    for species in cfg["members"][:-1]:
        later = re.search(rf"(?m)^{re.escape(species)}(?: @ [^\n]+)?$", block[match.end():])
        if later:
            raise RuntimeError(f"{trainer}: {legend} is no longer final; refusing broad edit")
    block = block[:match.start()] + cfg["replacement"].rstrip() + "\n"

    ace = cfg["ace"]
    ace_match = re.search(rf"(?m)^{re.escape(ace)}(?: @ [^\n]+)?$", block)
    if ace_match is None:
        raise RuntimeError(f"{trainer}: missing signature ace {ace}")
    ace_end = block.find("\n\n", ace_match.end())
    if ace_end < 0:
        ace_end = len(block)
    ace_chunk = block[ace_match.start():ace_end]
    if "Tags: Ace" not in ace_chunk:
        ace_chunk2, count = re.subn(r"(?m)^(Ability:.*)$", r"\1\nTags: Ace", ace_chunk, count=1)
        if count != 1:
            raise RuntimeError(f"{trainer}: could not tag {ace} as Ace")
        block = block[:ace_match.start()] + ace_chunk2 + block[ace_end:]

    if species_line_count(block, legend) != 0:
        raise RuntimeError(f"{trainer}: legendary {legend} survived replacement")
    if species_line_count(block, cfg["replacement_name"]) != 1:
        raise RuntimeError(f"{trainer}: replacement verification failed")
    if len(re.findall(r"(?m)^Party Size:\s*5\s*$", block)) != 1:
        raise RuntimeError(f"{trainer}: Party Size verification failed")
    if len(re.findall(r"(?m)^Tags:\s*Ace\s*$", block)) != 1:
        raise RuntimeError(f"{trainer}: Ace tag verification failed")

    final_names = tuple(cfg["members"][:-1]) + (cfg["replacement_name"],)
    if any(species_line_count(block, species) != 1 for species in final_names):
        raise RuntimeError(f"{trainer}: final six-candidate pool verification failed")

    print(
        f"[gym5-test] {trainer}: Party Size 5 from 6; "
        f"{legend} -> {cfg['replacement_name']}; guaranteed Ace={ace}"
    )
    return text[:start] + block + text[end:]


def force_gen6_exp_share(root: Path) -> Path:
    candidates: list[tuple[Path, int, int]] = []
    name = "IsGen6ExpShareEnabled"

    for path in (root / "src").rglob("*.c"):
        text = path.read_text(encoding="utf-8")
        pos = text.find(name + "(")
        while pos >= 0:
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
    new_body = "{\n    // QARRO_TEST_GYM5_EXP_SHARE: test build only.\n    return TRUE;\n}"
    text = text[:body_start] + new_body + text[body_end:]
    path.write_text(text, encoding="utf-8")
    print(f"[exp-share-test] native Gen VI party Exp Share forced ON in {path.relative_to(root)}")
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
    for trainer, cfg in LEADERS.items():
        text = patch_leader(text, trainer, cfg)
    party_path.write_text(text, encoding="utf-8")

    exp_path = force_gen6_exp_share(root)

    final = party_path.read_text(encoding="utf-8")
    for cfg in LEADERS.values():
        if re.search(rf"(?m)^{re.escape(cfg['legend'])}(?: @ [^\n]+)?$", final):
            raise RuntimeError(f"legendary remained in gym data: {cfg['legend']}")

    print(
        "[QARRO_TEST_GYM5_EXP_SHARE] PASS: all 8 Kanto gyms use native 5-of-6, "
        "no legendary gym candidates remain; party-wide Exp Share forced ON via "
        + str(exp_path.relative_to(root))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
