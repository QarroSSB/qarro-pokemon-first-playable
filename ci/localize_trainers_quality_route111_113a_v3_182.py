#!/usr/bin/env python3
"""Qarro v3.182: human-quality RU pass for trainer chunk 4.

Covers the next contiguous 100 machine-translated blocks in trainers.inc:
Route 111 through the opening of Route 113. Localization-only; exact runtime
control-token sequences are preserved and source drift fails closed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_TRAINERS_QUALITY_ROUTE111_113A_V3_182"
TARGET = Path("data/text/trainers.inc")

TRANSLATIONS = {
    "Route111_Text_DrewIntro": "О, привет! GO-GOGGLES тебе идут.\\nНо на мне они смотрятся лучше.\\pДавай выясним, кому они идут больше,\\nв бою!$",
    "Route111_Text_DrewDefeat": "Из-за GO-GOGGLES я не видел, что\\nпроисходит по сторонам.$",
    "Route111_Text_DrewPostBattle": "GO-GOGGLES позволяют идти\\nсквозь песчаную бурю.\\lВот за это я их и люблю!$",
    "Route111_Text_HeidiIntro": "Я устроила пикник прямо в пустыне.\\pЗдесь всегда найдется тренер,\\nтак что и сразиться можно!$",
    "Route111_Text_HeidiDefeat": "О-о-ох! Ну и жестоко!$",
    "Route111_Text_HeidiPostBattle": "Во время боя в песчаной буре\\nследи за HP своих POKeMON.\\pЕсли не смотреть за ними,\\nони могут потерять сознание!$",
    "Route111_Text_BeauIntro": "В этих GO-GOGGLES я\\nчувствую себя супергероем.\\lСейчас меня никто не победит!$",
    "Route111_Text_BeauDefeat": "Одной силы духа для победы мало...$",
    "Route111_Text_BeauPostBattle": "Когда-нибудь я стану настоящим героем.\\nБуду тренироваться еще усерднее, чтобы мы\\lс моим POKeMON стали сильнее.$",
    "Route111_Text_BeckyIntro": "Говорят, в пустыне можно найти\\nископаемые. Где же они?$",
    "Route111_Text_BeckyDefeat": "Мне совсем немного не хватило...$",
    "Route111_Text_BeckyPostBattle": "Если в пустыне находят ископаемые,\\nзначит, когда-то здесь было море.$",
    "Route111_Text_DustyIntro": "Тридцать лет я ищу\\nдревние руины!\\lИ ты бросаешь мне вызов?$",
    "Route111_Text_DustyDefeat": "Пока искал руины,\\nя совсем не искал сильных POKeMON.$",
    "Route111_Text_DustyPostBattle": "Тридцать лет я ищу\\nдревние руины!\\pНет, постой, может, сорок лет?\\nСколько же все-таки?$",
    "Route111_Text_DustyRegister": "Сильных POKeMON я вообще\\nне искал.\\pНо почему-то мне ужасно нравятся\\nPOKeNAV.$",
    "Route111_Text_DustyRematchIntro": "Тридцать лет я ищу\\nдревние руины!\\pНет, постой, может, сорок лет?\\nТак или иначе, сразимся?$",
    "Route111_Text_DustyRematchDefeat": "Ни руин не нашел, ни\\nсильных POKeMON...$",
    "Route111_Text_DustyPostRematch": "Тридцать лет я ищу\\nдревние руины!\\pНет, постой, может, уже сорок лет\\nищу?\\pХм... А может, даже пятьдесят...\\nСколько же времени прошло?$",
    "Route111_Text_TravisIntro": "Я полон энергии!\\nИ мой POKeMON тоже!$",
    "Route111_Text_TravisDefeat": "Мой POKeMON растерял весь запал...$",
    "Route111_Text_TravisPostBattle": "Когда вижу энергичного тренера,\\nневольно обращаю внимание.$",
    "Route111_Text_IreneIntro": "Не знаю, куда ты направляешься,\\nно, может, сразимся?$",
    "Route111_Text_IreneDefeat": "Ох, до чего же хорошо сражаешься!$",
    "Route111_Text_IrenePostBattle": "Думаю подняться на\\nГОРУ ЧИМНИ, но и вид\\lотсюда очень красивый.$",
    "Route111_Text_DaisukeIntro": "Чтобы стать сильнее, я вызываю всех,\\nкого встречаю!$",
    "Route111_Text_DaisukeDefeat": "Сдаюсь! Пощади!$",
    "Route111_Text_DaisukePostBattle": "Мне остается только тренироваться, пока\\nя не смогу победить таких тренеров,\\lкак ты.$",
    "Route111_Text_WiltonIntro": "Покажи, насколько сильнее стали\\nтвои POKeMON.$",
    "Route111_Text_WiltonDefeat": "Вижу, они стали\\nнамного сильнее.$",
    "Route111_Text_WiltonPostBattle": "POKeMON и тренеры многому учатся\\nв боях.\\pГлавное - никогда не сдаваться,\\nдаже после поражения.$",
    "Route111_Text_WiltonRegister": "У твоего стиля тренировок\\nесть чему поучиться.\\pПрошу о реванше, если\\nтебе будет угодно.$",
    "Route111_Text_WiltonRematchIntro": "Мы тренируемся здесь, чтобы поднять\\nсвое мастерство на новый уровень.\\lОставайся и тренируйся с нами!$",
    "Route111_Text_WiltonRematchDefeat": "О, неплохо!$",
    "Route111_Text_WiltonPostRematch": "С такой силой тебе стоит\\nнацелиться на ЛИГУ POKeMON.$",
    "Route111_Text_BrookeIntro": "О, твои POKeMON выглядят очень\\nсерьезными бойцами.\\lПридется пригласить тебя на бой.$",
    "Route111_Text_BrookeDefeat": "Они не просто выглядят сильными,\\nони и правда сильны!$",
    "Route111_Text_BrookePostBattle": "Я думала, что прилежно растила POKeMON,\\nно, похоже, впереди еще\\lочень много работы.$",
    "Route111_Text_BrookeRegister": "Хотелось бы подружиться с\\nбольшим числом сильных людей вроде тебя!$",
    "Route111_Text_BrookeRematchIntro": "POKeMON можно сделать сильнее или\\nслабее в зависимости от приемов,\\lкоторым их обучаешь.\\pКакие приемы знают твои POKeMON\\nсейчас?$",
    "Route111_Text_BrookeRematchDefeat": "Ты отлично подобрал им приемы!$",
    "Route111_Text_BrookePostRematch": "Может, мне стоило не давать моим\\nPOKeMON эволюционировать, пока они\\lне выучили лучшие приемы...$",
    "Route111_Text_CeliaIntro": "Не стоило приходить в такое\\nместо на пикник!$",
    "Route111_Text_CeliaDefeat": "Ох!\\nИ правда не стоило сюда приходить!$",
    "Route111_Text_CeliaPostBattle": "В такой песчаной буре я не могу устроить\\nпикник даже в своих\\lGO-GOGGLES...$",
    "Route111_Text_BryanIntro": "Насколько ты силен?\\nСейчас мы раскроем эту тайну!$",
    "Route111_Text_BryanDefeat": "Ох! Твоя сила!\\nОна окутана тайной!$",
    "Route111_Text_BryanPostBattle": "Эта пустыня скрывает тайны в\\nсвоих вечно движущихся песках!$",
    "Route111_Text_BrandenIntro": "Отдам тебе часть своего бутерброда,\\nесли проиграешь.$",
    "Route111_Text_BrandenDefeat": "Тц! Я думал, бутерброда будет\\nдостаточно в качестве взятки...$",
    "Route111_Text_BrandenPostBattle": "Мой SANDSHREW обожает\\nесть мои бутерброды.$",
    "Route111_Text_TyronIntro": "Вот мой любимый вид POKeMON!$",
    "Route111_Text_TyronDefeat": "Постой!\\nТы хорошо рассмотрел моего POKeMON?$",
    "Route111_Text_TyronPostBattle": "В бою я особенно люблю\\nпоказывать своего POKeMON.\\pДумаю, все чувствуют то же, когда\\nвступают в бой!$",
    "Route111_Text_CelinaIntro": "Покажи, как добавить немного острых ощущений\\nв мою жизнь.$",
    "Route111_Text_CelinaDefeat": "Ох... боже...\\nЭто было слишком волнующе.$",
    "Route111_Text_CelinaPostBattle": "Сердце до сих пор колотится.\\nТы потрясающий тренер.$",
    "Route111_Text_HaydenIntro": "Когда голоден так же сильно, как я,\\nна жалость места не остается!$",
    "Route111_Text_HaydenDefeat": "Уф...$",
    "Route111_Text_HaydenPostBattle": "Живот уже урчит!\\nМожет, поджарить несколько ягод...$",
    "Route111_Text_BiancaIntro": "Ты пришел из МОВИЛЛЯ?\\nТогда энергии у тебя должно быть полно!$",
    "Route111_Text_BiancaDefeat": "О-ля-ля!\\nВот это удар!$",
    "Route111_Text_BiancaPostBattle": "Эта дорога...\\nТебе еще очень далеко идти.$",
    "Route112_Text_BriceIntro": "Ха-ха-ха-ха!\\nНу что, устроим бой?\\lТы и я!\\lХа-ха-ха-ха!$",
    "Route112_Text_BriceDefeat": "Я проиграл!\\nХа-ха-ха-ха!$",
    "Route112_Text_BricePostBattle": "Ха-ха-ха! Что-то залетело мне в нос!\\nХа-ха-ха-апчхи!$",
    "Route112_Text_TrentIntro": "Мои ноги стали крепкими от постоянных\\nподъемов и спусков в горах.\\pТак просто они не подкосятся,\\nдружище!$",
    "Route112_Text_TrentDefeat": "Ай! Ноги свело судорогой!$",
    "Route112_Text_TrentPostBattle": "Попробуй ходить по этим горным тропам,\\nпо-настоящему много ходить,\\lс тяжелым рюкзаком весом в десятки\\lфунтов.\\pВот тогда, дружище, твое тело\\nстанет по-настоящему крепким.$",
    "Route112_Text_TrentRegister": "Ай, ноги свело.\\nДостанешь бинты из\\lмоего рюкзака?\\pНет, это мой POKeNAV!\\nЛадно, тогда запишу тебя.$",
    "Route112_Text_TrentRematchIntro": "Я поддерживаю форму походами.\\nСилы у меня хоть отбавляй!$",
    "Route112_Text_TrentRematchDefeat": "Меня превзошли в силе?$",
    "Route112_Text_TrentRematchPostBattle": "Говорят, на вершине ГОРЫ ЧИМНИ есть\\nпо-настоящему сильные тренеры.\\pЯ собираюсь подняться туда и бросить им\\nвызов!$",
    "Route112_Text_LarryIntro": "Я сильный.\\nЕсли проиграю, плакать не буду.$",
    "Route112_Text_LarryDefeat": "А-а-а-а!$",
    "Route112_Text_LarryPostBattle": "Я плачу не потому, что скучаю по маме!\\nШмыг...$",
    "Route112_Text_CarolIntro": "На пикнике просто невозможно\\nне петь!\\lДавай, пой вместе со мной!$",
    "Route112_Text_CarolDefeat": "Ох, какая сила!$",
    "Route112_Text_CarolPostBattle": "Неважно, хорошо ты поешь или играешь\\nв POKeMON.\\pКто веселится больше всех, тот и победил!$",
    "Route112_Text_BryantIntro": "Я поймал горячего POKeMON на ОГНЕННОЙ ТРОПЕ!\\nСмотри!$",
    "Route112_Text_BryantDefeat": "Вот это была тряска!$",
    "Route112_Text_BryantPostBattle": "Мне нравится, как ты сражаешься.\\nВ этом есть свой стиль.$",
    "Route112_Text_ShaylaIntro": "Ох, какой очаровательный тренер!\\nМне просто нужен романтичный бой!\\lЯ и сама неплоха!$",
    "Route112_Text_ShaylaDefeat": "Ох, какая сила!\\nВот это ты меня удивил!$",
    "Route112_Text_ShaylaPostBattle": "Ты сейчас занят?\\nЯ подумала, что мы могли бы\\lпрямо сейчас устроить реванш...\\lНо если занят, ничего страшного.$",
    "Route113_Text_JaylenIntro": "Угадаешь, почему здесь так\\nпрохладно?$",
    "Route113_Text_JaylenDefeat": "Фу-у!\\nНу и вонь!$",
    "Route113_Text_JaylenPostBattle": "Вулканический пепел заслоняет солнце,\\nпоэтому здесь не слишком жарко.\\pДля меня идеально - терпеть не могу жару!$",
    "Route113_Text_DillonIntro": "Извержение вулкана доказывает, что\\nземля живая.$",
    "Route113_Text_DillonDefeat": "Вот это у тебя сила!$",
    "Route113_Text_DillonPostBattle": "Ай! Ай-ай! Ничего не вижу!\\nПепел попал на ресницы!\\pПонял? Пепел и ресницы?\\pЛадно, шутка плохая, извини...$",
    "Route113_Text_MadelineIntro": "Этим зонтиком я защищаю от\\nмерзкого вулканического пепла\\lмоего дорогого NUMEL.$",
    "Route113_Text_MadelineDefeat": "Фух, фух...\\nЯ совсем выдохлась...$",
    "Route113_Text_MadelinePostBattle": "Ты очень хорошо сражаешься.\\nДолжна признать, я впечатлена!$",
    "Route113_Text_MadelineRegister": "Иди под мой зонтик.\\nЯ запишу тебя в свой POKeNAV.$",
    "Route113_Text_MadelineRematchIntro": "О, привет! Давно не виделись.\\nМожно пригласить тебя на бой?$",
    "Route113_Text_MadelineRematchDefeat": "Ох, великолепно!$",
    "Route113_Text_MadelinePostRematch": "Ты по-прежнему прекрасно сражаешься.\\nДолжна признать, я впечатлена!$",
    "Route113_Text_LaoIntro": "Я выскакиваю прямо из пепла! Хия!\\nБросаю тебе вызов!$",
    "Route113_Text_LaoDefeat": "С честью признаю поражение!$",
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
        raise SystemExit("usage: localize_trainers_quality_route111_113a_v3_182.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise FileNotFoundError(path)
    if len(TRANSLATIONS) != 100:
        raise RuntimeError(f"expected exactly 100 quality-pass blocks, got {len(TRANSLATIONS)}")
    for label, translated in TRANSLATIONS.items():
        replace_label(path, label, translated)

    out = root / "build" / "qarro_ru_trainers_quality_route111_113a_v3_182_audit.json"
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
