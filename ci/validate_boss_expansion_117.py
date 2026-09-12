#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import re
import sys
import zlib
from collections import defaultdict
from pathlib import Path

PINNED = "e8bd1cd7b03fc032ea37e3ecd38b379b5d01a1e7"
EXPECTED_BUILDS = 342
GEN5_GAMES = {"rb", "rby", "r", "b", "y", "gs", "c", "rs", "e", "frlg", "dp", "pt", "hgss", "bw", "b2w2"}
CAMPAIGN_FORBIDDEN = {
    "Articuno","Zapdos","Moltres","Mewtwo","Mew","Raikou","Entei","Suicune","Lugia","Ho-Oh","Celebi",
    "Regirock","Regice","Registeel","Latias","Latios","Kyogre","Groudon","Rayquaza","Jirachi","Deoxys",
    "Uxie","Mesprit","Azelf","Dialga","Palkia","Heatran","Regigigas","Giratina","Cresselia","Phione","Manaphy",
    "Darkrai","Shaymin","Arceus","Victini","Cobalion","Terrakion","Virizion","Tornadus","Thundurus",
    "Reshiram","Zekrom","Landorus","Kyurem","Keldeo","Meloetta","Genesect",
}


def die(msg: str) -> None:
    raise SystemExit(f"[QARRO_BOSS_117] ERROR: {msg}")


def load_manifest(path: Path) -> dict:
    raw = base64.b64decode(path.read_text(encoding="ascii"))
    obj = json.loads(zlib.decompress(raw).decode("utf-8"))
    if obj.get("pinned_commit") != PINNED:
        die(f"manifest pin drift: {obj.get('pinned_commit')}")
    builds = obj.get("builds", [])
    if len(builds) != EXPECTED_BUILDS or obj.get("build_count") != EXPECTED_BUILDS:
        die(f"expected {EXPECTED_BUILDS} builds, got {len(builds)} / declared {obj.get('build_count')}")
    return obj


def parse_spread(text: str, kind: str) -> tuple[dict[str,int], int]:
    if kind == "ivs" and text.strip().lower() == "31 all":
        vals = {k:31 for k in ("HP","Atk","Def","SpA","SpD","Spe")}
        return vals, 186
    vals: dict[str,int] = {}
    for amount, stat in re.findall(r"(\d+)\s+(HP|Atk|Def|SpA|SpD|Spe)", text):
        vals[stat] = int(amount)
    if not vals:
        die(f"cannot parse {kind}: {text!r}")
    return vals, sum(vals.values())


def structural_audit(builds: list[dict]) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    for i,b in enumerate(builds, start=1):
        ident = f"#{i} {b['layer']}/{b['trainer']}/{b['species']}"
        if not (1 <= int(b['level']) <= 100): errors.append(f"{ident}: level {b['level']}")
        if len(b.get("moves", [])) != 4 or any(not m for m in b["moves"]): errors.append(f"{ident}: must have exactly 4 moves")
        ivs, _ = parse_spread(str(b["ivs"]), "ivs")
        if any(v < 0 or v > 31 for v in ivs.values()): errors.append(f"{ident}: IV out of range: {ivs}")
        evs, total = parse_spread(str(b["evs"]), "evs")
        if any(v < 0 or v > 252 for v in evs.values()): errors.append(f"{ident}: EV out of range: {evs}")
        if total > 510: errors.append(f"{ident}: EV total {total} > 510")
        if b["layer"] in ("E4", "Champion") and b["species"] in CAMPAIGN_FORBIDDEN:
            errors.append(f"{ident}: campaign Legendary/Mythical forbidden")
        if any(x in str(b) for x in ("Ash Bond", "Ash Cap", "ITEM_ASH_CAP")):
            errors.append(f"{ident}: protected Ash feature leaked into manifest")
    if errors:
        die("structural audit failed:\n" + "\n".join(errors[:100]))
    return {"errors": errors, "warnings": warnings}


def party_chunk(b: dict) -> str:
    ivs, _ = parse_spread(str(b["ivs"]), "ivs")
    ivline = " / ".join(f"{ivs.get(k,0)} {k}" for k in ("HP","Atk","Def","SpA","SpD","Spe"))
    lines = [
        f"{b['species']} @ {b['item']}",
        f"Level: {int(b['level'])}",
        f"IVs: {ivline}",
        f"EVs: {b['evs']}",
        f"{b['nature']} Nature",
        f"Ability: {b['ability']}",
    ]
    if b.get("ace"):
        lines.append("Tags: Ace")
    lines.extend(f"- {m}" for m in b["moves"])
    return "\n".join(lines)


