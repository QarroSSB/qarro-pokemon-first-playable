#!/usr/bin/env python3
"""Qarro balance wrapper: stable Build 255 Kanto balance + fixed v3.25 gym 5-of-6.

Preserves the proven Kanto levels / hard caps exactly, then applies the scoped
Gym Leader party-selection pass. Elite Four, Champion and postgame remain on
the native trainer-party path. Font, localization, Ash Bond and Ash Cap are not
touched here.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "158974c25113e5aef88e02af45059a97ef8209e8"
BASE_PATH = "ci/balance_kanto_v3_2.py"
GYM_PATH = "ci/gym_five_v3_25.py"


def load_git_module(repo: Path, commit: str, path: str, name: str) -> dict:
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", commit],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        text=True,
    )
    ns = {"__name__": name, "__file__": str(Path(__file__).resolve())}
    exec(compile(code, f"{commit}:{path}", "exec"), ns)
    return ns


def load_local(repo: Path, path: str, name: str) -> dict:
    source = repo / path
    if not source.is_file():
        raise RuntimeError(f"missing Qarro gym pass: {source}")
    code = source.read_text(encoding="utf-8")
    ns = {"__name__": name, "__file__": str(source.resolve())}
    exec(compile(code, str(source), "exec"), ns)
    return ns


def main() -> int:
    repo = Path(__file__).resolve().parents[1]

    baseline = load_git_module(repo, BASE_COMMIT, BASE_PATH, "qarro_balance_build255")
    rc = int(baseline["main"]() or 0)
    if rc:
        return rc

    gym = load_local(repo, GYM_PATH, "qarro_gym_five_v325_fixed")
    rc = int(gym["main"]() or 0)
    if rc:
        return rc

    print(
        "[QARRO_BALANCE_GYM_V3_25] PASS: stable Kanto balance/caps preserved; "
        "eight story Gym Leaders use deterministic save-stable 5-of-6 parties"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
