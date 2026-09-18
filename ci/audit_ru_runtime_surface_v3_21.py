#!/usr/bin/env python3
"""Qarro RU localization audit: FireRed map runtime + broader user-facing surface.

Read-only. Keeps the historical map-runtime fields for continuity, but excludes
four verified non-dialogue/canonical entries (3 dynamic STR_VAR buffers + Mew
cry/name) from untranslated-dialogue totals. Also inventories English-only text
outside maps: FRLG/common data text, scripts, core UI/system C strings, and
item/ability/move/Pokedex description data. Pokemon/Move/Ability proper names
are classified separately and are not translation defects by project canon.
"""
from __future__ import annotations
import ast, json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_RUNTIME_SURFACE_V3_21"
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
ASCII_ALPHA_RE = re.compile(r"[A-Za-z]")
LABEL_RE = re.compile(r"^([A-Za-z0-9_]+)::\s*$")
STRING_RE = re.compile(r'^\s*\.string\s+"(.*)"\s*$')
C_MACRO_RE = re.compile(r'(?P<macro>COMPOUND_STRING|_)\s*\(\s*(?P<body>(?:"(?:\\.|[^"\\])*"\s*)+)\)', re.S)
C_QUOTED_RE = re.compile(r'"(?:\\.|[^"\\])*"')

KNOWN_MAP_NON_DIALOGUE = {
    "SevenIsland_House_Room1_Text_StrVar1_1": "dynamic STR_VAR_1 buffer",
    "SevenIsland_House_Room1_Text_StrVar1_2": "dynamic STR_VAR_1 buffer",
    "SevenIsland_House_Room1_Text_StrVar1_3": "dynamic STR_VAR_1 buffer",
    "CeruleanCave_B1F_Text_Mew": "canonical Mew cry/name",
}

COMMON_TEXT = {
    "move_relearner.inc", "pc.inc",
    "pc_transfer.inc", "pkmn_center_nurse.inc", "pokedex_rating.inc",
    "save.inc", "trainers.inc",
}
COMMON_SCRIPTS = {
    "aide.inc", "day_care.inc", "field_move_scripts.inc", "route23.inc",
    "safari_zone.inc",
}
CORE_C = {
    "strings.c", "battle_message.c", "battle_interface.c", "item_menu.c",
    "item_use.c", "party_menu.c", "pokemon_summary_screen.c", "pokedex.c",
    "pokedex_area_screen.c", "main_menu.c", "start_menu.c", "option_menu.c",
    "shop.c", "pokemon_storage_system.c", "hall_of_fame_frlg.c",
    "credits_frlg.c", "starter_choose.c", "trade.c", "daycare.c",
    "move_relearner.c", "egg_hatch.c", "mail.c", "overworld.c",
}
DATA_HEADERS = {
    "src/data/items.h", "src/data/abilities.h", "src/data/moves_info.h",
    "src/data/pokemon/species_info/shared_dex_text.h",
}

def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")

def visible_text(raw: str) -> str:
    s = raw
    s = re.sub(r"\{[^{}]*\}", " ", s)
    for token in ("\\n", "\\p", "\\l", "\\c", "\\v", "\\x"):
        s = s.replace(token, " ")
    s = re.sub(r"\\[A-Za-z0-9_]+", " ", s)
    s = s.replace("$", " ")
    return re.sub(r"\s+", " ", s).strip()

def english_only(s: str) -> bool:
    v = visible_text(s)
    return bool(ASCII_ALPHA_RE.search(v)) and not CYRILLIC_RE.search(v)

