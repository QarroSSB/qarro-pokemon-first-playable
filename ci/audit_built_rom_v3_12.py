#!/usr/bin/env python3
"""Post-build integrity gate for the Qarro FireRed artifact.

Read-only: verifies the produced ROM is a plausible 32 MiB FireRed BPRE image,
its recorded SHA-256 matches the actual bytes, and all prerequisite regression
reports that gated the build are present. No gameplay/source data is modified;
Ash Bond and Ash Cap are not touched.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

MARKER = "QARRO_BUILT_ROM_V3_12"
ROM_NAME = "Qarro_FIRST_PLAYABLE_v3_8.gba"
SHA_NAME = ROM_NAME + ".sha256"
REQUIRED_AUDITS = {
    "qarro_qol_regression_v3_10_audit.json": "QARRO_QOL_REGRESSION_V3_10",
    "qarro_regression_bundle_v3_11_audit.json": "QARRO_REGRESSION_BUNDLE_V3_11",
    "qarro_protected_features_v3_13_audit.json": "QARRO_PROTECTED_FEATURES_V3_13",
}
RU_AUDIT = "qarro_ru_foundation_v3_9_audit.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict:
    require(path.is_file(), f"missing required audit evidence: {path.name}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"invalid audit evidence: {path.name}") from exc
    require(isinstance(data, dict), f"unexpected audit root: {path.name}")
    return data


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <ci-output-dir>", file=sys.stderr)
        return 2

    out = Path(sys.argv[1]).resolve()
    rom_path = out / ROM_NAME
    sha_path = out / SHA_NAME
    require(rom_path.is_file(), f"missing built ROM: {rom_path}")
    require(sha_path.is_file(), f"missing ROM checksum: {sha_path}")

    rom = rom_path.read_bytes()
    require(len(rom) == 32 * 1024 * 1024, f"unexpected ROM size: {len(rom)}")
    require(len(rom) >= 0xB0, "ROM too small for GBA header")
    game_code = rom[0xAC:0xB0].decode("ascii", errors="replace")
    require(game_code == "BPRE", f"unexpected GBA game code: {game_code!r}")

    actual_sha = hashlib.sha256(rom).hexdigest()
    sha_tokens = sha_path.read_text(encoding="ascii").strip().split()
    require(bool(sha_tokens), "empty ROM checksum file")
    require(sha_tokens[0].lower() == actual_sha, "ROM SHA-256 mismatch")

    for name, marker in REQUIRED_AUDITS.items():
        data = load_json(out / name)
        require(data.get("marker") == marker, f"audit marker drift: {name}")

    ru = load_json(out / RU_AUDIT)
    policy = ru.get("policy", "")
    require("FireRed" in policy and "Expansion 1.17.0" in policy and "Gen I-V" in policy,
            "RU policy evidence drift")

    report = {
        "marker": MARKER,
        "rom": ROM_NAME,
        "sizeBytes": len(rom),
        "gameCode": game_code,
        "sha256": actual_sha,
        "requiredAuditEvidence": sorted([*REQUIRED_AUDITS, RU_AUDIT]),
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    report_path = out / "qarro_built_rom_v3_12_audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: 32 MiB BPRE ROM + SHA-256 + regression evidence verified")
    print(f"audit: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
