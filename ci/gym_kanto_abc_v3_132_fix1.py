#!/usr/bin/env python3
"""Compatibility fix for Qarro Kanto Gym A/B/C v3.132 save-var validation.

The v3.132 implementation correctly reserves FireRed save slots 0x40BD/0x40BE,
but its first fail-closed validator treated declarations in the shared
include/constants/vars.h (Emerald aliases at the same numeric addresses) as
runtime use.  This wrapper keeps every v3.132 team/selector edit unchanged and
only replaces that validator with a declaration-aware check.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MARKER = "QARRO_KANTO_GYM_ABC_V3_132_FIX1"


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def validate_free_save_vars(root: Path) -> None:
    definition_headers = {
        (root / "include/constants/vars.h").resolve(),
        (root / "include/constants/vars_frlg.h").resolve(),
    }
    needles = (
        "VAR_0x40BD",
        "VAR_0x40BE",
        "VAR_JAGGED_PASS_ASH_WEATHER",
        "VAR_GLASS_WORKSHOP_STATE",
        "0x40BD",
        "0x40BE",
    )
    hits: list[str] = []
    for base in (root / "src", root / "data", root / "include"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".c", ".h", ".inc", ".s", ".txt"}:
                continue
            if path.resolve() in definition_headers:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if any(needle in text for needle in needles):
                hits.append(str(path.relative_to(root)))
                if len(hits) >= 10:
                    break
        if hits:
            break
    if hits:
        die(f"save vars 0x40BD/0x40BE have real runtime references: {hits}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    script = Path(__file__).resolve().with_name("gym_kanto_abc_v3_132.py")
    if not script.is_file():
        die(f"base v3.132 script missing: {script}")

    spec = importlib.util.spec_from_file_location("qarro_gym_kanto_abc_v3_132_base", script)
    if spec is None or spec.loader is None:
        die("could not load base v3.132 module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Replace only the over-broad preflight. All team data, trainer IDs,
    # persistence encoding and battle_setup patching remain from v3.132.
    module.validate_free_save_vars = validate_free_save_vars
    rc = int(module.main() or 0)
    if rc == 0:
        print(f"[{MARKER}] PASS: declaration-aware save-var validation; base v3.132 applied unchanged")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
