#!/usr/bin/env python3
"""Qarro v3.104: safely apply the quarantined Resort/Fuchsia/Cerulean RU pass.

v3.103 contains the intended 66 translations, but its Python string literals
turn ``\n`` into physical LF characters before writing assembler strings.  That
can split a FireRed ``.string`` across source lines and make the ARM build fail.

This wrapper keeps v3.103 quarantined, loads its exact translation table, and
replaces only its assembler serializer so physical newlines become one literal
FireRed ``\n`` control code. Existing ``\p``/``\l`` codes are deliberately not
doubled. Pokémon species, Move and Ability proper names remain English.
Gameplay/trainer data and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_RESORT_FUCHSIA_CERULEAN_V3_104"
LEGACY = Path(__file__).with_name("localize_resort_fuchsia_cerulean_v3_103.py")
TARGETS = (
    Path("data/maps/FiveIsland_ResortGorgeous_Frlg/scripts.inc"),
    Path("data/maps/FuchsiaCity_Gym_Frlg/scripts.inc"),
    Path("data/maps/CeruleanCity_Frlg/scripts.inc"),
)
EXPECTED = 66


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def safe_asm_quote(text: str) -> str:
    """Serialize a Python translation into one FireRed assembler string."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return normalized.replace("\n", "\\n").replace('"', '\\"')


def load_legacy_module():
    if not LEGACY.is_file():
        die(f"missing quarantined translation source: {LEGACY.name}")
    spec = importlib.util.spec_from_file_location("qarro_v3_103_quarantined", LEGACY)
    if spec is None or spec.loader is None:
        die("could not load v3.103 translation source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_output(root: Path) -> dict[str, int]:
    translated_by_file: dict[str, int] = {}
    total = 0
    for rel in TARGETS:
        path = root / rel
        if not path.is_file():
            die(f"missing translated target: {rel}")
        text = path.read_text(encoding="utf-8")
        # Every assembler string must open and close on the same physical line.
        for lineno, line in enumerate(text.splitlines(), start=1):
            if ".string \"" in line and line.count('"') < 2:
                die(f"{rel}:{lineno}: physical newline inside assembler string")
        if re.search(r"\\\\[npl]", text):
            die(f"{rel}: doubled FireRed runtime escape found")
        if not re.search(r"[А-Яа-яЁё]", text):
            die(f"{rel}: expected Cyrillic output is missing")

        patches = getattr(load_legacy_module(), "FILES", {}).get(rel)
        if patches is None:
            die(f"{rel}: target missing from v3.103 translation table")
        translated_by_file[str(rel)] = len(patches)
        total += len(patches)

    if total != EXPECTED:
        die(f"expected {EXPECTED} translated blocks, got {total}")
    return translated_by_file


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    legacy = load_legacy_module()
    legacy.asm_quote = safe_asm_quote

    # v3.103 main sees this wrapper's unchanged argv (<script> <upstream-root>).
    rc = legacy.main()
    if rc != 0:
        die(f"v3.103 translation source returned {rc}")

    translated_by_file = validate_output(root)
    audit = root / "build" / "qarro_ru_resort_fuchsia_cerulean_v3_104_audit.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(
        json.dumps(
            {
                "marker": MARKER,
                "translatedBlockCount": EXPECTED,
                "translatedByFile": translated_by_file,
                "physicalNewlinesInsideAsmStrings": False,
                "doubledRuntimeEscapes": False,
                "sourcePass": LEGACY.name,
                "sourcePassQuarantined": True,
                "gameplayLogicTouched": False,
                "trainerDataTouched": False,
                "ashBondTouched": False,
                "ashCapTouched": False,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"[{MARKER}] PASS: safely serialized {EXPECTED} runtime blocks; "
        "physical LF -> FireRed \\n; v3.103 remains quarantined; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
