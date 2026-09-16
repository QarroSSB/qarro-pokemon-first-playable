#!/usr/bin/env python3
"""Qarro integration wrapper: localization + final Kanto Gym A/B/C + story bosses + Kanto League + e normalization.

Runs the exact previously-green Oak lab localization from commit 0ddb5e3,
applies every completed incremental Russian localization pass through the
single ordered v3.85 manifest, establishes the green Kanto 6v6 Variant-A
baseline, removes the historical 5-of-6 runtime interception, upgrades the eight
story Gyms to final save-fixed A/B/C 6v6 selection, applies the two
implementation-derived pre-Gym Giovanni story boss teams, installs the
final-canon Kanto Elite Four and Champion first-clear 6v6 builds, and only then
normalizes literal é/É to ordinary e/E.

The ordering keeps FireRed POKéMON anchors intact until all localization passes
have consumed them. Ash Bond / Ash Cap are untouched.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "0ddb5e33c653bc4550cecb18d5e0440232df7a8a"
BASE_PATH = "ci/localize_oaks_lab_starter_v3_5.py"
MARKER = "QARRO_POST_LOCALIZATION_E_V3_7"
INCREMENTAL_RUNNER = "apply_ru_incremental_v3_85.py"
GYM_SIX_RUNNER = "gym_six_variant_a_v3_86.py"
GYM_SIX_FINALIZER = "gym_six_finalize_v3_88.py"
KANTO_GYM_ABC_RUNNER = "gym_kanto_abc_v3_132.py"
ROCKET_BOSS_RUNNER = "rocket_boss_giovanni_v3_98.py"
KANTO_E4_BOSS_RUNNER = "boss_kanto_e4_first_v3_130.py"
KANTO_CHAMPION_BOSS_RUNNER = "boss_kanto_champion_first_v3_131.py"


def load_base(repo: Path) -> dict:
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    code = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )
    ns = {
        "__name__": "qarro_oak_lab_pre_e_normalization",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    return ns


def run_ci_pass(root: Path, filename: str) -> None:
    script = Path(__file__).resolve().with_name(filename)
    if not script.is_file():
        raise FileNotFoundError(f"required Qarro pass missing: {script}")
    subprocess.run([sys.executable, str(script), str(root)], check=True)


def normalize_accented_e(root: Path) -> tuple[int, int]:
    roots = [root / "src", root / "data", root / "include"]
    suffixes = {".c", ".h", ".inc", ".s", ".txt"}
    changed_files = 0
    replacements = 0

    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            count = text.count("é") + text.count("É")
            if not count:
                continue

            path.write_text(
                text.replace("é", "e").replace("É", "E"),
                encoding="utf-8",
            )
            replacements += count
            changed_files += 1

    return replacements, changed_files


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    base = load_base(repo)
    rc = int(base["main"]() or 0)
    if rc:
        return rc

    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()

    # Apply translations while original POKéMON anchors still exist.
    run_ci_pass(root, INCREMENTAL_RUNNER)

    # Establish the known-green six-Pokemon baseline, then layer the final
    # save-fixed A/B/C selector without changing the eight story Leader IDs.
    run_ci_pass(root, GYM_SIX_RUNNER)
    run_ci_pass(root, GYM_SIX_FINALIZER)
    run_ci_pass(root, KANTO_GYM_ABC_RUNNER)

    # Strengthen only the two story Giovanni battles. Exact rosters are
    # implementation-derived; final Gym Giovanni and ordinary Rocket trainers
    # remain outside this pass.
    run_ci_pass(root, ROCKET_BOSS_RUNNER)

    # Install only the four original first-clear Kanto Elite Four teams from
    # the final boss workbook. Rematches remain separate work.
    run_ci_pass(root, KANTO_E4_BOSS_RUNNER)

    # FireRed selects one of three first-clear Champion IDs from the starter.
    # Keep that selector intact, but give all three IDs the same final-canon
    # Gary team. Champion rematches remain untouched.
    run_ci_pass(root, KANTO_CHAMPION_BOSS_RUNNER)

    replacements, changed_files = normalize_accented_e(root)

    leftovers = []
    for base_dir in (root / "src", root / "data", root / "include"):
        if not base_dir.exists():
            continue
        for path in base_dir.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".c", ".h", ".inc", ".s", ".txt"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "é" in text or "É" in text:
                leftovers.append(str(path.relative_to(root)))
                if len(leftovers) >= 10:
                    break
        if leftovers:
            break

    if leftovers:
        raise RuntimeError(f"accented e remained after normalization: {leftovers}")

    audit_path = root / "build/qarro_ru_oak_lab_starter_v3_5_audit.json"
    audit = {}
    if audit_path.exists():
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
    audit.update(
        {
            "incrementalLocalizationManifest": INCREMENTAL_RUNNER,
            "incrementalLocalizationApplied": True,
            "gymSixPass": GYM_SIX_RUNNER,
            "gymSixFinalizer": GYM_SIX_FINALIZER,
            "gymSixVariantATestApplied": True,
            "legacyFiveOfSixRemoved": True,
            "kantoGymABCPass": KANTO_GYM_ABC_RUNNER,
            "kantoGymABC6v6Applied": True,
            "kantoGymSaveFixedSelector": True,
            "rocketBossPass": ROCKET_BOSS_RUNNER,
            "storyGiovanniImplementationDerived": True,
            "kantoEliteFourBossPass": KANTO_E4_BOSS_RUNNER,
            "kantoEliteFourFirstClearCanonApplied": True,
            "kantoChampionBossPass": KANTO_CHAMPION_BOSS_RUNNER,
            "kantoChampionFirstClearCanonApplied": True,
            "kantoChampionFixedTeamAcrossStarterSelectors": True,
            "postLocalizationAccentedENormalized": True,
            "accentedEReplacements": replacements,
            "accentedEChangedFiles": changed_files,
            "specialAccentedEGlyphRequired": False,
        }
    )
    audit_path.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"[{MARKER}] PASS: incremental RU + final Kanto 6v6 A/B/C + story Giovanni bosses + "
        f"Kanto Elite Four + Champion first-clear canon applied; legacy 5-of-6 removed; "
        f"{replacements} literal é/É -> e/E replacements in {changed_files} files; Ash code untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
