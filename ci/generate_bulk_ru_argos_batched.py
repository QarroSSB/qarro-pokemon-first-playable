#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

import argostranslate.package
import argostranslate.settings as argos_settings
import argostranslate.translate
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

class BatchTranslator:
    def __init__(self, canonical_terms: list[str]):
        # Protected fragments are never passed through the MT model. This makes
        # FireRed control tokens and canonical Pokemon/Move/Ability names exact
        # by construction instead of hoping a placeholder survives translation.
        alt = "|".join(re.escape(x) for x in canonical_terms)
        control = r"\\{[^{}]+\\}|\\\\[A-Za-z0-9_]+|\\$"
        self.protect_re = re.compile(f"({control}|{alt})" if alt else f"({control})")
        self.cache: dict[str, str] = {}
        self.changed = 0
        self.batch_inputs = 0

    def _parts(self, s: str) -> list[tuple[str, bool]]:
        out = []
        for part in self.protect_re.split(s):
            if not part:
                continue
            out.append((part, bool(self.protect_re.fullmatch(part))))
        return out

    def _ensure_engine(self):
        translation = argostranslate.translate.get_translation_from_codes("en", "ru")
        # Argos exposes a CachedTranslation wrapper publicly; unwrap it until
        # the underlying PackageTranslation that owns pkg/translator is reached.
        while hasattr(translation, "underlying"):
            translation = translation.underlying
        pkg = translation.pkg
        if translation.translator is None:
            params = {
                "model_path": str(pkg.package_path / "model"),
                "device": argos_settings.device,
                "inter_threads": max(1, argos_settings.inter_threads),
                "intra_threads": argos_settings.intra_threads,
            }
            if argos_settings.compute_type != "auto":
                params["compute_type"] = argos_settings.compute_type
            translation.translator = ctranslate2.Translator(**params)
        return translation, pkg

    def preload(self, strings: list[str]) -> None:
        chunks = []
        for s in strings:
            for part, protected in self._parts(s):
                if protected or not english_only(part):
                    self.cache.setdefault(part, part)
                else:
                    chunks.append(part)

        todo = [x for x in OrderedDict.fromkeys(chunks) if x not in self.cache]
        if not todo:
            return

        translation, pkg = self._ensure_engine()
        tokenized = [pkg.tokenizer.encode(x) for x in todo]
        target_prefix = None
        if pkg.target_prefix != "":
            target_prefix = [[pkg.target_prefix]] * len(tokenized)

        results = translation.translator.translate_batch(
            tokenized,
            target_prefix=target_prefix,
            replace_unknowns=True,
            max_batch_size=1024,
            batch_type="tokens",
            beam_size=1,
            num_hypotheses=1,
            length_penalty=0.2,
            return_scores=True,
        )
        if len(results) != len(todo):
            raise RuntimeError(f"batch result count mismatch: {len(results)} != {len(todo)}")

        self.batch_inputs += len(todo)
        for source, result in zip(todo, results):
            ru = pkg.tokenizer.decode(result.hypotheses[0])
            if pkg.target_prefix and ru.startswith(pkg.target_prefix):
                ru = ru[len(pkg.target_prefix):]
            if ru.startswith(" "):
                ru = ru[1:]
            ru = normalize_ru(ru)
            if not CYRILLIC_RE.search(ru):
                ru = source
            self.cache[source] = ru
            if ru != source:
                self.changed += 1

    def translate(self, s: str) -> str:
        out = []
        for part, protected in self._parts(s):
            if protected:
                out.append(part)
            else:
                if part not in self.cache:
                    # Non-English punctuation/whitespace segments can be absent
                    # from preload; they must pass through unchanged.
                    if not english_only(part):
                        out.append(part)
                        continue
                    raise RuntimeError(f"unpreloaded translation segment: {part[:120]!r}")
                out.append(self.cache[part])
        return "".join(out)

def escape_quoted(s: str) -> str:
    return s.replace("\n", " ").replace('"', r'\"')

def collect_asm(path: Path) -> list[str]:
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

def collect_c(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    out = []
    for m in C_MACRO_RE.finditer(text):
        body = m.group("body")
        out.append("".join(q.group("body") for q in C_QUOTED_RE.finditer(body)))
    return out

def translate_asm(path: Path, tr: BatchTranslator) -> dict:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    out = []
    blocks = translated = 0
    i = 0
    while i < len(lines):
        m = ASM_STRING_RE.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        prefix = m.group("prefix")
        bodies = []
        j = i
        while j < len(lines):
            mm = ASM_STRING_RE.match(lines[j])
            if not mm: break
            bodies.append(mm.group("body")); j += 1
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

def translate_c(path: Path, tr: BatchTranslator) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    matches = list(C_MACRO_RE.finditer(text))
    translated = 0
    for m in reversed(matches):
        body = m.group("body")
        raw = "".join(q.group("body") for q in C_QUOTED_RE.finditer(body))
        ru = tr.translate(raw)
        if ru == raw: continue
        replacement = '"' + escape_quoted(ru) + '"'
        text = text[:m.start("body")] + replacement + text[m.end("body"):]
        translated += 1
    path.write_text(text, encoding="utf-8")
    return {"macroMatches": len(matches), "translatedMacros": translated}

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: generate_bulk_ru_argos_batched.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    install_argos_model()
    canonical = collect_canonical_terms(root)
    tr = BatchTranslator(canonical)

    all_strings = ["{STR_VAR_1} used Rock Smash!$"]
    for rel in TARGET_ASM:
        all_strings.extend(collect_asm(root / rel))
    for rel in TARGET_C:
        all_strings.extend(collect_c(root / rel))
    tr.preload(all_strings)

    probe = tr.translate("{STR_VAR_1} used Rock Smash!$")
    if "{STR_VAR_1}" not in probe or "Rock Smash" not in probe or "$" not in probe:
        raise RuntimeError(f"placeholder/canon preflight failed: {probe!r}")

    report = {"targetAsm": {}, "targetC": {}, "canonicalTermCount": len(canonical)}
    for rel in TARGET_ASM:
        report["targetAsm"][rel] = translate_asm(root / rel, tr)
    for rel in TARGET_C:
        report["targetC"][rel] = translate_c(root / rel, tr)

    report["batchInputs"] = tr.batch_inputs
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