def scan_map_file(path: Path, root: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    out, excluded = [], []
    current_label = None; current_start = 0; chunks = []
    def flush():
        nonlocal chunks
        if current_label is None or not chunks:
            chunks=[]; return
        joined = visible_text(" ".join(chunks))
        if ASCII_ALPHA_RE.search(joined) and not CYRILLIC_RE.search(joined) and ("_Text_" in current_label or current_label.endswith("_Text")):
            item={"file":path.relative_to(root).as_posix(),"label":current_label,"line":current_start,"preview":joined[:220],"characters":len(joined)}
            if current_label in KNOWN_MAP_NON_DIALOGUE:
                item["reason"] = KNOWN_MAP_NON_DIALOGUE[current_label]; excluded.append(item)
            else: out.append(item)
        chunks=[]
    for lineno,line in enumerate(lines,1):
        m=LABEL_RE.match(line)
        if m:
            flush(); current_label=m.group(1); current_start=lineno; continue
        sm=STRING_RE.match(line)
        if sm and current_label is not None: chunks.append(sm.group(1))
        elif chunks and line.strip() and not line.lstrip().startswith(".string"): flush()
    flush(); return out, excluded

def decode_c_body(body: str) -> str:
    vals=[]
    for q in C_QUOTED_RE.findall(body):
        try: vals.append(ast.literal_eval(q))
        except Exception: vals.append(q[1:-1])
    return "".join(vals)

def context_class(path: Path, text: str, start: int) -> tuple[str,bool]:
    rel=path.as_posix()
    left=text[max(0,start-240):start]
    if rel.endswith("src/data/abilities.h") and re.search(r"\.name\s*=", left):
        return "ability_name", True
    if rel.endswith("src/data/moves_info.h") and re.search(r"\.name\s*=", left):
        return "move_name", True
    if "species_info" in rel and re.search(r"\.(?:speciesName|name)\s*=", left):
        return "pokemon_name", True
    if re.search(r"\.description\s*=", left): return "description", False
    if rel.endswith("src/data/items.h") and re.search(r"\.name\s*=", left): return "item_name", False
    if rel.endswith("shared_dex_text.h"): return "pokedex_description", False
    if rel.endswith("strings.c"): return "system_ui", False
    if rel.endswith("battle_message.c"): return "battle_message", False
    return "runtime_text", False

def scan_c_file(path: Path, root: Path):
    text=path.read_text(encoding="utf-8",errors="replace")
    out=[]; allowed=[]
    for m in C_MACRO_RE.finditer(text):
        raw=decode_c_body(m.group("body")); v=visible_text(raw)
        if not ASCII_ALPHA_RE.search(v) or CYRILLIC_RE.search(v): continue
        line=text.count("\n",0,m.start())+1
        cls,is_allowed=context_class(path.relative_to(root),text,m.start())
        prefix=text[max(0,m.start()-300):m.start()]
        last_line=prefix.splitlines()[-1].strip() if prefix.splitlines() else ""
        sym=None
        sm=re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[[^\]]*\])?\s*=\s*$", last_line)
        if sm: sym=sm.group(1)
        item={"file":path.relative_to(root).as_posix(),"line":line,"kind":cls,"symbol":sym,"anchor":last_line[-180:],"raw":raw,"preview":v[:240],"characters":len(v)}
        if is_allowed:
            item["reason"]="English proper name allowed by canon"; allowed.append(item)
        else: out.append(item)
    return out,allowed

def scan_asm_text_file(path: Path, root: Path):
    lines=path.read_text(encoding="utf-8",errors="replace").splitlines(); out=[]
    label=None; start=0; chunks=[]
    def flush():
        nonlocal chunks
        if not chunks: return
        v=visible_text(" ".join(chunks))
        if ASCII_ALPHA_RE.search(v) and not CYRILLIC_RE.search(v):
            out.append({"file":path.relative_to(root).as_posix(),"label":label,"line":start,"kind":"data_text","preview":v[:240],"characters":len(v)})
        chunks=[]
    for n,line in enumerate(lines,1):
        m=LABEL_RE.match(line)
        if m: flush(); label=m.group(1); start=n; continue
        sm=STRING_RE.match(line)
        if sm:
            if not chunks: start=n
            chunks.append(sm.group(1))
        elif chunks and line.strip() and not line.lstrip().startswith(".string"): flush()
    flush(); return out

