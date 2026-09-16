#!/usr/bin/env python3
"""Apply every completed Russian localization pass after Misty v3.22.

This is the single ordered manifest for the incremental FireRed translation
passes. Some historical localization scripts chain the next pass themselves;
therefore this runner checks the build audit marker for each version and skips
a pass that an earlier script has already applied. This prevents double-patch
failures while keeping the sequence fail-closed for genuinely missing anchors.

After all passes, known unsupported Unicode dash characters are normalized to
the FireRed-safe ASCII hyphen before the normal quote/e sanitizers run.
Pokemon, Move and Ability proper names stay English by project canon.
Ash Bond / Ash Cap are not touched.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_INCREMENTAL_V3_85"

SCRIPTS = [
    "localize_cerulean_rival_v3_23.py",
    "localize_route25_bill_v3_24.py",
    "localize_cerulean_rocket_tm28_v3_25.py",
    "localize_ssanne_captain_v3_26.py",
    "localize_ssanne_rival_v3_27.py",
    "localize_vermilion_surge_v3_28.py",
    "localize_celadon_erika_v3_29.py",
    "localize_rocket_hideout_giovanni_v3_30.py",
    "localize_pokemon_tower_fuji_v3_31.py",
    "localize_lavender_poke_flute_v3_32.py",
    "localize_fuchsia_koga_v3_33.py",
    "localize_saffron_sabrina_v3_34.py",
    "localize_cinnabar_blaine_v3_35.py",
    "localize_viridian_giovanni_v3_36.py",
    "localize_route22_late_rival_v3_37.py",
    "localize_pokemon_league_lorelei_v3_38.py",
    "localize_pokemon_league_bruno_v3_39.py",
    "localize_pokemon_league_agatha_v3_40.py",
    "localize_pokemon_league_lance_v3_41.py",
    "localize_pokemon_league_champion_v3_42.py",
    "localize_pokemon_league_rematches_v3_43.py",
    "localize_pokemon_league_hall_of_fame_v3_44.py",
    "localize_sevii_entry_v3_45.py",
    "localize_two_island_lostelle_quest_v3_46.py",
    "localize_three_island_biker_intro_v3_47.py",
    "localize_three_island_biker_battles_v3_48.py",
    "localize_three_island_lostelle_hint_v3_49.py",
    "localize_berry_forest_lostelle_rescue_v3_50.py",
    "localize_two_island_lostelle_return_v3_51.py",
    "localize_two_island_meteorite_handoff_v3_52.py",
    "localize_one_island_return_kanto_v3_53.py",
    "localize_pallet_oak_rating_v3_54.py",
    "localize_pallet_oak_national_dex_v3_55.py",
    "localize_one_island_celio_ruby_request_v3_56.py",
    "localize_mt_ember_rocket_password_v3_57.py",
    "localize_mt_ember_rocket_battles_v3_58.py",
    "localize_mt_ember_ruby_pickup_v3_59.py",
    "localize_one_island_celio_ruby_handoff_v3_60.py",
    "localize_four_island_rival_arrival_v3_61.py",
    "localize_icefall_cave_lorelei_rockets_v3_62.py",
    "localize_ruin_valley_dotted_hole_door_v3_63.py",
    "localize_dotted_hole_sapphire_theft_v3_64.py",
    "localize_rocket_warehouse_grunt1_v3_65.py",
    "localize_rocket_warehouse_grunt2_v3_66.py",
    "localize_rocket_warehouse_grunt3_v3_67.py",
    "localize_rocket_warehouse_admin1_v3_68.py",
    "localize_rocket_warehouse_admin2_v3_69.py",
    "localize_rocket_warehouse_gideon_v3_70.py",
    "localize_celio_sapphire_network_v3_71.py",
    "localize_mt_moon_fossil_choice_v3_72.py",
    "localize_route24_nugget_bridge_v3_73.py",
    "localize_route24_remaining_v3_74.py",
    "localize_route5_sign_v3_75.py",
    "localize_route6_v3_76.py",
    "localize_vermilion_boarding_v3_77.py",
    "localize_vermilion_grimer_v3_78.py",
    "localize_vermilion_gym_advice_v3_79.py",
    "localize_vermilion_route2_aide_v3_80.py",
    "localize_vermilion_fanclub_bike_voucher_v3_81.py",
    "localize_vermilion_fanclub_remaining_v3_82.py",
    "localize_ssanne_kitchen_v3_83.py",
    "localize_ssanne_deck_v3_84.py",
    "localize_routes8_14_v3_87.py",
    "localize_routes15_19_v3_89.py",
    "localize_routes13_17_v3_90.py",
    "localize_routes11_12_20_v3_91.py",
    "fix_bulk_localization_escapes_v3_92.py",
    "localize_routes3_9_16_v3_93.py",
    "localize_route10_rocktunnel_viridianforest_v3_94.py",
    "localize_kindleroad_patternbush_v3_95.py",
    "localize_fanclub_gamecorner_v3_96.py",
    "localize_sevault_canyon_v3_97.py",
    "localize_sevii_dojo_v3_99.py",
    "localize_gyms_route25_v3_100.py",
    "localize_saffron_silph_v3_101.py",
    "localize_celadon_mtmoon_route21_v3_102.py",
    "localize_resort_fuchsia_cerulean_v3_104.py",
    "localize_memorial_silph6_outcast_v3_105.py",
    "localize_tower_vermilion_victory_v3_106.py",
    "localize_oneisland_silph5_celadonroof_v3_107.py",
    "localize_city_museum_v3_108.py",
    "localize_silph11_ruinvalley_fishing_v3_109.py",
    "localize_rocket_hideout_b1f_v3_110.py",
    "localize_pewter_vermilion_gym_v3_111.py",
    "localize_daycare_victory2_school_v3_112.py",
    "localize_safari_tower_mtmoon_v3_113.py",
    "localize_oak_aides_gatehouses_v3_114.py",
    "localize_pc_mart_residuals_v3_115.py",
    "localize_route4_bikeshop_celadon3f_v3_116.py",
    "localize_celadon_service_ember_spa_v3_117.py",
    "localize_safe_mart_npcs_v3_118.py",
    "localize_silph_2f_8f_9f_v3_119.py",
    "localize_silph_3f_4f_10f_v3_120.py",
    "localize_pokemon_tower_3f_4f_6f_7f_v3_121.py",
    "localize_tanoby_meadow_v3_122.py",
    "localize_cerulean_houses_warden_v3_123.py",
    "localize_route18_name_rater_v3_124.py",
    "localize_lavender_fishing_v3_125.py",
    "localize_lavender_move_deleter_heracross_v3_126.py",
    "localize_celadon_condominiums_v3_127.py",
    "localize_museum_lab_chansey_v3_128.py",
    "localize_dept_research_lorelei_v3_129.py",
    "localize_residual_runtime_v3_133.py",
    "localize_residual_runtime_v3_134.py",
    "localize_residual_runtime_v3_135.py",
    "localize_residual_runtime_v3_136.py",
    "localize_residual_runtime_v3_137.py",
    "localize_residual_runtime_v3_138.py",
    "localize_residual_runtime_v3_139.py",
    "localize_residual_runtime_v3_140_142.py",
    "localize_residual_runtime_v3_143.py",
    "localize_system_runtime_accentfix_v3_145.py",
    "localize_system_runtime_v3_146.py",
    "localize_full_surface_system_v3_147.py",
    "localize_full_surface_system_v3_148.py",
    "localize_cable_club_help_v3_149.py",
    "localize_full_surface_system_v3_150.py",
    "localize_full_surface_system_v3_151.py",
    "localize_full_surface_system_v3_152.py",
    "localize_full_surface_system_v3_153.py",
    "localize_save_pc_v3_154.py",
]

VERSION_RE = re.compile(r"_v3_(\d+)\.py$")


def already_applied(root: Path, name: str) -> bool:
    match = VERSION_RE.search(name)
    if not match:
        return False
    version = match.group(1)
    return any((root / "build").glob(f"*v3_{version}_audit.json"))


def apply_all(root: Path) -> tuple[int, int]:
    ci_dir = Path(__file__).resolve().parent
    missing = [name for name in SCRIPTS if not (ci_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing localization scripts: {missing}")

    applied = 0
    skipped = 0
    for index, name in enumerate(SCRIPTS, start=1):
        if already_applied(root, name):
            skipped += 1
            print(f"[{MARKER}] {index:02d}/{len(SCRIPTS):02d} SKIP already applied {name}", flush=True)
            continue
        script = ci_dir / name
        print(f"[{MARKER}] {index:02d}/{len(SCRIPTS):02d} APPLY {name}", flush=True)
        subprocess.run([sys.executable, str(script), str(root)], check=True)
        applied += 1
    return applied, skipped


def sanitize_unsupported_dashes(root: Path) -> tuple[int, int]:
    changed_files = 0
    replacements = 0
    suffixes = {".c", ".h", ".inc", ".s", ".txt"}
    for base in (root / "src", root / "data", root / "include"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            count = text.count("—") + text.count("–")
            if not count:
                continue
            path.write_text(text.replace("—", "-").replace("–", "-"), encoding="utf-8")
            changed_files += 1
            replacements += count
    return replacements, changed_files


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    applied, skipped = apply_all(root)
    dash_count, dash_files = sanitize_unsupported_dashes(root)
    print(
        f"[{MARKER}] PASS: applied {applied}, skipped {skipped} already-applied passes; "
        f"normalized {dash_count} unsupported dash characters in {dash_files} files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
