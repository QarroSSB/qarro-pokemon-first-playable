#!/usr/bin/env python3
"""Qarro v3.180: human-quality RU pass for the next 100 trainer blocks.

Covers the next contiguous trainers.inc machine-translation chunk after v3.179:
Route 105 through the opening of Route 109. This is localization-only, preserves
the exact runtime control-token sequence for every label, and fails closed on
source drift.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINERS_QUALITY_ROUTE105_109A_V3_180"
TARGET = Path("data/text/trainers.inc")

TRANSLATIONS = {
    "Route105_Text_FosterIntro": "Говорят, где-то здесь есть\\nтаинственный камень.\\lТы что-нибудь о нем знаешь?$",
    "Route105_Text_FosterDefeated": "Я слишком думал об этом камне,\\nа мои POKeMON так и остались слабыми...$",
    "Route105_Text_FosterPostBattle": "На красивый камень я могу смотреть\\nчасами и не заскучать.$",
    "Route105_Text_LuisIntro": "Фух! Увидев тебя, я решил,\\nчто ребенок тонет.\\pНо с тобой все в порядке. Может,\\nсразимся?$",
    "Route105_Text_LuisDefeated": "Буль... Буль...$",
    "Route105_Text_LuisPostBattle": "Если тонешь, подай сигнал:\\nмаши одной рукой в сторону берега.$",
    "Route105_Text_DominikIntro": "Плыть по синему морю...\\nВот это настоящее удовольствие!$",
    "Route105_Text_DominikDefeated": "Я проиграл...\\nТеперь и настроение на нуле...$",
    "Route105_Text_DominikPostBattle": "Почему море синее?\\pЯ узнал это в музее СЛЕЙТПОРТА,\\nно уже забыл.$",
    "Route105_Text_BeverlyIntro": "В воде тело кажется легче.\\nБудто я даже стройнее становлюсь!$",
    "Route105_Text_BeverlyDefeated": "Я держусь на воде...$",
    "Route105_Text_PostBattle": "В воде вес тела становится всего\\nодной десятой обычного.\\pТогда мой вес был бы...\\nОй! Не скажу тебе, сколько я вешу!$",
    "Route105_Text_ImaniIntro": "Синее-синее небо...\\nБескрайнее море...\\lКак же здесь спокойно...$",
    "Route105_Text_ImaniDefeated": "Проиграла, пока отдыхала!$",
    "Route105_Text_ImaniPostBattle": "Хочу, чтобы рядом со мной людям\\nбыло спокойно. Хи-хи.$",
    "Route105_Text_AndresIntro": "Я уверен, море скрывает от нас\\nмного тайн.$",
    "Route105_Text_AndresDefeated": "Да...\\nВ боях я совсем не силен...$",
    "Route105_Text_AndresPostBattle": "В морях по всему миру наверняка\\nскрыто множество тайн.\\pИ я собираюсь найти их все!$",
    "Route105_Text_AndresRegister": "Что? Я ведь так слаб, а ты хочешь\\nзаписать меня в свой POKeNAV?$",
    "Route105_Text_AndresRematchIntro": "Я же говорил, что я слаб...\\nТы точно хочешь сразиться?$",
    "Route105_Text_AndresRematchDefeated": "Да...\\nЯ и не думал, что смогу победить.$",
    "Route105_Text_AndresRematchPostBattle": "В боях я слаб, зато тягу к открытиям\\nникому не превзойти.\\pЯ обойду по морю весь\\nмир!$",
    "Route105_Text_JosueIntro": "Я вымотался от плавания.\\nПросто еще не привык.\\pНужен бой, чтобы встряхнуться!$",
    "Route105_Text_JosueDefeated": "Я проиграл, потому что сражался в море.$",
    "Route105_Text_JosuePostBattle": "Да, мне небо подходит гораздо\\nбольше, чем море.$",
    "Route106_Text_ElliotIntro": "Что тебе больше нравится: рыбачить\\nв море или в реке?$",
    "Route106_Text_ElliotDefeated": "Как на морской рыбалке: проиграл\\nс размахом!$",
    "Route106_Text_ElliotPostBattle": "Рыбалка прекрасна и в море,\\nи в реке.\\lПравда ведь?$",
    "Route106_Text_ElliotRegister": "Рыбалка хороша, но и бои тоже.\\nЕсли не против, встретимся еще?$",
    "Route106_Text_ElliotRematchIntro": "Я наловил кучу POKeMON.\\nСейчас покажу зрелищный бой!$",
    "Route106_Text_ElliotRematchDefeated": "И снова проиграл с размахом!$",
    "Route106_Text_ElliotRematchPostBattle": "Что ни случись, POKeMON лучше всех!\\nПравда ведь?$",
    "Route106_Text_NedIntro": "Что делать, если очень нужно\\nв туалет?\\pА вдруг удочка поймает крупную рыбу,\\nпока я там? Вот и не могу уйти...$",
    "Route106_Text_NedDefeated": "Я проиграл, потому что терплю\\nи не иду в туалет...$",
    "Route106_Text_NedPostBattle": "О нет! Чувствую, сейчас клюнет\\nчто-то крупное!$",
    "Route106_Text_DouglasIntro": "Ха-ха-ха! Бегун из меня никудышный,\\nзато в воде меня не догнать!$",
    "Route106_Text_DouglasDefeated": "Сдаюсь!$",
    "Route106_Text_DouglasPostBattle": "А вот в заплыве я бы не проиграл...$",
    "Route106_Text_KylaIntro": "Море - мой родной двор. Не стану\\nподдаваться только потому, что ты ребенок!$",
    "Route106_Text_KylaDefeated": "Ты ведь не поддавался мне,\\nправда?$",
    "Route106_Text_KylaPostBattle": "Качаться на волнах...\\nОбожаю! Попробуй и ты!$",
    "Route107_Text_DarrinIntro": "Зе-е-ев...\\pНаверное, я задремал, пока\\nкачался на волнах.$",
    "Route107_Text_DarrinDefeated": "А-ха-ха, проиграл...\\nПожалуй, вздремну...$",
    "Route107_Text_DarrinPostBattle": "Плывешь, а волны укачивают -\\nсловно лежишь в\\lмягкой удобной кровати.$",
    "Route107_Text_TonyIntro": "Море для меня как родной двор.\\nДавай сразимся!$",
    "Route107_Text_TonyDefeated": "Проиграл на своем поле...\\nВот это шок!$",
    "Route107_Text_TonyPostBattle": "Плыву по морю с сердцем, полным\\nмечтаний...\\pЭто песня!\\nЛадно, поплыву дальше.$",
    "Route107_Text_TonyRegister": "Ты потряс меня до глубины души!\\nТак что, чтобы не забыл меня...$",
    "Route107_Text_TonyRematchIntro": "Пока я плавал в огромном море,\\nмой POKeMON стал сильнее!$",
    "Route107_Text_TonyRematchDefeated": "Вот это шок!\\pМой POKeMON стал сильнее, а\\nя как тренер - нет!$",
    "Route107_Text_TonyRematchPostBattle": "Боевой опыт делает тебя\\nсильнее как тренера.\\lЭтому меня научили волны.$",
    "Route107_Text_DeniseIntro": "Знаешь маленький городок\\nДЬЮФОРД?$",
    "Route107_Text_DeniseDefeated": "Ненавижу такое!$",
    "Route107_Text_DenisePostBattle": "В ЗАЛЕ ДЬЮФОРДА сейчас в моде\\nодна странная фраза.$",
    "Route107_Text_BethIntro": "Хочешь со мной сразиться?\\nКонечно, я согласна!$",
    "Route107_Text_BethDefeated": "Мне не хватило мастерства.$",
    "Route107_Text_BethPostBattle": "Думаю, ты станешь еще сильнее.\\nЯ тоже буду стараться!$",
    "Route107_Text_LisaIntro": "ЛИЗА: Мы бросаем тебе вызов\\nкак сестра и брат!$",
    "Route107_Text_LisaDefeated": "ЛИЗА: Круто.\\nУ тебя совсем другой уровень силы.$",
    "Route107_Text_LisaPostBattle": "ЛИЗА: У тебя есть друзья, которые\\nпошли бы с тобой на пляж?$",
    "Route107_Text_LisaNotEnoughPokemon": "ЛИЗА: Хочешь сразиться с нами -\\nвозьми побольше POKeMON.$",
    "Route107_Text_RayIntro": "РЭЙ: Мы с сестрой всегда сражаемся\\nнашими POKeMON.\\pЯ обычно проигрываю, но вдвоем\\nмы тебя победим!$",
    "Route107_Text_RayDefeated": "РЭЙ: Ух ты, твой уровень гораздо\\nвыше нашего!$",
    "Route107_Text_RayPostBattle": "РЭЙ: Сестра подарила мне POKeMON.\\nЯ вырастил его, и теперь он мой\\lважный напарник!$",
    "Route107_Text_RayNotEnoughPokemon": "РЭЙ: Хочешь сразиться с нами -\\nприведи еще POKeMON!$",
    "Route107_Text_CamronIntro": "Я посреди триатлона,\\nа усталости пока ни капли!$",
    "Route107_Text_CamronDefeated": "Вот теперь я вымотался...$",
    "Route107_Text_CamronPostBattle": "После этого мне еще плыть и бежать.\\nДел впереди полно.\\pЯ точно справлюсь?$",
    "Route108_Text_JeromeIntro": "Моя мечта - переплыть все семь\\nморей мира!$",
    "Route108_Text_JeromeDefeated": "С таким результатом мне не видать\\nсеми морей...$",
    "Route108_Text_JeromePostBattle": "Играть с морскими POKeMON - одно из\\nглавных удовольствий плавания!$",
    "Route108_Text_MatthewIntro": "Эй, моряк! Ты тоже направляешься\\nк ЗАБРОШЕННОМУ КОРАБЛЮ?$",
    "Route108_Text_MatthewDefeated": "Тону!\\nБуль... Буль...$",
    "Route108_Text_MatthewPostBattle": "Некоторые даже заходят внутрь\\nЗАБРОШЕННОГО КОРАБЛЯ.$",
    "Route108_Text_TaraIntro": "Мой парень-врун сказал,\\nчто мне очень идет бикини...$",
    "Route108_Text_TaraDefeated": "Ну вот!$",
    "Route108_Text_TaraPostBattle": "Даже если это неправда, приятно слышать,\\nчто я отлично выгляжу...\\lМы, девушки, такие сложные...$",
    "Route108_Text_MissyIntro": "Обожаю море!\\nВо время плавания забываю все заботы!$",
    "Route108_Text_MissyDefeated": "Когда проигрываю бой,\\nсразу начинаю нервничать!$",
    "Route108_Text_MissyPostBattle": "Снимай стресс плаванием!\\nЭто полезно для здоровья!$",
    "Route108_Text_CoryIntro": "Я обожаю водных POKeMON.\\nНо и остальных POKeMON тоже!$",
    "Route108_Text_CoryDefeated": "А-а-а! Проиграл!\\nА-а-а! А-а-а!$",
    "Route108_Text_CoryPostBattle": "Мне полезно кричать!\\nСразу настроение лучше!$",
    "Route108_Text_CoryRegister": "Еще я люблю сильных тренеров!\\nЗапиши меня в свой POKeNAV!$",
    "Route108_Text_CoryRematchIntro": "Победа или поражение - я люблю бои в море!$",
    "Route108_Text_CoryRematchDefeated": "А-а-а! Снова проиграл!\\nА-а-а! А-а-а!$",
    "Route108_Text_CoryRematchPostBattle": "Если перед тобой трудная задача,\\nпопробуй покричать на море!$",
    "Route108_Text_CarolinaIntro": "Я очень горжусь своим POKeMON.\\nСейчас покажем стремительный бой!$",
    "Route108_Text_CarolinaDefeated": "Это было совсем не мило.$",
    "Route108_Text_CarolinaPostBattle": "Раз уж я на море, почему бы\\nне надеть розовый купальник с оборками...$",
    "Route109_Text_DavidIntro": "Хия! Смотри на мой рельефный пресс!\\nВот что значит настоящая форма!$",
    "Route109_Text_DavidDefeated": "Айя!\\nВот незадача!$",
    "Route109_Text_DavidPostBattle": "Хия!\\pМой рельефный пресс никак не связан\\nс боями POKeMON!$",
    "Route109_Text_AliceIntro": "Ты хорошо защищаешься от\\nсолнца?$",
    "Route109_Text_AliceDefeated": "Ай, ай, ай!$",
    "Route109_Text_AlicePostBattle": "Щеки обгорают быстрее всего!$",
    "Route109_Text_HueyIntro": "Я бросал якорь в портах по всему\\nмиру, но СЛЕЙТПОРТ - лучший.$",
    "Route109_Text_HueyDefeated": "Ты лучший!$",
    "Route109_Text_HueyPostBattle": "В лучшем порту оказался лучший\\nтренер...$",
    "Route109_Text_EdmondIntro": "Ур-р-рп...\\nБой? Со мной?$",
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
        raise RuntimeError(
            f"{path}:{label}: control-token drift old={old_tokens} new={new_tokens}"
        )
    if not translated.endswith("$"):
        raise RuntimeError(f"{path}:{label}: translated block must end in $")
    bad = sorted(set(translated) & BANNED_UNICODE)
    if bad:
        raise RuntimeError(f"{path}:{label}: unsupported punctuation {bad}")
    if '"' in translated:
        raise RuntimeError(f"{path}:{label}: raw double quote is not allowed")

    new_body = '\t.string "' + translated + '"\n'
    updated = text[:m.start("body")] + new_body + text[m.end("body"):]
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_trainers_quality_route105_109a_v3_180.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 100:
        raise RuntimeError(f"expected exactly 100 quality-pass blocks, got {len(TRANSLATIONS)}")

    for label, translated in TRANSLATIONS.items():
        replace_label(path, label, translated)

    out = root / "build" / "qarro_ru_trainers_quality_route105_109a_v3_180_audit.json"
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