def main() -> int:
    if len(sys.argv)!=2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>",file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve(); maps=root/"data/maps"
    if not maps.is_dir(): die(f"missing {maps}")

    map_candidates=[]; map_excluded=[]
    map_files=sorted(maps.glob("*_Frlg/scripts.inc"))
    for path in map_files:
        a,b=scan_map_file(path,root); map_candidates+=a; map_excluded+=b
    map_candidates.sort(key=lambda x:(-x["characters"],x["file"],x["line"]))

    broad=[]; allowed=[]; scanned=[]
    text_dir=root/"data/text"
    for path in sorted(text_dir.glob("*.inc")):
        if path.name.endswith("_frlg.inc") or path.name in COMMON_TEXT:
            scanned.append(path.relative_to(root).as_posix()); broad+=scan_asm_text_file(path,root)
    scripts_dir=root/"data/scripts"
    for path in sorted(scripts_dir.glob("*.inc")):
        if "frlg" in path.name.lower() or path.name in COMMON_SCRIPTS:
            scanned.append(path.relative_to(root).as_posix()); broad+=scan_asm_text_file(path,root)
    src=root/"src"
    for name in sorted(CORE_C):
        path=src/name
        if path.is_file():
            scanned.append(path.relative_to(root).as_posix()); a,b=scan_c_file(path,root); broad+=a; allowed+=b
    for rel in sorted(DATA_HEADERS):
        path=root/rel
        if path.is_file():
            scanned.append(rel); a,b=scan_c_file(path,root); broad+=a; allowed+=b

    seen=set(); dedup=[]
    for x in broad:
        key=(x["file"],x["line"],x.get("preview",""))
        if key not in seen: seen.add(key); dedup.append(x)
    broad=sorted(dedup,key=lambda x:(-x["characters"],x["file"],x["line"]))
    by_kind={}; by_file={}
    for x in broad:
        by_kind[x["kind"]]=by_kind.get(x["kind"],0)+1
        by_file[x["file"]]=by_file.get(x["file"],0)+1

    report={
      "marker":MARKER,
      "policy":"FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names may remain English",
      "mapRuntime":{
        "filesScanned":len(map_files),
        "untranslatedDialogueBlocks":len(map_candidates),
        "filesWithUntranslatedDialogue":len({x['file'] for x in map_candidates}),
        "excludedCanonicalOrDynamic":map_excluded,
        "candidates":map_candidates,
      },
      "fireRedMapScriptFilesScanned":len(map_files),
      "filesWithEnglishOnlyRuntimeText":len({x['file'] for x in map_candidates}),
      "englishOnlyRuntimeTextBlocks":len(map_candidates),
      "byFile":{k:v for k,v in sorted(((f,sum(1 for x in map_candidates if x['file']==f)) for f in {x['file'] for x in map_candidates}),key=lambda kv:(-kv[1],kv[0]))},
      "largestCandidates":map_candidates[:250],
      "fullSurface":{
        "filesScanned":len(scanned),
        "scannedFiles":scanned,
        "englishOnlyCandidateCount":len(broad),
        "filesWithCandidates":len({x['file'] for x in broad}),
        "byKind":dict(sorted(by_kind.items(),key=lambda kv:(-kv[1],kv[0]))),
        "byFile":dict(sorted(by_file.items(),key=lambda kv:(-kv[1],kv[0]))),
        "candidates":broad[:2000],
        "allowedEnglishProperNames":allowed[:1000],
      },
      "readOnly":True,"ashBondTouched":False,"ashCapTouched":False,
    }
    out=root/"build"/"qarro_ru_runtime_surface_v3_21_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: map untranslated dialogue={len(map_candidates)}; known map exclusions={len(map_excluded)}; broader English candidates={len(broad)} across {len({x['file'] for x in broad})} files; Ash untouched")
    for x in broad[:25]: print(f"[{MARKER}] FULL {x['file']}:{x['line']} {x['kind']}: {x['preview'][:120]}")
    return 0
if __name__=="__main__": raise SystemExit(main())