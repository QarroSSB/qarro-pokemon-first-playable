#!/usr/bin/env python3
"""Qarro v3.102: localize remaining Celadon Gym, Mt. Moon 1F and Route 21 South runtime text.

Translates exactly the English-only runtime blocks still reported by the v3.101
RU surface audit in:
  * CeladonCity_Gym_Frlg: 23 blocks (Erika's story blocks stay untouched)
  * MtMoon_1F_Frlg: 23 blocks
  * Route21_South_Frlg: 23 blocks

Pokemon species, Move and Ability proper names remain English by project canon.
Gameplay logic, trainer data, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_CELADON_MTMOON_ROUTE21_V3_102"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES: dict[Path, dict[str, str]] = {
    Path("data/maps/CeladonCity_Gym_Frlg/scripts.inc"): {
        "CeladonCity_Gym_Text_KayIntro": "Расскажу тебе об этом ГИМЕ.\\pСюда допускают только\\nнастоящих леди!$",
        "CeladonCity_Gym_Text_KayDefeat": "Ты слишком груб!$",
        "CeladonCity_Gym_Text_KayPostBattle": "Буэ!\\nНадеюсь, ЭРИКА тебя разгромит!$",
        "CeladonCity_Gym_Text_BridgetIntro": "О, добро пожаловать.\\nМне уже стало скучно.$",
        "CeladonCity_Gym_Text_BridgetDefeat": "Мой макияж!$",
        "CeladonCity_Gym_Text_BridgetPostBattle": "ПОКЕМОНЫ типа GRASS сильны\\nпротив типа WATER.\\pТакже они сильны против\\nтипов ROCK и GROUND.$",
        "CeladonCity_Gym_Text_TinaIntro": "...Ты ведь подглядывал сюда\\nраньше?$",
        "CeladonCity_Gym_Text_TinaDefeat": "Вот это сюрприз!$",
        "CeladonCity_Gym_Text_TinaPostBattle": "О, ты смотрел на ЭРИКУ...\\nА не на меня...$",
        "CeladonCity_Gym_Text_TamiaIntro": "Смотри, смотри!\\nВот мои ПОКЕМОНЫ!\\pМне нравится тип GRASS.\\nИх легко растить.$",
        "CeladonCity_Gym_Text_TamiaDefeat": "Нет!$",
        "CeladonCity_Gym_Text_TamiaPostBattle": "В нашем ГИМЕ только ПОКЕМОНЫ\\nтипа GRASS.\\pПочему? Мы используем их и для\\nцветочных композиций!$",
        "CeladonCity_Gym_Text_LisaIntro": "О, привет!\\pМы не любим здесь ПОКЕМОНОВ\\nтипов BUG или FIRE!$",
        "CeladonCity_Gym_Text_LisaDefeat": "О!\\nТы!$",
        "CeladonCity_Gym_Text_LisaPostBattle": "Наш ЛИДЕР ЭРИКА тихая,\\nно здесь она знаменита.$",
        "CeladonCity_Gym_Text_LoriIntro": "Рада знакомству.\\nЯ люблю тренировать ПОКЕМОНОВ.$",
        "CeladonCity_Gym_Text_LoriDefeat": "О!\\nПрекрасно!$",
        "CeladonCity_Gym_Text_LoriPostBattle": "У меня скоро свидание вслепую.\\nНадо стать вежливее,\\lдаже во время боя.$",
        "CeladonCity_Gym_Text_MaryIntro": "Добро пожаловать\\nв ГИМ СЕЛАДОНА!\\pНе смей недооценивать\\nместных милых девушек.$",
        "CeladonCity_Gym_Text_MaryDefeat": "О!\\nПобеждена!$",
        "CeladonCity_Gym_Text_MaryPostBattle": "Я не взяла лучших ПОКЕМОНОВ.\\nВ следующий раз берегись!$",
        "CeladonCity_Gym_Text_GymStatue": "ГИМ ПОКЕМОНОВ СЕЛАДОНА\\nЛИДЕР: ЭРИКА\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}$",
        "CeladonCity_Gym_Text_GymStatuePlayerWon": "ГИМ ПОКЕМОНОВ СЕЛАДОНА\\nЛИДЕР: ЭРИКА\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}, {PLAYER}$",
    },
    Path("data/maps/MtMoon_1F_Frlg/scripts.inc"): {
        "MtMoon_1F_Text_MarcosIntro": "ОГО!\\nТы меня напугал!\\l...А, ты просто ребенок!$",
        "MtMoon_1F_Text_MarcosDefeat": "Ух ты!\\nСнова удивил!$",
        "MtMoon_1F_Text_MarcosPostBattle": "Таким детям, как ты, не стоит\\nбродить здесь в темноте.$",
        "MtMoon_1F_Text_JoshIntro": "Ты тоже пришел исследовать\\nпещеру?$",
        "MtMoon_1F_Text_JoshDefeat": "Проигрывать отстой!\\nСовсем не круто.$",
        "MtMoon_1F_Text_JoshPostBattle": "Я спустился сюда только затем,\\nчтобы покрасоваться\\lперед девочками.$",
        "MtMoon_1F_Text_MiriamIntro": "Ух ты! Здесь намного больше,\\nчем я думала!$",
        "MtMoon_1F_Text_MiriamDefeat": "Ой!\\nЯ проиграла!$",
        "MtMoon_1F_Text_MiriamPostBattle": "Как отсюда выбраться?\\nЗдесь так просторно,\\lчто можно заблудиться.$",
        "MtMoon_1F_Text_JovanIntro": "Что?!\\nНе подкрадывайся ко мне!$",
        "MtMoon_1F_Text_JovanDefeat": "Мои ПОКЕМОНЫ не справились!$",
        "MtMoon_1F_Text_JovanPostBattle": "Мне нужны ПОКЕМОНЫ посильнее.\\nГде бы их найти?$",
        "MtMoon_1F_Text_IrisIntro": "Что?\\nЯ жду, пока друзья найдут\\lменя здесь.$",
        "MtMoon_1F_Text_IrisDefeat": "Я проиграла?$",
        "MtMoon_1F_Text_IrisPostBattle": "Я пришла, потому что слышала:\\nздесь есть редкие\\lокаменелости.$",
        "MtMoon_1F_Text_KentIntro": "В пещере бродят\\nподозрительные люди.\\lА ты кто такой?$",
        "MtMoon_1F_Text_KentDefeat": "Ты меня поймал!$",
        "MtMoon_1F_Text_KentPostBattle": "Я их видел!\\nУверен, они из КОМАНДЫ R!$",
        "MtMoon_1F_Text_RobbyIntro": "Через эту пещеру нужно пройти,\\nчтобы попасть в СЕРУЛИН.$",
        "MtMoon_1F_Text_RobbyDefeat": "Я проиграл.$",
        "MtMoon_1F_Text_RobbyPostBattle": "ZUBAT крепкий!\\nНо если поймаешь одного,\\lна него можно положиться.$",
        "MtMoon_1F_Text_ZubatIsABloodsucker": "Осторожно!\\nZUBAT - кровосос!$",
        "MtMoon_1F_Text_BrockHelpsExcavateFossils": "Привет, я ищу окаменелости\\nпод МТ. МУН.\\pИногда БРОК из ГИМА ПЬЮТЕРА\\nпомогает мне.$",
    },
    Path("data/maps/Route21_South_Frlg/scripts.inc"): {
        "Route21_South_Text_JackIntro": "Я поймал ПОКЕМОНОВ в море.$",
        "Route21_South_Text_JackDefeat": "Нырок!!\\nНа дно!!$",
        "Route21_South_Text_JackPostBattle": "А где ты поймал ПОКЕМОНОВ?$",
        "Route21_South_Text_JeromeIntro": "Сейчас я участвую в триатлоне.$",
        "Route21_South_Text_JeromeDefeat": "Фух...\\nФух... Фух...$",
        "Route21_South_Text_JeromePostBattle": "Я выжат! Но впереди еще\\nвелогонка и марафон!$",
        "Route21_South_Text_RolandIntro": "Ах!\\nПочувствуй солнце и ветер!$",
        "Route21_South_Text_RolandDefeat": "Ай!\\nЯ проиграл!$",
        "Route21_South_Text_RolandPostBattle": "Я весь обгорел на солнце!$",
        "Route21_South_Text_ClaudeIntro": "Эй, не распугивай рыбу!$",
        "Route21_South_Text_ClaudeDefeat": "Извини! Я просто злюсь,\\nчто ничего не поймал.$",
        "Route21_South_Text_ClaudePostBattle": "Эх, я так ничего и не поймал.\\nМожет, это место вообще\\lогромный бассейн?$",
        "Route21_South_Text_NolanIntro": "Побудь со мной, пока клюнет.$",
        "Route21_South_Text_NolanDefeat": "Хоть время прошло.$",
        "Route21_South_Text_NolanPostBattle": "Погоди!\\nКлюет! Да!$",
        "Route21_North_Text_LilIntro": "ЛИЛ: А? Бой?\\nИАН, ты сам не справишься?$",
        "Route21_North_Text_LilDefeat": "ЛИЛ: Ну вот, видишь?\\nМы проиграли. Доволен?$",
        "Route21_North_Text_LilPostBattle": "ЛИЛ: Я устала.\\nМожет, уже пойдем домой?$",
        "Route21_North_Text_LilNotEnoughMons": "ЛИЛ: А? Бой?\\nМне лень драться одной.\\lПриведи двух ПОКЕМОНОВ, ладно?$",
        "Route21_North_Text_IanIntro": "ИАН: Сестра мало двигается,\\nпоэтому я привел ее сюда.$",
        "Route21_North_Text_IanDefeat": "ИАН: Ну вот, сестренка!\\nСоберись!$",
        "Route21_North_Text_IanPostBattle": "ИАН: Давай, сестренка!\\pТак ты точно не похудеешь!$",
        "Route21_North_Text_IanNotEnoughMons": "ИАН: Мы хотим бой два на два.\\nПриведи двух ПОКЕМОНОВ.$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/CeladonCity_Gym_Frlg/scripts.inc": 23,
    "data/maps/MtMoon_1F_Frlg/scripts.inc": 23,
    "data/maps/Route21_South_Frlg/scripts.inc": 23,
}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]


def asm_quote(text: str) -> str:
    return text.replace('"', '\\"')


def replace_block(text: str, label: str, translated: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: target already contains Cyrillic; refusing broad overwrite")
    if ".string " not in old:
        die(f"{label}: target does not look like a text block")
    block = f'{label}::\n\t.string "{asm_quote(translated)}"\n\n'
    return text[:start] + block + text[end:]


def validate_translation(label: str, translated: str) -> None:
    if not translated.endswith("$"):
        die(f"{label}: translated text must end with $")
    if any(ch in translated for ch in ("—", "–", "“", "”", "’")):
        die(f"{label}: unsupported Unicode punctuation")
    if "\\\\" in translated:
        die(f"{label}: doubled runtime backslash in translation value")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    total = 0
    by_file: dict[str, int] = {}

    for rel, patches in FILES.items():
        expected = EXPECTED_COUNTS[str(rel)]
        if len(patches) != expected:
            die(f"{rel}: expected {expected} patches in script, got {len(patches)}")
        path = root / rel
        if not path.is_file():
            die(f"missing source file: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in patches.items():
            validate_translation(label, translated)
            text = replace_block(text, label, translated)
        path.write_text(text, encoding="utf-8")
        by_file[str(rel)] = len(patches)
        total += len(patches)

    if total != 69:
        die(f"expected exactly 69 translated blocks, got {total}")

    for rel, patches in FILES.items():
        text = (root / rel).read_text(encoding="utf-8")
        for label in patches:
            _, _, block = block_bounds(text, label)
            if not re.search(r"[А-Яа-яЁё]", block):
                die(f"{label}: Cyrillic missing after replacement")
            if "\\\\n" in block or "\\\\p" in block or "\\\\l" in block:
                die(f"{label}: doubled FireRed runtime control escape after write")

    audit = {
        "marker": MARKER,
        "translatedBlockCount": total,
        "byFile": by_file,
        "scope": "remaining English-only Celadon Gym + Mt. Moon 1F + Route 21 South runtime text after v3.101",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "trainerDataTouched": False,
        "gameplayLogicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_celadon_mtmoon_route21_v3_102_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} runtime blocks across 3 files; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
