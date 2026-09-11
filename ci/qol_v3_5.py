#!/usr/bin/env python3
"""Qarro QoL wrapper: proven v3.5 behavior + v3.22 toggleable Exp. Share.

Runs the exact Build 249 QoL implementation first, then applies the next
confirmed project feature: one-time post-Pokedex Exp. Share with party-wide
Gen 6-style ON/OFF Key Item behavior. Species/content policy remains Gen I-V.
Ash Bond / Ash Cap remain untouched.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "cdce73eba8ca7c7b6c2ef12eca199e197abe2687"
BASE_PATH = "ci/qol_v3_5.py"
FOLLOWUP_PATH = "ci/exp_share_v3_22.py"


def load_from_git(repo: Path, commit: str, path: str, module_name: str) -> dict:
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", commit],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        text=True,
    )
    ns = {"__name__": module_name, "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{commit}:{path}", "exec"), ns)
    return ns


def load_followup(repo: Path) -> dict:
    path = repo / FOLLOWUP_PATH
    if not path.is_file():
        raise RuntimeError(f"missing Qarro Exp. Share follow-up: {path}")
    code = path.read_text(encoding="utf-8")
    ns = {"__name__": "qarro_exp_share_v322", "__file__": str(path.resolve())}
    exec(compile(code, str(path), "exec"), ns)
    return ns


def main() -> int:
    repo = Path(__file__).resolve().parents[1]

    base = load_from_git(repo, BASE_COMMIT, BASE_PATH, "qarro_qol_build249_baseline")
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    followup = load_followup(repo)
    rc = int(followup["main"]() or 0)
    if rc:
        return rc

    print(
        "[QARRO_QOL_V3_22] PASS: Build 249 QoL preserved; post-Pokedex toggleable "
        "party-wide Exp. Share added; Gen I-V content policy and Ash protections unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
