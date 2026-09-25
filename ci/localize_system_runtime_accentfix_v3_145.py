#!/usr/bin/env python3
"""Qarro v3.145 exact-anchor wrapper for pre-normalization FireRed text.

The v3.145 donor table was generated from an audit snapshot taken after the
final accented-e normalizer, while the incremental localization runner executes
before that normalizer. Restore only the mechanically normalized POKe* tokens
in expected English anchors to their pinned FireRed POKé* spelling, then run
the unchanged v3.145 translator. Russian replacements, placeholder/control
contracts, gameplay, trainer logic, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

from pathlib import Path

BASE = "localize_system_runtime_v3_145.py"
EXPECTED_RESTORED_ANCHORS = 30


def load_base() -> dict:
    path = Path(__file__).resolve().with_name(BASE)
    if not path.is_file():
        raise RuntimeError(f"missing v3.145 base translator: {path}")
    code = path.read_text(encoding="utf-8")
    ns = {
        "__name__": "qarro_system_runtime_v3145_base",
        "__file__": str(path),
    }
    exec(compile(code, str(path), "exec"), ns)
    return ns


def main() -> int:
    ns = load_base()
    targets = ns.get("TARGETS")
    if not isinstance(targets, dict):
        raise RuntimeError("v3.145 TARGETS table missing or changed type")

    restored = 0
    for file_targets in targets.values():
        for symbol, pair in list(file_targets.items()):
            if not isinstance(pair, tuple) or len(pair) != 2:
                raise RuntimeError(f"{symbol}: unexpected target record")
            expected, replacement = pair
            restored_expected = expected.replace("POKe", "POKé")
            if restored_expected != expected:
                restored += 1
                file_targets[symbol] = (restored_expected, replacement)

    if restored != EXPECTED_RESTORED_ANCHORS:
        raise RuntimeError(
            f"expected to restore {EXPECTED_RESTORED_ANCHORS} accented-e anchors, got {restored}"
        )

    rc = int(ns["main"]() or 0)
    if rc:
        return rc
    print(
        "[QARRO_RU_SYSTEM_ACCENTFIX_V3_145] PASS: restored exactly 30 pre-normalization "
        "POKé* source anchors; unchanged 355-string translator completed; Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
