#!/usr/bin/env python3
"""Qarro v3.26 mandatory S.S. Anne Captain / HM01 Russian runtime localization.

Translates only the verified pinned Captain progression chain required to obtain
HM01/CUT and unlock the Vermilion progression flag. Pokemon species / move /
ability proper names remain English. Ash Bond / Ash Cap are not referenced or
changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_SSANNE_CAPTAIN_V3_26"
REL = Path("data/maps/SSAnne_CaptainsOffice_Frlg/scripts.inc")

PATCHES = {
    "SSAnne_CaptainsOffice_Text_CaptainIFeelSeasick": (
        "SSAnne_CaptainsOffice_Text_CaptainIFeelSeasick::\n"
        "\t.string \"CAPTAIN: Ooargh…\\n\"\n"
        "\t.string \"I feel hideous…\\l\"\n"
        "\t.string \"Urrp! Seasick…$\"\n",
        "SSAnne_CaptainsOffice_Text_CaptainIFeelSeasick::\n"
        "\t.string \"КАПИТАН: Ох…\\n\"\n"
        "\t.string \"Мне ужасно плохо…\\l\"\n"
        "\t.string \"Уф! Морская болезнь…$\"\n",
    ),
    "SSAnne_CaptainsOffice_Text_RubbedCaptainsBack": (
        "SSAnne_CaptainsOffice_Text_RubbedCaptainsBack::\n"
        "\t.string \"{PLAYER} rubbed the CAPTAIN's\\n\"\n"
        "\t.string \"back!\\p\"\n"
        "\t.string \"Rub-rub…\\n\"\n"
        "\t.string \"Rub-rub…$\"\n",
        "SSAnne_CaptainsOffice_Text_RubbedCaptainsBack::\n"
        "\t.string \"{PLAYER} растёр спину\\n\"\n"
        "\t.string \"КАПИТАНА!\\p\"\n"
        "\t.string \"Трём-трём…\\n\"\n"
        "\t.string \"Трём-трём…$\"\n",
    ),
    "SSAnne_CaptainsOffice_Text_ThankYouHaveHMForCut": (
        "SSAnne_CaptainsOffice_Text_ThankYouHaveHMForCut::\n"
        "\t.string \"CAPTAIN: Whew! Thank you!\\n\"\n"
        "\t.string \"I'm feeling much better now.\\p\"\n"
        "\t.string \"You want to see my hidden CUT\\n\"\n"
        "\t.string \"technique?\\p\"\n"
        "\t.string \"I could show you my prized CUT\\n\"\n"
        "\t.string \"technique if I weren't so ill…\\p\"\n"
        "\t.string \"I know! You can have this!\\n\"\n"
        "\t.string \"This HIDDEN MACHINE!\\p\"\n"
        "\t.string \"Teach CUT to your POKéMON, and\\n\"\n"
        "\t.string \"you can see it CUT anytime!$\"\n",
        "SSAnne_CaptainsOffice_Text_ThankYouHaveHMForCut::\n"
        "\t.string \"КАПИТАН: Фух! Спасибо!\\n\"\n"
        "\t.string \"Мне уже гораздо лучше.\\p\"\n"
        "\t.string \"Хочешь увидеть мою секретную\\n\"\n"
        "\t.string \"технику CUT?\\p\"\n"
        "\t.string \"Я бы показал её сам, если бы\\n\"\n"
        "\t.string \"не был так слаб…\\p\"\n"
        "\t.string \"Придумал! Возьми вот это!\\n\"\n"
        "\t.string \"Эту HIDDEN MACHINE!\\p\"\n"
        "\t.string \"Научи ПОКЕМОНА CUT, и сможешь\\n\"\n"
        "\t.string \"использовать её когда угодно!$\"\n",
    ),
    "SSAnne_CaptainsOffice_Text_ObtainedHM01FromCaptain": (
        "SSAnne_CaptainsOffice_Text_ObtainedHM01FromCaptain::\n"
        "\t.string \"{PLAYER} obtained HM01\\n\"\n"
        "\t.string \"from the CAPTAIN!$\"\n",
        "SSAnne_CaptainsOffice_Text_ObtainedHM01FromCaptain::\n"
        "\t.string \"{PLAYER} получил HM01\\n\"\n"
        "\t.string \"от КАПИТАНА!$\"\n",
    ),
    "SSAnne_CaptainsOffice_Text_ExplainCut": (
        "SSAnne_CaptainsOffice_Text_ExplainCut::\n"
        "\t.string \"Using CUT, you can chop down\\n\"\n"
        "\t.string \"small trees.\\p\"\n"
        "\t.string \"Why not try it with the trees\\n\"\n"
        "\t.string \"around VERMILION CITY?$\"\n",
        "SSAnne_CaptainsOffice_Text_ExplainCut::\n"
        "\t.string \"С помощью CUT можно срубать\\n\"\n"
        "\t.string \"небольшие деревья.\\p\"\n"
        "\t.string \"Попробуй её на деревьях возле\\n\"\n"
        "\t.string \"VERMILION CITY.$\"\n",
    ),
    "SSAnne_CaptainsOffice_Text_SSAnneWillSetSailSoon": (
        "SSAnne_CaptainsOffice_Text_SSAnneWillSetSailSoon::\n"
        "\t.string \"CAPTAIN: …Whew!\\p\"\n"
        "\t.string \"Now that I'm not sick anymore,\\n\"\n"
        "\t.string \"I guess it's time.\\p\"\n"
        "\t.string \"The S.S. ANNE will set sail soon!\\p\"\n"
        "\t.string \"Farewell, until our return to\\n\"\n"
        "\t.string \"VERMILION CITY!$\"\n",
        "SSAnne_CaptainsOffice_Text_SSAnneWillSetSailSoon::\n"
        "\t.string \"КАПИТАН: …Фух!\\p\"\n"
        "\t.string \"Теперь, когда мне больше не плохо,\\n\"\n"
        "\t.string \"пора отправляться.\\p\"\n"
        "\t.string \"S.S. ANNE скоро выйдет в море!\\p\"\n"
        "\t.string \"Прощай до нашего возвращения в\\n\"\n"
        "\t.string \"VERMILION CITY!$\"\n",
    ),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_ssanne_captain_v3_26.py <upstream-root>")
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
    out = root / "build" / "qarro_ru_ssanne_captain_v3_26_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "translatedBlocks": applied,
        "translatedBlockCount": len(applied),
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names may remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} mandatory S.S. Anne Captain/HM01 runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
