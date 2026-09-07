#!/usr/bin/env python3
"""Qarro v3.1 content-pass bootstrap.

This keeps the exact content pass from commit 656937d975e48a6a559ff3e06f79b70b1c6fbf2f,
while removing the two .party lines that CPP interpreted as invalid # directives.
No gameplay/content changes beyond that first observed build error are made here.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "656937d975e48a6a559ff3e06f79b70b1c6fbf2f"
BASE_PATH = "ci/content_pass_v3_1.py"


def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )
    # FIRST REAL v3.1 ERROR (run #12): arm-none-eabi-cpp treated these
    # marker lines as preprocessing directives in trainers_frlg.party.
    code = code.replace("# QARRO_CONTENT_V3_1_TRAINERS_BEGIN\n", "")
    code = code.replace("# QARRO_CONTENT_V3_1_TRAINERS_END\n", "")
    return code


def main() -> int:
    code = load_base()
    ns = {
        "__name__": "qarro_content_v31_base",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = ns["main"]()
    return int(rc or 0)


if __name__ == "__main__":
    raise SystemExit(main())
