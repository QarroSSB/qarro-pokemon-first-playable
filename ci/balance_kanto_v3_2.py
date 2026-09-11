#!/usr/bin/env python3
"""Qarro Kanto balance wrapper + persistent 5-of-6 Gym Leader battles.

Runs the exact green balance/cap implementation from the last pre-gym baseline,
then applies v3.24: each of the eight Kanto Gym Leaders keeps six prepared mons
but battles with one save-stable five-mon subset. Elite Four / Champion /
postgame remain on the native 6v6 path. Frozen font/localization and Ash code
are untouched.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "158974c25113e5aef88e02af45059a97ef8209e8"
BASE_PATH = "ci/balance_kanto_v3_2.py"
FOLLOWUP_PATH = "ci/gym_five_v3_24.py"


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
        raise RuntimeError(f"missing gym follow-up: {path}")
    code = path.read_text(encoding="utf-8")
    ns = {"__name__": "qarro_gym_five_v324", "__file__": str(path.resolve())}
    exec(compile(code, str(path), "exec"), ns)
    return ns


def main() -> int:
    repo = Path(__file__).resolve().parents[1]

    base = load_from_git(repo, BASE_COMMIT, BASE_PATH, "qarro_balance_pre_gym_baseline")
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    followup = load_followup(repo)
    rc = int(followup["main"]() or 0)
    if rc:
        return rc

    print(
        "[QARRO_BALANCE_GYM_V3_24] PASS: prior Kanto balance/caps preserved; "
        "eight Leaders now use persistent 5-of-6 parties; non-gym boss paths unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
