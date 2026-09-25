#!/usr/bin/env python3
"""Qarro v3.132: final-canon Kanto Gym A/B/C 6v6 runtime with save-fixed selection.

Extends the already-green v3.86/v3.88 Kanto Variant-A 6v6 baseline with two
additional party records per story Leader. The original eight story Leader IDs
remain Variant A so all map scripts, defeat flags, battle text, item use and
Leader metadata stay untouched.

At first party creation for a Kanto story Leader, a save-specific A/B/C variant
is derived from the saved OTID, written to two otherwise-unused FRLG variables,
and reused on every retry. Resetting before a manual save still resolves to the
same variant because the fallback derivation is deterministic from the existing
save OTID. Rematches, Elite Four, Champion, localization, font, Ash Bond and
Ash Cap are outside this pass.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_KANTO_GYM_ABC_V3_132"
VARIANT_BITS_VAR = "0x40BD"
VARIANT_INIT_VAR = "0x40BE"
FIRST_NEW_TRAINER_ID = 624
LAST_NEW_TRAINER_ID = 639
EXPECTED_TRAINERS_COUNT = 624
NEW_TRAINERS_COUNT = 640

EXPECTED_A = {'TRAINER_LEADER_BLAINE': ['Ninetales', 'Arcanine', 'Rapidash', 'Magmar', 'Houndoom', 'Magcargo'],
 'TRAINER_LEADER_BROCK': ['Golem', 'Aerodactyl', 'Tyranitar', 'Omastar', 'Cradily', 'Kabutops'],
 'TRAINER_LEADER_ERIKA': ['Ninetales', 'Venusaur', 'Victreebel', 'Vileplume', 'Jumpluff', 'Celebi'],
 'TRAINER_LEADER_GIOVANNI': ['Nidoking', 'Nidoqueen', 'Rhydon', 'Dugtrio', 'Donphan', 'Hippowdon'],
 'TRAINER_LEADER_KOGA': ['Crobat', 'Weezing', 'Muk', 'Venomoth', 'Tentacruel', 'Qwilfish'],
 'TRAINER_LEADER_LT_SURGE': ['Electrode', 'Raichu', 'Jolteon', 'Magneton', 'Electivire', 'Ampharos'],
 'TRAINER_LEADER_MISTY': ['Politoed', 'Lapras', 'Starmie', 'Vaporeon', 'Lanturn', 'Slowbro'],
 'TRAINER_LEADER_SABRINA': ['Alakazam', 'Espeon', 'Mr. Mime', 'Exeggutor', 'Slowking', 'Mew']}
HEADERS = {'TRAINER_LEADER_BLAINE': 'Name: BLAINE\nClass: Leader Frlg\nPic: Leader Blaine Frlg\nGender: Male\nMusic: Male\nItems: Hyper Potion / Hyper Potion / Full Heal\nDouble Battle: No\nAI: Check Bad Move / Try To Faint / Check Viability',
 'TRAINER_LEADER_BROCK': 'Name: BROCK\nClass: Leader Frlg\nPic: Leader Brock Frlg\nGender: Male\nMusic: Male\nDouble Battle: No\nAI: Check Bad Move / Try To Faint / Check Viability',
 'TRAINER_LEADER_ERIKA': 'Name: ERIKA\nClass: Leader Frlg\nPic: Leader Erika Frlg\nGender: Male\nMusic: Female\nItems: Hyper Potion / Full Heal\nDouble Battle: No\nAI: Check Bad Move / Try To Faint / Check Viability',
 'TRAINER_LEADER_GIOVANNI': 'Name: GIOVANNI\nClass: Leader Frlg\nPic: Leader Giovanni Frlg\nGender: Male\nMusic: Aqua\nItems: Hyper Potion / Hyper Potion / Full Heal\nDouble Battle: No\nAI: Check Bad Move / Try To Faint / Check Viability',
 'TRAINER_LEADER_KOGA': 'Name: KOGA\nClass: Leader Frlg\nPic: Leader Koga Frlg\nGender: Male\nMusic: Male\nItems: Hyper Potion / Hyper Potion / Full Heal\nDouble Battle: No\nAI: Check Bad Move / Try To Faint / Check Viability',
 'TRAINER_LEADER_LT_SURGE': 'Name: LT. SURGE\nClass: Leader Frlg\nPic: Leader Lt Surge Frlg\nGender: Male\nMusic: Male\nItems: Super Potion / Full Heal\nDouble Battle: No\nAI: Check Bad Move / Try To Faint / Check Viability',
 'TRAINER_LEADER_MISTY': 'Name: MISTY\nClass: Leader Frlg\nPic: Leader Misty Frlg\nGender: Male\nMusic: Female\nItems: Super Potion\nDouble Battle: No\nAI: Check Bad Move / Try To Faint / Check Viability',
 'TRAINER_LEADER_SABRINA': 'Name: SABRINA\nClass: Leader Frlg\nPic: Leader Sabrina Frlg\nGender: Male\nMusic: Female\nItems: Hyper Potion / Hyper Potion / Full Heal\nDouble Battle: No\nAI: Check Bad Move / Try To Faint / Check Viability'}
VARIANTS = {'1B': {'ace': 'Tyranitar',
        'base_trainer': 'TRAINER_LEADER_BROCK',
        'ev_budget': 0,
        'gym': 1,
        'item_count': 2,
        'iv': 12,
        'leader': 'Брок',
        'party': [{'ability': 'Sturdy',
                   'evs': None,
                   'item': None,
                   'iv': 12,
                   'level': 13,
                   'moves': ['Stealth Rock', 'Earthquake', 'Rock Slide', 'Rock Polish'],
                   'nature': 'Adamant',
                   'species': 'Golem'},
                  {'ability': 'Battle Armor',
                   'evs': None,
                   'item': None,
                   'iv': 12,
                   'level': 13,
                   'moves': ['Waterfall', 'Rock Slide', 'Aqua Jet', 'Swords Dance'],
                   'nature': 'Adamant',
                   'species': 'Kabutops'},
                  {'ability': 'Sturdy',
                   'evs': None,
                   'item': None,
                   'iv': 12,
                   'level': 14,
                   'moves': ['Toxic', 'Encore', 'Protect', 'Rock Tomb'],
                   'nature': 'Careful',
                   'species': 'Shuckle'},
                  {'ability': 'Shell Armor',
                   'evs': None,
                   'item': None,
                   'iv': 12,
                   'level': 14,
                   'moves': ['Surf', 'Ice Beam', 'Ancient Power', 'Protect'],
                   'nature': 'Modest',
                   'species': 'Omastar'},
                  {'ability': 'Storm Drain',
                   'evs': None,
                   'item': 'Leftovers',
                   'iv': 12,
                   'level': 15,
                   'moves': ['Toxic', 'Recover', 'Giga Drain', 'Ancient Power'],
                   'nature': 'Calm',
                   'species': 'Cradily'},
                  {'ability': 'Sand Stream',
                   'evs': None,
                   'item': 'Leftovers',
                   'iv': 12,
                   'level': 16,
                   'moves': ['Stealth Rock', 'Crunch', 'Rock Slide', 'Thunder Wave'],
                   'nature': 'Careful',
                   'species': 'Tyranitar'}],
        'trainer': 'TRAINER_QARRO_BROCK_B',
        'variant': 'B'},
 '1C': {'ace': 'Tyranitar',
        'base_trainer': 'TRAINER_LEADER_BROCK',
        'ev_budget': 0,
        'gym': 1,
        'item_count': 2,
        'iv': 12,
        'leader': 'Брок',
        'party': [{'ability': 'Sand Stream',
                   'evs': None,
                   'item': 'Leftovers',
                   'iv': 12,
                   'level': 13,
                   'moves': ['Stealth Rock', 'Crunch', 'Rock Slide', 'Thunder Wave'],
                   'nature': 'Careful',
                   'species': 'Tyranitar'},
                  {'ability': 'Lightning Rod',
                   'evs': None,
                   'item': None,
                   'iv': 12,
                   'level': 13,
                   'moves': ['Earthquake', 'Rock Slide', 'Megahorn', 'Thunder Punch'],
                   'nature': 'Adamant',
                   'species': 'Rhydon'},
                  {'ability': 'Pressure',
                   'evs': None,
                   'item': None,
                   'iv': 12,
                   'level': 14,
                   'moves': ['Rock Slide', 'Earthquake', 'Thunder Fang', 'Ice Fang'],
                   'nature': 'Jolly',
                   'species': 'Aerodactyl'},
                  {'ability': 'Shell Armor',
                   'evs': None,
                   'item': 'White Herb',
                   'iv': 12,
                   'level': 14,
                   'moves': ['Hydro Pump', 'Ice Beam', 'Earth Power', 'Shell Smash'],
                   'nature': 'Modest',
                   'species': 'Omastar'},
                  {'ability': 'Storm Drain',
                   'evs': None,
                   'item': None,
                   'iv': 12,
                   'level': 15,
                   'moves': ['Giga Drain', 'Toxic', 'Recover', 'Protect'],
                   'nature': 'Calm',
                   'species': 'Cradily'},
                  {'ability': 'Battle Armor',
                   'evs': None,
                   'item': None,
                   'iv': 12,
                   'level': 16,
                   'moves': ['Waterfall', 'Rock Slide', 'Aqua Jet', 'Swords Dance'],
                   'nature': 'Adamant',
                   'species': 'Kabutops'}],
        'trainer': 'TRAINER_QARRO_BROCK_C',
        'variant': 'C'},
 '2B': {'ace': 'Starmie',
        'base_trainer': 'TRAINER_LEADER_MISTY',
        'ev_budget': 0,
        'gym': 2,
        'item_count': 3,
        'iv': 16,
        'leader': 'Мисти',
        'party': [{'ability': 'Natural Cure',
                   'evs': None,
                   'item': 'Leftovers',
                   'iv': 16,
                   'level': 19,
                   'moves': ['Thunder', 'Scald', 'Recover', 'Rapid Spin'],
                   'nature': 'Timid',
                   'species': 'Starmie'},
                  {'ability': 'Regenerator',
                   'evs': None,
                   'item': None,
                   'iv': 16,
                   'level': 19,
                   'moves': ['Scald', 'Psychic', 'Slack Off', 'Thunder Wave'],
                   'nature': 'Bold',
                   'species': 'Slowbro'},
                  {'ability': 'Skill Link',
                   'evs': None,
                   'item': 'White Herb',
                   'iv': 16,
                   'level': 20,
                   'moves': ['Shell Smash', 'Icicle Spear', 'Rock Blast', 'Razor Shell'],
                   'nature': 'Jolly',
                   'species': 'Cloyster'},
                  {'ability': 'Unaware',
                   'evs': None,
                   'item': None,
                   'iv': 16,
                   'level': 20,
                   'moves': ['Scald', 'Earthquake', 'Recover', 'Toxic'],
                   'nature': 'Impish',
                   'species': 'Quagsire'},
                  {'ability': 'Water Absorb',
                   'evs': None,
                   'item': None,
                   'iv': 16,
                   'level': 21,
                   'moves': ['Surf', 'Ice Beam', 'Thunderbolt', 'Perish Song'],
                   'nature': 'Modest',
                   'species': 'Lapras'},
                  {'ability': 'Water Absorb',
                   'evs': None,
                   'item': 'Leftovers',
                   'iv': 16,
                   'level': 22,
                   'moves': ['Scald', 'Ice Beam', 'Wish', 'Protect'],
                   'nature': 'Bold',
                   'species': 'Vaporeon'}],
        'trainer': 'TRAINER_QARRO_MISTY_B',
        'variant': 'B'},
 '2C': {'ace': 'Starmie',
        'base_trainer': 'TRAINER_LEADER_MISTY',
        'ev_budget': 0,
        'gym': 2,
        'item_count': 3,
        'iv': 16,
        'leader': 'Мисти',
        'party': [{'ability': 'Volt Absorb',
                   'evs': None,
                   'item': None,
                   'iv': 16,
                   'level': 19,
                   'moves': ['Scald', 'Volt Switch', 'Ice Beam', 'Thunder Wave'],
                   'nature': 'Calm',
                   'species': 'Lanturn'},
                  {'ability': 'Water Absorb',
                   'evs': None,
                   'item': None,
                   'iv': 16,
                   'level': 19,
                   'moves': ['Surf', 'Ice Beam', 'Thunderbolt', 'Perish Song'],
                   'nature': 'Modest',
                   'species': 'Lapras'},
                  {'ability': 'Natural Cure',
                   'evs': None,
                   'item': 'Leftovers',
                   'iv': 16,
                   'level': 20,
                   'moves': ['Thunderbolt', 'Scald', 'Ice Beam', 'Recover'],
                   'nature': 'Timid',
                   'species': 'Starmie'},
                  {'ability': 'Regenerator',
                   'evs': None,
                   'item': 'Leftovers',
                   'iv': 16,
                   'level': 20,
                   'moves': ['Scald', 'Psychic', 'Slack Off', 'Ice Beam'],
                   'nature': 'Calm',
                   'species': 'Slowking'},
                  {'ability': 'Water Absorb',
                   'evs': None,
                   'item': 'Leftovers',
                   'iv': 16,
                   'level': 21,
                   'moves': ['Scald', 'Ice Beam', 'Wish', 'Protect'],
                   'nature': 'Bold',
                   'species': 'Vaporeon'},
                  {'ability': 'Regenerator',
                   'evs': None,
                   'item': None,
                   'iv': 16,
                   'level': 22,
                   'moves': ['Scald', 'Psychic', 'Slack Off', 'Thunder Wave'],
                   'nature': 'Bold',
                   'species': 'Slowbro'}],
        'trainer': 'TRAINER_QARRO_MISTY_C',
        'variant': 'C'},
 '3B': {'ace': 'Electivire',
        'base_trainer': 'TRAINER_LEADER_LT_SURGE',
        'ev_budget': 80,
        'gym': 3,
        'item_count': 4,
        'iv': 20,
        'leader': 'Лейтенант Сёрдж',
        'party': [{'ability': 'Lightning Rod',
                   'evs': '40 SpA / 40 Spe',
                   'item': 'Life Orb',
                   'iv': 20,
                   'level': 25,
                   'moves': ['Thunderbolt', 'Focus Blast', 'Grass Knot', 'Nasty Plot'],
                   'nature': 'Timid',
                   'species': 'Raichu'},
                  {'ability': 'Static',
                   'evs': '40 SpA / 40 Spe',
                   'item': None,
                   'iv': 20,
                   'level': 25,
                   'moves': ['Thunderbolt', 'Focus Blast', 'Signal Beam', 'Volt Switch'],
                   'nature': 'Modest',
                   'species': 'Ampharos'},
                  {'ability': 'Volt Absorb',
                   'evs': '40 HP / 40 SpD',
                   'item': None,
                   'iv': 20,
                   'level': 26,
                   'moves': ['Scald', 'Volt Switch', 'Ice Beam', 'Thunder Wave'],
                   'nature': 'Calm',
                   'species': 'Lanturn'},
                  {'ability': 'Magnet Pull',
                   'evs': '40 SpA / 40 Spe',
                   'item': 'Eviolite',
                   'iv': 20,
                   'level': 26,
                   'moves': ['Thunderbolt', 'Flash Cannon', 'Volt Switch', 'Hidden Power'],
                   'nature': 'Timid',
                   'species': 'Magneton'},
                  {'ability': 'Vital Spirit',
                   'evs': '40 SpA / 40 Spe',
                   'item': 'Eviolite',
                   'iv': 20,
                   'level': 27,
                   'moves': ['Thunderbolt', 'Focus Blast', 'Psychic', 'Hidden Power'],
                   'nature': 'Timid',
                   'species': 'Electabuzz'},
                  {'ability': 'Motor Drive',
                   'evs': '40 Atk / 40 Spe',
                   'item': 'Expert Belt',
                   'iv': 20,
                   'level': 28,
                   'moves': ['Wild Charge', 'Ice Punch', 'Earthquake', 'Cross Chop'],
                   'nature': 'Jolly',
                   'species': 'Electivire'}],
        'trainer': 'TRAINER_QARRO_LT_SURGE_B',
        'variant': 'B'},
 '3C': {'ace': 'Electivire',
        'base_trainer': 'TRAINER_LEADER_LT_SURGE',
        'ev_budget': 80,
        'gym': 3,
        'item_count': 4,
        'iv': 20,
        'leader': 'Лейтенант Сёрдж',
        'party': [{'ability': 'Lightning Rod',
                   'evs': '40 SpA / 40 Spe',
                   'item': 'Life Orb',
                   'iv': 20,
                   'level': 25,
                   'moves': ['Thunderbolt', 'Focus Blast', 'Grass Knot', 'Nasty Plot'],
                   'nature': 'Timid',
                   'species': 'Raichu'},
                  {'ability': 'Volt Absorb',
                   'evs': '40 SpA / 40 Spe',
                   'item': 'Choice Specs',
                   'iv': 20,
                   'level': 25,
                   'moves': ['Thunderbolt', 'Volt Switch', 'Shadow Ball', 'Hidden Power'],
                   'nature': 'Timid',
                   'species': 'Jolteon'},
                  {'ability': 'Soundproof',
                   'evs': '40 SpA / 40 Spe',
                   'item': None,
                   'iv': 20,
                   'level': 26,
                   'moves': ['Rain Dance', 'Thunder', 'Taunt', 'Volt Switch'],
                   'nature': 'Timid',
                   'species': 'Electrode'},
                  {'ability': 'Static',
                   'evs': '40 SpA / 40 Spe',
                   'item': None,
                   'iv': 20,
                   'level': 26,
                   'moves': ['Thunderbolt', 'Focus Blast', 'Signal Beam', 'Volt Switch'],
                   'nature': 'Modest',
                   'species': 'Ampharos'},
                  {'ability': 'Lightning Rod',
                   'evs': '40 SpA / 40 Spe',
                   'item': 'Choice Specs',
                   'iv': 20,
                   'level': 27,
                   'moves': ['Thunderbolt', 'Volt Switch', 'Flamethrower', 'Hidden Power'],
                   'nature': 'Timid',
                   'species': 'Manectric'},
                  {'ability': 'Motor Drive',
                   'evs': '40 Atk / 40 Spe',
                   'item': 'Expert Belt',
                   'iv': 20,
                   'level': 28,
                   'moves': ['Wild Charge', 'Ice Punch', 'Earthquake', 'Cross Chop'],
                   'nature': 'Jolly',
                   'species': 'Electivire'}],
        'trainer': 'TRAINER_QARRO_LT_SURGE_C',
        'variant': 'C'},
 '4B': {'ace': 'Venusaur',
        'base_trainer': 'TRAINER_LEADER_ERIKA',
        'ev_budget': 160,
        'gym': 4,
        'item_count': 5,
        'iv': 24,
        'leader': 'Эрика',
        'party': [{'ability': 'Effect Spore',
                   'evs': '80 HP / 80 Def',
                   'item': 'Black Sludge',
                   'iv': 24,
                   'level': 31,
                   'moves': ['Giga Drain', 'Sludge Bomb', 'Sleep Powder', 'Synthesis'],
                   'nature': 'Bold',
                   'species': 'Vileplume'},
                  {'ability': 'Chlorophyll',
                   'evs': '80 HP / 80 Def',
                   'item': None,
                   'iv': 24,
                   'level': 31,
                   'moves': ['Giga Drain', 'Sleep Powder', 'Synthesis', 'Hidden Power'],
                   'nature': 'Bold',
                   'species': 'Bellossom'},
                  {'ability': 'Natural Cure',
                   'evs': '80 SpA / 80 Spe',
                   'item': 'Leftovers',
                   'iv': 24,
                   'level': 32,
                   'moves': ['Giga Drain', 'Psychic', 'Recover', 'Thunder Wave'],
                   'nature': 'Timid',
                   'species': 'Celebi'},
                  {'ability': 'Chlorophyll',
                   'evs': '80 SpA / 80 Spe',
                   'item': 'Life Orb',
                   'iv': 24,
                   'level': 32,
                   'moves': ['Psychic', 'Giga Drain', 'Sleep Powder', 'Hidden Power'],
                   'nature': 'Modest',
                   'species': 'Exeggutor'},
                  {'ability': 'Dry Skin',
                   'evs': '80 HP / 80 SpD',
                   'item': 'Leftovers',
                   'iv': 24,
                   'level': 33,
                   'moves': ['Spore', 'Leech Seed', 'X-Scissor', 'Synthesis'],
                   'nature': 'Careful',
                   'species': 'Parasect'},
                  {'ability': 'Chlorophyll',
                   'evs': '80 SpA / 80 Spe',
                   'item': 'Life Orb',
                   'iv': 24,
                   'level': 34,
                   'moves': ['Growth', 'Giga Drain', 'Sludge Bomb', 'Sleep Powder'],
                   'nature': 'Timid',
                   'species': 'Venusaur'}],
        'trainer': 'TRAINER_QARRO_ERIKA_B',
        'variant': 'B'},
 '4C': {'ace': 'Venusaur',
        'base_trainer': 'TRAINER_LEADER_ERIKA',
        'ev_budget': 160,
        'gym': 4,
        'item_count': 5,
        'iv': 24,
        'leader': 'Эрика',
        'party': [{'ability': 'Chlorophyll',
                   'evs': '80 SpA / 80 Spe',
                   'item': 'Life Orb',
                   'iv': 24,
                   'level': 31,
                   'moves': ['Growth', 'Giga Drain', 'Sludge Bomb', 'Sleep Powder'],
                   'nature': 'Timid',
                   'species': 'Venusaur'},
                  {'ability': 'Regenerator',
                   'evs': '80 HP / 80 Def',
                   'item': 'Leftovers',
                   'iv': 24,
                   'level': 31,
                   'moves': ['Giga Drain', 'Sleep Powder', 'Hidden Power', 'Knock Off'],
                   'nature': 'Bold',
                   'species': 'Tangrowth'},
                  {'ability': 'Chlorophyll',
                   'evs': '80 Atk / 80 Spe',
                   'item': 'Life Orb',
                   'iv': 24,
                   'level': 32,
                   'moves': ['Swords Dance', 'Leaf Blade', 'Sucker Punch', 'Poison Jab'],
                   'nature': 'Adamant',
                   'species': 'Victreebel'},
                  {'ability': 'Chlorophyll',
                   'evs': '80 Atk / 80 Spe',
                   'item': None,
                   'iv': 24,
                   'level': 32,
                   'moves': ['Sleep Powder', 'Leech Seed', 'Substitute', 'Encore'],
                   'nature': 'Jolly',
                   'species': 'Jumpluff'},
                  {'ability': 'Natural Cure',
                   'evs': '80 SpA / 80 Spe',
                   'item': 'Leftovers',
                   'iv': 24,
                   'level': 33,
                   'moves': ['Giga Drain', 'Psychic', 'Recover', 'Thunder Wave'],
                   'nature': 'Timid',
                   'species': 'Celebi'},
                  {'ability': 'Effect Spore',
                   'evs': '80 HP / 80 Def',
                   'item': 'Black Sludge',
                   'iv': 24,
                   'level': 34,
                   'moves': ['Giga Drain', 'Sludge Bomb', 'Sleep Powder', 'Synthesis'],
                   'nature': 'Bold',
                   'species': 'Vileplume'}],
        'trainer': 'TRAINER_QARRO_ERIKA_C',
        'variant': 'C'},
 '5B': {'ace': 'Crobat',
        'base_trainer': 'TRAINER_LEADER_KOGA',
        'ev_budget': 252,
        'gym': 5,
        'item_count': 6,
        'iv': 26,
        'leader': 'Кога',
        'party': [{'ability': 'Inner Focus',
                   'evs': '252 Spe',
                   'item': 'Black Sludge',
                   'iv': 26,
                   'level': 37,
                   'moves': ['Brave Bird', 'U-Turn', 'Roost', 'Taunt'],
                   'nature': 'Jolly',
                   'species': 'Crobat'},
                  {'ability': 'Tinted Lens',
                   'evs': '252 Spe',
                   'item': 'Leftovers',
                   'iv': 26,
                   'level': 37,
                   'moves': ['Quiver Dance', 'Bug Buzz', 'Sleep Powder', 'Roost'],
                   'nature': 'Timid',
                   'species': 'Venomoth'},
                  {'ability': 'Levitate',
                   'evs': '252 Def',
                   'item': 'Black Sludge',
                   'iv': 26,
                   'level': 38,
                   'moves': ['Will-O-Wisp', 'Sludge Bomb', 'Fire Blast', 'Pain Split'],
                   'nature': 'Bold',
                   'species': 'Weezing'},
                  {'ability': 'Intimidate',
                   'evs': '252 Def',
                   'item': 'Black Sludge',
                   'iv': 26,
                   'level': 38,
                   'moves': ['Spikes', 'Toxic Spikes', 'Waterfall', 'Taunt'],
                   'nature': 'Impish',
                   'species': 'Qwilfish'},
                  {'ability': 'Insomnia',
                   'evs': '252 Atk',
                   'item': 'Focus Sash',
                   'iv': 26,
                   'level': 39,
                   'moves': ['Toxic Spikes', 'Megahorn', 'Poison Jab', 'Sucker Punch'],
                   'nature': 'Adamant',
                   'species': 'Ariados'},
                  {'ability': 'Sticky Hold',
                   'evs': '252 Atk',
                   'item': 'Black Sludge',
                   'iv': 26,
                   'level': 40,
                   'moves': ['Poison Jab', 'Shadow Sneak', 'Ice Punch', 'Curse'],
                   'nature': 'Adamant',
                   'species': 'Muk'}],
        'trainer': 'TRAINER_QARRO_KOGA_B',
        'variant': 'B'},
 '5C': {'ace': 'Crobat',
        'base_trainer': 'TRAINER_LEADER_KOGA',
        'ev_budget': 252,
        'gym': 5,
        'item_count': 6,
        'iv': 26,
        'leader': 'Кога',
        'party': [{'ability': 'Levitate',
                   'evs': '252 Def',
                   'item': 'Black Sludge',
                   'iv': 26,
                   'level': 37,
                   'moves': ['Will-O-Wisp', 'Sludge Bomb', 'Fire Blast', 'Pain Split'],
                   'nature': 'Bold',
                   'species': 'Weezing'},
                  {'ability': 'Sheer Force',
                   'evs': '252 SpA',
                   'item': 'Life Orb',
                   'iv': 26,
                   'level': 37,
                   'moves': ['Earth Power', 'Sludge Wave', 'Ice Beam', 'Stealth Rock'],
                   'nature': 'Modest',
                   'species': 'Nidoqueen'},
                  {'ability': 'Inner Focus',
                   'evs': '252 Spe',
                   'item': 'Black Sludge',
                   'iv': 26,
                   'level': 38,
                   'moves': ['Brave Bird', 'U-Turn', 'Roost', 'Taunt'],
                   'nature': 'Jolly',
                   'species': 'Crobat'},
                  {'ability': 'Rain Dish',
                   'evs': '252 Spe',
                   'item': 'Black Sludge',
                   'iv': 26,
                   'level': 38,
                   'moves': ['Scald', 'Rapid Spin', 'Toxic Spikes', 'Ice Beam'],
                   'nature': 'Timid',
                   'species': 'Tentacruel'},
                  {'ability': 'Sticky Hold',
                   'evs': '252 Atk',
                   'item': 'Black Sludge',
                   'iv': 26,
                   'level': 39,
                   'moves': ['Poison Jab', 'Shadow Sneak', 'Ice Punch', 'Curse'],
                   'nature': 'Adamant',
                   'species': 'Muk'},
                  {'ability': 'Tinted Lens',
                   'evs': '252 Spe',
                   'item': 'Leftovers',
                   'iv': 26,
                   'level': 40,
                   'moves': ['Quiver Dance', 'Bug Buzz', 'Sleep Powder', 'Roost'],
                   'nature': 'Timid',
                   'species': 'Venomoth'}],
        'trainer': 'TRAINER_QARRO_KOGA_C',
        'variant': 'C'},
 '6B': {'ace': 'Alakazam',
        'base_trainer': 'TRAINER_LEADER_SABRINA',
        'ev_budget': 360,
        'gym': 6,
        'item_count': 6,
        'iv': 28,
        'leader': 'Сабрина',
        'party': [{'ability': 'Magic Guard',
                   'evs': '252 SpA / 108 Spe',
                   'item': 'Life Orb',
                   'iv': 28,
                   'level': 43,
                   'moves': ['Psychic', 'Focus Blast', 'Shadow Ball', 'Calm Mind'],
                   'nature': 'Timid',
                   'species': 'Alakazam'},
                  {'ability': 'Regenerator',
                   'evs': '252 HP / 108 Def',
                   'item': 'Leftovers',
                   'iv': 28,
                   'level': 43,
                   'moves': ['Scald', 'Psychic', 'Slack Off', 'Thunder Wave'],
                   'nature': 'Bold',
                   'species': 'Slowbro'},
                  {'ability': 'Dry Skin',
                   'evs': '252 SpA / 108 Spe',
                   'item': 'Focus Sash',
                   'iv': 28,
                   'level': 44,
                   'moves': ['Lovely Kiss', 'Ice Beam', 'Psychic', 'Nasty Plot'],
                   'nature': 'Timid',
                   'species': 'Jynx'},
                  {'ability': 'Insomnia',
                   'evs': '252 HP / 108 SpD',
                   'item': 'Leftovers',
                   'iv': 28,
                   'level': 44,
                   'moves': ['Psychic', 'Calm Mind', 'Shadow Ball', 'Thunder Wave'],
                   'nature': 'Calm',
                   'species': 'Hypno'},
                  {'ability': 'Magic Bounce',
                   'evs': '252 SpA / 108 Spe',
                   'item': 'Leftovers',
                   'iv': 28,
                   'level': 45,
                   'moves': ['Psychic', 'Shadow Ball', 'Morning Sun', 'Calm Mind'],
                   'nature': 'Timid',
                   'species': 'Espeon'},
                  {'ability': 'Synchronize',
                   'evs': '252 SpA / 108 Spe',
                   'item': 'Leftovers',
                   'iv': 28,
                   'level': 46,
                   'moves': ['Psychic', 'Aura Sphere', 'Recover', 'Thunder Wave'],
                   'nature': 'Timid',
                   'species': 'Mew'}],
        'trainer': 'TRAINER_QARRO_SABRINA_B',
        'variant': 'B'},
 '6C': {'ace': 'Alakazam',
        'base_trainer': 'TRAINER_LEADER_SABRINA',
        'ev_budget': 360,
        'gym': 6,
        'item_count': 6,
        'iv': 28,
        'leader': 'Сабрина',
        'party': [{'ability': 'Magic Bounce',
                   'evs': '252 SpA / 108 Spe',
                   'item': 'Leftovers',
                   'iv': 28,
                   'level': 43,
                   'moves': ['Psychic', 'Shadow Ball', 'Morning Sun', 'Calm Mind'],
                   'nature': 'Timid',
                   'species': 'Espeon'},
                  {'ability': 'Filter',
                   'evs': '252 SpA / 108 Spe',
                   'item': 'Light Clay',
                   'iv': 28,
                   'level': 43,
                   'moves': ['Reflect', 'Light Screen', 'Psychic', 'Baton Pass'],
                   'nature': 'Timid',
                   'species': 'Mr. Mime'},
                  {'ability': 'Magic Guard',
                   'evs': '252 SpA / 108 Spe',
                   'item': 'Life Orb',
                   'iv': 28,
                   'level': 44,
                   'moves': ['Psychic', 'Focus Blast', 'Shadow Ball', 'Calm Mind'],
                   'nature': 'Timid',
                   'species': 'Alakazam'},
                  {'ability': 'Synchronize',
                   'evs': '252 SpA / 108 Spe',
                   'item': 'Leftovers',
                   'iv': 28,
                   'level': 44,
                   'moves': ['Psychic', 'Aura Sphere', 'Recover', 'Thunder Wave'],
                   'nature': 'Timid',
                   'species': 'Mew'},
                  {'ability': 'Regenerator',
                   'evs': '252 HP / 108 SpD',
                   'item': 'Leftovers',
                   'iv': 28,
                   'level': 45,
                   'moves': ['Scald', 'Psychic', 'Slack Off', 'Ice Beam'],
                   'nature': 'Calm',
                   'species': 'Slowking'},
                  {'ability': 'Steadfast',
                   'evs': '252 Atk / 108 Spe',
                   'item': 'Life Orb',
                   'iv': 28,
                   'level': 46,
                   'moves': ['Psycho Cut', 'Close Combat', 'Night Slash', 'Swords Dance'],
                   'nature': 'Jolly',
                   'species': 'Gallade'}],
        'trainer': 'TRAINER_QARRO_SABRINA_C',
        'variant': 'C'},
 '7B': {'ace': 'Arcanine',
        'base_trainer': 'TRAINER_LEADER_BLAINE',
        'ev_budget': 420,
        'gym': 7,
        'item_count': 6,
        'iv': 30,
        'leader': 'Блейн',
        'party': [{'ability': 'Drought',
                   'evs': '252 SpA / 168 Spe',
                   'item': 'Heat Rock',
                   'iv': 30,
                   'level': 49,
                   'moves': ['Fire Blast', 'Solarbeam', 'Will-O-Wisp', 'Nasty Plot'],
                   'nature': 'Timid',
                   'species': 'Ninetales'},
                  {'ability': 'Intimidate',
                   'evs': '252 Atk / 168 Spe',
                   'item': 'Life Orb',
                   'iv': 30,
                   'level': 49,
                   'moves': ['Flare Blitz', 'Extreme Speed', 'Wild Charge', 'Crunch'],
                   'nature': 'Adamant',
                   'species': 'Arcanine'},
                  {'ability': 'Flame Body',
                   'evs': '252 HP / 168 Def',
                   'item': 'Leftovers',
                   'iv': 30,
                   'level': 50,
                   'moves': ['Lava Plume', 'Recover', 'Stealth Rock', 'Toxic'],
                   'nature': 'Bold',
                   'species': 'Magcargo'},
                  {'ability': 'Blaze',
                   'evs': '252 SpA / 168 Spe',
                   'item': 'Choice Scarf',
                   'iv': 30,
                   'level': 50,
                   'moves': ['Eruption', 'Fire Blast', 'Focus Blast', 'Hidden Power'],
                   'nature': 'Timid',
                   'species': 'Typhlosion'},
                  {'ability': 'Flash Fire',
                   'evs': '252 SpA / 168 Spe',
                   'item': 'Life Orb',
                   'iv': 30,
                   'level': 51,
                   'moves': ['Nasty Plot', 'Dark Pulse', 'Fire Blast', 'Hidden Power'],
                   'nature': 'Timid',
                   'species': 'Houndoom'},
                  {'ability': 'Flash Fire',
                   'evs': '252 Atk / 168 Spe',
                   'item': 'Life Orb',
                   'iv': 30,
                   'level': 52,
                   'moves': ['Flare Blitz', 'Wild Charge', 'Megahorn', 'Morning Sun'],
                   'nature': 'Jolly',
                   'species': 'Rapidash'}],
        'trainer': 'TRAINER_QARRO_BLAINE_B',
        'variant': 'B'},
 '7C': {'ace': 'Arcanine',
        'base_trainer': 'TRAINER_LEADER_BLAINE',
        'ev_budget': 420,
        'gym': 7,
        'item_count': 6,
        'iv': 30,
        'leader': 'Блейн',
        'party': [{'ability': 'Flash Fire',
                   'evs': '252 Atk / 168 Spe',
                   'item': 'Life Orb',
                   'iv': 30,
                   'level': 49,
                   'moves': ['Flare Blitz', 'Wild Charge', 'Megahorn', 'Morning Sun'],
                   'nature': 'Jolly',
                   'species': 'Rapidash'},
                  {'ability': 'Blaze',
                   'evs': '252 SpA / 168 Spe',
                   'item': 'Life Orb',
                   'iv': 30,
                   'level': 49,
                   'moves': ['Fire Blast', 'Air Slash', 'Focus Blast', 'Roost'],
                   'nature': 'Timid',
                   'species': 'Charizard'},
                  {'ability': 'Intimidate',
                   'evs': '252 Atk / 168 Spe',
                   'item': 'Life Orb',
                   'iv': 30,
                   'level': 50,
                   'moves': ['Flare Blitz', 'Extreme Speed', 'Wild Charge', 'Crunch'],
                   'nature': 'Adamant',
                   'species': 'Arcanine'},
                  {'ability': 'Vital Spirit',
                   'evs': '252 SpA / 168 Spe',
                   'item': 'Eviolite',
                   'iv': 30,
                   'level': 50,
                   'moves': ['Fire Blast', 'Focus Blast', 'Thunderbolt', 'Will-O-Wisp'],
                   'nature': 'Timid',
                   'species': 'Magmar'},
                  {'ability': 'Flash Fire',
                   'evs': '252 SpA / 168 Spe',
                   'item': 'Life Orb',
                   'iv': 30,
                   'level': 51,
                   'moves': ['Nasty Plot', 'Dark Pulse', 'Fire Blast', 'Hidden Power'],
                   'nature': 'Timid',
                   'species': 'Houndoom'},
                  {'ability': 'Drought',
                   'evs': '252 SpA / 168 Spe',
                   'item': 'Heat Rock',
                   'iv': 30,
                   'level': 52,
                   'moves': ['Fire Blast', 'Solarbeam', 'Will-O-Wisp', 'Nasty Plot'],
                   'nature': 'Timid',
                   'species': 'Ninetales'}],
        'trainer': 'TRAINER_QARRO_BLAINE_C',
        'variant': 'C'},
 '8B': {'ace': 'Nidoking',
        'base_trainer': 'TRAINER_LEADER_GIOVANNI',
        'ev_budget': 510,
        'gym': 8,
        'item_count': 6,
        'iv': 31,
        'leader': 'Джованни',
        'party': [{'ability': 'Lightning Rod',
                   'evs': '252 HP / 252 Atk / 6 SpD',
                   'item': 'Eviolite',
                   'iv': 31,
                   'level': 55,
                   'moves': ['Earthquake', 'Rock Slide', 'Megahorn', 'Thunder Punch'],
                   'nature': 'Adamant',
                   'species': 'Rhydon'},
                  {'ability': 'Sheer Force',
                   'evs': '252 HP / 252 SpA / 6 Def',
                   'item': 'Life Orb',
                   'iv': 31,
                   'level': 55,
                   'moves': ['Earth Power', 'Sludge Wave', 'Ice Beam', 'Stealth Rock'],
                   'nature': 'Modest',
                   'species': 'Nidoqueen'},
                  {'ability': 'Rock Head',
                   'evs': '252 HP / 252 Atk / 6 SpD',
                   'item': 'Thick Club',
                   'iv': 31,
                   'level': 56,
                   'moves': ['Earthquake', 'Stone Edge', 'Double-Edge', 'Fire Punch'],
                   'nature': 'Adamant',
                   'species': 'Marowak'},
                  {'ability': 'Sand Veil',
                   'evs': '252 HP / 252 Atk / 6 SpD',
                   'item': 'Leftovers',
                   'iv': 31,
                   'level': 56,
                   'moves': ['Earthquake', 'Stone Edge', 'Rapid Spin', 'Swords Dance'],
                   'nature': 'Adamant',
                   'species': 'Sandslash'},
                  {'ability': 'Sheer Force',
                   'evs': '252 SpA / 252 Spe / 6 HP',
                   'item': 'Life Orb',
                   'iv': 31,
                   'level': 57,
                   'moves': ['Earth Power', 'Sludge Wave', 'Ice Beam', 'Thunderbolt'],
                   'nature': 'Modest',
                   'species': 'Nidoking'},
                  {'ability': 'Sand Stream',
                   'evs': '252 HP / 252 Def / 6 SpD',
                   'item': 'Leftovers',
                   'iv': 31,
                   'level': 58,
                   'moves': ['Earthquake', 'Stone Edge', 'Slack Off', 'Stealth Rock'],
                   'nature': 'Impish',
                   'species': 'Hippowdon'}],
        'trainer': 'TRAINER_QARRO_GIOVANNI_B',
        'variant': 'B'},
 '8C': {'ace': 'Nidoking',
        'base_trainer': 'TRAINER_LEADER_GIOVANNI',
        'ev_budget': 510,
        'gym': 8,
        'item_count': 6,
        'iv': 31,
        'leader': 'Джованни',
        'party': [{'ability': 'Arena Trap',
                   'evs': '252 Atk / 252 Spe / 6 HP',
                   'item': 'Focus Sash',
                   'iv': 31,
                   'level': 55,
                   'moves': ['Earthquake', 'Stone Edge', 'Sucker Punch', 'Stealth Rock'],
                   'nature': 'Jolly',
                   'species': 'Dugtrio'},
                  {'ability': 'Sturdy',
                   'evs': '252 HP / 252 Atk / 6 SpD',
                   'item': 'Leftovers',
                   'iv': 31,
                   'level': 55,
                   'moves': ['Earthquake', 'Ice Shard', 'Rapid Spin', 'Stealth Rock'],
                   'nature': 'Adamant',
                   'species': 'Donphan'},
                  {'ability': 'Sheer Force',
                   'evs': '252 HP / 252 SpA / 6 Def',
                   'item': 'Life Orb',
                   'iv': 31,
                   'level': 56,
                   'moves': ['Earth Power', 'Sludge Wave', 'Ice Beam', 'Stealth Rock'],
                   'nature': 'Modest',
                   'species': 'Nidoqueen'},
                  {'ability': 'Lightning Rod',
                   'evs': '252 HP / 252 Atk / 6 SpD',
                   'item': 'Eviolite',
                   'iv': 31,
                   'level': 56,
                   'moves': ['Earthquake', 'Rock Slide', 'Megahorn', 'Thunder Punch'],
                   'nature': 'Adamant',
                   'species': 'Rhydon'},
                  {'ability': 'Unaware',
                   'evs': '252 HP / 252 Def / 6 SpD',
                   'item': 'Leftovers',
                   'iv': 31,
                   'level': 57,
                   'moves': ['Scald', 'Earthquake', 'Recover', 'Toxic'],
                   'nature': 'Impish',
                   'species': 'Quagsire'},
                  {'ability': 'Sheer Force',
                   'evs': '252 SpA / 252 Spe / 6 HP',
                   'item': 'Life Orb',
                   'iv': 31,
                   'level': 58,
                   'moves': ['Earth Power', 'Sludge Wave', 'Ice Beam', 'Thunderbolt'],
                   'nature': 'Modest',
                   'species': 'Nidoking'}],
        'trainer': 'TRAINER_QARRO_GIOVANNI_C',
        'variant': 'C'}}

TRAINER_ID_ORDER = [
    "TRAINER_QARRO_BROCK_B", "TRAINER_QARRO_BROCK_C",
    "TRAINER_QARRO_MISTY_B", "TRAINER_QARRO_MISTY_C",
    "TRAINER_QARRO_LT_SURGE_B", "TRAINER_QARRO_LT_SURGE_C",
    "TRAINER_QARRO_ERIKA_B", "TRAINER_QARRO_ERIKA_C",
    "TRAINER_QARRO_KOGA_B", "TRAINER_QARRO_KOGA_C",
    "TRAINER_QARRO_SABRINA_B", "TRAINER_QARRO_SABRINA_C",
    "TRAINER_QARRO_BLAINE_B", "TRAINER_QARRO_BLAINE_C",
    "TRAINER_QARRO_GIOVANNI_B", "TRAINER_QARRO_GIOVANNI_C",
]

ORIGINAL_CREATE_PARTY = """static void CreateNPCTrainerParty(struct Pokemon *party, u16 trainerNum)
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
"""

SELECTOR_CREATE_PARTY = r"""// QARRO_KANTO_GYM_ABC_V3_132_BEGIN
#define QARRO_KANTO_GYM_VARIANT_BITS_VAR 0x40BD
#define QARRO_KANTO_GYM_VARIANT_INIT_VAR 0x40BE

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
    u16 initialized = VarGet(QARRO_KANTO_GYM_VARIANT_INIT_VAR);
    u16 packed = VarGet(QARRO_KANTO_GYM_VARIANT_BITS_VAR);
    u16 initBit = 1u << gymIndex;
    u8 shift = gymIndex * 2u;
    u8 variant;

    if (!(initialized & initBit))
    {
        variant = DeriveQarroKantoGymVariantV3132(gymIndex);
        packed &= ~(3u << shift);
        packed |= (u16)variant << shift;
        initialized |= initBit;
        VarSet(QARRO_KANTO_GYM_VARIANT_BITS_VAR, packed);
        VarSet(QARRO_KANTO_GYM_VARIANT_INIT_VAR, initialized);
        return variant;
    }

    variant = (packed >> shift) & 3u;
    if (variant > 2u)
    {
        // Self-heal a corrupt/legacy 2-bit value without giving a reset reroll.
        variant = DeriveQarroKantoGymVariantV3132(gymIndex);
        packed &= ~(3u << shift);
        packed |= (u16)variant << shift;
        VarSet(QARRO_KANTO_GYM_VARIANT_BITS_VAR, packed);
    }
    return variant;
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


