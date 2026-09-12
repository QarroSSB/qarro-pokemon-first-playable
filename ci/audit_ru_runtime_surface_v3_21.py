#!/usr/bin/env python3
"""Inventory untranslated FireRed runtime text after Qarro RU localization passes.

Read-only audit. It does not modify upstream files. The purpose is to turn the
next localization step into evidence-driven work instead of guessing which
runtime surface remains English.

Policy preserved:
- FireRed target / pinned Expansion 1.17.0
- Gen I-V
- Pokemon, move and ability proper names may remain English
- Ash Bond / Ash Cap are never touched
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_RUNTIME_SURFACE_V3_21"
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
ASCII_ALPHA_RE = re.compile(r"[A-Za-z]")
LABEL_RE = re.compile(r"^([A-Za-z0-9_]+)::\s*$")
STRING_RE = re.compile(r'^\s*\.string\s+"(.*)"\s*$')


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def visible_text(raw: str) -> str:
    # Remove common FireRed text controls while keeping readable words.
    s = raw
    for token in ("\\n", "\\p", "\\l", "\\c", "\\v", "\\x"):
        s = s.replace(token, " ")
    s = re.sub(r"\\[A-Za-z0-9_{}]+", " ", s)
    s = s.replace("$", " ")
    return re.sub(r"\s+", " ", s).strip()


def scan_file(path: Path, root: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[dict] = []
    current_label: str | None = None
    current_start = 0
    chunks: list[str] = []

    def flush() -> None:
        nonlocal current_label, current_start, chunks
        if current_label is None or not chunks:
            chunks = []
            return
        joined = visible_text(" ".join(chunks))
        if ASCII_ALPHA_RE.search(joined) and not CYRILLIC_RE.search(joined):
            # Runtime text labels are the useful surface; script/event labels are ignored.
            if "_Text_" in current_label or current_label.endswith("_Text"):
                out.append({
                    "file": path.relative_to(root).as_posix(),
                    "label": current_label,
                    "line": current_start,
                    "preview": joined[:220],
                    "characters": len(joined),
                })
        chunks = []

    for lineno, line in enumerate(lines, start=1):
        m = LABEL_RE.match(line)
        if m:
            flush()
            current_label = m.group(1)
            current_start = lineno
            continue
        sm = STRING_RE.match(line)
        if sm and current_label is not None:
            chunks.append(sm.group(1))
        elif chunks and line.strip() and not line.lstrip().startswith(".string"):
            flush()
    flush()
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    maps = root / "data/maps"
    if not maps.is_dir():
        die(f"missing {maps}")

    files = sorted(maps.glob("*_Frlg/scripts.inc"))
    if not files:
        die("no FireRed map script files found")

    candidates: list[dict] = []
    files_with_candidates: set[str] = set()
    for path in files:
        found = scan_file(path, root)
        candidates.extend(found)
        files_with_candidates.update(x["file"] for x in found)

    # Sort largest dialogue blocks first so the next pass attacks meaningful surfaces.
    candidates.sort(key=lambda x: (-x["characters"], x["file"], x["line"]))
    by_file: dict[str, int] = {}
    for item in candidates:
        by_file[item["file"]] = by_file.get(item["file"], 0) + 1

    report = {
        "marker": MARKER,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability names may remain English",
        "scope": "data/maps/*_Frlg/scripts.inc runtime _Text_ labels after all current RU passes",
        "fireRedMapScriptFilesScanned": len(files),
        "filesWithEnglishOnlyRuntimeText": len(files_with_candidates),
        "englishOnlyRuntimeTextBlocks": len(candidates),
        "byFile": dict(sorted(by_file.items(), key=lambda kv: (-kv[1], kv[0]))),
        "largestCandidates": candidates[:250],
        "readOnly": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }

    build = root / "build"
    build.mkdir(parents=True, exist_ok=True)
    out = build / "qarro_ru_runtime_surface_v3_21_audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: scanned {len(files)} FireRed map scripts; "
        f"English-only runtime blocks={len(candidates)} across {len(files_with_candidates)} files; "
        "read-only inventory written; Ash Bond/Ash Cap untouched"
    )
    for item in candidates[:20]:
        print(f"[{MARKER}] CANDIDATE {item['file']}:{item['line']} {item['label']}: {item['preview'][:120]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
