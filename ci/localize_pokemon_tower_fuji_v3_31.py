#!/usr/bin/env python3
"""Qarro v3.31 mandatory Pokemon Tower / Mr. Fuji Russian runtime localization.

Translates only the verified pinned Mr. Fuji rescue dialogue on Pokemon Tower 7F.
Pokemon species / move / ability proper names remain English. Ash Bond / Ash
Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKEMON_TOWER_FUJI_V3_31"
REL = Path("data/maps/PokemonTower_7F_Frlg/scripts.inc")

PATCHES = {
    "PokemonTower_7F_Text_MrFujiThankYouFollowMe": (
        "PokemonTower_7F_Text_MrFujiThankYouFollowMe::\n"
        "\t.string \"MR. FUJI: Heh?\\n\"\n"
        "\t.string \"You came to save me?\\p\"\n"
        "\t.string \"Thank you. But, I came here of my\\n\"\n"
        "\t.string \"own free will.\\p\"\n"
        "\t.string \"I came to calm the spirit of\\n\"\n"
        "\t.string \"CUBONE's mother.\\p\"\n"
        "\t.string \"I think MAROWAK's spirit has\\n\"\n"
        "\t.string \"finally left us.\\p\"\n"
        "\t.string \"I must thank you for your kind\\n\"\n"
        "\t.string \"concern.\\p\"\n"
        "\t.string \"Follow me to my home, POKéMON\\n\"\n"
        "\t.string \"HOUSE, at the foot of this tower.$\"\n",
        "PokemonTower_7F_Text_MrFujiThankYouFollowMe::\n"
        "\t.string \"МР. ФУДЗИ: Хм?\\n\"\n"
        "\t.string \"Ты пришёл спасти меня?\\p\"\n"
        "\t.string \"Спасибо. Но я пришёл сюда\\n\"\n"
        "\t.string \"по собственной воле.\\p\"\n"
        "\t.string \"Я хотел успокоить дух\\n\"\n"
        "\t.string \"матери CUBONE.\\p\"\n"
        "\t.string \"Думаю, дух MAROWAK наконец\\n\"\n"
        "\t.string \"обрёл покой.\\p\"\n"
        "\t.string \"Спасибо тебе за заботу.\\p\"\n"
        "\t.string \"Идём со мной в мой ДОМ ПОКЕМОНОВ\\n\"\n"
        "\t.string \"у подножия этой башни.$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_pokemon_tower_fuji_v3_31.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied = []

    for label, (pinned, ru) in PATCHES.items():
        variants = [pinned]
        normalized = pinned.replace("é", "e").replace("É", "E")
        if normalized != pinned:
            variants.append(normalized)
        hits = [(variant, text.count(variant)) for variant in variants]
        total = sum(count for _, count in hits)
        if total != 1:
            raise SystemExit(f"{MARKER}: {label}: expected exactly one pinned/normalized anchor, found {total}")
        source = next(variant for variant, count in hits if count == 1)
        text = text.replace(source, ru, 1)
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_pokemon_tower_fuji_v3_31_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory Pokemon Tower Mr. Fuji runtime block; Ash Bond/Ash Cap untouched")

    flute_script = Path(__file__).with_name("localize_lavender_poke_flute_v3_32.py")
    subprocess.run([sys.executable, str(flute_script), str(root)], check=True)
    koga_script = Path(__file__).with_name("localize_fuchsia_koga_v3_33.py")
    subprocess.run([sys.executable, str(koga_script), str(root)], check=True)
    sabrina_script = Path(__file__).with_name("localize_saffron_sabrina_v3_34.py")
    subprocess.run([sys.executable, str(sabrina_script), str(root)], check=True)
    blaine_script = Path(__file__).with_name("localize_cinnabar_blaine_v3_35.py")
    subprocess.run([sys.executable, str(blaine_script), str(root)], check=True)
    viridian_script = Path(__file__).with_name("localize_viridian_giovanni_v3_36.py")
    subprocess.run([sys.executable, str(viridian_script), str(root)], check=True)
    route22_script = Path(__file__).with_name("localize_route22_late_rival_v3_37.py")
    subprocess.run([sys.executable, str(route22_script), str(root)], check=True)
    lorelei_script = Path(__file__).with_name("localize_pokemon_league_lorelei_v3_38.py")
    subprocess.run([sys.executable, str(lorelei_script), str(root)], check=True)
    bruno_script = Path(__file__).with_name("localize_pokemon_league_bruno_v3_39.py")
    subprocess.run([sys.executable, str(bruno_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
