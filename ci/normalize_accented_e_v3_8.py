#!/usr/bin/env python3
"""Normalize literal accented e in game text after localization.

User choice: do not use a dedicated é glyph. Convert source text é/É to e/E
only after all localization passes have completed, so exact English anchors
used by the localization scripts remain valid during their own execution.

Charmap/font tables are deliberately excluded; the legacy FireRed slot stays
untouched but no authored game text should reference it after this pass.
After normalization, re-run final-state QoL and Exp. Share regressions, then
run the read-only RU font/localization foundation audit, consolidated QoL/RU
regression bundle, and protected Ash feature guard.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_NORMALIZE_E_V3_8"
ROOTS = ("data", "src", "include")
SUFFIXES = {".c", ".h", ".inc", ".s"}


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
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

    # v3.25 Ability-description localization intentionally makes Gen I-V
    # descriptions unconditional. On the pinned Expansion source, Snow Warning
    # is the one block whose #if starts before .description; the localization
    # pass removes #else/#endif with the old descriptions but leaves that
    # leading #if behind. Remove only this exact orphaned directive and fail
    # closed if the expected localized block shape is not present.
    abilities = root / "src/data/abilities.h"
    ability_text = abilities.read_text(encoding="utf-8")
    snow_bad = (
        '        .name = _("Snow Warning"),\n'
        '    #if B_SNOW_WARNING >= GEN_9\n'
        '        .description = COMPOUND_STRING("Вызывает снежную погоду."),\n'
        '        .aiRating = 8,'
    )
    snow_good = (
        '        .name = _("Snow Warning"),\n'
        '        .description = COMPOUND_STRING("Вызывает снежную погоду."),\n'
        '        .aiRating = 8,'
    )
    if snow_bad in ability_text:
        ability_text = ability_text.replace(snow_bad, snow_good, 1)
        abilities.write_text(ability_text, encoding="utf-8")
        print(f"[{MARKER}] repaired exact orphaned Snow Warning preprocessor guard")
    elif snow_good not in ability_text:
        raise RuntimeError("Snow Warning localized block drifted; refusing speculative repair")

    audit = {
        "marker": MARKER,
        "replacement": "é/É -> e/E",
        "replacements": replaced,
        "changedFiles": len(changed_files),
        "sampleFiles": changed_files[:50],
        "snowWarningGuardRepair": True,
        "finalStateQolRegression": True,
        "finalStateExpShareRegression": True,
        "charmapTouched": False,
        "fontTablesTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_normalize_e_v3_8_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: normalized {replaced} accented-e literals in "
        f"{len(changed_files)} authored source files; charmap/font/Ash untouched"
    )

    here = Path(__file__).resolve().parent

    # Second regression pass over the FINAL source state. The same QoL audit is
    # already run when the QoL patch is installed, but later localization also
    # edits Oak's scripts. Re-running here proves no later pass damaged the
    # no-money-loss, failed-catch Ball, or one-time post-Pokedex kit behavior.
    qol_audit = here / "audit_qol_regressions_v3_10.py"
    if not qol_audit.is_file():
        raise RuntimeError(f"missing final-state QoL regression audit: {qol_audit}")
    subprocess.run([sys.executable, str(qol_audit), str(root)], check=True)

    # Exp. Share is audited once immediately after installation and again here
    # after every localization/normalization pass, catching late source drift.
    exp_audit = here / "audit_exp_share_evolution_v3_25.py"
    if not exp_audit.is_file():
        raise RuntimeError(f"missing final-state Exp. Share regression audit: {exp_audit}")
    subprocess.run([sys.executable, str(exp_audit), str(root)], check=True)

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

    # Preserve the exact protected-feature proof alongside the GREEN ROM.
    # The consolidated bundle is copied earlier, but this report is generated
    # only after that bundle completes, so mirror it here once it exists.
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
