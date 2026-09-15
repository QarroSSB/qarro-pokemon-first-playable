#!/usr/bin/env python3
"""Qarro v3.127: localize Celadon Condominiums 1F and 3F runtime text.

Translates exactly 17 English-only FireRed text blocks after v3.126:
  * CeladonCity_Condominiums_1F_Frlg: 8
  * CeladonCity_Condominiums_3F_Frlg: 9

Tea gift/flags, Pokemon cries, Kanto Pokedex completion check, diploma special,
trainer data, Pokemon/Move/Ability proper-name policy, and Ash Bond/Ash Cap
are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_CELADON_CONDOMINIUMS_V3_127"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    "data/maps/CeladonCity_Condominiums_1F_Frlg/scripts.inc": {
        "CeladonCity_Condominiums_1F_Text_Meowth": "MEOWTH: Мяу!$",
        "CeladonCity_Condominiums_1F_Text_TryThisDrinkInstead": "Не стоит тратить все деньги\\nна напитки.\\pПопробуй лучше это.$",
        "CeladonCity_Condominiums_1F_Text_NothingBeatsThirstLikeTea": "Нет ничего лучше горячего\\nЧАЯ, когда мучает жажда.\\pОн и правда лучший.$",
        "CeladonCity_Condominiums_1F_Text_MyDearMonsKeepMeCompany": "Мои дорогие ПОКЕМОНЫ\\nсоставляют мне компанию.\\pMEOWTH даже приносит домой деньги!$",
        "CeladonCity_Condominiums_1F_Text_DaisyComesToBuyTea": "О, здравствуй.\\nТебе понравился мой ЧАЙ?\\pКстати, ты случайно\\nне из ПАЛЛЕТ-ТАУНА?\\pДевушка оттуда, DAISY,\\nпьёт ЧАЙ каждый день.\\pОна приходит в УНИВЕРМАГ CELADON,\\nчтобы купить ЧАЙ.$",
        "CeladonCity_Condominiums_1F_Text_Clefairy": "CLEFAIRY: Пи-пиппиппи!$",
        "CeladonCity_Condominiums_1F_Text_Nidoran": "NIDORAN♀: Кя-кяу!$",
        "CeladonCity_Condominiums_1F_Text_ManagersSuite": "ОСОБНЯК CELADON\\nКомната управляющего$",
    },
    "data/maps/CeladonCity_Condominiums_3F_Frlg/scripts.inc": {
        "CeladonCity_Condominiums_3F_Text_ImTheProgrammer": "Я?\\nЯ программист!$",
        "CeladonCity_Condominiums_3F_Text_ImTheGraphicArtist": "Я художник!\\nЭто я тебя нарисовал!$",
        "CeladonCity_Condominiums_3F_Text_IWroteTheStory": "Я написал сюжет!\\nРазве ЭРИКА не милая?\\pМИСТИ мне тоже очень нравится!\\nИ САБРИНА тоже!$",
        "CeladonCity_Condominiums_3F_Text_ImGameDesignerShowMeFinishedPokedex": "Вот как?\\pЯ геймдизайнер!\\pЗаполнить ПОКЕДЕКС нелегко,\\nно не сдавайся!\\pКогда закончишь, приходи ко мне!$",
        "CeladonCity_Condominiums_3F_Text_CompletedPokedexCongratulations": "Ого! Превосходно!\\nТы заполнил ПОКЕДЕКС!\\lПоздравляю!\\l...$",
        "CeladonCity_Condominiums_3F_Text_ItsTheGameProgram": "Это программа игры! Если её менять,\\nв игре могут появиться ошибки!$",
        "CeladonCity_Condominiums_3F_Text_SomeonesPlayingGame": "Кто-то играет вместо того,\\nчтобы работать!$",
        "CeladonCity_Condominiums_3F_Text_ItsScriptBetterNotLookAtEnding": "Это сценарий!\\nЛучше не смотреть концовку!$",
        "CeladonCity_Condominiums_3F_Text_GameFreakDevelopmentRoom": "Комната разработки GAME FREAK$",
    },
}
EXPECTED_TOTAL = 17


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
            "Tea gift and flags untouched",
            "Pokemon cry logic untouched",
            "Kanto Pokedex completion check and diploma special untouched",
            "Trainer data untouched",
            "Ash Bond/Ash Cap untouched",
        ],
    }
    out = root / "build" / "qarro_ru_celadon_condominiums_v3_127_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {total} runtime blocks; tea/diploma/trainer/Ash logic untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