def write_synthetic_party(builds: list[dict], out: Path) -> None:
    ids = ["TRAINER_YOUNGSTER_BEN", "TRAINER_LEADER_BROCK", "TRAINER_CUE_BALL_PAXTON"]
    n = len(builds)
    cuts = [0, n//3, (2*n)//3, n]
    blocks = []
    for k, tid in enumerate(ids):
        header = [
            f"=== {tid} ===",
            f"Name: QA{k+1}",
            "Class: Youngster Frlg",
            "Pic: Youngster Frlg",
            "Gender: Male",
            "Music: Male",
            "Double Battle: No",
            "AI: Check Bad Move",
            "",
        ]
        mons = [party_chunk(b) for b in builds[cuts[k]:cuts[k+1]]]
        blocks.append("\n".join(header) + "\n\n".join(mons))
    out.write_text("\n\n".join(blocks).rstrip() + "\n", encoding="utf-8")


def combined_gen5_learnables(upstream: Path) -> dict[str,set[str]]:
    root = upstream / "tools/learnset_helpers/porymoves_files"
    if not root.is_dir(): die(f"missing {root}")
    learn: dict[str,set[str]] = defaultdict(set)
    used = []
    for p in sorted(root.glob("*.json")):
        if p.stem.lower() not in GEN5_GAMES:
            continue
        used.append(p.name)
        data = json.loads(p.read_text(encoding="utf-8"))
        for species, by_method in data.items():
            for rec in by_method.get("LevelMoves", []):
                mv = rec.get("Move")
                if mv: learn[species].add(mv)
            for key in ("TMMoves", "EggMoves", "TutorMoves"):
                for mv in by_method.get(key, []):
                    if mv: learn[species].add(mv)
    if "b2w2.json" not in used:
        die(f"B2W2 learnset source not selected; selected={used}")
    print(f"[QARRO_BOSS_117] learnset sources <=Gen5: {', '.join(used)}")
    return learn


def move_legality_audit(builds: list[dict], upstream: Path) -> list[dict]:
    learn = combined_gen5_learnables(upstream)
    issues = []
    for i,b in enumerate(builds, start=1):
        species = b["species"]
        available = learn.get(species)
        if available is None:
            issues.append({"index":i,"trainer":b["trainer"],"species":species,"move":"*","reason":"species absent from <=Gen5 porymoves inputs"})
            continue
        for mv in b["moves"]:
            if mv not in available:
                issues.append({"index":i,"trainer":b["trainer"],"species":species,"move":mv,"reason":"not learnable in selected Gen I-V game sources"})
    return issues


def constantize(prefix: str, human: str) -> str:
    out = []
    for c in human:
        if c.isalnum(): out.append(c.upper())
        elif c == "'": continue
        else: out.append("_")
    return prefix + "_" + "".join(out)


def species_constant_candidates(name: str) -> list[str]:
    base = constantize("SPECIES", name)
    return list(dict.fromkeys([
        base,
        base.replace("__", "_"),
        base.replace("MR._MIME", "MR_MIME"),
        base.replace("MIME_JR.", "MIME_JR"),
        base.replace("FARFETCH_D", "FARFETCHD"),
        base.replace("NIDORAN_F", "NIDORAN_F"),
        base.replace("NIDORAN_M", "NIDORAN_M"),
        base.replace("ROTOM_WASH", "ROTOM_WASH"),
    ]))


def parse_species_ability_blocks(upstream: Path) -> dict[str,set[str]]:
    roots = [upstream / "src/data/pokemon/species_info", upstream / "src/data/pokemon/species_info.h"]
    files = []
    for root in roots:
        if root.is_dir(): files.extend(root.rglob("*.h"))
        elif root.is_file(): files.append(root)
    if not files: die("species_info files not found")
    text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
    blocks: dict[str,set[str]] = {}
    starts = list(re.finditer(r"\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*\{", text))
    for j,m in enumerate(starts):
        end = starts[j+1].start() if j+1 < len(starts) else min(len(text), m.start()+12000)
        block = text[m.start():end]
        am = re.search(r"\.abilities\s*=\s*\{([^}]*)\}", block, re.S)
        if am:
            blocks[m.group(1)] = set(re.findall(r"ABILITY_[A-Z0-9_]+", am.group(1)))
    return blocks


def ability_legality_audit(builds: list[dict], upstream: Path) -> list[dict]:
    blocks = parse_species_ability_blocks(upstream)
    issues = []
    for i,b in enumerate(builds, start=1):
        sc = None
        for cand in species_constant_candidates(b["species"]):
            if cand in blocks:
                sc = cand; break
        if sc is None:
            issues.append({"index":i,"trainer":b["trainer"],"species":b["species"],"ability":b["ability"],"reason":"species_info block not resolved"})
            continue
        ac = constantize("ABILITY", b["ability"]).replace("__","_")
        if ac not in blocks[sc]:
            issues.append({"index":i,"trainer":b["trainer"],"species":b["species"],"ability":b["ability"],"reason":f"{ac} not in {sorted(blocks[sc])}"})
    return issues


def main() -> int:
    if len(sys.argv) != 4:
        print(f"usage: {Path(sys.argv[0]).name} <manifest.zlib.b64> <upstream> <outdir>", file=sys.stderr)
        return 2
    manifest_path, upstream, outdir = map(Path, sys.argv[1:])
    upstream = upstream.resolve(); outdir.mkdir(parents=True, exist_ok=True)
    obj = load_manifest(manifest_path)
    builds = obj["builds"]
    structural = structural_audit(builds)
    party = outdir / "qarro_boss_342.party"
    write_synthetic_party(builds, party)
    move_issues = move_legality_audit(builds, upstream)
    ability_issues = ability_legality_audit(builds, upstream)
    report = {
        "pinned": PINNED,
        "builds": len(builds),
        "structural": structural,
        "move_issue_count": len(move_issues),
        "move_issues": move_issues,
        "ability_issue_count": len(ability_issues),
        "ability_issues": ability_issues,
        "synthetic_party": str(party),
    }
    (outdir / "qarro_boss_117_precompile_audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(f"[QARRO_BOSS_117] builds={len(builds)} move_issues={len(move_issues)} ability_issues={len(ability_issues)}")
    if move_issues:
        print("[QARRO_BOSS_117] first move issues:")
        for x in move_issues[:80]: print(json.dumps(x, ensure_ascii=False))
    if ability_issues:
        print("[QARRO_BOSS_117] first ability issues:")
        for x in ability_issues[:80]: print(json.dumps(x, ensure_ascii=False))
    return 1 if (move_issues or ability_issues) else 0

if __name__ == "__main__":
    raise SystemExit(main())
