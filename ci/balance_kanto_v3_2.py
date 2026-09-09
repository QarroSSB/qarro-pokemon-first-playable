#!/usr/bin/env python3
"""Stable v3.2 test wrapper: 5-Pokemon gyms + party Exp Share.

Runs the exact verified production balance script from stable v3.2 commit
067927d9f34c638e72c152b1209809664a6a0d3a, then applies the isolated test
profile. Main is untouched. Ash Bond / Ash Cap are untouched.
"""
from __future__ import annotations

import importlib.util
import re
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


def enable_exp_share_after_pokedex(root: Path) -> Path:
    """Enable Expansion's native party-wide Exp Share after the Pokédex flag."""
    path = root / "include/config/item.h"
    if not path.exists():
        raise RuntimeError(f"missing {path}")
    text = path.read_text(encoding="utf-8")

    flag_pattern = re.compile(r"(?m)^(#define\s+I_EXP_SHARE_FLAG\s+)(\S+)(.*)$")
    flag_matches = list(flag_pattern.finditer(text))
    if len(flag_matches) != 1:
        raise RuntimeError(f"I_EXP_SHARE_FLAG: expected one define, found {len(flag_matches)}")
    current_flag = flag_matches[0].group(2)
    if current_flag == "0":
        text = flag_pattern.sub(
            lambda m: f"{m.group(1)}FLAG_SYS_POKEDEX_GET{m.group(3)}",
            text,
            count=1,
        )
    elif current_flag != "FLAG_SYS_POKEDEX_GET":
        raise RuntimeError(
            f"I_EXP_SHARE_FLAG: expected 0 or FLAG_SYS_POKEDEX_GET, got {current_flag}"
        )

    item_pattern = re.compile(r"(?m)^#define\s+I_EXP_SHARE_ITEM\s+(\S+).*$")
    item_matches = list(item_pattern.finditer(text))
    if len(item_matches) != 1 or item_matches[0].group(1) != "GEN_5":
        observed = [m.group(1) for m in item_matches]
        raise RuntimeError(f"I_EXP_SHARE_ITEM: expected exactly GEN_5, got {observed}")

    path.write_text(text, encoding="utf-8")
    print(
        "[exp-share-test] native party Exp Share activates after Pokedex via "
        "I_EXP_SHARE_FLAG=FLAG_SYS_POKEDEX_GET; item mode remains GEN_5"
    )
    return path


def main() -> int:
    ns = load_base()
    rc = int(ns["main"]() or 0)
    if rc != 0:
        return rc

    test_module = load_test_module()
    test_module.force_gen6_exp_share = enable_exp_share_after_pokedex
    rc = int(test_module.main() or 0)
    if rc == 0:
        print(
            "[QARRO_TEST_WRAPPER] PASS: stable v3.2 + native 5-of-6 no-legend gyms "
            "+ party Exp Share after Pokedex"
        )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