def read(path: Path) -> str:
    if not path.is_file():
        die(f"missing {path}")
    return path.read_text(encoding="utf-8")


def trainer_block(text: str, trainer: str) -> str:
    token = f"=== {trainer} ==="
    start = text.find(token)
    if start < 0:
        die(f"trainer block missing: {trainer}")
    next_start = text.find("\n=== ", start + len(token))
    end = len(text) if next_start < 0 else next_start
    return text[start:end]


def species_lines(block: str) -> list[str]:
    return re.findall(r"(?m)^([^\n]+?)(?: @ [^\n]+)?\nLevel:\s*\d+\s*$", block)


def validate_free_save_vars(root: Path) -> None:
    vars_header = (root / "include/constants/vars_frlg.h").resolve()
    hits = []
    for base in (root / "src", root / "data", root / "include"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".c", ".h", ".inc", ".s", ".txt"}:
                continue
            if path.resolve() == vars_header:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if any(n in text for n in ("VAR_0x40BD", "VAR_0x40BE", "0x40BD", "0x40BE")):
                hits.append(str(path.relative_to(root)))
                if len(hits) >= 10:
                    break
        if hits:
            break
    if hits:
        die(f"save vars 0x40BD/0x40BE are no longer free; references={hits}")


def patch_opponents(path: Path) -> None:
    text = read(path)
    if MARKER in text or "TRAINER_QARRO_BROCK_B" in text:
        die("v3.132 trainer constants already present; refusing duplicate installation")

    if not re.search(r"(?m)^#define\s+TRAINER_CUE_BALL_PAXTON\s+623\s*$", text):
        die("expected final vanilla trainer id 623 not found")
    count_match = re.search(r"(?m)^#define\s+TRAINERS_COUNT_FRLG\s+(\d+)\s*$", text)
    if not count_match or int(count_match.group(1)) != EXPECTED_TRAINERS_COUNT:
        die(f"expected TRAINERS_COUNT_FRLG={EXPECTED_TRAINERS_COUNT}, got {count_match.group(1) if count_match else 'missing'}")
    if not re.search(r"(?m)^#define\s+MAX_TRAINERS_COUNT_FRLG\s+768\s*$", text):
        die("MAX_TRAINERS_COUNT_FRLG drifted; refusing to consume trainer flag space")

    define_lines = [f"#define {name:<48} {FIRST_NEW_TRAINER_ID + i}" for i, name in enumerate(TRAINER_ID_ORDER)]
    insertion = "\n// QARRO_KANTO_GYM_ABC_V3_132 trainer-only B/C party records\n" + "\n".join(define_lines) + "\n"
    anchor = "#define TRAINER_CUE_BALL_PAXTON                    623\n"
    if anchor not in text:
        die("exact trainer 623 insertion anchor drifted")
    text = text.replace(anchor, anchor + insertion, 1)
    text, n = re.subn(
        r"(?m)^#define\s+TRAINERS_COUNT_FRLG\s+624\s*$",
        "#define TRAINERS_COUNT_FRLG                      640",
        text,
        count=1,
    )
    if n != 1:
        die("failed to raise TRAINERS_COUNT_FRLG to 640")
    path.write_text(text, encoding="utf-8")


