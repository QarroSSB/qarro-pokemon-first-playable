#!/usr/bin/env python3
"""Qarro v3.133: safe save-var compatibility layer for Kanto Gym A/B/C v3.132.

The v3.132 implementation is kept intact. This runner relocates its two packed
save variables from 0x40BD/0x40BE (which collide textually with Emerald aliases
in the shared vars.h header) to 0x40DB/0x40DC, addresses explicitly marked
unused in both the generic and FRLG variable maps. Before applying v3.132 it
fail-closes if either replacement address is referenced anywhere in runtime
source/data outside the two declaration headers.

No roster, move, item, trainer, map, localization, font, Ash Bond or Ash Cap
logic is changed here.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

MARKER = "QARRO_KANTO_GYM_ABC_SAVEVARS_V3_133"
BITS_ADDR = "0x40DB"
INIT_ADDR = "0x40DC"


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def load_v3132() -> object:
    path = Path(__file__).resolve().with_name("gym_kanto_abc_v3_132.py")
    if not path.is_file():
        die(f"missing required base pass: {path}")
    spec = importlib.util.spec_from_file_location("qarro_gym_kanto_abc_v3132", path)
    if spec is None or spec.loader is None:
        die("could not create import spec for v3.132")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_replacement_vars(root: Path) -> None:
    frlg = root / "include/constants/vars_frlg.h"
    generic = root / "include/constants/vars.h"
    if not frlg.is_file() or not generic.is_file():
        die("missing vars_frlg.h or vars.h")

    frlg_text = frlg.read_text(encoding="utf-8")
    generic_text = generic.read_text(encoding="utf-8")
    expected = (
        (frlg_text, r"(?m)^#define\s+VAR_0x40DB\s+0x40DB\b", "FRLG 0x40DB"),
        (frlg_text, r"(?m)^#define\s+VAR_0x40DC\s+0x40DC\b", "FRLG 0x40DC"),
        (generic_text, r"(?m)^#define\s+VAR_UNUSED_0x40DB\s+0x40DB\b", "generic unused 0x40DB"),
        (generic_text, r"(?m)^#define\s+VAR_UNUSED_0x40DC\s+0x40DC\b", "generic unused 0x40DC"),
    )
    for text, pattern, label in expected:
        if re.search(pattern, text) is None:
            die(f"expected unused declaration missing: {label}")

    ignored = {frlg.resolve(), generic.resolve()}
    needles = (
        "0x40DB", "0x40DC",
        "VAR_0x40DB", "VAR_0x40DC",
        "VAR_UNUSED_0x40DB", "VAR_UNUSED_0x40DC",
    )
    hits: list[str] = []
    for base in (root / "src", root / "data", root / "include"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".c", ".h", ".inc", ".s", ".txt"}:
                continue
            if path.resolve() in ignored:
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
        die(f"replacement save vars 0x40DB/0x40DC are in runtime use: {hits}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    validate_replacement_vars(root)

    base = load_v3132()
    if getattr(base, "VARIANT_BITS_VAR", None) != "0x40BD" or getattr(base, "VARIANT_INIT_VAR", None) != "0x40BE":
        die("v3.132 save-var anchors drifted; refusing monkeypatch")

    selector = getattr(base, "SELECTOR_CREATE_PARTY", "")
    if selector.count("0x40BD") != 1 or selector.count("0x40BE") != 1:
        die("v3.132 selector save-var literals drifted")

    base.VARIANT_BITS_VAR = BITS_ADDR
    base.VARIANT_INIT_VAR = INIT_ADDR
    base.SELECTOR_CREATE_PARTY = selector.replace("0x40BD", BITS_ADDR).replace("0x40BE", INIT_ADDR)
    base.validate_free_save_vars = validate_replacement_vars

    rc = int(base.main() or 0)
    if rc:
        return rc

    battle = root / "src/battle_setup.c"
    text = battle.read_text(encoding="utf-8")
    required = (
        "#define QARRO_KANTO_GYM_VARIANT_BITS_VAR 0x40DB",
        "#define QARRO_KANTO_GYM_VARIANT_INIT_VAR 0x40DC",
        "VarGet(QARRO_KANTO_GYM_VARIANT_BITS_VAR)",
        "VarSet(QARRO_KANTO_GYM_VARIANT_BITS_VAR, packed)",
        "VarSet(QARRO_KANTO_GYM_VARIANT_INIT_VAR, initialized)",
    )
    for token in required:
        if token not in text:
            die(f"post-apply selector verification failed: {token}")
    if "#define QARRO_KANTO_GYM_VARIANT_BITS_VAR 0x40BD" in text or "#define QARRO_KANTO_GYM_VARIANT_INIT_VAR 0x40BE" in text:
        die("old v3.132 save-var addresses survived")

    print(
        f"[{MARKER}] PASS: v3.132 roster/selector preserved; save vars safely relocated "
        f"to {BITS_ADDR}/{INIT_ADDR}; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
