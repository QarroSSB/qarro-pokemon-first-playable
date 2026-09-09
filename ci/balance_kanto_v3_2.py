#!/usr/bin/env python3
"""Stable v3.2 test wrapper: 5-Pokemon gyms + party Exp Share.

Runs the exact verified production balance script from stable v3.2 commit
067927d9f34c638e72c152b1209809664a6a0d3a, then applies the isolated test
profile. Main is untouched. Ash Bond / Ash Cap are untouched.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "067927d9f34c638e72c152b1209809664a6a0d3a"
BASE_PATH = "ci/balance_kanto_v3_2.py"


def load_base() -> dict:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )
    ns = {
        "__name__": "qarro_balance_v32_stable_base",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    return ns


def load_test_module():
    path = Path(__file__).with_name("test_gym5_exp_share.py")
    spec = importlib.util.spec_from_file_location("qarro_test_gym5_exp_share", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ns = load_base()
    rc = int(ns["main"]() or 0)
    if rc != 0:
        return rc
    test_module = load_test_module()
    rc = int(test_module.main() or 0)
    if rc == 0:
        print("[QARRO_TEST_WRAPPER] PASS: stable v3.2 + 5-mon gyms + party Exp Share")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
