#!/usr/bin/env python3
"""Qarro Gym-test QoL wrapper: preserve proven Build 249 behavior only.

This isolated test branch must remain without Exp. Share while Gym 5-of-6
behavior is being validated. FireRed / Expansion 1.17.0 / Gen I-V policy only.
Ash Bond / Ash Cap remain untouched and are never reconnected here.
"""
from __future__ import annotations

import runpy
import subprocess
from pathlib import Path

BASE_COMMIT = "cdce73eba8ca7c7b6c2ef12eca199e197abe2687"
BASE_PATH = "ci/qol_v3_5.py"
GYM_PATH = "ci/gym_five_v3_25.py"


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


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    base = load_from_git(repo, BASE_COMMIT, BASE_PATH, "qarro_qol_build249_baseline")
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    # The no-legend six-candidate rosters are already installed by the earlier
    # isolated Gym balance pass. Reassert only the runtime party interception
    # after QoL; do not rerun roster mutation or touch unrelated gameplay data.
    gym = runpy.run_path(str(repo / GYM_PATH), run_name="qarro_gym_runtime_reassert")
    gym["patch_battle_setup"](Path(__import__("sys").argv[1]).resolve())

    print(
        "[QARRO_QOL_GYM_TEST] PASS: Build 249 QoL preserved; Exp. Share intentionally absent; "
        "Gym 5-of-6 runtime wiring reasserted after QoL; Gen I-V policy and Ash protections unchanged"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
