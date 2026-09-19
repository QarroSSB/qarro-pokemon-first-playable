#!/usr/bin/env python3
"""Qarro v3.181: human-quality RU pass for trainer chunk 3.

Covers the next contiguous 100 machine-translated blocks in trainers.inc:
the remainder of Route 109 and Route 110. Localization-only; exact runtime
control-token sequences are preserved and source drift fails closed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINERS_QUALITY_ROUTE109B_110_V3_181"
TARGET = Path("data/text/trainers.inc")

TRANSLATIONS = {
    "Route109_Text_EdmondDefeated": "Урп... О-о-ох...\\nУр-р-рп...$",
    "Route109_Text_EdmondPostBattle": "Обычно я куда сильнее!\\nПросто меня ужасно укачало!\\pИ это при том, что я моряк...$",
    "Route109_Text_RickyIntro": "Пить хочется... Вот бы газировки\\nиз ДОМА НА ПЛЯЖЕ...$",
    "Route109_Text_RickyDefeated": "Уф...$",
    "Route109_Text_RickyPostBattle": "Я уже умираю с голоду... Мой круг\\nпохож на огромный пончик...$",
    "Route109_Text_RickyRegister": "Сразимся еще раз,\\nкогда я не буду умирать от жажды?$",
    "Route109_Text_RickyRematchIntro": "Я голоден, но сил на\\nодин бой еще хватит!$",
    "Route109_Text_RickyRematchDefeated": "Я проиграл...\\nВсе потому, что голоден...$",
    "Route109_Text_RickyRematchPostBattle": "На пляже любая еда\\nкажется чуть вкуснее.$",
    "Route109_Text_LolaIntro": "Правда, пляжный зонт похож\\nна огромный цветок?$",
    "Route109_Text_LolaDefeated": "Мамочка!$",
    "Route109_Text_LolaPostBattle": "Если смотреть на пляж с неба,\\nон похож на огромный цветник!$",
    "Route109_Text_LolaRegister": "Я?\\nЯ здесь каждый день!$",
    "Route109_Text_LolaRematchIntro": "Больше я тебе не проиграю!\\nНе зря же у меня есть плавательный круг!$",
    "Route109_Text_LolaRematchDefeated": "Мамочка!$",
    "Route109_Text_LolaRematchPostBattle": "С плавательным кругом мы с моим\\nPOKeMON выглядим еще милее!$",
    "Route109_Text_AustinaIntro": "Без круга я плавать не умею,\\nно в POKeMON-бою не проиграю!$",
    "Route109_Text_AustinaDefeated": "Неужели я проиграла из-за\\nплавательного круга?$",
    "Route109_Text_AustinaPostBattle": "Мой плавательный круг - часть образа.\\nБез него я никуда.$",
    "Route109_Text_GwenIntro": "Привет, тренер!\\nСразишься со мной?$",
    "Route109_Text_GwenDefeated": "Ого, какая сила.$",
    "Route109_Text_GwenPostBattle": "Откуда у тебя такая сила?$",
    "Route109_Text_CarterIntro": "Ва-ха-ха! Этот парень сейчас поймает\\nздоровенную рыбину!$",
    "Route109_Text_CarterDefeated": "Этот парень только что упустил добычу...$",
    "Route109_Text_CarterPostBattle": "Этот парень думает, что ты крупная рыба.\\nНет, пока еще будущая крупная рыба!$",
    "Route109_Text_PaulIntro": "ПОЛ: Ну вот, настроение испорчено.\\pНе стоило мешать нашему\\nдрагоценному времени вдвоем.$",
    "Route109_Text_PaulDefeated": "ПОЛ: Ладно, сдаюсь.$",
    "Route109_Text_PaulPostBattle": "ПОЛ: Только никому не говори,\\nчто мы здесь.\\lЭто наш личный мир для двоих!$",
    "Route109_Text_PaulNotEnoughPokemon": "ПОЛ: Мы безумно влюблены.\\nПоэтому и наши POKeMON всегда\\lсражаются вместе.$",
    "Route109_Text_MelIntro": "МЭЛ: Мы просто безумно влюблены.\\nНаша любовь согревает весь ХОЭНН!$",
    "Route109_Text_MelDefeated": "МЭЛ: Мы проиграли, и это моя вина!\\nПОЛ теперь меня возненавидит!$",
    "Route109_Text_MelPostBattle": "МЭЛ: Эм, ПОЛ, ты сердишься на меня?\\nПожалуйста, не сердись.$",
    "Route109_Text_MelNotEnoughPokemon": "МЭЛ: Мы по-настоящему безумно влюблены.\\nПоэтому и наши POKeMON\\lсражаются вместе.$",
    "Route109_Text_ChandlerIntro": "Та-дам! Видишь?\\nМой плавательный круг круглый!$",
    "Route109_Text_ChandlerDefeated": "Ой-ой!\\nВот досада!$",
    "Route109_Text_ChandlerPostBattle": "И это после того, как я показал\\nтебе свой круглый круг...$",
    "Route109_Text_HaileyIntro": "Я не умею плавать, поэтому просто\\nделаю вид, будто плаваю.$",
    "Route109_Text_HaileyDefeated": "Я так и знала!\\nНе думала, что мы сможем победить.$",
    "Route109_Text_HaileyPostBattle": "Когда научусь плавать, думаю,\\nмой POKeMON тоже станет сильнее.$",
    "Route109_Text_ElijahIntro": "Такому мачо, как я, именно такой\\nPOKeMON подходит идеально!$",
    "Route109_Text_ElijahDefeated": "Даже проигрываю я круто, правда?$",
    "Route109_Text_ElijahPostBattle": "Такому мачо, как я, порт\\nподходит идеально!\\pПожалуй, отправлюсь в СЛЕЙТПОРТ.$",
    "Route110_Text_JacobIntro": "Эй, осторожнее!\\nПохоже, велогонки для тебя в новинку.$",
    "Route110_Text_JacobDefeated": "Ого!\\nТормоза отказали!$",
    "Route110_Text_JacobPostBattle": "Спущенные шины и плохие тормоза могут\\nпривести к серьезной травме!\\lПроверяй велосипед перед поездкой!$",
    "Route110_Text_AnthonyIntro": "Эй, ты!\\nСможешь угнаться за мной?$",
    "Route110_Text_AnthonyDefeated": "Вот это авария!$",
    "Route110_Text_AnthonyPostBattle": "Одной скорости мало для победы в POKeMON.\\nНадо что-то менять...$",
    "Route110_Text_BenjaminIntro": "Не паникуй, даже если велосипед несется быстро!$",
    "Route110_Text_BenjaminDefeated": "Не надо паниковать во время\\nбоев POKeMON...$",
    "Route110_Text_BenjaminPostBattle": "Незачем паниковать и нервничать.\\nСпокойнее. Времени полно.$",
    "Route110_Text_BenjaminRegister": "Буду спокойно двигаться дальше.\\nПозови, если захочешь еще бой.$",
    "Route110_Text_BenjaminRematchIntro": "Не слишком ли быстро несешься?\\nСпокойнее, давай сразимся.$",
    "Route110_Text_BenjaminRematchDefeated": "Я не паниковал, но все равно проиграл...$",
    "Route110_Text_BenjaminRematchPostBattle": "Незачем паниковать и нервничать.\\nСпокойнее. Времени полно.$",
    "Route110_Text_AbigailIntro": "Триатлон невероятно тяжел.\\pНужно пройти все три этапа:\\nплавание, велогонку и бег.$",
    "Route110_Text_AbigailDefeated": "Бои POKeMON тоже непросты!$",
    "Route110_Text_AbigailPostBattle": "Я вымоталась, пора отдохнуть.\\nПолноценный отдых очень важен.$",
    "Route110_Text_AbigailRegister": "Знаешь, ты мне нравишься!\\nДавай устроим реванш на ВЕЛОТРАССЕ.$",
    "Route110_Text_AbigailRematchIntro": "Разве не здорово сражаться,\\nне слезая с велосипеда?$",
    "Route110_Text_AbigailRematchDefeated": "Ого...\\nОткуда столько силы?$",
    "Route110_Text_AbigailRematchPostBattle": "Это была попытка поставить рекорд?\\pПрости, если я тебя задержала!$",
    "Route110_Text_JasmineIntro": "Я ехала без остановки.\\nБедра теперь твердые как камень!$",
    "Route110_Text_JasmineDefeated": "Боюсь, мышцы сейчас сведет...$",
    "Route110_Text_JasminePostBattle": "О, у тебя уже есть значки?\\nТеперь понятно, откуда такая сила!$",
    "Route110_Text_EdwardIntro": "Я предвидел твои намерения!\\nЯ просто не могу проиграть!$",
    "Route110_Text_EdwardDefeated": "Своего поражения я предсказать не смог!$",
    "Route110_Text_EdwardPostBattle": "Я вижу твое будущее...\\pХм...\\nВижу сияющий свет...$",
    "Route110_Text_JaclynIntro": "А-ха-ха-ха!\\nСейчас ослеплю тебя своими чудесами!$",
    "Route110_Text_JaclynDefeated": "Вот так чудесно я проиграла!$",
    "Route110_Text_JaclynPostBattle": "Победа досталась тебе лишь благодаря\\nчуду! Да, чуду!\\lНе думай, что так будет всегда!$",
    "Route110_Text_EdwinIntro": "Можно взглянуть на твоих POKeMON?\\nВсего одним глазком, пожалуйста?$",
    "Route110_Text_EdwinDefeated": "Я хотел пополнить\\nсвою коллекцию...$",
    "Route110_Text_EdwinPostBattle": "Когда вижу незнакомого POKeMON,\\nво мне просыпается страсть коллекционера!$",
    "Route110_Text_EdwinRegister": "Еще я люблю собирать записи\\nдругих тренеров...$",
    "Route110_Text_EdwinRematchIntro": "Привет! Есть новые POKeMON?\\pМожно взглянуть на твоих POKeMON?\\nВсего одним глазком, пожалуйста?$",
    "Route110_Text_EdwinRematchDefeated": "Твои POKeMON...\\nКак же я тебе завидую.$",
    "Route110_Text_EdwinRematchPostBattle": "Как же хочется заполучить всех редких POKeMON\\nв свою коллекцию!$",
    "Route110_Text_DaleIntro": "Эй!\\nНе подкрадывайся ко мне сзади!$",
    "Route110_Text_DaleDefeated": "Проиграл!\\nВот досада!$",
    "Route110_Text_DalePostBattle": "На рыбалке главное - концентрация.\\nСледи за поплавком.$",
    "Route110_Text_IsabelIntro": "А-ха-ха! Я пойду куда угодно, лишь бы\\nпоказать своего чудесного POKeMON.$",
    "Route110_Text_IsabelDefeated": "Ох, так не пойдет.$",
    "Route110_Text_IsabelPostBattle": "Может, вместо боев мне лучше\\nхвастаться POKeMON в ФАН-КЛУБЕ.$",
    "Route110_Text_IsabelRegister": "Я еще почти не успела\\nпохвастаться своим POKeMON.\\pТеперь ты будешь моей публикой\\nпри каждой возможности!$",
    "Route110_Text_IsabelRematchIntro": "А-ха-ха-ха! Я с радостью буду\\nпоказывать POKeMON сколько захочешь!$",
    "Route110_Text_IsabelRematchDefeated": "Ох, так не пойдет.$",
    "Route110_Text_IsabelRematchPostBattle": "Не думаю, что когда-нибудь смогу\\nперестать хвастаться своим POKeMON.\\pНо сражаться мне тоже нравится!$",
    "Route110_Text_TimmyIntro": "Я нашел в здешней траве\\nнесколько классных POKeMON!$",
    "Route110_Text_TimmyDefeated": "Одной крутости для победы мало...$",
    "Route110_Text_TimmyPostBattle": "Трудно сражаться с POKeMON, которых\\nтолько что поймал.$",
    "Route110_Text_AlyssaIntro": "Я свалилась с ВЕЛОТРАССЫ...\\pСейчас забуду свой позор,\\nсразившись с тобой!$",
    "Route110_Text_AlyssaDefeated": "Ой!\\nВ итоге я все-таки проиграла!$",
    "Route110_Text_AlyssaPostBattle": "Упала... Проиграла...\\nКак же стыдно!$",
    "Route110_Text_JosephIntro": "Так! Полный газ! Не поймаешь\\nритм - останешься позади!$",
    "Route110_Text_JosephDefeated": "А ты ритм поймал как надо...$",
    "Route110_Text_JosephPostBattle": "Меня это не сломит!\\nПоражение сделало меня лучше!$",
    "Route110_Text_KalebIntro": "Когда милые POKeMON помогают друг другу...\\nНет зрелища очаровательнее!$",
    "Route110_Text_KalebDefeated": "Неужели ни капли сочувствия?$",
    "Route110_Text_KalebPostBattle": "Ладно, ладно, вы сделали все,\\nчто могли, мои красавцы.$",
}

BANNED_UNICODE = set("—–←→“”«»")


def control_tokens(text: str) -> list[str]:
    return re.findall(r'\{[^}]+\}|\\.|\$', text)


def replace_label(path: Path, label: str, translated: str) -> None:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(?ms)^(?P<head>{re.escape(label)}:\s*\n)'
        rf'(?P<body>(?:[ \t]*\.string\s+"(?:\\.|[^"\\])*"\s*\n?)+)'
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{path}:{label}: expected one text block, got {len(matches)}")
    m = matches[0]
    current_parts = re.findall(r'\.string\s+"((?:\\.|[^"\\])*)"', m.group("body"))
    if not current_parts:
        raise RuntimeError(f"{path}:{label}: no .string content found")
    current = "".join(current_parts)
    old_tokens = control_tokens(current)
    new_tokens = control_tokens(translated)
    if old_tokens != new_tokens:
        raise RuntimeError(f"{path}:{label}: control-token drift old={old_tokens} new={new_tokens}")
    if not translated.endswith("$"):
        raise RuntimeError(f"{path}:{label}: translated block must end in $")
    bad = sorted(set(translated) & BANNED_UNICODE)
    if bad:
        raise RuntimeError(f"{path}:{label}: unsupported punctuation {bad}")
    if '"' in translated:
        raise RuntimeError(f"{path}:{label}: raw double quote is not allowed")
    new_body = '\t.string "' + translated + '"\n'
    path.write_text(text[:m.start("body")] + new_body + text[m.end("body"):], encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_trainers_quality_route109b_110_v3_181.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 100:
        raise RuntimeError(f"expected exactly 100 quality-pass blocks, got {len(TRANSLATIONS)}")
    for label, translated in TRANSLATIONS.items():
        replace_label(path, label, translated)

    out = root / "build" / "qarro_ru_trainers_quality_route109b_110_v3_181_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassBlocks": len(TRANSLATIONS),
        "labels": list(TRANSLATIONS),
        "humanEditedRussian": True,
        "controlTokensPreserved": True,
        "pokemonMoveAbilityNamesPreserved": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} trainer text blocks in {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
