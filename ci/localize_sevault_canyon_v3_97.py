#!/usr/bin/env python3
"""Qarro v3.97: Russian runtime localization for Sevault Canyon and entrance.

Translates the 49 remaining English-only FireRed runtime text blocks in:
- SevenIsland_SevaultCanyon_Frlg (28)
- SevenIsland_SevaultCanyon_Entrance_Frlg (21)

Pokemon / Move / Ability proper names remain English by project canon.
Ash Bond / Ash Cap are not referenced or changed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_SEVAULT_CANYON_V3_97"

FILES = {
    Path("data/maps/SevenIsland_SevaultCanyon_Frlg/scripts.inc"): {
        "SevenIsland_SevaultCanyon_Text_CyndyIntro": ["Я в отличной форме!$"],
        "SevenIsland_SevaultCanyon_Text_CyndyDefeat": ["Что?\\n", "Что-то не так...$"],
        "SevenIsland_SevaultCanyon_Text_CyndyPostBattle": ["В таком состоянии мне лучше\\n", "пока не идти в БАШНЮ ТРЕНЕРОВ...$"],
        "SevenIsland_SevaultCanyon_Text_EvanIntro": ["Неважно, есть ли у тебя\\n", "самые сильные ПОКЕМОНЫ...\\p", "Если не умеешь ими пользоваться,\\n", "они тебе не помогут!$"],
        "SevenIsland_SevaultCanyon_Text_EvanDefeat": ["Ты настоящий мастер.$"],
        "SevenIsland_SevaultCanyon_Text_EvanPostBattle": ["Иногда встречаются ТРЕНЕРЫ\\n", "с отличными ПОКЕМОНАМИ,\\l", "но совсем не знают, что делать.\\p", "Прежде чем растить ПОКЕМОНОВ,\\n", "самому ТРЕНЕРУ надо повзрослеть.$"],
        "SevenIsland_SevaultCanyon_Text_JacksonIntro": ["Я защищаю природу.\\n", "А природа защищает меня!$"],
        "SevenIsland_SevaultCanyon_Text_JacksonDefeat": ["Ого! Ты силён!\\n", "Может, защитишь и меня?$"],
        "SevenIsland_SevaultCanyon_Text_JacksonPostBattle": ["Издалека среди звёзд наша\\n", "планета - лишь капля воды.\\p", "Но мы хотим сохранить эту каплю\\n", "для всех.$"],
        "SevenIsland_SevaultCanyon_Text_KatelynIntro": ["Какие у тебя классные\\n", "ботинки.$"],
        "SevenIsland_SevaultCanyon_Text_KatelynDefeat": ["Ты очень крут, несмотря на\\n", "милую внешность.$"],
        "SevenIsland_SevaultCanyon_Text_KatelynPostBattle": ["Мама купила тебе эти классные\\n", "БЕГОВЫЕ БОТИНКИ?\\p", "Наверное, она тебя обожает.$"],
        "SevenIsland_SevaultCanyon_Text_LeroyIntro": ["Ты выглядишь сильным.\\n", "Сразись со мной, пожалуйста!$"],
        "SevenIsland_SevaultCanyon_Text_LeroyDefeat": ["Я так и знал!\\n", "Ты именно такой сильный!$"],
        "SevenIsland_SevaultCanyon_Text_LeroyPostBattle": ["Твой стиль боя дал мне\\n", "много полезных данных.\\p", "Большое спасибо!$"],
        "SevenIsland_SevaultCanyon_Text_MichelleIntro": ["Мне дали лучшее обучение,\\n", "чтобы я стала сильной.\\p", "Я не хочу никому проигрывать!$"],
        "SevenIsland_SevaultCanyon_Text_MichelleDefeat": ["Спасибо. После поражения от тебя\\n", "я будто стала свободнее.$"],
        "SevenIsland_SevaultCanyon_Text_MichellePostBattle": ["Почему-то я бешусь из-за\\n", "любого пустяка.\\p", "Успокоюсь и сделаю несколько\\n", "глубоких вдохов.$"],
        "SevenIsland_SevaultCanyon_Text_LexIntro": ["ЛЕКС: Моя дорогая НЬЯ, вместе\\n", "мы сможем победить!$"],
        "SevenIsland_SevaultCanyon_Text_LexDefeat": ["ЛЕКС: Похоже, я был слишком\\n", "беспечен...$"],
        "SevenIsland_SevaultCanyon_Text_LexPostBattle": ["ЛЕКС: Думаю, для НЬИ это был\\n", "полезный опыт.\\p", "Благодарю тебя.$"],
        "SevenIsland_SevaultCanyon_Text_LexNotEnoughMons": ["ЛЕКС: Можно попросить тебя\\n", "сразиться сразу с нами обоими?$"],
        "SevenIsland_SevaultCanyon_Text_NyaIntro": ["НЬЯ: Я постараюсь не подвести\\n", "моего наставника ЛЕКСА!$"],
        "SevenIsland_SevaultCanyon_Text_NyaDefeat": ["НЬЯ: О нет...\\n", "Мне так жаль, я...$"],
        "SevenIsland_SevaultCanyon_Text_NyaPostBattle": ["НЬЯ: Мне ещё многому нужно\\n", "научиться у ЛЕКСА...\\p", "ЛЕКС, пожалуйста, можно мне\\n", "и дальше учиться у тебя?$"],
        "SevenIsland_SevaultCanyon_Text_NyaNotEnoughMons": ["НЬЯ: Извини, но можно провести\\n", "бой два на два?$"],
        "SevenIsland_SevaultCanyon_Text_RouteSign": ["КАНЬОН СЕВО\\n", "ВПЕРЕДИ РУИНЫ ТАНОБИ$"],
        "SevenIsland_SevaultCanyon_Text_BrunoTrainedWithBrawly": ["Тренироваться одному совсем\\n", "неплохо.\\p", "Но и стремиться к вершине\\n", "с напарником тоже полезно.\\p", "Даже БРУНО когда-то тренировался\\n", "вместе с БРОЛИ.$"],
    },
    Path("data/maps/SevenIsland_SevaultCanyon_Entrance_Frlg/scripts.inc"): {
        "SevenIsland_SevaultCanyon_Entrance_Text_MiahIntro": ["Кья-ха-ха!\\n", "Я легко смету тебя с пути!$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_MiahDefeat": ["Тц!\\n", "Ты слишком силён для меня!$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_MiahPostBattle": ["Что такое?\\n", "Я веду себя не так, как выгляжу?\\p", "Хех, это часть моей стратегии!$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_MasonIntro": ["Привет!\\n", "Ты состоишь в моём фан-клубе?$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_MasonDefeat": ["О, значит, ты не мой фанат...\\p", "Ничего, это можно исправить.\\n", "Дай я тебе спою!$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_MasonPostBattle": ["Ла-ла-ла...\\n", "Я выпускаю ПОКЕМОНОВ,\\l", "а девушки кричат от восторга!$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_NicolasIntro": ["Остров слишком большой...\\n", "Патрулировать его нелегко.$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_NicolasDefeat": ["Угу...$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_NicolasPostBattle": ["ТРЕНЕРЫ из больших городов\\n", "и правда сильны.\\p", "Ты ведь направляешься\\n", "к БАШНЕ, верно?$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_MadelineIntro": ["Я наказываю тех, кто плохо\\n", "обращается с ПОКЕМОНАМИ!$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_MadelineDefeat": ["Похоже, ты не из тех ТРЕНЕРОВ,\\n", "которые причиняют им вред.$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_MadelinePostBattle": ["Если относиться к ПОКЕМОНАМ\\n", "с добротой, они всё поймут.$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_EveIntro": ["ИВ: Мы с ДЖОНОМ объединимся\\n", "и будем сражаться вместе.$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_EveDefeat": ["ИВ: Мы с ДЖОНОМ проиграли.\\n", "Хе-хе.$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_EvePostBattle": ["ИВ: Мы с ДЖОНОМ будем\\n", "тренироваться ещё усерднее.$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_EveNotEnoughMons": ["ИВ: Я хочу сражаться вместе\\n", "с ДЖОНОМ.\\p", "Возвращайся с двумя\\n", "ПОКЕМОНАМИ, хорошо?$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_JonIntro": ["ДЖОН: Когда я рядом с ИВ,\\n", "кажется, мы непобедимы.$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_JonDefeat": ["ДЖОН: Когда я рядом с ИВ,\\n", "даже поражение не ощущается!$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_JonPostBattle": ["ДЖОН: Рядом с ИВ я счастлив,\\n", "неважно, победил или проиграл.\\p", "Это настоящее волшебство!$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_JonNotEnoughMons": ["ДЖОН: С ИВ я с радостью\\n", "сражусь с тобой.\\p", "Но давай устроим бой\\n", "два на два.$"],
        "SevenIsland_SevaultCanyon_Entrance_Text_RouteSign": ["ВХОД В КАНЬОН СЕВО\\p", "Просьба к ТРЕНЕРАМ не повреждать\\n", "растения в КАНЬОНЕ.$"],
    },
}


def render(label: str, lines: list[str]) -> str:
    out = [f"{label}::"]
    for line in lines:
        # FireRed control codes are already represented as a single literal backslash
        # in the runtime string value; only quotes require escaping here.
        escaped = line.replace('"', '\\"')
        out.append(f'\t.string "{escaped}"')
    return "\n".join(out) + "\n"


def replace_block(text: str, label: str, lines: list[str]) -> str:
    pattern = re.compile(rf"^{re.escape(label)}::\n(?:\t\.string [^\n]*(?:\n|$))+", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"[{MARKER}] {label}: expected exactly one text block, found {len(matches)}")
    old = matches[0].group(0)
    if re.search(r"[А-Яа-яЁё]", old):
        raise SystemExit(f"[{MARKER}] {label}: source block is already Cyrillic; refusing double patch")
    return text[:matches[0].start()] + render(label, lines) + text[matches[0].end():]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    per_file = {}
    total = 0
    for rel, patches in FILES.items():
        path = root / rel
        if not path.is_file():
            raise SystemExit(f"[{MARKER}] missing source file: {rel}")
        text = path.read_text(encoding="utf-8")
        for label, lines in patches.items():
            text = replace_block(text, label, lines)
        path.write_text(text, encoding="utf-8")
        per_file[str(rel)] = len(patches)
        total += len(patches)
    if total != 49:
        raise SystemExit(f"[{MARKER}] expected 49 translations, got {total}")
    audit = {
        "marker": MARKER,
        "translatedBlockCount": total,
        "byFile": per_file,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build" / "qarro_ru_sevault_canyon_v3_97_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} Sevault Canyon runtime blocks; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
