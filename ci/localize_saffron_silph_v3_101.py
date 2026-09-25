#!/usr/bin/env python3
"""Qarro v3.101: localize remaining Silph 7F, Saffron City and Saffron Gym runtime text.

Translates exactly the English-only runtime blocks still reported by the v3.100
RU surface audit in:
  * SilphCo_7F_Frlg: 27 blocks
  * SaffronCity_Frlg: 25 blocks
  * SaffronCity_Gym_Frlg: 25 blocks (Sabrina's authored story blocks stay untouched)

Pokemon species, Move and Ability proper names remain English by project canon.
Gameplay logic, trainer data, Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_SAFFRON_SILPH_V3_101"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES: dict[Path, dict[str, str]] = {
    Path("data/maps/SilphCo_7F_Frlg/scripts.inc"): {
        "SilphCo_7F_Text_HaveMonForSavingUs": "О! Привет! Ты не из КОМАНДЫ R!\\nТы пришел нас спасти?\\lСпасибо тебе!\\pЯ хочу отдать тебе этого ПОКЕМОНА\\nза наше спасение.$",
        "SilphCo_7F_Text_ObtainedLaprasFromEmployee": "{PLAYER} получил LAPRAS\\nот сотрудника СИЛФ!$",
        "SilphCo_7F_Text_ExplainLapras": "Это LAPRAS.\\nОчень умный ПОКЕМОН.\\pМы держали его в лаборатории, но\\nс тобой ему будет гораздо лучше.\\pДумаю, ты станешь хорошим\\nТРЕНЕРОМ для LAPRAS!\\pОн отлично плавает.\\nИ сможет перевозить тебя по воде!$",
        "SilphCo_7F_Text_RocketBossWentToBoardroom": "БОСС КОМАНДЫ R ушел\\nв зал совета!\\pС нашим ПРЕЗИДЕНТОМ все в порядке?\\nЯ волнуюсь.$",
        "SilphCo_7F_Text_RocketsAfterMasterBall": "КОМАНДА R охотилась за\\nМАСТЕР-БОЛЛОМ, который ловит любого ПОКЕМОНА.$",
        "SilphCo_7F_Text_CanceledMasterBallProject": "Мы закрыли проект МАСТЕР-БОЛЛА\\nиз-за КОМАНДЫ R.$",
        "SilphCo_7F_Text_BadIfTeamRocketTookOver": "Было бы ужасно, если бы КОМАНДА R\\nзахватила СИЛФ или наших ПОКЕМОНОВ.$",
        "SilphCo_7F_Text_WowYouChasedOffTeamRocket": "Ух ты!\\pТы в одиночку прогнал\\nКОМАНДУ R?$",
        "SilphCo_7F_Text_ReallyDangerousHere": "Ты!\\nЗдесь очень опасно!\\pТы пришел меня спасти?\\nНо тебе нельзя сюда!$",
        "SilphCo_7F_Text_ThankYouSoMuch": "Огромное спасибо!$",
        "SilphCo_7F_Text_Grunt3Intro": "Ой-ой!\\nЧую маленькую мышь!$",
        "SilphCo_7F_Text_Grunt3Defeat": "Свет погас!$",
        "SilphCo_7F_Text_Grunt3PostBattle": "Так ты моего БОССА не найдешь,\\nсколько ни носись вокруг!$",
        "SilphCo_7F_Text_JoshuaIntro": "Хе-хе!\\pТы принял меня за сотрудника СИЛФ?$",
        "SilphCo_7F_Text_JoshuaDefeat": "С меня хватит!$",
        "SilphCo_7F_Text_JoshuaPostBattle": "Несмотря на возраст, ты\\nумелый ТРЕНЕР!$",
        "SilphCo_7F_Text_Grunt1Intro": "Я один из четырех\\nБРАТЬЕВ КОМАНДЫ R!$",
        "SilphCo_7F_Text_Grunt1Defeat": "А-а!\\nБратья, я проиграл!$",
        "SilphCo_7F_Text_Grunt1PostBattle": "Неважно.\\nМои братья отплатят тебе!$",
        "SilphCo_7F_Text_Grunt2Intro": "Ребенок проник внутрь?\\nЗначит, это ты!$",
        "SilphCo_7F_Text_Grunt2Defeat": "Ладно!\\nЯ проиграл!$",
        "SilphCo_7F_Text_Grunt2PostBattle": "Иди домой, пока мой БОСС\\nне разозлился!$",
        "SilphCo_7F_Text_RivalWhatKeptYou": "{RIVAL}: Где ты пропадал, {PLAYER}?$",
        "SilphCo_7F_Text_RivalIntro": "{RIVAL}: Ха-ха! Я знал, что ты\\nпоявишься, если подожду!\\pПохоже, КОМАНДА R тебя задержала!\\nНе то чтобы мне было дело!\\pЯ видел тебя в САФФРОНЕ и решил\\nпроверить, стал ли ты сильнее!$",
        "SilphCo_7F_Text_RivalDefeat": "Вот черт!\\nЗначит, ты уже готов к БОССУ\\lКОМАНДЫ R!$",
        "SilphCo_7F_Text_RivalPostBattle": "Ну что, {PLAYER}!\\nЯ двигаюсь дальше и выше!\\pГлядя в ПОКЕДЕКС, я уже понимаю,\\nкто силен и как они эволюционируют!\\pЯ гений или как?\\pЯ иду в ЛИГУ ПОКЕМОНОВ, чтобы\\nвышвырнуть ЭЛИТНУЮ ЧЕТВЕРКУ.\\pЯ стану сильнейшим\\nТРЕНЕРОМ в мире!\\pА тебе, {PLAYER}, удачи!\\nНе напрягайся!\\lЕще увидимся!$",
        "SilphCo_7F_Text_FloorSign": "ГЛАВНЫЙ ОФИС СИЛФ\\n7 ЭТАЖ$",
    },
    Path("data/maps/SaffronCity_Frlg/scripts.inc"): {
        "SaffronCity_Text_WhatDoYouWantGetLost": "Чего тебе?\\nПроваливай!$",
        "SaffronCity_Text_BossTakeTownForTeamRocket": "БОСС сказал, что заберет город\\nдля КОМАНДЫ R!$",
        "SaffronCity_Text_DontGetDefiantOrIllHurtYou": "Не дерзи!\\nА то мне придется тебя проучить!$",
        "SaffronCity_Text_SaffronBelongsToTeamRocket": "САФФРОН принадлежит КОМАНДЕ R!$",
        "SaffronCity_Text_CriminalLifeMakesMeFeelAlive": "Преступная жизнь заставляет меня\\nчувствовать себя живым!$",
        "SaffronCity_Text_WatchWhereYoureWalking": "Ай!\\nСмотри, куда идешь!$",
        "SaffronCity_Text_WeCanExploitMonsAroundWorld": "Когда СИЛФ под нашим контролем,\\nмы сможем использовать ПОКЕМОНОВ всего мира!\\pИ станем неприлично богаты! Ха-ха!$",
        "SaffronCity_Text_YouBeatTeamRocket": "Ты в одиночку победил КОМАНДУ R?\\nНевероятно!$",
        "SaffronCity_Text_SafeToGoOutAgain": "Да! КОМАНДА R ушла!\\nСнова можно спокойно выходить!$",
        "SaffronCity_Text_PeopleComingBackToSaffron": "Когда пришла КОМАНДА R, люди\\nтолпами бежали отсюда.\\pТеперь они должны вернуться\\nв САФФРОН.$",
        "SaffronCity_Text_FlewHereOnPidgeot": "Я прилетел сюда на PIDGEOT,\\nкогда прочитал про СИЛФ.\\pВсе уже закончилось?\\nЯ пропустил самое интересное...$",
        "SaffronCity_Text_Pidgeot": "PIDGEOT: Би-бибии!$",
        "SaffronCity_Text_SawRocketBossEscaping": "Я видел, как БОСС КОМАНДЫ R\\nубегал из здания СИЛФ.$",
        "SaffronCity_Text_ImASecurityGuard": "Я охранник.\\pПодозрительных детей я не пускаю!$",
        "SaffronCity_Text_HesTakingASnooze": "...\\nХр-р-р...\\pХа! Он просто дремлет!$",
        "SaffronCity_Text_CitySign": "САФФРОН\\nСияющий золотой центр торговли$",
        "SaffronCity_Text_FightingDojo": "БОЕВОЕ ДОДЗЕ$",
        "SaffronCity_Text_GymSign": "ГИМ ПОКЕМОНОВ САФФРОНА\\nЛИДЕР: САБРИНА\\lМастер ПОКЕМОНОВ типа PSYCHIC!$",
        "SaffronCity_Text_FullHealCuresStatus": "СОВЕТ ТРЕНЕРУ\\pПОЛНОЕ ЛЕЧЕНИЕ снимает ожог,\\nпаралич, отравление, заморозку и сон.\\pСтоит дороже, зато удобнее, чем\\nпокупать разные лекарства.$",
        "SaffronCity_Text_GreatBallImprovedCatchRate": "СОВЕТ ТРЕНЕРУ\\pНовый ГРЕЙТ-БОЛЛ заметно повышает\\nшанс поимки.\\pПопробуй его на ПОКЕМОНАХ,\\nкоторых трудно поймать.$",
        "SaffronCity_Text_SilphCoSign": "ОФИСНОЕ ЗДАНИЕ СИЛФ$",
        "SaffronCity_Text_MrPsychicsHouse": "ДОМ МИСТЕРА ПСИХИКА$",
        "SaffronCity_Text_SilphsLatestProduct": "Новейший продукт СИЛФ!\\nДата выпуска пока не определена...$",
        "SaffronCity_Text_TrainerFanClubSign": "ФАН-КЛУБ ТРЕНЕРОВ ПОКЕМОНОВ\\pНа этой табличке многие ТРЕНЕРЫ\\nнацарапали свои имена.$",
        "SaffronCity_Text_HowCanClubNotRecognizeLance": "Этот ФАН-КЛУБ...\\nЗдесь никто ничего не понимает!\\pКак можно не признать величие ЛЭНСА?\\pОн стоит за справедливость!\\nОн крут и при этом страстен!\\lЛЭНС - лучший!$",
    },
    Path("data/maps/SaffronCity_Gym_Frlg/scripts.inc"): {
        "SaffronCity_Gym_Text_AmandaIntro": "САБРИНА намного младше меня,\\nно заслужила мое уважение.$",
        "SaffronCity_Gym_Text_AmandaDefeat": "Недостаточно хорошо!$",
        "SaffronCity_Gym_Text_AmandaPostBattle": "В равном бою побеждает тот,\\nчья воля сильнее.\\pХочешь победить САБРИНУ -\\nсосредоточься и настройся на победу.$",
        "SaffronCity_Gym_Text_JohanIntro": "Тебя пугает наша невидимая сила?$",
        "SaffronCity_Gym_Text_JohanDefeat": "Я этого не предвидел!$",
        "SaffronCity_Gym_Text_JohanPostBattle": "ПОКЕМОНЫ типа PSYCHIC боятся\\nтолько призраков и жуков!$",
        "SaffronCity_Gym_Text_StacyIntro": "ПОКЕМОНЫ становятся похожи\\nна своих ТРЕНЕРОВ.\\pЗначит, твои ПОКЕМОНЫ крепкие!$",
        "SaffronCity_Gym_Text_StacyDefeat": "Я так и знала!$",
        "SaffronCity_Gym_Text_StacyPostBattle": "Мне еще многому учиться...\\pНужно освоить PSYCHIC и научить\\nэтому своих ПОКЕМОНОВ...$",
        "SaffronCity_Gym_Text_TyronIntro": "Ты ведь понимаешь?\\pОдной силы недостаточно, чтобы\\nпобеждать в мире ПОКЕМОНОВ?$",
        "SaffronCity_Gym_Text_TyronDefeat": "Не могу поверить!$",
        "SaffronCity_Gym_Text_TyronPostBattle": "САБРИНА только что разгромила\\nМАСТЕРА КАРАТЕ по соседству.$",
        "SaffronCity_Gym_Text_TashaIntro": "Ты и я - наши ПОКЕМОНЫ\\nсразятся!$",
        "SaffronCity_Gym_Text_TashaDefeat": "И все-таки я проиграла!$",
        "SaffronCity_Gym_Text_TashaPostBattle": "Я знала, что так и произойдет.$",
        "SaffronCity_Gym_Text_CameronIntro": "САБРИНА молода, но она\\nочень сильный ЛИДЕР.\\pДо нее тебе будет нелегко добраться!$",
        "SaffronCity_Gym_Text_CameronDefeat": "Ай!\\nЯ повержен!$",
        "SaffronCity_Gym_Text_CameronPostBattle": "Раньше в САФФРОНЕ было два\\nГИМА ПОКЕМОНОВ.\\pБОЕВОЕ ДОДЗЕ по соседству\\nлишилось статуса ГИМА.\\pКогда решили оставить один ГИМ,\\nмы просто разгромили их.$",
        "SaffronCity_Gym_Text_PrestonIntro": "ГИМ ПОКЕМОНОВ САФФРОНА известен\\nобучением экстрасенсов.\\pТы хочешь увидеть САБРИНУ, верно?\\nЯ это чувствую!$",
        "SaffronCity_Gym_Text_PrestonDefeat": "Ар-р-р!$",
        "SaffronCity_Gym_Text_PrestonPostBattle": "Именно! Я прочитал твои мысли\\nс помощью телепатии!$",
        "SaffronCity_Gym_Text_GymGuyAdvice": "Йо!\\nБудущий чемпион!\\pПОКЕМОНЫ САБРИНЫ используют\\nпсихическую силу вместо обычной.\\pПОКЕМОНЫ типа FIGHTING особенно\\nслабы против типа PSYCHIC.\\pИх уничтожат прежде, чем они\\nуспеют нанести удар!$",
        "SaffronCity_Gym_Text_GymGuyPostVictory": "Психическая сила, да?\\pБудь она у меня, я бы сорвал куш\\nна игровых автоматах!$",
        "SaffronCity_Gym_Text_GymStatue": "ГИМ ПОКЕМОНОВ САФФРОНА\\nЛИДЕР: САБРИНА\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}$",
        "SaffronCity_Gym_Text_GymStatuePlayerWon": "ГИМ ПОКЕМОНОВ САФФРОНА\\nЛИДЕР: САБРИНА\\pПОБЕДИВШИЕ ТРЕНЕРЫ:\\n{RIVAL}, {PLAYER}$",
    },
}

EXPECTED_COUNTS = {
    "data/maps/SilphCo_7F_Frlg/scripts.inc": 27,
    "data/maps/SaffronCity_Frlg/scripts.inc": 25,
    "data/maps/SaffronCity_Gym_Frlg/scripts.inc": 25,
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

    if total != 77:
        die(f"expected exactly 77 translated blocks, got {total}")

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
        "scope": "remaining English-only Silph 7F + Saffron City + Saffron Gym runtime text after v3.100",
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names remain English",
        "trainerDataTouched": False,
        "gameplayLogicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_saffron_silph_v3_101_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} runtime blocks across 3 files; Ash Bond/Ash Cap untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
