#!/usr/bin/env python3
"""Read-only guard for permanently protected Ash Bond / Ash Cap policy.

Audits only the Qarro-applied diff against the pinned upstream checkout. The
upstream project may contain dormant Ash-related support; this gate does not
ban that baseline. It fails only if Qarro's applied patch changes an Ash-named
path or adds/removes Ash Bond / Ash Cap identifiers, which would indicate an
attempt to touch, restore, or reconnect those features.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_PROTECTED_FEATURES_V3_13"
PATTERN = re.compile(r"ash[ _-]?(?:bond|cap)|ASH_?(?:BOND|CAP)", re.IGNORECASE)


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    if not (root / ".git").exists():
        raise RuntimeError(f"not a git checkout: {root}")

    changed = [line.strip() for line in git(root, "diff", "--name-only").splitlines() if line.strip()]
    path_hits = [path for path in changed if PATTERN.search(path)]

    diff = git(root, "diff", "--no-ext-diff", "--unified=0")
    line_hits: list[str] = []
    for line in diff.splitlines():
        if not line or line.startswith(("+++", "---")):
            continue
        if line[0] not in "+-":
            continue
        if PATTERN.search(line[1:]):
            line_hits.append(line[:240])

    if path_hits or line_hits:
        raise RuntimeError(
            "protected Ash feature regression: "
            f"paths={path_hits[:10]} diffLines={line_hits[:10]}"
        )

    report = {
        "marker": MARKER,
        "scope": "Qarro-applied diff vs pinned upstream",
        "changedFilesAudited": len(changed),
        "ashBondTouched": False,
        "ashCapTouched": False,
        "protectedPathHits": 0,
        "protectedDiffLineHits": 0,
    }
    out = root / "build/qarro_protected_features_v3_13_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: Qarro diff does not touch Ash Bond or Ash Cap")
    print(f"audit: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
