#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import argostranslate.package
import argostranslate.translate
import argostranslate.settings
import ctranslate2

CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
ASCII_ALPHA_RE = re.compile(r"[A-Za-z]")
ASM_STRING_RE = re.compile(r'^(?P<prefix>\s*\.string\s+)"(?P<body>(?:\\.|[^"\\])*)"\s*$')
C_MACRO_RE = re.compile(r'(?P<macro>COMPOUND_STRING|_)\s*\(\s*(?P<body>(?:"(?:\\.|[^"\\])*"\s*)+)\)', re.S)
C_QUOTED_RE = re.compile(r'"(?P<body>(?:\\.|[^"\\])*)"')
CONTROL_RE = re.compile(r'\{[^{}]+\}|\\[A-Za-z0-9_]+|\$')

TARGET_ASM = [
    "data/text/trainers.inc",
    "data/text/fame_checker_frlg.inc",
    "data/text/trainers_frlg.inc",
    "data/scripts/cable_club_frlg.inc",
    "data/text/trainer_card_frlg.inc",
]
TARGET_C = [
    "src/data/items.h",
    "src/battle_message.c",
    "src/strings.c",
    "src/pokedex.c",
    "src/data/pokemon/species_info/shared_dex_text.h",
]

def visible_text(s: str) -> str:
    s = re.sub(r"\{[^{}]*\}", " ", s)
    s = re.sub(r"\\[A-Za-z0-9_]+", " ", s)
    s = s.replace("$", " ")
    return re.sub(r"\s+", " ", s).strip()

def english_only(s: str) -> bool:
    v = visible_text(s)
    return bool(ASCII_ALPHA_RE.search(v)) and not CYRILLIC_RE.search(v)

def normalize_ru(s: str) -> str:
    return (
        s.replace("\r", " ")
         .replace("\n", " ")
         .replace("\u00a0", " ")
         .replace("—", "-")
         .replace("–", "-")
         .replace("“", '"')
         .replace("”", '"')
         .replace("„", '"')
         .replace("«", '"')
         .replace("»", '"')
         .replace("‘", "'")
         .replace("’", "'")
    )

def collect_canonical_terms(root: Path) -> list[str]:
    terms = {"POKéMON", "POKeMON", "Pokémon", "Pokemon", "POKéDEX", "POKeDEX", "Pokédex", "Pokedex"}

    def add_names(path: Path, field_pattern: str):
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        pat = re.compile(field_pattern)
        for m in pat.finditer(text):
            name = m.group(1)
            if name and any(ch.isalpha() for ch in name):
                terms.add(name)
                terms.add(name.upper())

    add_names(root / "src/data/moves_info.h", r'\.name\s*=\s*COMPOUND_STRING\("([^"]+)"\)')
    add_names(root / "src/data/abilities.h", r'\.name\s*=\s*(?:COMPOUND_STRING|_)\("([^"]+)"\)')

    species_root = root / "src/data/pokemon/species_info"
    if species_root.is_dir():
        for path in species_root.rglob("*.h"):
            add_names(path, r'\.speciesName\s*=\s*(?:COMPOUND_STRING|_)\("([^"]+)"\)')

    return sorted(terms, key=lambda x: (-len(x), x))

def install_argos_model() -> None:
    installed = argostranslate.translate.get_installed_languages()
    if any(x.code == "en" for x in installed) and any(x.code == "ru" for x in installed):
        return
    argostranslate.package.update_package_index()
    packages = argostranslate.package.get_available_packages()
    pkg = next(p for p in packages if p.from_code == "en" and p.to_code == "ru")
    argostranslate.package.install_from_path(pkg.download())

