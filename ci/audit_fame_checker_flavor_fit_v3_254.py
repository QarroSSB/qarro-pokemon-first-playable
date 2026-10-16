#!/usr/bin/env python3
"""Qarro v3.254: targeted Fame Checker flavor fit-risk QA.

The three longest hand-edited flavor lines exceeded 36 Unicode characters.
Shorten only those three exact installed surfaces while preserving all
FireRed text-control tokens and the meaning of the source. Then inventory
all 96 flavor entries for long unbroken display lines.

The 36-character threshold is a *conservative triage heuristic*, NOT a
pixel-accurate font or in-emulator layout proof. Visual QA remains required.

Text only; no gameplay, balance, Gym policy, Ash Bond or Ash Cap changes.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_FLAVOR_FIT_QA_V3_254"
TARGET = Path("data/text/fame_checker_frlg.inc")
PERSONS = (
    "ProfOak", "Daisy", "Brock", "Misty", "LtSurge", "Erika", "Koga",
    "Sabrina", "Blaine", "Lorelei", "Bruno", "Agatha", "Lance",
    "Bill", "MrFuji", "Giovanni",
)
MAX_DISPLAY_CHARACTERS = 36

EXPECTED = {
    "gFameCheckerFlavorText_Sabrina1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Знаешь девушку-ЛИДЕРА ГИМА\nиз САФФРОНА?\pОна использует ПСИХИЧЕСКИХ ПОКЕМОНОВ,\nверно?$",
    "gFameCheckerFlavorText_Sabrina3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я не люблю сражаться, но если хочешь,\nпокажу тебе свою силу!$",
    "gFameCheckerFlavorText_MrFuji1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Этот старик сам пришёл прямо\nк нашему УБЕЖИЩУ.\pА потом начал возмущаться, что\nКОМАНДА R плохо обращается с ПОКЕМОНАМИ.\pВот мы и обсуждаем это,\nкак взрослые.$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorText_Sabrina1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Знаешь девушку-ЛИДЕРА ГИМА\nиз САФФРОНА?\pУ неё ПОКЕМОНЫ ПСИХИЧЕСКОГО ТИПА,\nверно?$",
    "gFameCheckerFlavorText_Sabrina3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Не люблю бои, но раз ты хочешь,\nпокажу тебе свою силу!$",
    "gFameCheckerFlavorText_MrFuji1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Этот старик сам пришёл прямо\nк нашему УБЕЖИЩУ.\pА потом начал возмущаться, что\nКОМАНДА R мучает ПОКЕМОНОВ.\pВот мы и обсуждаем это,\nкак взрослые.$",
}

BANNED_UNICODE = set("—–←→“”«»…")


def controls(body: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", body)


def find_entry(text: str, label: str) -> re.Match[str]:
    pattern = re.compile(
        rf'(?m)^(?P<label>{re.escape(label)}::[^\n]*\n)'
        rf'(?P<prefix>\s*\.string ")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\s*)$'
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected exactly one text entry, got {len(matches)}")
    return matches[0]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <upstream-root>")
    if set(EXPECTED) != set(TRANSLATIONS) or len(EXPECTED) != 3:
        raise RuntimeError("unexpected v3.254 targeted QA set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")
    text = path.read_text(encoding="utf-8")
    for label, old in EXPECTED.items():
        new = TRANSLATIONS[label]
        if controls(old) != controls(new):
            raise RuntimeError(f"{label}: control-token drift")
        match = find_entry(text, label)
        if match.group("body") not in (old, new):
            raise RuntimeError(f"{label}: unexpected installed text (fail closed)")
        if match.group("body") != new:
            replacement = match.group("label") + match.group("prefix") + new + match.group("suffix")
            text = text[:match.start()] + replacement + text[match.end():]

    expected_labels = {f"gFameCheckerFlavorText_{person}{idx}"
                       for person in PERSONS for idx in range(6)}
    if len(expected_labels) != 96:
        raise RuntimeError("unexpected flavor inventory cardinality")

    lengths = []
    for label in sorted(expected_labels):
        body = find_entry(text, label).group("body")
        if not body.endswith("$") or "$" in body[:-1]:
            raise RuntimeError(f"{label}: invalid terminator")
        if set(body) & BANNED_UNICODE:
            raise RuntimeError(f"{label}: unsupported Unicode surface")
        if not re.search(r"[А-Яа-яЁё]", body):
            raise RuntimeError(f"{label}: expected Cyrillic flavor text")
        if re.search(r"\\(?![npl])", re.sub(r"\{[^}]+\}", "", body)):
            raise RuntimeError(f"{label}: unexpected text escape")
        visible = re.sub(r"\{[^}]+\}", "", body).removesuffix("$")
        for line in re.split(r"\\[npl]", visible):
            if len(line) > MAX_DISPLAY_CHARACTERS:
                raise RuntimeError(
                    f"{label}: long-line risk {len(line)} > {MAX_DISPLAY_CHARACTERS}: {line!r}"
                )
            lengths.append({"label": label, "characters": len(line), "line": line})

    for label, new in TRANSLATIONS.items():
        if find_entry(text, label).group("body") != new:
            raise RuntimeError(f"{label}: post-rewrite mismatch")
    path.write_text(text, encoding="utf-8")

    longest = sorted(lengths, key=lambda item: item["characters"], reverse=True)[:12]
    report = {
        "marker": MARKER,
        "targetFile": str(TARGET),
        "targetedRewrites": len(TRANSLATIONS),
        "flavorEntriesAudited": len(expected_labels),
        "displayLinesAudited": len(lengths),
        "maximumLineCharacters": max(item["characters"] for item in lengths),
        "heuristicLimit": MAX_DISPLAY_CHARACTERS,
        "pixelAccurateOrEmulatorVisualProof": False,
        "visualQAStillRequired": True,
        "controlTokensPreserved": True,
        "exactSourceAnchors": True,
        "postTranslationSurfacesVerified": True,
        "longestLines": longest,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "gymPolicyTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build" / "qarro_ru_fame_checker_flavor_fit_v3_254_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: {len(TRANSLATIONS)} targeted line edits, "
        f"{len(expected_labels)} flavor entries, {len(lengths)} display lines; "
        "pixel/emulator visual QA still required"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
