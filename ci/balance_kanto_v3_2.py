#!/usr/bin/env python3
"""Test-branch wrapper around the verified v3.2 balance pass.

Runs the exact production balance script from commit
27383446e2489ede5699ecfb99d5312545b36d85, then applies the isolated
5-Pokemon-gym + always-on Gen VI party Exp Share test profile.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "27383446e2489ede5699ecfb99d5312545b36d85"
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
        "__name__": "qarro_balance_v32_base",
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
        print("[QARRO_TEST_WRAPPER] PASS: production v3.2 balance + gym5/Exp Share test profile")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
