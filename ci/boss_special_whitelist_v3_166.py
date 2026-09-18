#!/usr/bin/env python3
"""Qarro v3.166: apply the approved Gen I-V special-Pokemon whitelist to boss teams."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_BOSS_SPECIAL_WHITELIST_V3_166"
ALLOWED_LEGENDARY = {"Articuno", "Zapdos", "Moltres", "Entei"}
ALLOWED_MYTHICAL = {"Mew", "Celebi", "Jirachi", "Phione", "Shaymin", "Keldeo"}
ALLOWED = ALLOWED_LEGENDARY | ALLOWED_MYTHICAL
ALL_SPECIAL = {
    "Articuno","Zapdos","Moltres","Mewtwo","Mew","Raikou","Entei","Suicune","Lugia","Ho-Oh","Celebi",
    "Regirock","Regice","Registeel","Latias","Latios","Kyogre","Groudon","Rayquaza","Jirachi","Deoxys",
    "Uxie","Mesprit","Azelf","Dialga","Palkia","Heatran","Regigigas","Giratina","Cresselia","Phione","Manaphy","Darkrai","Shaymin","Arceus",
    "Victini","Cobalion","Terrakion","Virizion","Tornadus","Thundurus","Reshiram","Zekrom","Landorus","Kyurem","Keldeo","Meloetta","Genesect",
}
FORBIDDEN = ALL_SPECIAL - ALLOWED

TOBIAS = "TRAINER_QARRO_POSTGAME_02_TOBIAS_FIXED"
BRANDON = "TRAINER_QARRO_POSTGAME_12_BRANDON_POOL"
TOBIAS_BEFORE = ["Darkrai","Latias","Latios","Entei","Zapdos","Lugia"]
TOBIAS_AFTER = ["Mew","Jirachi","Shaymin","Entei","Zapdos","Keldeo"]
BRANDON_BEFORE = ["Regirock","Regice","Registeel","Dusclops","Ninjask","Solrock","Claydol","Metagross","Aerodactyl","Tyranitar"]
BRANDON_AFTER = ["Articuno","Zapdos","Moltres","Dusclops","Ninjask","Solrock","Claydol","Metagross","Aerodactyl","Tyranitar"]

BUILDS = {
"Darkrai": """Mew @ Focus Sash\nLevel: 100\nIVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe\nEVs: 252 SpA / 4 SpD / 252 Spe\nTimid Nature\nAbility: Synchronize\n- Psychic\n- Aura Sphere\n- Taunt\n- Nasty Plot""",
"Latias": """Jirachi @ Leftovers\nLevel: 100\nIVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe\nEVs: 252 HP / 80 Def / 176 SpD\nCareful Nature\nAbility: Serene Grace\n- Iron Head\n- Wish\n- Thunder Wave\n- U-turn""",
"Latios": """Shaymin @ Life Orb\nLevel: 100\nIVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe\nEVs: 252 SpA / 4 SpD / 252 Spe\nTimid Nature\nAbility: Natural Cure\n- Seed Flare\n- Earth Power\n- Psychic\n- Synthesis""",
"Lugia": """Keldeo @ Life Orb\nLevel: 100\nIVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe\nEVs: 252 SpA / 4 SpD / 252 Spe\nTimid Nature\nAbility: Justified\n- Hydro Pump\n- Secret Sword\n- Icy Wind\n- Calm Mind""",
"Regirock": """Articuno @ Leftovers\nLevel: 100\nIVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe\nEVs: 252 HP / 176 Def / 80 SpD\nBold Nature\nAbility: Pressure\nTags: Ace\n- Ice Beam\n- Roost\n- Toxic\n- Haze""",
"Regice": """Zapdos @ Expert Belt\nLevel: 100\nIVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe\nEVs: 252 SpA / 4 SpD / 252 Spe\nTimid Nature\nAbility: Pressure\n- Thunderbolt\n- Heat Wave\n- Roost\n- Volt Switch""",
"Registeel": """Moltres @ Life Orb\nLevel: 100\nIVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe\nEVs: 252 SpA / 4 SpD / 252 Spe\nTimid Nature\nAbility: Pressure\n- Fire Blast\n- Air Slash\n- Roost\n- U-turn""",
}

def die(msg): raise SystemExit(f"[{MARKER}] ERROR: {msg}")
def block_bounds(text, trainer):
    token=f"=== {trainer} ==="; s=text.find(token)
    if s < 0 or text.find(token, s+1) >= 0: die(f"bad trainer anchor: {trainer}")
    e=text.find("\n=== TRAINER_", s+len(token)); e=len(text) if e<0 else e
    return s,e,text[s:e]
def seq(block): return [x.split(" @ ",1)[0].strip() for x in block.splitlines() if " @ " in x]
def replace_mon(block, old, new):
    m=list(re.finditer(rf"(?m)^{re.escape(old)}(?: @ [^\n]+)?$", block))
    if len(m)!=1: die(f"{old}: expected one build, got {len(m)}")
    s=m[0].start(); e=block.find("\n\n", m[0].end()); e=len(block) if e<0 else e
    return block[:s]+new.rstrip()+block[e:]
def patch(text, trainer, before, after, olds):
    s,e,b=block_bounds(text, trainer); cur=seq(b)
    if cur==after: return text
    if cur!=before: die(f"{trainer}: drift {cur}")
    for old in olds: b=replace_mon(b, old, BUILDS[old])
    if seq(b)!=after: die(f"{trainer}: post-patch mismatch {seq(b)}")
    return text[:s]+b+text[e:]
def specials(block):
    return sorted(x for x in ALL_SPECIAL if re.search(rf"(?m)^{re.escape(x)}(?: @ [^\n]+)?$", block))

def main():
    if len(sys.argv)!=2: return 2
    root=Path(sys.argv[1]).resolve(); p=root/"src/data/trainers_frlg.party"
    text=p.read_text(encoding="utf-8"); before=text
    text=patch(text,TOBIAS,TOBIAS_BEFORE,TOBIAS_AFTER,("Darkrai","Latias","Latios","Lugia"))
    text=patch(text,BRANDON,BRANDON_BEFORE,BRANDON_AFTER,("Regirock","Regice","Registeel"))

    # This pass runs before the final Kanto A/B/C installer in some CI paths.
    # Final Gym policy is enforced by the dedicated same-commit Kanto regression.

    postgame=sorted(set(re.findall(r"(?m)^=== (TRAINER_QARRO_POSTGAME_[A-Z0-9_]+) ===$",text)))
    if len(postgame)!=20: die(f"postgame block count={len(postgame)}")
    bad={}
    for tr in postgame:
        _,_,b=block_bounds(text,tr); hit=[x for x in specials(b) if x in FORBIDDEN]
        if hit: bad[tr]=hit
    if bad: die(f"unavailable special Pokemon survived: {bad}")

    if text!=before: p.write_text(text,encoding="utf-8")
    audit={"marker":MARKER,"allowedLegendary":sorted(ALLOWED_LEGENDARY),"allowedMythical":sorted(ALLOWED_MYTHICAL),
           "tobias":TOBIAS_AFTER,"brandon":BRANDON_AFTER,"postgameBlocks":len(postgame),"forbiddenAfter":0,
           "mapsTouched":False,"progressionTouched":False,"ashBondTouched":False,"ashCapTouched":False}
    out=root/"build/qarro_boss_special_whitelist_v3_166_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: whitelist enforced; Tobias/Brandon rebuilt; forbidden special Pokemon=0; Ash untouched")
    return 0
if __name__=="__main__": raise SystemExit(main())
