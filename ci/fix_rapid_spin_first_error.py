#!/usr/bin/env python3
from pathlib import Path
import sys


def fix_rapid_spin(s: str) -> str:
    marker = "        .description = COMPOUND_STRING(\n    #if B_SPEED_BUFFING_RAPID_SPIN >= GEN_8"
    start = s.index(marker)
    end = s.index("        .effect = EFFECT_RAPID_SPIN,", start)

    actual = s[start:end]
    expected = (
        "        .description = COMPOUND_STRING(\n"
        "    #if B_SPEED_BUFFING_RAPID_SPIN >= GEN_8\n"
        "            \"Spins to remove traps\\n\"\n"
        "            \"and raise Speed.\"),\n"
        "        .additionalEffects = ADDITIONAL_EFFECTS({\n"
        "            .moveEffect = MOVE_EFFECT_STAT_PLUS,\n"
        "            .speed = 1,\n"
        "            .self = TRUE,\n"
        "            .chance = 100,\n"
        "        }),\n"
        "    #else\n"
        "            \"Spins the body at high\\n\"\n"
        "            \"speed to remove traps.\"),\n"
        "    #endif\n"
    )
    if actual != expected:
        raise RuntimeError("Unexpected pinned Rapid Spin block; refusing broad edit.")

    fixed = (
        "    #if B_SPEED_BUFFING_RAPID_SPIN >= GEN_8\n"
        "        .description = COMPOUND_STRING(\n"
        "            \"Spins to remove traps\\n\"\n"
        "            \"and raise Speed.\"),\n"
        "        .additionalEffects = ADDITIONAL_EFFECTS({\n"
        "            .moveEffect = MOVE_EFFECT_STAT_PLUS,\n"
        "            .speed = 1,\n"
        "            .self = TRUE,\n"
        "            .chance = 100,\n"
        "        }),\n"
        "    #else\n"
        "        .description = COMPOUND_STRING(\n"
        "            \"Spins the body at high\\n\"\n"
        "            \"speed to remove traps.\"),\n"
        "    #endif\n"
    )
    return s[:start] + fixed + s[end:]


def fix_charge(s: str) -> str:
    marker = "        .description = COMPOUND_STRING(\n    #if B_CHARGE >= GEN_9"
    start = s.index(marker)
    end = s.index("        .effect = EFFECT_CHARGE,", start)

    actual = s[start:end]
    expected = (
        "        .description = COMPOUND_STRING(\n"
        "    #if B_CHARGE >= GEN_9\n"
        "        #if B_CHARGE_SPDEF_RAISE >= GEN_5\n"
        "            \"Ups the user's next Electric\\n\"\n"
        "            \"move. It also raises Sp. Def.\"),\n"
        "        #else\n"
        "            \"Charges power to boost the\\n\"\n"
        "            \"Electric move used next.\"),\n"
        "        #endif\n"
        "    #else\n"
        "        #if B_CHARGE_SPDEF_RAISE >= GEN_5\n"
        "            \"Ups the user's next move if\\n\"\n"
        "            \"Electric. Also raises Sp. Def.\"),\n"
        "        #else\n"
        "            \"Charges power to boost the\\n\"\n"
        "            \"Electric move used next turn.\"),\n"
        "        #endif\n"
        "    #endif\n"
    )
    if actual != expected:
        raise RuntimeError("Unexpected pinned Charge block; refusing broad edit.")

    fixed = (
        "    #if B_CHARGE >= GEN_9\n"
        "        #if B_CHARGE_SPDEF_RAISE >= GEN_5\n"
        "        .description = COMPOUND_STRING(\n"
        "            \"Ups the user's next Electric\\n\"\n"
        "            \"move. It also raises Sp. Def.\"),\n"
        "        #else\n"
        "        .description = COMPOUND_STRING(\n"
        "            \"Charges power to boost the\\n\"\n"
        "            \"Electric move used next.\"),\n"
        "        #endif\n"
        "    #else\n"
        "        #if B_CHARGE_SPDEF_RAISE >= GEN_5\n"
        "        .description = COMPOUND_STRING(\n"
        "            \"Ups the user's next move if\\n\"\n"
        "            \"Electric. Also raises Sp. Def.\"),\n"
        "        #else\n"
        "        .description = COMPOUND_STRING(\n"
        "            \"Charges power to boost the\\n\"\n"
        "            \"Electric move used next turn.\"),\n"
        "        #endif\n"
        "    #endif\n"
    )
    return s[:start] + fixed + s[end:]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: fix_rapid_spin_first_error.py <upstream-root>", file=sys.stderr)
        return 2

    p = Path(sys.argv[1]) / "src/data/moves_info.h"
    s = p.read_text()
    try:
        s = fix_rapid_spin(s)
        s = fix_charge(s)
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 3

    p.write_text(s)
    print("Applied exact Rapid Spin fix plus exact next observed Charge directive-layout fix.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
