#!/usr/bin/env python3
"""Normalize literal accented e in game text after localization.

User choice: do not use a dedicated é glyph. Convert source text é/É to e/E
only after all localization passes have completed, so exact English anchors
used by the localization scripts remain valid during their own execution.

This pass also applies the next evidence-driven Russian runtime increment:
Brock's mandatory Pewter Gym intro and badge-victory dialogue. The exact pinned
FireRed source blocks are required. A prior localization pass may already have
normalized literal é/É to e/E, so each Brock anchor accepts exactly one of the
pinned source block or its mechanically normalized equivalent and otherwise
fails closed.

Charmap/font tables are deliberately excluded; the legacy FireRed slot stays
untouched but no authored game text should reference it after this pass.
After normalization, run the read-only RU font/localization foundation audit,
consolidated QoL/RU regression bundle, and protected Ash feature guard.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_NORMALIZE_E_V3_8"
ROOTS = ("data", "src", "include")
SUFFIXES = {".c", ".h", ".inc", ".s"}

BROCK_FILE = "data/maps/PewterCity_Gym_Frlg/scripts.inc"
BROCK_PATCHES = (
    (
        "PewterCity_Gym_Text_BrockIntro",
        '''PewterCity_Gym_Text_BrockIntro::
\t.string "So, you're here. I'm BROCK.\\n"
\t.string "I'm PEWTER's GYM LEADER.\\p"
\t.string "My rock-hard willpower is evident\\n"
\t.string "even in my POKéMON.\\p"
\t.string "My POKéMON are all rock hard, and\\n"
\t.string "have true-grit determination.\\p"
\t.string "That's right - my POKéMON are all\\n"
\t.string "the ROCK type!\\p"
\t.string "Fuhaha! You're going to challenge\\n"
\t.string "me knowing that you'll lose?\\p"
\t.string "That's the TRAINER's honor that\\n"
\t.string "compels you to challenge me.\\p"
\t.string "Fine, then!\\n"
\t.string "Show me your best!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$"''',
        '''PewterCity_Gym_Text_BrockIntro::
\t.string "Итак, ты пришёл.\\n"
\t.string "Я БРОК, ЛИДЕР ГИМА ПЬЮТЕРА.\\p"
\t.string "Моя воля крепка, как скала,\\n"
\t.string "и это видно по ПОКЕМОНАМ.\\p"
\t.string "Мои ПОКЕМОНЫ стойкие\\n"
\t.string "и полны решимости.\\p"
\t.string "Верно - все мои ПОКЕМОНЫ\\n"
\t.string "относятся к типу ROCK!\\p"
\t.string "Ха-ха! Ты бросаешь мне вызов,\\n"
\t.string "хотя знаешь, что проиграешь?\\p"
\t.string "Такова честь ТРЕНЕРА -\\n"
\t.string "всегда принимать вызов.\\p"
\t.string "Ну что ж!\\n"
\t.string "Покажи всё, на что способен!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$"''',
    ),
    (
        "PewterCity_Gym_Text_BrockDefeat",
        '''PewterCity_Gym_Text_BrockDefeat::
\t.string "I took you for granted, and so\\n"
\t.string "I lost.\\p"
\t.string "As proof of your victory, I confer\\n"
\t.string "on you this…the official POKéMON\\l"
\t.string "LEAGUE BOULDERBADGE.\\p"
\t.string "{FONT_NORMAL}{PLAYER} received the BOULDERBADGE\\n"
\t.string "from BROCK!{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}\\p"
\t.string "{FONT_MALE}Just having the BOULDERBADGE makes\\n"
\t.string "your POKéMON more powerful.\\p"
\t.string "It also enables the use of the\\n"
\t.string "move FLASH outside of battle.\\p"
\t.string "Of course, a POKéMON must know the\\n"
\t.string "move FLASH to use it.$"''',
        '''PewterCity_Gym_Text_BrockDefeat::
\t.string "Я недооценил тебя,\\n"
\t.string "поэтому и проиграл.\\p"
\t.string "В знак твоей победы\\n"
\t.string "вручаю тебе официальный\\l"
\t.string "ЗНАЧОК БУЛДЕРА ЛИГИ.\\p"
\t.string "{FONT_NORMAL}{PLAYER} получил ЗНАЧОК БУЛДЕРА\\n"
\t.string "от БРОКА!{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}\\p"
\t.string "{FONT_MALE}ЗНАЧОК БУЛДЕРА сделает\\n"
\t.string "твоих ПОКЕМОНОВ сильнее.\\p"
\t.string "Он также позволяет применять\\n"
\t.string "FLASH вне боя.\\p"
\t.string "Но ПОКЕМОН должен знать\\n"
\t.string "атаку FLASH, чтобы её применять.$"''',
    ),
)


def apply_brock_runtime_localization(root: Path) -> list[str]:
    path = root / BROCK_FILE
    if not path.is_file():
        raise RuntimeError(f"missing Brock runtime source: {path}")
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []
    for label, old, new in BROCK_PATCHES:
        if new in text:
            applied.append(f"{label}:already")
            continue

        normalized_old = old.replace("é", "e").replace("É", "E")
        candidates = [old]
        if normalized_old != old:
            candidates.append(normalized_old)
        matches = [(candidate, text.count(candidate)) for candidate in candidates]
        total = sum(count for _, count in matches)
        if total != 1:
            raise RuntimeError(
                f"{label}: expected exactly one pinned English block or normalized equivalent, "
                f"found {total} ({[count for _, count in matches]})"
            )
        matched = next(candidate for candidate, count in matches if count == 1)
        text = text.replace(matched, new, 1)
        applied.append(f"{label}:applied")
    path.write_text(text, encoding="utf-8")
    return applied


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    brock_localization = apply_brock_runtime_localization(root)
    changed_files: list[str] = []
    replaced = 0

    for dirname in ROOTS:
        base = root / dirname
        if not base.exists():
            raise RuntimeError(f"missing source root: {base}")
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            count = text.count("é") + text.count("É")
            if not count:
                continue
            new = text.replace("é", "e").replace("É", "E")
            path.write_text(new, encoding="utf-8")
            changed_files.append(str(path.relative_to(root)))
            replaced += count

    remaining: list[str] = []
    for dirname in ROOTS:
        base = root / dirname
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "é" in text or "É" in text:
                remaining.append(str(path.relative_to(root)))

    if remaining:
        raise RuntimeError(f"accented e remained in authored source: {remaining[:20]}")

    audit = {
        "marker": MARKER,
        "replacement": "é/É -> e/E",
        "replacements": replaced,
        "changedFiles": len(changed_files),
        "sampleFiles": changed_files[:50],
        "runtimeLocalizationIncrement": {
            "file": BROCK_FILE,
            "labels": brock_localization,
            "blocks": len(BROCK_PATCHES),
        },
        "charmapTouched": False,
        "fontTablesTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_normalize_e_v3_8_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: localized {len(BROCK_PATCHES)} verified Brock runtime blocks; "
        f"normalized {replaced} accented-e literals in {len(changed_files)} authored source files; "
        "charmap/font/Ash untouched"
    )

    here = Path(__file__).resolve().parent
    ru_audit = here / "audit_ru_foundation_v3_9.py"
    if not ru_audit.is_file():
        raise RuntimeError(f"missing RU foundation audit: {ru_audit}")
    subprocess.run([sys.executable, str(ru_audit), str(root)], check=True)

    bundle_audit = here / "audit_regression_bundle_v3_11.py"
    if not bundle_audit.is_file():
        raise RuntimeError(f"missing consolidated regression audit: {bundle_audit}")
    subprocess.run([sys.executable, str(bundle_audit), str(root)], check=True)

    protected_audit = here / "audit_protected_features_v3_13.py"
    if not protected_audit.is_file():
        raise RuntimeError(f"missing protected-feature audit: {protected_audit}")
    subprocess.run([sys.executable, str(protected_audit), str(root)], check=True)

    protected_report = root / "build/qarro_protected_features_v3_13_audit.json"
    if not protected_report.is_file():
        raise RuntimeError(f"protected-feature audit did not produce evidence: {protected_report}")
    ci_out = root.parent / "qarro_ci_out_v3_8"
    if ci_out.is_dir():
        (ci_out / protected_report.name).write_bytes(protected_report.read_bytes())
        print(f"[{MARKER}] preserved protected-feature audit in {ci_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
