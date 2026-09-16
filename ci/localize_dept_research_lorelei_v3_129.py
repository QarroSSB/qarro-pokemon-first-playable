#!/usr/bin/env python3
"""Qarro v3.129: localize safe Celadon 5F, Cinnabar Research Room and Lorelei House text.

Translates exactly 10 English-only FireRed runtime blocks after v3.128:
  * CeladonCity_DepartmentStore_5F_Frlg: 3
  * CinnabarIsland_PokemonLab_ResearchRoom_Frlg: 3
  * FourIsland_LoreleisHouse_Frlg: 4

Mart inventories, METRONOME tutor logic, Lorelei flags/doll-update logic,
trainer data, Pokemon/Move/Ability proper-name policy, and Ash Bond/Ash Cap
are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_DEPT_RESEARCH_LORELEI_V3_129"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/CeladonCity_DepartmentStore_5F_Frlg/scripts.inc": {
        "CeladonCity_DepartmentStore_5F_Text_ExplainStatEnhancers": "Усилители характеристик ПОКЕМОНОВ\\nпродаются только здесь.\\pHP UP повышает базовый запас HP\\nПОКЕМОНА.\\pCALCIUM повышает базовый\\nпоказатель SP. ATK ПОКЕМОНА.\\pZINC повышает базовый\\nпоказатель SP. DEF ПОКЕМОНА.\\pCARBOS повышает базовый\\nпоказатель SPEED.$",
        "CeladonCity_DepartmentStore_5F_Text_HereForStatEnhancers": "Мне нужны усилители\\nхарактеристик ПОКЕМОНОВ.\\pPROTEIN повышает базовый\\nпоказатель ATTACK.\\pIRON повышает базовый\\nпоказатель DEFENSE.$",
        "CeladonCity_DepartmentStore_5F_Text_Drugstore": "5F: АПТЕКА$",
    },
    "data/maps/CinnabarIsland_PokemonLab_ResearchRoom_Frlg/scripts.inc": {
        "CinnabarIsland_PokemonLab_ResearchRoom_Text_EeveeCanEvolveIntroThreeMons": "EEVEE может эволюционировать\\nв один из трёх видов ПОКЕМОНОВ.$",
        "CinnabarIsland_PokemonLab_ResearchRoom_Text_LegendaryBirdEmail": "Это сообщение электронной почты.\\p... ... ...\\pЕсть три легендарных\\nптицы-ПОКЕМОНА.\\pЭто ARTICUNO, ZAPDOS и\\nMOLTRES.\\pИх местонахождение неизвестно.\\pМы планируем исследовать пещеру\\nрядом с CERULEAN.\\pОт: ГРУППА ИССЛЕДОВАНИЯ\\nПОКЕМОНОВ...$",
        "CinnabarIsland_PokemonLab_ResearchRoom_Text_AnAmberPipe": "Янтарная трубка!$",
    },
    "data/maps/FourIsland_LoreleisHouse_Frlg/scripts.inc": {
        "FourIsland_LoreleisHouse_Text_IfAnythingWereToHappenToIsland": "LORELEI: Меня кое-что сильно\\nтревожит.\\pЕсли что-то случится на острове,\\nгде я родилась...\\pБудучи в ЛИГЕ ПОКЕМОНОВ,\\nя об этом не узнаю.\\pНе будет ли это безответственно\\nпо отношению к моему дому...$",
        "FourIsland_LoreleisHouse_Text_IllReturnToLeagueInShortWhile": "LORELEI: Значит, тебе удалось\\nрешить здесь все проблемы?\\pЭто замечательно.\\pТеперь мне незачем постоянно\\nоставаться здесь.\\pСпасибо...\\pСкоро я вернусь\\nв ЛИГУ ПОКЕМОНОВ.$",
        "FourIsland_LoreleisHouse_Text_WillDoWhatICanHereAndNow": "Я не знаю, что случится\\nв будущем, но...\\pЯ сделаю всё, что могу,\\nздесь и сейчас.\\pЭто всё, что я могу.$",
        "FourIsland_LoreleisHouse_Text_StuffedMonDollsGalore": "Здесь полно плюшевых\\nкукол ПОКЕМОНОВ!$",
    },
}
EXPECTED_TOTAL = 10


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def validate_translation(label: str, tr: str) -> None:
    if not tr.endswith("$"):
        die(f"{label}: must end with $")
    if "\n" in tr or "\r" in tr:
        die(f"{label}: physical newline")
    if any(ch in tr for ch in ("—", "–", "“", "”", "’", "…", "«", "»")):
        die(f"{label}: unsupported punctuation")
    if "\\\\" in tr:
        die(f"{label}: doubled runtime backslash")
    if not re.search(r"[А-Яа-яЁё]", tr):
        die(f"{label}: expected Cyrillic")


def block_bounds(text: str, label: str):
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected one label, got {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def replace_block(text: str, label: str, tr: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: already Cyrillic")
    if ".string " not in old:
        die(f"{label}: not text block")
    safe = tr.replace('"', '\\"')
    return text[:start] + f'{label}::\n\t.string "{safe}"\n\n' + text[end:]


def validate_written(rel: Path, text: str) -> None:
    for n, line in enumerate(text.splitlines(), 1):
        if '.string "' in line and line.count('"') < 2:
            die(f"{rel}:{n}: broken string")
    if re.search(r"\\\\[npl]", text):
        die(f"{rel}: doubled runtime escape")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    total = 0
    by_file = {}
    for rel_s, patches in FILES.items():
        path = root / rel_s
        if not path.is_file():
            die(f"missing target: {rel_s}")
        text = path.read_text(encoding="utf-8")
        for label, tr in patches.items():
            validate_translation(label, tr)
            text = replace_block(text, label, tr)
        validate_written(Path(rel_s), text)
        path.write_text(text, encoding="utf-8")
        by_file[rel_s] = len(patches)
        total += len(patches)

    if total != EXPECTED_TOTAL:
        die(f"expected {EXPECTED_TOTAL} blocks, got {total}")

    audit = {
        "marker": MARKER,
        "localizedBlocks": total,
        "byFile": by_file,
        "protected": [
            "Pokemon species names remain English",
            "Move names remain English",
            "Ability names remain English",
            "Celadon 5F mart inventories and clerk logic untouched",
            "METRONOME tutor logic untouched",
            "Lorelei flags and doll-update logic untouched",
            "Trainer data untouched",
            "Ash Bond/Ash Cap untouched",
        ],
    }
    out = root / "build" / "qarro_ru_dept_research_lorelei_v3_129_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {total} runtime blocks; mart/tutor/event/trainer/Ash logic untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
