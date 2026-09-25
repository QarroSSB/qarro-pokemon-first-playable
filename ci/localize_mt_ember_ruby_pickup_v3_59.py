#!/usr/bin/env python3
"""Qarro v3.59 mandatory Mt. Ember Ruby pickup localization.

Translates only the verified progression message shown when the Ruby object is
collected on Mt. Ember. The Ruby event, FLAG_GOT_RUBY, Celio handoff, Rainbow
Pass, optional NPC text, Ash Bond, and Ash Cap remain untouched. Pokemon species
/ move / ability proper names remain English.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_MT_EMBER_RUBY_PICKUP_V3_59"
REL = Path("data/maps/MtEmber_RubyPath_B3F_Frlg/scripts.inc")
LABEL = "MtEmber_RubyPath_B3F_Text_FoundARuby"
NEEDLES = ("{PLAYER} found a RUBY!",)
RU = '''MtEmber_RubyPath_B3F_Text_FoundARuby::
\t.string "{PLAYER} нашел РУБИН!$"
'''
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")


def replace_label_block(text: str) -> str:
    matches = list(re.finditer(rf"(?m)^{re.escape(LABEL)}::\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {LABEL}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    block = text[start:end]
    missing = [needle for needle in NEEDLES if needle not in block]
    if missing:
        raise SystemExit(f"{MARKER}: {LABEL}: pinned evidence mismatch; missing {missing}")
    if re.search(r"[А-Яа-яЁё]", block):
        raise SystemExit(f"{MARKER}: {LABEL}: block is already localized or unexpectedly contains Cyrillic")
    return text[:start] + RU + "\n" + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_mt_ember_ruby_pickup_v3_59.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    text = replace_label_block(text)
    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_mt_ember_ruby_pickup_v3_59_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": [LABEL],
        "translatedBlockCount": 1,
        "scope": "mandatory Mt. Ember Ruby pickup message",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated Ruby pickup message; Ash Bond/Ash Cap untouched")

    next_script = Path(__file__).with_name("localize_one_island_celio_ruby_handoff_v3_60.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
