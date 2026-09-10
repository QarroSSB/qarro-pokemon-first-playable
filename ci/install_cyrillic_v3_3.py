#!/usr/bin/env python3
"""Targeted compact Cyrillic masks for font atlases that clip in CI.

Reuses the exact v3.3.3 per-font scaler from commit 6593ba7 and changes only
verified glyph source masks while an affected atlas is rendered. Full source
forms remain the reference everywhere else.

Normal-font, short-font and short-narrow CI chains are fully past all observed
compact-glyph blockers. Short-narrower chain:
- #131: short-narrow passed; Д overflow y=0..17
- #132: Д passed; Ё overflow y=-4..13
- #133: Ё passed; Й overflow y=-4..15
- #134: Й passed; Ц overflow y=0..17
- #135: Ц passed; Щ overflow y=0..17
- #136: Щ passed; б overflow y=-5..13
- #137: б passed; д overflow y=0..16
- #138: д passed; ё overflow y=-8..13
- #139: ё passed; й overflow y=-8..13
- #140: й passed; р overflow y=0..18
- #141: р passed; у overflow y=0..18
- #142: у passed; ф overflow y=-8..18
- #143: ф passed; ц overflow y=0..16
- #144: ц passed; щ overflow y=0..16
- #145: short-narrower passed; small Ё overflow y=-2..12
- #146: small Ё passed; Й overflow y=-2..14
- #147: small Й passed; б overflow y=-3..12
- #148: small б passed; ё overflow y=-6..12
- #149: small ё passed; й overflow y=-6..12
- #150: small й passed; р overflow y=1..16
- #151: small р passed; у overflow y=1..16
- #152: small у passed; ф overflow y=-6..16
- #153: small font passed; small-narrow Ё overflow y=-2..12
- #154: small-narrow Ё passed; Й overflow y=-2..14
- #155: small-narrow Й passed; б overflow y=-3..12
- #156: small-narrow б passed; ё overflow y=-6..12
- #157: small-narrow ё passed; й overflow y=-6..12
- #158: small-narrow й passed; р overflow y=1..16
- #159: small-narrow р passed; у overflow y=1..16
- #161: small-narrow у passed; ф overflow y=-6..16

The compact forms below already pass the smaller narrow atlases. Additional
atlases use them only after CI proves the full glyph clips. Fail-closed checks
remain active. English, unrelated Cyrillic glyphs, Ash Bond and Ash Cap are
untouched.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

BASE_COMMIT = "6593ba731a84d565b70d5e712a5ab7f0e01e90dd"
BASE_PATH = "ci/install_cyrillic_v3_3.py"

SPECIALS = {
    "Д": ("0000003c24242424247e4242", "0000003c2424247e42420000"),
    "Ё": ("0014003e20203e20203e0000", "000000143e20203e203e0000"),
    "Й": ("0028380026262e2a3a323200", "00000038262e2a3a32320000"),
    "Ц": ("0000004444444444447e0202", "00000044444444447e020000"),
    "Щ": ("0000005454545454547e0202", "00000054545454547e020000"),
    "б": ("0000001e303c2222221c0000", "0000000000001e3c221c0000"),
    "д": ("00000000003c2424247e4200", "00000000003c24247e420000"),
    "ё": ("00001400001c223e201e0000", "0000000000141c3e201e0000"),
    "й": ("0000283800242c2c34240000", "000000000028382c34240000"),
    "р": ("00000000003c2222223c2020", "0000000000003c223c200000"),
    "у": ("000000000022141408080830", "000000000000221408300000"),
    "ф": ("00000808081c2a2a2a1c0808", "0000000000081c2a1c080000"),
    "ц": ("0000000000242424243e0200", "00000000000024243e020000"),
    "щ": ("0000000000545454547e0200", "00000000000054547e020000"),
}


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
        "__name__": "qarro_cyrillic_v333_base",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    return ns


def main() -> int:
    ns = load_base()
    indices = {ch: ns["CYRILLIC"].index(ch) for ch in SPECIALS}
    for ch, (full, _) in SPECIALS.items():
        if ns["GLYPH_HEX"][indices[ch]] != full:
            raise RuntimeError(f"{ch} changed from verified v3.3.3 source")

    original_patch_font = ns["patch_font"]

    def patch_font_narrow_specials(path):
        if path.name == "latin_narrow.png":
            selected = SPECIALS
        elif path.name == "latin_narrower.png":
            selected = {
                "Д": (SPECIALS["Д"][0], "000000003c24247e42000000"),
                "Ё": (SPECIALS["Ё"][0], "0000000000143e203e000000"),
                "Й": (SPECIALS["Й"][0], "0000000038262e3a32000000"),
                "Ц": (SPECIALS["Ц"][0], "000000004444447e02000000"),
                "Щ": (SPECIALS["Щ"][0], "000000005454547e02000000"),
                "б": SPECIALS["б"],
                "д": SPECIALS["д"],
                "ё": SPECIALS["ё"],
                "й": SPECIALS["й"],
                "р": SPECIALS["р"],
                "у": SPECIALS["у"],
                "ф": SPECIALS["ф"],
                "ц": SPECIALS["ц"],
                "щ": SPECIALS["щ"],
            }
        elif path.name == "latin_normal.png":
            selected = {
                "Д": SPECIALS["Д"],
                "Ё": SPECIALS["Ё"],
                "Й": SPECIALS["Й"],
                "Ц": SPECIALS["Ц"],
                "Щ": SPECIALS["Щ"],
                "б": SPECIALS["б"],
                "д": SPECIALS["д"],
                "ё": SPECIALS["ё"],
                "й": SPECIALS["й"],
                "р": SPECIALS["р"],
                "у": SPECIALS["у"],
                "ф": SPECIALS["ф"],
                "ц": SPECIALS["ц"],
                "щ": SPECIALS["щ"],
            }
        elif path.name == "latin_short.png":
            selected = {
                "Д": SPECIALS["Д"],
                "Ё": SPECIALS["Ё"],
                "Й": SPECIALS["Й"],
                "Ц": SPECIALS["Ц"],
                "Щ": SPECIALS["Щ"],
                "б": SPECIALS["б"],
                "д": SPECIALS["д"],
                "ё": SPECIALS["ё"],
                "й": SPECIALS["й"],
                "р": SPECIALS["р"],
                "у": SPECIALS["у"],
                "ф": SPECIALS["ф"],
                "ц": SPECIALS["ц"],
                "щ": SPECIALS["щ"],
            }
        elif path.name == "latin_short_narrow.png":
            selected = {
                "Д": SPECIALS["Д"],
                "Ё": SPECIALS["Ё"],
                "Й": SPECIALS["Й"],
                "Ц": SPECIALS["Ц"],
                "Щ": SPECIALS["Щ"],
                "б": SPECIALS["б"],
                "д": SPECIALS["д"],
                "ё": SPECIALS["ё"],
                "й": SPECIALS["й"],
                "р": SPECIALS["р"],
                "у": SPECIALS["у"],
                "ф": SPECIALS["ф"],
                "ц": SPECIALS["ц"],
                "щ": SPECIALS["щ"],
            }
        elif path.name == "latin_short_narrower.png":
            selected = {
                "Д": (SPECIALS["Д"][0], "000000003c24247e42000000"),
                "Ё": (SPECIALS["Ё"][0], "0000000000143e203e000000"),
                "Й": (SPECIALS["Й"][0], "0000000038262e3a32000000"),
                "Ц": (SPECIALS["Ц"][0], "000000004444447e02000000"),
                "Щ": (SPECIALS["Щ"][0], "000000005454547e02000000"),
                "б": SPECIALS["б"],
                "д": SPECIALS["д"],
                "ё": SPECIALS["ё"],
                "й": SPECIALS["й"],
                "р": SPECIALS["р"],
                "у": SPECIALS["у"],
                "ф": SPECIALS["ф"],
                "ц": SPECIALS["ц"],
                "щ": SPECIALS["щ"],
            }
        elif path.name == "latin_small.png":
            selected = {
                "Ё": SPECIALS["Ё"],
                "Й": SPECIALS["Й"],
                "б": SPECIALS["б"],
                "ё": SPECIALS["ё"],
                "й": SPECIALS["й"],
                "р": SPECIALS["р"],
                "у": SPECIALS["у"],
                "ф": SPECIALS["ф"],
            }
        elif path.name == "latin_small_narrow.png":
            selected = {
                "Ё": SPECIALS["Ё"],
                "Й": SPECIALS["Й"],
                "б": SPECIALS["б"],
                "ё": SPECIALS["ё"],
                "й": SPECIALS["й"],
                "р": SPECIALS["р"],
                "у": SPECIALS["у"],
                "ф": SPECIALS["ф"],
            }
        else:
            return original_patch_font(path)

        selected_indices = {indices[ch] for ch in selected}
        saved = {
            idx: (ns["GLYPH_HEX"][idx], ns["SOURCE_BBOXES"][idx])
            for idx in selected_indices
        }
        try:
            for ch, (_, compact) in selected.items():
                idx = indices[ch]
                ns["GLYPH_HEX"][idx] = compact
                ns["SOURCE_BBOXES"][idx] = ns["source_bbox"](compact)
            print(f"[cyrillic-v3340] {path.name}: targeted compact Cyrillic masks enabled")
            return original_patch_font(path)
        finally:
            for idx, (old_hex, old_bbox) in saved.items():
                ns["GLYPH_HEX"][idx] = old_hex
                ns["SOURCE_BBOXES"][idx] = old_bbox

    ns["patch_font"] = patch_font_narrow_specials
    return int(ns["main"]() or 0)


if __name__ == "__main__":
    raise SystemExit(main())
