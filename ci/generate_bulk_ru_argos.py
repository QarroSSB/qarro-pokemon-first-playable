#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import argostranslate.package
import argostranslate.translate

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
        self.calls = 0
        self.changed = 0
        self.failed = []

    def _mask(self, s: str):
        mapping: list[tuple[str, str]] = []

        def add(value: str) -> str:
            token = f"ZXQ{len(mapping):04d}QXZ"
            mapping.append((token, value))
            return token

        s = CONTROL_RE.sub(lambda m: add(m.group(0)), s)
        for term in self.canonical_terms:
            if term in s:
                s = s.replace(term, add(term))
        return s, mapping

    def translate(self, s: str) -> str:
        if s in self.cache:
            return self.cache[s]
        if not english_only(s):
            self.cache[s] = s
            return s

        masked, mapping = self._mask(s)
        ru = argostranslate.translate.translate(masked, "en", "ru")
        self.calls += 1
        for token, original in mapping:
            if token not in ru:
                self.failed.append({"source": s, "masked": masked, "translation": ru, "missing": token})
                self.cache[s] = s
                return s
            ru = ru.replace(token, original)

        ru = normalize_ru(ru)
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

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: generate_bulk_ru_argos.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    install_argos_model()
    canonical = collect_canonical_terms(root)
    tr = Translator(canonical)

    probe = tr.translate("{STR_VAR_1} used Rock Smash!$")
    if "{STR_VAR_1}" not in probe or "Rock Smash" not in probe or "$" not in probe:
        raise RuntimeError(f"placeholder/canon preflight failed: {probe!r}")

    report = {"targetAsm": {}, "targetC": {}, "canonicalTermCount": len(canonical)}
    for rel in TARGET_ASM:
        report["targetAsm"][rel] = translate_asm(root / rel, tr)
    for rel in TARGET_C:
        report["targetC"][rel] = translate_c(root / rel, tr)

    report["translationCalls"] = tr.calls
    report["changedUniqueStrings"] = tr.changed
    report["cacheSize"] = len(tr.cache)
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
