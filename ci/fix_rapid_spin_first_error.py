#!/usr/bin/env python3
from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: fix_rapid_spin_first_error.py <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1])
    p = root / "src/data/moves_info.h"
    s = p.read_text()

    marker = "        .description = COMPOUND_STRING(\n    #if B_SPEED_BUFFING_RAPID_SPIN >= GEN_8"
    try:
        start = s.index(marker)
        end = s.index("        .effect = EFFECT_RAPID_SPIN,", start)
    except ValueError:
        print("Pinned Rapid Spin block not found; refusing broad edit.", file=sys.stderr)
        return 3

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
        print("Unexpected pinned Rapid Spin block; refusing broad edit.", file=sys.stderr)
        print(repr(actual), file=sys.stderr)
        return 4

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

    p.write_text(s[:start] + fixed + s[end:])
    print("Applied minimal semantic-preserving Rapid Spin directive-layout fix.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
