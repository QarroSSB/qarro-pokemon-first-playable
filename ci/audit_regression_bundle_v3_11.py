#!/usr/bin/env python3
"""Read-only consolidated regression gate for the Qarro FireRed build.

Runs after the existing QoL and RU foundation audits. It verifies that their
machine-readable reports exist and still encode the confirmed user policy:
FireRed / Expansion 1.17.0 / Gen I-V, readable Cyrillic coverage, no money
loss on defeat, failed-catch Ball refund only, and the one-time post-Pokedex
starter kit. It changes no gameplay data and does not touch Ash Bond/Cap.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_REGRESSION_BUNDLE_V3_11"


def load(path: Path) -> dict:
    if not path.is_file():
        raise RuntimeError(f"missing prerequisite audit: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"invalid prerequisite audit: {path}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"unexpected audit root type: {path}")
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    build = root / "build"
    qol = load(build / "qarro_qol_regression_v3_10_audit.json")
    ru = load(build / "qarro_ru_foundation_v3_9_audit.json")

    require(qol.get("marker") == "QARRO_QOL_REGRESSION_V3_10", "QoL audit marker drift")
    money = qol.get("money", {})
    catch = qol.get("failedCatchBall", {})
    kit = qol.get("starterKit", {})
    require(money.get("removeMoneyCalls") == 0, "defeat money regression")
    require(money.get("winRewardPreserved") is True, "trainer win reward regression")
    require(catch.get("refundCalls") == 1, "failed-catch Ball refund count regression")
    require(catch.get("refundAfterSuccessfulCaptureReturn") is True, "Ball refund path regression")
    require(catch.get("successStillConsumesBall") is True, "successful catch consumption regression")
    require(catch.get("safariExcluded") is True, "Safari Ball path regression")
    require(kit.get("oneTimeSceneGuard") is True, "starter kit one-time guard regression")
    require(kit.get("pokeBallsTotal") == 20, "starter Poké Ball total regression")
    require(kit.get("potions") == 10, "starter Potion total regression")
    require(kit.get("antidotes") == 5, "starter Antidote total regression")
    require(kit.get("paralyzeHeals") == 5, "starter Paralyze Heal total regression")
    require(kit.get("duplicateNewGameGrant") is False, "duplicate starter grant regression")
    require(qol.get("ashBondTouched") is False and qol.get("ashCapTouched") is False,
            "Ash invariant regression in QoL audit")

    policy = ru.get("policy", "")
    require("FireRed" in policy and "Expansion 1.17.0" in policy and "Gen I-V" in policy,
            "RU foundation policy drift")
    require(ru.get("cyrillic_glyph_count", 0) >= 66, "Cyrillic charmap coverage regression")
    fonts = ru.get("fonts", {})
    require(len(fonts) == 9, "FireRed font-atlas coverage regression")
    for name, stats in fonts.items():
        require(stats.get("cyrillic_nonempty", 0) >= 66, f"Cyrillic glyph regression in {name}")
        require(stats.get("min_ink_pixels", 0) > 0, f"empty Cyrillic ink regression in {name}")
    text = ru.get("text", {})
    require(text.get("files_with_cyrillic", 0) >= 4, "Russian localization file-count regression")
    require(text.get("cyrillic_characters", 0) >= 100, "Russian localization character-count regression")
    require(text.get("accented_e_file_count") == 0, "accented-e normalization regression")

    report = {
        "marker": MARKER,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V",
        "qolRegression": "PASS",
        "ruFoundation": "PASS",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = build / "qarro_regression_bundle_v3_11_audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # The workflow artifact already uploads qarro_ci_out_v3_8/**. Mirror the
    # read-only audit evidence there when running in CI so a GREEN ROM carries
    # the exact QoL/RU regression proof that gated it. Outside CI this is a no-op.
    ci_out = root.parent / "qarro_ci_out_v3_8"
    if ci_out.is_dir():
        for name in (
            "qarro_qol_regression_v3_10_audit.json",
            "qarro_ru_foundation_v3_9_audit.json",
            "qarro_regression_bundle_v3_11_audit.json",
        ):
            src = build / name
            if not src.is_file():
                raise RuntimeError(f"missing audit evidence for artifact: {src}")
            (ci_out / name).write_bytes(src.read_bytes())
        print(f"[{MARKER}] preserved 3 regression audit reports in {ci_out}")

    print(f"[{MARKER}] PASS: QoL + RU foundation policies remain internally consistent")
    print(f"audit: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