def mon_text(mon: dict) -> str:
    first = mon["species"] if not mon["item"] else f'{mon["species"]} @ {mon["item"]}'
    lines = [
        first,
        f'Level: {mon["level"]}',
        f'IVs: {mon["iv"]} HP / {mon["iv"]} Atk / {mon["iv"]} Def / {mon["iv"]} SpA / {mon["iv"]} SpD / {mon["iv"]} Spe',
    ]
    if mon["evs"]:
        lines.append(f'EVs: {mon["evs"]}')
    lines += [f'{mon["nature"]} Nature', f'Ability: {mon["ability"]}']
    lines += [f"- {move}" for move in mon["moves"]]
    return "\n".join(lines)


def patch_parties(path: Path) -> list[dict]:
    text = read(path)
    if any(f"=== {name} ===" in text for name in TRAINER_ID_ORDER):
        die("v3.132 B/C party blocks already exist; refusing duplicate installation")

    # The pass is only valid on top of the green final-canon Variant-A baseline.
    for trainer, expected in EXPECTED_A.items():
        actual = species_lines(trainer_block(text, trainer))
        if actual != expected:
            die(f"{trainer} Variant A drifted: expected {expected}, got {actual}")

    report = []
    chunks = []
    for key in sorted(VARIANTS, key=lambda x: (int(x[:-1]), x[-1])):
        cfg = VARIANTS[key]
        header = HEADERS[cfg["base_trainer"]]
        party = cfg["party"]
        if len(party) != 6 or len({m["species"] for m in party}) != 6:
            die(f'{cfg["trainer"]} must contain six unique Pokemon')
        if cfg["ace"] not in {m["species"] for m in party}:
            die(f'{cfg["trainer"]} missing guaranteed Ace {cfg["ace"]}')
        held = sum(bool(m["item"]) for m in party)
        if held != cfg["item_count"]:
            die(f'{cfg["trainer"]} item budget mismatch: expected {cfg["item_count"]}, got {held}')
        for mon in party:
            ev_sum = 0
            if mon["evs"]:
                ev_sum = sum(int(v) for v in re.findall(r"(\d+)\s+(?:HP|Atk|Def|SpA|SpD|Spe)", mon["evs"]))
            if ev_sum != cfg["ev_budget"]:
                die(f'{cfg["trainer"]} {mon["species"]} EV budget {ev_sum} != {cfg["ev_budget"]}')

        chunks.append(
            f'=== {cfg["trainer"]} ===\n{header}\n\n'
            + "\n\n".join(mon_text(mon) for mon in party)
            + "\n"
        )
        report.append({
            "trainer": cfg["trainer"],
            "baseTrainer": cfg["base_trainer"],
            "variant": cfg["variant"],
            "partySize": 6,
            "species": [m["species"] for m in party],
            "levels": [m["level"] for m in party],
            "ace": cfg["ace"],
            "baseIV": cfg["iv"],
            "evBudgetPerPokemon": cfg["ev_budget"],
            "meaningfulHeldItems": held,
        })

    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + "\n".join(chunks)
    path.write_text(text, encoding="utf-8")

    verify = read(path)
    for row in report:
        actual = species_lines(trainer_block(verify, row["trainer"]))
        if actual != row["species"]:
            die(f'{row["trainer"]} post-write party verification failed: {actual}')
    return report


