#!/usr/bin/env python3
"""Fail-closed completion gate for the FireRed Russian runtime audit.

This does not modify upstream sources. It promotes the existing inventory into a
regression gate for map dialogue: after the localization chain has run, no
English-only FireRed map dialogue blocks may remain. Canonical/dynamic exclusions
continue to be owned by audit_ru_runtime_surface_v3_21.py.

FireRed / Expansion 1.17.0 / Gen I-V only. Ash Bond / Ash Cap untouched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_RUNTIME_COMPLETION_V3_215"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <audit-json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        raise SystemExit(f"[{MARKER}] ERROR: missing audit report: {path}")

    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("marker") != "QARRO_RU_RUNTIME_SURFACE_V3_21":
        raise SystemExit(f"[{MARKER}] ERROR: unexpected audit marker: {report.get('marker')!r}")

    runtime = report.get("mapRuntime")
    if not isinstance(runtime, dict):
        raise SystemExit(f"[{MARKER}] ERROR: mapRuntime section missing")

    count = runtime.get("untranslatedDialogueBlocks")
    candidates = runtime.get("candidates")
    if not isinstance(count, int) or not isinstance(candidates, list):
        raise SystemExit(f"[{MARKER}] ERROR: malformed map runtime evidence")
    if count != len(candidates):
        raise SystemExit(
            f"[{MARKER}] ERROR: candidate count mismatch: declared={count}, listed={len(candidates)}"
        )
    if count:
        first = candidates[0]
        raise SystemExit(
            f"[{MARKER}] BLOCKER: {count} English-only FireRed map dialogue block(s) remain; "
            f"first={first.get('file')}:{first.get('line')} {first.get('label')}"
        )

    print(f"[{MARKER}] PASS: zero English-only FireRed map dialogue blocks remain")
    print(f"[{MARKER}] Ash Bond/Ash Cap untouched; read-only gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
