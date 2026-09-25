#!/usr/bin/env python3
"""Qarro v3.100: localize remaining Cinnabar/Viridian Gym + Route 25 runtime text.

Translates exactly the English-only runtime blocks still reported by the v3.99
RU surface audit in:
  * CinnabarIsland_Gym_Frlg: 34 blocks (Blaine's 7 story blocks stay untouched)
  * Route25_Frlg: 30 blocks (Bill quest blocks stay untouched)
  * ViridianCity_Gym_Frlg: 28 blocks (Giovanni's 7 story blocks stay untouched)

Pokemon species, Move and Ability proper names remain English by project canon.
Gameplay logic, trainer data, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_GYMS_ROUTE25_V3_100"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES: dict[Path, dict[str, str]] = {
    Path("data/maps/CinnabarIsland_Gym_Frlg/scripts.inc"): {
        "CinnabarIsland_Gym_Text_ErikIntro": "Ты знаешь, насколько горячим\\nбывает огненное дыхание ПОКЕМОНА?$",
        "CinnabarIsland_Gym_Text_ErikDefeat": "Ай!\\nГорячо, горячо, горячо!$",
        "CinnabarIsland_Gym_Text_ErikPostBattle": "Огонь, а точнее - горение...\\p...Кислород в воздухе...\\nБла-бла-бла-бла...$",
        "CinnabarIsland_Gym_Text_QuinnIntro": "Раньше я был вором, но исправился\\nи стал ТРЕНЕРОМ.$",
        "CinnabarIsland_Gym_Text_QuinnDefeat": "Сдаюсь!$",
        "CinnabarIsland_Gym_Text_QuinnPostBattle": "У меня бывает неудержимое желание\\nукрасть чужого ПОКЕМОНА.$",
        "CinnabarIsland_Gym_Text_AveryIntro": "Я досконально изучил ПОКЕМОНОВ.\\nТебе не победить!$",
        "CinnabarIsland_Gym_Text_AveryDefeat": "А-а!\\nМоих знаний оказалось мало!$",
        "CinnabarIsland_Gym_Text_AveryPostBattle": "Мои теории слишком сложны,\\nтебе их не понять.$",
        "CinnabarIsland_Gym_Text_RamonIntro": "Мне нравятся ПОКЕМОНЫ типа FIRE.\\nПросто нравятся.$",
        "CinnabarIsland_Gym_Text_RamonDefeat": "Слишком горячо!$",
        "CinnabarIsland_Gym_Text_RamonPostBattle": "Жаль, что нет ПОКЕМОНА-вора.\\nЯ бы его использовал!$",
        "CinnabarIsland_Gym_Text_DerekIntro": "Я знаю, почему БЛЕЙН стал\\nТРЕНЕРОМ.$",
        "CinnabarIsland_Gym_Text_DerekDefeat": "Ай!$",
        "CinnabarIsland_Gym_Text_DerekPostBattle": "Наш ЛИДЕР БЛЕЙН однажды совсем\\nзаблудился в горах.\\pНаступила ночь, и появился\\nогненный птице-ПОКЕМОН.\\pЕго свет помог БЛЕЙНУ\\nбезопасно спуститься.$",
        "CinnabarIsland_Gym_Text_DustyIntro": "Я побывал во многих ГИМАХ,\\nно этот лучше всего подходит мне.$",
        "CinnabarIsland_Gym_Text_DustyDefeat": "Ух!\\nСлишком горячо!$",
        "CinnabarIsland_Gym_Text_DustyPostBattle": "PONYTA, NINETALES...\\nПопулярные ПОКЕМОНЫ типа FIRE.$",
        "CinnabarIsland_Gym_Text_ZacIntro": "Огонь слаб против H2O.$",
        "CinnabarIsland_Gym_Text_ZacDefeat": "Ох!\\nПогас!$",
        "CinnabarIsland_Gym_Text_ZacPostBattle": "Конечно, вода побеждает огонь.\\pНо огонь плавит лед, поэтому FIRE\\nсильнее ПОКЕМОНОВ типа ICE.$",
        "CinnabarIsland_Gym_Text_GymGuyAdvice": "Йо!\\nБудущий чемпион!\\pГорячий БЛЕЙН - профи по\\nПОКЕМОНАМ типа FIRE.\\pОхлади его пыл водой!\\pИ прихвати с собой\\nЛЕКАРСТВА ОТ ОЖОГА.$",
        "CinnabarIsland_Gym_Text_GymGuyPostVictory": "{PLAYER}!\\nТы победил этого огненного парня!$",
        "CinnabarIsland_Gym_Text_GymStatue": "ГИМ ПОКЕМОНОВ СИННАБАРА\\nЛИДЕР: БЛЕЙН\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}$",
        "CinnabarIsland_Gym_Text_GymStatuePlayerWon": "ГИМ ПОКЕМОНОВ СИННАБАРА\\nЛИДЕР: БЛЕЙН\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}, {PLAYER}$",
        "CinnabarIsland_Gym_Text_PokemonQuizRules": "Викторина о ПОКЕМОНАХ!\\pОтветишь правильно - дверь\\nв следующую комнату откроется.\\pОшибешься - сразишься с ТРЕНЕРОМ!\\pХочешь поберечь ПОКЕМОНОВ\\nдля ЛИДЕРА ГИМА...\\pТогда отвечай правильно!\\nНачинаем!$",
        "CinnabarIsland_Gym_Text_QuizQuestion1": "CATERPIE эволюционирует\\nв METAPOD?$",
        "CinnabarIsland_Gym_Text_QuizQuestion2": "Существует девять официальных\\nЗНАЧКОВ ЛИГИ ПОКЕМОНОВ?$",
        "CinnabarIsland_Gym_Text_QuizQuestion3": "POLIWAG эволюционирует трижды?$",
        "CinnabarIsland_Gym_Text_QuizQuestion4": "Атаки ELECTRIC эффективны\\nпротив ПОКЕМОНОВ типа GROUND?$",
        "CinnabarIsland_Gym_Text_QuizQuestion5": "ПОКЕМОНЫ одного вида и уровня\\nне обязательно одинаковы?$",
        "CinnabarIsland_Gym_Text_QuizQuestion6": "В TM28 находится TOMBSTONY?$",
        "CinnabarIsland_Gym_Text_CorrectGoOnThrough": "Совершенно верно!\\pПроходи дальше!$",
        "CinnabarIsland_Gym_Text_SorryBadCall": "Извини!\\nНеверный ответ!$",
    },
    Path("data/maps/Route25_Frlg/scripts.inc"): {
        "Route25_Text_JoeyIntro": "Местные ТРЕНЕРЫ приходят сюда\\nтренироваться.$",
        "Route25_Text_JoeyDefeat": "Ты неплох.$",
        "Route25_Text_JoeyPostBattle": "У всех ПОКЕМОНОВ есть слабости.\\nДаже у самых сильных.\\pПоэтому лучше растить ПОКЕМОНОВ\\nразных типов.$",
        "Route25_Text_DanIntro": "Папа водил меня на отличную вечеринку\\nна S.S. ANNE в ВЕРМИЛИОНЕ.$",
        "Route25_Text_DanDefeat": "Я не злюсь!$",
        "Route25_Text_DanPostBattle": "На S.S. ANNE я видел ТРЕНЕРОВ\\nсо всего мира.$",
        "Route25_Text_FlintIntro": "Я крутой парень.\\nИ у меня есть девушка!$",
        "Route25_Text_FlintDefeat": "Эх, черт...$",
        "Route25_Text_FlintPostBattle": "Ну и ладно.\\nМоя девушка меня подбодрит.$",
        "Route25_Text_KelseyIntro": "Привет!\\nМой парень такой крутой!$",
        "Route25_Text_KelseyDefeat": "Я сегодня не в лучшей форме...$",
        "Route25_Text_KelseyPostBattle": "Хотела бы я, чтобы мой парень\\nсражался так же хорошо, как ты.$",
        "Route25_Text_ChadIntro": "У меня было предчувствие...\\nЯ знал, что должен с тобой сразиться!$",
        "Route25_Text_ChadDefeat": "Я и поражение предчувствовал!$",
        "Route25_Text_ChadPostBattle": "Если твой ПОКЕМОН запутался,\\nсмени его.\\pЭто хорошая тактика.$",
        "Route25_Text_HaleyIntro": "У моей подруги много милых ПОКЕМОНОВ.\\nЯ так ей завидую!$",
        "Route25_Text_HaleyDefeat": "Теперь уже не так завидую!$",
        "Route25_Text_HaleyPostBattle": "Ты пришел с МТ. МУН?\\nМожно мне CLEFAIRY?$",
        "Route25_Text_FranklinIntro": "Я только что спустился с МТ. МУН,\\nно сил у меня еще полно!$",
        "Route25_Text_FranklinDefeat": "Ты хорошо постарался!$",
        "Route25_Text_FranklinPostBattle": "Вот досада!\\nВ той пещере меня укусил ZUBAT.$",
        "Route25_Text_NobIntro": "Я иду посмотреть коллекцию\\nПОКЕМАНЬЯКА на мысе.$",
        "Route25_Text_NobDefeat": "Ты меня здорово одолел!$",
        "Route25_Text_NobPostBattle": "ПОКЕМАНЬЯК полностью оправдывает\\nсвое прозвище.\\pВ его коллекции много редких\\nвидов ПОКЕМОНОВ.$",
        "Route25_Text_WayneIntro": "Идешь к БИЛЛУ?\\nСначала сразимся!$",
        "Route25_Text_WayneDefeat": "А ты хорош.$",
        "Route25_Text_WaynePostBattle": "Тропа внизу - короткий путь\\nв СЕРУЛИН.$",
        "Route25_Text_SeaCottageSign": "МОРСКОЙ ДОМ\\nЗдесь живет БИЛЛ!$",
        "Route25_Text_MistyHighHopesAboutThisPlace": "Этот мыс - знаменитое место для свиданий.\\pМИСТИ, ЛИДЕР ГИМА, очень\\nлюбит это место.$",
        "Route25_Text_AreYouHereAlone": "Привет, ты здесь один?\\pЕсли уж пришел на мыс СЕРУЛИНА...\\nЛучше приходить сюда вдвоем.$",
    },
    Path("data/maps/ViridianCity_Gym_Frlg/scripts.inc"): {
        "ViridianCity_Gym_Text_YujiIntro": "Хех!\\nНаверняка ты уже выдыхаешься!$",
        "ViridianCity_Gym_Text_YujiDefeat": "У меня кончились силы!$",
        "ViridianCity_Gym_Text_YujiPostBattle": "Тебе понадобится мощь, чтобы\\nтягаться с нашим ЛИДЕРОМ ГИМА.$",
        "ViridianCity_Gym_Text_AtsushiIntro": "Р-р-р-рев!\\nЯ довожу себя до ярости!$",
        "ViridianCity_Gym_Text_AtsushiDefeat": "Аргх!$",
        "ViridianCity_Gym_Text_AtsushiPostBattle": "Я все еще недостоин!$",
        "ViridianCity_Gym_Text_JasonIntro": "Мы с моими ПОКЕМОНАМИ создаем\\nпрекрасную музыку вместе!$",
        "ViridianCity_Gym_Text_JasonDefeat": "У тебя идеальная гармония!$",
        "ViridianCity_Gym_Text_JasonPostBattle": "Ты знаешь, кто на самом деле\\nнаш ЛИДЕР ГИМА?$",
        "ViridianCity_Gym_Text_KiyoIntro": "Карате - высшая форма\\nбоевых искусств!$",
        "ViridianCity_Gym_Text_KiyoDefeat": "Ай-я!$",
        "ViridianCity_Gym_Text_KiyoPostBattle": "Если бы мои ПОКЕМОНЫ владели\\nкарате так же хорошо, как я...$",
        "ViridianCity_Gym_Text_WarrenIntro": "Настоящий талант побеждает стильно.$",
        "ViridianCity_Gym_Text_WarrenDefeat": "Я потерял хватку!$",
        "ViridianCity_Gym_Text_WarrenPostBattle": "ЛИДЕР отругает меня\\nза такое поражение...$",
        "ViridianCity_Gym_Text_TakashiIntro": "Я КОРОЛЬ КАРАТЕ!\\nТвоя судьба в моих руках!$",
        "ViridianCity_Gym_Text_TakashiDefeat": "Ай-я!$",
        "ViridianCity_Gym_Text_TakashiPostBattle": "ЛИГА ПОКЕМОНОВ?\\nТы? Не зазнавайся!$",
        "ViridianCity_Gym_Text_ColeIntro": "Твои ПОКЕМОНЫ задрожат\\nот щелчка моего кнута!$",
        "ViridianCity_Gym_Text_ColeDefeat": "Ай!\\nВот это удар!$",
        "ViridianCity_Gym_Text_ColePostBattle": "Постой!\\nЯ просто был неосторожен!$",
        "ViridianCity_Gym_Text_SamuelIntro": "ГИМ ВИРИДИАНА долго был закрыт.\\pНо теперь наш ЛИДЕР вернулся!$",
        "ViridianCity_Gym_Text_SamuelDefeat": "Меня победили?$",
        "ViridianCity_Gym_Text_SamuelPostBattle": "Ты попадешь в ЛИГУ ПОКЕМОНОВ\\nтолько победив нашего\\lЛИДЕРА ГИМА!$",
        "ViridianCity_Gym_Text_GymGuyAdvice": "Йо!\\nБудущий чемпион!\\pДаже я не знаю, кто ЛИДЕР\\nВИРИДИАНА.\\pНо одно известно точно.\\nЭто будет самый тяжелый\\lиз всех ЛИДЕРОВ ГИМОВ.\\pИ еще я слышал, что ТРЕНЕРЫ\\nздесь любят ПОКЕМОНОВ типа GROUND.$",
        "ViridianCity_Gym_Text_GymGuyPostVictory": "Ничего себе! ГИОВАННИ был\\nЛИДЕРОМ ГИМА ВИРИДИАНА?$",
        "ViridianCity_Gym_Text_GymStatue": "ГИМ ПОКЕМОНОВ ВИРИДИАНА\\nЛИДЕР: ?\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}$",
        "ViridianCity_Gym_Text_GymStatuePlayerWon": "ГИМ ПОКЕМОНОВ ВИРИДИАНА\\nЛИДЕР: ГИОВАННИ\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}, {PLAYER}$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/CinnabarIsland_Gym_Frlg/scripts.inc": 34,
    "data/maps/Route25_Frlg/scripts.inc": 30,
    "data/maps/ViridianCity_Gym_Frlg/scripts.inc": 28,
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

    if total != 92:
        die(f"expected exactly 92 translated blocks, got {total}")

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
        "scope": "remaining English-only Cinnabar Gym + Route 25 + Viridian Gym runtime text after v3.99",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "trainerDataTouched": False,
        "gameplayLogicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_gyms_route25_v3_100_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} runtime blocks across 3 files; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
