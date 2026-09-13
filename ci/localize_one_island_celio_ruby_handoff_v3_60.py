#!/usr/bin/env python3
"""Qarro v3.60 mandatory Celio Ruby handoff / Rainbow Pass localization.

Translates only the verified progression text reached after FLAG_GOT_RUBY on
One Island: Ruby handoff, Celio's follow-up request, the reachable decline loop,
and Rainbow Pass / map-page handoff. Sapphire progression, optional NPC text,
Ash Bond, and Ash Cap remain untouched. Pokemon species / move / ability proper
names remain English.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_ONE_ISLAND_CELIO_RUBY_HANDOFF_V3_60"
REL = Path("data/maps/OneIsland_PokemonCenter_1F_Frlg/scripts.inc")

PATCHES = {
    "OneIsland_PokemonCenter_1F_Text_OhThats": {
        "needles": ("Oh!", "Th-that's"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_OhThats::
\t.string "О!\\n"
\t.string "Э-это же...$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_HandedRubyToCelio": {
        "needles": ("handed the RUBY", "to CELIO"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_HandedRubyToCelio::
\t.string "{PLAYER} передал РУБИН\\n"
\t.string "СЕЛИО.$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_MayIAskOneMoreFavor": {
        "needles": ("you're simply amazing", "May I ask one more giant favor"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_MayIAskOneMoreFavor::
\t.string "Спасибо!\\n"
\t.string "{PLAYER}, ты просто невероятен!\\p"
\t.string "... ... ...  ... ... ...\\p"
\t.string "Эм... Можно попросить тебя\\n"
\t.string "ещё об одном большом одолжении?$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_PleaseINeedYourHelp": {
        "needles": ("It's not anything weird", "I need your help"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_PleaseINeedYourHelp::
\t.string "Н-ничего странного, правда.\\n"
\t.string "Пожалуйста, мне нужна твоя помощь.$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_AnotherGemstoneInSeviiIslands": {
        "needles": ("another gem that forms", "pair with this RUBY", "SEVII ISLANDS", "ferry", "PASS and the TOWN MAP"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_AnotherGemstoneInSeviiIslands::
\t.string "Изучая драгоценные камни,\\n"
\t.string "я обнаружил кое-что важное.\\p"
\t.string "Есть ещё один камень, который\\n"
\t.string "образует пару с этим РУБИНОМ.\\p"
\t.string "Он должен находиться где-то\\n"
\t.string "на островах СЕВИИ.\\p"
\t.string "{PLAYER}, пожалуйста, найди\\n"
\t.string "этот второй камень.\\p"
\t.string "{PLAYER}, можно твой паромный\\n"
\t.string "ПРОПУСК и КАРТУ?$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_ReturnedTriPassForRainbowPass": {
        "needles": ("returned the TRI-PASS", "RAINBOW PASS"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_ReturnedTriPassForRainbowPass::
\t.string "{PLAYER} вернул ТРИ-ПРОПУСК и\\n"
\t.string "получил РАДУЖНЫЙ ПРОПУСК.$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_ObtainedExtraMapPage": {
        "needles": ("Obtained an extra page", "TOWN MAP"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_ObtainedExtraMapPage::
\t.string "Получена дополнительная страница\\n"
\t.string "для КАРТЫ!$"
''',
    },
    "OneIsland_PokemonCenter_1F_Text_PassLetYouGetToAllIslands": {
        "needles": ("my own ferry PASS", "all the", "SEVII ISLANDS", "can't do", "without your help"),
        "ru": '''OneIsland_PokemonCenter_1F_Text_PassLetYouGetToAllIslands::
\t.string "Это мой собственный пропуск\\n"
\t.string "на паром.\\p"
\t.string "С ним можно попасть на все\\n"
\t.string "острова СЕВИИ.\\p"
\t.string "{PLAYER}, пожалуйста, без твоей\\n"
\t.string "помощи мне не справиться.$"
''',
    },
}

LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")


def replace_label_block(text: str, label: str, needles: tuple[str, ...], replacement: str) -> str:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        raise SystemExit(f"{MARKER}: {label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    block = text[start:end]
    missing = [needle for needle in needles if needle not in block]
    if missing:
        raise SystemExit(f"{MARKER}: {label}: pinned evidence mismatch; missing {missing}")
    if re.search(r"[А-Яа-яЁё]", block):
        raise SystemExit(f"{MARKER}: {label}: block is already localized or unexpectedly contains Cyrillic")
    return text[:start] + replacement + "\n" + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_one_island_celio_ruby_handoff_v3_60.py <upstream-root>")
    root = Path(sys.argv[1])
    path = root / REL
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []

    for label, spec in PATCHES.items():
        text = replace_label_block(text, label, spec["needles"], spec["ru"])
        applied.append(label)

    path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_one_island_celio_ruby_handoff_v3_60_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "scope": "mandatory Celio Ruby handoff and Rainbow Pass progression",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} Celio Ruby handoff blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