def patch_battle_setup(path: Path) -> None:
    text = read(path)
    if MARKER in text:
        die("v3.132 runtime selector already present; refusing duplicate installation")
    if ORIGINAL_CREATE_PARTY not in text:
        die("native CreateNPCTrainerParty shape drifted after v3.88; refusing broad replacement")
    text = text.replace(ORIGINAL_CREATE_PARTY, SELECTOR_CREATE_PARTY, 1)
    if text.count("QARRO_KANTO_GYM_ABC_V3_132_BEGIN") != 1:
        die("selector installation marker verification failed")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    party_path = root / "src/data/trainers_frlg.party"
    opponents_path = root / "include/constants/opponents_frlg.h"
    battle_setup = root / "src/battle_setup.c"
    for path in (party_path, opponents_path, battle_setup):
        if not path.is_file():
            die(f"required source missing: {path}")

    validate_free_save_vars(root)
    patch_opponents(opponents_path)
    variants = patch_parties(party_path)
    patch_battle_setup(battle_setup)

    # Strong postconditions: scope is exactly 8 A IDs + 16 party-only B/C IDs.
    opponents = read(opponents_path)
    if not re.search(r"(?m)^#define\s+TRAINERS_COUNT_FRLG\s+640\s*$", opponents):
        die("post-write trainer count is not 640")
    for i, name in enumerate(TRAINER_ID_ORDER):
        wanted = FIRST_NEW_TRAINER_ID + i
        if not re.search(rf"(?m)^#define\s+{re.escape(name)}\s+{wanted}\s*$", opponents):
            die(f"missing exact trainer id {name}={wanted}")

    audit = {
        "marker": MARKER,
        "battleMode": "Kanto story Gym 6v6 A/B/C",
        "storyLeaderCount": 8,
        "newPartyOnlyTrainerRecords": 16,
        "newTrainerIdRange": [FIRST_NEW_TRAINER_ID, LAST_NEW_TRAINER_ID],
        "trainersCountBefore": EXPECTED_TRAINERS_COUNT,
        "trainersCountAfter": NEW_TRAINERS_COUNT,
        "selector": {
            "variantBitsVar": VARIANT_BITS_VAR,
            "initializedMaskVar": VARIANT_INIT_VAR,
            "selection": "save-OTID-derived A/B/C on first story-Leader party creation",
            "persistence": "explicit packed save vars; deterministic OTID fallback prevents reset reroll before next save",
            "variantEncoding": {"A": 0, "B": 1, "C": 2},
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
        f"[{MARKER}] PASS: 8 Kanto story Leaders now have save-fixed A/B/C 6v6 parties; "
        f"16 B/C records installed at IDs 624-639; 0x40BD/0x40BE persistence; "
        f"rematches/E4/Champion/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