class Translator:
    def __init__(self, canonical_terms: list[str]):
        self.canonical_terms = canonical_terms
        self.cache: dict[str, str] = {}
        self.segment_cache: dict[str, str] = {}
        self.calls = 0
        self.changed = 0
        self.failed = []

    def _protected_regex(self):
        # Protect runtime controls and every canonical Pokémon / Move / Ability
        # term by splitting around them. Protected spans never enter Argos.
        terms = [re.escape(x) for x in self.canonical_terms if x]
        parts = [r'\{[^{}]+\}', r'\\[A-Za-z0-9_]+', r'\$']
        if terms:
            parts.append("|".join(terms))
        return re.compile("(" + "|".join(parts) + ")")

    def prepare(self, sources: list[str]) -> None:
        protected = self._protected_regex()
        unique = []
        seen = set()
        for s in sources:
            if not english_only(s):
                continue
            for piece in protected.split(s):
                if not piece or protected.fullmatch(piece) or not ASCII_ALPHA_RE.search(piece):
                    continue
                if piece not in seen:
                    seen.add(piece)
                    unique.append(piece)
        if not unique:
            return

        packages = argostranslate.package.get_installed_packages()
        pkg = next(p for p in packages if p.from_code == "en" and p.to_code == "ru")
        params = {
            "model_path": str(pkg.package_path / "model"),
            "device": argostranslate.settings.device,
            "inter_threads": argostranslate.settings.inter_threads,
            "intra_threads": argostranslate.settings.intra_threads,
        }
        if argostranslate.settings.compute_type != "auto":
            params["compute_type"] = argostranslate.settings.compute_type
        engine = ctranslate2.Translator(**params)
        tokenized = [pkg.tokenizer.encode(x) for x in unique]
        target_prefix = None
        if pkg.target_prefix != "":
            target_prefix = [[pkg.target_prefix]] * len(tokenized)
        results = engine.translate_batch(
            tokenized,
            target_prefix=target_prefix,
            replace_unknowns=True,
            max_batch_size=128,
            batch_type="tokens",
            beam_size=1,
            num_hypotheses=1,
            return_scores=True,
        )
        if len(results) != len(unique):
            raise RuntimeError(f"batch result count mismatch: {len(results)} != {len(unique)}")
        for src, result in zip(unique, results):
            ru = pkg.tokenizer.decode(result.hypotheses[0])
            if pkg.target_prefix and ru.startswith(pkg.target_prefix):
                ru = ru[len(pkg.target_prefix):]
            if ru.startswith(" "):
                ru = ru[1:]
            self.segment_cache[src] = normalize_ru(ru)
        self.calls += len(unique)

    def translate(self, s: str) -> str:
        if s in self.cache:
            return self.cache[s]
        if not english_only(s):
            self.cache[s] = s
            return s

        protected = self._protected_regex()
        pieces = protected.split(s)
        out = []
        for piece in pieces:
            if not piece:
                continue
            if protected.fullmatch(piece):
                out.append(piece)
                continue
            if not ASCII_ALPHA_RE.search(piece):
                out.append(piece)
                continue
            ru_piece = self.segment_cache.get(piece)
            if ru_piece is None:
                ru_piece = normalize_ru(argostranslate.translate.translate(piece, "en", "ru"))
                self.calls += 1
                self.segment_cache[piece] = ru_piece
            out.append(ru_piece)

        ru = "".join(out)
        # Exact invariant: all protected controls/canonical terms occur in the
        # same order after translation because they were never model input.
        before = protected.findall(s)
        after = protected.findall(ru)
        if before != after:
            self.failed.append({"source": s, "translation": ru, "before": before, "after": after})
            self.cache[s] = s
            return s

        if not CYRILLIC_RE.search(ru):
            self.cache[s] = s
            return s
        self.cache[s] = ru
        if ru != s:
            self.changed += 1
        return ru

def escape_quoted(s: str) -> str:
    s = s.replace("\n", " ")
    return s.replace('"', r'\"')

def translate_asm(path: Path, tr: Translator) -> dict:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    out = []
    blocks = translated = 0
    i = 0
    while i < len(lines):
        m = ASM_STRING_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        prefix = m.group("prefix")
        bodies = []
        j = i
        while j < len(lines):
            mm = ASM_STRING_RE.match(lines[j])
            if not mm:
                break
            bodies.append(mm.group("body"))
            j += 1
        raw = "".join(bodies)
        blocks += 1
        ru = tr.translate(raw)
        if ru != raw:
            translated += 1
            out.append(f'{prefix}"{escape_quoted(ru)}"')
        else:
            out.extend(lines[i:j])
        i = j
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return {"blocks": blocks, "translatedBlocks": translated}

def translate_c(path: Path, tr: Translator) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    matches = list(C_MACRO_RE.finditer(text))
    translated = 0
    for m in reversed(matches):
        body = m.group("body")
        raw = "".join(q.group("body") for q in C_QUOTED_RE.finditer(body))
        if not english_only(raw):
            continue
        ru = tr.translate(raw)
        if ru == raw:
            continue
        replacement = '"' + escape_quoted(ru) + '"'
        text = text[:m.start("body")] + replacement + text[m.end("body"):]
        translated += 1
    path.write_text(text, encoding="utf-8")
    return {"macroMatches": len(matches), "translatedMacros": translated}

def collect_asm_raw(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    out = []
    i = 0
    while i < len(lines):
        m = ASM_STRING_RE.match(lines[i])
        if not m:
            i += 1
            continue
        bodies = []
        j = i
        while j < len(lines):
            mm = ASM_STRING_RE.match(lines[j])
            if not mm:
                break
            bodies.append(mm.group("body"))
            j += 1
        out.append("".join(bodies))
        i = j
    return out

def collect_c_raw(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    out = []
    for m in C_MACRO_RE.finditer(text):
        body = m.group("body")
        out.append("".join(q.group("body") for q in C_QUOTED_RE.finditer(body)))
    return out

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: generate_bulk_ru_argos.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    install_argos_model()
    canonical = collect_canonical_terms(root)
    tr = Translator(canonical)

    probe_src = "{STR_VAR_1} used Rock Smash!\\nDone.$"
    raw_sources = [probe_src]
    for rel in TARGET_ASM:
        raw_sources.extend(collect_asm_raw(root / rel))
    for rel in TARGET_C:
        raw_sources.extend(collect_c_raw(root / rel))
    tr.prepare(raw_sources)
    probe = tr.translate(probe_src)
    if "{STR_VAR_1}" not in probe or "Rock Smash" not in probe or "\\n" not in probe or "$" not in probe:
        raise RuntimeError(f"placeholder/canon preflight failed: {probe!r}")

    report = {"targetAsm": {}, "targetC": {}, "canonicalTermCount": len(canonical)}
    for rel in TARGET_ASM:
        report["targetAsm"][rel] = translate_asm(root / rel, tr)
    for rel in TARGET_C:
        report["targetC"][rel] = translate_c(root / rel, tr)

    report["translationCalls"] = tr.calls
    report["changedUniqueStrings"] = tr.changed
    report["cacheSize"] = len(tr.cache)
    report["preparedSegmentCount"] = len(tr.segment_cache)
    report["placeholderFailures"] = tr.failed
    out = root / "build" / "qarro_argos_bulk_translation_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if tr.failed:
        raise RuntimeError(f"placeholder failures: {len(tr.failed)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
