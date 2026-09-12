#!/usr/bin/env python3
"""Post-build integrity gate for the Qarro FireRed artifact.

Read-only: verifies the produced ROM is a plausible 32 MiB FireRed BPRE image,
its recorded SHA-256 matches the actual bytes, all prerequisite regression
reports are present, and the RU+EN font/localization foundation evidence is
actually healthy rather than merely present. No gameplay/source data is
modified; Ash Bond and Ash Cap are never touched.
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
    "qarro_ground_items_v3_23_audit.json": "QARRO_GROUND_ITEMS_V3_23",
    "qarro_regression_bundle_v3_11_audit.json": "QARRO_REGRESSION_BUNDLE_V3_11",
    "qarro_protected_features_v3_13_audit.json": "QARRO_PROTECTED_FEATURES_V3_13",
}
RU_AUDIT = "qarro_ru_foundation_v3_9_audit.json"
EXPECTED_FONT_ATLASES = {
    "latin_small_narrow.png",
    "latin_small.png",
    "latin_normal.png",
    "latin_short.png",
    "latin_narrow.png",
    "latin_narrower.png",
    "latin_small_narrower.png",
    "latin_short_narrow.png",
    "latin_short_narrower.png",
}
EXPECTED_EARLY_MARKERS = {"Привет", "ПОКЕМОН", "ПАЛЛЕТ", "ОУК", "МАМА", "Пора идти"}
EXPECTED_CYRILLIC_GLYPHS = 66


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


def verify_ru_foundation(ru: dict) -> dict:
    policy = ru.get("policy", "")
    require(
        "FireRed" in policy and "Expansion 1.17.0" in policy and "Gen I-V" in policy,
        "RU policy evidence drift",
    )
    require(
        ru.get("cyrillic_glyph_count") == EXPECTED_CYRILLIC_GLYPHS,
        f"unexpected Cyrillic glyph count: {ru.get('cyrillic_glyph_count')!r}",
    )

    fonts = ru.get("fonts")
    require(isinstance(fonts, dict), "missing RU font-atlas evidence")
    require(set(fonts) == EXPECTED_FONT_ATLASES, "RU font-atlas set drift")
    for name in sorted(EXPECTED_FONT_ATLASES):
        evidence = fonts.get(name)
        require(isinstance(evidence, dict), f"invalid font evidence: {name}")
        require(
            evidence.get("cyrillic_nonempty") == EXPECTED_CYRILLIC_GLYPHS,
            f"{name}: not all Cyrillic glyphs are non-empty",
        )
        require(
            evidence.get("advance_raster_matches") == EXPECTED_CYRILLIC_GLYPHS,
            f"{name}: raster/advance mismatch evidence",
        )
        require(int(evidence.get("min_ink_pixels", 0)) > 0, f"{name}: empty glyph ink evidence")
        require(4 <= int(evidence.get("min_advance", 0)) <= 16, f"{name}: invalid min advance")
        require(4 <= int(evidence.get("max_advance", 99)) <= 16, f"{name}: invalid max advance")

    text = ru.get("text")
    require(isinstance(text, dict), "missing Russian text audit evidence")
    require(int(text.get("scanned_text_files", 0)) >= 1000, "RU audit scanned too few text files")
    require(int(text.get("files_with_cyrillic", 0)) >= 10, "Russian localization coverage unexpectedly sparse")
    require(int(text.get("cyrillic_characters", 0)) >= 5000, "Russian localization character count unexpectedly sparse")

    hits = text.get("early_marker_hits")
    require(isinstance(hits, dict), "missing early-game Russian marker evidence")
    require(EXPECTED_EARLY_MARKERS.issubset(hits), "early-game Russian marker set drift")
    for marker in EXPECTED_EARLY_MARKERS:
        require(int(hits.get(marker, 0)) > 0, f"missing localized early-game marker: {marker}")

    require(int(text.get("accented_e_file_count", -1)) == 0, "unsupported accented-e remains in source text")
    require(text.get("files_still_containing_accented_e") == [], "accented-e file list is not empty")

    return {
        "cyrillicGlyphs": EXPECTED_CYRILLIC_GLYPHS,
        "fontAtlases": len(EXPECTED_FONT_ATLASES),
        "scannedTextFiles": int(text["scanned_text_files"]),
        "filesWithCyrillic": int(text["files_with_cyrillic"]),
        "cyrillicCharacters": int(text["cyrillic_characters"]),
        "earlyMarkers": len(EXPECTED_EARLY_MARKERS),
        "accentedEFiles": 0,
    }


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

    ru_summary = verify_ru_foundation(load_json(out / RU_AUDIT))

    report = {
        "marker": MARKER,
        "rom": ROM_NAME,
        "sizeBytes": len(rom),
        "gameCode": game_code,
        "sha256": actual_sha,
        "requiredAuditEvidence": sorted([*REQUIRED_AUDITS, RU_AUDIT]),
        "ruFoundation": ru_summary,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    report_path = out / "qarro_built_rom_v3_12_audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: 32 MiB BPRE ROM + SHA-256 + regression evidence + "
        f"{ru_summary['cyrillicGlyphs']} Cyrillic glyphs across {ru_summary['fontAtlases']} font atlases + "
        f"Russian text coverage verified"
    )
    print(f"audit: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
